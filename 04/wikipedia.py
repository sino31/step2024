import sys
from collections import deque
import time

class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.links[id] = []
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()

    # Convert title to ID
    def title_to_id(self, title):
        for page_id, page_title in self.titles.items():
            if page_title == title:
                return page_id
        return None

    # Convert ID to title
    def id_to_title(self, id):
        for page_id, page_title in self.titles.items():
            if page_id == id:
                return page_title
        return None


    # Find the longest titles. This is not related to a graph algorithm at all
    # though :)
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()


    # Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()


    def find_shortest_path(self, start, goal):
        """

            Find the shortest path.
            - Use BFS and add nodes to the queue as tuples of (PageID, the path to reach that PageID).

            Arguments:
            - |start|: The title of the start page.
            - |goal|: The title of the goal page.

        """
        # Convert the start and goal titles to their corresponding IDs
        start_id = self.title_to_id(start)
        goal_id = self.title_to_id(goal)
        assert start_id and goal_id # Ensure both start and goal IDs are valid

        # Initialize the queue with the start node and its path
        queue = deque()
        visited = set()
        queue.append((start_id,[start_id]))
        visited.add(start_id)

        # BFS
        while queue:
            (node_id, path) = queue.popleft()

            # If the goal node is reached, print the path
            if node_id == goal_id:
                print(f"The shortest path from '{start}' to '{goal}' is:")
                for node in path:
                    title = self.id_to_title(node)
                    print(title)
                print()
                return

            # Visit all the children of the current node
            for child_id in self.links[node_id]:
                if child_id not in visited:
                    visited.add(child_id)
                    queue.append((child_id, path + [child_id])) # Add the child node and the updated path to the queue

        # If no path is found
        print("Path not found")
        print()


    def find_most_popular_pages(self, max_iterations=100, p=0.85, convergence_eps = 0.01, assert_eps = 1.0e-6):
        """

            Calculate the page ranks and print the most popular pages.

            Arguments:
            - max_iterations : Maximum number of iterations.
            - p : Probability of following a link from the current page to the next page.
            - convergence_eps : Convergence judgment. The acceptable error margin for considering the algorithm to have converged.
            - assert_eps : Acceptable error margin to prevent assertion failure due to rounding errors when distributing ranks.

        """
        num_pages = len(self.titles)
        pagerank = {id: 1.0 / num_pages for id in self.titles} # Initialize PageRank for each page

        for i in range(max_iterations):
            new_pagerank = {id: (1.0 * (1 - p)) / num_pages for id in self.titles} # Create a new PageRank and add the rank for random openings
            for from_id, to_ids in self.links.items():
                if to_ids: # Page has links
                    shared_rank = pagerank[from_id] / len(to_ids)
                    for to_id in to_ids:
                        new_pagerank[to_id] += p * shared_rank
                else: # Page has no links
                    shared_rank = pagerank[from_id] / num_pages
                    for id in self.titles:
                        new_pagerank[id] += p * shared_rank

            # Check for convergence
            sum_diff = sum(abs(new_pagerank[id] - pagerank[id]) for id in self.titles)
            if sum_diff**2 < convergence_eps:
                break

            pagerank = new_pagerank

        # Calculate the total rank to ensure it sums to 1
        total_rank = sum(pagerank[id] for id in self.titles)
        assert abs(total_rank - 1.0) < assert_eps, f"Total rank ({total_rank}) did not converge to 1.0"

        # Get the top 10 pages based on PageRank
        top10_pages = sorted(pagerank, key=pagerank.get, reverse=True)[:10]
        print("The 10 most popular pages are:")
        for i, page_id in enumerate(top10_pages):
            page_title = self.id_to_title(page_id)
            print(f"{i}: {page_title}")


    # Do something more interesting!!
    def find_something_more_interesting(self, start):
        pass


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    wikipedia.find_longest_titles()
    wikipedia.find_most_linked_pages()
    wikipedia.find_shortest_path("A", "D")
    wikipedia.find_most_popular_pages()
