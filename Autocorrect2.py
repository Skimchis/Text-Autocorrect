import random

import math


def load_dictionary(path="Dictionary.txt"):  # Dictionary for words wih popularity
    words = set()
    rank_w = {}
    with open(path, "r", encoding="utf-8") as f:
        # The 'rank'/popularity of the word is based on how high it is on the list
        for i, line in enumerate(f):
            w = line.strip().lower()
            if not w:
                continue
            words.add(w)
            rank = i + 1
            rank_w[w] = (1.0) / rank
    return words, rank_w  # Making a dictionary with the rank system,


DICTIONARY, RANK_W = load_dictionary("Dictionary.txt")  # Set up the dictionary

ADJ = {  # Dictionary for letters
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
    # Function to make a list of pairs, enter the key from the keyboard (will be a list) and gives pairs in format : (neighbouring key, probability of that key being the correct key)
    base = key[0].lower()

    # Sets up a list with all the neighbours (extracting from the ADJ dictionary)
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
    Prob_Pairs.append((base, Probability_key))  # List of pairs
    p = (1 - Probability_key) / len(neighbours)

    j = 0
    while j < len(neighbours):
        k = neighbours[j]
        Prob_Pairs.append((k, p))
        j += 1

    return Prob_Pairs


def letter_options_loop(ch, ADJ, p=0.80):
    # Given the character, makes the list with the neighbour keys so that we can input that list into the above function

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
    # Function takes the word and the dictionary to create a list for each letter in the word containing
    w = word.lower()
    per_letter = []  # A list containing lists of options for each letter of the word

    i = 0  # Loop through each letter in the word
    while i < len(w):
        ch = w[i]
        # A list too with the options for each letter
        opts = letter_options_loop(ch, ADJ, 0.80)
        per_letter.append(opts)
        i += 1

    return per_letter


# Word Replacement Options chosen from the options of letters
def word_candidates(word, ADJ, p=0.80):
    per_letter = per_letter_opt(word, ADJ, 0.80)

    partials = [("", 1.0)]  # Empty list to begin with

    pos = 0  # Position of the letters
    while pos < len(per_letter):
        next_partials = []  # Load up the next list to include

        i = 0  # For each letter we want to take the already set up partials and in the next loop add letter options
        while i < len(partials):
            # Take out the probability of the previously arranged small bit of the word alongside the actual bit
            prefix, p_prefix = partials[i]

            j = 0  # For each letter we are now checking each option out
            while j < len(per_letter[pos]):
                # Taking the letter options for the letter in position pos, taking letter in position j of the possible options
                letter, p_letter = per_letter[pos][j]
                new_word = prefix + letter  # Previous preix added with each possible letter option
                # Multiply the probability ih every probability option
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
    # Function that outputs the suggest word(s)
    best_suggestion = word.lower()  # Set the best_suggestion up first
    p_max = 0.0  # Assume a probability of 0, so any option that exists has a higher probability

    # Take all the candidates into a list
    candidates = word_candidates(word, ADJ, p=0.80)

    best = -1.0  # Starting 'score'
    tied = []  # The list that'll contain all words that are considered for suggestion

    i = 0
    while i < len(candidates):
        c, prob_c = candidates[i]  # Taking out items from the pair
        if (c in DICTIONARY):  # Being in the dictionary is most important
            pop = RANK_W.get(c, 0.0)  # Taking popularity value
            score = prob_c * (pop ** scale)  # Taking a score valuie
            if score > best + tol:  # If the score of larger, take new word
                best = score  # Set the new best score as this new word and make it the list. Then keep continuing through all the options
                tied = [c]
            # If scores are similar, add to a list together (if multiple words have the same score)
            elif abs(best - score) <= tol:
                tied.append(c)
        i += 1
    return tied


def Autocorrected_word(word):
    return suggested_words(word, DICTIONARY, ADJ, RANK_W, p=0.6, scale=0.7, tol=1e-12)


print(Autocorrected_word("cooo"))


# Final function, takes the probabilities and narrows down to words in the dictionary and highest probability
