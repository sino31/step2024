### Homework 1

**purpose: find_shortest_path 関数で最短経路を求める**

-   BFS を使用し、キューに追加するノードを (PageID, その PageID に辿り着くまでの経路) のタプルにする
-   title_to_id,id_to_titld 関数：PageID と PageTitle を変換する関数

### Homework 2

**purpose: find_most_popular_pages 関数で pagerank を計算し、重要度の高いページ top10 を求める**

-   全体で 1.0 の pagerank を持つ
-   85%の確率で現在のページに存在する link から次のページへ遷移する
-   15%の確率で完全に random なページを開く
-   収束条件：sum(新しい pagerank-１つ前の pagerank)^2 < 0.01
-   引数:
    -   max_iterations: 最大反復回数
    -   p: リンクで遷移する確率
    -   convergence_eps: 収束の許容誤差. 計算が収束したと見なすための基準
    -   assert_eps: rank 分配時に割り切れない場合の丸め誤差による assert を防ぐための許容誤差

1. 全てのページのランクを 1.0 / (全てのページ数) で初期化.
2. max_iterations に到達する or 収束条件を満たすまで、以下の処理を繰り返す.
   2-1. 新しい pagerank を格納する new_pagerank を生成.  
   2-2. 15% を全ノードに均等に分配.  
   2-3. 全てのページ(self.title)に対して
    - ページが link を持つ時は 85%を「全ての link 先に」均等に分配
    - ページが link を持たない場合は 85%を「全ての node に」均等に分配
3. pagerank が収束したかどうか確認
   前回の pagerank と新しく計算した new_pagerank の差の合計を計算し、その 2 乗が誤差範囲内かどうか判別
4. pagerank を new_pagerank に更新
5. 「全部のノードのページランクの合計値」が一定に保たれていることを確認
   pagerank の合計を計算し、その合計と元の rank 合計 1.0 の差が誤差範囲内であることを確認する
6. pagerank の多い順に sort し、top10 を出力

### code execution result

**small**

```
time python wikipedia.py wikipedia_dataset/pages_small.txt wikipedia_dataset/links_small.txt
Finished reading wikipedia_dataset/pages_small.txt
Finished reading wikipedia_dataset/links_small.txt

The longest titles are:
A
B
C
D
E
F

The most linked pages are:
B 3

The shortest path from 'A' to 'D' is:
A
B
D

The 10 most popular pages are:
0: C
1: D
2: B
3: E
4: F
5: A
python wikipedia.py wikipedia_dataset/pages_small.txt   0.03s user 0.01s system 78% cpu 0.048 total
```

**midium**

```
time python wikipedia.py wikipedia_dataset/pages_medium.txt wikipedia_dataset/links_medium.txt
Finished reading wikipedia_dataset/pages_medium.txt
Finished reading wikipedia_dataset/links_medium.txt

The longest titles are:
日本国とアメリカ合衆国との間の相互協力及び安全保障条約第六条に基づく施設及び区域並びに日本国における合衆国軍隊の地位に関する協定の実施に伴う刑事特別法
一般社団法人及び一般財団法人に関する法律及び公益社団法人及び公益財団法人の認定等に関する法律の施行に伴う関係法律の整備等に関する法律案
日本国とアメリカ合衆国との間の相互協力及び安全保障条約第 6 条に基づく施設及び区域並びに日本国における合衆国軍隊の地位に関する協定
日本国とアメリカ合衆国との間の相互協力及び安全保障条約第六条に基づく施設及び区域並びに日本国における合衆国軍隊の地位に関する協定
国際的な協力の下に規制薬物に係る不正行為を助長する行為等の防止を図るための麻薬及び向精神薬取締法等の特例等に関する法律
民放 5 局史上最大のコラボレーション!地デジ夏祭り 2006 全部見せます!ナゴヤのテレビ"過去""現在"そして"未来"
アイルランドの貧民の子供たちが両親及び国の負担となることを防ぎ、国家社会の有益なる存在たらしめるための穏健なる提案
ドナウダンプフシファールトゼレクトリツィテーテンハウプトベトリープスヴェルクバウウンターベアムテンゲゼルシャフト
マルキ・ド・サドの演出のもとにシャラントン精神病院患者たちによって演じられたジャン＝ポール・マラーの迫害と暗殺
くりぃむしちゅーも観ながらいろいろゴチャゴチャ言ってますけども…笑いのタマゴ L サイズ（おひとり様何回でも）
偽造カード等及び盗難カード等を用いて行われる不正な機械式預貯金払戻し等からの預貯金者の保護等に関する法律
ルイージ・アメデーオ・ジュゼッペ・マリーア・フェルディナンド・フランチェスコ・ディ・サヴォイア＝アオスタ
中居正広のテレビ 50 年名番組だョ!全員集合笑った泣いた感動したあのシーンをもう一度夢の総決算スペシャル
タウマタファカタンギハンガコアウアウオタマテアトゥリプカカピキマウンガホロヌクポカイフェヌアキタナタフ
アウグステ・ヴィクトリア・フォン・シュレースヴィヒ＝ホルシュタイン＝ゾンダーブルク＝アウグステンブルク

The most linked pages are:
ISBN 52641

The shortest path from '渋谷' to '小野妹子' is:
渋谷
ギャルサー\_(テレビドラマ)
小野妹子

The 10 most popular pages are:
0: 英語
1: ISBN
2: 2006 年
3: 2005 年
4: 2007 年
5: 東京都
6: 昭和
7: 2004 年
8: 2003 年
9: 2000 年
python wikipedia.py wikipedia_dataset/pages_medium.txt 4784.89s user 5.72s system 99% cpu 1:20:11.80 total
```
