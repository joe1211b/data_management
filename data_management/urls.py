from django.urls import path
from api.views import CreateTableView, AddColumnView, DeleteTableView,InsertRecordView, GetRecordsView, UpdateRecordView, DeleteRecordView, UploadCSVView

urlpatterns = [
    path('api/create-table/', CreateTableView.as_view(), name='create_table'),
    path('api/add-column/', AddColumnView.as_view(), name='add_column'),
    path('api/delete-table/', DeleteTableView.as_view(), name='delete_table'),
    path('api/insert-record/', InsertRecordView.as_view(), name='insert_record'),
    path('api/get-records/', GetRecordsView.as_view(), name='get_records'),
    path('api/update-record/', UpdateRecordView.as_view(), name='update_record'),
    path('api/delete-record/', DeleteRecordView.as_view(), name='delete_record'),
    path('api/upload-csv/', UploadCSVView.as_view(), name='upload_csv'),
]
