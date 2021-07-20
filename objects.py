import pygame
pygame.init()

def index(elements, element):
	for i in range(len(elements)):
		if elements[i] == element:
			return i
	return len(elements)

class Piece:
	def __init__(self, color, pos, image):
		self.color = color
		self.pos = pos
		self.image = image
		self.isClicked = False
		self.isMoved = False
	def showMoves(self, surface, board):
		valid_moves = self.validMoves(board)
		for move in valid_moves:
			pygame.draw.circle(surface, 'grey', (move[1]*75 + 75/2, move[0]*75 + 75/2), 75/2)
	def move(self, pos, board):
		for m in self.validMoves(board):
			if m == pos:
				board[self.pos[0]][self.pos[1]] = 0
				board[pos[0]][pos[1]] = self
				self.pos = pos
				self.isMoved = True
				self.isClicked = False
				return
	def draw(self, surface):
		surface.blit(self.image, (self.pos[1]*75, self.pos[0]*75))
	def king(self, board):
		for i in range(8):
			for j in range(8):
				if type(board[i][j]) == King and board[i][j].color == self.color:
					return board[i][j]
		return King(self.color, [9,9], self.image)
	def removeChecks(self, valid_moves, board):
		for i in range(len(valid_moves)):
			board[self.pos[0]][self.pos[1]] = 0
			x = board[valid_moves[i][0]][valid_moves[i][1]] 
			board[valid_moves[i][0]][valid_moves[i][1]] = self
			if self.king(board).isCheck(board):
				board[valid_moves[i][0]][valid_moves[i][1]] = x
				valid_moves = valid_moves[:i] + valid_moves[i+1:]
			else:
				board[valid_moves[i][0]][valid_moves[i][1]] = x
			board[self.pos[0]][self.pos[1]] = self


class Pawn(Piece):
	def validMoves(self, board):
		moves = []
		if self.color:
			if self.pos[0] > 0:
				if(board[self.pos[0]-1][self.pos[1]] == 0):
					moves += [[self.pos[0]-1,self.pos[1]]]
				if not self.isMoved and (board[self.pos[0]-2][self.pos[1]] == 0 and board[self.pos[0]-1][self.pos[1]] == 0):
					moves += [[self.pos[0]-2, self.pos[1]]]
				if self.pos[1] > 0 and (board[self.pos[0]-1][self.pos[1]-1] != 0 and board[self.pos[0]-1][self.pos[1]-1].color == (not self.color)):
					moves += [[self.pos[0]-1, self.pos[1]-1]]
				if self.pos[1] < 7 and (board[self.pos[0]-1][self.pos[1]+1] != 0 and board[self.pos[0]-1][self.pos[1]+1].color == (not self.color)):
					moves += [[self.pos[0]-1, self.pos[1]+1]]
		else:
			if self.pos[0] < 7:
				if(board[self.pos[0]+1][self.pos[1]] == 0):
					moves += [[self.pos[0]+1,self.pos[1]]]
				if not self.isMoved and (board[self.pos[0]+2][self.pos[1]] == 0 and board[self.pos[0]+1][self.pos[1]] == 0):
					moves += [[self.pos[0]+2, self.pos[1]]]
				if self.pos[1] > 0 and (board[self.pos[0]+1][self.pos[1]-1] != 0 and board[self.pos[0]+1][self.pos[1]-1].color == (not self.color)):
					moves += [[self.pos[0]+1, self.pos[1]-1]]
				if self.pos[1] < 7 and (board[self.pos[0]+1][self.pos[1]+1] != 0 and board[self.pos[0]+1][self.pos[1]+1].color == (not self.color)):
					moves += [[self.pos[0]+1, self.pos[1]+1]]
		# self.removeChecks(moves, board)
		return moves

class Rook(Piece):
	def validMoves(self, board):
		moves = []
		for i in range(self.pos[0]+1,8):
			if board[i][self.pos[1]] != 0 and board[i][self.pos[1]].color == self.color:
				break
			moves += [[i, self.pos[1]]]
		for i in range(self.pos[0]-1,-1,-1):
			if board[i][self.pos[1]] != 0 and board[i][self.pos[1]].color == self.color:
				break
			moves += [[i, self.pos[1]]]
		for j in range(self.pos[1]+1,8):
			if board[self.pos[0]][j] != 0  and board[self.pos[0]][j].color == self.color:
				break
			moves += [[self.pos[0], j]]
		for j in range(self.pos[1]-1,-1,-1):
			if board[self.pos[0]][j] != 0  and board[self.pos[0]][j].color == self.color:
				break
			moves += [[self.pos[0], j]]
		# self.removeChecks(moves, board)
		return moves

class Knight(Piece):
	def validMoves(self, board):
		moves = []
		for i in [-1,+1]:
			for j in [-2,+2]:
				if 0 <= self.pos[0]+i < 8 and 0 <= self.pos[1]+j < 8 and (board[self.pos[0]+i][self.pos[1]+j] ==0  or board[self.pos[0]+i][self.pos[1]+j].color != self.color):
					moves += [[self.pos[0]+i, self.pos[1]+j]]
				if 0 <= self.pos[0]+j < 8 and 0 <= self.pos[1]+i < 8 and (board[self.pos[0]+j][self.pos[1]+i] ==0  or board[self.pos[0]+j][self.pos[1]+i].color != self.color):
					moves += [[self.pos[0]+j, self.pos[1]+i]]
		# self.removeChecks(moves, board)
		return moves

class Bishop(Piece):
	def validMoves(self, board):
		moves = []
		for i in range(1,8):
			if not (0 <= self.pos[0]+i < 8 and 0 <= self.pos[1]+i < 8 and (board[self.pos[0]+i][self.pos[1]+i] == 0 or board[self.pos[0]+i][self.pos[1]+i].color != self.color)):
				break
			moves += [[self.pos[0]+i,self.pos[1]+i]]
		for i in range(1,8):
			if not (0 <= self.pos[0]-i < 8 and 0 <= self.pos[1]+i < 8 and (board[self.pos[0]-i][self.pos[1]+i] == 0 or board[self.pos[0]-i][self.pos[1]+i].color != self.color)):
				break
			moves += [[self.pos[0]-i,self.pos[1]+i]]
		for i in range(1,8):
			if not (0 <= self.pos[0]+i < 8 and 0 <= self.pos[1]-i < 8 and (board[self.pos[0]+i][self.pos[1]-i] == 0 or board[self.pos[0]+i][self.pos[1]-i].color != self.color)):
				break
			moves += [[self.pos[0]+i,self.pos[1]-i]]
		for i in range(1,8):
			if not (0 <= self.pos[0]-i < 8 and 0 <= self.pos[1]-i < 8 and (board[self.pos[0]-i][self.pos[1]-i] == 0 or board[self.pos[0]-i][self.pos[1]-i].color != self.color)):
				break
			moves += [[self.pos[0]-i,self.pos[1]-i]]
		self.removeChecks(moves, board)
		return moves

class Queen(Piece):
	def validMoves(self, board):
		moves = []
		r = Rook(self.color, self.pos, self.image)
		b = Bishop(self.color, self.pos, self.image)

		moves += r.validMoves(board) + b.validMoves(board)
		# self.removeChecks(moves, board)
		return moves


class King(Piece):
	def validMoves(self, board):
		moves = []
		test_king = King(self.color, self.pos, self.image)
		for m in [-1,0,1]:
			for n in [-1,0,1]:
				if 0 <= self.pos[0]+m < 8 and 0 <= self.pos[1]+n < 8 and (m!=self.pos[0] or n!=self.pos[1]):
					if board[self.pos[0]+m][self.pos[1]+n] == 0 or board[self.pos[0]+m][self.pos[1]+n].color != self.color:
						board[self.pos[0]][self.pos[1]] = 0
						test_king = King(self.color, [self.pos[0]+m, self.pos[1]+n], self.image)
						if not test_king.isCheck(board):
							moves += [test_king.pos]
						board[self.pos[0]][self.pos[1]] = self

		return moves

	def isCheck(self, board):
		for i in range(8):
			for j in range(8):
				if board[i][j] !=0 and board[i][j].color != self.color and (self.pos in board[i][j].validMoves(board)):
					print(True)
					return True
		print(False)
		return False