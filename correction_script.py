import re
from collections import Counter
import numpy as np
import pandas as pd

# Preprocess text data
def process_text(path):
    words = []
    with open(path) as f:
        file_name_data = f.read()
    file_name_data = file_name_data.lower()
    words = re.findall(r'\w+', file_name_data)
    return words

# Load words from the text file and prepare vocabulary
book_words = process_text('alice_in_wonderland.txt')
vocab = set(book_words)

# Create a counter dictionary for word frequency
def get_count(words):
    word_count_dict = Counter(words)
    return word_count_dict

word_count_dict = get_count(book_words)

# Calculate probability of occurrence for each word
def occurr_prob(word_count_dict):
    probs = {}
    m = sum(word_count_dict.values())
    for key in word_count_dict:
        probs[key] = word_count_dict[key] / m
    return probs

prob_of_occurr = occurr_prob(word_count_dict)

# Define edit distance functions
def del_letter(word):
    del_letter = []
    split_letter = []
    for i in range(len(word)):
        split_letter.append([word[:i], word[i:]])
    for a, b in split_letter:
        del_letter.append(a + b[1:])
    return del_letter

def switch_letter(word):
    sw_letter = []
    split_letter = []
    for c in range(len(word)):
        split_letter.append([word[:c], word[c:]])
    sw_letter = [a + b[1] + b[0] + b[2:] for a, b in split_letter if len(b) >= 2]
    return sw_letter

def replace_letter(word):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    repl_let = []
    split_let = []
    for c in range(len(word)):
        split_let.append([word[:c], word[c:]])
    repl_let = [a + l + (b[1:] if len(b) > 1 else '') for a, b in split_let if b for l in letters]
    repl_set = set(repl_let)
    repl_set.discard(word)  # Avoid including the original word itself
    return sorted(list(repl_set))

def insert_letter(word):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    ins_let = []
    split_let = []
    for c in range(len(word) + 1):
        split_let.append([word[:c], word[c:]])
    ins_let = [a + l + b for a, b in split_let for l in letters]
    return ins_let

# Edit distance functions
def edit_one_letter(word, allow_switches=True):
    edit_one_set = set()
    edit_one_set.update(del_letter(word))
    if allow_switches:
        edit_one_set.update(switch_letter(word))
    edit_one_set.update(replace_letter(word))
    edit_one_set.update(insert_letter(word))
    return edit_one_set

def edit_two_letter(word, allow_switches=True):
    edit_two_set = set()
    edit_one = edit_one_letter(word, allow_switches=allow_switches)
    for w in edit_one:
        if w:
            edit_two = edit_one_letter(w, allow_switches=allow_switches)
            edit_two_set.update(edit_two)
    return edit_two_set

# Get list of suggested words
def get_correlations(word, probs, vocab, n=5):
    # Generate suggestions (with at most 5 edits) that are in the vocabulary
    suggestions = list((word in vocab and word) or 
                       edit_one_letter(word).intersection(vocab) or 
                       edit_two_letter(word).intersection(vocab))
    
    # Sort suggestions by probability (highest first) and return the top n
    n_best = sorted([[s, probs.get(s, 0)] for s in suggestions], key=lambda x: x[1], reverse=True)[:n]
    
    return n_best
