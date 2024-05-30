# Homework 1

**Purpose: "\*" と "/" に対応する.**

1. read_multiply, read_devide 関数の追加
2. tokenize 関数で\*と/を処理
3. +or-は evaluate_plus_and_minus 関数で処理するように修正
4. evaluate 関数を、evaluate の流れを書いた関数に修正
    1. dummy の+を index=0 に追加
    2. \*or/ の処理
    3. +or- の処理
5. evaluate_multiply_and_devide 関数で計算
    - 0 で割った場合 ZeroDivisionError を raise
    - 計算結果 answer で「数値 \*or/ 数値」の tokens を置き換え  
      e.g. `3.0+4\*2−1` -> answer = 8 -> `3.0+answer-1`

**その他細かい仕様：**

-   negative numbers に対応
    e.g. `2\*-3` = -6
-   空白に対応
    e.g. `1 + 1` = 2
-   「+数値」に対応
    e.g. `2-+3` = -1
-   「0 数値」を除外："ERROR : Leading zeros are not allowed"を raise
    e.g. `1\*01`
-   FAIL を RED、ERROR を YELLOW で表示

# Homework 2

**Purpose: テストケースを考える.**

1. PASS するべきもの
    - +,-のみを含む
    - +, -, \*, /を含む
    - 0 を割る
    - 結果が大きい
    - negative numbers を含む
    - 「+数値」を含む
    - 空白" "を含む
2. ERROR を起こすべきもの
    - 0 で割る
    - 関係ない文字が混じっている
    - 「0 数値」

# Homework 3

**Purpose: 括弧に対応する.**

1. read_left_parethesis, read_right_parethesis 関数の追加
2. tokenize 関数で(と)を処理
3. evaluate 関数に括弧を処理する手順を追加
    1. dummy の+を index=0 に追加
    2. ()の中身の処理
    3. \*or/ の処理
    4. +or- の処理
4. evaluate_parethesis 関数で()の中身を再帰的に処理
    1. 括弧と閉じ括弧の数があっているか確認 (is_valid_parenthesis 関数)  
       -> False なら "Error : Unbalanced parentheses"を raise
    2. 括弧を見つけたら対応する閉じ括弧を探す (find_the_matching_parenthesis 関数)
    3. 括弧の中身を Evaluate 関数に通す (再帰)
    4. 計算結果 answer で「(計算式)」の tokens を置き換え  
       e.g. `(-2-2)*2` -> answer = -4 -> `-4*2`

# Homework 4

**Purpose: abs(), int(), round()に対応する.**

1. read_abs, read_int, read_round 関数の追加
2. tokenize 関数で abs,int,round を処理
3. evaluate 関数に abs,int,round を処理する手順を追加
    1. dummy の+を index=0 に追加
    2. ()の中身の処理
       -> abs,int,round の後ろの括弧も処理して削除  
       e.g. [ABS, 2, PLUS, 9]
    3. abs, int, round の処理
    4. \*or/ の処理
    5. +or- の処理
4. evaluate_abs_int_round 関数で計算
   前提：先に()を処理しているので、ABS/INT/ROUND の後ろには 1 つの数値のみ続く
    1. 各関数に通して計算
    2. 計算結果 answer で「ABS/INT/ROUND 数値」の tokens を置き換え  
        e.g. `12+abs(-12)` -> answer = 12 -> `12+12`

# Overall Module Structure

**Purpose: module 化する** : 機能ごとにファイル,関数を分割

-   main.py : test を走らせる  
    test, run_test, main
-   tokenizer.py : tokenize を行う  
    handle_negative_numbers, read_*, tokenize
-   evaluator.py : evaluate を行う  
    evaluate_*, evaluate
-   utils.py : 他ファイルで使用される helper 関数  
    for evaluate_parenthesis : is_valid_parenthesis, find_the_matching_parenthesis  
    for main : print_fail, print_error
