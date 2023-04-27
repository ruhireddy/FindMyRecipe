"""Creates an unordered map backed by a chained hash table in order to store recipes"""

class HashMap:
  #initialized table and vars
  def __init__(self, capacity):
    self.__size = 0
    self.__capacity = capacity
    self.__load_factor = 0.8
    self.__table = [[] for _ in range(self.__capacity)]
    
  #hash is the number of ingredients in the recipe
  def __hash_function(self, recipe):
    return len(recipe.getIngredients()) % self.__capacity
  
  #insert recipe into hash table
  def insert(self, recipe):
    #get hash key
    index = self.__hash_function(recipe)
    if len(self.__table[index]) == 0:
      self.__size += 1
    #rehash if load factor is too high
    if (self.__size / self.__capacity) >= self.__load_factor or index > self.__capacity - 1:
      temp_table = [[] for _ in range(self.__capacity * 2)]
      for i in self.__table:
        for j in i:
          temp_index = self.__hash_function(j)
          temp_table[temp_index].append(j)
      self.__table = temp_table
      del temp_table
      self.__capacity *= 2
    #make sure no repeats before entering
    found = False
    for i in self.__table[index]:
      if i.getTitle() == recipe.getTitle:
        found = True
        break
    if not found:
      self.__table[index].append(recipe)
      
  #search for recipes that include given ingredient list
  def search_for_valid_recipes(self, ingredients):
    list_of_recipes = []
    num_of_ingredients = len(ingredients)
    #start from max num of ingredients
    for i in range(num_of_ingredients, 1, -1):
      for j in self.__table[i]:
        if j.searchIngredients(ingredients):
          print(j.getTitle())
          print(j.getIngredients())
          list_of_recipes.append(j)
          #get max 20 recipes
          if len(list_of_recipes) >= 20:
            return list_of_recipes
    return list_of_recipes
