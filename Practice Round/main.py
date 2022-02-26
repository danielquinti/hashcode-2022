import os
from collections import defaultdict
def empty_list():
    return []

from itertools import chain, combinations

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def is_client_valid(recipe,client):
    for like in client["likes"]:
        if not like in recipe:
            return False
    for dislike in client["dislikes"]:
        if dislike in recipe:
            return False
    return True

def evaluate(powerset,preferences):
    max_recipe = (0,[])
    for recipe in powerset:
        metric = []
        for client in preferences:
            if is_client_valid(recipe,client):
                metric.append(client)
        if len(metric) > max_recipe[0]:
            max_recipe = (len(metric), recipe)
    return max_recipe

def design_pizza(file):
    clients = int(file.readline())
    total_preferences=[]
    for client in range(clients):
        client_preferences = defaultdict(empty_list)
        likes = file.readline().split()
        client_preferences["likes"] = likes[1:]
        dislikes = file.readline().split()
        client_preferences["dislikes"] = dislikes[1:]
        total_preferences.append(client_preferences)
    total_likes = []
    for preferences in total_preferences:
        total_likes += preferences["likes"]
    print(total_likes)
    ps = list(powerset(total_likes))
    print(ps)
    print(len(ps))
    print(evaluate(ps, total_preferences))

def list_difference(list1,list2):
    return [item for item in list1 if item not in list2]


def design_pizza_2(file):
    n_clients = int(file.readline())
    total_preferences=[]
    for client in range(n_clients):
        client_preferences = defaultdict(empty_list)
        likes = file.readline().split()
        client_preferences["likes"] = likes[1:]
        dislikes = file.readline().split()
        client_preferences["dislikes"] = dislikes[1:]
        total_preferences.append(client_preferences)
    total_likes = []
    total_dislikes = []
    for preferences in total_preferences:
        total_likes += preferences["likes"]
    for preferences in total_preferences:
        total_dislikes += preferences["dislikes"]
    pizza = list_difference(total_likes, total_dislikes)
    ingredients=" ".join(pizza)
    print(f'{len(pizza)} {ingredients}')

class IngredientInfo:
    def __init__(self):
        self.loved = 0
        self.hated = 0
        self.ratio = 1

def design_pizza_3(file):
    n_clients = int(file.readline())
    ingredients=defaultdict(IngredientInfo)
    pizza = []
    for client in range(n_clients):
        loved = file.readline().split()[1:]
        for name in loved:
            ingredients[name].loved+=1
        hated = file.readline().split()[1:]
        for name in hated:
            ingredients[name].hated += 1
    for name, ingredient in ingredients.items():
        ingredient.ratio = ingredient.loved/ingredient.hated if ingredient.hated > 0 else 10
        if ingredient.ratio>=1:
            pizza.append(name)
    text=" ".join(pizza)
    print(f'{len(pizza)}')

if __name__ == '__main__':
    folder = "input_data"
    for filename in os.listdir(folder):
        with open(os.path.join(folder,filename), 'r') as file:
            design_pizza_3(file)
