import random


def random_fruits_veggies():
    with open("lib/fruitsAndVeggies.txt") as lines:
        fruits_veggies = lines.readlines()
        limit = len(fruits_veggies)
        ran_num = random.randint(0, limit)
        return fruits_veggies[ran_num].replace("\n", "")


def random_animals():
    with open("lib/animals.txt") as lines:
        animals = lines.readlines()
        limit = len(animals)
        ran_num = random.randint(0, limit)
        return animals[ran_num].replace("\n", "")


def random_ideas():
    return random_animals() + " + " + random_fruits_veggies()
