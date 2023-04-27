class Recipes:
  
  def __init__(self, title, ingredients, instructions):
    self.__title = title;
    self.__ingredients = ingredients
    self.__instructions = instructions
    self.parseIngredients()
    
  def searchIngredients(self, ingredient_to_search):

    for i in self.__ingredients:
      countIterations = 0
      for j in ingredient_to_search:
        countIterations += 1
        if j in i:
          if i[i.index(j) - 1] == ' ':
            break
          elif len(i) > i.index(j) + len(j):
            if i[i.index(j) + len(j)] == " " or i[i.index(j) + len(j)] == ",":
              break
            else:
              continue
          else: 
            continue
        elif countIterations == len(ingredient_to_search) - 1:
          return False
      
    return True

  def parseIngredients(self):
    for i in self.__ingredients:
      if "ADVERTISEMENT" in i:
        i = i.split("ADVERTISEMENT")

  def recipe_to_string(self):
    recipe_string = self.__title + "\n"
    recipe_string += "________________\n"
    for i in self.__ingredients:
      recipe_string += (i + "\n")
    recipe_string += ("\n"+ self.__instructions + "\n" + "\n")
    return recipe_string
    

  def getIngredients(self):
    return self.__ingredients

  def getTitle(self):
    return self.__title
    