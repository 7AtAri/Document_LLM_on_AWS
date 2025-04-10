import os
import boto3
import torch
from transformers import LlamaTokenizer, LlamaForCausalLM
from pathlib import Path

# to connect to S3 (AWS storage)
s3_client = boto3.client('s3')

# define S3 related variables
S3_BUCKET_NAME = 'doc-task-bucket-1'
MODEL_PATH = 'models/llama_model_hf/'

def download_model_from_s3(bucket, prefix, local_dir):
    paginator = s3_client.get_paginator("list_objects_v2")
    
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        keys = [obj["Key"] for obj in page.get("Contents", [])]
        for key in keys:
            relative_path = Path(key).relative_to(prefix)
            target_path = Path(local_dir) / relative_path
            target_path.parent.mkdir(parents=True, exist_ok=True)
            try:
                s3_client.download_file(bucket, key, str(target_path))
            except Exception as e:
                print(f"download of {key} failed because of: {e}")

def load_model(model_path):
    # loading tokenizer and model
    tokenizer = LlamaTokenizer.from_pretrained(model_path)
    model = LlamaForCausalLM.from_pretrained(model_path, torch_dtype=torch.float32).to("cpu")
    
    if torch.cuda.is_available():
        model = model.to('cuda')

    print(f"Model and tokenizer loaded")
    
    return tokenizer, model

def main():
    print("Running app test!")
    # download the model from S3
    download_model_from_s3(S3_BUCKET_NAME, MODEL_PATH, 'models/llama_model_hf')
    
    # load the model
    tokenizer, model = load_model('models/llama_model_hf')
    
    # test the model with a sample input
    input_text = "Tell me a joke!"
    inputs = tokenizer(input_text, return_tensors="pt").to(model.device)
    
    with torch.no_grad():
        outputs = model.generate(**inputs)
    
    output_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"Output: {output_text}")


if __name__ == "__main__":
    main()