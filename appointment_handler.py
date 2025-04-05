from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

appointments = []

def schedule_appointment(patient_name, doctor_name, appointment_date, appointment_time, email):
    appointment = {
        'patient_name': patient_name,
        'doctor_name': doctor_name,
        'date': appointment_date,
        'time': appointment_time,
        'email': email
    }
    
    appointments.append(appointment)
    send_confirmation_email(appointment)

def send_confirmation_email(appointment):
    sender_email = "your_email@gmail.com"  # Replace with your email
    sender_password = "your_password"      # Replace with your password

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = appointment['email']
    msg['Subject'] = "Appointment Confirmation"

    body = f"""
    Dear {appointment['patient_name']},

    Your appointment has been scheduled successfully:

    Doctor: Dr. {appointment['doctor_name']}
    Date: {appointment['date']}
    Time: {appointment['time']}

    Please arrive 15 minutes before your scheduled time.
    If you need to reschedule, please contact us at least 24 hours in advance.

    Best regards,
    Health Care Center
    """

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print(f"Error sending email: {str(e)}")