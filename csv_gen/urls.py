from .views import ListSchemaApi, SchemaApi, ColumnAPI, ListColumnAPI, UserAPI, DataSetAPI, DownloadCSV
from django.urls import path


urlpatterns = [
    path('schema/list', ListSchemaApi.as_view()),
    path('schema/<int:id>', SchemaApi.as_view()),
    path('schema/', SchemaApi.as_view()),
    path('column/<int:id>', ColumnAPI.as_view()),
    path('column/', ColumnAPI.as_view()),
    path('column/list', ListColumnAPI.as_view()),
    path('user/', UserAPI.as_view()),
    path('dataset/', DataSetAPI.as_view()),
    path('dataset/download/<int:id>', DownloadCSV, name='download_csv')
]
