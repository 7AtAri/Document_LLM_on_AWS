import torch
from transformers import LlamaForCausalLM, PreTrainedTokenizerFast

def load_model(model_path):
    # loading tokenizer and model
    tokenizer = PreTrainedTokenizerFast.from_pretrained(model_path)
    model = LlamaForCausalLM.from_pretrained(model_path, torch_dtype=torch.float32).to("cpu")
    
    if torch.cuda.is_available():
        model = model.to('cuda')

    print(f"Model and tokenizer loaded")
    
    return tokenizer, model