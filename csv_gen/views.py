import json
import os
from .serializers import SchemaSerializer, ColumnSerializer, UserSerializer, DatasetSerializer
from django.core import serializers
from .models import Schema, Column, Dataset
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework.authtoken.models import Token
from .tasks import generate_csv
from django.core.files import File
from django.http import HttpResponse
from rest_framework.decorators import api_view
from .tasks import DATASET_PATH
from django.conf import settings


class SchemaApi(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, pk):
        try:
            return Schema.objects.get(id=pk)
        except Schema.DoesNotExist:
            raise Http404

    def get_user(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            raise Http404

    def get(self, request):
        schema = self.get_object(request.query_params['id'])
        serializer = SchemaSerializer(schema)
        serializer.data['columns'].sort(key=lambda column: column['order'])
        return Response(serializer.data)

    def post(self, request):
        for column in request.data.get('columns', ""):
            if column.get("from", None) and column.get("to", None):
                col_filter = {
                    "from": column["from"],
                    "to": column["to"]
                }
            elif column.get('length', None):
                col_filter = {
                    "length": column["length"]
                }
            else:
                col_filter = ''
            column['col_filter'] = col_filter
        try:
            request.data["delimeter"] = [p[0] for p in Schema._meta.get_field(
                'delimeter').choices if p[1] == request.data["delimeter"]][0]
            request.data["quote"] = [p[0] for p in Schema._meta.get_field(
                'quote').choices if p[1] == request.data["quote"]][0]
        except IndexError:
            pass
        request.data['user'] = request.user.id
        serializer = SchemaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            for column in request.data.get('columns', []):
                column['schema'] = serializer.data['id']
                column_serializer = ColumnSerializer(data=column)
                if column_serializer.is_valid():
                    column_serializer.save()
            new_schema = SchemaSerializer(
                self.get_object(serializer.data['id']))
            return Response(new_schema.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        request.data['user'] = request.user.id
        for new_column in request.data['columns']:
            if new_column.get("from", None) and new_column.get("to", None):
                col_filter = {
                    "from": new_column["from"],
                    "to": new_column["to"]
                }
            elif new_column.get('length', None):
                col_filter = {
                    "length": new_column["length"]
                }
            else:
                col_filter = ''
            new_column['col_filter'] = col_filter
        try:
            request.data["delimeter"] = [p[0] for p in Schema._meta.get_field(
                'delimeter').choices if p[1] == request.data["delimeter"]][0]
            request.data["quote"] = [p[0] for p in Schema._meta.get_field(
                'quote').choices if p[1] == request.data["quote"]][0]
        except IndexError:
            pass

        schema = Schema.objects.get(id=request.data['id'])
        schema.name = request.data['name']
        schema.delimeter = request.data['delimeter']
        schema.quote = request.data['quote']
        schema.save()
        # Compare new columns with previous
        for curr_column in schema.columns.all():
            if curr_column.id not in [item.get("id", "") for item in request.data['columns']]:
                curr_column.delete()
        for new_column in request.data['columns']:
            if new_column.get("id", None):
                upd_column = Column.objects.get(id=new_column['id'])
                upd_column.col_filter = new_column["col_filter"]
                upd_column.name = new_column["name"]
                upd_column.order = new_column["order"]
                upd_column.col_type = new_column["col_type"]
            else:
                upd_column = Column.objects.create(col_filter=new_column["col_filter"],
                                                   name=new_column["name"],
                                                   schema=schema,
                                                   order=new_column["order"],
                                                   col_type=new_column["col_type"])
            upd_column.save()
        new_schema = SchemaSerializer(self.get_object(schema.id))
        return Response(new_schema.data, status=status.HTTP_200_OK)

    def delete(self, request):
        schema = self.get_object(request.data['id'])
        schema.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListSchemaApi(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, user_id):
        try:
            return User.objects.get(id=user_id).schemas
        except User.DoesNotExist:
            raise Http404

    def get(self, request):
        schemas = self.get_object(request.user.id)
        serializer = SchemaSerializer(schemas, many=True)
        return Response(serializer.data)


class ColumnAPI(APIView):
    def get_object(self, pk):
        try:
            return Column.objects.get(id=pk)
        except Column.DoesNotExist:
            raise Http404

    def get(self, request):
        column = self.get_object(request.query_params['id'])
        serializer = ColumnSerializer(column)
        return Response(serializer.data)

    def post(self, request):
        serializer = ColumnSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        column = self.get_object(request.data['id'])
        serializer = ColumnSerializer(column, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, schema_id):
        column = self.get_object(request.data['id'])
        column.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListColumnAPI(APIView):
    """
    Available columns types
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        choices = Column.Type.choices
        return Response([p[0] for p in choices])


class UserAPI(APIView):
    """
    Exchange token for user object
    """

    def get(self, request):
        user_id = Token.objects.get(key=request.auth.key).user_id
        user = User.objects.get(id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class DataSetAPI(APIView):
    """
    Generate fake data
    """

    def get(self, request):
        dataset = Dataset.objects.get(id=request.query_params['id'])
        resp = {
            'id': dataset.id,
            'created_at': dataset.created_at,
            'status': dataset.status,
            'line_status': settings.REDIS_CONN.get(str(dataset.id)) or dataset.rows,
            'rows': dataset.rows,
        }
        return Response(resp)

    def post(self, request):
        serializer = DatasetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        schema = Schema.objects.get(id=serializer.data['schema'])
        schema_serializer = SchemaSerializer(schema)
        task = generate_csv.delay(serializer.data,
                                  schema_serializer.data)
        context = {
            'task_id': task.id,
            'task_status': task.status
        }
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def DownloadCSV(self, id):
    dataset = Dataset.objects.get(id=id)
    if not dataset.status == "Ready":
        raise Http404
    path_to_file = DATASET_PATH.format(id=dataset.id)
    s3_file = open(path_to_file, 'wb')
    settings.S3_CLIENT.download_fileobj(
        os.environ["S3_BUCKET"], path_to_file, s3_file)
    f = open(path_to_file, 'rb')
    csv_file = File(f)
    response = HttpResponse(csv_file.read())
    response['Content-Disposition'] = 'attachment; filename="report.csv"'
    response['Content-Type'] = 'text/csv'
    return response
