import pygame
import objects
from sys import exit

pygame.init()

height = 600
width = 1000

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess")

start = True
run = False
reset = False

# images
logo = pygame.image.load("logo.png")
logo = pygame.transform.scale(logo, (400,400))
start = pygame.image.load("start.png")
white_king = pygame.image.load("pieces/white_king.png")
black_king = pygame.image.load("pieces/black_king.png")
white_queen = pygame.image.load("pieces/white_queen.png")
black_queen = pygame.image.load("pieces/black_queen.png")
white_rook = pygame.image.load("pieces/white_rook.png")
black_rook = pygame.image.load("pieces/black_rook.png")
white_bishop = pygame.image.load("pieces/white_bishop.png")
black_bishop = pygame.image.load("pieces/black_bishop.png")
white_knight = pygame.image.load("pieces/white_knight.png")
black_knight = pygame.image.load("pieces/black_knight.png")
white_pawn = pygame.image.load("pieces/white_pawn.png")
black_pawn = pygame.image.load("pieces/black_pawn.png")

whites = [white_king, white_queen, white_bishop, white_knight, white_rook, white_pawn]
blacks = [black_king, black_queen, black_bishop, black_knight, black_rook, black_pawn]

board = [[objects.Rook(0,[0,0], black_rook),objects.Knight(0,[0,1], black_knight),objects.Bishop(0,[0,2], black_bishop),objects.King(0,[0,3], black_king),objects.Queen(0,[0,4], black_queen),objects.Bishop(0,[0,5], black_bishop),objects.Knight(0,[0,6], black_knight),objects.Rook(0,[0,7], black_rook)],[objects.Pawn(0,[1,0], black_pawn),objects.Pawn(0,[1,1], black_pawn),objects.Pawn(0,[1,2], black_pawn),objects.Pawn(0,[1,3], black_pawn),objects.Pawn(0,[1,4], black_pawn),objects.Pawn(0,[1,5], black_pawn),objects.Pawn(0,[1,6], black_pawn),objects.Pawn(0,[1,7], black_pawn)],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[objects.Pawn(1,[6,0], white_pawn),objects.Pawn(1,[6,1], white_pawn),objects.Pawn(1,[6,2], white_pawn),objects.Pawn(1,[6,3], white_pawn),objects.Pawn(1,[6,4], white_pawn),objects.Pawn(1,[6,5], white_pawn),objects.Pawn(1,[6,6], white_pawn),objects.Pawn(1,[6,7], white_pawn)],[objects.Rook(1,[7,0], white_rook),objects.Knight(1,[7,1], white_knight),objects.Bishop(1,[7,2], white_bishop),objects.King(1,[7,3], white_king),objects.Queen(1,[7,4], white_queen),objects.Bishop(1,[7,5], white_bishop),objects.Knight(1,[7,6], white_knight),objects.Rook(1,[7,7], white_rook)]]

change_position = False

def draw(obj, surface):
	surface.blit(obj.image, (obj.pos[1]*75, obj.pos[0]*75))

def showValidMoves(obj, board, surface):
		valid_moves = obj.validMoves(board)
		for i in  valid_moves:
			pygame.draw.circle(surface, 'grey', (i[1]*75 + 75/2, i[0]*75 + 75/2), 75/2)

# main game loop
while True:
	if start:
		mouse = pygame.Rect(pygame.mouse.get_pos(), (1, 1))
		startButton = start.get_rect()
		startButton.left = 325
		startButton.top = 400
		if mouse.colliderect(startButton) and pygame.mouse.get_pressed()[0]:
			start = False
			run = True
	if run:
		mos_pos = pygame.mouse.get_pos()
		mos_pos = [mos_pos[1]//75, mos_pos[0]//75]
		for i in range(8):
			for j in range(8):
				if type(board[i][j]) != int and board[i][j].isClicked and pygame.mouse.get_pressed()[0]:
					board[i][j].move(mos_pos, board)
		mos_pos = pygame.mouse.get_pos()
		for i in range(8):
			for j in range(8):
				if type(board[i][j]) == objects.King:
					print(board[i][j].color, board[i][j].isCheck(board))
				if board[i][j] != 0:
					 if pygame.mouse.get_pressed()[0] and i == mos_pos[1]//75 and j == mos_pos[0]//75:
					 	board[i][j].isClicked = True
					 	for m in range(8):
					 		for n in range(8):
					 			if (m != i or n != j) and type(board[m][n]) != int and board[m][n].isClicked:
					 				board[m][n].isClicked = False

		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					for i in range(8):
						for j in range(8):
							if board[i][j] != 0:
								board[i][j].isClicked = False
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()

	# event manager
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

	pygame.Surface.fill(screen, 'white')
	if start:
		screen.blit(logo, (300,0))
		screen.blit(start, (325,400))
	elif run:
		for i in range(8):
			for j in range(8):
				if (i+j)%2:
					pygame.draw.rect(screen, (0,100,0), pygame.Rect(75*i,75*j,75,75))

		for i in range(8):
			for j in range(8):
					if(board[i][j] != 0 and board[i][j].isClicked):
						board[i][j].showMoves(screen, board)
		for i in range(8):
			for j in range(8):
				if board[i][j] != 0:
					board[i][j].draw(screen)

		

	pygame.display.update()