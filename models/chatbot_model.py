from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load the model once when the script runs
model_name = "facebook/blenderbot-400M-distill"  
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

def generate_response(prompt):
    """Generates a chatbot response based on the input prompt."""
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    output = model.generate(**inputs, max_length=200)
    return tokenizer.decode(output[0], skip_special_tokens=True)
