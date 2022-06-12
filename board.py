import pygame


# RGB color
ORANGE = (236, 140, 85)
GREY = (187, 174, 161)
BROWN = (219, 212, 206)
WHITE = (255, 255, 255)


class Board:
    """
    Don't modify the value of class variables below.
    """
    M, N = 10, 15
    font_size = 15
    offset, candy_offset, grid_offset = 15, 2, 5
    candy_width, candy_height = 30, 30
    grid_width = (candy_width + candy_offset) * M + 2*grid_offset - candy_offset
    grid_height = (candy_height + candy_offset) * N + 2*grid_offset - candy_offset
    box_width, box_height = (grid_width - offset) / 2, 60
    screen_width, screen_height = grid_width + 2*offset, grid_height + 3*box_height + 4*offset

    def __init__(self, stud_id, name, game, row=10, col=15):
        self.update(row, col)

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("HW4 - " + stud_id + " " + name)

        # initialize scores, turns, and grid
        self._turns = 0
        self._score = 0
        self._target_score = 0
        self._best_score = 0
        self._grid = None

        self.game = game

        """
        Don't modify the value of instance variables below.
        """
        self._is_highlighted = False
        self._candy_box_ulx = self.offset + self.grid_offset
        self._candy_box_uly = 3 * (self.box_height + self.offset) + self.grid_offset
        
        self._candy_box_drx = self.offset + self.M * (self.candy_width + self.candy_offset) + self.grid_offset
        self._candy_box_dry = 3 * (self.box_height + self.offset) + self.N * (self.candy_height + self.candy_offset) + self.grid_offset

        self._highlighted_candy_row = None
        self._highlighted_candy_col = None

    # TODO: Complete the following setter functions
    def set_turns(self, turns):
        pass

    def set_score(self, score):
        pass

    def set_target_score(self, target_score):
        pass

    def set_best_score(self, best_score):
        pass

    def save_best_score(self):
        # save the best score to 'best_score.txt'.
        pass

    def load_best_score(self):
        # load the previous best score from 'best_score.txt'.
        pass

    def set_grid(self, grid):
        self._grid = grid

    def get_grid(self):
        return self._grid

    def get_best_score(self):
        pass

    """ Don't modify functions below """
    @classmethod
    def update(cls, row, col):
        cls.M = row
        cls.N = col
        cls.grid_width = (cls.candy_width + cls.candy_offset) * cls.M + 2*cls.grid_offset - cls.candy_offset
        cls.grid_height = (cls.candy_height + cls.candy_offset) * cls.N + 2*cls.grid_offset - cls.candy_offset
        cls.box_width = (cls.grid_width - cls.offset) / 2
        cls.screen_width = cls.grid_width + 2*cls.offset
        cls.screen_height = cls.grid_height + 3*cls.box_height + 4*cls.offset

    def click_button(self, x, y):
        if (self.grid_width - 2 * self.offset <= x <= self.grid_width - 2 * self.offset + 25
                and self.offset <= y <= self.offset + 25):
            return True
        else:
            return False

    def click_candy(self, x, y):
        if self._candy_box_ulx <= x <= self._candy_box_drx and self._candy_box_uly <= y <= self._candy_box_dry:
            return True
        else:
            return False

    def click_continue(self, x, y):
        box_width, box_height = self.candy_width * 5, self.candy_height * 1.5
        ulx, uly = self.screen_width / 2 - box_width / 2, self.screen_height - self.grid_height * 1/2
        if ulx <= x <= ulx + box_width and uly - 3/2*box_height <= y <= uly - 1/2*box_height:
            return True
        else:
            return False

    def click_restart(self, x, y):
        box_width, box_height = self.candy_width * 5, self.candy_height * 1.5
        ulx, uly = self.screen_width / 2 - box_width / 2, self.screen_height - self.grid_height * 1/2
        if ulx <= x <= ulx + box_width and uly - 1/2*box_height + 10 <= y <= uly + 1/2*box_height + 10:
            return True
        else:
            return False

    def click_quit(self, x, y):
        box_width, box_height = self.candy_width * 5, self.candy_height * 1.5
        ulx, uly = self.screen_width / 2 - box_width / 2, self.screen_height - self.grid_height * 1/2
        if ulx <= x <= ulx + box_width and uly + 1/2*box_height + 20 <= y <= uly + 3/2*box_height + 20:
            return True
        else:
            return False

    def draw(self):
        offset, candy_offset, grid_offset = self.offset, self.candy_offset, self.grid_offset
        font_size = self.font_size
        box_width, box_height = self.box_width, self.box_height
        grid_width, grid_height = self.grid_width, self.grid_height
        candy_width, candy_height = self.candy_width, self.candy_height

        # Screen background
        self.screen.fill((250, 248, 239))

        # Title
        font = pygame.font.SysFont('arial', 2*font_size, True, False)
        text = font.render('Candy Crush', True, (112, 98, 89))
        self.screen.blit(text, (offset, offset))

        # Button
        button = pygame.image.load('./images/continue.png')
        button = pygame.transform.scale(button, (25, 25))
        self.screen.blit(button, (grid_width - 2*offset, offset))

        # Turns
        pygame.draw.rect(self.screen, GREY, [offset, box_height+offset, box_width, box_height], 0)
        font = pygame.font.SysFont('arial', font_size, True, False)
        turns = font.render('TURNS', True, BROWN)
        self.text_blit(turns, offset + box_width / 2, box_height + offset + font_size)
        turns_num = font.render(str(self._turns), True, WHITE)
        self.text_blit(turns_num, offset + box_width / 2, box_height + offset + 5/2*font_size)

        # Best score
        pygame.draw.rect(self.screen, GREY, [offset*2+box_width, box_height+offset, box_width, box_height], 0)
        best_score = font.render('BEST SCORE', True, BROWN)
        self.text_blit(best_score, 2 * offset + 3/2 * box_width, box_height + offset + font_size)
        bscore_num = font.render(str(self._best_score), True, WHITE)
        self.text_blit(bscore_num, 2 * offset + 3/2 * box_width, box_height + offset + 5/2*font_size)

        # Score
        pygame.draw.rect(self.screen, GREY, [offset, 2*(box_height+offset), box_width, box_height], 0)
        score = font.render('SCORE', True, BROWN)
        self.text_blit(score, offset + box_width / 2, 2 * box_height + 2 * offset + font_size)
        score_num = font.render(str(self._score), True, WHITE)
        self.text_blit(score_num, offset + box_width / 2, 2 * box_height + 2 * offset + 5/2*font_size)

        # Target score
        pygame.draw.rect(self.screen, GREY, [offset*2+box_width, 2*(box_height+offset), box_width, box_height], 0)
        target_score = font.render('TARGET SCORE', True, BROWN)
        self.text_blit(target_score, 2 * offset + 3/2 * box_width, 2 * box_height + 2 * offset + font_size)
        tscore_num = font.render(str(self._target_score), True, WHITE)
        self.text_blit(tscore_num, 2 * offset + 3/2 * box_width, 2 * box_height + 2 * offset + 5/2*font_size)

        # Board
        pygame.draw.rect(self.screen, GREY, [offset, 3*(box_height+offset), grid_width, grid_height], 0)
        for row in range(self.N):
            up_left_y = 3 * (box_height+offset) + row * (candy_height + candy_offset) + grid_offset
            for col in range(self.M):
                up_left_x = offset + col * (candy_width + candy_offset) + grid_offset
                pygame.draw.rect(self.screen, (239, 223, 212), [up_left_x, up_left_y, candy_width, candy_height], 0)
        
        self.draw_candy_grid()

        if self._is_highlighted:
            self._is_highlighted = False
            self.draw_highlight(self._highlighted_tile_x, self._highlighted_tile_y)

    def draw_candy_grid(self):
        for row in range(self.N):
            up_left_y = 3 * (self.box_height+self.offset) + row * (self.candy_height + self.candy_offset) + self.grid_offset
            for col in range(self.M):
                up_left_x = self.offset + col * (self.candy_width + self.candy_offset) + self.grid_offset
                if self._grid[row][col] == 0:
                    pygame.draw.rect(self.screen, (239, 223, 212), [up_left_x, up_left_y, self.candy_width, self.candy_height], 0)
                else:
                    image_dir = self._grid[row][col].img_dir
                    candy_image = pygame.image.load(image_dir)
                    candy_image = pygame.transform.scale(candy_image, (self.candy_width, self.candy_height))
                    self.screen.blit(candy_image, (self._grid[row][col].coord[0], self._grid[row][col].coord[1]))

    def draw_stop(self):
        self.draw()

        box_width, box_height = self.candy_width * 5, self.candy_height * 1.5
        ulx, uly = self.screen_width / 2 - box_width / 2, self.screen_height - self.grid_height * 1/2
        font = pygame.font.SysFont('arial', 30, True, False)
        # Continue
        pygame.draw.rect(self.screen, ORANGE, [ulx, uly - 3/2*box_height, box_width, box_height], 0)
        continue_text = font.render("Continue", True, WHITE)
        self.text_blit(continue_text, ulx + box_width/2, uly - box_height)

        # Restart
        pygame.draw.rect(self.screen, ORANGE, [ulx, uly - 1/2*box_height + 10, box_width, box_height], 0)
        restart_text = font.render("Restart", True, WHITE)
        self.text_blit(restart_text, ulx + box_width/2, uly + 10)

        # Quit
        pygame.draw.rect(self.screen, ORANGE, [ulx, uly + 1/2*box_height + 20, box_width, box_height], 0)
        quit_text = font.render("Quit", True, WHITE)
        self.text_blit(quit_text, ulx + box_width/2, uly + box_height + 20)

    def text_blit(self, text, cx, cy):
        rect = text.get_rect()
        rect.centerx = cx
        rect.centery = cy
        self.screen.blit(text, rect)

    def draw_highlight(self, x, y):
        candy_tile_width = self.candy_width + self.candy_offset
        candy_tile_height = self.candy_height + self.candy_offset
        
        highlighted_tile_x = self._candy_box_ulx + (x - self._candy_box_ulx) // candy_tile_width * candy_tile_width
        highlighted_tile_y = self._candy_box_uly + (y - self._candy_box_uly) // candy_tile_height * candy_tile_height
        
        row = (y - self._candy_box_uly) // candy_tile_height
        col = (x - self._candy_box_ulx) // candy_tile_width

        swap = None
        if not self._is_highlighted:
            self._highlighted_tile_x = highlighted_tile_x
            self._highlighted_tile_y = highlighted_tile_y
            pygame.draw.rect(self.screen, (255, 0, 0), [highlighted_tile_x, highlighted_tile_y, self.candy_width, self.candy_height], 5)
            self._highlighted_candy_row = row
            self._highlighted_candy_col = col
            self._is_highlighted = True
        else:
            if self._highlighted_tile_x == highlighted_tile_x and self._highlighted_tile_y == highlighted_tile_y:
                #Select the same spot
                pass

            elif not ((abs(self._highlighted_tile_x - highlighted_tile_x) == candy_tile_width and (self._highlighted_tile_y == highlighted_tile_y)) 
                or (self._highlighted_tile_x == highlighted_tile_x and (abs(self._highlighted_tile_y - highlighted_tile_y) == candy_tile_height))):
                #Select invalid place
                image_dir = self._grid[self._highlighted_candy_row][self._highlighted_candy_col].img_dir
                candy_image = pygame.image.load(image_dir)
                candy_image = pygame.transform.scale(candy_image, (self.candy_width, self.candy_height))
                center_x = self.offset + self._highlighted_candy_col * (self.candy_width + self.candy_offset) + self.grid_offset
                center_y = 3 * (self.box_height+self.offset) + self._highlighted_candy_row * (self.candy_height + self.candy_offset) + self.grid_offset

                pygame.draw.rect(self.screen, GREY, [self._highlighted_tile_x, self._highlighted_tile_y, self.candy_width, self.candy_height], 5)
                self.screen.blit(candy_image, (center_x, center_y))

                self._is_highlighted = False
            else:
                #Select valid place
                reference_candy = self._grid[self._highlighted_candy_row][self._highlighted_candy_col]
                target_candy = self._grid[row][col]

                swap = [reference_candy, target_candy]
                self._is_highlighted = False

        return swap

    def swap_candies(self, block_pair):
        self._grid[block_pair[0].grid[0]][block_pair[0].grid[1]] = block_pair[1]
        self._grid[block_pair[1].grid[0]][block_pair[1].grid[1]] = block_pair[0]

        tmp_grid = block_pair[0].grid
        tmp_coord = block_pair[0].coord
        block_pair[0].grid = block_pair[1].grid
        block_pair[0].coord = block_pair[1].coord
        block_pair[1].grid = tmp_grid
        block_pair[1].coord = tmp_coord

    def initialize_candy(self):
        for row in range(self.N):
            center_y = 3 * (self.box_height + self.offset) + row * (
                        self.candy_height + self.candy_offset) + self.grid_offset
            for col in range(self.M):
                center_x = self.offset + col * (self.candy_width + self.candy_offset) + self.grid_offset
                if self._grid[row][col] == 0:
                    continue
                else:
                    self._grid[row][col].coord = [center_x, center_y]
                    self._grid[row][col].grid = [row, col]

            
