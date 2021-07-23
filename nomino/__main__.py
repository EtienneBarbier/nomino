#!/usr/bin/env python
"""
Copyright (c) 2021 Etienne Barbier
Use of this source code is governed by an MIT-style
license that can be found in the LICENSE.md file or at
https://opensource.org/licenses/MIT.
"""

from nomino import *
import sys
import getopt


def help():
    print("Nomino word generator\n")
    print("Usage:")
    print("\tnomino.py -h")
    print("\tnomino.py")
    print("\tnomino.py -f <dictionary_file> -s <number_of_syllables> -n <number_of_words>")
    print("\tnomino.py -d <dictionary_directory>")
    print("")
    print("Options:")
    print("\t-h --help                                                  Display this current view.")
    print("\t-f --dictionary-file=<file> (=dictionaries/nomino.json)    Use given <file> as dictionary.")
    print("\t-s --number-of-syllables=<number> (=2)                     Number of syllables for generated words.")
    print("\t-n --number-of-words=<number> (=1)                         Number of generated words.")
    print("\t-d --dictionaries-directory=<directory>                    Display dictionaries information for given <directory>")


def main(argv):
    dictionary_file = 'dictionaries/nomino.json'
    nb_syllables = 2
    nb_words = 1
    try:
        opts, args = getopt.getopt(argv, "hf:s:d:n:", ["dictionary-file=", "number-of-syllables=", "dictionaries-directory=", "number-of-words="])
    except getopt.GetoptError:
        help()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            help()
            sys.exit()
        elif opt in ("-f", "--dictionary-file"):
            dictionary_file = arg
        elif opt in ("-s", "--number-of-syllables"):
            nb_syllables = int(arg)
        elif opt in ("-n", "--number-of-words"):
            nb_words = int(arg)
        elif opt in ("-d", "--dictionaries-directory"):
            dictionaries = NominoDictionariesDirectory(arg).dictionaries()
            print(dictionaries)
            sys.exit()

    dictionary = NominoGenerator.read_dictionary_file(dictionary_file)

    my_gen = NominoGenerator(dictionary)
    for i in range(nb_words):
        print(my_gen.create_word(nb_syllables))


if __name__ == '__main__':
    main(sys.argv[1:])
