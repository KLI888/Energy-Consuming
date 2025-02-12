from flask import Flask, render_template, request, jsonify
import os
import numpy as np

app = Flask(__name__)

# Dummy data storage (replace with DB later)
appliances = []  # Stores added appliances
bill_history = []  # Stores last 3 months' bills

@app.route('/')
def home():
    return render_template('index.html', appliances=appliances, bill_history=bill_history)

@app.route('/add_appliance', methods=['POST'])
def add_appliance():
    data = request.json
    appliances.append(data)
    return jsonify({"message": "Appliance added successfully!", "appliances": appliances})

@app.route('/predict_bill', methods=['POST'])
def predict_bill():
    if len(bill_history) < 3:
        return jsonify({"error": "Not enough data for prediction. Enter at least 3 months' bills."})
    
    prediction = np.mean(bill_history) * 1.05  # Simple prediction with a 5% increase
    return jsonify({"predicted_bill": round(prediction, 2)})

@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_message = request.json.get('message', '').lower()
    responses = {
        "how to reduce electricity bill?": "Use energy-efficient appliances and turn off unused devices.",
        "what is the average electricity cost?": "It varies by region. In most places, it's around $0.12/kWh.",
        "how does power consumption work?": "Power is measured in watts. More wattage = more consumption.",
    }
    response = responses.get(user_message, "I'm not sure. Please ask something else.")
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
