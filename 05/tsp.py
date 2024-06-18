#!/usr/bin/env python3

"""

遺伝的アルゴリズム G.A.
参考 : https://www.econ.osaka-cu.ac.jp/~hashimo/Genetic.pdf

・遺伝子配列 : 聖地を回り切った経路(聖地を巡った順序)
・適応度 : 経路の短さ(短いほど適応度が高いので経路距離の逆数)
・ルーレット法 : 適合度の合計を100%として個体数を適合度に応じて配分
・交叉 : ランダムな2つの経路のランダムな一部分を入れ替える -> 順序交叉を行う
        参考 : http://ono-t.d.dooo.jp/GA/GA-order.html#OX:~:text=1.2%20%E9%A0%86%E5%BA%8F%E4%BA%A4%E5%8F%89(OX%3AOrder%20crossover)
・突然変異 : ランダムな1つの経路に対しランダムな2つの聖地を選択し順序を入れ替える
・世代交代 : 一定回数処理を繰り返したら、一定数値よりも適応度が低いものは可能性として考えない(削除する)
・経路の決定 : 最終的に繰り返し処理を終了させた時点で適応度が一番高いものが最短経路

1. ランダムに一定数の経路を生成し、適応度を計算 -> create_init_path
2. ルーレット法で親となる経路を2つ選び、交叉によって子経路を作成 -> generate_child
3. 生成された子経路に対して一定の確率で突然変異を起こす -> mutation
4. 新しい経路の総距離を計算し、全ての経路の適応度を更新 -> calculate_fitness
5. 適応度が低い個体を削除し、世代を交代する(2-5を繰り返す) -> remove_low_fitness_path
6. 一定回数世代を交代したら、その時点で1番適応度が高いものを最短経路とする

"""

import sys
import random
import math
from common import print_tour, read_input


class GeneticAlgorithm:
    def __init__(self, cities):
        self.cities_with_index = [(i, city) for i, city in enumerate(cities)]
        self.max_generations = 10000
        self.init_path_size = 1000
        self.mutation_rate = 0.1
        self.retain_rate = 0.8
        self.paths = {}  # paths={tuple(path):fitness} : keyは不変の必要があるのでtupleで保存

        print(f"Max generations: {self.max_generations}")
        print(f"Initial path size: {self.init_path_size}")
        print(f"Mutation rate: {self.mutation_rate}")
        print(f"Retain rate: {self.retain_rate}")


    # node間の距離を計算
    def distance(self, city1, city2):
        return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

    # path全体の距離を計算
    def path_distance(self, path):
        distance = 0
        for i in range(len(path) - 1):
            city1 = path[i][1]
            city2 = path[i + 1][1]
            distance += self.distance(city1, city2)
        distance += self.distance(path[-1][1], path[0][1])
        return distance

    # 任意のpathの適応度を計算
    def calculate_fitness(self, path):
        distance = self.path_distance(path)
        return 1 / distance


    def create_init_path(self):
        for _ in range(self.init_path_size):
            path = random.sample(self.cities_with_index, len(self.cities_with_index))
            self.paths[tuple(path)] = self.calculate_fitness(path)


    def roulette_selection(self):
        total_fitness = sum(self.paths.values())
        selection_probs = [fitness / total_fitness for fitness in self.paths.values()]
        parent1, parent2 = random.choices(list(self.paths.keys()), weights= selection_probs, k=2)
        return parent1, parent2


    def crossover(self, parent1, parent2):
        length = len(parent1)
        start = random.randint(0, length//2)
        end = random.randint(start, length)

        child1 = [None] * length
        child2 = [None] * length

        # remain部分のコピー
        child1[start:end + 1] = parent1[start:end + 1]
        child2[start:end + 1] = parent2[start:end + 1]

        # 親2の順序を右回りで保持しながら子1を完成させる
        # endの次からlengthまで -> 0からstartまで : "%length"でindexがlengthまで行ったら0に戻す
        parent2_i = (end + 1) % length
        for i in range(length):
            child1_i = (end + 1 + i) % length
            if child1[child1_i] is None:
                while parent2[parent2_i] in child1:
                    parent2_i = (parent2_i + 1) % length
                child1[child1_i] = parent2[parent2_i]
                parent2_i = (parent2_i + 1) % length

        # 親1の順序を右回りで保持しながら子2を完成させる
        parent1_i = (end + 1) % length
        for i in range(length):
            child2_i = (end + 1 + i) % length
            if child2[child2_i] is None:
                while parent1[parent1_i] in child2:
                    parent1_i = (parent1_i + 1) % length
                child2[child2_i] = parent1[parent1_i]
                parent1_i = (parent1_i + 1) % length

        return child1, child2


    def inversion_mutation(self, path):
        if random.random() < self.mutation_rate:
            length = len(path)
            start = random.randint(0, length - 2)
            end = random.randint(start + 1, length - 1)
            path[start:end + 1] = reversed(path[start:end + 1])
        return path


    def remove_low_fitness_path(self):
        sorted_paths = sorted(self.paths.items(), key=lambda item:item[1], reverse=True)
        retain_length = max(int(len(sorted_paths) * self.retain_rate), 1)
        self.paths = dict(sorted_paths[:retain_length])


    def solve(self):
        self.create_init_path() # 1. ランダムに一定数の経路を生成し、適応度を計算

        for _ in range(self.max_generations):
            parent1, parent2 = self.roulette_selection() # 2. ルーレット法で親となる経路を2つ選び
            child1, child2 = self.crossover(parent1, parent2) # 交叉によって子経路を作成

            # 3. 生成された子経路に対して一定の確率で突然変異を起こす
            # 4. 新しい経路の総距離を計算し、全ての経路の適応度を更新
            # for child1
            child1 = self.inversion_mutation(child1)
            self.paths[tuple(child1)] = self.calculate_fitness(child1)
            # for child2
            child2 = self.inversion_mutation(child2)
            self.paths[tuple(child2)] = self.calculate_fitness(child2)

            self.remove_low_fitness_path() # 5. 適応度が低い個体を削除し、世代を交代する

        shortest_path = max(self.paths, key=self.paths.get) # 6. 一定回数世代を交代したら、その時点で1番適応度が高いものを最短経路とする
        print("finished g.a")
        # 7. 2-optでさらに経路を最短にする
        shortest_path = self.two_opt(shortest_path)
        return shortest_path


    # 2-optでpathを交換した場合の距離計算(交換した場所のみを計算し、どちらが最短か確認)
    def delta_distance(self, best, i, j):
        before = self.distance(best[i - 1], best[i]) + self.distance(best[j - 1], best[j])
        after = self.distance(best[i - 1], best[j - 1]) + self.distance(best[i], best[j])
        return after - before


    # 2-opt
    def two_opt(self, path):
        best = list(path)
        improved = True
        while improved:
            improved = False
            for i in range(1, len(best) - 2):
                for j in range(i + 1, len(best)):
                    if j - i == 1:
                        continue
                    delta = self.delta_distance(best, i, j)
                    if delta < 0:
                        new_path = best.copy()
                        new_path[i:j] = best[j - 1:i - 1:-1]
                        best = new_path
                        improved = True
        return tuple(best)


    def output(self, shortest_path, file):
        with open(file, 'w') as f:
            f.write("index\n")
            for city in shortest_path:
                f.write(f"{city[0]}\n")

        print(f"Shortest path: {self.path_distance(shortest_path)}")


if __name__ == '__main__':
    assert len(sys.argv) > 2
    cities = read_input(sys.argv[1])
    ga = GeneticAlgorithm(cities)
    tour = ga.solve()
    ga.output(tour, sys.argv[2])
