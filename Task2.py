import timeit
from functools import lru_cache
import matplotlib.pyplot as plt
import sys


# Fibonacci implementation using lru_cache
@lru_cache(maxsize=None)
def fibonacci_lru(n):
    """Compute the n-th Fibonacci number using lru_cache."""
    if n < 2:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


# Clear the cache between measurement series for a "clean" start
def reset_lru_cache():
    fibonacci_lru.cache_clear()


# Splay Tree implementation
class SplayNode:
    """A node of the Splay Tree storing a (key, value) pair."""

    __slots__ = ("key", "value", "left", "right")

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None


class SplayTree:
    """
    Basic implementation of a Splay Tree.
    Stores (key, value) -> (n, fibonacci(n)).
    """

    def __init__(self):
        self.root = None

    def _right_rotate(self, x):
        """Right rotation around node x."""
        y = x.left
        x.left = y.right
        y.right = x
        return y

    def _left_rotate(self, x):
        """Left rotation around node x."""
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def _splay(self, root, key):
        """
        Main 'splay' operation. Moves the node with the given key
        (or the last known node on the path to the key) to the root of the tree.
        """
        if root is None or root.key == key:
            return root

        # Zig-Zig or Zig-Zag depending on the location of the key.
        # Key in left subtree
        if key < root.key:
            if root.left is None:
                return root
            # Zig-Zig (Left Left)
            if key < root.left.key:
                root.left.left = self._splay(root.left.left, key)
                root = self._right_rotate(root)
            # Zig-Zag (Left Right)
            elif key > root.left.key:
                root.left.right = self._splay(root.left.right, key)
                if root.left.right is not None:
                    root.left = self._left_rotate(root.left)

            return root if root.left is None else self._right_rotate(root)

        # Key in right subtree
        else:
            if root.right is None:
                return root
            # Zig-Zig (Right Right)
            if key > root.right.key:
                root.right.right = self._splay(root.right.right, key)
                root = self._left_rotate(root)
            # Zig-Zag (Right Left)
            elif key < root.right.key:
                root.right.left = self._splay(root.right.left, key)
                if root.right.left is not None:
                    root.right = self._right_rotate(root.right)

            return root if root.right is None else self._left_rotate(root)

    def search(self, key):
        """Search for a value by key. If found, the root will be the element with this key."""
        self.root = self._splay(self.root, key)
        if self.root and self.root.key == key:
            return self.root.value
        return None

    def insert(self, key, value):
        """Insert a new node (key, value). After insertion, perform splay."""
        if self.root is None:
            self.root = SplayNode(key, value)
            return

        # First perform splay so that the last processed node is key
        self.root = self._splay(self.root, key)

        # If after splay the key is already at the root (existing key), just update value
        if self.root.key == key:
            self.root.value = value
            return

        # Otherwise create a new node
        new_node = SplayNode(key, value)
        # Split the tree by key
        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
        else:
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None

        self.root = new_node  # new node becomes the root


# Fibonacci using Splay Tree
def fibonacci_splay(n, tree):
    """
    Compute the n-th Fibonacci number using a Splay Tree as a “cache” of computed results.
    """
    # Check if n is in the tree
    cached_val = tree.search(n)
    if cached_val is not None:
        return cached_val

    # If not in the tree – compute it
    if n < 2:
        result = n
    else:
        result = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)

    # Store the result in the splay tree
    tree.insert(n, result)
    return result


def reset_splay_tree():
    """Completely creates a new tree (to start calculations from scratch)."""
    return SplayTree()


# Time measurement
def measure_time(func, setup, number=950):
    """
    Returns the average time (in seconds) taken to call `func()`,
    measured using timeit.timeit.
    Parameter `number` – how many repetitions to run (more repetitions -> more accurate result).
    """
    t = timeit.timeit(func, setup=setup, number=number)
    return t / number


def main():
    sys.setrecursionlimit(10**7)  # just in case, to avoid recursion depth issues

    ns = list(range(0, 951, 50))  # 0, 50, 100, 150, ... 950

    # Each function is called several times and average time is measured.
    # For demonstration, 100 or 200 repetitions are enough to keep it fast.
    repeat_count = 200

    results_lru = []
    results_splay = []

    print("n         LRU Cache Time (s)    Splay Tree Time (s)")
    print("----------------------------------------------------")

    for n in ns:
        # ---------- LRU Cache measurements ----------
        # Clear cache so each n starts "from scratch"
        reset_lru_cache()

        # Prepare setup strings for timeit
        setup_lru = "from __main__ import fibonacci_lru;" f"n={n}"
        code_lru = f"fibonacci_lru({n})"

        t_lru = measure_time(code_lru, setup_lru, number=repeat_count)
        results_lru.append(t_lru)

        # ---------- Splay Tree measurements ----------
        # New tree for each n
        setup_splay = (
            "from __main__ import fibonacci_splay, reset_splay_tree;"
            "tree = reset_splay_tree();"
            f"n = {n}"
        )
        code_splay = "fibonacci_splay(n, tree)"

        t_splay = measure_time(code_splay, setup_splay, number=repeat_count)
        results_splay.append(t_splay)

        print(f"{n:<10} {t_lru:<20.8g} {t_splay:<20.8g}")

    # Plotting the results
    plt.figure(figsize=(8, 5))
    plt.plot(ns, results_lru, "o-", label="LRU Cache")
    plt.plot(ns, results_splay, "x-", label="Splay Tree")

    plt.title("Execution Time Comparison: LRU Cache vs Splay Tree")
    plt.xlabel("Fibonacci Number (n)")
    plt.ylabel("Average Execution Time (seconds)")
    plt.legend()
    plt.grid(True)

    plt.show()


if __name__ == "__main__":
    main()
