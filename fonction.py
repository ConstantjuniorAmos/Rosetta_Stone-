
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
from keras.models import load_model
import numpy as np
import tensorflow as tf
import pickle
import nltk
nltk.download('punkt')

import string

from nltk.tokenize import word_tokenize

models=load_model('./model.h5')
with open('./english_tokenizer.txt') as f:
    contents = f.readlines()



# loading
with open('english_tokenizer.pickle', 'rb') as handle:
    tokenizer_mod = pickle.load(handle)
with open('preproc_english_sentences.pickle', 'rb') as handle:
    preproc_english_sentences = pickle.load(handle)

with open('french_tokenizer.pickle', 'rb') as handle:
    french_tokenizer = pickle.load(handle)




def translate(corpus):
    y_id_to_word = {value: key for key, value in french_tokenizer.word_index.items()}
    y_id_to_word[0] = ''
    # sentence = 'he saw a old yellow truck'
    tokens = word_tokenize(corpus.lower())
    
    tokens =' '.join( list(filter(lambda token: token not in string.punctuation, tokens)))
    sentence = []
    unknow_word = []
    for word in tokens.split():
        if word in tokenizer_mod.word_index:
            sentence.append(tokenizer_mod.word_index[word])
        else:
            unknow_word.append(word)
            sentence.append(505)
    if 505 not in sentence:
        sentence = pad_sequences([sentence], maxlen=preproc_english_sentences.shape[-1], padding='post')
        predictions = models.predict(sentence, len(sentence))
        return ' '.join([y_id_to_word[np.argmax(x)] for x in predictions[0]])
    else:
        return [505,unknow_word]
