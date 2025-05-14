FROM public.ecr.aws/lambda/python:3.9

# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install the specified packages
RUN pip install -r requirements.txt

# Copy function code and model files
COPY app.py ${LAMBDA_TASK_ROOT}
COPY preprocessor.pkl ${LAMBDA_TASK_ROOT}
COPY hierarchical_model.pkl ${LAMBDA_TASK_ROOT}
COPY clustered_data.pkl ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler
CMD [ "app.lambda_handler" ]