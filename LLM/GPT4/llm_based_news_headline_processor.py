from transformers import GPT2LMHeadModel, GPT2Tokenizer, GPT2Model
import torch
import torch.nn.functional as F

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
head_model = GPT2LMHeadModel.from_pretrained("gpt2")
embedding_model = GPT2Model.from_pretrained("gpt2")

# Add Padding Tokens {Becuase this is not default in GPT2}
tokenizer.pad_token = tokenizer.eos_token
head_model.pad_token_id = head_model.config.eos_token_id

news_article = (
    "India and the United States have agreed to remove several trade tariffs in order to boost economic cooperation. "
    "This move is expected to benefit sectors like agriculture, electronics, and manufacturing while reducing costs "
    "for exporters on both sides. The agreement signals a stronger strategic alignment between the two nations."
)

# GPT2 Prompt = Question + Context
news_headline_prompt = f"Generate a headline for this news: \n {news_article} \n Headline: "

news_headline_prompt_ids = tokenizer.encode(news_headline_prompt, return_tensors= "pt")
model_response = head_model.generate(
    news_headline_prompt_ids, # Generate Text for news_headline_prompt
    max_new_tokens=50,
    num_return_sequences=10,
    do_sample=True,
    temperature=0.8
)


def get_mean_embedding(input_text):
    input_text_tokens = tokenizer(input_text, return_tensors="pt")
    with torch.no_grad():
        embeddings = embedding_model(**input_text_tokens)
    return embeddings.last_hidden_state.mean(dim=1) # Share [1,768] 768-d

news_article_embedding =  get_mean_embedding (news_article)

results = []
for i, news_headline in enumerate(model_response):
    headline = tokenizer.decode(news_headline, skip_special_tokens = True)
    headline_embedding = get_mean_embedding(headline)
    similarity = F.cosine_similarity(news_article_embedding,headline_embedding).item()
    results.append ((headline.strip(),similarity))

results.sort(key=lambda x: x[1], reverse=True)

top_three_headlines = results[:5]

print ("\n Top 5 Headlines are:")
for i, (headline,similarity)  in enumerate(top_three_headlines,1):
    print (f"{headline} - Score {similarity:.4f}")

# print (top_three_headlines)


# headline_seq_0 = tokenizer.decode(model_response[0], skip_special_tokens = True)
# headline_seq_1 = tokenizer.decode(model_response[1], skip_special_tokens = True)
# headline_seq_2 = tokenizer.decode(model_response[2], skip_special_tokens = True)

# print (f"Seq 0 : {headline_seq_0}")
# print (f"Seq 1 : {headline_seq_1}")
# print (f"Seq 2 : {headline_seq_2}")


