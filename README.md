# Task 1. Data Access Optimization with LRU Cache

Implement a program that demonstrates how an LRU cache speeds up repeated "hot" queries to a large array of numbers.

## Technical Requirements

We have an array of length N containing strictly positive integers (1 ≤ N ≤ 100,000).
We need to process Q queries (1 ≤ Q ≤ 50,000) of two types:

Range(L, R) — calculate the sum of elements array[L : R + 1].

Update(index, value) — set array[index] ← value.

Implement the following four functions:

range_sum_no_cache(array, left, right) — returns the sum without caching.

update_no_cache(array, index, value) — updates an element without caching.

range_sum_with_cache(array, left, right) — performs a lookup in the given LRUCache class (capacity K = 1000).
If cache.get() returns -1 (cache miss), compute the sum, store it with put(), and return the result.

update_with_cache(array, index, value) — updates the array and removes all cached ranges that contain the modified index.
Invalidation is done via a linear scan through cache keys — no other modification of the class is required.

# Task 2. Comparing the Performance of Fibonacci Number Computation Using LRU Cache and Splay Tree
Implement a program to compute Fibonacci numbers in two ways: using an LRU cache and using a Splay Tree to store previously computed values. Perform a comparative analysis of their efficiency by measuring the average execution time for each approach.

## Technical Requirements
Implement two functions for computing Fibonacci numbers:

fibonacci_lru(n)
This function should use the @lru_cache decorator to cache computation results. This allows it to reuse previously computed Fibonacci values.

fibonacci_splay(n, tree)
This function should use a Splay Tree data structure to store computed values.
If the Fibonacci number for the given n has already been computed, the value should be returned from the tree; otherwise, it should be computed, stored in the Splay Tree, and returned.

Measure the execution time of computing Fibonacci numbers for each approach:

Create a set of Fibonacci numbers from 0 to 950 with a step of 50:
0, 50, 100, 150, ...

Use the timeit module to measure execution time.

For each value of n, compute the average execution time of Fibonacci computation using LRU Cache and Splay Tree.

Build a graph comparing execution times for the two approaches:

Use the matplotlib library to create the graph.

On the x-axis, plot the value of n (Fibonacci number index).

On the y-axis, plot the average execution time in seconds.

Add a legend indicating the two approaches: LRU Cache and Splay Tree.

Draw conclusions about the efficiency of both approaches based on the graph.

Additionally, besides building the graph, output a text table containing:

Value of n

Average execution time for LRU Cache

Average execution time for Splay Tree

The table should be formatted for easy reading.