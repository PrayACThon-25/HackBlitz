from flask import Blueprint, render_template, request, redirect, flash, url_for
from datetime import datetime
from appointment_handler import schedule_appointment, appointments  # You'll need to create this module

# Create a Blueprint instead of Flask app
appointment_blueprint = Blueprint('appointment', __name__)

@appointment_blueprint.route('/appointment-reminder', methods=['GET', 'POST'])
def manage_appointments():
    if request.method == 'POST':
        patient_name = request.form.get('patientName')
        doctor_name = request.form.get('doctorName')
        appointment_date = request.form.get('appointmentDate')
        appointment_time = request.form.get('appointmentTime')
        email = request.form.get('email')

        if patient_name and doctor_name and appointment_date and appointment_time and email:
            try:
                schedule_appointment(patient_name, doctor_name, appointment_date, appointment_time, email)
                flash(f"✅ Appointment scheduled with Dr. {doctor_name} for {patient_name} on {appointment_date} at {appointment_time}", "success")
            except Exception as e:
                flash(f"❌ Error scheduling appointment: {str(e)}", "error")
        else:
            flash("⚠️ Please fill in all fields!", "warning")

        return redirect(url_for('appointment.manage_appointments'))

    return render_template('appointment.html', appointments=appointments)