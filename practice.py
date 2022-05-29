import pygame
import math
import os

# pygame initializer
pygame.init()
clock = pygame.time.Clock()
FPS = 10

# make screen
screen_width = 640
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Chess 2.0")

# colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
light = (200, 200, 200)
dark = (100, 100, 100)

# set up chess board
chess_board = [[0 for a in range(8)] for b in range(8)]
y_square = 0
width = 80
height = 80
for i in range(8):
    x_square = 0
    for j in range(8):
        if i % 2 == 0:
            if j % 2 == 0:
                chess_board[i][j] = pygame.draw.rect(screen, light, [x_square, y_square, width, height])
            else:
                chess_board[i][j] = pygame.draw.rect(screen, dark, [x_square, y_square, width, height])
        else:
            if j % 2 == 0:
                chess_board[i][j] = pygame.draw.rect(screen, dark, [x_square, y_square, width, height])
            else:
                chess_board[i][j] = pygame.draw.rect(screen, light, [x_square, y_square, width, height])
        x_square += 80
    y_square += 80


# images
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "Images")

blackpawn_img = "blackpawn.png"
whitepawn_img = "whitepawn.png"

blackrook_img = "blackrook.png"
whiterook_img = "whiterook.png"

blackknight_img = "blackknight.png"
whiteknight_img = "whiteknight.png"

blackbishop_img = "blackbishop.png"
whitebishop_img = "whitebishop.png"

blackqueen_img = "blackqueen.png"
whitequeen_img = "whitequeen.png"

blackking_img = "blackking.png"
whiteking_img = "whiteking.png"

redcircle_img = "redcircle.png"

# sprites
sprites = pygame.sprite.Group()
black_sprites = pygame.sprite.Group()
white_sprites = pygame.sprite.Group()

# lists
all_pieces = []
white_pieces = []
black_pieces = []

# variables
y_black = 40
y_white = 600
y_blackpawns = 120
y_whitepawns = 520
x_pawns = 40
x_rook1 = 40
x_rook2 = 600
x_knight1 = 120
x_knight2 = 520
x_bishop1 = 200
x_bishop2 = 440
x_queen = 280
x_king = 360
amt_of_turns = 1
black_turn = True
white_turn = False

# class for circle
class Circle(pygame.sprite.Sprite):

    def __init__(self, x=0, y=0):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = pygame.image.load(os.path.join(img_folder, redcircle_img))
        self.image = pygame.transform.scale(self.image, (15, 15))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def __str__(self):
        x_val = str(self.x)
        y_val = str(self.y)
        return "x, y = " + x_val + ", " + y_val

# class for pieces
class Piece(pygame.sprite.Sprite):

    def __init__(self, piece_img, x, y, color):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.board_x = 0
        self.board_y = 0
        self.color = color
        self.image = pygame.image.load(os.path.join(img_folder, piece_img))
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.free_x = []
        self.free_y = []
        self.not_free_x = []
        self.not_free_y = []
        self.circles_posX = []
        self.circles_negX = []
        self.circles_posY = []
        self.circles_negY = []
        self.blocks_posX = [1, 1, 1, 1, 1, 1, 1]
        self.blocks_negX = [1, 1, 1, 1, 1, 1, 1]
        self.blocks_posY = [1, 1, 1, 1, 1, 1, 1]
        self.blocks_negY = [1, 1, 1, 1, 1, 1, 1]
        self.circles_northeast = []
        self.circles_northwest = []
        self.circles_southeast = []
        self.circles_southwest = []
        self.blocks_northeast = [1, 1, 1, 1, 1, 1, 1]
        self.blocks_northwest = [1, 1, 1, 1, 1, 1, 1]
        self.blocks_southeast = [1, 1, 1, 1, 1, 1, 1]
        self.blocks_southwest = [1, 1, 1, 1, 1, 1, 1]
        self.click = False

    def find_board_position(self):
        for i in range(8):
            for j in range(8):
                if self.x in range(chess_board[i][j].x, chess_board[i][j].x + 80) and self.y in range(chess_board[i][j].y, chess_board[i][j].y + 80):
                    print("self.x, self.y = " + str(p.x) + ", " + str(p.y))
                    print("chess_board[" + str(i) + "]" + "[" + str(j) + "]" + ".x" + " = " + str(chess_board[i][j].x) + " < " + str(p.x) + " < " + str(chess_board[i][j].x + 80))
                    print("chess_board[" + str(i) + "]" + "[" + str(j) + "]" + ".y" + " = " + str(chess_board[i][j].y) + " < " + str(p.y) + " < " + str(chess_board[i][j].y + 80))
                    self.board_x = j
                    self.board_y = i
                    print(self.__str__() + "'s x on board = " + str(j))
                    print(self.__str__() + "'s y on board = " + str(i))

    def check_for_click(self, leftx, lefty):
        if self.x in range(leftx - 30, leftx + 30) and self.y in range(lefty - 30, lefty + 30):
            self.click = True

    def check_for_collision(self):
        if self.color == black:
            for p in white_pieces:
                if self.x == p.x and self.y == p.y:
                    white_pieces.remove(p)
                    all_pieces.remove(p)
                    p.kill()
        if self.color == white:
            for p in black_pieces:
                if self.x == p.x and self.y == p.y:
                    black_pieces.remove(p)
                    all_pieces.remove(p)
                    p.kill()

    def kill_circles(self, circle_list):
        for i in range(len(circle_list)):
            circle_list[i].kill()

    def set_all_blocks(self, blocks, x):
        for i in range(x, 7):
            blocks[i] = True

    def check_attack1(self, pieces):
        self.check_attack_positiveX(pieces)
        self.check_attack_negativeX(pieces)
        self.check_attack_positiveY(pieces)
        self.check_attack_negativeY(pieces)

    def check_attack2(self, pieces):
        self.check_attack_northeast(pieces)
        self.check_attack_northwest(pieces)
        self.check_attack_southeast(pieces)
        self.check_attack_southwest(pieces)

    def check_attack_positiveX(self, pieces):
        add = 80
        first_true = -1
        for i in range(len(self.blocks_posX)):
            if self.blocks_posX[i]:
                first_true = i
                break
            else:
                add += 80

        if first_true != -1:
            for p in pieces:
                if self.y == p.y and self.x + add == p.x:
                    self.blocks_posX[first_true] = False
        print("new list for positive x = " + str(self.blocks_posX))

    def check_attack_negativeX(self, pieces):
        add = 80
        first_true = -1
        for i in range(len(self.blocks_negX)):
            if self.blocks_negX[i]:
                first_true = i
                break
            else:
                add += 80

        if first_true != -1:
            for p in pieces:
                if self.y == p.y and self.x - add == p.x:
                    self.blocks_negX[first_true] = False
        print("new list for negative x = " + str(self.blocks_negX))

    def check_attack_positiveY(self, pieces):
        add = 80
        first_true = -1
        for i in range(len(self.blocks_posY)):
            if self.blocks_posY[i]:
                first_true = i
                break
            else:
                add += 80

        if first_true != -1:
            for p in pieces:
                if self.x == p.x and self.y + add == p.y:
                    self.blocks_posY[first_true] = False
        print("new list for positive y = " + str(self.blocks_posY))

    def check_attack_negativeY(self, pieces):
        add = 80
        first_true = -1
        for i in range(len(self.blocks_negY)):
            if self.blocks_negY[i]:
                first_true = i
                break
            else:
                add += 80

        if first_true != -1:
            for p in pieces:
                if self.x == p.x and self.y - add == p.y:
                    self.blocks_negY[first_true] = False
        print("new list for negative y = " + str(self.blocks_negY))

    def check_attack_northeast(self, pieces):
        add = 80
        first_true = -1
        for i in range(len(self.blocks_northeast)):
            if self.blocks_northeast[i]:
                first_true = i
                break
            else:
                add += 80

        if first_true != -1:
            for p in pieces:
                if self.y - add == p.y and self.x + add == p.x:
                    self.blocks_northeast[first_true] = False
        print("new list for northeast = " + str(self.blocks_northeast))

    def check_attack_northwest(self, pieces):
        add = 80
        first_true = -1
        for i in range(len(self.blocks_northwest)):
            if self.blocks_northwest[i]:
                first_true = i
                break
            else:
                add += 80

        if first_true != -1:
            for p in pieces:
                if self.y - add == p.y and self.x - add == p.x:
                    self.blocks_northwest[first_true] = False
        print("new list for northwest = " + str(self.blocks_northwest))

    def check_attack_southeast(self, pieces):
        add = 80
        first_true = -1
        for i in range(len(self.blocks_southeast)):
            if self.blocks_southeast[i]:
                first_true = i
                break
            else:
                add += 80

        if first_true != -1:
            for p in pieces:
                if self.x + add == p.x and self.y + add == p.y:
                    self.blocks_southeast[first_true] = False
        print("new list for southeast = " + str(self.blocks_southeast))

    def check_attack_southwest(self, pieces):
        add = 80
        first_true = -1
        for i in range(len(self.blocks_southwest)):
            if self.blocks_southwest[i]:
                first_true = i
                break
            else:
                add += 80

        if first_true != -1:
            for p in pieces:
                if self.x - add == p.x and self.y + add == p.y:
                    self.blocks_southwest[first_true] = False
        print("new list for southwest = " + str(self.blocks_southwest))

    def check_for_blocks1(self, pieces):
        num1 = 1
        num2 = 1
        num3 = 1
        num4 = 1
        add1 = 80
        add2 = 80
        add3 = 80
        add4 = 80
        for i in range(7):
            for p in pieces:
                if self.y == p.y and self.x + add1 == p.x:
                    self.set_all_blocks(self.blocks_posX, i)
                    num1 = 1
                    break
                elif self.y == p.y and self.x + add1 != p.x:
                    self.blocks_posX[i] = False
                    num1 = 2
            if num1 == 1:
                break
            add1 += 80
        for i in range(7):
            for p in pieces:
                if self.y == p.y and self.x - add2 == p.x:
                    self.set_all_blocks(self.blocks_negX, i)
                    num2 = 1
                    break
                elif self.y == p.y and self.x - add2 != p.x:
                    self.blocks_negX[i] = False
                    num2 = 2
            if num2 == 1:
                break
            add2 += 80
        for i in range(7):
            for p in pieces:
                if self.x == p.x and self.y + add3 == p.y:
                    self.set_all_blocks(self.blocks_posY, i)
                    num3 = 1
                    break
                elif self.x == p.x and self.y + add3 != p.y:
                    self.blocks_posY[i] = False
                    num3 = 2
            if num3 == 1:
                break
            add3 += 80
        for i in range(7):
            for p in pieces:
                if self.x == p.x and self.y - add4 == p.y:
                    self.set_all_blocks(self.blocks_negY, i)
                    num4 = 1
                    break
                elif self.x == p.x and self.y - add4 != p.y:
                    self.blocks_negY[i] = False
                    num4 = 2
            if num4 == 1:
                break
            add4 += 80

    def check_for_blocks2(self, pieces):
        num1 = 1
        num2 = 1
        num3 = 1
        num4 = 1
        add1 = 80
        add2 = 80
        add3 = 80
        add4 = 80
        for i in range(7):
            for p in pieces:
                if self.y - add1 == p.y and self.x + add1 == p.x:
                    self.set_all_blocks(self.blocks_northeast, i)
                    num1 = 1
                    break
                else:
                    self.blocks_northeast[i] = False
                    num1 = 2
            if num1 == 1:
                break
            add1 += 80
        for i in range(7):
            for p in pieces:
                if self.y - add2 == p.y and self.x - add2 == p.x:
                    self.set_all_blocks(self.blocks_northwest, i)
                    num2 = 1
                    break
                else:
                    self.blocks_northwest[i] = False
                    num2 = 2
            if num2 == 1:
                break
            add2 += 80
        for i in range(7):
            for p in pieces:
                if self.x + add3 == p.x and self.y + add3 == p.y:
                    self.set_all_blocks(self.blocks_southeast, i)
                    num3 = 1
                    break
                else:
                    self.blocks_southeast[i] = False
                    num3 = 2
            if num3 == 1:
                break
            add3 += 80
        for i in range(7):
            for p in pieces:
                if self.x - add4 == p.x and self.y + add4 == p.y:
                    self.set_all_blocks(self.blocks_southwest, i)
                    num4 = 1
                    break
                else:
                    self.blocks_southwest[i] = False
                    num4 = 2
            if num4 == 1:
                break
            add4 += 80

    def move_child1(self, new_x, new_y, circle_list):
        for i in range(len(circle_list)):
            if new_x in range(circle_list[i].x - 35, circle_list[i].x + 35) and new_y in range(circle_list[i].y - 35, circle_list[i].y + 35):
                self.rect.center = circle_list[i].rect.center
                self.x = circle_list[i].x
                self.y = circle_list[i].y

    def move1(self, new_x, new_y):
        self.move_child1(new_x, new_y, self.circles_posX)
        self.move_child1(new_x, new_y, self.circles_negX)
        self.move_child1(new_x, new_y, self.circles_posY)
        self.move_child1(new_x, new_y, self.circles_negY)

    def move_child2(self, new_x, new_y, circle_list):
        for i in range(len(circle_list)):
            if new_x in range(circle_list[i].x - 35, circle_list[i].x + 35) and new_y in range(circle_list[i].y - 35, circle_list[i].y + 35):
                self.rect.center = circle_list[i].rect.center
                self.x = circle_list[i].x
                self.y = circle_list[i].y

    def move2(self, new_x, new_y):
        self.move_child2(new_x, new_y, self.circles_northeast)
        self.move_child2(new_x, new_y, self.circles_northwest)
        self.move_child2(new_x, new_y, self.circles_southeast)
        self.move_child2(new_x, new_y, self.circles_southwest)


class Pawn(Piece):

    def __init__(self, piece_img, x, y, color):
        super().__init__(piece_img, x, y, color)
        self.circle1 = Circle()
        self.circle2 = Circle()
        self.black_attack1 = Circle()
        self.black_attack2 = Circle()
        self.white_attack1 = Circle()
        self.white_attack2 = Circle()
        self.block1 = False
        self.block2 = False

    def kill_pawn_circles(self):
        self.circle1.kill()
        self.circle2.kill()
        self.black_attack1.kill()
        self.black_attack2.kill()
        self.white_attack1.kill()
        self.white_attack2.kill()

    def check_blocks(self):
        if self.color == black:
            for p in all_pieces:
                if self.y == y_blackpawns:
                    if self.x == p.x and self.y + 80 == p.y:
                        print("black pawn in starting position, blocked completely")
                        self.block1 = True
                        self.block2 = True
                    elif self.x == p.x and self.y + 160 == p.y:
                        print("black pawn in starting position, blocked partially")
                        self.block2 = True
                else:
                    if self.x == p.x and self.y + 80 == p.y:
                        print("black pawn is blocked")
                        self.block1 = True
        elif self.color == white:
            for p in all_pieces:
                if self.y == y_whitepawns:
                    if self.x == p.x and self.y - 80 == p.y:
                        print("white pawn in starting position, blocked completely")
                        self.block1 = True
                        self.block2 = True
                    elif self.x == p.x and self.y - 160 == p.y:
                        print("white pawn in starting position, blocked partially")
                        self.block2 = True
                else:
                    if self.x == p.x and self.y - 80 == p.y:
                        print("white pawn is blocked")
                        self.block1 = True

    def possible_moves(self):
        if self.click:
            self.check_blocks()
            if self.color == black:
                if self.y == y_blackpawns and not self.block1 and not self.block2:
                    print("black pawn in starting position")
                    self.circle1.rect.center = (self.x, self.y + 80)
                    self.circle1.x = self.x
                    self.circle1.y = self.y + 80
                    self.circle2.rect.center = (self.x, self.y + 160)
                    self.circle2.x = self.x
                    self.circle2.y = self.y + 160
                    sprites.add(self.circle1)
                    sprites.add(self.circle2)
                elif not self.block1:
                    self.circle1.rect.center = (self.x, self.y + 80)
                    self.circle1.x = self.x
                    self.circle1.y = self.y + 80
                    sprites.add(self.circle1)
                for p in white_pieces:
                    if self.x + 80 == p.x and self.y + 80 == p.y:
                        self.black_attack1.rect.center = (p.x, p.y)
                        sprites.add(self.black_attack1)
                    elif self.x - 80 == p.x and self.y + 80 == p.y:
                        self.black_attack2.rect.center = (p.x, p.y)
                        sprites.add(self.black_attack2)
            if self.color == white:
                if self.y == y_whitepawns and not self.block1 and not self.block2:
                    print("white pawn in starting position")
                    self.circle1.rect.center = (self.x, self.y - 80)
                    self.circle1.x = self.x
                    self.circle1.y = self.y - 80
                    self.circle2.rect.center = (self.x, self.y - 160)
                    self.circle2.x = self.x
                    self.circle2.y = self.y - 160
                    sprites.add(self.circle1)
                    sprites.add(self.circle2)
                elif not self.block1:
                    self.circle1.rect.center = (self.x, self.y - 80)
                    self.circle1.x = self.x
                    self.circle1.y = self.y - 80
                    sprites.add(self.circle1)
                for p in black_pieces:
                    if self.x + 80 == p.x and self.y - 80 == p.y:
                        self.white_attack1.rect.center = (p.x, p.y)
                        sprites.add(self.white_attack1)
                    elif self.x - 80 == p.x and self.y - 80 == p.y:
                        self.white_attack2.rect.center = (p.x, p.y)
                        sprites.add(self.white_attack2)

    def starting_position_move(self, new_x, new_y):
        if new_x in range(self.circle1.x - 35, self.circle1.x + 35) and new_y in range(self.circle1.y - 35, self.circle1.y + 35):
            print("moved to 1st circle")
            self.rect.center = self.circle1.rect.center
            self.x = self.circle1.x
            self.y = self.circle1.y
        elif new_x in range(self.circle2.x - 35, self.circle2.x + 35) and new_y in range(self.circle2.y - 35, self.circle2.y + 35):
            print("moved to 2nd circle")
            self.rect.center = self.circle2.rect.center
            self.x = self.circle2.x
            self.y = self.circle2.y

    def attack_move_black(self, new_x, new_y):
        attack1_x = self.black_attack1.rect.center[0]
        attack1_y = self.black_attack1.rect.center[1]
        attack2_x = self.black_attack2.rect.center[0]
        attack2_y = self.black_attack2.rect.center[1]
        attack1_x_range = range(attack1_x - 35, attack1_x + 35)
        attack1_y_range = range(attack1_y - 35, attack1_y + 35)
        attack2_x_range = range(attack2_x - 35, attack2_x + 35)
        attack2_y_range = range(attack2_y - 35, attack2_y + 35)
        if new_x in attack1_x_range and new_y in attack1_y_range:
            self.rect.center = self.black_attack1.rect.center
            self.x = self.black_attack1.rect.center[0]
            self.y = self.black_attack1.rect.center[1]
            print("moved to circle diagonally right")
        if new_x in attack2_x_range and new_y in attack2_y_range:
            self.rect.center = self.black_attack2.rect.center
            self.x = self.black_attack2.rect.center[0]
            self.y = self.black_attack2.rect.center[1]
            print("moved to circle diagonally left")

    def attack_move_white(self, new_x, new_y):
        attack1_x = self.white_attack1.rect.center[0]
        attack1_y = self.white_attack1.rect.center[1]
        attack2_x = self.white_attack2.rect.center[0]
        attack2_y = self.white_attack2.rect.center[1]
        attack1_x_range = range(attack1_x - 35, attack1_x + 35)
        attack1_y_range = range(attack1_y - 35, attack1_y + 35)
        attack2_x_range = range(attack2_x - 35, attack2_x + 35)
        attack2_y_range = range(attack2_y - 35, attack2_y + 35)
        if new_x in attack1_x_range and new_y in attack1_y_range:
            self.rect.center = self.white_attack1.rect.center
            self.x = self.white_attack1.rect.center[0]
            self.y = self.white_attack1.rect.center[1]
            print("moved to circle diagonally right")
        if new_x in attack2_x_range and new_y in attack2_y_range:
            self.rect.center = self.white_attack2.rect.center
            self.x = self.white_attack2.rect.center[0]
            self.y = self.white_attack2.rect.center[1]
            print("moved to circle diagonally left")

    def move(self, new_x, new_y):
        if self.click:
            if self.color == black:
                if self.y == y_blackpawns:
                    self.starting_position_move(new_x, new_y)
                elif new_x in range(self.circle1.x - 35, self.circle1.x + 35) and new_y in range(self.circle1.y - 35, self.circle1.y + 35):
                    print("moved to 1st circle")
                    self.rect.center = self.circle1.rect.center
                    self.x = self.circle1.x
                    self.y = self.circle1.y
                self.attack_move_black(new_x, new_y)
            if self.color == white:
                if self.y == y_whitepawns:
                    self.starting_position_move(new_x, new_y)
                elif new_x in range(self.circle1.x - 35, self.circle1.x + 35) and new_y in range(self.circle1.y - 35, self.circle1.y + 35):
                    print("moved to 1st circle")
                    self.rect.center = self.circle1.rect.center
                    self.x = self.circle1.x
                    self.y = self.circle1.y
                self.attack_move_white(new_x, new_y)
        # self.click = False
        self.block1 = False
        self.block2 = False
        self.kill_pawn_circles()

    def __str__(self):
        if self.color == black:
            color = "Black"
        else:
            color = "White"
        return color + " Pawn"

class Rook(Piece):

    def __init__(self, piece_img, x, y, color):
        super().__init__(piece_img, x, y, color)

    def check_blocks(self):
        if self.color == black:
            self.check_for_blocks1(all_pieces)
            print("block in positive x: " + str(self.blocks_posX))
            print("block in negative x: " + str(self.blocks_negX))
            print("block in positive y: " + str(self.blocks_posY))
            print("block in negative y: " + str(self.blocks_negY))
            self.check_attack1(white_pieces)
        if self.color == white:
            self.check_for_blocks1(all_pieces)
            print("block in positive x: " + str(self.blocks_posX))
            print("block in negative x: " + str(self.blocks_negX))
            print("block in positive y: " + str(self.blocks_posY))
            print("block in negative y: " + str(self.blocks_negY))
            self.check_attack1(black_pieces)

    def possible_moves(self):
        if self.click:
            self.check_blocks()
            add = 80
            for i in range(7):
                if not self.blocks_posX[i]:
                    circle1 = Circle(self.x + add, self.y)
                    self.circles_posX.append(circle1)
                    sprites.add(circle1)
                if not self.blocks_negX[i]:
                    circle2 = Circle(self.x - add, self.y)
                    self.circles_negX.append(circle2)
                    sprites.add(circle2)
                if not self.blocks_posY[i]:
                    circle3 = Circle(self.x, self.y + add)
                    self.circles_posY.append(circle3)
                    sprites.add(circle3)
                if not self.blocks_negY[i]:
                    circle4 = Circle(self.x, self.y - add)
                    self.circles_negY.append(circle4)
                    sprites.add(circle4)
                add += 80

    def move(self, new_x, new_y):
        if self.click:
            self.move1(new_x, new_y)
        # self.click = False
        self.kill_circles(self.circles_posX)
        self.kill_circles(self.circles_negX)
        self.kill_circles(self.circles_posY)
        self.kill_circles(self.circles_negY)

    def __str__(self):
        if self.color == black:
            color = "Black"
        else:
            color = "White"
        return color + " Rook"

class Knight(Piece):

    def __init__(self, piece_img, x, y, color):
        super().__init__(piece_img, x, y, color)
        self.circle_positiveX1 = Circle()
        self.circle_positiveX2 = Circle()
        self.circle_negativeX1 = Circle()
        self.circle_negativeX2 = Circle()
        self.circle_positiveY1 = Circle()
        self.circle_positiveY2 = Circle()
        self.circle_negativeY1 = Circle()
        self.circle_negativeY2 = Circle()
        self.block_px1 = False
        self.block_px2 = False
        self.block_nx1 = False
        self.block_nx2 = False
        self.block_py1 = False
        self.block_py2 = False
        self.block_ny1 = False
        self.block_ny2 = False

    def set_block_false(self):
        self.block_px1 = False
        self.block_px2 = False
        self.block_nx1 = False
        self.block_nx2 = False
        self.block_py1 = False
        self.block_py2 = False
        self.block_ny1 = False
        self.block_ny2 = False

    def kill_knight_circles(self):
        self.circle_positiveX1.kill()
        self.circle_positiveX2.kill()
        self.circle_negativeX1.kill()
        self.circle_negativeX2.kill()
        self.circle_positiveY1.kill()
        self.circle_positiveY2.kill()
        self.circle_negativeY1.kill()
        self.circle_negativeY2.kill()

    def check_blocks(self, pieces):
        for p in pieces:
            if self.x + 160 == p.x and self.y + 80 == p.y:
                self.block_px1 = True
                self.circle_positiveX1.kill()
            if self.x + 160 == p.x and self.y - 80 == p.y:
                self.block_px2 = True
                self.circle_positiveX2.kill()
            if self.x - 160 == p.x and self.y + 80 == p.y:
                self.block_nx1 = True
                self.circle_negativeX1.kill()
            if self.x - 160 == p.x and self.y - 80 == p.y:
                self.block_nx2 = True
                self.circle_negativeX2.kill()
            if self.y + 160 == p.y and self.x + 80 == p.x:
                self.block_py1 = True
                self.circle_positiveY1.kill()
            if self.y + 160 == p.y and self.x - 80 == p.x:
                self.block_py2 = True
                self.circle_positiveY2.kill()
            if self.y - 160 == p.y and self.x + 80 == p.x:
                self.block_ny1 = True
                self.circle_negativeY1.kill()
            if self.y - 160 == p.y and self.x - 80 == p.x:
                self.block_ny2 = True
                self.circle_negativeY2.kill()

    def make_circles(self, circle, x, y):
        circle.x = self.x + x
        circle.y = self.y + y
        circle.rect.center = (circle.x, circle.y)
        sprites.add(circle)

    def possible_moves(self):
        if self.click:
            self.make_circles(self.circle_positiveX1, 160, 80)
            self.make_circles(self.circle_positiveX2, 160, -80)
            self.make_circles(self.circle_negativeX1, -160, 80)
            self.make_circles(self.circle_negativeX2, -160, -80)
            self.make_circles(self.circle_positiveY1, 80, 160)
            self.make_circles(self.circle_positiveY2, -80, 160)
            self.make_circles(self.circle_negativeY1, 80, -160)
            self.make_circles(self.circle_negativeY2, -80, -160)
            if self.color == black:
                self.check_blocks(black_pieces)
            if self.color == white:
                self.check_blocks(white_pieces)

    def move_child(self, new_x, new_y, circle, block):
        if not block:
            if new_x in range(circle.x - 35, circle.x + 35) and new_y in range(circle.y - 35, circle.y + 35):
                self.rect.center = circle.rect.center
                self.x = circle.x
                self.y = circle.y

    def move(self, new_x, new_y):
        if self.click:
            self.move_child(new_x, new_y, self.circle_positiveX1, self.block_px1)
            self.move_child(new_x, new_y, self.circle_positiveX2, self.block_px2)
            self.move_child(new_x, new_y, self.circle_negativeX1, self.block_nx1)
            self.move_child(new_x, new_y, self.circle_negativeX2, self.block_nx2)
            self.move_child(new_x, new_y, self.circle_positiveY1, self.block_py1)
            self.move_child(new_x, new_y, self.circle_positiveY2, self.block_py2)
            self.move_child(new_x, new_y, self.circle_negativeY1, self.block_ny1)
            self.move_child(new_x, new_y, self.circle_negativeY2, self.block_ny2)
        self.kill_knight_circles()
        self.set_block_false()
        # self.click = False

    def __str__(self):
        if self.color == black:
            color = "Black"
        else:
            color = "White"
        return color + " Knight"

class Bishop(Piece):

    def __init__(self, piece_img, x, y, color):
        super().__init__(piece_img, x, y, color)

    def check_blocks(self):
        if self.color == black:
            self.check_for_blocks2(all_pieces)
            print("block in northeast: " + str(self.blocks_northeast))
            print("block in northwest: " + str(self.blocks_northwest))
            print("block in southeast: " + str(self.blocks_southeast))
            print("block in southwest: " + str(self.blocks_southwest))
            self.check_attack2(white_pieces)
        if self.color == white:
            self.check_for_blocks2(all_pieces)
            print("block in northeast: " + str(self.blocks_northeast))
            print("block in northwest: " + str(self.blocks_northwest))
            print("block in southeast: " + str(self.blocks_southeast))
            print("block in southwest: " + str(self.blocks_southwest))
            self.check_attack2(black_pieces)

    def possible_moves(self):
        if self.click:
            self.check_blocks()
            add = 80
            for i in range(7):
                if not self.blocks_northeast[i]:
                    circle1 = Circle(self.x + add, self.y - add)
                    self.circles_northeast.append(circle1)
                    sprites.add(circle1)
                if not self.blocks_northwest[i]:
                    circle2 = Circle(self.x - add, self.y - add)
                    self.circles_northwest.append(circle2)
                    sprites.add(circle2)
                if not self.blocks_southeast[i]:
                    circle3 = Circle(self.x + add, self.y + add)
                    self.circles_southeast.append(circle3)
                    sprites.add(circle3)
                if not self.blocks_southwest[i]:
                    circle4 = Circle(self.x - add, self.y + add)
                    self.circles_southwest.append(circle4)
                    sprites.add(circle4)
                add += 80

    def move(self, new_x, new_y):
        if self.click:
            self.move2(new_x, new_y)
        # self.click = False
        self.kill_circles(self.circles_northeast)
        self.kill_circles(self.circles_northwest)
        self.kill_circles(self.circles_southeast)
        self.kill_circles(self.circles_southwest)

    def __str__(self):
        if self.color == black:
            color = "Black"
        else:
            color = "White"
        return color + " Bishop"

class Queen(Piece):

    def __init__(self, piece_img, x, y, color):
        super().__init__(piece_img, x, y, color)

    def check_attack(self, pieces):
        self.check_attack1(pieces)
        self.check_attack2(pieces)

    def check_blocks(self):
        if self.color == black:
            self.check_for_blocks1(all_pieces)
            self.check_for_blocks2(all_pieces)
            self.check_attack(white_pieces)
        if self.color == white:
            self.check_for_blocks1(all_pieces)
            self.check_for_blocks2(all_pieces)
            self.check_attack(black_pieces)

    def possible_moves1(self):
        if self.click:
            self.check_blocks()
            add = 80
            for i in range(7):
                if not self.blocks_posX[i]:
                    circle1 = Circle(self.x + add, self.y)
                    self.circles_posX.append(circle1)
                    sprites.add(circle1)
                if not self.blocks_negX[i]:
                    circle2 = Circle(self.x - add, self.y)
                    self.circles_negX.append(circle2)
                    sprites.add(circle2)
                if not self.blocks_posY[i]:
                    circle3 = Circle(self.x, self.y + add)
                    self.circles_posY.append(circle3)
                    sprites.add(circle3)
                if not self.blocks_negY[i]:
                    circle4 = Circle(self.x, self.y - add)
                    self.circles_negY.append(circle4)
                    sprites.add(circle4)
                add += 80

    def possible_moves2(self):
        if self.click:
            self.check_blocks()
            add = 80
            for i in range(7):
                if not self.blocks_northeast[i]:
                    circle1 = Circle(self.x + add, self.y - add)
                    self.circles_northeast.append(circle1)
                    sprites.add(circle1)
                if not self.blocks_northwest[i]:
                    circle2 = Circle(self.x - add, self.y - add)
                    self.circles_northwest.append(circle2)
                    sprites.add(circle2)
                if not self.blocks_southeast[i]:
                    circle3 = Circle(self.x + add, self.y + add)
                    self.circles_southeast.append(circle3)
                    sprites.add(circle3)
                if not self.blocks_southwest[i]:
                    circle4 = Circle(self.x - add, self.y + add)
                    self.circles_southwest.append(circle4)
                    sprites.add(circle4)
                add += 80

    def possible_moves(self):
        self.possible_moves1()
        self.possible_moves2()

    def move(self, new_x, new_y):
        if self.click:
            self.move1(new_x, new_y)
            self.move2(new_x, new_y)
        # self.click = False
        self.kill_circles(self.circles_posX)
        self.kill_circles(self.circles_negX)
        self.kill_circles(self.circles_posY)
        self.kill_circles(self.circles_negY)
        self.kill_circles(self.circles_northeast)
        self.kill_circles(self.circles_northwest)
        self.kill_circles(self.circles_southeast)
        self.kill_circles(self.circles_southwest)

    def __str__(self):
        if self.color == black:
            color = "Black"
        else:
            color = "White"
        return color + " Queen"

class King(Piece):

    def __init__(self, piece_img, x, y, color):
        super().__init__(piece_img, x, y, color)
        self.circle_px = Circle()
        self.circle_nx = Circle()
        self.circle_py = Circle()
        self.circle_ny = Circle()
        self.circle_ne = Circle()
        self.circle_se = Circle()
        self.circle_sw = Circle()
        self.circle_nw = Circle()
        self.block_px = False
        self.block_nx = False
        self.block_py = False
        self.block_ny = False
        self.block_ne = False
        self.block_se = False
        self.block_sw = False
        self.block_nw = False

    def kill_king_circles(self):
        self.circle_px.kill()
        self.circle_nx.kill()
        self.circle_py.kill()
        self.circle_ny.kill()
        self.circle_ne.kill()
        self.circle_se.kill()
        self.circle_sw.kill()
        self.circle_nw.kill()

    def reset_king_blocks(self):
        self.block_px = False
        self.block_nx = False
        self.block_py = False
        self.block_ny = False
        self.block_ne = False
        self.block_se = False
        self.block_sw = False
        self.block_nw = False

    def check_king_blocks(self, pieces):
        for p in pieces:
            if self.y == p.y and self.x + 80 == p.x:
                self.block_px = True
            if self.y == p.y and self.x - 80 == p.x:
                self.block_nx = True
            if self.x == p.x and self.y + 80 == p.y:
                self.block_py = True
            if self.x == p.x and self.y - 80 == p.y:
                self.block_ny = True
            if self.x + 80 == p.x and self.y - 80 == p.y:
                self.block_ne = True
            if self.x + 80 == p.x and self.y + 80 == p.y:
                self.block_se = True
            if self.x - 80 == p.x and self.y + 80 == p.y:
                self.block_sw = True
            if self.x - 80 == p.x and self.y - 80 == p.y:
                self.block_nw = True

    def make_king_circle(self, circle, x, y, block):
        if not block:
            circle.x = self.x + x
            circle.y = self.y + y
            circle.rect.center = (circle.x, circle.y)
            sprites.add(circle)

    def possible_moves(self):
        if self.color == black:
            self.check_king_blocks(black_pieces)
        if self.color == white:
            self.check_king_blocks(white_pieces)
        self.make_king_circle(self.circle_px, 80, 0, self.block_px)
        self.make_king_circle(self.circle_nx, -80, 0, self.block_nx)
        self.make_king_circle(self.circle_py, 0, 80, self.block_py)
        self.make_king_circle(self.circle_ny, 0, -80, self.block_ny)
        self.make_king_circle(self.circle_ne, 80, -80, self.block_ne)
        self.make_king_circle(self.circle_se, 80, 80, self.block_se)
        self.make_king_circle(self.circle_sw, -80, 80, self.block_sw)
        self.make_king_circle(self.circle_nw, -80, -80, self.block_nw)

    def move_king_child(self, new_x, new_y, circle):
        if new_x in range(circle.x - 35, circle.x + 35) and new_y in range(circle.y - 35, circle.y + 35):
            self.rect.center = circle.rect.center
            self.x = circle.x
            self.y = circle.y

    def move(self, new_x, new_y):
        if self.click:
            self.move_king_child(new_x, new_y, self.circle_px)
            self.move_king_child(new_x, new_y, self.circle_nx)
            self.move_king_child(new_x, new_y, self.circle_py)
            self.move_king_child(new_x, new_y, self.circle_ny)
            self.move_king_child(new_x, new_y, self.circle_ne)
            self.move_king_child(new_x, new_y, self.circle_se)
            self.move_king_child(new_x, new_y, self.circle_sw)
            self.move_king_child(new_x, new_y, self.circle_nw)
        # self.click = False
        self.kill_king_circles()
        self.reset_king_blocks()

    def __str__(self):
        if self.color == black:
            color = "Black"
        else:
            color = "White"
        return color + " King"


# functions
def check_board_position(p):
    for i in range(8):
        for j in range(8):
            if p.x in range(chess_board[i][j].x, chess_board[i][j].x + 80) and p.y in range(chess_board[i][j].y, chess_board[i][j].y + 80):
                print("p.x, p.y = " + str(p.x) + ", " + str(p.y))
                print("chess_board[" + str(i) + "][" + str(j) + "]" + " = " + str(chess_board[i][j]))

def drawLightSquares():
    x_square = 0
    y_square = 0
    og_x = x_square
    width = 80
    height = 80
    for i in range(0, 8):
        if i % 2 == 0:
            x_square = og_x
        else:
            x_square = og_x + 80
        for j in range(0, 8):
            pygame.draw.rect(screen, light, [x_square, y_square, width, height])
            x_square += 160
        y_square += 80

def make_piece(range_num, class_type, piece_img1, piece_img2, x1, x2, yb, yw):
    if range_num == 8:
        for i in range(range_num):
            black_pawn_made = class_type(piece_img1, x1, yb, black)
            black_pieces.append(black_pawn_made)
            all_pieces.append(black_pawn_made)
            black_sprites.add(black_pawn_made)
            sprites.add(black_pawn_made)

            white_pawn_made = class_type(piece_img2, x1, yw, white)
            white_pieces.append(white_pawn_made)
            all_pieces.append(white_pawn_made)
            white_sprites.add(white_pawn_made)
            sprites.add(white_pawn_made)

            x1 += 80

    else:
        for i in range(range_num):
            black_piece_made = class_type(piece_img1, x1, y_black, black)
            black_pieces.append(black_piece_made)
            all_pieces.append(black_piece_made)
            black_sprites.add(black_piece_made)
            sprites.add(black_piece_made)

            white_piece_made = class_type(piece_img2, x1, y_white, white)
            white_pieces.append(white_piece_made)
            all_pieces.append(white_piece_made)
            white_sprites.add(white_piece_made)
            sprites.add(white_piece_made)

            x1 = x2

def make_royal(class_type, piece_img1, piece_img2, x):
    black_royal_piece = class_type(piece_img1, x, y_black, black)
    black_pieces.append(black_royal_piece)
    all_pieces.append(black_royal_piece)
    black_sprites.add(black_royal_piece)
    sprites.add(black_royal_piece)

    white_royal_piece = class_type(piece_img2, x, y_white, white)
    white_pieces.append(white_royal_piece)
    all_pieces.append(white_royal_piece)
    white_sprites.add(white_royal_piece)
    sprites.add(white_royal_piece)

# make pieces
pawn_range_num = 8
other_range_num = 2
# pawns
make_piece(pawn_range_num, Pawn, blackpawn_img, whitepawn_img, x_pawns, 0, y_blackpawns, y_whitepawns)
# rooks
make_piece(other_range_num, Rook, blackrook_img, whiterook_img, x_rook1, x_rook2, y_black, y_white)
# knights
make_piece(other_range_num, Knight, blackknight_img, whiteknight_img, x_knight1, x_knight2, y_black, y_white)
# bishops
make_piece(other_range_num, Bishop, blackbishop_img, whitebishop_img, x_bishop1, x_bishop2, y_black, y_white)
# queens
make_royal(Queen, blackqueen_img, whitequeen_img, x_queen)
# kings
make_royal(King, blackking_img, whiteking_img, x_king)

# game play
playing = True

while playing:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
            playing = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            left_click = pygame.mouse.get_pos()
            left_x = left_click[0]
            left_y = left_click[1]

            right_click = pygame.mouse.get_pos()
            right_x = right_click[0]
            right_y = right_click[1]

            if event.button == 1:
                if black_turn:
                    for p in black_pieces:
                        p.check_for_click(left_x, left_y)
                        if p.click:
                            print("left button clicked, " + "type is " + p.__str__())
                            p.find_board_position()
                            p.possible_moves()
                if white_turn:
                    for p in white_pieces:
                        p.check_for_click(left_x, left_y)
                        if p.click:
                            print("left button clicked, " + "type is " + p.__str__())
                            p.find_board_position()
                            p.possible_moves()

            if event.button == 3:
                if black_turn:
                    for p in black_pieces:
                        old_x, old_y = p.x, p.y
                        p.move(right_x, right_y)
                        p.check_for_collision()
                        if p.click:
                            print("old x, old y = " + str(old_x) + ", " + str(old_y))
                            print("new x, new y = " + str(p.x) + ", " + str(p.y))
                        p.click = False
                        if old_x != p.x or old_y != p.y:
                            amt_of_turns += 1
                if white_turn:
                    for p in white_pieces:
                        old_x, old_y = p.x, p.y
                        p.move(right_x, right_y)
                        p.check_for_collision()
                        if p.click:
                            print("old x, old y = " + str(old_x) + ", " + str(old_y))
                            print("new x, new y = " + str(p.x) + ", " + str(p.y))
                        p.click = False
                        if old_x != p.x or old_y != p.y:
                            amt_of_turns += 1

                if amt_of_turns % 2 == 0:
                    black_turn = False
                    white_turn = True
                else:
                    black_turn = True
                    white_turn = False

    screen.fill(dark)
    drawLightSquares()

    sprites.draw(screen)
    sprites.update()
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
quit()
