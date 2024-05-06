import os
import sys
import tkinter
import customtkinter
import constants as con
import tkinter.messagebox


def reset_app():
    # restarts the current program
    python_app = sys.executable
    os.execl(python_app, python_app, *sys.argv)


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


def calculate_spice(spice_amount):
    dc = con.SPICE_DICT[spice_amount]
    return dc


def get_quality_mod(quality):
    return con.QUALITY_DICT[quality]


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.training_results = []
        self.training_box_list = []
        self.ingredient_items = []
        self.ingredient_box_list = []
        self.quality_items = []
        self.quality_box_list = []
        self.starting_ingredient_count = 0
        self.final_ingredient_count = 0
        self.spice_mod = 0
        self.player_roll = 0

        # frame for widgets
        self.frame = customtkinter.CTkFrame(self, border_width=3)
        self.frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        # all buttons
        self.start_button = customtkinter.CTkButton(self.frame, text="LET ME COOK",
                                                    command=self.create_ingredient_inputs)
        self.start_button.grid(padx=345, pady=255)

        # buttons below are placed on the grid from the create_ingredient_inputs function
        self.spice_combo_box = customtkinter.CTkComboBox(self.frame, width=185, values=con.SPICE_DICT["Keys"])
        self.spice_combo_box.set("Select Spice Amount")
        self.player_roll_entry = customtkinter.CTkEntry(self.frame, placeholder_text="Player Roll")
        self.calculate_button = customtkinter.CTkButton(self.frame, text="Calculate DC", command=self.calculate_dc)
        self.reset_button = customtkinter.CTkButton(self.frame, text="Reset", command=reset_app)

    def calculate_training(self):
        training_mod = 0

        for box in self.training_box_list:
            training_mod += int(box.get())
        return training_mod

    def get_ingredient_mod(self):
        ingredient_total = 0
        try:
            for item in self.ingredient_items:
                ingredient_total += con.INGREDIENT_DICT[item]
            return ingredient_total
        except KeyError:
            return "Error"

    def get_ingredient_count_dc(self):
        if self.final_ingredient_count in range(1, 4):
            return 12
        elif self.final_ingredient_count in range(4, 7):
            return 14
        elif self.final_ingredient_count in range(7, 10):
            return 16
        elif self.final_ingredient_count in range(10, 13):
            return 18
        elif self.final_ingredient_count in range(13, 16):
            return 20
        return 22

    def calculate_dc(self):
        try:
            # adjust player dc
            player_roll = int(self.player_roll_entry.get())
        except (TypeError, ValueError):
            tkinter.messagebox.askokcancel(title="Player Roll Error", message="Player Roll is not valid, please "
                                                                              "re-enter.")
            return

        try:
            # clears list in case button was clicked multiple times
            self.training_results.clear()
            training_dc = int(self.calculate_training())
            # add training dc to player dc
            player_roll += training_dc
        except ValueError:
            tkinter.messagebox.askokcancel(title="Training Error", message="Please select all training bonuses.")
            return

        try:
            # add spice to ingredient list if not 0
            spice_mod = int(calculate_spice(self.spice_combo_box.get()))
            if spice_mod != 0:
                self.final_ingredient_count = self.starting_ingredient_count + 1
            else:
                self.final_ingredient_count = self.starting_ingredient_count
        except KeyError:
            tkinter.messagebox.askokcancel(title="Spice Error", message="Please select the spice amount.")
            return

        try:
            # add quality and ingredients to lists from boxes
            self.update_quality_list()
            self.update_ingredient_list()

            # get ingredient count dc
            ingredient_count_dc = self.get_ingredient_count_dc()

            # get ingredient dc
            ingredient_mod = self.get_ingredient_mod()

            # get quality dc and add to player roll
            highest_quality = ""
            for quality in self.quality_items:
                if len(quality) > len(highest_quality):
                    highest_quality = quality
            quality_mod = int(get_quality_mod(highest_quality))
            player_roll += quality_mod

            dm_dc = spice_mod + ingredient_count_dc + ingredient_mod

            total_dc = player_roll - dm_dc

            tkinter.messagebox.askokcancel(title="Results", message=f"{total_dc}\n{get_results(total_dc)}")

        except (TypeError, ValueError, KeyError):
            tkinter.messagebox.askokcancel(title="Error", message="Please select all quality and ingredients!")

    def update_quality_list(self):
        self.quality_items.clear()
        for box in self.quality_box_list:
            if box.get() not in self.quality_items:
                self.quality_items.append(box.get())

    def update_ingredient_list(self):
        self.ingredient_items.clear()
        for box in self.ingredient_box_list:
            if box.get() not in self.ingredient_items:
                self.ingredient_items.append(box.get())

    def create_ingredient_inputs(self):
        try:
            dialogue = customtkinter.CTkInputDialog(text="How many ingredients are there?",
                                                    title="Ingredient Count")
            starting_ingredient_count = int(dialogue.get_input())
            self.start_button.destroy()

            for count in range(0, starting_ingredient_count):
                new_quality_combo = customtkinter.CTkComboBox(self.frame, values=con.QUALITY_DICT["Keys"])
                self.quality_box_list.append(new_quality_combo)
                self.quality_box_list[count].set("Select Quality")
                self.quality_box_list[count].grid(row=count, column=0, padx=10, pady=5)

                new_ingredient_combo = customtkinter.CTkComboBox(self.frame, width=200,
                                                                 values=con.INGREDIENT_DICT["Keys"])
                self.ingredient_box_list.append(new_ingredient_combo)
                self.ingredient_box_list[count].set("Select Ingredient")
                self.ingredient_box_list[count].grid(row=count, column=1, padx=10, pady=5)

                training_combo_box = customtkinter.CTkComboBox(self.frame, width=125, values=con.TRAINING_LIST)
                self.training_box_list.append(training_combo_box)
                self.training_box_list[count].set("Select Training Tier")
                self.training_box_list[count].grid(row=count, column=2, padx=10, pady=5)

            self.calculate_button.grid(row=starting_ingredient_count + 2, column=3, padx=20, pady=5)
            self.spice_combo_box.grid(row=starting_ingredient_count + 1, column=3, padx=10, pady=5)
            self.player_roll_entry.grid(row=0, column=4, padx=10, pady=5)
            self.reset_button.grid(row=starting_ingredient_count + 3, column=0, padx=10, pady=5)

        except ValueError:
            self.create_ingredient_inputs()
