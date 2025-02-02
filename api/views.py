from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.services.schema_service import SchemaService
from api.services.crud_service import CRUDService
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from api.tasks import process_csv_import

class CreateTableView(APIView):
    def post(self, request):
        """
        API to create a table dynamically.
        Expected JSON:
        {
            "table_name": "Customer",
            "fields": {
                "name": "TEXT",
                "email": "TEXT UNIQUE",
                "created_at": "DATE"
            }
        }
        """
        try:
            table_name = request.data.get("table_name")
            fields = request.data.get("fields")

            if not table_name or not fields:
                return Response({"error": "Table name and fields are required"}, status=status.HTTP_400_BAD_REQUEST)

            SchemaService.create_table(table_name, fields)
            return Response({"message": f"Table {table_name} created successfully"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AddColumnView(APIView):
    def post(self, request):
        """
        API to add a column to an existing table.
        Expected JSON:
        {
            "table_name": "Customer",
            "column_name": "phone_number",
            "column_type": "TEXT"
        }
        """
        try:
            table_name = request.data.get("table_name")
            column_name = request.data.get("column_name")
            column_type = request.data.get("column_type")

            if not table_name or not column_name or not column_type:
                return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

            SchemaService.add_column(table_name, column_name, column_type)
            return Response({"message": f"Column {column_name} added to {table_name} successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DeleteTableView(APIView):
    def delete(self, request):
        """
        API to delete a table.
        Expected JSON:
        {
            "table_name": "Customer"
        }
        """
        try:
            table_name = request.data.get("table_name")

            if not table_name:
                return Response({"error": "Table name is required"}, status=status.HTTP_400_BAD_REQUEST)

            SchemaService.delete_table(table_name)
            return Response({"message": f"Table {table_name} deleted successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class InsertRecordView(APIView):
    def post(self, request):
        """
        API to insert a new record into a table.
        Expected JSON:
        {
            "table_name": "Customer",
            "data": {
                "name": "John",
                "email": "john@example.com",
                "created_at": "2024-02-01"
            }
        }
        """
        try:
            table_name = request.data.get("table_name")
            data = request.data.get("data")

            if not table_name or not data:
                return Response({"error": "Table name and data are required"}, status=status.HTTP_400_BAD_REQUEST)

            result = CRUDService.insert_record(table_name, data)
            return Response({"message": "Record inserted successfully", "data": result}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetRecordsView(APIView):
    def get(self, request):
        """
        API to retrieve records from a table with optional filters, search, pagination, and sorting.
        URL Parameters:
        - table_name (required)
        - filters (JSON object as string)
        - search (string)
        - page (int, default 1)
        - limit (int, default 10)
        - order_by (string, default "id")
        - order_direction (ASC/DESC)
        """
        try:
            table_name = request.GET.get("table_name")
            filters = request.GET.get("filters")
            search = request.GET.get("search")
            page = int(request.GET.get("page", 1))
            limit = int(request.GET.get("limit", 10))
            order_by = request.GET.get("order_by", "id")
            order_direction = request.GET.get("order_direction", "ASC")

            if filters:
                import json
                filters = json.loads(filters)

            results = CRUDService.get_records(table_name, filters, search, page, limit, order_by, order_direction)
            return Response({"data": results}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UpdateRecordView(APIView):
    def put(self, request):
        """
        API to update a record.
        Expected JSON:
        {
            "table_name": "Customer",
            "id": 1,
            "data": {"name": "Jane Doe"}
        }
        """
        try:
            table_name = request.data.get("table_name")
            record_id = request.data.get("id")
            data = request.data.get("data")

            if not table_name or not record_id or not data:
                return Response({"error": "Table name, record ID, and data are required"}, status=status.HTTP_400_BAD_REQUEST)

            result = CRUDService.update_record(table_name, record_id, data)
            if result:
                return Response({"message": "Record updated successfully", "data": result}, status=status.HTTP_200_OK)
            return Response({"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DeleteRecordView(APIView):
    def delete(self, request):
        """
        API to delete a record.
        Expected JSON:
        {
            "table_name": "Customer",
            "id": 1
        }
        """
        try:
            table_name = request.data.get("table_name")
            record_id = request.data.get("id")

            if not table_name or not record_id:
                return Response({"error": "Table name and record ID are required"}, status=status.HTTP_400_BAD_REQUEST)

            deleted_id = CRUDService.delete_record(table_name, record_id)
            if deleted_id:
                return Response({"message": "Record deleted successfully"}, status=status.HTTP_200_OK)
            return Response({"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class UploadCSVView(APIView):
    def post(self, request):
        """
        API to upload a CSV file for bulk import.
        Expected form-data:
        - file: CSV file
        - table_name: Target table for import
        - email: User email for notification
        """
        try:
            file = request.FILES.get("file")
            table_name = request.data.get("table_name")
            user_email = request.data.get("email")

            if not file or not table_name or not user_email:
                return Response({"error": "File, table_name, and email are required"}, status=status.HTTP_400_BAD_REQUEST)

            file_path = f"uploads/{file.name}"
            default_storage.save(file_path, ContentFile(file.read()))

            # Trigger async processing
            process_csv_import.delay(file_path, table_name, user_email)

            return Response({"message": "File uploaded successfully, processing started."}, status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
