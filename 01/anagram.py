import sys

DICT_FILE = "words.txt"

def find_matching_indices(sorted_dict, mid):
    first = last = mid
    while first > 0 and sorted_dict[first - 1][0] == sorted_dict[mid][0]:
        first -= 1
    while last < len(sorted_dict) - 1 and sorted_dict[last + 1][0] == sorted_dict[mid][0]:
        last += 1
    return list(range(first, last + 1))


def binary_search_in_dict(sorted_word, sorted_dict):
    anagram = []
    left, right = 0, len(sorted_dict) - 1
    while left <= right:
        mid = (left + right) // 2
        if sorted_word == sorted_dict[mid][0]:
            indices = find_matching_indices(sorted_dict, mid)
            anagram.extend([sorted_dict[i][1] for i in indices])
            break
        elif sorted_word < sorted_dict[mid][0]:
            right = mid - 1
        else:
            left = mid + 1
    return anagram


def find_anagram(words, dictionary):
    new_dictionary = [("".join(sorted(word)), word) for word in dictionary]
    new_dictionary.sort()

    results = []
    for word in words:
        sorted_word = "".join(sorted(word))
        anagram = binary_search_in_dict(sorted_word, new_dictionary)
        results.append(anagram)
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