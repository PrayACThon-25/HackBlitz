from flask import Blueprint, render_template, request
from markupsafe import Markup
import google.generativeai as genai

disease_blueprint = Blueprint('disease', __name__)

def format_response(text):
    # Split the response into sections
    sections = text.split('\n')
    formatted_text = []
    
    for section in sections:
        if section.strip():
            if any(section.startswith(str(i)) for i in range(1, 5)):
                # Main sections (1., 2., 3., 4.)
                formatted_text.append(f"<h4 class='section-title'>{section}</h4>")
            else:
                # Regular text
                formatted_text.append(f"<p>{section}</p>")
    
    return Markup("".join(formatted_text))

def query_disease_ai(symptoms):
    try:
        genai.configure(api_key="AIzaSyA2byhZ6SP-ychVIeye29Qsc8iH6q9hIwo")
        model = genai.GenerativeModel("gemini-1.5-flash")
        chat = model.start_chat(history=[])
        
        prompt = f"""As a medical assistant, please analyze these symptoms: {symptoms}
        
        Provide a detailed analysis in the following format:
        1. Possible Conditions:
        - List potential conditions
        - Brief description of each
        
        2. Risk Level:
        - Overall assessment
        - Factors to consider
        
        3. General Advice:
        - Immediate steps to take
        - Home care recommendations
        - Lifestyle modifications
        
        4. When to Seek Medical Help:
        - Warning signs
        - Emergency symptoms
        - Recommended medical consultation timeframe
        
        Keep the response professional and informative."""
        
        response = chat.send_message(prompt)
        return format_response(response.text.strip())
    except Exception as e:
        print("Disease AI Error:", e)
        return format_response("Sorry, I'm having trouble analyzing your symptoms. Please try again or consult a healthcare professional.")

@disease_blueprint.route('/predict-disease', methods=['GET', 'POST'])
def symptom_checker():
    result = None
    if request.method == 'POST':
        symptoms = request.form['symptoms']
        result = query_disease_ai(symptoms)
    return render_template('symptom_checker.html', result=result)