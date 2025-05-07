from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON payload
        data = request.get_json()

        # Validate numerical features
        numerical_features = ['child_mort', 'exports', 'health', 'imports', 
                            'income', 'inflation', 'life_expec', 'total_fer', 'gdpp']
        
        for feature in numerical_features:
            if feature not in data:
                return jsonify({
                    'error': f'Missing numerical feature: {feature}',
                    'status': 'error'
                }), 400
            if not isinstance(data[feature], (int, float)):
                return jsonify({
                    'error': f'Feature {feature} must be a number',
                    'status': 'error'
                }), 400

        # Validate categorical features
        if 'country' not in data:
            return jsonify({
                'error': 'Missing categorical feature: country',
                'status': 'error'
            }), 400

        # Mock response - you can replace this with actual clustering logic
        response = {
            'status': 'success',
            'message': 'Data received successfully',
            'received_data': data,
            'cluster': 1  # Mock cluster assignment
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=4000, host='0.0.0.0')