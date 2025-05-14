
import pandas as pd
import pickle
import numpy as np
import json

# Load the required models and data at startup
def load_models():
    with open('preprocessor.pkl', 'rb') as f:
        preprocessor = pickle.load(f)
    with open('hierarchical_model.pkl', 'rb') as f:
        hierarchical_model = pickle.load(f)
    clustered_df = pd.read_pickle("clustered_data.pkl")
    return preprocessor, hierarchical_model, clustered_df

preprocessor, hierarchical_model, clustered_df = load_models()

def lambda_handler(event, context):
    try:
        # Get data from request
        data = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        if not data:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'No data found in request'})
            }
        
        # Validate input data
        required_fields = ['country', 'child_mort', 'exports', 'health', 'imports', 
                         'income', 'inflation', 'life_expec', 'total_fer', 'gdpp']
        
        if not all(field in data for field in required_fields):
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'error': 'Missing required fields',
                    'required_fields': required_fields
                })
            }

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
        
        # Keep the original fit_predict logic
        cluster_labels = hierarchical_model.fit_predict(combined_data_model_input)
        
        # Get cluster of new country (last row)
        new_country_cluster = cluster_labels[-1]

        if int(new_country_cluster) == 1:
            message = "🌍 Cluster 1: High Risk Zone – Urgent attention needed for development and stability."
        elif int(new_country_cluster) == 2:
            message = "✅ Cluster 2: Low Risk – Strong indicators of economic and social well-being!"
        else:
            message = "⚠️ Cluster 0: Moderate Risk – Developing steadily, but with key areas to improve."

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'country': data['country'],
                'message': message
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'error': 'Error processing request',
                'message': str(e)
            })
        }
