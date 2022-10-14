# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 14:29:57 2022

@author: Yuanjing Zhu
"""

import numpy as np
import nltk


# 10000 sentences for this time

tgt = nltk.corpus.brown.tagged_sents(tagset="universal")[0:10000]

tagseq = []
zidian = []

# output the tag sequence for all constions..

# fro the generation of the fundamental data

for sentence in tgt:
    for word in sentence:
        tagseq.append(word[1])
    tagseq = list(set(tagseq))


for sentence in tgt:
    for w in sentence:
        zidian.append(w[0])
    zidian = list(set(zidian))


# a fucntion to do
# using smoothing here


def smoothing(array, tpe):

    if tpe == 0:

        for i in range(array.shape[0]):
            array[i] = (array[i]) / (np.sum(array[i]))
    elif tpe == 1:
        array = array / (np.sum(array))

    return array


def observation(tgt=tgt, tagseq=tagseq):

    observmatrix = np.ones((len(tagseq), len(zidian)))

    for sentence in tgt:
        for word in sentence:
            observmatrix[tagseq.index(word[1]), zidian.index(word[0])] += 1

    return smoothing(observmatrix, 0)


def transition(tgt=tgt, tagseq=tagseq):

    transimatrix = np.ones((len(tagseq), len(tagseq)))

    for sentence in tgt:

        for i in range(len(sentence) - 1):

            transimatrix[
                tagseq.index(sentence[i][1]), tagseq.index(sentence[i + 1][1])
            ] += 1

    return smoothing(transimatrix, 0)


# should be n rows and 1 column for sure......
# very clear for sure..
#


def initial(tgt=tgt, tagseq=tagseq):

    initmatrix = np.ones((len(tagseq)))

    for sentence in tgt:

        initmatrix[tagseq.index(sentence[0][1])] += 1

    return smoothing(initmatrix, 1)


def match(llist, zidian=zidian):

    numberlist = []
    k = len(zidian)

    for word in llist:
        if word in zidian:
            numberlist.append(zidian.index(word))
        else:
            k -= 1
            numberlist.append(k)

    return numberlist


def showtag(numlist, zidian=tagseq):

    taglist = []

    for i in numlist:

        taglist.append(zidian[i])

    return taglist


# X as the string....A emmission matrix   B transition matrix........


# viterbi(obs=[1,1,2],pi=initial(),A=transition(),B=observation())


def viterbi(obs, pi=initial(), A=transition(), B=observation()):

    """Infer most likely state sequence using the Viterbi algorithm.

    Args:
        obs: An iterable of ints representing observations.
        pi: A 1D numpy array of floats representing initial state probabilities.
        A: A 2D numpy array of floats representing state transition probabilities.
        B: A 2D numpy array of floats representing emission probabilities.
    Returns:
        A tuple of:
        * A 1D numpy array of ints representing the most likely state sequence.
        * A float representing the probability of the most likely state sequence.
    """

    N = len(obs)
    Q, V = B.shape  # num_states, num_observations

    # d_{ti} = max prob of being in state i at step t
    #   AKA viterbi
    # \psi_{ti} = most likely state preceeding state i at step t......
    #  ...AKA backpointer...

    # initialization
    log_d = [np.log(pi) + np.log(B[:, obs[0]])]
    log_psi = [np.zeros((Q,))]

    # recursion
    for z in obs[1:]:
        log_da = np.expand_dims(log_d[-1], axis=1) + np.log(A)
        log_d.append(np.max(log_da, axis=0) + np.log(B[:, z]))
        log_psi.append(np.argmax(log_da, axis=0))

    # termination
    log_ps = np.max(log_d[-1])
    qs = [-1] * N
    qs[-1] = int(np.argmax(log_d[-1]))
    for i in range(N - 2, -1, -1):
        qs[i] = log_psi[i + 1][qs[i + 1]]

    return qs, np.exp(log_ps)


def validation(statis=1):

    newtgt = nltk.corpus.brown.tagged_sents(tagset="universal")[10150:10153]

    totalwords = 0
    correctwords = 0
    overallstatis = [[], [], []]

    for sentence in newtgt:

        obs = []
        trueanswer = []

        for word in sentence:

            obs.append(word[0])
            trueanswer.append(word[1])

            overallstatis[0].append(word[0])
            overallstatis[1].append(word[1])

        obs = match(obs)
        trueanswer = match(trueanswer, zidian=tagseq)

        totalwords += len(sentence)
        correctwords += np.sum(np.array(viterbi(obs=obs)[0]) == np.array(trueanswer))

        overallstatis[2].extend(showtag(viterbi(obs=obs)[0]))

    if statis == 0:
        return overallstatis

    else:
        return correctwords / totalwords


#print(validation(statis=1))
#print(validation(statis=0))
#print(transition())
#print(tagseq)
