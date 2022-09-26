from levenshteinDistance import levenshteinDistance
from dictionary import wordDictionary
import numpy as np

dictionary = wordDictionary()
def corrector(wrongWord, p = 0.01):
    words = list(dictionary.keys())
    distance = np.array([levenshteinDistance(wrongWord, word) for word in dictionary.keys()])
    prob = np.array(list(dictionary.values()))
    weight = distance*np.log(p) + np.log(prob)
    word = words[np.argmax(weight)]
    return word

