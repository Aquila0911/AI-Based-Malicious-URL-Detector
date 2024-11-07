from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
import pickle
import os
from src.pipeline.predict_pipeline import PredictPipeline
from src.xss import test_xss

app = Flask(__name__)

# Path to model and Load Model
model_path = "./models/"
with open(os.path.join(model_path, 'dectree.pkl'), 'rb') as f:
    model = pickle.load(f)

pred = PredictPipeline()

# Enable CORS with all origins
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
@cross_origin()
def predict():
    # Receive data from frontend
    url = request.json['url']
    print("URL: " + url)
    
    # Check for XSS patterns
    xss_detected, xss_patterns = test_xss(url)
    if xss_detected:
        print("xss detected")
        return jsonify({'prediction': 'malicious', 'reason': 'XSS detected', 'patterns': xss_patterns})

    transform_url = pred.transformURL(url)
    transform_url = transform_url.reshape(1, -1)

    # print("transform_url" , transform_url)
    prediction = model.predict(transform_url)
    print("prediction: ", prediction)
    
    # 'benign', 'defacement','phishing','malware'
    if prediction == 0:
        res = 'benign'
    elif prediction == 1:
        res = 'defacement'
    elif prediction == 2:
        res = 'phishing'
    else:
        res = 'malware'
    
    result = 'safe' if res == 'benign' else 'malicious'
    response = jsonify({'prediction': result, 'xss': 'not detected'})
    
    return response

if __name__ == '__main__':
    print("Starting server at http://127.0.0.1:5000/")
    app.run(debug=True)
