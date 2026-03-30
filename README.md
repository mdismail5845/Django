# Custom Authentication System — Django

Professional and extensible custom authentication system built with **Django**.

This repository implements a flexible authentication layer with support for multiple user types and custom authentication flows on top of Django’s authentication framework. It’s designed to be a foundation you can adapt for real-world applications that require more than the default Django auth system.

---

## 🚀 Features

- Multi‑role authentication (e.g., customer, seller, admin)
- Custom user models and authentication logic
- Django session‑based login / logout
- Modular app structure for scalability
- Ready for extension (e.g., email verification, API tokens)

> Django’s authentication system is extensible via custom backends and custom user models — this project implements those extensibility points to provide tailored auth workflows beyond the default system. :contentReference[oaicite:1]{index=1}

---

## 🧱 Project Structure
Custom-authentication-System-Django/
├──> account/ # Primary auth app
├──> auth/ # Custom authentication logic & backends
├──> customer/ # Customer‑specific models/views/templates
├──> seller/ # Seller‑specific logic
├──> manage.py # Django management entry
├──> requirements.txt # Dependencies
└──> README.md # Project documentation


## 🛠 Installation & Setup

1. **Clone the repository**

   git clone https://github.com/mdismail5845/Custom-authentication-System-Django.git
   cd Custom-authentication-System-Django

3. Create and activate a Python virtual environment
python -m venv venv
source venv/bin/activate      # macOS / Linux
venv\Scripts\activate         # Windows

4. Install dependencies
pip install -r requirements.txt

5. Apply migrations and run

python manage.py makemigrations
python manage.py migrate
python manage.py runserver

5. Access the app(Open your browser and visit):
http://127.0.0.1:8000/
