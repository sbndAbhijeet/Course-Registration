# Course Registration System - IIIT Vadodara

A comprehensive web-based course registration system for IIIT Vadodara, built with Django. This system allows students to register for courses, faculty to review registrations, and administrators to manage the entire process.

## 🌟 Features

### For Students
- Secure login with email and password
- Course registration with dynamic course filtering based on semester and branch
- Real-time course availability checking
- Registration status tracking
- Email notifications for registration updates
- Profile management
- Access to academic schedules (bus, mess, class schedules)

### For Faculty
- Faculty dashboard for reviewing student registrations
- Ability to approve/reject registrations with feedback
- Email notifications for new registrations
- Status tracking of all assigned registrations


## 🚀 Project Setup

### Prerequisites
- Python 3
- Django 5
- DB SQLite
- Virtual environment

### Installation Steps

1. **Clone the Repository**
```sh
git clone https://github.com/sbndAbhijeet/Course-Registration.git
cd Course-Registration
```

2. **Create and Activate Virtual Environment**
```sh
python -m venv .venv
```
- **Windows:**
  ```sh
  .venv\Scripts\activate
  ```
- **Mac/Linux:**
  ```sh
  source .venv/bin/activate
  ```

3. **Install Dependencies**
```sh
pip install -r requirements.txt
```

4. **Configure Environment Variables**
Create a `.env` file in the root directory with the following variables:
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-email-password
DEFAULT_FROM_EMAIL=your-default-email
```

5. **Run Migrations**
```sh
python manage.py makemigrations
python manage.py migrate
```

6. **Create Superuser**
```sh
python manage.py createsuperuser
```

7. **Run the Development Server**
```sh
python manage.py runserver
```

## 📱 Usage

1. **Access the Application**
   - Open your browser and navigate to `http://127.0.0.1:8000`
   - Login with your credentials

2. **Student Registration Process**
   - Login as a student
   - Navigate to "Register for a Semester"
   - Fill in the registration form
   - Select courses based on your branch and semester
   - Submit the registration
   - Wait for faculty approval

3. **Faculty Review Process**
   - Login as faculty
   - Access the faculty dashboard
   - Review assigned registrations
   - Update registration status with feedback
   - Send notifications to students

## 🔧 Technical Details

### Project Structure
```
course_register/
├── accounts/          # User authentication and profiles
├── course_registration/  # Main application
│   ├── models.py     # Database models
│   ├── views.py      # View logic
│   ├── forms.py      # Form definitions
│   └── urls.py       # URL routing
├── templates/        # HTML templates
└── static/          # Static files (CSS, JS, images)
```

### Key Technologies
- Django 5
- SQLite
- Bootstrap 4
- jQuery
- Django Forms
- Django Admin (`Note`: This is a session-based application no inbuilt Django Admin is used)

## 🛠️ Development

### Running Tests
```sh
python manage.py test
```

### Code Style
The project follows PEP 8 guidelines. Use the following command to check code style:
```sh
flake8 .
```

### Git Workflow
1. Create a new branch for features:
   ```sh
   git checkout -b feature/your-feature-name
   ```
2. Commit changes:
   ```sh
   git add .
   git commit -m "Description of changes"
   ```
3. Push to remote:
   ```sh
   git push origin feature/your-feature-name
   ```
4. Create a Pull Request on GitHub


## Contributors
- Sapparapu Abhijeet
- G Nikhil
- Keshav Badaya
- Mohli Tapa


## Requirements
pillow
sendgrid

---
Made with ❤️ for IIIT Vadodara