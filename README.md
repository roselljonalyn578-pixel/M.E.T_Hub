# MET HUB - Misinformation & Erosion Truth Hub

A Django-based web platform designed to detect and analyze misleading or false information shared online.

## Features

- User authentication with role-based access (Admin/User)
- File upload system for images, videos, and links
- Project management and tracking
- Statistics and reporting dashboard
- Profile management with picture upload
- Responsive design with neon-themed UI

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd M.E.T
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

7. Access the application at `http://127.0.0.1:8000/`

## Project Structure

- `hub/` - Main application directory
- `templates/` - HTML templates
- `static/` - CSS, JavaScript, and static assets
- `media/` - User uploaded files
- `MET/` - Project settings

## Technologies Used

- Django 4.2+
- Python 3.x
- HTML5/CSS3
- SQLite (development)

## License

Educational project for learning purposes.
