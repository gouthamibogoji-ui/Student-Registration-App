# Student Registration App (Streamlit + MySQL)
A full-stack Student Registration System built using Streamlit, MySQL, and Python, featuring secure authentication, CRUD operations, and a clean interactive UI.This application allows authenticated users to manage student records efficiently with full CRUD functionality and secure user authentication.

## Features

### Authentication

--User Registration

--Secure Login

--Forgot / Reset Password

--Passwords hashed using bcrypt

###  Student Management (CRUD)

➕ Add new students

✏️ Update student details

🗑️ Delete students

📋 View all records in a table

 ### Validation & Security

Input validation for all fields

Passwords stored in encrypted format

Protection against SQL Injection

Session-based user access control

## Tech Stack

--Python 3

--Streamlit – Web application framework

--MySQL – Relational database

--bcrypt – Password hashing

--pandas – Data handling

📂 Project Structure

├── Student_Registration.py                 # Main Streamlit application

├── requirements.txt                        # Required Python libraries

├── README.md                               # Project documentation

## Database Schema

📌 Users Table

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

📌 Registration Table

CREATE TABLE registration (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    course VARCHAR(100) NOT NULL,
    fee INT NOT NULL
);

## Application Screens

--Login / Register / Reset Password

--Student Add / Update / Delete

--Live Student Data Table

--Secure Logout

## Use Cases

--Academic Mini Project

--Internship Project

--Resume / Portfolio

--CRUD + Authentication Demo

## How to Run the Project

#### Step 1: Clone the Repository

git clone https://github.com/gouthamibogoji-ui/student-App.git

cd student-registration-system

#### Step 2: Install Required Packages

pip install -r requirements.txt

#### Step 3: Configure Database

Update MySQL credentials in the code:

host="localhost"

user="root"

password="YOUR_PASSWORD"

database="webgui"

#### Step 4: Launch the App

streamlit run app.py

### Author

Gouthami Bogoji

Aspiring Data Scientist | Python Developer | Streamlit Enthusiast

### Feedback & Support

--If you find this project useful:

⭐ Star the repository

🛠️ Suggest improvements.


