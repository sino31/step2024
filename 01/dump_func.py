# for anagram1(without sort function)
def word_sort(word):
    cnt = [0] * 26

    for c in word:
        index = ord(c) - ord('a')
        cnt[index] += 1

    sorted_word = ""
    for i in range(26):
        sorted_word += chr(ord('a') + i) * cnt[i]

    return sorted_word


def dict_merge_sort(dictionary):
    if len(dictionary) == 1:
        return dictionary

    mid = len(dictionary)//2
    sorted_a = dict_merge_sort(dictionary[:mid])
    sorted_b = dict_merge_sort(dictionary[mid:])

    c = []
    a_cnt, b_cnt = 0, 0
    while(a_cnt < len(sorted_a) or b_cnt < len(sorted_b)):
        if a_cnt == len (sorted_a):
            c.append(sorted_b[b_cnt])
            b_cnt += 1
        elif b_cnt == len(sorted_b):
            c.append(sorted_a[a_cnt])
            a_cnt += 1
        else:
            if sorted_a[a_cnt] <= sorted_b[b_cnt]:
                c.append(sorted_a[a_cnt])
                a_cnt += 1
            else:
                c.append(sorted_b[b_cnt])
                b_cnt += 1
    return c