import argparse
import string
import itertools
import math
abet = string.ascii_lowercase

def get_sys_word_list():
    """ Makes a list of all words found in the system dictionary file """
    dictionary = list()
    with open("/usr/share/dict/words", "r") as f:
        for line in f.readlines():
            dictionary.append(line.strip())
    return dictionary

def read_crypttext():
    crypttext = list()
    with open("LCR.txt", "r") as f:
        for line in f.readlines():
            crypttext.append(line.strip())
    return crypttext

def remove_symbols(word):
    word = word.strip()
    remove_list = [",","(",")","."]
    for symbol in remove_list:
        word = word.replace(symbol, "")
    return word

def letter_shift(letter, shift):
    index = abet.find(letter.lower())
    return abet[(index+shift) %26]

def do_lcr(letter):
    """ return left center right for letter """
#     print("LCR Letter: %s" % letter)
    if letter == "!":
        return ("a","z") #, "e", "i", "o", "u")
    else:
        return (letter_shift(letter, -1), letter_shift(letter, 0), letter_shift(letter, 1))

def find_options(lcrword):
    # Clean Word
    lcrword = remove_symbols(lcrword)
    print("Input Word: %s" % lcrword)
    test_list = list()
    lcrword = [do_lcr(x) for x in lcrword]
    # All combination of elements
    # https://stackoverflow.com/a/798893
    output = list(itertools.product(*lcrword))
    # Rebuild sets into word strings
    output = ["".join(combo) for combo in output]
    print("found %d possibilities" % len(output))
    return output

    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--word", type=str)
    parser.add_argument("--file", action="store_true")
    args = parser.parse_args()

    skip = 26
    valid_words = get_sys_word_list()
    if args.file:
        """ Process the cyphertext file """
        crypttext = read_crypttext()
        count = skip
        for word in crypttext[skip:]:
            count += 1
            print("")
            try:
                options = find_options(word)
                filtered = [x for x in options if x in valid_words]
                print("[%d] %s => %s" % (count, word, filtered))
            except KeyboardInterrupt:
                exit(0)
            except IndexError:
                print("%s: Skipping due to error" % word)

    if args.word:
        """ Just do one word you type in from command line"""
        options = find_options(args.word)
        filtered = [x for x in options if x in valid_words]
        print("%s => %s" % (args.word, filtered))


