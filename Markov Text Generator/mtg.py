# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 14:51:04 2022

@author: Yuanjing Zhu
"""


import random as rm


class SmartSentence(object):
    def __init__(self, contents):

        self.__contents = contents
        # ...string only...
        self.__nextword = []

    def whatisnextword(self, n, corpus, deterministic=True):

        realn = max(
            (len(self.__contents) + 1) * (n > len(self.__contents) + 1)
            + n * (n <= len(self.__contents) + 1),
            2,
        )

        for i in range(realn, 0, -1):

            core = self.__contents[-(i - 1) :]
            matched_words = []
            matched_frequency = []

            for j in range(len(corpus) - (i - 1)):

                # looking for the match
                if core == corpus[j : j + realn - 1]:

                    if corpus[j + realn - 1] in matched_words:
                        matched_frequency[
                            matched_words.index(corpus[j + realn - 1])
                        ] += 1

                    else:
                        matched_words.append(corpus[j + realn - 1])
                        matched_frequency.append(1)

            # if match then break the loop....

            if len(matched_words) > 0:

                if deterministic == True:
                    self.__nextword = matched_words[
                        matched_frequency.index(max(matched_frequency))
                    ]
                else:
                    self.__nextword = rm.choices(
                        matched_words, weights=matched_frequency
                    )[0]
                break

        return self.__nextword

    def finish_sentence(self, n, corpus, deterministic):

        while self.__contents[-1] not in {".", "?", "!"} and len(self.__contents) < 10:

            self.__contents.append(
                self.whatisnextword(n=n, corpus=corpus, deterministic=deterministic)
            )

        return self.__contents


def finish_sentence(sentence, n, corpus, deterministic=True):

    aa = SmartSentence(contents=sentence)
    # let it finish...
    return aa.finish_sentence(n=n, corpus=corpus, deterministic=deterministic)
