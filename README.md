# Vehicle Roadside Assistance System

A web-based **Vehicle Roadside Assistance System** designed to connect vehicle users with mechanics and provide roadside assistance services through an online platform.

## Technologies Used

- HTML5
- CSS3
- JavaScript
- Python
- Flask
- MySQL

## Key Features

- User Registration and Login
- Mechanic Registration and Login
- Admin Login
- User Dashboard
- Mechanic Dashboard
- Admin Dashboard
- Roadside Service Requests
- Mechanic Service Request Management
- Service Status Tracking
- Emergency Support
- Travel and Service Assistance
- Feedback and Reviews
- Mechanic Profile Management
- Emergency Contact Management

## Project Modules

### User Module
Users can register, log in, request roadside assistance, view service requests, track service status, access emergency support, and provide feedback.

### Mechanic Module
Mechanics can register, manage their profile, view service requests, accept or reject requests, and update service status.

### Admin Module
The administrator can manage users, mechanics, service requests, feedback, emergency contacts, and other system activities.

## Screenshots

### Home and Login
![Home](static/home.png)
![Login](static/log.png)

### User Service Request
![Service Request](static/sr.png)
![Request Status](static/req.png)

### Mechanic Profile and Registration
![Mechanic Registration](static/mech_reg.png)
![Mechanic Profile](static/prof.png)

### Emergency and Travel Assistance
![Emergency Support](static/emg.png)
![Travel Assistance](static/travel.png)

### Feedback
![Feedback](static/feed.png)

## Project Structure

```text
Vehicle-Roadside-Assistance-System/
├── app.py
├── db/
├── static/
├── templates/
├── .gitignore
└── README.md
```

## Database

The system uses **MySQL** to store application data such as users, mechanics, service requests, feedback, emergency contacts, and related records.

## How to Run

1. Install Python and MySQL.
2. Install the required Python packages used by the project.
3. Create the project database using the SQL file provided in the `db` folder.
4. Configure the database connection in the Flask application.
5. Run the Flask application.
6. Open the local application URL in a web browser.

## Future Enhancements

- Real-time location tracking
- Online payment integration
- SMS and notification services
- Mobile application support
- Advanced mechanic location matching
