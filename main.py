import os
import sys
import tkinter
import customtkinter
import tkinter.messagebox

# constant variables
TRAINING_LIST = [
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
]

SPICE_LIST = [
    "0-3",
    "4-6",
    "7-9",
    "10+"
]

SPICE_DICT = {
    "0-3": 0,
    "4-6": 1,
    "7-9": 2,
    "10+": 3
}

INGREDIENT_LIST = [
    "Fruit",
    "Vegetables",
    "Artisan Goods",
    "Legumes",
    "Grains",
    "Raw Animal Products",
    "Herbs",
    "Red Meat",
    "Seafood"
]

INGREDIENT_DICT = {
    "Fruit": 1,
    "Vegetables": 1,
    "Artisan Goods": 1,
    "Legumes": 0,
    "Grains": 0,
    "Raw Animal Products": -1,
    "Herbs": 1,
    "Red Meat": -1,
    "Seafood": -1
}


QUALITY_LIST = [
    "☆",
    "☆☆",
    "☆☆☆",
    "☆☆☆☆",
    "☆☆☆☆☆"
]

QUALITY_DICT = {
    "☆": 0,
    "☆☆": 1,
    "☆☆☆": 2,
    "☆☆☆☆": 4,
    "☆☆☆☆☆": 5
}

# global variables to be modified
training_results = []
training_box_list = []
ingredient_items = []
ingredient_box_list = []
quality_items = []
quality_box_list = []
starting_ingredient_count = 0
final_ingredient_count = 0
spice_dc = 0
player_dc = 0


def main():

    def reset_app():
        # restarts the current program
        python_app = sys.executable
        os.execl(python_app, python_app, * sys.argv)

    def get_results(total_dc):
        # results are calculated from the final player dc minus the full dish dc
        if total_dc <= -15:
            return "Not edible."
        elif total_dc <= -10:
            return "Constitution saving throw at disadvantage to stomach it."
        elif total_dc <= -5:
            return "Constitution saving throw to stomach it."
        elif total_dc >= 20:
            return "Legendary. Those who eat this, gains temporary hit points equal to the result. This lasts for 24 " \
                   "hours."
        elif total_dc >= 15:
            return "Amazing. Can be sold for an amount of gold equal to the result."
        elif total_dc >= 10:
            return "Very good. Can be sold for an amount of gold equal to half the result."
        elif total_dc >= 5:
            return "Better than expected."
        return "Average."

    def calculate_training():
        global training_results
        training_dc = 0

        for box in training_box_list:
            training_dc += int(box.get())
        return training_dc

    def calculate_spice(spice_amount):
        dc = SPICE_DICT[spice_amount]
        return dc

    def get_ingredient_dc():
        ingredient_total = 0
        try:
            for item in ingredient_items:
                ingredient_total += INGREDIENT_DICT[item]
            return ingredient_total
        except KeyError:
            return "Error"

    def get_ingredient_count_dc():
        if final_ingredient_count in range(1, 4):
            return 12
        elif final_ingredient_count in range(4, 7):
            return 14
        elif final_ingredient_count in range(7, 10):
            return 16
        elif final_ingredient_count in range(10, 13):
            return 18
        elif final_ingredient_count in range(13, 16):
            return 20
        return 22

    def get_quality_dc(quality):
        if quality == "☆":
            return 0
        elif quality == "☆☆":
            return 1
        elif quality == "☆☆☆":
            return 2
        elif quality == "☆☆☆☆":
            return 4
        elif quality == "☆☆☆☆☆":
            return 5
        return "Error"

    def calculate_dc():
        global starting_ingredient_count, final_ingredient_count, player_dc, spice_dc
        try:
            # adjust player dc
            player_dc = int(player_dc_entry.get())
        except (TypeError, ValueError):
            tkinter.messagebox.askokcancel(title="Player DC Error", message="Player DC is not valid, please re-enter.")
            return

        try:
            # clears list in case button was clicked multiple times
            training_results.clear()
            training_dc = int(calculate_training())
            # add training dc to player dc
            player_dc += training_dc
        except ValueError:
            tkinter.messagebox.askokcancel(title="Training Error", message="Please select all training bonuses.")
            return

        try:
            # add spice to ingredient list if not 0
            spice_dc = int(calculate_spice(spice_combo_box.get()))
            if spice_dc != 0:
                final_ingredient_count = starting_ingredient_count + 1
            else:
                final_ingredient_count = starting_ingredient_count
        except KeyError:
            tkinter.messagebox.askokcancel(title="Spice Error", message="Please select the spice amount.")
            return

        try:
            # add quality and ingredients to lists from boxes
            update_quality_list()
            update_ingredient_list()

            # get ingredient count dc
            ingredient_count_dc = get_ingredient_count_dc()

            # get ingredient dc
            ingredient_dc = get_ingredient_dc()

            # get quality dc
            highest_quality = ""
            for quality in quality_items:
                if len(quality) > len(highest_quality):
                    highest_quality = quality
            quality_dc = int(get_quality_dc(highest_quality))

            dm_dc = spice_dc + ingredient_count_dc + ingredient_dc + quality_dc

            total_dc = player_dc - dm_dc

            tkinter.messagebox.askokcancel(title="Results", message=f"{total_dc}\n{get_results(total_dc)}")

        except (TypeError, ValueError):
            tkinter.messagebox.askokcancel(title="Error", message="Please select all quality and ingredients!")

    def update_quality_list():
        quality_items.clear()
        for box in quality_box_list:
            if box.get() not in quality_items:
                quality_items.append(box.get())

    def update_ingredient_list():
        ingredient_items.clear()
        for box in ingredient_box_list:
            if box.get() not in ingredient_items:
                ingredient_items.append(box.get())

    def create_ingredient_inputs():
        global starting_ingredient_count
        try:
            dialogue = customtkinter.CTkInputDialog(text="How many ingredients are there?", title="Ingredient Count")
            starting_ingredient_count = int(dialogue.get_input())
            start_button.destroy()

            for count in range(0, starting_ingredient_count):
                new_quality_combo = customtkinter.CTkComboBox(frame, values=QUALITY_LIST)
                quality_box_list.append(new_quality_combo)
                quality_box_list[count].set("Select Quality")
                quality_box_list[count].grid(row=count, column=0, padx=10, pady=5)

                new_ingredient_combo = customtkinter.CTkComboBox(frame, width=200, values=INGREDIENT_LIST)
                ingredient_box_list.append(new_ingredient_combo)
                ingredient_box_list[count].set("Select Ingredient")
                ingredient_box_list[count].grid(row=count, column=1, padx=10, pady=5)

                training_combo_box = customtkinter.CTkComboBox(frame, width=125, values=TRAINING_LIST)
                training_box_list.append(training_combo_box)
                training_box_list[count].set("Select Training Tier")
                training_box_list[count].grid(row=count, column=2, padx=10, pady=5)

            calculate_button.grid(row=starting_ingredient_count + 2, column=3, padx=20, pady=5)
            spice_combo_box.grid(row=starting_ingredient_count + 1, column=3, padx=10, pady=5)
            player_dc_entry.grid(row=0, column=4, padx=10, pady=5)
            reset_button.grid(row=starting_ingredient_count + 3, column=0, padx=10, pady=5)

        except ValueError:
            create_ingredient_inputs()

    # main window
    customtkinter.set_appearance_mode("dark")
    app = customtkinter.CTk()
    app.title("Ingredient Calculator")
    app.geometry("900x600")

    # frame for widgets
    frame = customtkinter.CTkFrame(app, border_width=3)
    frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    # all buttons
    start_button = customtkinter.CTkButton(frame, text="LET ME COOK", command=create_ingredient_inputs)
    start_button.grid(padx=345, pady=255)

    # buttons below are placed on the grid from the create_ingredient_inputs function
    spice_combo_box = customtkinter.CTkComboBox(frame, width=185, values=SPICE_LIST)
    spice_combo_box.set("Select Spice Amount")

    player_dc_entry = customtkinter.CTkEntry(frame, placeholder_text="Player DC")

    calculate_button = customtkinter.CTkButton(frame, text="Calculate DC", command=calculate_dc)

    reset_button = customtkinter.CTkButton(frame, text="Reset", command=reset_app)

    app.mainloop()


main()
