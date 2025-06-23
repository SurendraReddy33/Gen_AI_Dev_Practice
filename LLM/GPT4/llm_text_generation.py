from transformers import GPT2Tokenizer, GPT2Model, GPT2LMHeadModel
import torch


prompt = "Python is used for programming  the ai models"

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
head_model = GPT2LMHeadModel.from_pretrained("gpt2")


input_ids = tokenizer.encode (prompt, return_tensors ="pt")

output_ids =  head_model.generate(input_ids, max_length=500, do_sample=True)

generated_text = tokenizer.decode(output_ids[0], skip_special_tokens = True)

print  (f"\n {prompt} \n")
print  (f"\n Generated Text : {generated_text}")