# Test how ghosts behave when arriving and leaving the ghost house. Remove and False from line ~253 in Pacman.check_collision()

# Test how ghosts behave when leaving the ghost house after being murdered

# Sort out end print statements to put them as text in the pygame window

# Ghosts leave through the wall, not the door, after having died

import os
import csv
import math
import pygame
import random
import threading
try:
        from colours import *
except ModuleNotFoundError:
        from modules.colours import *
from time import sleep

PARENT_DIRECTORY = os.getcwd().replace("\\", "/")

os.chdir("images")

SCALE = 1  # Has to be 1 or 2 # 1 does not work as intended

global yellow
yellow = [255, 204, 0]

if SCALE == 1:
	OFFSET = 50
elif SCALE == 2:
	OFFSET = 0
SCREENSIZE = ((988-(2*OFFSET))//SCALE, ((1144-(2*OFFSET)))//SCALE)
TILESIZE = (52//SCALE, 52//SCALE)
PACMANSIZE = (40//SCALE, 40//SCALE)
GHOSTSIZE = (40//SCALE, 48//SCALE)
PICKUPSIZE = (4//SCALE, 4//SCALE)
ENERGYPICKUPSIZE = (20//SCALE, 20//SCALE)
GAP = 6//SCALE
GHOSTGAP = (6//SCALE, 2//SCALE)
STARTTEXTSIZE = (SCREENSIZE)
FONTSIZE = 30//SCALE

FPS = 240//SCALE

LIVES = 3

LEFT = "LEFT"
RIGHT = "RIGHT"
DOWN = "DOWN"
UP = "UP"

OPEN = "OPEN"
CLOSED = "CLOSED"

SCATTER = "SCATTER"
CHASE = "CHASE"
FRIGHTENED = "FRIGHTENED"

WALL = "WALL"
FLOOR = "FLOOR"
DOOR = "DOOR"


class Dot(pygame.sprite.Sprite):
	def __init__(self, x, y):
		self.image = pygame.Surface((1, 1))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

	def sprite_at_position(self):
		if pygame.sprite.spritecollide(self, wallgroup, False):
			return WALL
		else:
			return FLOOR
		# elif pygame.sprite.spritecollide(self, floorgroup, False):
		# 	return FLOOR
		# else:
		# 	raise Exception("UNKNOW TILE")


class Pacman(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()

		self.lock = threading.Lock()

		if SCALE == 1:
			self.imor = pygame.image.load("or.png").convert_alpha()
			self.imol = pygame.image.load("ol.png").convert_alpha()
			self.imou = pygame.image.load("ou.png").convert_alpha()
			self.imod = pygame.image.load("od.png").convert_alpha()
			self.imclosed = pygame.image.load("closed.png").convert_alpha()
		elif SCALE == 2:
			self.imor = pygame.image.load("orhalf.png").convert_alpha()
			self.imol = pygame.image.load("olhalf.png").convert_alpha()
			self.imou = pygame.image.load("ouhalf.png").convert_alpha()
			self.imod = pygame.image.load("odhalf.png").convert_alpha()
			self.imclosed = pygame.image.load("closedhalf.png").convert_alpha()
		self.image = pygame.Surface(PACMANSIZE).convert_alpha()
		self.image.fill((0, 0, 0, 0))
		self.image.blit(self.imor, (0, 0))
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = x, y

		self.start_position = (x, y)

		self.tempdir = RIGHT
		self.dir = RIGHT
		self.pic = OPEN
		self.score = 0
		self.ghostscore = 0

		self.lives = LIVES

		self.position = (self.rect.centerx //
						 TILESIZE[0]+1, self.rect.centery//TILESIZE[1]+1)

		self.dying = False
		self.amdead = False
		self.energised = False

		self.counter = -TILESIZE[0]//4

		pacmangroup.add(self)

	def changepic(self):
		pickupcollision = pygame.sprite.spritecollide(self, pickupgroup, False)
		energypickupcollision = pygame.sprite.spritecollide(
			self, energypickupgroup, False)
		if self.pic == CLOSED and pickupcollision:
			for i in pickupcollision:
				i.kill()
				self.increment_score(10)
		if self.pic == CLOSED and energypickupcollision:
			for i in energypickupcollision:
				i.kill()
				self.increment_score(10)
			threading.Thread(target=self.change_state, daemon=True).start()
		if self.dir == LEFT:
			if self.pic == OPEN:
				self.pic = CLOSED
				self.image = pygame.Surface(PACMANSIZE).convert_alpha()
				self.image.fill((0, 0, 0, 0))
				self.image.blit(self.imclosed, (0, 0))
			elif self.pic == CLOSED:
				self.pic = OPEN
				self.chimage(LEFT)
			else:
				raise Exception("\nPacman doesn't have open/closed state\n")
		elif self.dir == RIGHT:
			if self.pic == OPEN:
				self.pic = CLOSED
				self.image = pygame.Surface(PACMANSIZE).convert_alpha()
				self.image.fill((0, 0, 0, 0))
				self.image.blit(self.imclosed, (0, 0))
			elif self.pic == CLOSED:
				self.pic = OPEN
				self.chimage(RIGHT)
			else:
				raise Exception("\nPacman doesn't have open/closed state\n")
		elif self.dir == UP:
			if self.pic == OPEN:
				self.pic = CLOSED
				self.image = pygame.Surface(PACMANSIZE).convert_alpha()
				self.image.fill((0, 0, 0, 0))
				self.image.blit(self.imclosed, (0, 0))
			elif self.pic == CLOSED:
				self.pic = OPEN
				self.chimage(UP)
			else:
				raise Exception("\nPacman doesn't have open/closed state\n")
		elif self.dir == DOWN:
			if self.pic == OPEN:
				self.pic = CLOSED
				self.image = pygame.Surface(PACMANSIZE).convert_alpha()
				self.image.fill((0, 0, 0, 0))
				self.image.blit(self.imclosed, (0, 0))
			elif self.pic == CLOSED:
				self.pic = OPEN
				self.chimage(DOWN)
			else:
				raise Exception("\nPacman doesn't have open/closed state\n")
		else:
			raise Exception("\nPacman direction is not set\n")
		pickupcollision = pygame.sprite.spritecollide(self, pickupgroup, False)
		if self.pic == CLOSED and pickupcollision:
			for i in pickupcollision:
				i.kill()
				self.increment_score(10)
		energypickupcollision = pygame.sprite.spritecollide(
			self, energypickupgroup, False)
		if self.pic == CLOSED and energypickupcollision:
			for i in energypickupcollision:
				i.kill()
				self.increment_score(10)
			self.energised = True
			threading.Thread(target=self.change_state, daemon=True).start()

	def chimage(self, dir):
		if dir in [LEFT, RIGHT, UP, DOWN]:
			self.image = pygame.Surface(PACMANSIZE).convert_alpha()
			self.image.fill((0, 0, 0, 0))
			if dir == LEFT:
				self.image.blit(self.imol, (0, 0))
			elif dir == RIGHT:
				self.image.blit(self.imor, (0, 0))
			elif dir == UP:
				self.image.blit(self.imou, (0, 0))
			elif dir == DOWN:
				self.image.blit(self.imod, (0, 0))
			# self.rect = self.image.get_rect()
		else:
			raise ValueError("Invalid direction passed to Pacman.chimage()")

	def change_direction(self, dir):
		self.tempdir = dir
		if self.direction_check(dir, 7):
			if (self.tempdir == LEFT and self.dir == RIGHT) or (self.tempdir == RIGHT and self.dir == LEFT) or (self.tempdir == UP and self.dir == DOWN) or (self.tempdir == DOWN and self.dir == UP):
				self.dir = self.tempdir
				self.counter = (26//SCALE)-self.counter
				if self.pic == OPEN:
					self.chimage(self.dir)
			if (self.rect.x+OFFSET) % TILESIZE[0] == GAP and (self.rect.y+OFFSET) % TILESIZE[1] == GAP:
				self.dir = dir

	def direction_check(self, dir, distance):
		if SCALE == 2:
			distance = math.ceil(distance/2)
		if dir == UP:
			dotsprite = Dot(self.rect.centerx, self.rect.top-distance)
			tile = dotsprite.sprite_at_position()
			del dotsprite
		elif dir == DOWN:
			dotsprite = Dot(self.rect.centerx, self.rect.bottom+distance)
			tile = dotsprite.sprite_at_position()
			del dotsprite
		elif dir == LEFT:
			dotsprite = Dot(self.rect.left-distance, self.rect.centery)
			tile = dotsprite.sprite_at_position()
			del dotsprite
		elif dir == RIGHT:
			dotsprite = Dot(self.rect.right+distance, self.rect.centery)
			tile = dotsprite.sprite_at_position()
			del dotsprite
		if tile == WALL:
			return False
		else:
			return True

	def check_collision(self):
		ghost_positions = []
		ghost_positions.append(redsprite.return_position())
		ghost_positions.append(bluesprite.return_position())
		ghost_positions.append(orangesprite.return_position())
		ghost_positions.append(pinksprite.return_position())

		if self.get_position() in ghost_positions and False:
			pos = ghost_positions.index(self.get_position())
			if pos == 0:
				return "red"
			elif pos == 1:
				return "blue"
			elif pos == 2:
				return "orange"
			elif pos == 3:
				return "pink"
		else:
			return False

	def reset_position(self):
		self.rect.x, self.rect.y = self.start_position

	def die(self):
		if not self.amdead:
			self.lives -= 1
			self.dying = True
			self.ghostscore = 0
			sleep(1)
			self.reset_position()
			self.chimage(RIGHT)
			self.amdead = True
			bluesprite.reset_position()
			redsprite.reset_position()
			orangesprite.reset_position()
			pinksprite.reset_position()
		else:
			self.amdead = False
			sleep(1)
			self.counter = -TILESIZE[0]//4
			self.dir = RIGHT
			self.tempdir = RIGHT
			self.dying = False

	def change_state(self):
		self.lock.acquire()
		self.energised = True
		sleep(10)
		self.energised = False
		self.lock.release()

	def dead(self):
		return self.amdead

	def update(self):
		collide = self.check_collision()
		if collide and pacmansprite.energised == False:
			threading.Thread(target=self.die, daemon=True).start()
		elif collide and pacmansprite.energised == True:
			if collide == "red":
				redsprite.murder()
			elif collide == "blue":
				bluesprite.murder()
			elif collide == "orange":
				orangesprite.murder()
			elif collide == "pink":
				pinksprite.murder()

		else:
			self.current_position = self.position
			if self.current_position[0] == 20 and self.dir == RIGHT:
				self.rect.x = -TILESIZE[0]
			elif self.current_position[0] == -1 and self.dir == LEFT:
				self.rect.x = TILESIZE[0]*19
			if self.tempdir != self.dir and self.direction_check(self.tempdir, 7):
				if (self.rect.x+OFFSET) % TILESIZE[0] == GAP and (self.rect.y+OFFSET) % TILESIZE[1] == GAP:
					self.dir = self.tempdir
					if self.pic == OPEN:
						self.chimage(self.dir)
			if self.dir == LEFT or self.dir == UP:
				if self.direction_check(self.dir, 7):
					if self.dir == RIGHT:
						self.rect.x += 1
					elif self.dir == LEFT:
						self.rect.x -= 1
					elif self.dir == DOWN:
						self.rect.y += 1
					elif self.dir == UP:
						self.rect.y -= 1
					self.counter += 1
			else:
				if self.direction_check(self.dir, 6):
					if self.dir == RIGHT:
						self.rect.x += 1
					elif self.dir == LEFT:
						self.rect.x -= 1
					elif self.dir == DOWN:
						self.rect.y += 1
					elif self.dir == UP:
						self.rect.y -= 1
					self.counter += 1
			if self.counter == 26//SCALE:
				self.counter = 0
				self.changepic()

		self.position = (self.rect.centerx //
						 TILESIZE[0]+1, self.rect.centery//TILESIZE[1]+1)

	def energised_pacman(self):
		return self.energised

	def is_closed(self):
		if self.pic == CLOSED:
			return True
		else:
			return False

	def increment_score(self, num):
		self.score += num
		self.ghostscore += num

	def return_score(self):
		return self.score

	def return_ghost_score(self):
		return self.ghostscore

	def get_position(self):
		return self.position

	def get_direction(self):
		return self.dir

	def am_dying(self):
		return self.dying

	def return_lives(self):
		return self.lives


class Ghosts(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.Surface(GHOSTSIZE).convert_alpha()
		self.image.set_colorkey((0, 0, 0))

		if SCALE == 1:
			self.frightened_image = pygame.image.load(
				"frightened.png").convert_alpha()
			self.deadimage = pygame.image.load("dead.png").convert_alpha()
		elif SCALE == 2:
			self.frightened_image = pygame.image.load(
				"frightenedhalf.png").convert_alpha()
			self.deadimage = pygame.image.load("deadhalf.png").convert_alpha()

		self.current_image = "NORMAL"

		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		self.start_position = (x, y)

		self.state = None

		self.dead = False
		self.just_dead = False

		self.dir = None

		self.should_change_direction = False

		self.counter = 0

		ghostgroup.add(self)

		self.lock = threading.Lock()

	def change_state(self):
		self.lock.acquire()
		self.state = SCATTER
		self.should_change_direction = True
		self.lock.release()
		sleep(7)
		self.lock.acquire()
		self.state = CHASE
		self.should_change_direction = True
		self.lock.release()
		sleep(20)
		self.lock.acquire()
		self.state = SCATTER
		self.should_change_direction = True
		self.lock.release()
		sleep(7)
		self.lock.acquire()
		self.state = CHASE
		self.should_change_direction = True
		self.lock.release()
		sleep(20)
		self.lock.acquire()
		self.state = SCATTER
		self.should_change_direction = True
		self.lock.release()
		sleep(5)
		self.lock.acquire()
		self.state = CHASE
		self.should_change_direction = True
		self.lock.release()
		sleep(20)
		self.lock.acquire()
		self.state = SCATTER
		self.should_change_direction = True
		self.lock.release()
		sleep(5)
		self.lock.acquire()
		self.state = CHASE
		self.should_change_direction = True
		self.lock.release()

	def update(self):
		if not self.start and self.just_dead == False:
			self.current_position = self.return_position()
			if self.current_position[0] == 20 and self.dir == RIGHT:
				self.rect.x = -TILESIZE[0]
				self.counter = 0-GHOSTGAP[0]
			elif self.current_position[0] == -1 and self.dir == LEFT:
				self.rect.x = TILESIZE[0]*19
				self.counter = 0+GHOSTGAP[0]
			if self.should_change_direction and self.counter == 0:
				self.should_change_direction = False
				if self.dir == LEFT:
					if RIGHT in self.direction_check():
						self.dir = RIGHT
				elif self.dir == RIGHT:
					if LEFT in self.direction_check():
						self.dir = LEFT
				elif self.dir == UP:
					if DOWN in self.direction_check():
						self.dir = DOWN
				elif self.dir == DOWN:
					if UP in self.direction_check():
						self.dir == UP

			self.current_position = self.return_position()

			if self.dir == LEFT:
				self.rect.x -= 1
			elif self.dir == RIGHT:
				self.rect.x += 1
			elif self.dir == UP:
				self.rect.y -= 1
			elif self.dir == DOWN:
				self.rect.y += 1

			self.counter += 1
		else:
			if self.colour == 'PINK' or self.colour == 'RED':
				self.dir = UP
				self.rect.y -= 1
				self.counter += 1
				if self.counter == TILESIZE[0]*2:
					self.start = False
					self.counter = 0
					self.dir = LEFT
					self.just_dead = False
					self.state = redsprite.return_state()
					# self.pinkstatechange = threading.Thread(target=pinksprite.change_state, daemon=True)
					# self.pinkstatechange.start()
			elif self.colour == 'BLUE':
				if pacmansprite.return_ghost_score() == 150:
					self.starttomove = True
				if self.starttomove and self.counter <= TILESIZE[0]:
					self.rect.x += 1
					self.counter += 1
				elif self.starttomove and self.counter <= TILESIZE[0]*3:
					self.rect.y -= 1
					self.counter += 1
				if self.counter == TILESIZE[0]*3:
					self.counter = 0
					self.start = False
					self.dir = LEFT
					self.just_dead = False
					# self.bluestatechange = threading.Thread(target=self.change_state, daemon=True)
					# self.bluestatechange.start()
			elif self.colour == 'ORANGE':
				if pacmansprite.return_ghost_score() == 1250:
					self.starttomove = True
				if self.starttomove and self.counter <= TILESIZE[0]:
					self.rect.x -= 1
					self.counter += 1
				elif self.starttomove and self.counter <= TILESIZE[0]*3:
					self.rect.y -= 1
					self.counter += 1
				if self.counter == TILESIZE[0]*3:
					self.counter = 0
					self.start = False
					self.dir = LEFT
					self.just_dead = False
					# self.orangestatechange = threading.Thread(target=self.change_state, daemon=True)
					# self.orangestatechange.start()

	def reset_position(self):
		self.rect.x, self.rect.y = self.start_position
		self.reset_variables()

	def return_position(self):
		return (self.rect.centerx//TILESIZE[0]+1, self.rect.centery//TILESIZE[1]+1)

	def direction_check(self):

		self.current_position = list(self.return_position())
		self.current_position[0], self.current_position[1] = self.current_position[0] - \
			1, self.current_position[1]-1
		tuple(self.current_position)
		cango = []

		# LEFT
		if self.current_position[0]-1 < 0:
			self.current_position[0] = 19
		if GPS[self.current_position[1]][self.current_position[0]-1] == FLOOR:
			cango.append(LEFT)
		# RIGHT
		if self.current_position[0]+1 > 18:
			self.current_position[0] = -1
		if GPS[self.current_position[1]][self.current_position[0]+1] == FLOOR:
			cango.append(RIGHT)
		# DOWN
		if GPS[self.current_position[1]+1][self.current_position[0]] == FLOOR:
			cango.append(DOWN)
		elif GPS[self.current_position[1]+1][self.current_position[0]] == DOOR and self.dead == True:
			cango.append(DOWN)
		# UP
		if GPS[self.current_position[1]-1][self.current_position[0]] == FLOOR:
			cango.append(UP)

		return cango

	def decide_direction(self, start, target):
		self.possible_directions = self.direction_check()
		if start in [(8, 8), (8, 16), (10, 8), (10, 16)] and SCALE == 1 and self.dead == False:
			self.possible_directions.remove(UP)
		elif start in [(9, 9), (9, 17), (11, 9), (11, 17)] and SCALE == 2 and self.dead == False:
			self.possible_directions.remove(UP)
		if self.dir == LEFT and RIGHT in self.possible_directions:
			self.possible_directions.remove(RIGHT)
		elif self.dir == RIGHT and LEFT in self.possible_directions:
			self.possible_directions.remove(LEFT)
		elif self.dir == UP and DOWN in self.possible_directions:
			self.possible_directions.remove(DOWN)
		elif self.dir == DOWN and UP in self.possible_directions:
			self.possible_directions.remove(UP)
		if len(self.possible_directions) == 1:
			return self.possible_directions[0]
		else:
			self.turn = []
			for i in self.possible_directions:
				if i == LEFT:
					temppos = (start[0]-1, start[1])
					distance = int(
						(((temppos[0]-target[0])**2)+((temppos[1]-target[1])**2))**0.5)
					self.turn.append((distance, LEFT))
				elif i == RIGHT:
					temppos = (start[0]+1, start[1])
					distance = int(
						(((temppos[0]-target[0])**2)+((temppos[1]-target[1])**2))**0.5)
					self.turn.append((distance, RIGHT))
				elif i == DOWN:
					temppos = (start[0], start[1]+1)
					distance = int(
						(((temppos[0]-target[0])**2)+((temppos[1]-target[1])**2))**0.5)
					self.turn.append((distance, DOWN))
				elif i == UP:
					temppos = (start[0], start[1]-1)
					distance = int(
						(((temppos[0]-target[0])**2)+((temppos[1]-target[1])**2))**0.5)
					self.turn.append((distance, UP))
			self.shortest_route = self.turn[0]
			for i in self.turn:
				if i[0] < self.shortest_route[0]:
					self.shortest_route = i
			return self.shortest_route[1]

	def return_state(self):
		return self.state

	def murder(self):
		self.image = pygame.Surface(GHOSTSIZE).convert_alpha()
		self.image.set_colorkey((black))
		self.image.blit(self.deadimage, (0, 0))
		self.dead = True


class BlueGhost(Ghosts):  # Leaves when 15 dots have been eaten
	def __init__(self, x, y):
		super().__init__(x, y)
		if SCALE == 1:
			self.imb = pygame.image.load("blue.png").convert_alpha()
		elif SCALE == 2:
			self.imb = pygame.image.load("bluehalf.png").convert_alpha()
		self.image.blit(self.imb, (0, 0))

		self.colour = 'BLUE'
		self.start = True
		self.starttomove = False

		self.state = SCATTER

	def reset_variables(self):
		self.start = True
		self.starttomove = False
		self.counter = 0

	def move(self):
		if self.counter == TILESIZE[0] and self.start == False and self.dead == True:
			if SCALE == 1:
				self.target = (9, 11)
			elif SCALE == 2:
				self.target = (10, 12)
			if self.return_position() == self.target:
				self.dead = False
				self.just_dead = True
				if self.lock.locked():
					self.lock.release()
				self.image = pygame.Surface(GHOSTSIZE).convert_alpha()
				self.image.set_colorkey(black)
				self.image.blit(self.imb, (0, 0))
			else:
				self.counter = 0
				cango = self.direction_check()
				self.dir = self.decide_direction(self.return_position(), self.target)
		elif pacmansprite.energised_pacman():
			if self.current_image == "NORMAL":
				self.image = pygame.Surface(GHOSTSIZE).convert_alpha()
				self.image.set_colorkey((0, 0, 0))
				self.image.blit(self.frightened_image, (0, 0))
				self.current_image = "FRIGHTENED"
			if self.counter == TILESIZE[0] and self.start == False and self.dead == False:
				self.counter = 0
				cango = self.direction_check()
				if self.dir == UP and UP in cango:
					cango.remove(DOWN)
				elif self.dir == DOWN and DOWN in cango:
					cango.remove(UP)
				elif self.dir == LEFT and LEFT in cango:
					cango.remove(RIGHT)
				elif self.dir == RIGHT and RIGHT in cango:
					cango.remove(LEFT)
				else: pass
					# raise Exception("Blue ghost does not have a direction")
				self.dir = random.choice(cango)
		else:
			if self.current_image == "FRIGHTENED" and self.dead == False:
				self.image = pygame.Surface(GHOSTSIZE).convert_alpha()
				self.image.set_colorkey((0, 0, 0))
				self.image.blit(self.imb, (0, 0))
				self.current_image = "NORMAL"
			self.state = redsprite.return_state()
			if self.state == SCATTER and self.counter == TILESIZE[0] and self.start == False:
				self.counter = 0
				self.target = (19, 23)
				self.dir = self.decide_direction(
					self.return_position(), self.target)
			elif self.state == CHASE and self.counter == TILESIZE[0] and self.start == False:
				self.counter = 0
				redpos = redsprite.return_position()
				pacmandir = pacmansprite.get_direction()
				pacmanpos = pacmansprite.get_position()
				if pacmandir == LEFT:
					midtarget = (pacmanpos[0]-2, pacmanpos[1])
				elif pacmandir == RIGHT:
					midtarget = (pacmanpos[0]+2, pacmanpos[1])
				elif pacmandir == DOWN:
					midtarget = (pacmanpos[0], pacmanpos[1]+2)
				elif pacmandir == UP:
					# Intentional due to original overflow error
					midtarget = (pacmanpos[0]-2, pacmanpos[1]-2)
				dx = midtarget[0]-redpos[0]
				dx *= 2
				dy = midtarget[1]-redpos[1]
				dy *= 2
				self.target = (redpos[0]+dx, redpos[1]+dy)

				self.dir = self.decide_direction(
					self.return_position(), self.target)


class PinkGhost(Ghosts):
	def __init__(self, x, y):
		super().__init__(x, y)

		if SCALE == 1:
			self.imp = pygame.image.load("pink.png").convert_alpha()
		elif SCALE == 2:
			self.imp = pygame.image.load("pinkhalf.png").convert_alpha()

		self.image.blit(self.imp, (0, 0))

		self.dir = UP
		self.state = None

		self.start = True
		self.colour = 'PINK'

	def reset_variables(self):
		self.start = True
		self.counter = 0

	def move(self):
		if self.counter == TILESIZE[0] and self.start == False and self.dead == True:
			if SCALE == 1 or True:
				self.target = (10, 11)
			elif SCALE == 2:
				self.target = (11, 12)
			if self.return_position() == self.target:
				self.dead = False
				self.just_dead = True
				if self.lock.locked():
					self.lock.release()
				self.image = pygame.Surface(GHOSTSIZE).convert_alpha()
				self.image.set_colorkey(black)
				self.image.blit(self.imp, (0, 0))
			else:
				self.counter = 0
				cango = self.direction_check()
				self.dir = self.decide_direction(self.return_position(), self.target)
		elif pacmansprite.energised_pacman():
			if not self.lock.locked():
				self.lock.acquire()
			if self.current_image == "NORMAL":
				self.image = pygame.Surface(GHOSTSIZE).convert_alpha()
				self.image.set_colorkey((0, 0, 0))
				self.image.blit(self.frightened_image, (0, 0))
				self.current_image = "FRIGHTENED"
			if self.counter == TILESIZE[0] and self.start == False and self.dead == False:
				self.counter = 0
				cango = self.direction_check()
				if self.dir == UP and UP in cango:
					cango.remove(DOWN)
				elif self.dir == DOWN and DOWN in cango:
					cango.remove(UP)
				elif self.dir == LEFT and LEFT in cango:
					cango.remove(RIGHT)
				elif self.dir == RIGHT and RIGHT in cango:
					cango.remove(LEFT)
				else: pass
					# raise Exception("Pink ghost does not have a direction")
				self.dir = random.choice(cango)

		else:
			if self.lock.locked():
				self.lock.release()
			if self.current_image == "FRIGHTENED" and self.dead == False:
				self.image = pygame.Surface(GHOSTSIZE).convert_alpha()
				self.image.set_colorkey((0, 0, 0))
				self.image.blit(self.imp, (0, 0))
				self.current_image = "NORMAL"
			self.state = redsprite.return_state()
			if self.state == SCATTER and self.counter == TILESIZE[0] and self.start == False:
				self.counter = 0
				self.target = (2, -2)
				self.dir = self.decide_direction(
					self.return_position(), self.target)
			elif self.state == CHASE and self.counter == TILESIZE[0] and self.start == False:
				self.counter = 0
				pacmanpos = pacmansprite.get_position()
				pacmandir = pacmansprite.get_direction()
				if pacmandir == LEFT:
					self.target = (pacmanpos[0]-4, pacmanpos[1])
				elif pacmandir == RIGHT:
					self.target = (pacmanpos[0]+4, pacmanpos[1])
				elif pacmandir == DOWN:
					self.target = (pacmanpos[0], pacmanpos[1]+4)
				elif pacmandir == UP:
					# Intentional, due to an overflow error orginally
					self.target = (pacmanpos[0]-4, pacmanpos[1]-4)
				self.dir = self.decide_direction(
					self.return_position(), self.target)


class OrangeGhost(Ghosts):  # Leaves when 125 dots have been eaten
	def __init__(self, x, y):
		super().__init__(x, y)

		if SCALE == 1:
			self.imo = pygame.image.load("orange.png").convert_alpha()
		elif SCALE == 2:
			self.imo = pygame.image.load("orangehalf.png").convert_alpha()

		self.image.blit(self.imo, (0, 0))

		self.state = SCATTER
		self.dir = LEFT

		self.colour = 'ORANGE'
		self.start = True
		self.starttomove = False

	def reset_variables(self):
		self.start = True
		self.starttomove = False
		self.counter = 0

	def move(self):
		if self.counter == TILESIZE[0] and self.start == False and self.dead == True:
			if SCALE == 1:
				self.target = (11, 11)
			elif SCALE == 2:
				self.target = (12, 12)
			if self.return_position() == self.target:
				self.dead = False
				self.just_dead = True
				if self.lock.locked():
					self.lock.release()
				self.image = pygame.Surface(GHOSTSIZE).convert_alpha()
				self.image.set_colorkey(black)
				self.image.blit(self.imo, (0, 0))
			else:
				self.counter = 0
				cango = self.direction_check()
				self.dir = self.decide_direction(self.return_position(), self.target)
		elif pacmansprite.energised_pacman():
			if self.current_image == "NORMAL":
				self.image = pygame.Surface(GHOSTSIZE).convert_alpha()
				self.image.set_colorkey((0, 0, 0))
				self.image.blit(self.frightened_image, (0, 0))
				self.current_image = "FRIGHTENED"
			if self.counter == TILESIZE[0] and self.start == False and self.dead == False:
				self.counter = 0
				cango = self.direction_check()
				if self.dir == UP and UP in cango:
					cango.remove(DOWN)
				elif self.dir == DOWN and DOWN in cango:
					cango.remove(UP)
				elif self.dir == LEFT and LEFT in cango:
					cango.remove(RIGHT)
				elif self.dir == RIGHT and RIGHT in cango:
					cango.remove(LEFT)
				else: pass
					# raise Exception("Orange ghost does not have a direction")
				self.dir = random.choice(cango)
		else:
			if self.current_image == "FRIGHTENED" and self.dead == False:
				self.image = pygame.Surface(GHOSTSIZE).convert_alpha()
				self.image.set_colorkey((0, 0, 0))
				self.image.blit(self.imo, (0, 0))
				self.current_image = "NORMAL"
			self.state = redsprite.return_state()
			if self.state == SCATTER and self.counter == TILESIZE[0] and self.start == False:
				self.counter = 0
				self.target = (1, 23)
				self.dir = self.decide_direction(
					self.return_position(), self.target)
			elif self.state == CHASE and self.counter == TILESIZE[0] and self.start == False:
				self.counter = 0
				pacmanpos = pacmansprite.get_position()
				self.distance_from_pacman = (((pacmanpos[0]-self.return_position()[0])**2)+(
					(pacmanpos[1]-self.return_position()[1])**2))**0.5
				if self.distance_from_pacman < 6:
					self.target = (1, 23)
					self.dir = self.decide_direction(
						self.return_position(), self.target)
				else:
					self.target = pacmansprite.get_position()
					self.dir = self.decide_direction(
						self.return_position(), self.target)


class RedGhost(Ghosts):
	def __init__(self, x, y):
		super().__init__(x, y)

		if SCALE == 1:
			self.imr = pygame.image.load("red.png").convert_alpha()
		elif SCALE == 2:
			self.imr = pygame.image.load("redhalf.png").convert_alpha()
		self.image.blit(self.imr, (0, 0))

		self.dir = LEFT
		self.state = None
		self.start = False

		self.colour = 'RED'

	def reset_variables(self):
		self.start = False
		self.counter = 0
		self.dir = LEFT

	def move(self):
		if self.counter == TILESIZE[0] and self.start == False and self.dead == True:
			if SCALE == 1:
				self.target = (10, 11)
			elif SCALE == 2:
				self.target = (11, 12)
			if self.return_position() == self.target:
				self.dead = False
				self.just_dead = True
				if self.lock.locked():
					self.lock.release()
				self.image = pygame.Surface(GHOSTSIZE).convert_alpha()
				self.image.set_colorkey(black)
				self.image.blit(self.imr, (0, 0))
			else:
				self.counter = 0
				cango = self.direction_check()
				self.dir = self.decide_direction(self.return_position(), self.target)
		elif pacmansprite.energised_pacman():
			if self.current_image == "NORMAL":
				self.image = pygame.Surface(GHOSTSIZE).convert_alpha()
				self.image.set_colorkey((0, 0, 0))
				self.image.blit(self.frightened_image, (0, 0))
				self.current_image = "FRIGHTENED"
			if self.counter == TILESIZE[0] and self.start == False and self.dead == False:
				self.counter = 0
				cango = self.direction_check()
				if self.dir == UP and UP in cango:
					cango.remove(DOWN)
				elif self.dir == DOWN and DOWN in cango:
					cango.remove(UP)
				elif self.dir == LEFT and LEFT in cango:
					cango.remove(RIGHT)
				elif self.dir == RIGHT and RIGHT in cango:
					cango.remove(LEFT)
				else: pass
					# raise Exception("Red ghost does not have a direction")
				self.dir = random.choice(cango)
		else:
			if self.current_image == "FRIGHTENED" and self.dead == False:
				self.image = pygame.Surface(GHOSTSIZE).convert_alpha()
				self.image.set_colorkey((0, 0, 0))
				self.image.blit(self.imr, (0, 0))
				self.current_image = "NORMAL"
			if self.state == SCATTER and self.counter == TILESIZE[0] and self.start == False:
				self.counter = 0
				self.target = (17, -2)
				self.dir = self.decide_direction(
					self.return_position(), self.target)
			elif self.state == CHASE and self.counter == TILESIZE[0] and self.start == False:
				self.counter = 0
				self.target = pacmansprite.get_position()
				self.dir = self.decide_direction(
					self.return_position(), self.target)


class Pickup(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.Surface(PICKUPSIZE)
		self.image.fill(yellow)
		self.rect = self.image.get_rect()
		self.rect.centerx = x + TILESIZE[0]/2
		self.rect.centery = y + TILESIZE[1]/2

		pickupgroup.add(self)


class Energy_Blob(pygame.sprite.Sprite):  # Make this a circle
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.Surface(ENERGYPICKUPSIZE).convert_alpha()
		self.image.set_colorkey((0, 0, 0))
		pygame.draw.circle(
			self.image, yellow, (ENERGYPICKUPSIZE[0]//2, ENERGYPICKUPSIZE[1]//2), ENERGYPICKUPSIZE[0]//2)
		self.rect = self.image.get_rect()
		self.rect.centerx = x + TILESIZE[0]/2
		self.rect.centery = y + TILESIZE[0]/2

		energypickupgroup.add(self)


class Tile(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.Surface(TILESIZE)
		self.rect = self.image.get_rect()

		self.rect.x = x
		self.rect.y = y
		tilegroup.add(self)


class Floor(Tile):
	def __init__(self, x, y):
		super().__init__(x, y)
		self.image.fill(black)

		floorgroup.add(self)


class Wall(Tile):
	def __init__(self, x, y):
		super().__init__(x, y)
		self.image.fill(navy)

		wallgroup.add(self)


class Door(Tile):
	def __init__(self, x, y):
		super().__init__(x, y)
		self.image.fill(blue)

		wallgroup.add(self)
		doorgroup.add(self)


class Text(pygame.sprite.Sprite):
	def __init__(self, text, textboxsize, textpos):
		super().__init__()
		self.image = pygame.Surface(textboxsize).convert_alpha()
		self.image.set_colorkey((0, 0, 0))
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = textpos

		self.myfont = pygame.font.SysFont("Calibri", FONTSIZE)
		self.tsurf = self.myfont.render(text, True, white)
		self.trect = self.tsurf.get_rect()

		self.image.blit(self.tsurf, (self.rect.width//2 -
									 self.trect.w//2, self.rect.height//2-self.trect.h//2))
		textgroup.add(self)


pygame.init()
screen = pygame.display.set_mode(SCREENSIZE)
pygame.display.set_caption("Pacman")

pacmangroup = pygame.sprite.Group()
ghostgroup = pygame.sprite.Group()
pickupgroup = pygame.sprite.Group()
energypickupgroup = pygame.sprite.Group()
tilegroup = pygame.sprite.Group()
floorgroup = pygame.sprite.Group()
wallgroup = pygame.sprite.Group()
doorgroup = pygame.sprite.Group()
textgroup = pygame.sprite.Group()

try:
	with open('/media/luka/CE3D-D8EF/Pacman/map.csv') as file:
		reader = csv.reader(file)
		mapdata = []
		for i in reader:
			mapdata.append(i)
except FileNotFoundError:
	with open(f'{PARENT_DIRECTORY}/map.csv') as file:
		reader = csv.reader(file)
		mapdata = []
		for i in reader:
			mapdata.append(i)

worldmap = []
GPS = []
for i in range(len(mapdata)):
	worldmap.append([])
	GPS.append([])
	for j in range(len(mapdata[i])):
		if mapdata[i][j][0] == '#':
			worldmap[i].append(
				Wall(TILESIZE[0]*j-OFFSET, TILESIZE[1]*i-OFFSET))
			GPS[i].append(WALL)
		elif mapdata[i][j][0] == '~':
			worldmap[i].append(
				Door(TILESIZE[0]*j-OFFSET, TILESIZE[1]*i-OFFSET))
			GPS[i].append(DOOR)
		elif mapdata[i][j][0] == '.':
			worldmap[i].append(
				Floor(TILESIZE[0]*j-OFFSET, TILESIZE[1]*i-OFFSET))
			GPS[i].append(FLOOR)
			if mapdata[i][j][-1] != 'p' and mapdata[i][j][-1] != 'B':
				Pickup(TILESIZE[0]*j-OFFSET, TILESIZE[1]*i-OFFSET)
			if mapdata[i][j][-1] == 'e':
				Energy_Blob(TILESIZE[0]*j-OFFSET, TILESIZE[1]*i-OFFSET)
		if mapdata[i][j][-1] == 'p':
			pacmansprite = Pacman(
				TILESIZE[0]*j+GAP-OFFSET, TILESIZE[1]*i+GAP-OFFSET)
		if mapdata[i][j][0] == 'g':
			if mapdata[i][j][-2] == "r":
				redsprite = RedGhost(
					TILESIZE[0]*j+GHOSTGAP[0]-OFFSET, TILESIZE[1]*i+GHOSTGAP[1]-OFFSET)
				worldmap[i].append(
					Floor(TILESIZE[0]*j-OFFSET, TILESIZE[1]*i-OFFSET))
				GPS[i].append(FLOOR)
				Pickup(TILESIZE[0]*j-OFFSET, TILESIZE[1]*i-OFFSET)
			elif mapdata[i][j][-2] == "o":
				orangesprite = OrangeGhost(
					TILESIZE[0]*j+GHOSTGAP[0]-OFFSET, TILESIZE[1]*i+GHOSTGAP[1]-OFFSET)
				worldmap[i].append(
					Floor(TILESIZE[0]*j-OFFSET, TILESIZE[1]*i-OFFSET))
				GPS[i].append(FLOOR)
			elif mapdata[i][j][-2] == "p":
				pinksprite = PinkGhost(
					TILESIZE[0]*j+GHOSTGAP[0]-OFFSET, TILESIZE[1]*i+GHOSTGAP[1]-OFFSET)
				worldmap[i].append(
					Floor(TILESIZE[0]*j-OFFSET, TILESIZE[1]*i-OFFSET))
				GPS[i].append(FLOOR)
			elif mapdata[i][j][-2] == "b":
				bluesprite = BlueGhost(
					TILESIZE[0]*j+GHOSTGAP[0]-OFFSET, TILESIZE[1]*i+GHOSTGAP[1]-OFFSET)
				worldmap[i].append(
					Floor(TILESIZE[0]*j-OFFSET, TILESIZE[1]*i-OFFSET))
				GPS[i].append(FLOOR)

redspritestate = threading.Thread(target=redsprite.change_state, daemon=True)
redspritestate.start()

draw_dead_ghosts = True

started = False

starttext = Text("Press space to start", STARTTEXTSIZE, (0, 12))

while not started:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			started = True
			done = True
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				started = True
				done = True
			elif event.key in [pygame.K_SPACE, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN]:
				started = True
				done = False

	screen.fill(black)

	tilegroup.draw(screen)
	pickupgroup.draw(screen)
	energypickupgroup.draw(screen)
	ghostgroup.draw(screen)
	pacmangroup.draw(screen)
	textgroup.draw(screen)

	pygame.display.flip()

for i in textgroup:
	i.kill()

while not done and pacmansprite.return_lives() and pickupgroup:
	if not pacmansprite.dead():
		pygame.display.set_caption(
			f"Pacman - score: {pacmansprite.return_score()} - lives: {pacmansprite.return_lives()}")

		pygame.time.Clock().tick(FPS)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					done = True
				elif event.key == pygame.K_LEFT:
					pacmansprite.change_direction(LEFT)
				elif event.key == pygame.K_RIGHT:
					pacmansprite.change_direction(RIGHT)
				elif event.key == pygame.K_DOWN:
					pacmansprite.change_direction(DOWN)
				elif event.key == pygame.K_UP:
					pacmansprite.change_direction(UP)

		pacmansprite.update()
		ghostgroup.update()
		redsprite.move()
		pinksprite.move()
		bluesprite.move()
		orangesprite.move()

		screen.fill(black)

		tilegroup.draw(screen)
		pickupgroup.draw(screen)
		energypickupgroup.draw(screen)
		if not pacmansprite.am_dying():
			draw_dead_ghosts = True
			ghostgroup.draw(screen)
		else:
			if draw_dead_ghosts:
				ghostgroup.draw(screen)
				sleep(1)
				draw_dead_ghosts = False
			sleep(1)
			bluesprite.reset_position()
			redsprite.reset_position()
			orangesprite.reset_position()
			pinksprite.reset_position()
		pacmangroup.draw(screen)
		textgroup.draw(screen)

		pygame.display.flip()
	else:
		tilegroup.draw(screen)
		ghostgroup.draw(screen)
		pacmangroup.draw(screen)
		pacmansprite.die()
		pygame.display.flip()

if not pickupgroup:
	print("You won!")
elif pacmansprite.return_lives() == 0:
	print("You ran out of lives")
exit()
