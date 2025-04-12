import os
import torch
import boto3
import requests
import time
from utils.aws_utils import download_model_if_on_aws
from utils.model_utils import load_model


# define S3 related variables
S3_BUCKET_NAME = 'doc-task-bucket-1'
S3_MODEL_PATH = 'models/llama_model_hf/'
LOCAL_MODEL_PATH = 'models/llama_model_hf/'

def main():
    print("Running app test!")

    # if running on AWS, download the model from S3
    download_model_if_on_aws(S3_BUCKET_NAME, S3_MODEL_PATH, LOCAL_MODEL_PATH)

    # load the model
    tokenizer, model = load_model(LOCAL_MODEL_PATH)
    
    # test the model with a sample input
    input_text = "Tell me a joke!"
    inputs = tokenizer(input_text, return_tensors="pt").to(model.device)
    
    with torch.no_grad():
        outputs = model.generate(**inputs)
    
    output_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"Output: {output_text}")
    time.sleep(10)


if __name__ == "__main__":
    main()

