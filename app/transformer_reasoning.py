from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

print("Loading TinyLlama model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float32
)

model.eval()

print("TinyLlama loaded successfully.")


def generate_ai_summary(prompt, max_tokens=250):

    # Chat-style formatting (IMPORTANT for instruction model)
    messages = [
        {"role": "system", "content": "You are a professional financial analyst AI."},
        {"role": "user", "content": prompt}
    ]

    formatted_prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(formatted_prompt, return_tensors="pt")

    with torch.no_grad():
        outputs = model.generate(
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_new_tokens=max_tokens,
            temperature=0.6,
            top_p=0.9,
            repetition_penalty=1.2,
            pad_token_id=tokenizer.eos_token_id
        )

    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Clean assistant tag artifacts
    generated_text = generated_text.replace("|>", "")
    generated_text = generated_text.strip()

    # Remove everything before actual response
    if "Executive Summary:" in generated_text:
        generated_text = generated_text.split("Executive Summary:")[-1]

    return generated_text.strip()