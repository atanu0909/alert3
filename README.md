# Daily Attendance System

This system automatically generates daily attendance reports and sends them via email at 12:40 PM daily.

## Features

- Connects to SQL Server database to retrieve attendance data
- Finds the first IN time for each employee via Device 19
- Generates Excel reports with attendance data
- Sends email reports automatically
- Deployed using GitHub Actions for automated scheduling

## Setup Instructions

### 1. Database Setup
The system connects to your SQL Server database. Database connection details are configured via environment variables for security.

### 2. Email Configuration
You need to configure email settings for sending reports:

1. Create a Gmail App Password:
   - Go to your Google Account settings
   - Navigate to Security > App passwords
   - Generate a new app password for this application

2. Update the email configuration in GitHub Secrets (see below)

### 3. GitHub Actions Setup

1. Fork/Clone this repository to your GitHub account
2. Go to your repository Settings > Secrets and variables > Actions
3. Add the following secrets:

```
DB_SERVER=your_database_server
DB_NAME=your_database_name
DB_USERNAME=your_database_username
DB_PASSWORD=your_database_password
EMAIL_FROM=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
EMAIL_TO=recipient@email.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

### 4. Local Testing

1. Clone the repository
2. Create a `.env` file based on `.env.example`
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the system:
   ```bash
   python attendance_system.py
   ```

## Database Schema Requirements

The system expects the following tables in your database:

### Employee Table
- EmpCode (Primary Key)
- EmpName
- Department

### AttendanceLog Table
- EmpCode (Foreign Key)
- AttendanceTime (DateTime)
- InOutFlag (IN/OUT)
- DeviceId

### Device Table
- DeviceId (Primary Key)
- DeviceName

## How It Works

1. **Data Retrieval**: The system queries the database for attendance records where:
   - Date matches the target date (current date by default)
   - InOutFlag is 'IN'
   - DeviceId is 19

2. **Report Generation**: Creates an Excel file with:
   - Employee details (Code, Name, Department)
   - First IN time for each employee
   - Device information
   - Summary sheet with statistics

3. **Email Delivery**: Sends the report via email to the specified recipient

4. **Scheduling**: GitHub Actions runs the system daily at 12:40 PM UTC

## Customization

- **Time Zone**: Adjust the cron schedule in `.github/workflows/attendance.yml`
- **Email Template**: Modify the email body in `attendance_system.py`
- **Report Format**: Customize the Excel report structure
- **Database Query**: Modify the SQL query for different filtering criteria

## Troubleshooting

1. **Database Connection Issues**: Verify server details and credentials
2. **Email Delivery Problems**: Check Gmail App Password and SMTP settings
3. **GitHub Actions Failures**: Review the workflow logs in the Actions tab

## Security Notes

- Never commit sensitive credentials to the repository
- Use GitHub Secrets for all sensitive configuration
- The `.env` file should be in `.gitignore`

## License

This project is for internal use only.
