import random
import time
from collections import OrderedDict


# Functions without caching
def range_sum_no_cache(array, L, R):
    """
    Returns the sum of elements array[L]...array[R] (inclusive) without using a cache.
    """
    return sum(array[L : R + 1])


def update_no_cache(array, index, value):
    """
    Updates the value of array[index] to value without cache.
    """
    array[index] = value


# LRU Cache implementation
class LRUCache:
    """
    Class for storing range-sum results in the format:
    cache[(L, R)] = sum from L to R

    Uses OrderedDict to automatically track usage order.
    Key - tuple (L, R).
    Value - the computed sum array[L]...array[R].
    """

    def __init__(self, capacity=1000):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        """
        Get a value from cache by key (L, R).
        If the key exists, move it to the end (as most recently used).
        If the key does not exist, return None.
        """
        if key not in self.cache:
            return None
        # Move to the end because the key was used
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        """
        Add (or update) a value in the cache.
        If cache size exceeds capacity, remove the LRU (least recently used) item.
        """
        self.cache[key] = value
        self.cache.move_to_end(key)
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  # remove oldest (LRU)

    def invalidate(self, condition_func):
        """
        Remove all cache entries for which condition_func(key) returns True.
        For example, condition_func may check whether (L <= index <= R).
        """
        keys_to_remove = [k for k in self.cache.keys() if condition_func(k)]
        for k in keys_to_remove:
            del self.cache[k]


# Functions with caching
def range_sum_with_cache(array, L, R, lru_cache):
    """
    Returns the sum of elements array[L]...array[R] (inclusive),
    using lru_cache to avoid repeated computations.
    """
    # 1. Check if (L, R) is in cache
    cached_value = lru_cache.get((L, R))
    if cached_value is not None:
        # If in cache, return quickly
        return cached_value

    # 2. If not in cache, compute the sum and store it in cache
    s = sum(array[L : R + 1])
    lru_cache.put((L, R), s)
    return s


def update_with_cache(array, index, value, lru_cache):
    """
    Updates a value in the array and invalidates (removes) from the cache
    all entries that are no longer valid.
    """
    array[index] = value

    # All cached ranges that include index are now outdated
    # Therefore, remove them from the cache
    def condition(key):
        L, R = key
        return L <= index <= R

    lru_cache.invalidate(condition)


# Performance test example
def main():
    N = 100_000  # array size
    Q = 50_000  # number of queries
    CAPACITY = 1000  # LRU cache size

    # Generate a random array of N elements
    array = [random.randint(1, 1000) for _ in range(N)]

    # Generate random queries
    # Half of them are 'Range', half are 'Update' (or as desired)
    queries = []
    for _ in range(Q):
        query_type = random.choice(["Range", "Update"])
        if query_type == "Range":
            L = random.randint(0, N - 1)
            R = random.randint(L, N - 1)
            queries.append(("Range", L, R))
        else:  # Update
            index = random.randint(0, N - 1)
            value = random.randint(1, 1000)
            queries.append(("Update", index, value))

    # Execute queries without caching
    start_time_no_cache = time.perf_counter()

    array_no_cache = array[:]  # copy of original array
    for q in queries:
        if q[0] == "Range":
            _, L, R = q
            _ = range_sum_no_cache(array_no_cache, L, R)
        else:
            _, idx, val = q
            update_no_cache(array_no_cache, idx, val)

    end_time_no_cache = time.perf_counter()
    total_time_no_cache = end_time_no_cache - start_time_no_cache

    # Execute queries with LRU cache
    start_time_cache = time.perf_counter()

    array_with_cache = array[:]  # copy of original array
    lru_cache = LRUCache(capacity=CAPACITY)

    for q in queries:
        if q[0] == "Range":
            _, L, R = q
            _ = range_sum_with_cache(array_with_cache, L, R, lru_cache)
        else:
            _, idx, val = q
            update_with_cache(array_with_cache, idx, val, lru_cache)

    end_time_cache = time.perf_counter()
    total_time_cache = end_time_cache - start_time_cache

    # Output results
    print(f"Execution time without caching: {total_time_no_cache:.3f} seconds")
    print(f"Execution time with LRU cache: {total_time_cache:.3f} seconds")


if __name__ == "__main__":
    main()

    # Execution time without caching: 9.730 seconds
    # Execution time with LRU cache: 10.471 seconds
