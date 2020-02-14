# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 20:27:23 2020

@author: Najd
"""
import requests
import config as cf


def get_random_recipe():
    header = cf.headers
    
    res =  requests.request("GET", cf.url, headers=header, params=cf.querystring)
    data = res.json()
    recipe = data['recipes'][0]
    
    recipe_title = recipe['title']
    extended_ingredients = recipe['extendedIngredients']
    
    recipe_ingredients, fresh_ingredients = [], []
    for ingr in extended_ingredients:
        recipe_ingredients.append(ingr['originalName'])
        fresh_ingredients.append(ingr['name'])
        
    recipe_time = recipe['readyInMinutes']
    recipe_serving_ct = recipe['servings']
    recipe_instructions = recipe['instructions']
    recipe_link = recipe['sourceUrl']
    
    
    return recipe_title, recipe_ingredients, fresh_ingredients, recipe_time, recipe_serving_ct, recipe_instructions, recipe_link
   
    

    
def main():
    get_random_recipe()
            
            
if __name__ == '__main__':
    main()

