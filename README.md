# Data Management System

## Overview
This project is a **backend system** that allows users to **manage data schemas, perform CRUD operations, and handle large data imports efficiently**. It provides **secure and flexible APIs** for these operations using **Django 5, PostgreSQL 16, Celery, and Redis**.

## Features
- **Schema Management**: API to create, update, and delete tables dynamically.
- **CRUD Operations**: Insert, retrieve, update, and delete records with **search, pagination, and sorting**.
- **Bulk Data Import**: Upload **CSV files** (100K+ records) and import data asynchronously.
- **Data Validation**: Ensures schema compliance and enforces unique fields.
- **Error Reporting**: Provides feedback on invalid imports.
- **Email Notification**: Sends confirmation email after successful CSV import.
- **Security**: Implements **JWT authentication**.

## Tech Stack
- **Backend**: Python 3.12, Django 5, Django REST Framework
- **Database**: PostgreSQL 16
- **Asynchronous Processing**: Celery + Redis
- **Security**: JWT Authentication (djangorestframework-simplejwt)

## Installation & Setup
### 1. Clone the Repository

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure PostgreSQL Database
Ensure PostgreSQL is running and update `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'data_management_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
Run migrations:
```bash
python manage.py migrate
```

### 4. Run Celery Worker & Redis
```bash
redis-server  # Start Redis
celery -A data_management worker --loglevel=info  # Start Celery
```

### 5. Start the Django Server
```bash
python manage.py runserver
```

## API Endpoints
### Authentication
- **Obtain Token:** `POST /api/token/`
  ```json
  {"username": "admin", "password": "password"}
  ```
- **Refresh Token:** `POST /api/token/refresh/`
  ```json
  {"refresh": "your_refresh_token"}
  ```

### Schema Management
- **Create Table:** `POST /api/create-table/`
  ```json
  {"table_name": "Customer", "fields": {"name": "TEXT", "email": "TEXT UNIQUE", "created_at": "DATE"}}
  ```
- **Add Column:** `POST /api/add-column/`
  ```json
  {"table_name": "Customer", "column_name": "phone_number", "column_type": "TEXT"}
  ```
- **Delete Table:** `DELETE /api/delete-table/`
  ```json
  {"table_name": "Customer"}
  ```

### CRUD Operations
- **Insert Record:** `POST /api/insert-record/`
  ```json
  {"table_name": "Customer", "data": {"name": "John Doe", "email": "john@example.com"}}
  ```
- **Get Records (with search, pagination, sorting):** `GET /api/get-records/?table_name=Customer&page=1&limit=10&order_by=name&order_direction=ASC`
- **Update Record:** `PUT /api/update-record/`
  ```json
  {"table_name": "Customer", "id": 1, "data": {"name": "Jane Doe"}}
  ```
- **Delete Record:** `DELETE /api/delete-record/`
  ```json
  {"table_name": "Customer", "id": 1}
  ```

### Bulk Data Import (CSV)
- **Upload CSV:** `POST /api/upload-csv/`
  - Form Data:
    - `file`: CSV file
    - `table_name`: Target table
    - `email`: User email for notifications

## Security
- **JWT authentication required** for all protected routes.

## Notes & Future Improvements
- Add **api rate limit** to limit api abuse.
- Add **logging & monitoring** for audit tracking.
- Extend API to support **JSON schema validation** before table creation.

## Contact & Contribution
- Open issues or contribute via Pull Requests on GitHub.
- Maintained by **Joe Bejjani** joe.bejjani12@gmail.com.

