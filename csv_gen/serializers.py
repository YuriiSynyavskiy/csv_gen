from rest_framework import serializers
from .models import Schema, Column, Dataset
from django.contrib.auth.models import User


class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username']


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = '__all__'


class SchemaSerializer(serializers.ModelSerializer):
    columns = ColumnSerializer(many=True, read_only=True)
    datasets = DatasetSerializer(many=True, read_only=True)

    class Meta:
        model = Schema
        fields = ['id', 'name', 'columns', 'user',
                  'modified_date', 'delimeter', 'quote', 'datasets']
