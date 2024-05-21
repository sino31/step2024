import sys

DICT_FILE = "words.txt"

SCORES = {
    'a': 1, 'b': 3, 'c': 2, 'd': 2, 'e': 1, 'f': 3, 'g': 3, 'h': 1,
    'i': 1, 'j': 4, 'k': 4, 'l': 2, 'm': 2, 'n': 1, 'o': 1, 'p': 3,
    'q': 4, 'r': 1, 's': 1, 't': 1, 'u': 2, 'v': 3, 'w': 3, 'x': 4,
    'y': 3, 'z': 4
}


def count_alphabet_and_score(word):
    cnt = [0] * 26
    score = 0
    for c in word:
        cnt[ord(c) - ord('a')] += 1
        score += SCORES[c]
    return cnt, score


def is_anagram(word_cnt, dict_word_cnt):
    for i in range(26):
        if word_cnt[i] < dict_word_cnt[i]:
            return False
    return True


def find_anagram2(words, dictionary):
    cnt_pair_dict = {}
    for word in dictionary:
        cnt_pair_dict[word] = count_alphabet_and_score(word)
    sorted_dict_with_score = sorted(cnt_pair_dict.items(), key=lambda item: item[1][1], reverse=True)

    results = []
    for word in words:
        word_cnt = {}
        word_cnt[word], _ = count_alphabet_and_score(word)
        for dict_w in sorted_dict_with_score:
            if is_anagram(word_cnt[word], dict_w[word]):
                results.append(word)
                break
    return results


def main(words_path):
    dictionary, words = [], []
    with open(DICT_FILE, 'r', encoding='utf-8') as dict_file:
        for line in dict_file:
            dictionary.append(line.strip())

    with open(words_path, 'r', encoding='utf-8') as words_file:
        for line in words_file:
            words.append(line.strip())

    anagrams = find_anagram2(words, dictionary)

    with open(f"output_{words_path}", 'w', encoding='utf-8') as file:
        for anagram in anagrams:
            file.write(f"{anagram}\n")



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: %s data_file" % sys.argv[0])
        exit(1)
    main(sys.argv[1])
