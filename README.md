# 🔐 IntchSystem – Flask Authentication App

A complete authentication and user management system built with **Flask**, featuring role-based access control, user profile management, and secure file uploads.  

---

## 🚀 Features

- 🔑 **User Authentication** (Register, Login, Logout)
- 👤 **Profile Management** (update username, email, password, and profile image)
- 🧑‍💼 **Role-Based Access Control**  
  - `admin` users can view, edit, and delete all accounts  
  - `user` accounts have limited access
- 🖼️ **Profile Picture Uploads** with size and format validation
- 💾 **MySQL Database Integration** using SQLAlchemy ORM
- 🧱 **Database Migration** support with Flask-Migrate (Alembic)
- ⚙️ Environment-based configuration (`.env` support)
- 🧑‍💻 Modular structure using Flask Blueprints

---

## 🧭 Project Structure
```
IntchSystem/
│
├── app.py # Application entry point
├── config.py # Environment configuration
├── db_extensions.py # Database initialization
├── requirements.txt # Python dependencies
├── .env # Environment variables
│
├── accounts/ # Authentication blueprint
│ ├── init.py
│ ├── views.py
│ └── templates/
│ └── accounts/
│ ├── login.html
│ ├── register.html
│ ├── profile.html
│ ├── edit_profile.html
│ └── users.html
│
├── migrations/ # Alembic migration folder
│
├── static/
│ ├── css/
│ └── uploads/ # User-uploaded profile pictures
│
└── templates/
├── layout.html
├── index.html
└── 404.html
```


---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/IntchSystem.git
cd IntchSystem
```

##### 2. Create a Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate       # On macOS/Linux
.venv\Scripts\activate          # On Windows
```


### 3. Install Dependencies
```bash
pip install -r requirements.txt
```


###4. Configure Environment Variables

- Create a .env file in the project root:

SECRET_KEY=your_secret_key
MYSQL_HOST=localhost
MYSQL_USER=admin
MYSQL_PASSWORD=password
MYSQL_DB=pythonlogin


### 5. Initialize the Database
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 6. Run the Application
```flask run```
Then visit :  http://127.0.0.1:5000


🔧 Deployment
You can deploy the app to Render, Railway, or any cloud platform supporting Python/Flask.


--
```
🧠 Technologies Used : 
Flask – Python web framework
Flask-Migrate – Database migrations
Flask-SQLAlchemy – ORM for database management
PyMySQL – MySQL database driver
Jinja2 – Template engine
Gunicorn – Production server
Python-dotenv – Environment configuration
```
--

🛡️ Security :
Passwords are securely hashed before being stored
Secret keys are loaded from environment variables
File uploads are validated for size and extension

--  

🧩 Future Improvements
```
Email verification during registration
Password reset via email
REST API endpoints for mobile clients
Docker support for containerized deployment
```
--

💬 Author
Éric Tchindje
Machine Learning Engineer & Software Developer
📧 tchindjeeric61@gmail.com


🪪 License
This project is licensed under the MIT License – feel free to use and modify it.
