A community-driven donation platform for bridging the gap between NGOs, donors and individuals.

**Sahara**
A Django Rest Framework (DRF) based backend API for a fundraising platform, where users can request funds by specifying an amount, a reason, and an associated NGO.

**Project Overview**

This project allows users to submit fund requests associated with an NGO. Each request is reviewed and assigned a status (Pending, Approved, or Rejected). Users must be authenticated to make fund requests.

**Tech Stack**
    Backend: Django, Django Rest Framework (DRF)
    Authentication: Token-based authentication (JWT or DRF authentication)
    Database: PostgreSQL
    Storage: Django's default file storage for uploaded images
    Frontend: React.js
---
## Getting Started
1️Clone the Repository

```git clone https://github.com/your-username/fundraising-platform.git ```
```cd fundraising-platform```

2️Set Up a Virtual Environment

```python -m venv venv```
```source venv/bin/activate  # On macOS/Linux```
```venv\Scripts\activate     # On Windows```

3️Install Dependencies

```pip install -r requirements.txt```

4️Configure Database

    By default, the project is set up for SQLite.
    To use PostgreSQL, update DATABASES in settings.py and provide your credentials.

5️Apply Migrations

```python manage.py makemigrations```
```python manage.py migrate```

6️Create a Superuser (For Admin Access)

```python manage.py createsuperuser```

7️ Run the Server

```python manage.py runserver```
 
