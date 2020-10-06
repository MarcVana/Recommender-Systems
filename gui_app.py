'''
RECOMMENDER SYSTEM IN PYTHON

GUI VERSION

Based on MovieLens dataset.

@author: Marc
'''

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

'''
# Only for visualization purposes
plt.figure(figsize = (6, 9))
plt.hist(ratings['num of ratings'], bins = 70, color = 'blue', edgecolor = 'white')
plt.xlabel('Number of Ratings')
plt.ylabel('Count')
plt.title('Number of Ratings')
plt.savefig('number_of_ratings.png')
plt.close()

# Only for visualization purposes
plt.figure(figsize = (9, 6))
plt.hist(ratings['rating'], bins = 70, color = 'aqua', edgecolor = 'white')
plt.xlabel('Ratings (in stars)')
plt.ylabel('Count')
plt.title('Ratings')
plt.savefig('ratings_in_stars.png')
plt.close()

# Only for visualization purposes
sns.jointplot(x = 'rating', y = 'num of ratings', data = ratings, color = 'red')
plt.savefig('ratings_stars_vs_count.png')
plt.close()
'''

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

##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################

import tkinter as tk
from tkinter import *
from tkinter import ttk
import re

class FirstFrame(Frame):
    def __init__(self, *args, **kwargs):
        # Window
        Frame.__init__(self, *args, **kwargs, width = 600, height = 900)
        
        # Label
        self.search_label = Label(text = 'Search for a movie: ', font = ('Arial', 18))
        self.search_label.place(anchor = 'w', relx = 0.125, rely = 0.05)
        
        # Entry
        self.movie = ''
        self.main_entry = Entry(bd = 2, fg = 'red', font = ('Helvetica', 23), justify = 'center', width = 30)
        self.main_entry.place(anchor = 'w', relx = 0.025, rely = 0.1)
        
        # Note label
        note_label = Label(text = 'Note: You can also search the year if you do not remember the name.', font = ('Arial', 12))
        note_label.place(anchor = 'w', relx = 0.0375, rely = 0.15)
        
        # Search Button
        self.entry_button = Button(self, text = 'Search', font = ('Arial', 18), command = self.get_movie_name)
        self.entry_button.place(anchor = 'w', relx = 0.4, rely = 0.2)
        
        # List label
        list_label = Label(text = 'You need to select one of the movies below.', font = ('Arial', 12))
        list_label.place(anchor = 'w', relx = 0.0875, rely = 0.25)
        
        # Results list
        self.results_list = Listbox(width = 50, height = 15, bd = 2, fg = 'red', font = ('Helvetica', 15), justify = 'center', selectmode = tk.SINGLE)
        self.results_list.place(anchor = 'center', relx = 0.2, rely = 0.55)
        self.results_list.config(width = 0)
        self.update_list()
        # Results button
        self.recommender_button = Button(self, text = 'GET RECOMMENDATIONS', font = ('Arial', 18), command = self.get_recommendation)
        self.recommender_button.place(anchor = 'w', relx = 0.25, rely = 0.85)
        
    def get_movie_name(self):
        self.movie = self.main_entry.get()
        self.update_list()
        
    def get_recommendation(self):
        movie = self.results_list.get(self.results_list.curselection())
        global recommendations
        recommendations = find_recommendations(movie)
        recommendations = recommendations[1:16]
        self.update_table()
    
    def update_list(self):
        if self.movie == '':
            for i in range(len(movies)):
                self.results_list.insert(i, movies[i])
        else:
            self.results_list.delete(0, 'end')
            current = 0
            for movie in movies:
                if re.search(self.movie.lower(), movie.lower()):
                    self.results_list.insert(current, movie)
                    ++current
                    
    def update_table(self):
        global recommendations, tree
        for i in tree.get_children():
            tree.delete(i)
        for i in range(1, 16):
            tree.insert("", i, text = list(recommendations.index.values)[i - 1],
                        values = (int(recommendations.loc[list(recommendations.index.values)[i - 1]]['num of ratings']),
                                  str(int(recommendations.loc[list(recommendations.index.values)[i - 1]]['Correlation'] * 100)) + '%'),
                        tag = 'movie')
                    
class SecondFrame(Frame):
    def __init__(self, *args, **kwargs):
        # Window
        Frame.__init__(self, *args, **kwargs, width = 900, height = 900, bg = 'white')
        
        # Title
        self.title = Label(text = 'RECOMMENDATIONS', font = ('Arial', 23))
        self.title.place(anchor = 'e', relx = 0.8, rely = 0.05)
        
        # Table
        global tree
        tree=ttk.Treeview(self, height = 15)
        tree.place(anchor = 'e', relx = 0.95, rely = 0.5)
        style = ttk.Style()
        style.configure('Treeview.Heading', font = (None, 15))
        style.configure('Treeview', rowheight = 40)
        tree.tag_configure('movie', font = ('Helvetica', 20))
        # Table columns
        tree["columns"]=("one","two")
        tree.column("#0", width = 600,  stretch = tk.NO)
        tree.column("one", width = 90, stretch = tk.NO)
        tree.column("two", width = 110, stretch = tk.NO)
        # Table Headings
        tree.heading("#0", text = "   Movie Name", anchor = tk.W)
        tree.heading("one", text = "Ratings", anchor = tk.W)
        tree.heading("two", text = "Correlation", anchor = tk.W) 
    
if __name__ == "__main__":
    root = tk.Tk()
    root.title('Recommender Systems')
    FirstFrame(root).pack(side = 'left')
    SecondFrame(root).pack(side = 'right')
    root.mainloop()