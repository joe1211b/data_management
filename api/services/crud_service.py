from django.db import connection

class CRUDService:

    @staticmethod
    def insert_record(table_name, data):
        """
        Inserts a new record into the specified table.
        Example: insert_record("Customer", {"name": "John", "email": "john@example.com", "created_at": "2024-02-01"})
        """
        columns = ", ".join(data.keys())
        values = ", ".join(["%s"] * len(data))
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({values}) RETURNING id;"
        
        with connection.cursor() as cursor:
            cursor.execute(sql, list(data.values()))
            record_id = cursor.fetchone()[0]
        
        return {"id": record_id, **data}

    @staticmethod
    def get_records(table_name, filters=None, search=None, page=1, limit=10, order_by="id", order_direction="ASC"):
        """
        Retrieves records from a table with optional filters, search, pagination, and sorting.
        Example: get_records("Customer", filters={"name": "John"}, search="example", page=1, limit=10)
        """
        where_clauses = []
        params = []

        if filters:
            for column, value in filters.items():
                where_clauses.append(f"{column} = %s")
                params.append(value)

        if search:
            where_clauses.append(f" OR ".join([f"{col} ILIKE %s" for col in filters.keys()]))
            params.extend([f"%{search}%"] * len(filters))

        where_sql = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""

        offset = (page - 1) * limit
        sql = f"""
            SELECT * FROM {table_name} {where_sql}
            ORDER BY {order_by} {order_direction}
            LIMIT {limit} OFFSET {offset};
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in rows]

        return results

    @staticmethod
    def update_record(table_name, record_id, data):
        """
        Updates a record in a given table by ID.
        Example: update_record("Customer", 1, {"name": "Jane Doe"})
        """
        set_clause = ", ".join([f"{col} = %s" for col in data.keys()])
        sql = f"UPDATE {table_name} SET {set_clause} WHERE id = %s RETURNING id;"

        with connection.cursor() as cursor:
            cursor.execute(sql, list(data.values()) + [record_id])
            updated_id = cursor.fetchone()

        if updated_id:
            return {"id": updated_id[0], **data}
        return None

    @staticmethod
    def delete_record(table_name, record_id):
        """
        Deletes a record by ID.
        Example: delete_record("Customer", 1)
        """
        sql = f"DELETE FROM {table_name} WHERE id = %s RETURNING id;"

        with connection.cursor() as cursor:
            cursor.execute(sql, [record_id])
            deleted_id = cursor.fetchone()

        return deleted_id[0] if deleted_id else None
