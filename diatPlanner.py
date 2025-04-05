from flask import Blueprint, render_template, request, session, redirect
import google.generativeai as genai

diet_blueprint = Blueprint('diet', __name__)

def query_diet_ai(user_input):
    try:
        # Configure Gemini API
        genai.configure(api_key="AIzaSyA2byhZ6SP-ychVIeye29Qsc8iH6q9hIwo")
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Create a chat session
        chat = model.start_chat(history=[])
        
        # Prepare the prompt
        prompt = f"""As a nutrition and diet expert, please provide advice for the following query: {user_input}
        Be specific, practical, and focus on healthy eating habits and nutritional information."""
        
        # Get response
        response = chat.send_message(prompt)
        return response.text.strip()
    except Exception as e:
        print("Diet AI Error:", e)
        return "Sorry, I'm having trouble processing your request. Please try again."

@diet_blueprint.route('/diet', methods=['GET', 'POST'])
def diet_planner():
    if 'diet_chat' not in session:
        session['diet_chat'] = [("Bot", "Hi! I'm your diet assistant. Ask me anything about your meals, goals, or preferences!")]

    if request.method == 'POST':
        user_input = request.form['user_input']
        session['diet_chat'].append(("You", user_input))

        response = query_diet_ai(user_input)
        session['diet_chat'].append(("Bot", response))

    return render_template('diatPlanner.html', conversation=session['diet_chat'])

@diet_blueprint.route('/reset_diet')
def reset_diet():
    session.pop('diet_chat', None)
    return redirect('/diet')