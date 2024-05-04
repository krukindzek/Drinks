import tkinter as tk
from tkinter import ttk
import requests
from PIL import Image, ImageTk


def fetch_random_cocktail():
    api_key = '1'
    url = 'https://www.thecocktaildb.com/api/json/v1/{api_key}/random.php'.format(api_key=api_key)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        cocktail_info = data['drinks'][0]
        cocktail_name = cocktail_info['strDrink']
        isAlcoholic = cocktail_info['strAlcoholic']
        while isAlcoholic=="Alcoholic":
            fetch_random_cocktail()
            return
        ingredients = ""
        for i in range(1, 16):
            ingredient = cocktail_info.get(f'strIngredient{i}', '')
            measure = cocktail_info.get(f'strMeasure{i}', '')
            if ingredient and measure:
                ingredients += f"{ingredient}: {measure}\n"
            elif not ingredient:
                break
        instructions = cocktail_info['strInstructions']
        instructions = wrap_text(instructions, 40)  # Wrap text to fit 40 characters per line
        image_url = cocktail_info['strDrinkThumb']

        # Download the image
        image_response = requests.get(image_url)
        image_data = image_response.content
        with open("cocktail_image.jpg", "wb") as f:
            f.write(image_data)

        # Display the information in a Tkinter window
        window = tk.Tk()
        window.title("Random Cocktail")

        name_label = tk.Label(window, text="Name: " + cocktail_name, font=("Helvetica", 14, "bold"))
        name_label.grid(row=0, column=0, columnspan=2)

        # Load and display the image
        image = Image.open("cocktail_image.jpg")
        image = image.resize((200, 200), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        image_label = tk.Label(window, image=photo)
        image_label.image = photo  # To prevent garbage collection
        image_label.grid(row=1, column=0, rowspan=3)

        ingredients_label = tk.Label(window, text="Ingredients:\n" + ingredients, font=("Helvetica", 12))
        ingredients_label.grid(row=1, column=1, sticky="nsew")

        instructions_label = tk.Label(window, text="Instructions:\n" + instructions, font=("Helvetica", 12), wraplength=300)
        instructions_label.grid(row=2, column=1, sticky="nsew")

        alcoholic_label = tk.Label(window, text="Alcoholic: " + isAlcoholic, font=("Helvetica", 12))
        alcoholic_label.grid(row=3, column=1, sticky="nsew")

        # Update window size based on the text size
        window.update()
        window_width = max(window.winfo_width(), 400)
        window_height = max(window.winfo_height(), 400)
        window.geometry(f"{window_width}x{window_height}")

        window.mainloop()
    else:
        print("Failed to fetch random cocktail.")



def wrap_text(text, width):
    return '\n'.join([text[i:i+width] for i in range(0, len(text), width)])


fetch_random_cocktail()
