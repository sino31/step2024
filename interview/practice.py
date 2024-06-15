"""
同じ文字が何文字連続するかによって圧縮を行う

"aabbbBBccc" => "a2b3B2c3"
"a" => "a1"
"aba" => "a1b1a1"
"" => ""
"aaaaaa" => "a6"

・前から見ていって、連続する文字数をカウントして出力していく -> O(n^2)？
"""

def run_length(s):
    result = ""
    i = 0
    while i < len(s):
        cnt = 1
        j = i + 1
        while j < len(s) and s[i] == s[j]:
            cnt += 1
            j += 1
        result += s[i]
        result += str(cnt)
        i = j

    return result

assert run_length("aabbbBBccc") == "a2b3B2c3"
assert run_length("a") == "a1"
assert run_length("aba") == "a1b1a1"
assert run_length("") == ""

"""
逆に解凍する

"a2b3B2c3" => "aabbbBBccc"
"a1" => "a"
"a1b1a1" => "aba"
"" => ""
"a10b3" => "aaaaaaaaaabbb"

"ab3" =>
"3a" =>
alhpaを数えたかどうかのflagで対処できる

・前から見て今見ている文字が英字or数字を確認 -> 英字はそのまま、数字の間進めてint
"""

def rev_run_length(s):
    result = ""
    i = 0
    while i < len(s):
        if s[i].isalpha():
            i += 1
        elif s[i].isdigit():
            j = i
            while j < len(s) and s[j].isdigit():
                j += 1
            num = int(s[i:j])
            result += s[i-1]*num
            i = j

    return result

assert rev_run_length("a2b3B2c3") == "aabbbBBccc"
assert rev_run_length("a1") == "a"
assert rev_run_length("a1b1a1") == "aba"
assert rev_run_length("") == ""

"""
"aaa55" => "a352" => a*352 or a*3, 5*2
"aaa55" => "a3\52"
"aa1111111111" => "a2\110"
"""

def run_length2(s):
    result = ""
    i = 0
    while i < len(s):
        cnt = 1
        j = i + 1
        while j < len(s) and str[i] == str[j]:
            cnt += 1
            j += 1
        result += str[i]
        result += str(cnt)
        i = j

    return result


def encode(raw):
  encoded = ''
  current = None
  for char in raw:
    if current is None:
      current = char
      count = 1
    elif current == char:
      count += 1
    else:
      encoded += _output_encoded(current, count)
      current = char
      count = 1
  encoded += _output_encoded(current, count)
  return encoded

def _output_encoded(char, count):
  prefix = '\\' if char.isdecimal() else ''
  return prefix + char + str(count)


def decode(encoded):
  raw = ''
  current = None
  count = None
  for char in encoded:
    if char == '\\':
      if current is not None:
        raw += current * count
        current = None
        count = None
    elif current is None:
      current = char
    elif char.isdecimal():
      if count is None:
        count = int(char)
      else:
        count *= 10
        count += int(char)
    else:
      raw += current * count
      current = char
      count = None

  raw += current * count
  return raw
