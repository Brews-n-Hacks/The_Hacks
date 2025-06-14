#!/bin/python

import os
import random
import difflib
import tkinter as tk
from tkinter import messagebox

"""
This was a college project.
The concept was our family enjoys cooking and has a decent database of recipes, 
but we are also indecisive in what what we WANT to cook. 
This is inteneded to help randomize our options, 
based on what we have at hand.
"""

# Function to read recipes from markdown files in the "recipes" directory
def read_recipes_from_vault():
    recipes = []
    vault_path = "/home/user/ObsidianVaults/Meal_Planning"  # Update this with the path to your Obsidian vault
    for file_name in os.listdir(vault_path):
        if file_name.endswith(".md"):
            recipe_name = os.path.splitext(file_name)[0]  # Extract recipe name from file name
            recipes.append(recipe_name)
    return recipes

# Function to generate a random weekly meal plan
def generate_meal_plan(recipes):
    weekly_plan = random.sample(recipes, 7)  # Select 7 random recipes for the week
    return weekly_plan

# Function to generate ingredient checklist
def generate_shopping_list(weekly_plan, vault_path):
    ingredients = set()
    for recipe in weekly_plan:
        # Assuming each recipe is stored in a markdown file with ingredients listed with '-'
        with open(os.path.join(vault_path, f"{recipe}.md"), "r") as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("-"):
                    ingredients.add(line.strip("-").strip())
    return ingredients

def generate_plan_and_shopping_list():
    # Read recipes
    recipes = read_recipes_from_vault()
    
    # Get special request from entry widget
    special_request = special_request_entry.get().strip()
    
    # Handling typos by finding the most similar file
    if special_request:
        closest_match = difflib.get_close_matches(special_request, recipes, n=1, cutoff=0.6)
        if closest_match:
            special_request = closest_match[0]
        else:
            messagebox.showinfo("Information", "No similar recipe found for the special request.")
    
    # Generate weekly meal plan
    weekly_plan = generate_meal_plan(recipes)
    weekly_plan_text = "\n".join([f"Week {i+1}: {recipe}" for i, recipe in enumerate(weekly_plan)])
    weekly_plan_label.config(text=weekly_plan_text)
    
    # Generate shopping list
    vault_path = "/home/user/ObsidianVaults/Meal_Planning"  # Update this with the path to your Obsidian vault
    shopping_list = generate_shopping_list(weekly_plan, vault_path)
    shopping_list_text = "\n".join(shopping_list)
    shopping_list_label.config(text=shopping_list_text)

# Create Tkinter window
window = tk.Tk()
window.title("Weekly Meal Planner")

# Special request entry
special_request_label = tk.Label(window, text="Special Request:")
special_request_label.grid(row=0, column=0, sticky="w")
special_request_entry = tk.Entry(window)
special_request_entry.grid(row=0, column=1, padx=5, pady=5)

# Generate plan button
generate_button = tk.Button(window, text="Generate Plan", command=generate_plan_and_shopping_list)
generate_button.grid(row=0, column=2, padx=5, pady=5)

# Weekly plan label
weekly_plan_label = tk.Label(window, text="Your weekly meal plan will appear here.")
weekly_plan_label.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="w")

# Shopping list label
shopping_list_label = tk.Label(window, text="Your shopping list will appear here.")
shopping_list_label.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="w")

# Run the Tkinter event loop
window.mainloop()
