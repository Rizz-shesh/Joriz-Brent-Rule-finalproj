# Well Baby Blueprint

A web application for managing and tracking baby health records.

## Features

- Patient record management
- Birth date tracking
- Search functionality
- User-friendly interface

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/Rizz-shesh/Joriz-Brent-Rule-finalproj.git
cd Joriz-Brent-Rule-finalproj
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Start the development server:
```bash
python manage.py runserver
```

## Deployment

This application is configured for deployment on Render.

### Environment Variables Required:
- `DATABASE_URL`: Your PostgreSQL database URL
- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to False in production
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts 