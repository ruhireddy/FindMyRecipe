class HashMap:
  def __init__(self, size):
    self.size = size
    self.table = [[] for _ in range(self.size)]

  def __hash_function(self, recipe):
    return len(recipe.getIngredients())

  def insert(self, recipe):
    index = self.__hash_function(recipe)
    self.table[index].append(recipe)

  def search_for_valid_recipes(self, ingredients):
    list_of_recipes = []
    num_of_ingredients = len(ingredients)
    for i in range(num_of_ingredients, 1, -1):
      for j in self.table[i]:
        if j.searchIngredients(ingredients):
          print(j.getTitle())
          print(j.getIngredients())
          list_of_recipes.append(j)
          if len(list_of_recipes) >= 20:
            return list_of_recipes
    return list_of_recipes

  