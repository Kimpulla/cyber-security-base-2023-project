
# cyber-security-base-2023-project

Assignment from the course Cyber Security Base 2023 to create a web application that has at least five different flaws from the OWASP top ten list as well as their fixes. The application should have a backend.

> In this implementation I made and fixed 5 vulnerabilities from OWASP 2017 top 10 list. 1. SQL injection, 2. Broken Acces Control, 3. Cryptographig Failure, 4. Cross-site Scripting (xss) and 5. Broken authentication. Best way to find vulnerabilities and fixes is to search commits. I committed vulnerabilities and fixes as I found them.


## Prerequisites

Before you begin, ensure you have met the following requirements:

    You have installed the latest version of Python
    You have a <Windows/Linux/Mac> machine. State which OS is supported/which is not.


## To install cyber-security-base-2023-project, follow these steps:

### Windows, Linux and macOS:

### Clone the repository
> git clone https://github.com/Kimpulla/cyber-security-base-2023-project.git


### Install Python and pip if they are not installed
### Check Python
> python --version

### Check pip
> pip --version

## If Python or pip is not installed, please follow this guide
> https://www.python.org/downloads/ for Python
> https://pip.pypa.io/en/stable/installation/ for pip

## Install the requirements
> pip install -r requirements.txt


## Using cyber-security-base-2023-project

To use cyber-security-base-2023-project, follow these steps:

## Apply the migrations
> python manage.py migrate

## Run the server
> python manage.py runserver

## Then open your browser and navigate to http://localhost:8000.

## Superuser
Application has superuser:
email: admin.admin@gmail.com
password: Superuser123
username: admin

In case you can't use superuser, you can easily create one;

1. Go to projects source folder project/src
2. Run the following in the terminal: python manage.py createsuperuser
3. Then fill usernames, passwords etc.

### You can acces to admin view:

> http://localhost:8000/admin/

## Disclaimer

By using this code, the user assumes the responsibility for the outcomes. The developers do not guarantee any results and are not liable for any damages or losses caused by the use of this application. We highly encourage users to understand the workings of the code before using it in a production environment.
