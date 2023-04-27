"""Creates btree to store recipes; organized by number of ingredients in recipe"""

class Node:
    def __init__(self, t, leaf):
        self.keys = [None] * (2 * t - 1)  # array to hold each key in a node
        self.t = t  # minimum degree
        self.children = [None] * (2 * t)  # array to hold each child node
        self.n = 0  # counter for the number of keys in a node
        self.leaf = leaf  # boolean to determine if node is a leaf node
        self.recipes = [None] * (2 * t - 1) # array to hold each recipe that corresponds to a key

    # insert function for nodes that are not full
    def insert_not_full(self, index, recipe):
        i = self.n - 1
        
        # if the current node is a leaf, insert in the leaf
        if self.leaf:
            while i >= 0 and self.keys[i] > index:
                self.keys[i + 1] = self.keys[i]
                i -= 1
            self.keys[i + 1] = index
            self.recipes[i + 1] = recipe
            self.n += 1
        
        # else split the children and call insert again
        else:
            while i >= 0 and self.keys[i] > index:
                i -= 1
            if self.children[i + 1].n == 2 * self.t - 1:
                self.split_child(i + 1, self.children[i + 1])
                if self.keys[i + 1] < index:
                    i += 1
            self.children[i + 1].insert_not_full(index, recipe)

    # function to split a node if there are too many keys
    # inspired by GeeksforGeeks b-tree implementation
    def split_child(self, i, y):
        z = Node(y.t, y.leaf)
        z.n = self.t - 1
        for j in range(self.t - 1):
            z.keys[j] = y.keys[j + self.t]
        if not y.leaf:
            for j in range(self.t):
                z.children[j] = y.children[j + self.t]
        y.n = self.t - 1
        for j in range(self.n, i, -1):
            self.children[j + 1] = self.children[j]
        self.children[i + 1] = z
        for j in range(self.n - 1, i - 1, -1):
            self.keys[j + 1] = self.keys[j]
        self.keys[i] = y.keys[self.t - 1]
        self.n += 1

    # A function to search all nodes to find a recipes with wanted ingredients
    def search(self, list_of_ingredients, result):
        # iterate through nodes
        for i in range(self.n):
            if not self.leaf:
                self.children[i].search(list_of_ingredients, result)
            # check if ingredients are found in current key and print
            if self.recipes[i] is not None and len(self.recipes[i].getIngredients()) != 0 and self.recipes[i].searchIngredients(list_of_ingredients):
                # print(self.recipes[i].getTitle(), end='\n')
                # print(self.recipes[i].getIngredients(), end='\n')
                result.append(self.recipes[i])
        if not self.leaf:
            self.children[i + 1].search(list_of_ingredients, result)


# A BTree
class BTree:
    def __init__(self, t):
        self.root = None  # root node pointer
        self.t = t  # minimum degree
        self.used_indices = {}  # dictionary to store used indices to prevent collisions
        self.list_of_recipes = [] # array to hold search results

    # function to search for ingredients
    def search(self, list_of_ingredients):
        if self.root is not None:
            self.root.search(list_of_ingredients, self.list_of_recipes)

        return self.list_of_recipes

    # this function inserts a new recipe into the b tree
    def insert(self, recipe):

        index = self.create_index(recipe)

        # if tree is empty, add new node as the root
        if self.root is None:
            self.root = Node(self.t, True)
            self.root.keys[0] = index  # Insert key
            self.root.n = 1
            self.root.recipes[0] = recipe
        else:
            # if root is full, split it
            if self.root.n == 2 * self.t - 1:
                s = Node(self.t, False)
                s.children[0] = self.root
                s.split_child(0, self.root)
                i = 0
                if s.keys[0] < index:
                    i += 1
                s.children[i].insert_not_full(index, recipe)
                self.root = s
            # else insert new key in the root node
            else:
                self.root.insert_not_full(index, recipe)

    # this function creates an index to be used for each recipe in the b tree
    def create_index(self, recipe):
        # hash the number of ingredients to create an index
        index = len(recipe.getIngredients()) / 10

        # if the index already exists, use linear probing until an unused one is found
        while index in self.used_indices:
            index += 0.01

        # insert the new index in the dictionary of indices and return
        self.used_indices[index] = index
        return index
