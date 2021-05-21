![PassBank50](https://user-images.githubusercontent.com/60486163/118166108-16067180-b44b-11eb-8d9e-bd86dbb698a8.png)

## CS50's Final Projects

## Welcome to PassBank50

### Video Demo: https://youtu.be/GJp96KA49zw
  
### Description
  PassBank50 is a project that manages websites and passwords for you. It provides users to stores passwords and import passwords in `csv` format.
  

### Platform
- Web App


### Features
- User account registration
- User account management
- Add websites and passwords one by one
- Import passwords from Google Chrome or Microsoft Edge in `csv` format
- View added websites and passwords from dashboard


### Languages & Frameworks
- Python
- HTML
- CSS
- Flask
  - flask_sqlalchemy
  - flask_wtforms
  - flask_login
  - flask_mail
- Bootstrap

------------------------------------------------------------------------------------------------------------------------------------------------------------------
## User Documentation
### Registration
![Register](https://user-images.githubusercontent.com/60486163/118169255-bf029b80-b44e-11eb-87a0-3b9491f84bba.png)
- Every new user must create a user account.
- It has to provide a username, an email, a password and a confirmation password.
- On click `Register`, each data provided by the user is tested to meet the requirements such as duplicated username or invalid email.
- If pass, It will straight through to the `Login` page.

### Logging In
![Login](https://user-images.githubusercontent.com/60486163/118171481-44874b00-b451-11eb-9cd5-80b086b61938.png)
- To log in, the user must provide the registered email and password.
- If not the registered email, it will head to `Register` page for registration.
- With the registered email and incorrect password, it will need to log in the right ones.
- If the password is forgotten, it can be resetted by clicking `Forgot Password?`.
- It will ask the email to reset password.
- On submitting, a mail will be sent with the password reset link via the provided email.
- Copy and paste the link in browser, change the password and now you can log in with the new password again.




