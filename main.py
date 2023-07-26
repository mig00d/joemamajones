import pygame
import random
import math

"""
Todo:
- faire piege rapidité
- faire énemie qui suivent
- faire system vie et écran de mort
- infinie et plus dur ou niveaux ?
"""


class Background:
	def __init__(self, winHeight):
		self.img = pygame.image.load('images/background.png')
		self.imgWidth = self.img.get_size()[0]
		self.img = pygame.transform.scale(self.img, (self.imgWidth, winHeight))

	def render(self, screen):
		# répète pour remplir tout la fenêtre avec le bg
		screen.blit(self.img, (0, 0))
		screen.blit(self.img, (self.imgWidth, 0))
		screen.blit(self.img, (self.imgWidth * 2, 0))


class Game:
	"""
	level 0: start page
	"""
	def __init__(self):

		self.fps = 60
		pygame.init()
		self.screen = pygame.display.set_mode((winWidth, winHeight))
		self.clock = pygame.time.Clock()
		self.deltaTime = 0
		self.level = 0
		pygame.font.init()
		self.font = pygame.font.SysFont("font/upheavtt.ttf",50)

	def menu(self):
		backgroundMenu = pygame.transform.scale(pygame.image.load("images/backgroundmenu.png"), (winWidth, winHeight))
		title = pygame.image.load("images/joemamajones.png")
		titleWidth, titleHeight = title.get_size()
		playButton = pygame.image.load("images/playbutton.png")
		playButtonWidth, playButtonHeight = playButton.get_size()
		playButtonX, playButtonY = winWidth // 2 - playButtonWidth // 2, winHeight // 2
		self.screen.blit(backgroundMenu, (0,0))
		self.screen.blit(title, (winWidth // 2 - titleWidth // 2, winHeight // 3))
		self.screen.blit(playButton, (playButtonX, playButtonY))
		if clickButton(playButtonX, playButtonY, playButtonWidth, playButtonHeight):
			self.resetGame()
			self.level = 1

	def resetGame(self):
		self.background = Background(winHeight)
		self.player = Player(speed=500)
		self.rockList = spawnRock(10, self.player)
		self.treasureList = []
		for i in range(3):
			self.treasureList = spawnTreasure(self.treasureList, self.rockList)

		self.score = 0
		self.homeButton = pygame.image.load("images/homebutton.png")
		self.homeButtonWidth, self.homeButtonHeight = self.homeButton.get_size()
		self.homeButtonX, self.homeButtonY = 0, 0

	def game(self):
		self.player.move(self.deltaTime)
		self.player.screenCollision()

		self.background.render(self.screen)
		for rock in self.rockList:
			rock.collision(self.player)
			rock.render(self.screen)

		for treasure in self.treasureList:
			if treasure.collision(self.player):
				self.score += 1
				self.treasureList.remove(treasure)
				self.treasureList = spawnTreasure(self.treasureList, self.rockList)

			treasure.render(self.screen)

		if clickButton(self.homeButtonX, self.homeButtonY, self.homeButtonWidth, self.homeButtonHeight):
			self.level = 0

		self.player.render(self.screen)
		self.screen.blit(self.homeButton, (self.homeButtonX, self.homeButtonY))
		scoreText = self.font.render(str(self.score), False, (255, 255, 255))
		self.screen.blit(scoreText, (winWidth // 2, 0))


	def levelGestion(self):
		if self.level == 0:
			self.menu()

		if self.level == 1:
			self.game()

	def run(self):
		running = True
		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

			self.levelGestion()
			pygame.display.flip()
			self.deltaTime = self.clock.tick(self.fps) / 1000

		pygame.quit()


class Player:
	def __init__(self, speed):
		self.imgLeft = pygame.image.load('images/playerleft.png')
		self.imgRight = pygame.image.load('images/playerright.png')
		self.rect = self.imgLeft.get_rect()
		self.rect.x, self.rect.y = random.randint(0, winWidth), random.randint(0, winHeight)
		self.speed = speed
		self.postureDirection = 0
		self.direction = ""

	def move(self, dt):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_z]:
			self.rect.y -= self.speed * dt
			self.direction = "up"
		if keys[pygame.K_s]:
			self.rect.y += self.speed * dt
			self.direction = "down"
		if keys[pygame.K_q]:
			self.rect.x -= self.speed * dt
			self.postureDirection = 0
			self.direction = "left"
		if keys[pygame.K_d]:
			self.rect.x += self.speed * dt
			self.postureDirection = 1
			self.direction = "right"

	def screenCollision(self):
		if self.rect.left <= 0:
			self.rect.x = 0
		if self.rect.right >= winWidth:
			self.rect.x = winWidth - self.rect.width
		if self.rect.top <= 0:
			self.rect.y = 0
		if self.rect.bottom >= winHeight:
			self.rect.y = winHeight - self.rect.height

	def render(self, screen):
		if self.postureDirection == 0:
			screen.blit(self.imgLeft, (self.rect.x, self.rect.y))
		if self.postureDirection == 1:
			screen.blit(self.imgRight, (self.rect.x, self.rect.y))


class Rock:
	def __init__(self, imgPath, player):
		self.img = pygame.image.load(imgPath)
		self.rect = self.img.get_rect()
		self.rect.x, self.rect.y = random.randint(0, winWidth), random.randint(0, winHeight)
		while self.rect.x == player.rect.x and self.rect.y == player.rect.y:
			self.rect.x, self.rect.y = random.randint(0, winWidth), random.randint(0, winHeight)


	def collision(self, player):
		collisionTolerence = 10
		if player.rect.colliderect(self.rect):
			# coté haut pierre
			if abs(self.rect.top - player.rect.bottom) < collisionTolerence:
				if player.direction == "down" or "left" or "right":
					player.rect.bottom = self.rect.top
			# coté bas pierre
			if abs(self.rect.bottom - player.rect.top) < collisionTolerence:
				if player.direction == "up" or "left" or "right":
					player.rect.top = self.rect.bottom
			# coté gauche pierre
			if abs(self.rect.left - player.rect.right) < collisionTolerence:
				if player.direction == "right":
					player.rect.right = self.rect.left
			# coté droite pierre
			if abs(self.rect.right - player.rect.left) < collisionTolerence:
				if player.direction == "left":
					player.rect.left = self.rect.right

	def render(self, screen):
		screen.blit(self.img, (self.rect.x, self.rect.y))

class Treasure:
	def __init__(self, type, rockList):
		self.img = pygame.image.load("images/" + type + ".png")
		self.rect = self.img.get_rect()
		self.rect.x, self.rect.y = random.randint(0 + self.rect.width, winWidth - self.rect.width), random.randint(0 + self.rect.height, winHeight - self.rect.height)
		for rock in rockList:
			while self.rect.x == rock.rect.x and self.rect.y == rock.rect.y:
				self.rect.x, self.rect.y = random.randint(0 + self.rect.width, winWidth - self.rect.width), random.randint(0 + self.rect.height, winHeight - self.rect.height)

	def collision(self, player):
		if player.rect.colliderect(self.rect):
			return True
		return False

	def render(self, screen):
		screen.blit(self.img, (self.rect.x, self.rect.y))

def clickButton(buttonX, buttonY, buttonWidth, buttonHeight):
	if pygame.mouse.get_pressed()[0]:
		mouseX, mouseY = pygame.mouse.get_pos()
		if mouseX > buttonX and mouseX < buttonX + buttonWidth:
			if mouseY < buttonY + buttonHeight and mouseY > buttonY:
				return True
	return False


def spawnRock(nbRock, player):
	rockList = []
	for i in range(nbRock):
		rockList.append(Rock("images/rock.png", player))
	return rockList

def spawnTreasure(treasureList, rockList):
	type = ["diamond", "gold", "emerald"]
	treasureList.append(Treasure(type[random.randint(0,2)], rockList))
	return treasureList


def main():
	# fait spawn les premiers trésors
	for i in range(nbTreasure):
		treasureList = spawnTreasure(nbTreasure, treasureList)

		background.render(screen)
		player.render(screen)
		player.move(deltaTime)
		player.screenCollision()
		for rock in rockList:
			rock.collision(player)
			rock.render(screen)

		for treasure in treasureList:
			treasure.render(screen)
			if treasure.collision(player):
				score += 1
				treasureList.remove(treasure)
				treasureList = spawnTreasure(1, treasureList)

winWidth = 1280
winHeight = 720


Game().run()
