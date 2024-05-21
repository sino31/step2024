import sys
import time

DICT_FILE = "words.txt"
# 単語の文字数：n
# 辞書の単語数：m
# 辞書の各単語の平均文字数：p
# 単語クエリの数：q

def count_alphabet(word): # O(len(word))
    cnt = [0] * 26
    for c in word:
        cnt[ord(c) - ord('a')] += 1
    return cnt


def is_anagram(word_cnt, dict_word_cnt): # O(1)
    for i in range(26):
        if word_cnt[i] < dict_word_cnt[i]:
            return False
    return True


def find_anagram2(words, dictionary): # O(mp) + O(qnm)
    cnt_pair_dict = []
    for word in dictionary: # O(m)
        cnt_pair_dict.append((word, count_alphabet(word))) # O(p)

    results = [] # これが大きい
    for word in words: # O(q)
        word_cnt_pair = (word, count_alphabet(word)) # O(n)
        anagram = []
        for word, cnt in cnt_pair_dict: # O(m)
            if is_anagram(word_cnt_pair[1], cnt): # O(1)
                anagram.append(word)
        results.append(anagram)
    return results


def calculate_score(word):
    SCORES = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2, 2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]
    score = 0
    for character in list(word):
        score += SCORES[ord(character) - ord('a')]
    return score


def main(words_path):
    dictionary, words = [], []
    with open(DICT_FILE, 'r', encoding='utf-8') as dict_file:
        for line in dict_file:
            dictionary.append(line.strip())

    with open(words_path, 'r', encoding='utf-8') as words_file:
        for line in words_file:
            words.append(line.strip())

    anagrams = find_anagram2(words, dictionary)

    start = time.time()
    max_scores = []
    for anagram_list in anagrams:
        max_score = (0, None)
        for anagram in anagram_list:
            current_score = calculate_score(anagram)
            if max_score[0] < current_score:
                max_score = (current_score, anagram)
        max_scores.append(max_score)
    end = time.time()
    print("find max score: ", end-start)

    with open(f"output_{words_path}", 'w', encoding='utf-8') as file:
        for (_, anagram) in max_scores:
            file.write(f"{anagram}\n")



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: %s data_file" % sys.argv[0])
        exit(1)
    main(sys.argv[1])
