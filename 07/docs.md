## README
- malloc0.c : bestfit & free listは１つのまま
- malloc.c : bestfit & free list bin & merge

### 1. Best-fitの実装

- **First-fit**

    | Challenge    | simple_malloc  |                | my_malloc     |                |
    |--------------|----------------|----------------|---------------|----------------|
    |              | Time [ms]      | Utilization [%]| Time [ms]     | Utilization [%]|
    | Challenge #1 | 13             | 70             | 11            | 70             |
    | Challenge #2 | 7              | 40             | 10            | 40             |
    | Challenge #3 | 129            | 9              | 122           | 9              |
    | Challenge #4 | 29757          | 15             | 22250         | 15             |
    | Challenge #5 | 15394          | 15             | 14497         | 15             |



- **Best-fit**

    | Challenge    | simple_malloc  |                | my_malloc     |                |
    |--------------|----------------|----------------|---------------|----------------|
    |              | Time [ms]      | Utilization [%]| Time [ms]     | Utilization [%]|
    | Challenge #1 | 11             | 70             | 1636          | 70             |
    | Challenge #2 | 7              | 40             | 1050          | 40             |
    | Challenge #3 | 130            | 9              | 1270          | 51             |
    | Challenge #4 | 24722          | 15             | 11265         | 72             |
    | Challenge #5 | 16919          | 15             | 6680          | 75             |

    Timeが大幅に伸び(metadataをwhileで全て回しているため)、Utilizationは大幅に増加した！


### 2. Free List Binの実装
- 32,64,128,256,512,1024,2048,4096を区切りとしてbinsを作成
    |   size   |   ~32   |   ~64   |  ~128   |   ~256  |   ~512  |  ~1024  |  ~2048  |  ~4096  |
    | -------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- |
    |   bin    |  bin[0] |  bin[1] |  bin[2] |  bin[3] |  bin[4] |  bin[5] |  bin[6] |  bin[7] |
- dummyは全てのbinsで共有して使用  
-> utilizationが向上すると思ったが逆に少し下がった(challenge4が71%, 5が72%に)

### 3. 性能を上げるために色々と試す
- 隣り合う空き領域をmergeする : utilizationが向上すると思ったが変化がない -> 実装にミスがある？
    | Challenge    | simple_malloc  |                | my_malloc     |                |
    |--------------|----------------|----------------|---------------|----------------|
    |              | Time [ms]      | Utilization [%]| Time [ms]     | Utilization [%]|
    | Challenge #1 | 11             | 70             | 2835          | 70             |
    | Challenge #2 | 7              | 40             | 2238          | 40             |
    | Challenge #3 | 130            | 9              | 1512          | 51             |
    | Challenge #4 | 24722          | 15             | 1632          | 71             |
    | Challenge #5 | 16919          | 15             | 1268          | 72             |
