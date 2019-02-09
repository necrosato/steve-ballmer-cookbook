import tkinter
import tkinter.ttk
import json

def is_match(recipe, ingredients, allowed_missing):
    '''
    recipe: dict representing a recipe
    ingredients: user supplied ingredients to check against recipe ingredients.
                 dict with same keys as recipe["ingredients"] that map to lists of ingredient names
    allowed_missing: dict with same keys as recipe["ingredients"]. Should map to ints
    '''
    misses = {}
    for key in allowed_missing:
        misses[key] = 0

    for category in recipe["ingredients"]:
        for ingredient in recipe["ingredients"][category]:
            if ingredient not in ingredients[category]:
                misses[category] += 1
                if misses[category] > allowed_missing[category]:
                    return False
    return True

class ScrollableFrame(tkinter.Frame):
    def __init__(self, master, **kwargs):
        tkinter.Frame.__init__(self, master, **kwargs)

        # create a canvas object and a vertical scrollbar for scrolling it
        self.vscrollbar = tkinter.Scrollbar(self, orient=tkinter.VERTICAL)
        self.vscrollbar.pack(side='right', fill="y",  expand="true")
        self.canvas = tkinter.Canvas(self,
                                     bg='#ffffff', bd=0,
                                     height=250,
                                     highlightthickness=0,
                                     yscrollcommand=self.vscrollbar.set)
        self.canvas.pack(side="left", fill="y", expand="true")
        self.vscrollbar.config(command=self.canvas.yview)

        # reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = tkinter.Frame(self.canvas, **kwargs)
        self.canvas.create_window(0, 0, window=self.interior, anchor="nw")

        self.bind('<Configure>', self.set_scrollregion)


    def set_scrollregion(self, event=None):
        """ Set the scroll region on the canvas"""
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

class SteveBallmersCookbook:
    ''' The main application '''

    def __init__(self):
        ''' Loads the databse and sets up the gui '''
        self.database = json.load(open("./database/json/database.json", "r"))

        self.window = tkinter.Tk()
        self.window.geometry('900x700')
        self.window.title("Steve Ballmer's Cookbook")
        self.ma_label = tkinter.Label(self.window, text="Allowed missing alcohol ingredients: ")
        self.ma_label.grid(column=0, row=0)
        self.missing_alcohol_combo = tkinter.ttk.Combobox(self.window, state='readonly')
        self.missing_alcohol_combo['values'] = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
        self.missing_alcohol_combo.current(0)
        self.missing_alcohol_combo.grid(column=0, row=1)
        self.mg_label = tkinter.Label(self.window, text="Allowed missing garnish ingredients: ")
        self.mg_label.grid(column=1, row=0)
        self.missing_garnish_combo = tkinter.ttk.Combobox(self.window, state='readonly')
        self.missing_garnish_combo['values'] = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
        self.missing_garnish_combo.current(0)
        self.missing_garnish_combo.grid(column=1, row=1)
        self.mm_label = tkinter.Label(self.window, text="Allowed missing mixer ingredients: ")
        self.mm_label.grid(column=2, row=0)
        self.missing_mixer_combo = tkinter.ttk.Combobox(self.window, state='readonly')
        self.missing_mixer_combo['values'] = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
        self.missing_mixer_combo.current(0)
        self.missing_mixer_combo.grid(column=2, row=1)

        self.scrollbars = {}
        i = 0
        for category in sorted(self.database["ingredients"]):
            scrollbar = ScrollableFrame(self.window)
            scrollbar.grid(column=i, row=2)
            self.scrollbars[category] = scrollbar
            i+=1

        self.chk_buttons = {}
        i = 0
        for category in sorted(self.database["ingredients"]):
            self.chk_buttons[category] = {}
            j = 2
            for ingredient in sorted(self.database["ingredients"][category]):
                chk_state = tkinter.BooleanVar()
                chk_state.set(False)
                self.chk_buttons[category][ingredient] = [chk_state,
                        tkinter.ttk.Checkbutton(self.scrollbars[category].interior, text=ingredient, var=chk_state)] 
                self.chk_buttons[category][ingredient][1].grid(column=i, row=j)
                j+=1
            i+=1

        self.develop_button = tkinter.Button(self.window, text="Develop!", command=self.develop, padx=40, pady=20)
        self.develop_button.grid(column=1, row=3)
        self.matches_listbox = tkinter.Listbox(self.window, selectmode=tkinter.SINGLE)
        self.matches_listbox.bind('<<ListboxSelect>>', self.select_result)
        self.matches_listbox.grid(column=0, row=4)
        self.matches = {}

        self.selected_result_ingredients_scrollbar = ScrollableFrame(self.window)
        self.selected_result_ingredients_scrollbar.grid(column=1, row=4)
        self.selected_result_ingredients = tkinter.Text(self.selected_result_ingredients_scrollbar.interior, width=40)
        self.selected_result_ingredients.pack()

        self.selected_result_procedure_scrollbar = ScrollableFrame(self.window)
        self.selected_result_procedure_scrollbar.grid(column=2, row=4)
        self.selected_result_procedure = tkinter.Text(self.selected_result_procedure_scrollbar.interior, width=40)
        self.selected_result_procedure.config(wrap=tkinter.WORD)
        self.selected_result_procedure.pack()


    def select_result(self, evt):
        w = evt.widget
        if len(w.curselection()) == 1:
            i = w.curselection()[0]
            val = w.get(i)
            match = self.matches[val]
            ingredients = match['ingredients']
            self.selected_result_ingredients.delete(1.0, tkinter.END)
            self.selected_result_ingredients.insert(tkinter.END, 'Ingredients: \n')
            for category in sorted(ingredients):
                self.selected_result_ingredients.insert(tkinter.END, '\n'+category+': \n\n')
                for ingredient in sorted(ingredients[category]):
                    ingredient_dict = ingredients[category][ingredient]
                    ingredient_str = "\t{} {} {}\n".format(
                            ingredient_dict['amount'], ingredient_dict['unit'], ingredient)
                    self.selected_result_ingredients.insert(tkinter.END, ingredient_str)
                
            procedure = match['procedure']
            self.selected_result_procedure.delete(1.0, tkinter.END)
            self.selected_result_procedure.insert(tkinter.END, 'Procedure: \n\n')
            for step in procedure:
                self.selected_result_procedure.insert(tkinter.END, step + ' ')


    def develop(self):
        ''' parse the check buttons to build ingredients lists, then query the database '''
        current_ingredients = {}
        for category in self.chk_buttons:
            current_ingredients[category] = []
            for ingredient in sorted(self.chk_buttons[category]):
                if self.chk_buttons[category][ingredient][0].get():
                    current_ingredients[category].append(ingredient)

        allowed_missing = {"alcohol": int(self.missing_alcohol_combo.get()),
                           "garnish": int(self.missing_garnish_combo.get()),
                           "mixer": int(self.missing_mixer_combo.get()) }

        self.matches.clear()
        self.matches_listbox.delete(0, tkinter.END)
        for recipe_name in sorted(self.database['recipes']):
            recipe = self.database['recipes'][recipe_name]
            if is_match(recipe, current_ingredients, allowed_missing):
                self.matches[recipe_name] = recipe
                self.matches_listbox.insert(tkinter.END, recipe_name)


    def run(self):
        self.window.mainloop()

def main():
    app = SteveBallmersCookbook()
    app.run()


if __name__ == '__main__':
    main()
