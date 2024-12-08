"""Flask application for gift recommendations."""

from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
from services.recommendation_engine import get_recommendations
from services.instagram_analyzer import analyze_instagram_image

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze Instagram grid and user inputs for gift recommendations."""
    try:
        # Get form data
        age = int(request.form.get('age', 25))
        interests_text = request.form.get('interests', '')
        budget = float(request.form.get('budget', 100))

        # Handle image upload
        if 'instagram-grid' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400
        
        file = request.files['instagram-grid']
        if file.filename == '':
            return jsonify({'error': 'No image selected'}), 400

        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            try:
                # Analyze Instagram image
                image_interests = analyze_instagram_image(filepath)
                
                # Combine image interests with text interests
                all_interests = image_interests + [
                    interest.strip()
                    for interest in interests_text.split(',')
                    if interest.strip()
                ]

                # Get recommendations
                recommendations = get_recommendations(
                    interests=all_interests,
                    age=age,
                    budget=budget
                )

                # Clean up uploaded file
                os.remove(filepath)

                return jsonify({
                    'recommendations': recommendations,
                    'interests': all_interests
                })

            except Exception as e:
                # Clean up file on error
                if os.path.exists(filepath):
                    os.remove(filepath)
                raise e

    except Exception as e:
        return jsonify({
            'error': str(e),
            'recommendations': [],
            'interests': []
        }), 500

if __name__ == '__main__':
    app.run(port=8080, debug=True)
