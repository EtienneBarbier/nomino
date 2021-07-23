"""
Copyright (c) 2021 Etienne Barbier
Use of this source code is governed by an MIT-style
license that can be found in the LICENSE.md file or at
https://opensource.org/licenses/MIT.
"""

import os
import random
import json
from pathlib import Path


class NominoDictionariesDirectory:
    def __init__(self, directory):
        self._directory = directory
        self._load_directory(directory)

    def _load_directory(self, directory):
        files = os.listdir(directory)
        dictionaries_dict = {}
        for file in files:
            with open(directory + "/" + file) as json_file:
                data = json.load(json_file)
                dictionaries_dict[Path(json_file.name).resolve().stem] = data
        self._dictionaries = dictionaries_dict

    def reload(self):
        self._load_directory(self._directory)

    def dictionaries(self):
        dictionaries_list = list()
        for key, dictionary in self._dictionaries.items():
            entry = {"name": dictionary["name"], "id": key}
            dictionaries_list.append(entry)
        return dictionaries_list

    def dictionary(self, directory_id):
        return self._dictionaries[directory_id]


class NominoGenerator:
    def __init__(self, entry_dictionary):
        self._vowel_singles = [vowel[0] for vowel in entry_dictionary["vowel"]["singles"]]
        self._vowel_singles_weight = [vowel[1] * entry_dictionary["vowel"]["singles_weight"] for vowel in entry_dictionary["vowel"]["singles"]]
        self._consonant_singles = [consonant[0] for consonant in entry_dictionary["consonant"]["singles"]]
        self._consonant_singles_weight = [consonant[1] * entry_dictionary["consonant"]["singles_weight"] for consonant in entry_dictionary["consonant"]["singles"]]
        self._vowel_groups = [vowel_group[0] for vowel_group in entry_dictionary["vowel"]["groups"]]
        self._vowel_groups_weight = [vowel_group[1] * entry_dictionary["vowel"]["groups_weight"] for vowel_group in entry_dictionary["vowel"]["groups"]]
        self._consonant_groups = [consonant_group[0] for consonant_group in entry_dictionary["consonant"]["groups"]]
        self._consonant_groups_weight = [consonant_group[1] * entry_dictionary["consonant"]["groups_weight"] for consonant_group in entry_dictionary["consonant"]["groups"]]
        self._force_first_consonant = entry_dictionary["force_first_consonant"]
        self._force_last_vowel = entry_dictionary["force_last_vowel"]
        self._random_gen = random.Random()

    def _vowels_all(self):
        return self._vowel_singles + self._vowel_groups

    def _vowels_all_weight(self):
        return self._vowel_singles_weight + self._vowel_groups_weight

    def _consonants_all(self):
        return self._consonant_singles + self._consonant_groups

    def _consonants_all_weight(self):
        return self._consonant_singles_weight + self._consonant_groups_weight

    def _is_vowel(self, letter):
        return letter in self._vowels_all

    def _random_vowel(self, from_all=True):
        if from_all:
            return self._random_gen.choices(self._vowels_all(), self._vowels_all_weight())[0]
        else:
            return self._random_gen.choices(self._vowel_singles, self._vowel_singles_weight)[0]

    def _random_consonant(self, from_all=True):
        if from_all:
            return self._random_gen.choices(self._consonants_all(), self._consonants_all_weight())[0]
        else:
            return self._random_gen.choices(self._consonant_singles, self._consonant_singles_weight)[0]

    def _create_syllable(self, first=False, last=False, force_first_consonant=False, force_last_vowel=False):
        content = ""
        if first:
            if self._random_gen.choice([True, False]) and not force_first_consonant:
                content += self._random_vowel(True)
            else:
                content += self._random_consonant(False)
                content += self._random_vowel(True)
        elif last:
            if self._random_gen.choice([True, False]) or force_last_vowel:
                content += self._random_consonant(True)
                content += self._random_vowel(True)
            else:
                content += self._random_consonant(True)
                content += self._random_vowel(True)
                content += self._random_consonant(False)
        else:
            content += self._random_consonant(True)
            content += self._random_vowel(True)
        return content

    def _create_first_syllable(self, force_first_consonant=False):
        return self._create_syllable(True, False, force_first_consonant, False)

    def _create_last_syllable(self, force_last_vowel=False):
        return self._create_syllable(False, True, False, force_last_vowel)

    def create_word(self, nb_syllables):
        word = ""
        for count_syllables in range(nb_syllables):
            if count_syllables == 0:
                word += self._create_first_syllable(self._force_first_consonant)
            elif count_syllables == nb_syllables-1:
                word += self._create_last_syllable(self._force_last_vowel)
            else:
                word += self._create_syllable()
        return word

    @staticmethod
    def read_dictionary_file(file_name):
        with open(file_name) as json_file:
            data = json.load(json_file)
            return data
