from app import lambda_handler
import json

# Test data
test_event = {
    "body": json.dumps({
        "country": "TestCountry",
        "child_mort": 20.0,
        "exports": 45.0,
        "health": 8.0,
        "imports": 42.0,
        "income": 4000,
        "inflation": 5.5,
        "life_expec": 70.0,
        "total_fer": 2.5,
        "gdpp": 3000
    })
}

# Run the lambda handler
response = lambda_handler(test_event, None)

# Print the response
print("Status Code:", response['statusCode'])
print("Headers:", response['headers'])
print("Body:", json.loads(response['body']))