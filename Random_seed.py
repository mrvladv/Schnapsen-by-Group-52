import random

# Constants
NUMBER_OF_SEEDS = 100
list1 = list(range(0, 9999, 1))
seed_database = []

for i in range(NUMBER_OF_SEEDS):
    random_seed = random.choice(list1)
    seed_database.append(random_seed)
    print("Seed", i, "-", random_seed)


