import pygame
from pygame.locals import *
import time
from Heuristic import read_sokoban_map,a_star_sokoban
#General setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 800
surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Sokoban Solver")
running = True
clock = pygame.time.Clock()
FPS = 60

#---------------------
# Setup Colors 
#---------------------
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY_LIGHT = (231, 231, 231)
ORANGE = '#ff631c'
BLUE_LIGHT = (40, 53, 88)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
YELLOW_LIGHT = (255, 255, 51)
BROWN = (210, 105, 30)
PINK = (204, 0, 255)
GREEN_LIGHT = (0, 255, 140)
GREEN = (0, 255, 0)
GREEN_DARK = (0, 255, 0)

#---------------------
# Font Setup
#---------------------
menuFont = pygame.font.SysFont("CopperPlate Gothic", 60, bold = True)  
helpFont = pygame.font.SysFont("Comic Sans MS", 25)      
wordFont = pygame.font.SysFont("CopperPlate Gothic", 25)  
recordFont = pygame.font.SysFont("Comic Sans MS", 17)  
mapFont = pygame.font.SysFont("Comic Sans MS", 20, bold = True)   
levelFont = pygame.font.SysFont("Comic Sans MS", 25, bold = True)  
buttonFont = pygame.font.SysFont("CopperPlate Gothic", 18, bold = True)

#---------------------
# Global Variables
#---------------------
numsRow = 8 
numsCol = 8 

numsUnit = max(numsCol, numsRow)
lengthSquare = int(WINDOW_HEIGHT/numsUnit)

offsetX = lengthSquare * (numsUnit - numsCol)/2 
offsetY = lengthSquare * (numsUnit - numsRow)/2 

map_list = ['MINI COSMOS', 'MICRO COSMOS']
win = 0
map_index = 0
level = 0
mode = 0
step = 1
timeTook = 0
pushed = 0
startTime = 0
stepNode = 0
visualized = 0
moves = []
history = 0
name = ''
actions = []
ptr = -1


#---------------------
# Setup Items 
#---------------------
background = pygame.image.load("Items/background.jpg")
background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_WIDTH))

wall = pygame.image.load('Items/wall.jpg')
wall = pygame.transform.scale(wall, (lengthSquare, lengthSquare))

box = pygame.image.load('Items/box.png')
box = pygame.transform.scale(box, (lengthSquare, lengthSquare))

goal = pygame.image.load('Items/goal.jpg')
goal = pygame.transform.scale(goal, (lengthSquare, lengthSquare))

player_ = pygame.image.load('Items/player.png')
player_ = pygame.transform.scale(player_, (lengthSquare, lengthSquare))

up_arrow = pygame.image.load("Items/up_arrow.png")
up_arrow = pygame.transform.scale(up_arrow, (20, 20))

down_arrow = pygame.image.load("Items/down_arrow.png")
down_arrow = pygame.transform.scale(down_arrow, (20, 20))

undo_button = pygame.image.load("Items/undo.png")
undo_button = pygame.transform.scale(undo_button, (35, 35))

redo_button = pygame.image.load("Items/redo.png")
redo_button = pygame.transform.scale(redo_button, (35, 35))

#---------------------
# Setup Rectangles
#---------------------
mini_rect = Rect(810 + 70, 145, 185, 35)
micro_rect = Rect(810 + 70, 145 + 45, 185, 35)
up_arrow_rect = Rect(810 + 120, 235, 20, 20)
down_arrow_rect = Rect(810 + 120, 255, 20, 20)

manual_rect = Rect(830, 330, 100, 48)
bfs_rect = Rect(830 + 120, 330, 100, 48)
A_rect = Rect(830 + 240, 330, 100, 48)
start_rect = Rect(820 + 86, 400, 185, 40)

restart_rect = Rect(820 + 130, 650, 100, 40)
undo_rect = Rect(820 + 80, 650, 40, 40)
redo_rect = Rect(820 + 240, 650, 40, 40)


#---------------------
# Displays
#---------------------

def display_title():
	menuText = menuFont.render("SOKOBAN", True, ORANGE)
	surface.blit(menuText, [800 + 35, 20])	

def display_background():
	surface.blit(background, [0, 0])

def display_title_map_selection(color = YELLOW):
	title_map_selection = helpFont.render("Map Selection:", True, color)
	surface.blit(title_map_selection, [810, 100])

def display_text_set(color = ORANGE):
	text_set = helpFont.render("Set:", True, color)
	surface.blit(text_set, [810, 145])

def display_minicosmos_button(mini_selected):
	if mini_selected:
		pygame.draw.rect(surface, YELLOW, pygame.Rect(810 + 70 - 1, 145 - 1, 185 + 2, 35 + 2),  0, 6)
	pygame.draw.rect(surface, BLACK, pygame.Rect(810 + 70, 145, 185, 35),  0, 6)
	minicosmos_button = mapFont.render("MINI COSMOS", True, YELLOW)
	surface.blit(minicosmos_button, [810 + 70 + 10 + 4, 145 + 2])

def display_microcosmos_button(mini_selected):
	if not mini_selected:
		pygame.draw.rect(surface, YELLOW, pygame.Rect(810 + 70 - 1, 145 + 45 - 1, 185 + 2, 35 + 2),  0, 6)
	pygame.draw.rect(surface, BLACK, pygame.Rect(810 + 70, 145 + 45, 185, 35),  0, 6)
	microcosmos_button = mapFont.render("MICRO COSMOS", True, YELLOW)
	surface.blit(microcosmos_button, [810 + 70 + 10 - 2, 145 + 45 + 2])

def display_text_level(color = ORANGE):
	text_level = helpFont.render("Level:", True, color)
	surface.blit(text_level, [810, 0 + 235])

# def display_level(color = GRAY_LIGHT):
# 	levelText = levelFont.render(f"{level + 1}", True, color)
# 	if len(str(level) == 1):
# 		surface.blit(levelText, [810 + 105, 235])
# 	else:
# 		surface.blit(levelText, [810 + 105, 235])

def check_one_digit(n):
	if len(str(n)) == 1:
		return True
	return False

def display_level(color = GRAY_LIGHT):
	levelText = levelFont.render(f"{level + 1}", True, color)
	if check_one_digit(level + 1):
		surface.blit(levelText, [810 + 90, 235])
	else:
		surface.blit(levelText, [810 + 80, 235])

def display_up_arrow():
	surface.blit(up_arrow, [810 + 120, 235])

def display_down_arrow():
	surface.blit(down_arrow, [810 + 120, 255])

def display_text_1_40():
	text_1_40 = helpFont.render("(1 - 40)", True, ORANGE)
	surface.blit(text_1_40, [810 + 155, 235])

def display_title_gameplay_selection(color = YELLOW):
	title_gameplay_selection = helpFont.render("Gameplay Selection:", True, color)
	surface.blit(title_gameplay_selection, [810, 290])

def display_manual_button(mode_selected):
	if mode_selected == 1:
		pygame.draw.rect(surface, YELLOW, pygame.Rect(830 - 1, 330 - 1, 100 + 2, 48 + 2),  0, 6)
	pygame.draw.rect(surface, BLACK, pygame.Rect(830, 330, 100, 48),  0, 6)
	text_manual = buttonFont.render("Manually", True, YELLOW)
	surface.blit(text_manual, [834, 342])

def display_bfs_button(mode_selected):
	if mode_selected == 2:
		pygame.draw.rect(surface, YELLOW, pygame.Rect(830 + 120 - 1, 330 - 1, 100 + 2, 48 + 2),  0, 6)
	pygame.draw.rect(surface, BLACK, pygame.Rect(830 + 120, 330, 100, 48),  0, 6)
	text_bfs = buttonFont.render("BFS", True, YELLOW)
	surface.blit(text_bfs, [834 + 120 + 25, 342])

def display_A_button(mode_selected):
	if mode_selected == 3:
		pygame.draw.rect(surface, YELLOW, pygame.Rect(830 + 240 - 1, 330 - 1, 100 + 2, 48 + 2),  0, 6)
	pygame.draw.rect(surface, BLACK, pygame.Rect(830 + 240, 330, 100, 48),  0, 6)
	text_A = buttonFont.render("A*", True, YELLOW)
	surface.blit(text_A, [834 + 240 + 35, 342])

def display_start_button(step):
	if step == 1:
		pygame.draw.rect(surface, RED, pygame.Rect(820 + 86, 400, 185, 40),  0, 6)
		start_button = buttonFont.render("START", True, YELLOW)
		surface.blit(start_button, [820 + 85 + 60, 410])
	else:
		pygame.draw.rect(surface, GRAY_LIGHT, pygame.Rect(820 + 86, 400, 185, 40),  0, 6)
		start_button = buttonFont.render("START", True, BLACK)
		surface.blit(start_button, [820 + 85 + 60, 410])

def display_step_1():
	display_title_map_selection(RED if step == 2 else GREEN_DARK)
	display_text_set()
	display_minicosmos_button(1 if map_index == 0 else 0)
	display_microcosmos_button(1 if map_index == 0 else 0)
	display_text_level()
	display_level()
	display_up_arrow()
	display_down_arrow()
	display_text_1_40()
	display_title_gameplay_selection(RED if step == 2 else GREEN_DARK)
	display_manual_button(mode)
	display_bfs_button(mode)
	display_A_button(mode)
	display_start_button(step)

def display_title_records(color = YELLOW):
	title_records = helpFont.render("Records:", True, color)
	surface.blit(title_records, [810, 450])

def display_text_status(color = ORANGE):
	text_status = helpFont.render("Status:", True, color)
	surface.blit(text_status, [820, 490])

def display_text_time(color = ORANGE):
	text_time = helpFont.render("Time:", True, color)
	surface.blit(text_time, [820, 530])

def display_text_step(color = ORANGE):
	text_step = helpFont.render("Step:", True, color)
	surface.blit(text_step, [820, 570])

def display_text_pushed(color = ORANGE):
	text_pushed = helpFont.render("Pushed:", True, color)
	surface.blit(text_pushed, [820, 610])

def display_button_restart():
	pygame.draw.rect(surface, RED, pygame.Rect(820 + 130, 650, 100, 40),  0, 6)
	button_restart = buttonFont.render("RESTART", True, BLACK)
	surface.blit(button_restart, [820 + 132, 660])

def display_button_undo():
	pygame.draw.rect(surface, RED, pygame.Rect(820 + 80, 650, 40, 40),  0, 6)
	surface.blit(undo_button, [820 + 82, 652])

def display_button_redo():
	pygame.draw.rect(surface, RED, pygame.Rect(820 + 240, 650, 40, 40),  0, 6)
	surface.blit(redo_button, [820 + 242, 652])

def display_content_step_2():
	status_str = ""
	if win == -1:
		status_str = ""
		status_col = YELLOW
	if win == 0:
		status_str = "Solving . . ."
		status_col = (255,255,51)
	elif win == 2:
		status_str = "No solution"
		status_col = RED
	elif win == 1:
		status_str = "Win !!@@!!"
		status_col = GREEN_DARK

	statusText = wordFont.render(f"{status_str}", True, status_col)
	surface.blit(statusText, [800 + 127, 495])

	if not (mode >= 2 and win == 0):
		timeText = helpFont.render("{:0.6f} s".format(timeTook), True, GREEN_LIGHT)
		stepText = helpFont.render(f"{stepNode}", True, GREEN_LIGHT)
		pushedText = helpFont.render(f"{pushed}", True, GREEN_LIGHT)

		surface.blit(timeText, [800 + 110, 530])
		surface.blit(stepText, [800 + 135, 570])
		surface.blit(pushedText, [800 + 135, 610])

def display_step_2():
	display_title_records(RED if step == 3 else GREEN_DARK)
	display_text_status()
	display_text_time()
	display_text_step()
	display_text_pushed()
	display_button_restart()
	display_button_undo()
	display_button_redo()
	display_content_step_2()


def draw_menu():
	pygame.draw.rect(surface, BLUE_LIGHT, [800, 0, 1050, 800])
	display_title()
	if step == 1:
		display_step_1()
	if step == 2:
		display_step_1()
		display_step_2()

def draw_board():
	display_background()
	draw_menu()

	for point in walls:
		surface.blit(wall, [offsetX + lengthSquare * point[0], offsetY + lengthSquare * point[1]])
	
	for point in paths:
		pygame.draw.rect(surface, 'white', [offsetX + lengthSquare * point[0], offsetY + lengthSquare * point[1], lengthSquare, lengthSquare])

	for point in goals:
		surface.blit(goal, [offsetX + lengthSquare * point[0], offsetY + lengthSquare * point[1]])

	point = player
	surface.blit(player_, [offsetX + lengthSquare * point[0], offsetY + lengthSquare * point[1]])

	for point in boxes:
		surface.blit(box, [offsetX + lengthSquare * point[0], offsetY + lengthSquare * point[1]])

	pygame.display.flip()

#-----------------
# Refresh Data
#-----------------
def reset_data():
	global numsCol, numsRow, numsUnit, lengthSquare, offsetX, offsetY, wall, box, goal, player_, walls, goals, boxes, paths, player, name, distanceToGoal, dead_squares, actions, ptr
	
	wall = pygame.image.load('Items/wall.jpg')
	box = pygame.image.load('Items/box.png')
	goal = pygame.image.load('Items/goal.jpg')
	player_ = pygame.image.load('Items/player.png')
	name = "./Testcases/{}/{}.txt".format(map_list[map_index], level+1)
	walls, goals, boxes, paths, player, numsRow, numsCol = set_value(name)
	# distanceToGoal, dead_squares = set_distance()
	actions = []
	ptr = -1

	numsUnit = max(numsCol, numsRow)
	lengthSquare = int(WINDOW_HEIGHT/numsUnit)

	offsetX = lengthSquare * (numsUnit - numsRow)/2 
	offsetY = lengthSquare * (numsUnit - numsCol)/2 

	wall = pygame.transform.scale(wall, (lengthSquare, lengthSquare))
	box = pygame.transform.scale(box, (lengthSquare, lengthSquare))
	goal = pygame.transform.scale(goal, (lengthSquare, lengthSquare))
	player_ = pygame.transform.scale(player_, (lengthSquare, lengthSquare))

def init_data():
	global move, win, step, timeTook, pushed, startTime, stepNode, map_index, level, board, numsRow, numsCol, numsUnit, lengthSquare, offsetX, offsetY, visualized, actions
	
	mode = 0
	win = 0
	step = 1
	timeTook = 0
	pushed = 0
	startTime = 0
	stepNode = 0
	visualized = 0
	actions = []
	reset_data()

#------------------------
# Setting Data Structures and Functionalities
#------------------------
class Direction:
	def __init__(self, vector, char):
		self.vector = vector
		self.char = char

	def get_char(self):
		return self.char

# We set the coordinate from top-left corner and x-axis and y-axis as default
L = Direction((-1, 0), 'L')
R = Direction((1, 0), 'R')
U = Direction((0, -1), 'U')
D = Direction((0, 1), 'D')
directions = [U, L, D, R] # clock-wise

#$$ Rule for moving in SOKOBAN map, the rules below will apply for 4 directions: UP, DOWN, LEFT, RIGHT
# Rule 1: If the forward cell is empty, we literally can move
# Rule 2: If the forward cell has a wall, we can not move
# Rule 3: If the forward cell has a box:
	# Rule 3.1: If the forward of forward cell has a box or a wall, we can not move 
	# Rule 3.2: If the forward of forward cell not contains a box or a wall, we can move forward and push the box forward 

def set_available_moves(player, boxes): 
	# Setup attribute available_moves as a list storing legal moves up to date which is a subset of directions list (<= 4 elements)
	# Available moves <=> Rule 1 + Rule 3.2
	available_moves = []
	for direction in directions:
		if (player[0] + direction.vector[0], player[1] + direction.vector[1]) not in walls:
			# forward cell can be a box or empty
			if (player[0] + direction.vector[0], player[1] + direction.vector[1]) in boxes:
				# forward cell contains a box
				if ((player[0] + 2*direction.vector[0], player[1] + 2*direction.vector[1]) not in walls) and ((player[0] + 2*direction.vector[0], player[1] + 2*direction.vector[1]) not in boxes):
					available_moves.append(direction)
			else:
				# forward cell is empty
				available_moves.append(direction)
	return available_moves

# Move the player with direction but the argument make sure direction in the available_moves 
def move(player, boxes, direction):	
	temp = (player[0] + direction.vector[0], player[1] + direction.vector[1])
	is_pushed = 0
	res = True
	boxes = set(boxes)
	if temp in boxes:
		is_pushed = 1
		boxes.remove(temp)
		boxes.add((player[0] + 2*direction.vector[0], player[1] + 2*direction.vector[1]))
	
	boxes = tuple(boxes) 
	player = temp
	return res, is_pushed, player, boxes

def is_win(goals, boxes):
	return goals.issubset(boxes)

def set_value(filename):
	walls = set() # set of Point()
	goals = set()
	boxes = []
	paths = set()
	player = None
	x = 0
	y = 0
	with open(filename, 'r') as f:
		read_data = f.read()
		lines = read_data.split('\n')	
		for line in lines:
			x = 0
			for char in line:
				if char == '#': # Wall
					walls.add((x,y))
				elif char == 'x': # Box
					boxes.append((x,y))
					paths.add((x,y))
				elif char == '?': # Goal
					goals.add((x,y))
					paths.add((x,y))
				elif char == '@': # Player
					player = (x,y)
					paths.add((x,y))
				elif char == '-': # Player and Goal
					goals.add((x,y))
					player = (x,y)
					paths.add((x,y))
				elif char == '+': # Box and Goal
					goals.add((x,y))
					boxes.append((x,y))
					paths.add((x,y))
				elif char == '.': # Path - avaiable move
					paths.add((x,y))
				x += 1
			y += 1
	return walls, goals, tuple(boxes), paths, player, x, y

#-----------------
# Run Program
#-----------------
if __name__ == '__main__':
	name = "./Testcases/{}/{}.txt".format(map_list[0],1)
	walls, goals, boxes, paths, player, _, _ = set_value(name)
	
	while running:
		clock.tick(FPS)

		if is_win(goals, boxes) == True and mode == 1:
			win = 1

		if step == 2 and win == 0 and mode == 1:
			timeTook = time.time() - startTime
		if mode == 3 and step == 2 and win == 0 and visualized == 0:
			grid, player1, boxes1, goals1 = read_sokoban_map(name)
			start_time = time.time()
			path = a_star_sokoban(grid, player1, boxes1, goals1)
			timeTook = time.time() - start_time

			if path:
				actions = []
				px, py = player
				current_boxes = set(boxes)
				for move_char in path:
					dir_map = {'U': U, 'D': D, 'L': L, 'R': R}
					direction = dir_map[move_char]
					_, is_pushed, (px, py), current_boxes = move((px, py), current_boxes, direction)
					actions.append((direction, is_pushed))
				visualized = 1
				ptr = -1
			else:
				win = 2

		if visualized == 1 and step == 2 and win == 0:
			if ptr + 1 < len(actions):
				ptr += 1
				direction, is_pushed = actions[ptr]
				_, pushed_inc, player, boxes = move(player, boxes, direction)
				pushed += pushed_inc
				stepNode += 1
				
				draw_board()            # vẽ lại bản đồ sau mỗi bước
				pygame.display.update() # cập nhật màn hình
				pygame.time.delay(150)  # dừng 100ms
			else:
				win = 1

		for event in pygame.event.get():
			keys_pressed = pygame.key.get_pressed()
			if event.type == pygame.QUIT or keys_pressed[pygame.K_q]:
				pygame.quit()


			if event.type == pygame.KEYDOWN:
				if step == 2:
					if win == 0:
						if event.key == pygame.K_w or event.key == pygame.K_UP:
							if U in set_available_moves(player, boxes):
								if ptr + 1 < len(actions):
									actions = actions[0:(ptr+1)]
								(_, is_pushed, player, boxes) = move(player, boxes, U)
								stepNode += 1
								pushed += is_pushed
								ptr += 1
								actions.append((U, is_pushed))
						elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
							if D in set_available_moves(player, boxes):
								if ptr + 1 < len(actions):
									actions = actions[0:(ptr+1)]
								(_, is_pushed, player, boxes) = move(player, boxes, D)
								stepNode += 1
								pushed += is_pushed
								ptr += 1
								actions.append((D, is_pushed))
						elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
							if L in set_available_moves(player, boxes):
								if ptr + 1 < len(actions):
									actions = actions[0:(ptr+1)]
								(_, is_pushed, player, boxes) = move(player, boxes, L)
								stepNode += 1
								pushed += is_pushed
								ptr += 1
								actions.append((L, is_pushed))
						elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
							if R in set_available_moves(player, boxes):
								if ptr + 1 < len(actions):
									actions = actions[0:(ptr+1)]
								(_, is_pushed, player, boxes) = move(player, boxes, R)
								stepNode += 1
								pushed += is_pushed
								ptr += 1
								actions.append((R, is_pushed))

			if event.type == pygame.MOUSEBUTTONDOWN:
				x, y = event.pos

				if step == 1:
					if up_arrow_rect.collidepoint(x, y):
						level = (level + 1)%40
						reset_data()
					if down_arrow_rect.collidepoint(x,y):
						level = (level+39)%40
						reset_data()
					if mini_rect.collidepoint(x,y):
						map_index = 0
						reset_data()
					if micro_rect.collidepoint(x,y):
						map_index = 1
						reset_data()
					
					if manual_rect.collidepoint(x,y):
						mode = 1
						# startTime = time.time()
					if bfs_rect.collidepoint(x,y): 
						mode = 2
						continue
					if A_rect.collidepoint(x,y):
						mode = 3
						continue
					if start_rect.collidepoint(x,y):
						if mode != 0:
							step = 2
							startTime = time.time()
				if step == 2:
					if restart_rect.collidepoint(x,y):
						init_data()
						step = 1
					if mode == 1:
						pass
					if mode == 2:
						pass
					if mode == 3:
						pass

				# if step == 3:
				# 	if mode == 1:
				# 		if restart_rect.collidepoint(x,y):
				# 			init_data()
				# 			step = 1
				# 		if undo_rect.collidepoint(x,y):
				# 			undo()
				# 		if redo_rect.collidepoint(x,y):
				# 			redo()
				# 	if mode == 2:
				# 		#Bfs
				# 		if restart_rect.collidepoint(x,y):
				# 			init_data()
				# 			step = 1
				# 		if win == 1:
				# 			if visualized == 0:
				# 				if visualize_rect.collidepoint(x,y):
				# 					visualized = 1
				# 			else:
				# 				if undo_rect.collidepoint(x,y):
				# 					undo()
				# 				if redo_rect.collidepoint(x,y):
				# 					redo()
				# 	if mode == 3:
				# 		# A_star
				# 		if restart_rect.collidepoint(x,y):
				# 			init_data()
				# 			step = 1
				# 		if win == 1:
				# 			if visualized == 0:
				# 				if visualize_rect.collidepoint(x,y):
				# 					visualized = 1
				# 			else:
				# 				if undo_rect.collidepoint(x,y):
				# 					undo()
				# 				if redo_rect.collidepoint(x,y):
				# 					redo()
		draw_board()
		pygame.display.update()
	pygame.quit()