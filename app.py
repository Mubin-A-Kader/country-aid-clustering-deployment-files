
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import pickle
import numpy as np

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Range", "X-Content-Range"],
        "supports_credentials": True
    }
})

# Load the required models and data at startup
def load_models():
    with open('preprocessor.pkl', 'rb') as f:
        preprocessor = pickle.load(f)
    with open('hierarchical_model.pkl', 'rb') as f:
        hierarchical_model = pickle.load(f)
    clustered_df = pd.read_pickle("clustered_data.pkl")
    return preprocessor, hierarchical_model, clustered_df

preprocessor, hierarchical_model, clustered_df = load_models()

@app.route('/')
def home():
    return render_template('input.html')

@app.route('/predict', methods=['POST', 'OPTIONS'])
def predict():
    if request.method == 'OPTIONS':
        response = jsonify({'message': 'OK'})
        return response

    try:
        # Get data from request
        data = request.get_json()
        
        # Validate input data
        required_fields = ['country', 'child_mort', 'exports', 'health', 'imports', 
                         'income', 'inflation', 'life_expec', 'total_fer', 'gdpp']
        
        if not all(field in data for field in required_fields):
            return jsonify({
                'error': 'Missing required fields',
                'required_fields': required_fields
            }), 400

        # Create DataFrame from input data
        new_country_data = pd.DataFrame({
            'country': [data['country']],
            'child_mort': [float(data['child_mort'])],
            'exports': [float(data['exports'])],
            'health': [float(data['health'])],
            'imports': [float(data['imports'])],
            'income': [float(data['income'])],
            'inflation': [float(data['inflation'])],
            'life_expec': [float(data['life_expec'])],
            'total_fer': [float(data['total_fer'])],
            'gdpp': [float(data['gdpp'])]
        })

        # Preprocess new data
        new_country_transformed = preprocessor.transform(new_country_data)
        
        numerical_features = ['child_mort', 'exports', 'health', 'imports', 'income', 
                            'inflation', 'life_expec', 'total_fer', 'gdpp']
        categorical_features = ['country']
        feature_names = numerical_features + list(
            preprocessor.named_transformers_['cat'].get_feature_names_out(categorical_features)
        )
        
        new_country_processed = pd.DataFrame(new_country_transformed, columns=feature_names)
        
        # Ensure both have the same columns
        missing_cols = set(clustered_df.columns) - set(new_country_processed.columns)
        for col in missing_cols:
            new_country_processed[col] = 0.0
            
        # Reorder columns to match clustered_df
        new_country_processed = new_country_processed[clustered_df.columns]
        
        # Concatenate new country with clustered dataset
        combined_data = pd.concat([clustered_df, new_country_processed], ignore_index=True)
        
        # Drop unused columns
        columns_to_drop = ['country', 'High_Child_Mortality', 'Export_Import_Ratio']
        combined_data_model_input = combined_data.drop(columns=columns_to_drop, errors='ignore')
        
        # Predict clusters
        cluster_labels = hierarchical_model.fit_predict(combined_data_model_input)
        
        # Get cluster of new country (last row)
        new_country_cluster = cluster_labels[-1]

        if int(new_country_cluster) == 1:
            message = "🌍 Cluster 1: High Risk Zone – Urgent attention needed for development and stability."
        elif int(new_country_cluster) == 2:
            message = "✅ Cluster 2: Low Risk – Strong indicators of economic and social well-being!"
        else:
            message = "⚠️ Cluster 0: Moderate Risk – Developing steadily, but with key areas to improve."

        return jsonify({
            'country': data['country'],
            # 'cluster': int(new_country_cluster),
            'message': message
        })

    except Exception as e:
        return jsonify({
            'error': 'Error processing request',
            'message': str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True, port=4000)
