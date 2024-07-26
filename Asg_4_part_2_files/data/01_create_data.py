import pandas as pd
from faker import Faker

# Load the CSV file
file_path = 'amazon.csv'
amazon_data = pd.read_csv(file_path)

# Extract data for Product table
product_data = amazon_data[['product_id', 'product_name', 'about_product', 'rating', 'discounted_price']].copy()
product_data.rename(columns={
    'product_id': 'ProductID',
    'product_name': 'ProductName',
    'about_product': 'AboutProduct',
    'rating': 'ProductRating',
    'discounted_price': 'Price'
}, inplace=True)

# Extract data for Review table
review_data = amazon_data[['review_id', 'user_id', 'product_id', 'review_content', 'rating']].copy()
review_data.rename(columns={
    'review_id': 'ReviewID',
    'user_id': 'UserID',
    'product_id': 'ProductID',
    'review_content': 'ReviewText',
    'rating': 'Rating'
}, inplace=True)

# Extract and generate data for User table
user_data = amazon_data[['user_id', 'user_name']].copy()
user_data = user_data.drop_duplicates().copy()
user_data.rename(columns={
    'user_id': 'UserID',
    'user_name': 'UserName'
}, inplace=True)

# Generate fake email addresses for users
fake = Faker()
user_data['UserEmail'] = [fake.email() for _ in range(len(user_data))]

# Filter data to include only users with at least 3 reviews and products with at least 3 reviews
review_data = amazon_data[['user_id', 'product_id', 'review_id']]

user_review_counts = review_data['user_id'].value_counts()
users_with_3_or_more_reviews = user_review_counts[user_review_counts >= 3]

filtered_reviews = review_data[review_data['user_id'].isin(users_with_3_or_more_reviews.index)]

product_review_counts = filtered_reviews['product_id'].value_counts()
products_with_3_or_more_reviews = product_review_counts[product_review_counts >= 3]

final_filtered_reviews = filtered_reviews[filtered_reviews['product_id'].isin(products_with_3_or_more_reviews.index)]

final_user_review_counts = final_filtered_reviews['user_id'].value_counts()
final_users_with_3_or_more_reviews = final_user_review_counts[final_user_review_counts >= 3]

top_10_users = final_users_with_3_or_more_reviews.head(10)

final_data = final_filtered_reviews[final_filtered_reviews['user_id'].isin(top_10_users.index)]

# Prepare filtered data
final_product_data = amazon_data[amazon_data['product_id'].isin(final_data['product_id'].unique())][['product_id', 'product_name', 'about_product', 'rating', 'discounted_price']].copy()
final_product_data.rename(columns={
    'product_id': 'ProductID',
    'product_name': 'ProductName',
    'about_product': 'AboutProduct',
    'rating': 'ProductRating',
    'discounted_price': 'Price'
}, inplace=True)

final_review_data = amazon_data[amazon_data['review_id'].isin(final_data['review_id'].unique())][['review_id', 'user_id', 'product_id', 'review_content', 'rating']].copy()
final_review_data.rename(columns={
    'review_id': 'ReviewID',
    'user_id': 'UserID',
    'product_id': 'ProductID',
    'review_content': 'ReviewText',
    'rating': 'Rating'
}, inplace=True)

final_user_data = amazon_data[amazon_data['user_id'].isin(final_data['user_id'].unique())][['user_id', 'user_name']].drop_duplicates().copy()
final_user_data.rename(columns={
    'user_id': 'UserID',
    'user_name': 'UserName'
}, inplace=True)
final_user_data['UserEmail'] = [fake.email() for _ in range(len(final_user_data))]

# Save the final data as separate CSV files
final_product_data.to_csv('final_product_data.csv', index=False)
final_review_data.to_csv('final_review_data.csv', index=False)
final_user_data.to_csv('final_user_data.csv', index=False)
