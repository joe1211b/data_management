from celery import shared_task
from api.services.csv_service import CSVService
from django.core.mail import send_mail

@shared_task
def process_csv_import(file_path, table_name, user_email):
    """
    Celery task to process CSV import asynchronously.
    """
    try:
        df = CSVService.validate_csv(file_path, table_name)
        record_count = CSVService.bulk_insert(df, table_name)

        # Send success email
        send_mail(
            subject="CSV Import Completed",
            message=f"Successfully imported {record_count} records into {table_name}.",
            from_email="no-reply@data-management.com",
            recipient_list=[user_email],
        )

        return f"Imported {record_count} records into {table_name}"

    except Exception as e:
        send_mail(
            subject="CSV Import Failed",
            message=f"CSV import failed due to: {str(e)}",
            from_email="no-reply@data-management.com",
            recipient_list=[user_email],
        )
        return str(e)
