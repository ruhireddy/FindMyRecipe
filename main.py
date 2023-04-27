import tkinter as tk
from tkinter import *
import json
import recipes
import hashmap
import btree

window = tk.Tk()
window.title("Find My Recipe")
window.geometry("600x300")



hello = tk.Label(text="Select and type the ingredients you have and then press Find my Recipe!", font=("Georgia",11))
hello.pack()

recipes_text = tk.Text(font = ("Georgia", 9), yscrollcommand=True, xscrollcommand=True, height = 35, width = 90)
recipes_text.pack(side=RIGHT)

type_in_ingredients = tk.Text(font = ("Georgia", 9), yscrollcommand=True, xscrollcommand=True, height = 1, width = 30)
type_in_ingredients.pack(pady = 5,side=BOTTOM);



ingredients_to_check = [["chicken", "pork", "beef", "bacon", "turkey", "ham", "pepperoni", "brisket", "eggs", "tuna", "salmon", "fish"],["milk", "cheese", "heavy cream", "sour cream", "yogurt", "butter"],["rice","pasta","bread","noodles","quinoa","black beans", "chickpeas"],["apple", "orange","mango","banana","strawberries","blueberries","pineapple","blackberries","raspberries","cherries", "pear"],["tomato","broccoli","potato","celery","peppers","onions","squash","avocado","green peas","lettuce","asparagus","cauliflower","kale","arugula", "green beans"],["water","salt","oil","black pepper","cayenne","paprika","chili flakes","garlic","flour","dough","sugar","corn starch","stock","vinegar","baking powder", "baking soda"]]
checkbox_vars = []
checkbox_buttons = []

for i in range(0, len(ingredients_to_check)):
  checkbox_vars.append([])
  checkbox_buttons.append([])
  for j in range(0, len(ingredients_to_check[i])):
    find_recipe_button_var = IntVar() 
    find_recipe_button = tk.Checkbutton(window, text = ingredients_to_check[i][j], 
                        variable = find_recipe_button_var,
                        onvalue = 1,
                        offvalue = 0,
                        height = 1,
                        width = 12)
    checkbox_vars[i].append(find_recipe_button_var)
    checkbox_buttons[i].append(find_recipe_button)
    #find_recipe_button.pack(padx = 5, pady = 5, side = tk.TOP)
    find_recipe_button.place(x = 10 + 120 * i, y = j * 25 + 100)


# Opening JSON file
f = open('recipes_raw/recipes_raw_nosource_epi.json')
  
# returns JSON object as 
# a dictionary
data = json.load(f)
  
# Iterating through the json
# list
#for i in data['title']:
    #print(i)

i = 0

hashmap_recipes = hashmap.HashMap(100)
#btree_recipes = btree.BTree(20)

for key,value in data.items():
  if value['title']:
    recipe = recipes.Recipes(value['title'],value['ingredients'],value['instructions'])
    hashmap_recipes.insert(recipe);
    #btree_recipes.insert(recipe)
ingredient_list = []
def retrieve_input():
  input = type_in_ingredients.get("1.0",'end-1c')
  ingredient_list.append(input)
  type_in_ingredients.delete("1.0","end")
  print(ingredient_list)
def update_recipe_text():
  recipes_text.delete("1.0","end")
  for i in range(0, len(ingredients_to_check)):
    for j in range(0, len(ingredients_to_check[i])):
      if checkbox_vars[i][j].get() == 1:
        ingredient_list.append(ingredients_to_check[i][j])

  valid_recipes = hashmap_recipes.search_for_valid_recipes(ingredient_list)
  for i in valid_recipes:
    recipes_text.insert(tk.END, i.recipe_to_string())
  ingredient_list.clear()

button = tk.Button(text="Find My Recipe!", font = ("Georgia",11), command=update_recipe_text, bg='#90EE90')
button.pack()

type_in_ingredients_button = tk.Button(text="Use ingredient", font = ("Georgia",11), command=retrieve_input)
type_in_ingredients_button.pack(side=BOTTOM)

# Closing file
f.close()

tk.mainloop()