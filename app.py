from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
import pickle
import os
from src.pipeline.predict_pipeline import PredictPipeline

app = Flask(__name__)

# Path to the models folder
model_path = "./models/"

# Load the model
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
    
    url = request.json['url']
    print("URL: " + url)
    
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
    response = jsonify({'prediction': result})
    
    return response

if __name__ == '__main__':
    app.run(debug=True)
