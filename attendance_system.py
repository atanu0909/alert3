import pyodbc
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from datetime import datetime, timedelta
import schedule
import time
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AttendanceSystem:
    def __init__(self):
        self.server = os.getenv('DB_SERVER', '1.22.45.168:19471')
        self.database = os.getenv('DB_NAME', 'etimetrackliteWEB')
        self.username = os.getenv('DB_USERNAME', 'sa')
        self.password = os.getenv('DB_PASSWORD', 'sa@123')
        self.email_from = os.getenv('EMAIL_FROM')
        self.email_password = os.getenv('EMAIL_PASSWORD')
        self.email_to = os.getenv('EMAIL_TO', 'aghosh09092004@gmail.com')
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        
    def get_database_connection(self):
        """Establish connection to SQL Server database"""
        try:
            connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}"
            connection = pyodbc.connect(connection_string)
            logger.info("Database connection established successfully")
            return connection
        except Exception as e:
            logger.error(f"Error connecting to database: {e}")
            raise
    
    def get_daily_attendance(self, target_date=None):
        """Get first IN time for each employee via device 19 for a specific date"""
        if target_date is None:
            target_date = datetime.now().date()
        
        try:
            conn = self.get_database_connection()
            
            # Query to get first IN time for each employee via device 19
            query = """
            SELECT 
                e.EmpCode,
                e.EmpName,
                e.Department,
                MIN(CASE WHEN a.InOutFlag = 'IN' THEN a.AttendanceTime END) as FirstInTime,
                d.DeviceName
            FROM 
                AttendanceLog a
            INNER JOIN 
                Employee e ON a.EmpCode = e.EmpCode
            INNER JOIN 
                Device d ON a.DeviceId = d.DeviceId
            WHERE 
                CAST(a.AttendanceTime AS DATE) = ?
                AND a.InOutFlag = 'IN'
                AND a.DeviceId = 19
            GROUP BY 
                e.EmpCode, e.EmpName, e.Department, d.DeviceName
            ORDER BY 
                e.EmpCode
            """
            
            df = pd.read_sql_query(query, conn, params=[target_date])
            conn.close()
            
            logger.info(f"Retrieved attendance data for {len(df)} employees on {target_date}")
            return df
            
        except Exception as e:
            logger.error(f"Error retrieving attendance data: {e}")
            raise
    
    def create_attendance_report(self, df, target_date):
        """Create Excel report from attendance data"""
        try:
            filename = f"Daily_Attendance_{target_date.strftime('%Y%m%d')}.xlsx"
            filepath = os.path.join(os.getcwd(), filename)
            
            # Create Excel writer
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                # Write main attendance data
                df.to_excel(writer, sheet_name='Daily Attendance', index=False)
                
                # Get workbook and worksheet
                workbook = writer.book
                worksheet = writer.sheets['Daily Attendance']
                
                # Auto-adjust column widths
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
                
                # Add summary sheet
                summary_df = pd.DataFrame({
                    'Total Employees': [len(df)],
                    'Date': [target_date.strftime('%Y-%m-%d')],
                    'Report Generated': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
                })
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            logger.info(f"Excel report created: {filename}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error creating Excel report: {e}")
            raise
    
    def send_email_report(self, filepath, target_date):
        """Send email with attendance report attached"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_from
            msg['To'] = self.email_to
            msg['Subject'] = f"Daily Attendance Report - {target_date.strftime('%Y-%m-%d')}"
            
            # Email body
            body = f"""
            Dear Team,
            
            Please find attached the daily attendance report for {target_date.strftime('%Y-%m-%d')}.
            
            This report contains the first IN time for each employee via Device 19.
            
            Report Details:
            - Date: {target_date.strftime('%Y-%m-%d')}
            - Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            - Device: Device 19
            
            Best regards,
            Attendance System
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach file
            with open(filepath, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {os.path.basename(filepath)}'
                )
                msg.attach(part)
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_from, self.email_password)
            text = msg.as_string()
            server.sendmail(self.email_from, self.email_to, text)
            server.quit()
            
            logger.info(f"Email sent successfully to {self.email_to}")
            
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            raise
    
    def generate_and_send_report(self, target_date=None):
        """Main function to generate and send daily attendance report"""
        if target_date is None:
            target_date = datetime.now().date()
        
        try:
            logger.info(f"Starting attendance report generation for {target_date}")
            
            # Get attendance data
            df = self.get_daily_attendance(target_date)
            
            if df.empty:
                logger.warning(f"No attendance data found for {target_date}")
                return
            
            # Create Excel report
            filepath = self.create_attendance_report(df, target_date)
            
            # Send email
            self.send_email_report(filepath, target_date)
            
            # Clean up file
            os.remove(filepath)
            logger.info("Report file cleaned up")
            
            logger.info("Attendance report process completed successfully")
            
        except Exception as e:
            logger.error(f"Error in report generation process: {e}")
            raise

def job():
    """Job function to be scheduled"""
    try:
        attendance_system = AttendanceSystem()
        attendance_system.generate_and_send_report()
    except Exception as e:
        logger.error(f"Scheduled job failed: {e}")

def main():
    """Main function with scheduler"""
    logger.info("Starting Attendance System Scheduler")
    
    # Schedule job to run daily at 12:40 PM
    schedule.every().day.at("12:40").do(job)
    
    logger.info("Scheduler configured to run daily at 12:40 PM")
    
    # For testing, you can run immediately
    if os.getenv('RUN_IMMEDIATELY', 'false').lower() == 'true':
        logger.info("Running job immediately for testing")
        job()
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main()
