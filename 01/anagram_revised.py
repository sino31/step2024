import sys

DICT_FILE = "words.txt"

def find_anagram(words, dictionary):
    new_dictionary = {}
    for word in dictionary:
        sorted_word = "".join(sorted(word))
        if sorted_word not in new_dictionary:
            new_dictionary[sorted_word] = [word]
        else:
            new_dictionary[sorted_word].append(word)

    results = []
    for word in words:
        sorted_word = "".join(sorted(word))
        if sorted_word in new_dictionary:
            results.append(new_dictionary[sorted_word])
        else:
            results.append([])
    return results


def main(words_path):
    dictionary, words = [], []
    with open(DICT_FILE, 'r', encoding='utf-8') as dict_file:
        for line in dict_file:
            dictionary.append(line.strip())

    with open(words_path, 'r', encoding='utf-8') as words_file:
        for line in words_file:
            words.append(line.strip())

    anagrams = find_anagram(words, dictionary)

    for word, anagram in zip(words, anagrams):
        print(f"anagrams for {word}: {anagram}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: %s data_file" % sys.argv[0])
        exit(1)
    main(sys.argv[1])