import tkinter as tk
from tkinter import simpledialog


class GridApp(tk.Tk):
    def __init__(self, grid_width=10, grid_height=10):
        super().__init__()

        # Prompt for grid size before setting up the UI
        input_width = simpledialog.askinteger("Grid Width", "Enter the grid width:", parent=self, minvalue=1, maxvalue=20, initialvalue=grid_width)
        input_height = simpledialog.askinteger("Grid Height", "Enter the grid height:", parent=self, minvalue=1, maxvalue=20, initialvalue=grid_height)
        
        if input_width and input_height:  # Only proceed if the user provided the width and height
            self.grid_width = input_width
            self.grid_height = input_height
            self.title('Customizable Grid Colorer')
            self.default_tile_color = 'grey'
            self.constraint_mode = False
            self.tiles = []
            self.init_ui()
        else:
            self.quit()  # Close the app if the user cancels the prompt
    

    def init_ui(self):
        self.create_grid()
        self.create_control_buttons()
        self.create_text_entry_button()

    def create_grid(self):
        for row_widgets in self.tiles:
            for tile in row_widgets:
                tile.destroy()
        self.tiles.clear()

        for i in range(self.grid_height):
            row = []
            for j in range(self.grid_width):
                tile = tk.Canvas(self, width=50, height=50, bg=self.default_tile_color, highlightthickness=1)
                tile.grid(row=i, column=j, pady=1, padx=1)
                tile.bind('<Button-1>', lambda e, t=tile: self.handle_left_click(e, t))
                tile.bind('<Button-3>', lambda e, t=tile: self.handle_right_click(e, t))
                tile.bind('<Button-2>', lambda e, t=tile: self.handle_middle_click(e, t))  # Bind middle click to handle_middle_click

                row.append(tile)
            self.tiles.append(row)

    def create_control_buttons(self):
        self.toggle_mode_button = tk.Button(self, text='Toggle Set Constraints', command=self.toggle_mode)
        self.toggle_mode_button.grid(row=self.grid_height, column=0, columnspan=self.grid_width, pady=10)

        self.soft_reset_button = tk.Button(self, text='Soft Reset', command=self.soft_reset_grid)
        self.soft_reset_button.grid(row=self.grid_height+1, column=0, columnspan=self.grid_width, pady=10)

    def create_text_entry_button(self):
        self.text_entry_button = tk.Button(self, text='Enter Text for Tile', command=self.prompt_for_text)
        self.text_entry_button.grid(row=self.grid_height + 2, column=0, columnspan=self.grid_width, pady=10)
        self.current_text = ''  # Instance variable to store current text for tiles

    def prompt_for_text(self):
        self.current_text = simpledialog.askstring("Text for Tile", "Enter the text:", parent=self)
      

        

    def toggle_mode(self):
        self.constraint_mode = not self.constraint_mode
        mode_text = "Constraints Mode ON" if self.constraint_mode else "Constraints Mode OFF"
        self.toggle_mode_button.config(text=mode_text)

    def soft_reset_grid(self):
        for row in self.tiles:
            for tile in row:
                state = tile.itemcget("rect", "state")
                if state != tk.DISABLED:
                    tile.delete("rect")
                    tile.config(bg=self.default_tile_color, highlightbackground='black')
                    tile.delete("text")

    def color_tile(self, tile, color, outline=None):
        if outline:
            if color != 'grey':
                tile.create_rectangle(2, 2, 48, 48, fill=color, outline=outline, tags="rect", width=2)
                tile.itemconfig("rect", state=tk.DISABLED)  # Disable the rect to avoid coloring in normal play
            else:
                tile.create_rectangle(2, 2, 48, 48, fill=color, tags="rect", width=2)
                tile.itemconfig("rect", state=tk.NORMAL)
        else:
            state = tile.itemcget("rect", "state")
            if state != tk.DISABLED:  # Only color if not disabled by the constraint mode
                tile.config(bg=color)

        if self.constraint_mode and self.current_text:
            text_color = 'black' if color=="white" else "white"
            tile.create_text(30, 30, text=self.current_text, tags="text",fill=text_color)
            self.current_text=''
    
    def handle_left_click(self, event, tile):
        if self.constraint_mode:
            self.color_tile(tile, 'white', 'orange')
        else:
            self.color_tile(tile, 'white')

    def handle_right_click(self, event, tile):
        if self.constraint_mode:
            self.color_tile(tile, 'black', 'orange')
        else:
            self.color_tile(tile, 'black')

    def handle_middle_click(self, event, tile):
        if self.constraint_mode:
            self.color_tile(tile, 'grey','orange')
        else:
            self.color_tile(tile, 'grey')
    
    def reset_tile(self, tile):
        tile.delete("rect")
        tile.config(bg=self.default_tile_color)
        tile.delete("text")


if __name__ == "__main__":
    app = GridApp()
    app.mainloop()