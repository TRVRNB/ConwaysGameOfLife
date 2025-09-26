"""
CONWAY'S GAME OF LIFE
Travis Renberg
Started 10/3/24
Ended 1/8/2025
font: 22 pt nirmala ui
"""

import pygame # only necessary library
pygame.init()

WINDOW_SIZE = (640, 480) # standard size works well for this

ALIVE_COLOR = (50, 120, 200) # color for living cells
DEAD_COLOR = (40, 45, 40) # color for potential cells
CELL_SIZE = 16 # should be a factor of 480, unless you want weird bugs. 6, 8, 10, 12, 16, 20, and 24 all work well. anything below 10 is pretty laggy on here
CELL_AMOUNT = (WINDOW_SIZE[1] // CELL_SIZE, WINDOW_SIZE[1] // CELL_SIZE) # ensures it has the max amount of tiles that can fit.
BACKGROUND_COLOR = (0, 0, 0) # change this in other themes
BORDER = True # adds a grid; can make it harder to place 6x6 or 8x8 cells
THEMES = ( # tuple containing every theme
    {"background": (0, 0, 0), "alive": (50, 120, 200), "dead": (40, 45, 40)}, # black
    {"background": (52, 102, 64), "alive": (100, 250, 222), "dead": (20, 30, 25)}, # contrast
    {"background": (54, 13, 20), "alive": (217, 54, 84), "dead": (54, 40, 42)}, # burgundy
    {"background": (24, 12, 36), "alive": (232, 63, 7), "dead": (0, 0, 0)}, # halloween
    {"background": (122, 24, 29), "alive": (50, 97, 25), "dead": (160, 144, 144)}, # christmas
    {"background": (179, 25, 66), "alive": (255, 255, 255), "dead": (10, 49, 97)}, # america
    {"background": (92, 47, 20), "alive": (207, 155, 52), "dead": (26, 21, 15)}, # rustic
    {"background": (46, 81, 105), "alive": (60, 150, 68), "dead": (172, 173, 104)}, # beach
    {"background": (191, 46, 48), "alive": (232, 212, 30), "dead": (117, 75, 70)}, # barn
    )
CELL_SIZES = (16, 20, 24, 8, 10, 12, 15) # every possible size for the board
    
class Button(): # gui 

    
    def __init__(self, index : int, pos : list, image_path : str, size : list = [75, 75]):
        """
        index: an identifier for the button, used in on_click()
        pos: the position of the button
        image_path: the path to be loaded for the surface
        size: the width and height of the button
        """
        self.index = index
        self.pos = pos
        self.image_path = "images/" + image_path # images folder
        self.size = size
        self.update_sprite()
        self.selection = 0
        
        
        
    def click(self): # runs when a button is clicked
        
        global CELL_SIZE
        global CELL_SIZES
        global CELL_AMOUNT
        global WINDOW_SIZE
        global cells
        global generation
        global ALIVE_COLOR
        global DEAD_COLOR
        global BACKGROUND_COLOR
        global play
        global speed
        global ticking
        
        if self.index == 1: # change theme
            
            self.selection += 1 # change theme by 1
            
            if self.selection > len(THEMES) - 1: # wrap the tuple around
                self.selection = 0
                
            ALIVE_COLOR = THEMES[self.selection]["alive"] # update the colors
            DEAD_COLOR = THEMES[self.selection]["dead"]
            BACKGROUND_COLOR = THEMES[self.selection]["background"]
            
            
        elif self.index == 2: # resize and reset the cells
        
            self.selection += 1
            if self.selection > len(CELL_SIZES) - 1: # wrap
                self.selection = 0
            
            CELL_SIZE = CELL_SIZES[self.selection]
            CELL_AMOUNT = (WINDOW_SIZE[1] // CELL_SIZE, WINDOW_SIZE[1] // CELL_SIZE) # ensures it has the max amount of tiles that can fit.
            
            # copied from before the main loop
            cells = [] # index 1 is column, index 2 is the cell in the column

            for x in range(CELL_AMOUNT[0]): # adds the columns to the cell list
                column = [] # new blank column
                
                for y in range(CELL_AMOUNT[1]): # adds the cells to the column
            
                    
                    new_cell = Cell([x * CELL_SIZE, y * CELL_SIZE], (x, y)) # new blank cell
                    column.append(new_cell) # add it to the column
                
                cells.append(column) # add it to the massive list
                generation = 0
            play = False


        elif self.index == 3: # reset the cells

            # copied from before the main loop
            cells = [] # index 1 is column, index 2 is the cell in the column

            for x in range(CELL_AMOUNT[0]): # adds the columns to the cell list
                column = [] # new blank column
                
                for y in range(CELL_AMOUNT[1]): # adds the cells to the column
            
                    
                    new_cell = Cell([x * CELL_SIZE, y * CELL_SIZE], (x, y)) # new blank cell
                    column.append(new_cell) # add it to the column
                
                cells.append(column) # add it to the massive list
                generation = 0
            play = False


        elif self.index == 4: # pause / play
            play = bool(1 - play) # toggle between true and false

        
        elif self.index == 5: # step
            ticking = True # tick for 1 frame
            
            
        elif 6 <= self.index <= 8: # speed buttons
            speed = self.index - 5 # 1, 2, or 3

    
    def update_sprite(self): # updates the image and rect
        self.image = pygame.image.load(self.image_path)
        self.rect = pygame.Rect(self.pos, self.size)







class Cell(): # building block of life
    
    def __init__(self, pos : list, coordinates : tuple, life : bool=False):
        """
        pos: x and y position, to scale
        coordinates: x and y ON THE CELL GRID (each tile is 1x1 on the cell grid)
        life: whether or not a cell starts with life
        """
        self.pos = pos
        self.life = life
        self.new_life = life
        self.new_update = True
        if BORDER:
            self.rect = pygame.Rect((pos[0] + 1, pos[1] + 1), (CELL_SIZE - 2, CELL_SIZE - 2)) # creates fancy pattern
        else:
            self.rect = pygame.Rect((pos[0], pos[1]), (CELL_SIZE, CELL_SIZE)) # creates boring pattern
            
        self.mouse_mode = True # whether or not mouse needs to be let go to edit it
        self.coordinates = coordinates
        self.alive_last_gen = False
    
    
    def update_sprite(self): # draws onto the screen
        
        if self.life and self.new_update: # if it is alive
            color = ALIVE_COLOR # slightly brighter to show that it was just born
        elif self.life:
            color = [ALIVE_COLOR[0] / 1.3, ALIVE_COLOR[1] / 1.3, ALIVE_COLOR[2] / 1.3] # darker than newborn cells but still pops

        else: # but if it is dead
            color = DEAD_COLOR # hide its cadaver with a faint grey shroud
        
        pygame.draw.rect(screen, color, self.rect) # finally, draw it
        
        
    def process(self): # runs every frame, regardless of whether or not the time is ticking
        
        if not mouse_pressed: # if the mouse was unpressed
            self.mouse_mode = True # allow it to be edited again
            
        if mouse_pressed and self.rect.collidepoint(mouse_pos) and self.mouse_mode: # whether or not it can be edited
            # i have never made a tile grid editor this simply, python makes it super easy
            self.mouse_mode = False # stop it from being edited again (if this check didn't exist, it would change every frame while pressed)
            self.life = not self.life # inverts it
            self.new_update = True
            global play
            play = False
            
        if self.new_update: # if it was just born
            global updated_cells
            updated_cells += 1 # add 1 to the amount of new cells
        
        self.update_sprite() # draws it again
        
        
        if ticking: # this is most of the code
            neighbors = 0 # amount of living cells nearby
            self.alive_last_gen = self.life
            for x in range(3): # relative x coordinate
                cell_x = self.coordinates[0] + x - 1 # x coordinate
            
                if cell_x >= CELL_AMOUNT[0]: # makes x coordinate wrap
                    cell_x = 0
                elif cell_x < 0:
                    cell_x = CELL_AMOUNT[0] - 1
            
                
                for y in range(3): # relative y coordinate
                    cell_y = self.coordinates[1] + y - 1 # y coordinate
                    
                    if cell_y >= CELL_AMOUNT[1]: # makes y coordinate wrap
                        cell_y = 0
                    elif cell_y < 0:
                        cell_y = CELL_AMOUNT[1] - 1
                    
                    
                    if not (x == 1 and y == 1): # doesn't count itself as a neighbor
                        if cells[cell_x][cell_y].life: # if the cell it is checking is, indeed, alive
                            neighbors += 1 # add a living neighbor to the count
            
            if self.life: # harder to come to life than stay alive
                self.new_life = neighbors == 3 or neighbors == 2 # stays alive if it is either of these two values
            else: # if dead
                self.new_life = neighbors == 3 # comes to life if it is specifically 3
            
            self.new_update = self.new_life != self.alive_last_gen
            self.update_sprite()
            
        
    def update(self): # should be run after everything has processed. ensures cells use data from previous frames
        self.life = self.new_life





# CLASSES/FUNCTIONS END HERE






screen = pygame.display.set_mode(WINDOW_SIZE, pygame.SCALED)

frame = 0 # last frame that there was a tick
speed = 1
play = False
updated_cells = 0 # the amount of cells that were just born

mouse_clicked = False
mouse_pressed = False
space_held = False

buttons = [] # add any gui features to this list
buttons.append(Button(1, [500, 0], image_path = "button_theme.png")) # updates the theme when clicked
buttons.append(Button(2, [500, 80], image_path = "button_size.png")) # updates the cell size when clicked
buttons.append(Button(3, [500, 160], image_path = "button_clear.png")) # clears the board of cells
buttons.append(Button(4, [500, 240], image_path = "button_pause.png")) # pause / play
buttons.append(Button(5, [500, 320], image_path = "button_step.png")) # plays 1 generation when clicked
buttons.append(Button(6, [500, 400], image_path = "button_speed1.png")) # sets to slow speed
buttons.append(Button(7, [525, 400], image_path = "button_speed2.png")) # sets to medium speed
buttons.append(Button(8, [550, 400], image_path = "button_speed3.png")) # sets to fast speed


cells = [] # index 1 is column, index 2 is the cell in the column

for x in range(CELL_AMOUNT[0]): # adds the columns to the cell list
    column = [] # new blank column
    
    for y in range(CELL_AMOUNT[1]): # adds the cells to the column

        
        new_cell = Cell([x * CELL_SIZE, y * CELL_SIZE], (x, y)) # new blank cell
        column.append(new_cell) # add it to the column
    
    cells.append(column) # add it to the massive list
        
generation = 0
text = pygame.font.Font(pygame.font.get_default_font(), 16)

# starts with a glider
cells[14][15].life = True
cells[15][15].life = True
cells[16][15].life = True
cells[16][14].life = True
cells[15][13].life = True
cells[14][15].new_life = True
cells[15][15].new_life = True
cells[16][15].new_life = True
cells[16][14].new_life = True
cells[15][13].new_life = True

running = True
while running: # REMEMBER TO BREAK THIS LATER
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    
    frame += 1
    screen.fill(BACKGROUND_COLOR)
    
    pygame.event.pump() # new events
    pygame.event.get() # new events, volume 2
    
    mouse_pos = pygame.mouse.get_pos() # gets this once per frame
    space_held = pygame.key.get_pressed()[pygame.K_SPACE] # one means of unpausing
    
    ticking = space_held # says whether or not it should tick this frame
    if not mouse_pressed and pygame.mouse.get_pressed()[0]: # makes sure mouse cant be held to activate buttons
        mouse_clicked = True
    else:
        mouse_clicked = False    
    mouse_pressed = pygame.mouse.get_pressed()[0] # gets whether or not the mouse is pressed


    # it is important to do this step before to make sure the step function works
    for button in buttons: # updates the image and checks if every button is clicked
        screen.blit(button.image, button.pos)
        if mouse_clicked and button.rect.collidepoint(mouse_pos):
            button.click()    
            
    if not ticking:
        ticking = play and pygame.time.get_ticks() - frame >= 16 * (2 ** (4 - speed)) # only ticks when frame is above a certain value
    
    updated_cells = 0
    for column in cells: # goes over every cell and processes it
        for cell in column:
            cell.process() # processes it, most code is in the cell class
            

    if ticking and updated_cells > 0: # update cells while running, if nothing updated last frame then nothing will update this frame.
        for column in cells: # goes over every cell and updates it
            for cell in column:
                cell.update() # updates it, this just commits whatever operation was done in cell.process)_
        generation += 1
        frame = pygame.time.get_ticks()
        
    elif updated_cells == 0:
        play = False # stop playing if there are no recently-born cells

    text_surface = text.render("Gen " + str(generation), True, ALIVE_COLOR)
    screen.blit(text_surface, (500, 430))
    text_surface = text.render(str(CELL_AMOUNT[0]) + "x" + str(CELL_AMOUNT[1]), True, ALIVE_COLOR)
    screen.blit(text_surface, (500, 448))
    text_surface = text.render("Speed: " + str(speed), True, ALIVE_COLOR)
    screen.blit(text_surface, (500, 464))
    
    pygame.display.flip() # pygame.display.flip()
