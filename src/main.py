"""Manages GUI and inserts data into data structures"""

import tkinter as tk
from tkinter import *
import json
import recipes
import hashmap
import btree

#create a window for the GUI
window = tk.Tk()
window.title("Find My Recipe")
window.geometry("600x300")
#title label
hello = tk.Label(text="Select and type the ingredients you have and then press Find my Recipe!", font=("Georgia",11))
hello.pack()
#text box where recipes will be outputted
recipes_text = tk.Text(font = ("Georgia", 9), yscrollcommand=True, xscrollcommand=True, height = 35, width = 90)
recipes_text.pack(side=RIGHT)
#text box where user can type in ingredients
type_in_ingredients = tk.Text(font = ("Georgia", 9), yscrollcommand=True, xscrollcommand=True, height = 1, width = 30)
type_in_ingredients.pack(pady = 5,side=BOTTOM);
#ingredients that will appear as checkboxes, separated by category
ingredients_to_check = [["chicken", "pork", "beef", "bacon", "turkey", "ham", "pepperoni", "brisket", "eggs", "tuna", "salmon", "fish"],["milk", "cheese", "heavy cream", "sour cream", "yogurt", "butter"],["rice","pasta","bread","noodles","quinoa","black beans", "chickpeas"],["apple", "orange","mango","banana","strawberries","blueberries","pineapple","blackberries","raspberries","cherries", "pear"],["tomato","broccoli","potato","celery","peppers","onions","squash","avocado","green peas","lettuce","asparagus","cauliflower","kale","arugula", "green beans"],["water","salt","oil","black pepper","cayenne","paprika","chili flakes","garlic","flour","dough","sugar","corn starch","stock","vinegar","baking powder", "baking soda"]]
#boolean vars that show value of each ingredients checkbox
checkbox_vars = []

#button objects of each ingredient
checkbox_buttons = []

#create buttons and vars for each ingredient that have a checkbox
for i in range(0, len(ingredients_to_check)):
  checkbox_vars.append([])
  checkbox_buttons.append([])
  for j in range(0, len(ingredients_to_check[i])):
    ingredient_checkbox_var = IntVar() 
    ingredient_checkbox_button = tk.Checkbutton(window, text = ingredients_to_check[i][j], 
                        variable = ingredient_checkbox_var,
                        onvalue = 1,
                        offvalue = 0,
                        height = 1,
                        width = 12)
    checkbox_vars[i].append(ingredient_checkbox_var)
    checkbox_buttons[i].append(ingredient_checkbox_button)
    #place buttons
    ingredient_checkbox_button.place(x = 10 + 120 * i, y = j * 25 + 100)

# Opening JSON file
f = open('recipes_raw/recipes_raw_nosource_epi.json')
data = json.load(f)

#creates hash map with 100 initial buckets
hashmap_recipes = hashmap.HashMap(100)
#To create b-tree:
btree_recipes = btree.BTree(20)

for key,value in data.items():
  if value['title']:
    recipe = recipes.Recipes(value['title'],value['ingredients'],value['instructions'])
    hashmap_recipes.insert(recipe);
    #For b tree:
    #btree_recipes.insert(recipe)

#list of ingredients that are indicated by user that can be used in recipe
ingredient_list = []
#function that adds input from user input to ingredient list
def retrieve_input():
  input = type_in_ingredients.get("1.0",'end-1c')
  ingredient_list.append(input)
  type_in_ingredients.delete("1.0","end")
  print(ingredient_list)
#function that prints recipes to screen
def update_recipe_text():
  recipes_text.delete("1.0","end")
  for i in range(0, len(ingredients_to_check)):
    for j in range(0, len(ingredients_to_check[i])):
      if checkbox_vars[i][j].get() == 1:
        ingredient_list.append(ingredients_to_check[i][j])

  valid_recipes = hashmap_recipes.search_for_valid_recipes(ingredient_list)
  #for b tree:
  #valid_recipes = btree_recipes.search(ingredient_list)
  for i in valid_recipes:
    recipes_text.insert(tk.END, i.recipe_to_string())
  ingredient_list.clear()

#button that prompt to find recipes
find_recipe_button = tk.Button(text="Find My Recipe!", font = ("Georgia",11), command=update_recipe_text, bg='#90EE90')
find_recipe_button.pack()
#button to submit user-inputted ingredients
type_in_ingredients_button = tk.Button(text="Use ingredient", font = ("Georgia",11), command=retrieve_input)
type_in_ingredients_button.pack(side=BOTTOM)

# Closing file
f.close()

tk.mainloop()


