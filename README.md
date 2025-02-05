# Course Registration Project

## 🚀 Project Setup
This guide will help you set up the project correctly.



### 🔥 Installation Steps
#### 1️⃣ Clone the Repository
```sh
git clone https://github.com/sbndAbhijeet/Course-Registration.git
cd registration_project
```

#### 2️⃣ Create and Activate a Virtual Environment
```sh
python -m venv venv
```
- **Windows:**
  ```sh
  venv\Scripts\activate
  ```
- **Mac/Linux:**
  ```sh
  source venv/bin/activate
  ```

#### 3️⃣ Install Dependencies
Ensure you install the exact versions by running:
```sh
pip install -r requirements.txt
```

#### 4️⃣ Run the Django Server
```sh
python manage.py runserver
```


If you face issues, check your installed versions:
```sh
python --version
python -m django --version
```

### ⚡ Git Workflow
1. **Create a new branch** before making changes:
   ```sh
   git checkout -b feature-branch
   ```
2. **Commit your changes:**
   ```sh
   git add .
   git commit -m "Your message here"
   ```
3. **Push your branch:**
   ```sh
   git push origin feature-branch
   ```
4. **Create a Pull Request (PR)** on GitHub before merging into `main`.

### 🛑 Common Issues & Fixes
- **Virtual environment not activating?** Ensure you're in the correct directory.
- **Different Python version?** Install the correct version and recreate the virtual environment.
- **Dependency mismatch?** Run:
  ```sh
  pip install -r requirements.txt --no-cache-dir
  ```

### 📌 Contributors
- **Your Name** (@your-github)
- Other team members...

---
Happy coding! 🚀



# requirements
pillow
sendgrid
