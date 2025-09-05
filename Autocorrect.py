import random

import math


def load_dictionary(path="Dictionary.txt"):  #Dictionary for words wih popularity
    words = set()
    rank_w = {}
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            w = line.strip().lower()
            if not w:
                continue
            words.add(w)
            rank = i + 1
            rank_w[w] = (1.0) / rank
    return words, rank_w


DICTIONARY, RANK_W = load_dictionary("Dictionary.txt")

ADJ = { #Dictionary for letters
    'q': ['q', 'a', 's', 'w'],
    'w': ['w', 'q', 'a', 's', 'd', 'e'],
    'e': ['e', 'w', 's', 'd', 'f', 'r'],
    'r': ['r', 'e', 'd', 'f', 'g', 't'],
    't': ['t', 'r', 'f', 'g', 'h', 'y'],
    'y': ['y', 't', 'g', 'h', 'j', 'u'],
    'u': ['u', 'y', 'h', 'j', 'k', 'i'],
    'i': ['i', 'o', 'l', 'k', 'j', 'u'],
    'o': ['o', 'i', 'k', 'l', 'p'],
    'p': ['p', 'o', 'l'],
    'a': ['a', 'q', 'w', 's', 'z'],
    's': ['s', 'a', 'w', 'e', 'd', 'x', 'z'],
    'd': ['d', 's', 'e', 'r', 'f', 'c', 'x'],
    'f': ['f', 'd', 'r', 't', 'g', 'v', 'c'],
    'g': ['g', 'f', 't', 'y', 'h', 'b', 'v'],
    'h': ['h', 'b', 'g', 'y', 'u', 'j', 'n'],
    'j': ['j', 'h', 'u', 'i', 'k', 'm', 'n'],
    'k': ['k', 'j', 'i', 'o', 'l', 'm'],
    'l': ['l', 'k', 'o', 'p'],
    'z': ['z', 'a', 's', 'x'],
    'x': ['x', 'z', 's', 'd', 'c'],
    'c': ['c', 'x', 'd', 'f', 'v'],
    'v': ['v', 'c', 'f', 'g', 'b'],
    'b': ['b', 'v', 'g', 'h', 'n'],
    'n': ['n', 'b', 'h', 'j', 'm'],
    'm': ['m', 'n', 'j', 'k']
}


def probabilities_per_key(key, Probability_key=0.80):
    base = key[0].lower()

    neighbours = []
    i = 1
    while i < len(key):
        c = key[i].lower()
        if c != base and c not in neighbours:
            neighbours.append(c)
        i += 1

    if len(neighbours) == 0:
        return [(base, 1.0)]

    Prob_Pairs = []
    Prob_Pairs.append((base, Probability_key))
    p = (1 - Probability_key) / len(neighbours)

    j = 0
    while j < len(neighbours):
        k = neighbours[j]
        Prob_Pairs.append((k, p))
        j += 1

    return Prob_Pairs


def letter_options_loop(ch, ADJ, p=0.80):  # Getting lsit of options

    ch = ch.lower()

    l = [ch]

    k = 0
    while k < len(ADJ[ch]):  # List of letter options

        c = ADJ[ch][k].lower()
        if c != ch and c not in l:
            l.append(c)
        k += 1

    return probabilities_per_key(l)


# List of options for each letter with probabilities
def per_letter_opt(word, ADJ, p=0.80):
    w = word.lower()
    per_letter = []

    i = 0  # Loop through each letter in the word
    while i < len(w):
        ch = w[i]
        opts = letter_options_loop(ch, ADJ, 0.80)  # A list too
        per_letter.append(opts)
        i += 1

    return per_letter


def word_candidates(word, ADJ, p=0.80):  # Word Replacement Options
    per_letter = per_letter_opt(word, ADJ, 0.80)

    partials = [("", 1.0)]

    pos = 0  # Position of the letters
    while pos < len(per_letter):
        next_partials = []

        i = 0  # For each letter we want to take the already set up partials and in the next loop add letter options
        while i < len(partials):
            prefix, p_prefix = partials[i]

            j = 0  # For each letter we are now checking each option out
            while j < len(per_letter[pos]):
                # Taking the letter options for the letter in position pos, taking letter in position j of the possible options
                letter, p_letter = per_letter[pos][j]
                new_word = prefix + letter
                new_prob = p_prefix * p_letter
                # New partials list with new word types and their probabiliy into a pair
                next_partials.append((new_word, new_prob))
                j += 1
            i += 1
        # After loop partials will be filled with all possible options of words
        partials = next_partials
        pos += 1
    return partials


def suggested_words(word, DICTIONARY, ADJ, RANK_W, p=0.6, scale=5, tol=1e-12):
    best_suggestion = word.lower()
    p_max = 0.0

    candidates = word_candidates(word, ADJ, p=0.80)

    best = -1.0  #Starting 'score'
    tied = []

    i = 0
    while i < len(candidates):
        c, prob_c = candidates[i]  #Taking out items from the pair
        if (c in DICTIONARY):  #Being in the dictionary is most important
            pop = RANK_W.get(c, 0.0)  #Taking popularity value
            score = prob_c * (pop ** scale) #Taking a score valuie
            if score > best + tol:  #If the score of larger, take new word
                best = score
                tied = [c]
            elif abs(best - score) <= tol: #If scores are similar, add to a list together
                tied.append(c)
        i += 1
    return tied


def Autocorrected_word(word):
    return suggested_words(word, DICTIONARY, ADJ, RANK_W, p=0.6, scale=0.7, tol=1e-12)


print(Autocorrected_word("cooo"))


# Final function, takes the probabilities and narrows down to words in the dictionary and highest probability
