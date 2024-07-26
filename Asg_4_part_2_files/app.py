from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from Asg_4_part_2_files.utils.database_utils import run_query
from Asg_4_part_2_files.utils.llm_caller_utils import OpenAICaller

def make_review_function(product_id):
    # Run query to get all reviews for this product
    reviews_df = run_query(f'''SELECT * FROM "Review" WHERE "ProductID"='{product_id}';''')
    
    # Combine all reviews into a single string
    combined_reviews = ' '.join(reviews_df['ReviewText'].tolist())

    # Initialize the LLM caller with the appropriate prompt
    gpt_caller = OpenAICaller("You are an assistant who helps with product review generation.")
    
    # Call the LLM with the combined reviews and a specific prompt
    generated_review = gpt_caller.call_llm(f"Here are the product reviews from several users: {combined_reviews} Based on this information, please generate a high-level summary review of the product in 1 to 2 sentences.")

    return generated_review

def pointwise_recommender_function(user_id, product_id):
    # Get user's review history
    user_reviews = run_query(f'''SELECT "ReviewText" FROM "Review" WHERE "UserID"='{user_id}';''')
    user_reviews_text = ' '.join(user_reviews['ReviewText'].tolist())
    
    # Get the product information
    product_info = run_query(f'''SELECT * FROM "Product" WHERE "ProductID"='{product_id}';''').iloc[0]
    
    # Initialize the LLM caller
    gpt_caller = OpenAICaller("You are an assistant who helps with product recommendations based on user review history.")
    
    # Call the LLM
    response = gpt_caller.call_llm(f"Here is the user's review history: {user_reviews_text} Based on this history, will the user like the product '{product_info['ProductName']}'? Please provide a rating between 1 and 5.")
    return response


def pairwise_recommender_function(user_id, product_id1, product_id2):
    # Get user's review history
    user_reviews = run_query(f'''SELECT "ReviewText" FROM "Review" WHERE "UserID"='{user_id}';''')
    user_reviews_text = ' '.join(user_reviews['ReviewText'].tolist())
    
    # Get information for both products
    product_info1 = run_query(f'''SELECT * FROM "Product" WHERE "ProductID"='{product_id1}';''').iloc[0]
    product_info2 = run_query(f'''SELECT * FROM "Product" WHERE "ProductID"='{product_id2}';''').iloc[0]
    
    # Initialize the LLM caller
    gpt_caller = OpenAICaller("You are an assistant who helps with product recommendations based on user review history.")
    
    # Call the LLM
    response = gpt_caller.call_llm(f"Here is the user's review history: {user_reviews_text} Based on this history, which product would the user prefer: '{product_info1['ProductName']}' or '{product_info2['ProductName']}'? Please provide your preference and reasoning.")
    
    return response

def listwise_recommender_function(user_id, product_ids):
    # Get user's review history
    user_reviews = run_query(f'''SELECT "ReviewText" FROM "Review" WHERE "UserID"='{user_id}';''')
    user_reviews_text = ' '.join(user_reviews['ReviewText'].tolist())
    
    # Get information for all products
    product_info_list = [run_query(f'''SELECT * FROM "Product" WHERE "ProductID"='{product_id}';''').iloc[0] for product_id in product_ids]
    product_names = ', '.join([product_info['ProductName'] for product_info in product_info_list])
    
    # Initialize the LLM caller
    gpt_caller = OpenAICaller("You are an assistant who helps with product recommendations based on user review history.")
    
    # Call the LLM
    response = gpt_caller.call_llm(f"Here is the user's review history: {user_reviews_text} Based on this history, how would the user rank the following products: {product_names}? Please provide the ranking from most to least preferred.")

    return response


def summarize_product_features_function(product_id):
    # Get the product information
    product_info = run_query(f'''SELECT "AboutProduct" FROM "Product" WHERE "ProductID"='{product_id}';''').iloc[0]['AboutProduct']
    
    # Initialize the LLM caller
    gpt_caller = OpenAICaller("You are an assistant who helps summarize product features.")
    
    # Call the LLM
    response = gpt_caller.call_llm(f"Here is the product information: {product_info} Please summarize the main features of this product into a short, easy-to-read summary of 1-2 paragraphs.")
    
    return response

app = FastAPI()

class ReviewRequest(BaseModel):
    product_id: str

class PointwiseRequest(BaseModel):
    user_id: str
    product_id: str

class PairwiseRequest(BaseModel):
    user_id: str
    product_id1: str
    product_id2: str

class ListwiseRequest(BaseModel):
    user_id: str
    product_ids: List[str]

class SummarizeRequest(BaseModel):
    product_id: str

@app.post("/make_review")
def make_review(request: ReviewRequest):
    return {"review": make_review_function(request.product_id)}

@app.post("/pointwise_recommender")
def pointwise_recommender(request: PointwiseRequest):
    return {"recommendation": pointwise_recommender_function(request.user_id, request.product_id)}

@app.post("/pairwise_recommender")
def pairwise_recommender(request: PairwiseRequest):
    return {"recommendation": pairwise_recommender_function(request.user_id, request.product_id1, request.product_id2)}

@app.post("/listwise_recommender")
def listwise_recommender(request: ListwiseRequest):
    return {"ranking": listwise_recommender_function(request.user_id, request.product_ids)}

@app.post("/summarize_product_features")
def summarize_product_features(request: SummarizeRequest):
    return {"summary": summarize_product_features_function(request.product_id)}

