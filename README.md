# Genetic algorithms examples

For informal tutoring purposes.

-

### MIT License

-

Python 3 (Anaconda)

### generic guidelines.

1. Initialisation.
    Generate population of N items, each with randomly-generated chromosomes.

2. Selection.
	- a. Evaluate the fitness of each element of the population.
	- b. build a mating pool.

3. Reproduction.
	- Repeat N times:
		- a. pick two parents with probability according to relative fitness.
		- b. Crossover - create a child by combining the DNA of these two parents.
		- c. Mutation - mutate the child's chromosomes.
		- d. Add the new child to the new population.

4. Replacement of the old population with new population and return to Step 2.

-

#### GA Word search example.

```python main_word_search_example```

tests:

```python tests_word_search_ga.py```