def wordDictionary(path = 'count_1w.txt'):
    with open(path) as f:
        lines = f.readlines()
    dictionary = {}
    for word_freq in lines:
        [word, freq] = word_freq.strip().split('\t')
        dictionary[word] = int(freq)
    total_freq = sum(dictionary.values())
    for key, value in dictionary.items():
        dictionary[key] = value/total_freq
    return dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=True))