import sys
from hash_table import HashTable as hashtable

# Implement a data structure that stores the most recently accessed N pages.
# See the below test cases to see how it should work.
#
# Note: Please do not use a library like collections.OrderedDict). The goal is
#       to implement the data structure yourself!

# Implementation of a node in a doubly linked list
class Node:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

# Implement of doubly linked list
class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    # Add the node to the front of the doubly linked list.
    def add_node_to_front(self, node):
        if self.head:
            # If the list is not empty, insert the node at the front.
            node.next = self.head
            self.head.prev = node
            self.head = node
        else:
            # If the list is empty, initialize the head and tail to the new node.
            node.prev = node.next = None
            self.head = self.tail = node
        node = None

    # Remove the node from the doubly linked list.
    def remove_node(self, node):
        if node:
            if node.prev and node.next: # For intermediate node
                node.prev.next = node.next
                node.next.prev = node.prev
            elif node.next: # For the head node
                self.head = node.next
                self.head.prev = None
            elif node.prev: # For the tail node
                self.tail = node.prev
                self.tail.next = None
            else: # If the node is the only element in the list
                self.head = self.tail = None
            node = None

    # Move the node to the front of the doubly linked list.
    # 1. Save the node's value.
    # 2. Remove the node.
    # 3. Add the node to the front using the saved value.
    def move_node_to_front(self, node):
        key, value = node.key, node.value
        self.remove_node(node)
        self.add_node_to_front(Node(key,value))

class Cache:
    # Initialize the cache.
    # |n|: The size of the cache.
    def __init__(self, n):
        self.max_cache_size = n
        self.size = 0
        self.cache_hash_table = hashtable()
        self.cache_linked_list = DoublyLinkedList()

    # Access a page and update the cache so that it stores the most recently
    # accessed N pages. This needs to be done with mostly O(1).
    # |url|: The accessed URL
    # |contents|: The contents of the URL
    def access_page(self, url, contents):
        node, exists = self.cache_hash_table.get(url)
        if exists: # If the URL is in the hash table
            self.cache_linked_list.move_node_to_front(node) # Update to the most recent access.
            self.cache_hash_table.put(url, self.cache_linked_list.head) # Update the hash table value.
        else: # If the URL is NOT in the hash table
            if self.size == self.max_cache_size: # If the cache is full
                # Remove the oldest accessed site.
                tail_key = self.cache_linked_list.tail.key
                self.cache_linked_list.remove_node(self.cache_linked_list.tail)
                self.cache_hash_table.put(tail_key, None)
                self.size -= 1
            # Add the new page as the most recent access.
            new_node = Node(url, contents)
            self.cache_linked_list.add_node_to_front(new_node)
            self.cache_hash_table.put(url, self.cache_linked_list.head)
            self.size += 1

    # Return the URLs stored in the cache. The URLs are ordered in the order
    # in which the URLs are mostly recently accessed.
    def get_pages(self):
        urls = []
        current = self.cache_linked_list.head
        while current:
            urls.append(current.key)
            current = current.next
        return urls


def cache_test():
    # Set the size of the cache to 4.
    cache = Cache(4)

    # Initially, no page is cached.
    assert cache.get_pages() == []

    # Access "a.com".
    cache.access_page("a.com", "AAA")
    # "a.com" is cached.
    assert cache.get_pages() == ["a.com"]

    # Access "b.com".
    cache.access_page("b.com", "BBB")
    # The cache is updated to:
    #   (most recently accessed)<-- "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["b.com", "a.com"]

    # Access "c.com".
    cache.access_page("c.com", "CCC")
    # The cache is updated to:
    #   (most recently accessed)<-- "c.com", "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["c.com", "b.com", "a.com"]

    # Access "d.com".
    cache.access_page("d.com", "DDD")
    # The cache is updated to:
    #   (most recently accessed)<-- "d.com", "c.com", "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["d.com", "c.com", "b.com", "a.com"]

    # Access "d.com" again.
    cache.access_page("d.com", "DDD")
    # The cache is updated to:
    #   (most recently accessed)<-- "d.com", "c.com", "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["d.com", "c.com", "b.com", "a.com"]

    # Access "a.com" again.
    cache.access_page("a.com", "AAA")
    # The cache is updated to:
    #   (most recently accessed)<-- "a.com", "d.com", "c.com", "b.com" -->(least recently accessed)
    assert cache.get_pages() == ["a.com", "d.com", "c.com", "b.com"]

    cache.access_page("c.com", "CCC")
    assert cache.get_pages() == ["c.com", "a.com", "d.com", "b.com"]
    cache.access_page("a.com", "AAA")
    assert cache.get_pages() == ["a.com", "c.com", "d.com", "b.com"]
    cache.access_page("a.com", "AAA")
    assert cache.get_pages() == ["a.com", "c.com", "d.com", "b.com"]

    # Access "e.com".
    cache.access_page("e.com", "EEE")
    # The cache is full, so we need to remove the least recently accessed page "b.com".
    # The cache is updated to:
    #   (most recently accessed)<-- "e.com", "a.com", "c.com", "d.com" -->(least recently accessed)
    assert cache.get_pages() == ["e.com", "a.com", "c.com", "d.com"]

    # Access "f.com".
    cache.access_page("f.com", "FFF")
    # The cache is full, so we need to remove the least recently accessed page "c.com".
    # The cache is updated to:
    #   (most recently accessed)<-- "f.com", "e.com", "a.com", "c.com" -->(least recently accessed)
    assert cache.get_pages() == ["f.com", "e.com", "a.com", "c.com"]

    # Access "e.com".
    cache.access_page("e.com", "EEE")
    # The cache is updated to:
    #   (most recently accessed)<-- "e.com", "f.com", "a.com", "c.com" -->(least recently accessed)
    assert cache.get_pages() == ["e.com", "f.com", "a.com", "c.com"]

    # Access "a.com".
    cache.access_page("a.com", "AAA")
    # The cache is updated to:
    #   (most recently accessed)<-- "a.com", "e.com", "f.com", "c.com" -->(least recently accessed)
    assert cache.get_pages() == ["a.com", "e.com", "f.com", "c.com"]

    print("Tests passed!")


if __name__ == "__main__":
    cache_test()
