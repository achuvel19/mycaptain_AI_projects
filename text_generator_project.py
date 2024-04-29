# -*- coding: utf-8 -*-
"""text generator project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/18jFcXNZaLuzzVvmejV8Qeim2raLEdGtm
"""

import numpy
import sys
import nltk
nltk.download('stopwords')
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint

file = open("frankenstein.txt").read()

def tokenize_words(input):
  input = input.lower()
  tokenizer = RegexpTokenizer('r/w+')
  tokens = tokenizer.tokenize(input)
  filtered = filter(lambda token: token not in stopwords.words('english'), tokens)
  return "".join(filtered)

processed_inputs = tokenize_words(file)

chars = sorted(list(set(processed_inputs)))
char_to_num = dict((c,i) for i, c in enumerate(chars))

input_len = len(processed_inputs)
vocab_len = len(chars)
print ("Total number of characters:", input_len)
print ("Total vocab:", vocab_len)

seq_length = 100
x_data = []
y_data = []

for i in range(0, input_len - seq_length, 1):
  in_seq = processed_inputs[i:i + seq_length]
  out_seq = processed_inputs[i + seq_length]
  x_data.append([char_to_num[char] for char in in_seq])
  y_data.append([char_to_num[out_seq]])

n_patterns = len(x_data)
print ("Total Patterns:", n_patterns)

X = numpy.reshape(x_data, (n_patterns, seq_length))
X = X/float(vocab_len)

y = np_utils.to_categorical(y_data, num_classes=None)

model = Sequential()
model.add(LSTM(256, input_shape=(X.shape[1], X.shape[1]), return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(256, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(128))
model.add(LSTM(128))
model.add(Dropout(0.2))
model.add(Dense(y.shape[1], activation='softmax'))

model.compile(loss= 'categorical_crossntropy', optimizer='adam')

filepath = "model_weights_saved.kdf5"
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose = 1, save_best_only=True, mode='min')
desired_callbacks = [checkpoint]

model.fit(X,y, epochs=4, batch_size=256, callbacks=desired_callbacks)

filename = "model_weights_saved.hdf5"
model.load_weights(filename)
model.compile(loss= 'categorical_crossntropy', optimizer= 'adam')

for i in range (1000):
  x = numpy.reshape(pattern, (1,len(pattern), 1))
  x = x/float(vocab_len)
  prediction = model.predict(x, verhose=0)
  index = numpy.argmax(prediction)
  result = num_to_char[index]
  seq_in = [num_to_char[value] for value in pattern]
  sys.stdout.write(result)
  pattern.append(index)
  pattern = pattern[1:len(pattern)]