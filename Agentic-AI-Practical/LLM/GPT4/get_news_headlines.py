# Steps - 
# Identify Import
# Load GPT2Tokenizer and GPT2Model
# Get the news article (article)
# Get the Poosible Headlines (Candidate)
# Get Tokens for news article (article)
#   Convert to Tensor and send to Model 
#   Get the Full Embeddings for news article (article)
#   Get the Mean Embeddings for news article (article) from Full Embeddings
# Get the Poosible Headlines (Candidate) - Repeat for all possible headlines
#   Convert to Tensor and send to Model 
#   Get the Full Embeddings for news article (article)
#   Get the Mean Embeddings for news article (article) from Full Embeddings
# Find Cosine of News (Mean Embeddings for news article ) with Candidates
#  Print Output Top  3 and Full List with Scores

from transformers import GPT2Tokenizer, GPT2Model
import torch
import torch.nn.functional as F

# Load the Model and Tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2Model.from_pretrained("gpt2")

# Get the news Article 
article = """
The United States and India recently announced a rollback of certain tariffs imposed during previous trade disputes. The move is expected to boost bilateral trade, particularly in sectors like agriculture, electronics, and manufacturing. Economists believe this step will enhance market access and reduce costs for exporters on both sides, while signaling improved geopolitical alignment between the two democracies.
"""

# Get Possible Candidates
headlines = [
    "US and India remove tariffs to boost trade ties",
    "India launches lunar probe to explore moon's south pole",
    "Tariff rollback improves US-India manufacturing access",
    "Stock markets dip amid inflation concerns in Asia",
    "Improved trade relations could strengthen US-India alliance",
    "India bans certain Chinese tech products from ports"
]

def get_mean_embeddings (input_text):
    # Get the Tokens from the input_text
    model_input = tokenizer(input_text, return_tensors="pt")

    # Load Model with minimum features, for embeddings only
    with torch.no_grad():
        model_output = model (**model_input)
        mean_embeddings = model_output.last_hidden_state.mean(dim=1) # [1, 768]
    return mean_embeddings

article_embeddings = get_mean_embeddings(article) # Save to Vector DB

results = []
for headline in headlines:
    headline_embeddings = get_mean_embeddings(headline) # Save to Vector DB
    score = F.cosine_similarity(article_embeddings,headline_embeddings).item()
    results.append((headline,score ))

results.sort(key= lambda x: x[1],reverse=True)

print (f"\nNews Article {article} \n")

print ("Top 4 Similar headlines are: \n")

for i in range(4):
    headline, score = results[i]
    print  (f"{i + 1} - {headline} - Score {score:.4f}")

print  (f"\n All Headings as per Score \n")

for headline, score in results:
    print (f"{score:.4f} -> {headline}")