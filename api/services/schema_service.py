from django.db import connection

class SchemaService:
    
    @staticmethod
    def create_table(table_name, fields):
        """
        Creates a table dynamically based on user-defined fields.
        Example: create_table("Customer", {"name": "TEXT", "email": "TEXT UNIQUE", "created_at": "DATE"})
        """
        field_definitions = ", ".join([f"{name} {dtype}" for name, dtype in fields.items()])
        sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({field_definitions});"
        
        with connection.cursor() as cursor:
            cursor.execute(sql)
    
    @staticmethod
    def add_column(table_name, column_name, column_type):
        """
        Adds a new column to an existing table.
        Example: add_column("Customer", "phone_number", "TEXT")
        """
        sql = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type};"
        
        with connection.cursor() as cursor:
            cursor.execute(sql)
    
    @staticmethod
    def delete_table(table_name):
        """
        Deletes a table.
        Example: delete_table("Customer")
        """
        sql = f"DROP TABLE IF EXISTS {table_name};"
        
        with connection.cursor() as cursor:
            cursor.execute(sql)
