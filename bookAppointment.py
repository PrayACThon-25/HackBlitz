
from flask import Blueprint, render_template, request, redirect, flash, url_for
import smtplib
from email.message import EmailMessage

# Create Blueprint instead of Flask app
book_appointment_blueprint = Blueprint('book_appointment', __name__)

# Update with your email credentials
EMAIL_ADDRESS = 'personalhealthcare27@gmail.com'
EMAIL_PASSWORD = 'mumz kuyo eojg svgp'

def send_appointment_email(to_email, name, doctor, date, time):
    subject = "✅ Appointment Confirmation - HealthMate"
    body = f"""
    Hello {name},

    Your appointment with Dr. {doctor} has been successfully booked!

    📅 Date: {date}
    🕒 Time: {time}

    Thank you for choosing HealthMate.
    """

    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email
        msg.set_content(body)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        print(f"📩 Confirmation email sent to {to_email}")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

@book_appointment_blueprint.route("/book-appointment", methods=["GET", "POST"])
def appointment():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        doctor = request.form.get("doctor")
        date = request.form.get("date")
        time = request.form.get("time")

        if name and email and doctor and date and time:
            send_appointment_email(email, name, doctor, date, time)
            flash("✅ Appointment booked successfully and email sent!", "success")
        else:
            flash("⚠️ All fields are required!", "error")

        return redirect(url_for("book_appointment.appointment"))

    return render_template("appointment1.html")
