# internship task

simple web application for managing employees using Flask and MySQL. The application allows users to add, update, delete, and list employees.

## setup instructions

1. Install MySQL and Python if not already installed.
2. Create a new database and table:
   ```sql
   CREATE DATABASE company;
   USE company;
   
   CREATE TABLE Employee (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(255) NOT NULL,
       department VARCHAR(255) NOT NULL
   );
3. change the username and password from app.py to your MySQL credentials
4. run app.py 
