import numpy as np

def levenshteinDistance(word_1, word_2):
    word_1 = word_1.lower()
    word_2 = word_2.lower()
    word_matrix = np.zeros((len(word_2)+1,len(word_1)+1))
    word_matrix[0,:] = np.arange(len(word_1)+1)
    word_matrix[:,0] = np.arange(len(word_2)+1)
    for i in range(1,len(word_2)+1):
        for j in range(1,len(word_1)+1):
            if word_1[j-1] != word_2[i-1]:
                word_matrix[i,j] = min(word_matrix[i-1,j-1],word_matrix[i-1,j],word_matrix[i,j-1]) + 1
            else:
                word_matrix[i,j] = word_matrix[i-1,j-1]
    
    return word_matrix[-1,-1]