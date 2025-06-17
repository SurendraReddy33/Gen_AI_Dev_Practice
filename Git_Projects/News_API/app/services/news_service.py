from app.utils.logger import get_logger
from app.utils.decorators import handle_exceptions
import requests
import logging
import torch
import torch.nn.functional as F
from transformers import GPT2LMHeadModel, GPT2Tokenizer, GPT2Model
import json,os



logging = get_logger(__name__)


NEWS_API_URL = "https://newsapi.org/v2/everything?q=bitcoin&apiKey=5b502fb9f6d94a9c977ae3e9e49e03c8"


# define tokenizer,models
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
gen_model = GPT2LMHeadModel.from_pretrained("gpt2")
emb_model = GPT2Model.from_pretrained("gpt2")

tokenizer.pad_token = tokenizer.eos_token

gen_model.pad_token_id = gen_model.config.eos_token_id
emb_model.pad_token_id = emb_model.config.eos_token_id


@handle_exceptions
def mean_embedding(input_text):
    """
    Returns the mean embedding of the given text using the GPT2 model.
    """
    input_text_tokens = tokenizer(input_text, return_tensors="pt")
    if not input_text_tokens or len(input_text_tokens.get('input_ids', [])) == 0:
        raise ValueError("Input tokens are empty!")
    with torch.no_grad():
        embeddings = emb_model(**input_text_tokens)
    logging.info(f"Gnerated mean_embeddings")
    return embeddings.last_hidden_state.mean(dim=1)


@handle_exceptions
def fetch_news_articles(api_key, count) -> list[dict]:
    """
    Fetches news articles from the News API.
    """
    logging.info("Fetching news articles.....")
    news_api_response = requests.get(NEWS_API_URL, params = {
        "apiKey" : api_key,
        "pageSize" : count
    })

    news_api_response.raise_for_status()
    news_articles = news_api_response.json().get("articles", [])
    logging.info(f"Fetched {len(news_articles)} articles")
    return news_articles


# articles = fetch_news_articles(API_KEY, ARTICLE_COUNT)
# for a in articles:
#     print(a)
#     print("---------------------------------")


@handle_exceptions
def generate_headlines(prompt):
    """
    Generates multiple headline candidates for the given prompt using GPT2.
    """
    news_headline_tokens = tokenizer(prompt, return_tensors = "pt").input_ids
    headlines = gen_model.generate (
        news_headline_tokens,
        num_return_sequences = 5,
        do_sample = True,
        max_new_tokens = 50,
        temperature = 0.8,
        top_k = 50,
        top_p = 0.95
    )
    logging.info(f"Returing the generated headlines by decoding the tokenizer")
    return [tokenizer.decode(headline, skip_special_tokens = True).replace(prompt, "").strip() for headline in headlines]



@handle_exceptions
def process_news_articles(news_articles):
    """
    Processes each news article:
    - Generates headline candidates
    - Scores them using cosine similarity
    - Stores the top headlines with similarity scores
    """
    processed_articles = []

    for id, news_article in enumerate(news_articles):
        content = news_article.get("content") or ""
        title = news_article.get("title") or ""
        description = news_article.get("description") or ""

        news_text = f"{title}. {description}. {content}".strip()

        if not news_text:
            continue
        
        prompt = f"Generate a headline for this news: \n {news_text} \n Headline: "
        headline_candidates = generate_headlines(prompt)


        news_text_embedding = mean_embedding(prompt)

        results = []
        for headline in headline_candidates:
            headline_mean_embedding = mean_embedding(headline)
            score = F.cosine_similarity(headline_mean_embedding, news_text_embedding).item()
            results.append({"headline": headline, "score": round(score, 4)})

            
        results.sort(key=lambda x: x["score"], reverse=True)

        # Append top  headlines with scores
        news_article["top_headlines"] = results
        logging.info(f"Appended headlines for the article")
        processed_articles.append(news_article)

        # print(f"Article {id + 1}")
        # print(f"Original Title: {title}")
        # for i, h in enumerate(results, 1):
        #     print(f"{i}. {h['headline']} (Score: {h['score']:.4f})")
        # print("-------------------------------")
        
        # Print each article and its top headlines
        for key, value in news_article.items():
            print(f"{key}: {value}")
        print("---------------------")

   

        # for headline,score in results:
        #     print(f"Headline: {headline} - Score: {score:.4f}")
        #     print("-------------------------------")


    return {
        "status": "ok",
        "totalResults": len(processed_articles),
        "articles": processed_articles
    }













