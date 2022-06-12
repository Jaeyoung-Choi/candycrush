import random
import copy
import pygame
import sys
from candy import Candy
from pygame.locals import *

class CandyCrush:
    def __init__(self, gridsize):
        self.n_move = 10
        self.score = 0
        self.gridsize = gridsize
        self.candies = None

        self.grid = None
        self.board = None
        self.action = None
        self.move_counter = 0

        # you can add more variables if necessary
        self.counter = 0

        self.load_candy()

    def load_candy(self, input_file=None):
        #Example: It might be wrong, so you should correct the values below.
        self.candies = [ Candy('sky', 1, "./images/1.png"),\
                        Candy('blue', 1, "./images/2.png"),\
                        Candy('pink', 1, "./images/3.png"),\
                        Candy('purple', 1, "./images/4.png"),\
                        Candy('red', 1, "./images/5.png"),\
                        Candy('yellow', 1, "./images/6.png"),\
                        Candy('green', 1, "./images/7.png"),\
                        Candy('grey', 1, "./images/8.png")
                    ]
        ##
        # with open(input_file, 'r') as f:
        pass
    
    def update_grid(self, grid, block_pair):
        # TODO2. Pop candies process
        # Maintain swapped candies if swapped grid makes 3 consecutive candies of the same color, else restore (swap_candies)
        # Pop swapped item & 3/4/5 consecutive candies of the same color (pop_all_candies)
        # Fill empty grid (fill_grid)
        # Repeat until there are no more 3 consecutive candies of the same color (check_grid)
        # If any movement cannot make 3 consecutive candies of the same color, refresh the grid (check_infeasible_grid, refresh_grid)

        # TODO3. Pop remaining items process
        # Pop remaining items in the grid (pop_items)
        # Fill empty grid (fill_grid)
        # If there are 3 consecutive candies of the same color, pop 3/4/5 consecutive candies of the same color and fill empty grid (check_grid, pop_all_candiesm fill_grid)
        # Repeat until there are no items left

        # Example code
        self.grid = grid

        if self.counter == 0:
            self.grid[0][1] = 0
            self.grid[1][1] = 0
            self.grid[3][2] = 0
            self.grid[4][5] = 0
            self.board.set_grid(self.grid)
        elif self.counter == 1:
            self.grid = [[copy.deepcopy(random.sample(self.candies,1)[0]) for _ in range(self.gridsize[0])] for _ in range(self.gridsize[1])]
            self.board.set_grid(self.grid)
            self.board.initialize_candy()

        if self.counter == 0:
            self.counter += 1
            return True
        else:
            self.counter = 0
            return False

    # initialize random grid w/o 3 consecutive candies of the same color
    def initialize_grid(self):
        # TODO1. Modify initialize grid()
        # Initialize random grid w/o 3 consecutive candies of the same color until any movement can make 3 consecutive candies of the same color

        # Ex)
        self.grid = [[copy.deepcopy(random.sample(self.candies, 1)[0]) for _ in range(self.gridsize[0])] for _ in
                     range(self.gridsize[1])]

        self.board.set_grid(self.grid)
        self.board.initialize_candy()

    # return True if there are no 3 consecutive candies of the same color, else return False
    def check_grid(self, grid):
        return -1
    
    # return False if item exists or any movement makes 3 consecutive candies of the same color, else return True
    def check_infeasible_grid(self):
        return -1
    
    # swap candies for valid input
    def swap_candies(self):
        pass
    
    # pop candies if item is swapped in current move & pop all 5/4/3 consecutive candies of the same color
    def pop_all_candies(self):
        pass
    
    # fill grid if there exist empty space in grid
    def fill_grid(self):
        pass
                
    # refresh grid if any movement cannot make 3 consecutive candies of the same color
    def refresh_grid(self):
        pass
    
    # pop all remaining items in the grid
    def pop_items(self):
        pass

    # run game
    # you can add more functions but you must use all functions provided above 
    def run_game(self):
        self.initialize_grid()

        # initialize the game engine
        pygame.init()

        self.board.set_best_score(self.board.load_best_score())

        # FPS 초당 프레임 변수 설정
        clock = pygame.time.Clock()

        # initialize flags
        button_flag, continue_flag, restart_flag, quit_flag, candy_flag, wait_flag = False, False, False, False, False, False
        update_flag = False
        clock_fps = 15

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                # checks if a mouse is clicked
                if event.type == MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()

                    # if the mouse is clock on the button
                    if self.board.click_button(mouse[0], mouse[1]):
                        button_flag = not button_flag
                        wait_flag = False
                    elif self.board.click_continue(mouse[0], mouse[1]) and button_flag:
                        continue_flag = True
                        wait_flag = False
                    elif self.board.click_restart(mouse[0], mouse[1]) and button_flag:
                        restart_flag = True
                        wait_flag = False
                    elif self.board.click_quit(mouse[0], mouse[1]) and button_flag:
                        quit_flag = True
                        wait_flag = False
                    elif self.board.click_candy(mouse[0], mouse[1]):
                        candy_flag = True
                        mouse_coord = mouse
                        wait_flag = False

            if button_flag:
                self.board.draw_stop()
                if continue_flag:
                    self.board.draw()
                    button_flag, continue_flag, wait_flag = False, False, False
                elif restart_flag:
                    self.board.draw()
                    button_flag, restart_flag, wait_flag = False, False, False
                elif quit_flag:
                    pygame.quit()
                    sys.exit()
            elif update_flag or self.move_counter >= self.n_move:
                update_flag = self.update_grid(self.grid, self.action)
                self.board.draw_candy_grid()

                self.action = None
                wait_flag = False

                if (not update_flag) and (self.move_counter >= self.n_move):
                    pygame.display.update()
                    clock.tick(clock_fps)
                    break
            elif self.action is not None:
                # Swap candies in list, action[1]
                self.board.swap_candies(self.action)
                self.move_counter += 1

                self.board.draw()
                update_flag = True
                wait_flag = False

            elif candy_flag:
                self.action = self.board.draw_highlight(mouse_coord[0], mouse_coord[1])
                candy_flag = False

            elif not button_flag:
                self.board.draw()

            if not wait_flag:
                pygame.display.update()
                clock.tick(clock_fps)
                wait_flag = True


