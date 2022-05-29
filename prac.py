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
black_pawns = []
white_pawns = []
black_rooks = []
white_rooks = []
black_knights = []
white_knights = []
black_bishops = []
white_bishops = []

# x and y variables for pieces
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

# class for circle
class Circle(pygame.sprite.Sprite):

    def __init__(self, x=1000, y=1000):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = pygame.image.load(os.path.join(img_folder, redcircle_img))
        self.image = pygame.transform.scale(self.image, (15, 15))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

# class for pieces
class Piece(pygame.sprite.Sprite):

    def __init__(self, piece_img, x, y, color):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.color = color
        self.image = pygame.image.load(os.path.join(img_folder, piece_img))
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.click = False

    def check_for_click(self, leftx, lefty):
        if self.x in range(leftx - 30, leftx + 30) and self.y in range(lefty - 30, lefty + 30):
            self.click = True



class Pawn(Piece):

    def __init__(self, piece_img, x, y, color):
        super().__init__(piece_img, x, y, color)
        self.circle1 = Circle()
        self.circle2 = Circle()

    def possible_moves(self):
        if self.click:
            if self.color == black:
                if self.y == y_blackpawns:
                    print("black pawn in starting position")
                    self.circle1.rect.center = (self.x, self.y + 80)
                    self.circle2.rect.center = (self.x, self.y + 160)
                    sprites.add(self.circle1)
                    sprites.add(self.circle2)
                else:
                    print("black pawn not in starting position")
                    self.circle1.rect.center = (self.x, self.y + 80)
                    sprites.add(self.circle1)
            if self.color == white:
                if self.y == y_whitepawns:
                    print("white pawn in starting position")
                    self.circle1.rect.center = (self.x, self.y - 80)
                    self.circle2.rect.center = (self.x, self.y - 160)
                    sprites.add(self.circle1)
                    sprites.add(self.circle2)
                else:
                    print("white pawn not in starting position")
                    self.circle1.rect.center = (self.x, self.y - 80)
                    sprites.add(self.circle1)

    def move(self, new_x, new_y):
        if self.click:
            if self.color == black:
                if self.y == y_blackpawns:
                    self.rect.center = (new_x, new_y)


class Rook(Piece):

    def __init__(self, piece_img, x, y, color):
        super().__init__(piece_img, x, y, color)

class Knight(Piece):

    def __init__(self, piece_img, x, y, color):
        super().__init__(piece_img, x, y, color)

class Bishop(Piece):

    def __init__(self, piece_img, x, y, color):
        super().__init__(piece_img, x, y, color)

class Queen(Piece):

    def __init__(self, piece_img, x, y, color):
        super().__init__(piece_img, x, y, color)

class King(Piece):

    def __init__(self, piece_img, x, y, color):
        super().__init__(piece_img, x, y, color)



# functions
def check_board_position(p):
    for i in range(8):
        for j in range(8):
            if p.x in range(chess_board[i][j].x, chess_board[i][j].x + 80) and p.y in range(chess_board[i][j].y, chess_board[i][j].y + 80):
                print("p.x, p.y = " + str(p.x) + ", " + str(p.y))
                print("chess_board[" + str(i) + "][" + str(j) + "]" + " = " + str(chess_board[i][j]))

def make_pieces(range_num, class_type, specific_list1, specific_list2, piece_img1, piece_img2, x1, x2, yb, yw):
    if range_num == 8:
        for i in range(range_num):
            black_pawn_made = class_type(piece_img1, x1, yb, black)
            specific_list1.append(black_pawn_made)
            black_pieces.append(black_pawn_made)
            all_pieces.append(black_pawn_made)
            black_sprites.add(black_pawn_made)
            sprites.add(black_pawn_made)

            white_pawn_made = class_type(piece_img2, x1, yw, white)
            specific_list2.append(white_pawn_made)
            white_pieces.append(white_pawn_made)
            all_pieces.append(white_pawn_made)
            white_sprites.add(white_pawn_made)
            sprites.add(white_pawn_made)

            x1 += 80

    else:
        for i in range(range_num):
            black_piece_made = class_type(piece_img1, x1, y_black, black)
            specific_list1.append(black_piece_made)
            black_pieces.append(black_piece_made)
            all_pieces.append(black_piece_made)
            black_sprites.add(black_piece_made)
            sprites.add(black_piece_made)

            white_piece_made = class_type(piece_img2, x1, y_white, white)
            specific_list1.append(white_piece_made)
            white_pieces.append(white_piece_made)
            all_pieces.append(white_piece_made)
            white_sprites.add(white_piece_made)
            sprites.add(white_piece_made)

            x1 = x2

def make_royals(class_type, piece_img1, piece_img2, x):
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
make_pieces(pawn_range_num, Pawn, black_pawns, white_pawns, blackpawn_img, whitepawn_img, x_pawns, 0, y_blackpawns, y_whitepawns)
# rooks
make_pieces(other_range_num, Rook, black_rooks, white_rooks, blackrook_img, whiterook_img, x_rook1, x_rook2, y_black, y_white)
# knights
make_pieces(other_range_num, Knight, black_knights, white_knights, blackknight_img, whiteknight_img, x_knight1, x_knight2, y_black, y_white)
# bishops
make_pieces(other_range_num, Bishop, black_bishops, white_bishops, blackbishop_img, whitebishop_img, x_bishop1, x_bishop2, y_black, y_white)
# queens
make_royals(Queen, blackqueen_img, whitequeen_img, x_queen)
# kings
make_royals(King, blackking_img, whiteking_img, x_king)


# gameplay

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
                for p in all_pieces:
                    p.check_for_click(left_x, left_y)
                    if p.click:
                        print("left button clicked")
                        check_board_position(p)
                        p.possible_moves()

            if event.button == 3:
                for p in black_pawns:
                    p.move(right_x, right_y)



    sprites.draw(screen)
    sprites.update()
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
quit()

