"""
Created on Mon Oct  5 15:56:10 2020

SIMPLE RECOMMENDER SYSTEM (RATING BASED)

Based on MovieLens dataset.

@author: Marc
"""
# Importing the libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set the column names
column_names = ['user_id', 'item_id', 'rating', 'timestamp']

# Loading the data
df = pd.read_csv('u.data', sep = '\t', names = column_names)
movie_data = pd.read_csv('Movie_Id_Titles.csv')
df = df.merge(movie_data, on = 'item_id')
movies = movie_data['title'].tolist()

# Creating a dataframe for ratings
ratings = pd.DataFrame(df.groupby('title')['rating'].mean())
ratings['num of ratings'] = pd.DataFrame(df.groupby('title')['rating'].count())

# Only for visualization purposes
plt.figure(figsize = (6, 9))
plt.hist(ratings['num of ratings'], bins = 70, color = 'blue', edgecolor = 'white')
plt.xlabel('Number of Ratings')
plt.ylabel('Count')
plt.title('Number of Ratings')
plt.savefig('number_of_ratings.png')

# Only for visualization purposes
plt.figure(figsize = (9, 6))
plt.hist(ratings['rating'], bins = 70, color = 'aqua', edgecolor = 'white')
plt.xlabel('Ratings (in stars)')
plt.ylabel('Count')
plt.title('Ratings')
plt.savefig('ratings_in_stars.png')

# Only for visualization purposes
sns.jointplot(x = 'rating', y = 'num of ratings', data = ratings, color = 'red')
plt.savefig('ratings_stars_vs_count.png')

def find_recommendations(movie):
    # Correlation -> Recommender system
    movie_matrix = df.pivot_table(index = 'user_id', columns = 'title', values = 'rating')
    movie_user_ratings = movie_matrix[movie]
    similar_to_movie = pd.DataFrame(movie_matrix.corrwith(movie_user_ratings), columns = ['Correlation'])
    similar_to_movie = similar_to_movie.join(ratings['num of ratings'])
    
    # Threshold for number of ratings
    threshold = 75
    best_similar_to_movie = similar_to_movie[similar_to_movie['num of ratings'] > threshold].sort_values('Correlation', ascending = False)
    return best_similar_to_movie