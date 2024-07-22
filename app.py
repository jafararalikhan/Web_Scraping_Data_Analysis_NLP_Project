# -*- coding: utf-8 -*-
"""
@file name - app.py
@author - Jafar Ali Khan
@functionality -  text analysis, web scrapping, file operations
"""


#Import modules
import os
import pandas as pd
import string
import warnings
warnings.filterwarnings('ignore')

import requests
from bs4 import BeautifulSoup
from collections import Counter
from textblob import TextBlob

import nltk
from nltk.tokenize import word_tokenize
import re
import nltk
#nltk.download('punkt')

#output directory
directory = "Output"
if not os.path.exists(directory):
    os.makedirs(directory)

"""------- funtions-------"""
def read_web(url, url_id):
  '''web scraping'''
  try:
    response = requests.get(url)
    response.raise_for_status()  # Raises an HTTPError for bad responses

    # Parse the HTML content of the page with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the title of the article
    title = soup.title.text if soup.title else "No title found"

    # Extract the article text by combining all the text in <p> tags
    article_text = ' '.join(p.text for p in soup.find_all('p'))

    file = open(os.path.join( directory, f"{url_id}" +".txt" ), "w")
    file.write(str(title) + "\n\n" + str(article_text))
    file.close()

    return title, article_text

  except requests.RequestException as e:
    print(f"Request error: {e}")

def read_documents(folder_path):
    '''read documents from directory'''
    stopwords = set()
    # Iterate over every document in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):  # assuming the files are text files
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                # Read the file and split into words
                words = file.read().lower().split()
                # Add to the set of stopwords
                stopwords.update(words)
    return stopwords

def read_file(file_path):
    '''read file from directory'''
    words = set()
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
      # Read the file and split into words
      words = file.read().lower().split()
      # Add to the set of stopwords
      # words.update(words)
    return words

#Percentage of Complex words = the number of complex words / the number of words
def count_complex_words(words_list):
  c = 0
  for word in words_list:
    l = re.findall('(?! e$)[aeiou]+', word, re.I)+re.findall('[^aeiou]', word)
    if len(l) > 2:
      c = c + 1
  return c

def perc_complex(text):
  words = text.split()
  complex_words = count_complex_words(words)
  percentage = float(complex_words) / len(words) * 100
  return percentage


def read_documents(folder_path):
    stopwords = set()
    # Iterate over every document in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):  # assuming the files are text files
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                # Read the file and split into words
                words = file.read().lower().split()
                # Add to the set of stopwords
                stopwords.update(words)
    return stopwords

def read_file(file_path):
    words = set()
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
      # Read the file and split into words
      words = file.read().lower().split()
      # Add to the set of stopwords
      # words.update(words)
    return words


def remove_stopwords(text, stopwords_dict):
    words = text.split()
    filtered_words = [word for word in words if word not in stopwords_dict]
    return ' '.join(filtered_words)

def calculate_scores(text, positive_words, negative_words):
    # Tokenize the text
    tokens = word_tokenize(text)

    # Calculate Positive and Negative Scores
    positive_score = sum(1 for word in tokens if word in positive_words)
    negative_score = sum(1 for word in tokens if word in negative_words)

    # Calculate Polarity Score
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)

    return positive_score, negative_score, polarity_score


def count_complex_words(words_list):
  c = 0
  for word in words_list:
    l = re.findall('(?! e$)[aeiou]+', word, re.I)+re.findall('[^aeiou]', word)
    if len(l) > 2:
      c = c + 1
  return c

def perc_complex(text):
  words = text.split()
  complex_words = count_complex_words(words)
  percentage = float(complex_words) / len(words) * 100
  return percentage


def text_analysis(text, stopwords_dict, positive_words, negative_words):
  #'Function for text analysis'
  article_text = remove_stopwords(text, stopwords_dict )
  positive_score, negative_score, polarity_score = calculate_scores(article_text, positive_words, negative_words)
  subjectivity = TextBlob(article_text).sentiment.subjectivity
  average_sentence_length = len(word_tokenize(article_text)) / len(nltk.sent_tokenize(article_text))
  percentage_complex = perc_complex(article_text)
  complex_word_count = count_complex_words(word_tokenize(article_text))
  word_count = len(word_tokenize(article_text))
  syllable_count = sum(len(word) - word.count('-') for word in word_tokenize(article_text))
  personal_pronouns = len([token for token in word_tokenize(article_text) if token.lower() in ['i', 'me', 'my', 'we', 'us']])
  avg_word_length = sum(len(word) for word in word_tokenize(article_text)) / len(word_tokenize(article_text))
  fog_index = 0.4 * (average_sentence_length + perc_complex(article_text))
  avg_words_per_sentence = len(word_tokenize(article_text)) / len(nltk.sent_tokenize(article_text))

  return positive_score, negative_score, polarity_score, subjectivity, average_sentence_length, percentage_complex, complex_word_count, word_count, syllable_count, personal_pronouns, avg_word_length, fog_index, avg_words_per_sentence


def main():
   # Specify the path to your folder containing the documents

    input = pd.read_excel("Input.xlsx")

    stopwords_path = 'StopWords'
    stopwords_dict = read_documents(stopwords_path)
    stopwords_dict = list(stopwords_dict)

    n_ve_path = 'MasterDictionary/negative-words.txt'
    negative_words = read_file(n_ve_path)
    negative_words = list(negative_words)

    p_ve_path = 'MasterDictionary/positive-words.txt'
    positive_words = read_file(p_ve_path)
    positive_words = list(positive_words)

    positive_words = [word for word in positive_words if word not in stopwords_dict]
    negative_words = [word for word in negative_words if word not in stopwords_dict]
    
    #for index, row in input.head(5).iterrows():
    for index, row in input.iterrows():
      #read_web(row['URL'], row['URL_ID'])
      title, article_text = read_web(row['URL'], row['URL_ID'])
      positive_score, negative_score, polarity_score, subjectivity, average_sentence_length, percentage_complex, complex_word_count, word_count, syllable_count, personal_pronouns, avg_word_length, fog_index, avg_words_per_sentence = text_analysis(article_text, stopwords_dict, positive_words, negative_words)
      #POLARITY SCORE	SUBJECTIVITY SCORE	AVG SENTENCE LENGTH	PERCENTAGE OF COMPLEX WORDS	FOG INDEX	AVG NUMBER OF WORDS PER SENTENCE	COMPLEX WORD COUNT	WORD COUNT	SYLLABLE PER WORD	PERSONAL PRONOUNS	AVG WORD LENGTH

      print(positive_score, negative_score)
      input.loc[index, 'POSITIVE SCORE'] = positive_score
      input.loc[index, 'NEGTIVE SCORE'] = negative_score
      input.loc[index,'POLARITY SCORE'] = polarity_score
      input.loc[index,'SUBJECTIVITY SCORE'] = subjectivity
      input.loc[index,'AVG SENTENCE LENGTH'] = average_sentence_length
      input.loc[index,'PERCENTAGE OF COMPLEX WORDS'] = percentage_complex
      input.loc[index,'FOG INDEX'] = fog_index
      input.loc[index,'AVG NUMBER OF WORDS PER SENTENCE'] = avg_words_per_sentence
      input.loc[index,'COMPLEX WORD COUNT'] = complex_word_count
      input.loc[index,'WORD COUNT'] = word_count
      input.loc[index,'SYLLABLE PER WORD'] = syllable_count
      input.loc[index,'PERSONAL PRONOUNS'] = personal_pronouns
      input.loc[index,'AVG WORD LENGTH'] = avg_word_length
    
    input.to_excel('Output.xlsx')


if __name__ == "__main__":
   main()