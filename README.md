# Catalyst-Count

**Catalyst-Count** is a Django project that enables users to log in and filter records from a database table using a form. This project is designed to provide an easy-to-use interface for users to authenticate and interact with the data through dynamic filtering.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Setup](#setup)
- [Usage](#usage)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Requirements

- Python 3.x
- Django 3.x or higher
- PostgreSQL (or any other relational database)

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/Shreyamahindrakar/catalyst-count.git
    cd catalyst-count
    cd countapplication
    ```

2. **Create a virtual environment and activate it**:

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

4. **Set up PostgreSQL**:
   - Install PostgreSQL on your local machine or use a cloud service.
   - Create a new PostgreSQL database for this project:

     ```bash
     psql -U postgres
     CREATE DATABASE db_name;
     ```

5. **Update Database Settings**  
   In your project, modify the `DATABASES` setting in `settings.py` to connect to PostgreSQL:

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'db_name',
            'USER': 'dbuser',
            'PASSWORD': 'dbpassword',
            'HOST': 'localhost',  # or your PostgreSQL host
            'PORT': '5432',  # default PostgreSQL port
        }
    }
    ```

## Setup

1. **Apply Migrations**:  
   Run the migrations to set up your database schema:

    ```bash
    python manage.py migrate
    ```

2. **Create a Superuser** (Optional, for accessing Django admin):

    ```bash
    python manage.py createsuperuser
    ```

3. **Run the Development Server**:  
   Start the Django development server:

    ```bash
    python manage.py runserver
    ```

   Your application will be accessible at `http://127.0.0.1:8000`.

## Usage

Once your server is running, you can access the app and use the following features:

### Login

Users can log in by navigating to `/login/` and entering their credentials.

![image](https://github.com/user-attachments/assets/c4866240-7a68-403a-be0a-1ff53b2c7b34)

### Register
Users can also register

![image](https://github.com/user-attachments/assets/56635972-64d8-4e3b-9d5e-debfe2f2d3aa)

### Filtering Data

After logging in, users can filter records from a specific database table via a form. The filtering options and form fields depend on the model defined in the app.

![image](https://github.com/user-attachments/assets/7a1ba117-5a16-4791-85d1-bd136567ec14)


1. **Choose filter criteria** from available form options.
2. **Submit the form** to view the filtered records based on the selected criteria.

The table data is displayed dynamically based on the filtering options chosen by the user.

### upload file data:

- **upload file**: upload a file with speficif errors
  ![image](https://github.com/user-attachments/assets/239b5c15-c611-4c5d-afdb-c6d1d4f3a1e4)

### get user list data:
![image](https://github.com/user-attachments/assets/9bc0a88f-4855-4b9f-a964-2d8d96e432f4)


