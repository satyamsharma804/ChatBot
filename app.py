from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import markdown2
from time import sleep

app = Flask(__name__)

# Configure Gemini API key
genai.configure(api_key="AIzaSyC84LiHUHApWJjTyN7XdPy7dazsz8CfMog")
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message")
        if not user_message or not user_message.strip():
            return jsonify({"error": "Empty message"}), 400
            
        # Simulate typing delay for better UX
        sleep(0.5)
        
        response = model.generate_content(
            user_message,
            generation_config={
                "temperature": 0.7,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 2048,
            }
        )
        
        # Convert markdown to HTML for better formatting
        html_response = markdown2.markdown(response.text)
        return jsonify({"reply": html_response})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)