from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load the model once when the script runs
MODEL_NAME = "tiiuae/falcon-7b"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME, torch_dtype=torch.float16, device_map="auto"
)

def generate_response(prompt):
    """Generates a chatbot response based on the input prompt."""
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    output = model.generate(**inputs, max_length=200)
    return tokenizer.decode(output[0], skip_special_tokens=True)
