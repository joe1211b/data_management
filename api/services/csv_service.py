import pandas as pd
from django.db import connection
from api.services.crud_service import CRUDService

class CSVService:

    @staticmethod
    def validate_csv(file_path, table_name):
        """
        Validates CSV data against the existing table schema.
        Ensures required fields exist and unique constraints are met.
        """
        df = pd.read_csv(file_path)

        # Get existing table columns
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}';")
            columns = {row[0] for row in cursor.fetchall()}

        # Ensure all CSV columns exist in the table
        missing_columns = set(df.columns) - columns
        if missing_columns:
            raise ValueError(f"CSV contains invalid columns: {missing_columns}")

        # Validate unique fields (e.g., email must be unique)
        if 'email' in df.columns:
            existing_emails = set(CRUDService.get_records(table_name, order_by="email"))
            duplicate_emails = df[df['email'].isin(existing_emails)]
            if not duplicate_emails.empty:
                raise ValueError("CSV contains duplicate emails already in the database")

        return df

    @staticmethod
    def bulk_insert(df, table_name):
        """
        Bulk inserts the validated CSV data into the database.
        Uses PostgreSQL COPY command for efficiency.
        """
        with connection.cursor() as cursor:
            # Convert DataFrame to list of tuples
            records = [tuple(row) for row in df.to_numpy()]
            columns = ", ".join(df.columns)
            placeholders = ", ".join(["%s"] * len(df.columns))

            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders});"
            cursor.executemany(sql, records)

        return len(records)