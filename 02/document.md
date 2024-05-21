## homework 1: hash_table.py

hash table を自分で実装する.

### delete function

buckets に key に対応する item がない場合：何もせず False を返す  
buckets に key に対応する item がある場合：item を削除し size を 1 減らす

### rehashing function

hash 値の衝突による計算量の増加を防ぐために、要素数に応じてテーブルサイズを変更し再マッピングを行う.

-   要素数がテーブルサイズの 70%を上回ったら、テーブルサイズを 2 倍に拡張
-   要素数がテーブルサイズの 30%を下回ったら、テーブルサイズを半分に縮小
-   テーブルサイズは、その付近の素数に設定

### calculate_hash function

hash 値の衝突を減らす ex."alice"と"elica"の衝突を防ぐ

1. 文字の順番を hash 値に反映させる
   ord(i)に「何文字目か」をかければ"alice"と"elica"は衝突しない  
   alice：1*97 + 2*108 + 3*105 + 4*99 + 5*101 = 1529 ≡ 74 (mod 97)  
   elica：1*101 + 2*108 + 3*105 + 4*99 + 5*108 = 1568 ≡ 16 (mod 97)
2. sha-256 を使用する

**perfomance_test の検証：**
https://docs.google.com/spreadsheets/d/1rqNunMeH2mv0MZiJW2e-HjOTnytwtvospsagQl2WDSM/edit#gid=0

## homework 2

-   データの順序が重要な場合が多いから
-   ハッシュテーブルはハッシュ関数の性能がそのままハッシュテーブルの性能に影響するので、関数を考える手間とリスクを回避するため
-   木構造(バランス木など)は最悪計算量が O(logn)だが、ハッシュテーブルは平均計算量が O(1)でも関数によっては最悪計算量は O(logn)以上になる可能性があるから

## homework 3 and 4: cache.py

キャッシュを O(1)で実装する

-   hash table と別に要素数 x の双方向リストを用意.
-   hash table：key = url, value = url に対応する双方向リストの node
-   双方向リスト：key = url, value = contents  
    head を最新アクセスサイト、tail を最古アクセスサイトとする.

**hash table に存在しないサイト F にアクセスした場合**

1. (list が全て埋まっていたら)最古アクセスのページを削除：list の tail を delete  
   -> 削除したページに対応する hash table の中身を None に
2. 最新アクセスとして F を追加：list の head を F に
3. この head を中身として F を hash table に追加

**hash table に存在するサイト A にアクセスした場合**

1. (hash table で hit したらその中身である node を確認し url と web ページを get)
2. list の元の位置から A を削除 -> hash table の A の中身を None に
3. 最新アクセスとして A を追加：list の head を A に
4. この head を中身として F を hash table の A を更新
