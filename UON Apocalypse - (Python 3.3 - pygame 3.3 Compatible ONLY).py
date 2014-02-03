#!/usr/bin/env python

'''
University of Nottingham Apocalypse.

Created by Stephen Sowole and Oyedipo Areoye
'''
import pygame, random, sys

from pygame.sprite import Sprite
from random import choice


#SYSTEM CONFIGURATION

#SCREEN CONFIGURATION
VERSION = "2.6"
WIDTH = 800
HEIGHT = 600
FPS = 30
#GAME SETTINGS
POWERUP_SCORE = 50
COIN_SCORE = 250
ENEMY_KILL = 500
WAVE_SCORE = 10000
#ENEMY SETTINGS
ENEMY_SPAWNTIME = 60
#NORMAL ENEMY SETTINGS
ENEMY_SPEED = 1.5
ENEMY_MAXSPEED = 5.0
ENEMY_ACCELERATION = 0.1
#FAST ENEMY SETTINGS
FAST_ENEMY_SPEED = 3.0
FAST_ENEMY_MAXSPEED = 6.0
FAST_ENEMY_ACCEL = 0.2
#POWER EATING ENEMY SETTINGS
P_E_ENEMY_SPEED = 2.0
P_E_ENEMY_MAXSPEED = 4.0
P_E_ENEMY_ACCEL = 0.25
#SUPER ENEMY SETTINGS
SUPER_ENEMY_SPEED = 4.5
SUPER_ENEMY_MAXSPEED = 7.5
SUPER_ENEMY_ACCEL = 0.4
#COIN SETTINGS
MAX_COINS = 1
COIN_SPAWNTIME = 2
#HUMAN SETTINGS
HUMAN_SPEED = 6
HUMAN_LIFE = 3
MAX_LIFE = 5
SUPER_HUMAN_DURATION = 200
#POWER-UP SETTINGS
MAX_POWERUPS = 2
POWERUP_SPAWNTIME = 60
#WAVE SETTINGS
CURRENT_WAVE = 1
MAX_ENEMY = 10

'''
Game Class
'''
# main class that holds most of the information used in the program
class Game:
    def __init__(self):
        # set the default background to the first background image
        self.backgroundNo = 1
        self.backReset = False
        self.enemyCount = 0
        self.coinCount = 0
        self.powerUpCount = 0
        self.maxCoinCount = MAX_COINS
        self.maxPowerUpCount = MAX_POWERUPS
        self.coinSpawnTime = COIN_SPAWNTIME
        self.powerUpSpawnTime = POWERUP_SPAWNTIME
        self.spawnTime = ENEMY_SPAWNTIME 
        self.highScore = 0
        self.time = 0
        self.retreat = False
        self.running = True
        self.powerUpChosen = None
        self.distraction = False
        self.shop = False
        self.bombUpgraded = False
        self.lightUpgraded = False
        self.nukeUnlocked = False
        self.missileUnlocked = False
        self.help = False
        
    def getBackNo(self):
        return self.backgroundNo
    def resetBackNo(self):
        # when restarting, the program will choose a random background to display
        self.backReset = True
        self.backgroundNo = random.randrange(1,4)
    def unlockHelp(self):
        self.help = True
    def helper(self):
        return self.help
    def unlockMissile(self):
        self.missileUnlocked = True
    def missile(self):
        return self.missileUnlocked
    def unlockNuke(self):
        self.nukeUnlocked = True
    def nuke(self):
        return self.nukeUnlocked 
    def lightUpgrade(self):
        self.lightUpgraded = True
    def getLight(self):
        return self.lightUpgraded
    def bombUpgrade(self):
        self.bombUpgraded = True
    def getBomb(self):
        return self.bombUpgraded
    def setScreen(self):
        self.screen = pygame.display.set_mode([WIDTH,HEIGHT])
    def getScreen(self):
        return self.screen
    def getEnemyCount(self):
        return self.enemyCount
    def getCoinCount(self):
        return self.coinCount
    def getMaxCoinCount(self):
        return self.maxCoinCount
    def getPowerUpSpawnTime(self):
        return self.powerUpSpawnTime
    def getMaxPowerUpCount(self):
        return self.maxPowerUpCount
    def getCoinSpawnTime(self):
        return self.coinSpawnTime
    def getPowerUpCount(self):
        return self.powerUpCount
    def getHighScore(self):
        return self.highScore
    def getShop(self):
        return self.shop
    def getTime(self):
        return self.time
    def increaseTime(self):
        # i used a counter instead of pygame.time.get_ticks() as i found a counter was more reliable
        self.time += 1
    def increasePowerUpCount(self):
        self.powerUpCount += 1
    def decreasePowerUpCount(self):
        self.powerUpCount -= 1
    def increaseCoinCount(self):
        self.coinCount += 1
    def decreaseCoinCount(self):
        self.coinCount -= 1
    def increaseEnemyCount(self):
        self.enemyCount += 1
    def decreaseEnemyCount(self):
        self.enemyCount -= 1
    def setRetreat(self, retreat):
        self.retreat = retreat
    def getRetreat(self):
        return self.retreat
    def setShop(self, shop):
        self.shop = shop
    def setPower(self, power):
        self.powerUpChosen = power
    def getPower(self):
        return self.powerUpChosen
    def setDistraction(self, distract):
        self.distraction = distract
    def getDistraction(self):
        return self.distraction
    def getSpawnTime(self, wave):
        # set the spawn time based on the current wave the player is on
        if wave < 5:
            self.spawn = (self.spawnTime / 5)* (6 - wave) 
        else:
            self.spawn = (self.spawnTime / 5)
        return self.spawn
    def stop(self):
        self.running = False
    def getRunning(self):
        return self.running
    def resetEnemyCount(self):
        self.enemyCount = 0
    def restart(self):
        # this method is called when the program is reset
        self.highScore = 0
        self.enemyCount = 0
        self.coinCount = 0
        self.powerUpCount = 0
        self.time = 0

# below are all of the classes i used in the game. i chose to duplicate classes for different purposes rather than using inheritance as i was planning to make
# modifications

'''
Display Classes
'''

class Countdown(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.score = 0
        self.font = pygame.font.SysFont("Impact", 23)
        self.count = pygame.time.get_ticks()

    def update(self, human, score, remaining):
        # the time will start at 10 and count down until it reaches 0; at this point the sprite 'kills' itself
        time = 10 - ((pygame.time.get_ticks() - self.count)/ 1000)
        if time >= 0:
            self.image = self.font.render("Time until next wave: %.1f"%(time), True, pygame.Color("white"))
            self.rect = self.image.get_rect()
            self.rect.center = (WIDTH/2, HEIGHT * 9/10)
        else:
            Sprite.kill(self)

class Score(Sprite):
    def __init__(self, color):
        pygame.sprite.Sprite.__init__(self)
        self.color = pygame.Color(color)
        self.font = pygame.font.SysFont("Impact", 23)
        self.score = 0
        self.render_text()
        self.rect = self.image.get_rect()
        self.rect.center = 57, 15

    def render_text(self):
        self.image = self.font.render("%08d"%(self.score), True, self.color)

    # these methods are self explanatory
    def enemyScore(self):
        self.score += ENEMY_KILL
        self.render_text()

    def coinScore(self):
        self.score += COIN_SCORE
        self.render_text()

    def powerUpScore(self):
        self.score += POWERUP_SCORE
        self.render_text()

    def waveScore(self):
        self.score += WAVE_SCORE
        self.render_text()

    def reset(self):
        self.score = 0


class Waves(Sprite):
    def __init__(self, color):
        pygame.sprite.Sprite.__init__(self)
        self.color = pygame.Color(color)
        self.font = pygame.font.SysFont("Impact", 25)
        self.currentWave = CURRENT_WAVE
        self.render_text()
        self.rect = self.image.get_rect()
        self.rect.center = 500, 17

    def render_text(self):
        self.image = self.font.render("Wave  %d"%(self.currentWave), True, self.color)

    def increaseWave(self):
        self.currentWave += 1
        self.render_text()

    def getWave(self):
        return self.currentWave

    def reset(self):
        self.currentWave = CURRENT_WAVE
        
class Remaining(Sprite):
    def __init__(self, color, wave):
        pygame.sprite.Sprite.__init__(self)
        self.color = pygame.Color(color)
        self.font = pygame.font.SysFont("Impact", 23)
        self.enemyIncrease = 5
        # this class takes in the current wave number to calculate the amount of enemies to have in a level
        self.maxEnemy = MAX_ENEMY + ((wave - 1) * self.enemyIncrease) 
        self.remaining = self.maxEnemy
        self.render_text()
        self.rect = self.image.get_rect()
        self.rect.center = 230, 15

    def render_text(self):
        self.image = self.font.render("Enemies: %d"%(self.remaining), True, self.color)

    def increaseEnemy(self):
        self.maxEnemy += self.enemyIncrease
        self.remaining = self.maxEnemy

    def decrease(self):
        # everytime an enemy is killed decrease the remaining count
        self.remaining -= 1

    def reset(self):
        # reset the maxenemy count based on the current wave constant, this allows for starting the game at any wave (testing purposes and modifications)
        self.remaining = MAX_ENEMY + ((CURRENT_WAVE - 1) * self.enemyIncrease)
        self.maxEnemy = MAX_ENEMY + ((CURRENT_WAVE - 1) * self.enemyIncrease)

    def getMaxEnemy(self):
        return self.maxEnemy

    def getRemaining(self):
        return self.remaining

'''
Power-Up Classes
'''

class Coin(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pygame.image.load("images/coin.png")
        self.rect = self.image.get_rect()
        self.spawnTime = COIN_SPAWNTIME
        self.maxCount = MAX_COINS

    def spawn(self, width, height):
        # this is the method used to spawn the coin within the area on screen (and below the display) this is also used alot with other classes
        xpos = random.randrange(width)
        ypos = random.randrange(height)
        self.rect.center = (xpos,ypos)
        self.rect.top = max(30, self.rect.top)
        self.rect.bottom = min(height, self.rect.bottom)
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, width)

# all of the powerup classes use the same concept used in the bomb class

class Bomb(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pygame.image.load("images/bomb.png")
        self.rect = self.image.get_rect()
        # each power-up will have a unique ID
        self.powerUpNo = 1
        
    def spawn(self, width, height):
        xpos = random.randrange(width)
        ypos = random.randrange(height)
        self.rect.center=(xpos,ypos)
        self.rect.top = max(30, self.rect.top)
        self.rect.bottom = min(height, self.rect.bottom)
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, width)

    def update(self, eatingEnemy_list, time, retreat, enemy_list, wave, human):
        # this method updates the eating enemy list which will draw the eating powerup zombies towards it
        eatingEnemy_list.update(self.rect.x, self.rect.y, time, retreat, human)

    def getType(self):
        return self.powerUpNo

class Nuke(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pygame.image.load("images/nuke.png")
        self.rect = self.image.get_rect()
        self.powerUpNo = 5
        
    def spawn(self, width, height):
        xpos = random.randrange(width)
        ypos = random.randrange(height)
        self.rect.center=(xpos,ypos)
        self.rect.top = max(30, self.rect.top)
        self.rect.bottom = min(height, self.rect.bottom)
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, width)

    def update(self, eatingEnemy_list, time, retreat, enemy_list, wave, human):
        eatingEnemy_list.update(self.rect.x, self.rect.y, time, retreat, human)

    def getType(self):
        return self.powerUpNo

class Missile(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pygame.image.load("images/missile.png")
        self.rect = self.image.get_rect()
        self.powerUpNo = 6
        
    def spawn(self, width, height):
        xpos = random.randrange(width)
        ypos = random.randrange(height)
        self.rect.center=(xpos,ypos)
        self.rect.top = max(30, self.rect.top)
        self.rect.bottom = min(height, self.rect.bottom)
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, width)

    def update(self, eatingEnemy_list, time, retreat, enemy_list, wave, human):
        eatingEnemy_list.update(self.rect.x, self.rect.y, time, retreat, human)

    def getType(self):
        return self.powerUpNo
     
class HelperPower(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pygame.image.load("images/helperP.png")
        self.rect = self.image.get_rect()
        self.powerUpNo = 7

    def spawn(self, width, height):
        xpos = random.randrange(width)
        ypos = random.randrange(height)
        self.rect.center = (xpos,ypos)
        self.rect.top = max(30, self.rect.top)
        self.rect.bottom = min(height, self.rect.bottom)
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, width)

    def update(self, eatingEnemy_list, time, retreat, enemy_list, wave, human):
        eatingEnemy_list.update(self.rect.x, self.rect.y, time, retreat, human)

    def getType(self):
        return self.powerUpNo
        

class Life(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pygame.image.load("images/heart.png")
        self.rect = self.image.get_rect()
        self.powerUpNo = 4

    def spawn(self, width, height):
        xpos = random.randrange(width)
        ypos = random.randrange(height)
        self.rect.center = (xpos,ypos)
        self.rect.top = max(30, self.rect.top)
        self.rect.bottom = min(height, self.rect.bottom)
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, width)

    def update(self, eatingEnemy_list, time, retreat, enemy_list, wave, human):
        eatingEnemy_list.update(self.rect.x, self.rect.y, time, retreat, human)

    def getType(self):
        return self.powerUpNo

class Invincibility(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pygame.image.load("images/invincibility.png")
        self.rect = self.image.get_rect()
        self.powerUpNo = 3

    def spawn(self, width, height):
        xpos = random.randrange(width)
        ypos = random.randrange(height)
        self.rect.center = (xpos,ypos)
        self.rect.top = max(30, self.rect.top)
        self.rect.bottom = min(height, self.rect.bottom)
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, width)

    def update(self, eatingEnemy_list, time, retreat, enemy_list, wave, human):
        eatingEnemy_list.update(self.rect.x, self.rect.y, time, retreat, human)
        
        hit_list = pygame.sprite.spritecollide(self, eatingEnemy_list, False)
        # for every powerup eating zombie that has collided with this powerup, create a 'super zombie' and remove the original zombie to make it look as if it has transformed
        # instead of removing the powerup upon collision, respawn it so that the player will have direct access to it as soon as a super zombie is created
        # but this also means that all powerup eating zombies onscreen can become super zombies
        for hit in hit_list:
            if hit.helper == False:
                enemy = SuperEnemy((self.rect.x, self.rect.y), wave.getWave())
                enemy_list.add(enemy)
                self.spawn(WIDTH, HEIGHT)
                Sprite.kill(hit)
            else:
                self.spawn(WIDTH, HEIGHT)
                # set the current powerup to be followed as none
                game.setPower(None)

    def getType(self):
        return self.powerUpNo

class Distraction(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pygame.image.load("images/distract.png")
        self.rect = self.image.get_rect()
        self.powerUpNo = 2

    def spawn(self, width, height):
        xpos = random.randrange(width)
        ypos = random.randrange(height)
        self.rect.center = (xpos,ypos)
        self.rect.top = max(30, self.rect.top)
        self.rect.bottom = min(height, self.rect.bottom)
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, width)

    def update(self, eatingEnemy_list, time, retreat, enemy_list, wave, human):
        eatingEnemy_list.update(self.rect.x, self.rect.y, time, retreat, human)

    def getType(self):
        return self.powerUpNo

# all enemy classes use the same concept as the enemy class
        
'''
Enemy Classes
'''

class Enemy(Sprite):
    def __init__(self, wave):
        Sprite.__init__(self)
        self.image = pygame.image.load("images/zombie.png")
        self.rect = self.image.get_rect()
        self.acceleration = ENEMY_ACCELERATION
        self.speed = ENEMY_SPEED
        # this sets the speed range for each enemy
        self.difficulty = (ENEMY_MAXSPEED - self.speed) / 5
        # the following lines of code set a random speed for an enemy based on the range given for that current wave.
        # with each wave increase the range of speed to randomly choose from decreases towards the max enemy speed so that
        # the average enemy speed will increase every wave making the game seem harder
        if wave < 5:
            self.speed = (wave * self.difficulty) + self.speed

        else:
            self.speed = (4 * self.difficulty) + self.speed
        # random speed chosen for every instance of this enemy class, so that every enemy has a different max speed, making it seem
        # as if each enemy is travelling at different speeds
        self.maxSpeed = random.uniform(self.speed, ENEMY_MAXSPEED)
        self.time = pygame.time.get_ticks()
            
    def spawn(self, width, height):
        # randomly spawn the enemy outside of the screen
        randomNum = random.randrange(0,4)
        if randomNum == 0:
            xpos = - 10
            ypos = random.randrange(height+1)
        elif randomNum == 1:
            xpos = random.randrange(width+1)
            ypos = - 10
        elif randomNum == 2:
            xpos = random.randrange(width+1)
            ypos = height + 10
        elif randomNum == 3:
            xpos = width + 10
            ypos = random.randrange(height+1)
        self.rect.center = (xpos, ypos)
        
    def update(self, x, y, time, retreat):
        timer = pygame.time.get_ticks() - self.time

        if timer >= 100000:
            self.maxSpeed = HUMAN_SPEED + 2
            self.speed = HUMAN_SPEED + 2

        if time % 100 == 0:
            if self.speed <= self.maxSpeed:
                self.speed += self.acceleration
            else:
                self.speed -= self.acceleration

        # this is how the enemies follow the human
        # self speed increases acceleration of every enemy based on
        # the time theyve been onscreen
        
        diffx = (x - self.rect.x)
        diffy = (y - self.rect.y)
        z = (((diffx ** 2)+(diffy ** 2)) ** 0.5)
    
            
        if diffx != 0 and diffy != 0:
            if retreat == False:
                self.rect.move_ip((diffx/z) * self.speed, (diffy/z) * self.speed)
            else:
                self.rect.move_ip(-(diffx/z)*1.3, -(diffy/z)*1.3)
            
                self.rect.top = max(0, self.rect.top)
                self.rect.bottom = min(HEIGHT, self.rect.bottom)
                self.rect.left = max(self.rect.left, 0)
                self.rect.right = min(self.rect.right, WIDTH)
            
class FastEnemy(Sprite):
    def __init__(self, wave):
        Sprite.__init__(self)
        self.image = pygame.image.load("images/fastEnemy.png")
        self.rect = self.image.get_rect()
        self.acceleration = FAST_ENEMY_ACCEL
        self.speed = FAST_ENEMY_SPEED
        self.difficulty = (FAST_ENEMY_MAXSPEED - self.speed) / 5
        
        if wave < 5:
            self.speed = (wave * self.difficulty) + self.speed
        else:
            self.speed = (4 * self.difficulty) + self.speed
            
        self.maxSpeed = random.uniform(self.speed, FAST_ENEMY_MAXSPEED)
        self.time = pygame.time.get_ticks()

    def spawn(self, width, height):
        
        randomNum = random.randrange(0,4)
        if randomNum == 0:
            xpos = - 10
            ypos = random.randrange(height+1)
        elif randomNum == 1:
            xpos = random.randrange(width+1)
            ypos = - 10
        elif randomNum == 2:
            xpos = random.randrange(width+1)
            ypos = height + 10
        elif randomNum == 3:
            xpos = width + 10
            ypos = random.randrange(height+1)
        self.rect.center = (xpos, ypos)
        
    def update(self, x, y, time, retreat):
        timer = pygame.time.get_ticks() - self.time

        if timer >= 100000:
            self.maxSpeed = HUMAN_SPEED + 2
            self.speed = HUMAN_SPEED + 2
        
        if time % 100 == 0:
            if self.speed <= self.maxSpeed:
                self.speed += self.acceleration
            else:
                self.speed -= self.acceleration
                
        diffx = (x - self.rect.x)
        diffy = (y - self.rect.y)
        z = (((diffx ** 2)+(diffy ** 2)) ** 0.5)

        if diffx != 0 and diffy != 0:
            if retreat == False:
                self.rect.move_ip((diffx/z) * self.speed, (diffy/z) * self.speed)
            else:
                self.rect.move_ip(-(diffx/z)*1.3, -(diffy/z)*1.3)
            
                self.rect.top = max(0, self.rect.top)
                self.rect.bottom = min(HEIGHT, self.rect.bottom)
                self.rect.left = max(self.rect.left, 0)
                self.rect.right = min(self.rect.right, WIDTH)

class PowerEatingEnemy(Sprite):
    def __init__(self, wave):
        Sprite.__init__(self)
        self.image = pygame.image.load("images/powerEatingZombie.png")
        self.rect = self.image.get_rect()
        self.acceleration = P_E_ENEMY_ACCEL
        self.speed = P_E_ENEMY_SPEED
        self.difficulty = (P_E_ENEMY_MAXSPEED - self.speed) / 5
        self.helper = False
        
        if wave < 5:
            self.speed = (wave * self.difficulty) + self.speed
        else:
            self.speed = (4 * self.difficulty) + self.speed
            
        self.maxSpeed = random.uniform(self.speed, P_E_ENEMY_MAXSPEED)
        self.time = pygame.time.get_ticks()

    def spawn(self, width, height):
        
        randomNum = random.randrange(0,4)
        if randomNum == 0:
            xpos = - 10
            ypos = random.randrange(height+1)
        elif randomNum == 1:
            xpos = random.randrange(width+1)
            ypos = - 10
        elif randomNum == 2:
            xpos = random.randrange(width+1)
            ypos = height + 10
        elif randomNum == 3:
            xpos = width + 10
            ypos = random.randrange(height+1)
        self.rect.center = (xpos, ypos)
        
    def update(self, x, y, time, retreat, human):
        timer = pygame.time.get_ticks() - self.time

        if timer >= 100000:
            Sprite.kill(self)
            game.decreaseEnemyCount()
            
        if time % 100 == 0:
            if self.speed <= self.maxSpeed:
                self.speed += self.acceleration
            else:
                self.speed -= self.acceleration

        diffx = (x - self.rect.x)
        diffy = (y - self.rect.y)
        z = (((diffx ** 2)+(diffy ** 2)) ** 0.5)

        if diffx != 0 and diffy != 0:
            if retreat == False:
                self.rect.move_ip((diffx/z) * self.speed, (diffy/z) * self.speed)
            else:
                self.rect.move_ip(-(diffx/z)*1.3, -(diffy/z)*1.3)
            
                self.rect.top = max(0, self.rect.top)
                self.rect.bottom = min(HEIGHT, self.rect.bottom)
                self.rect.left = max(self.rect.left, 0)
                self.rect.right = min(self.rect.right, WIDTH)
    
class SuperEnemy(Sprite):
    def __init__(self, position, wave):
        Sprite.__init__(self)
        self.image = pygame.image.load("images/superEnemy.png")
        self.rect = self.image.get_rect()
        self.acceleration = SUPER_ENEMY_ACCEL
        self.speed = SUPER_ENEMY_SPEED
        self.difficulty = (SUPER_ENEMY_MAXSPEED - self.speed) / 5
        
        if wave < 5:
            self.speed = (wave * self.difficulty) + self.speed
        else:
            self.speed = (4 * self.difficulty) + self.speed
            
        self.maxSpeed = random.uniform(self.speed, SUPER_ENEMY_MAXSPEED)
        self.rect.center = position
        self.time = pygame.time.get_ticks()

    def spawn(self, width, height):
        
        randomNum = random.randrange(0,4)
        if randomNum == 0:
            xpos = - 10
            ypos = random.randrange(height+1)
        elif randomNum == 1:
            xpos = random.randrange(width+1)
            ypos = - 10
        elif randomNum == 2:
            xpos = random.randrange(width+1)
            ypos = height + 10
        elif randomNum == 3:
            xpos = width + 10
            ypos = random.randrange(height+1)
        self.rect.center = (xpos, ypos)
        
    def update(self, x, y, time, retreat):
        timer = pygame.time.get_ticks() - self.time

        if timer >= 100000:
            self.maxSpeed = HUMAN_SPEED + 2
            self.speed = HUMAN_SPEED + 2
            
        if time % 100 == 0:
            if self.speed <= self.maxSpeed:
                self.speed += self.acceleration
            else:
                self.speed -= self.acceleration

        diffx = (x - self.rect.x)
        diffy = (y - self.rect.y)
        z = (((diffx ** 2)+(diffy ** 2)) ** 0.5)

        if diffx != 0 and diffy != 0:
            if retreat == False:
                self.rect.move_ip((diffx/z) * self.speed, (diffy/z) * self.speed)
            else:
                self.rect.move_ip(-(diffx/z)*1.3, -(diffy/z)*1.3)
            
                self.rect.top = max(0, self.rect.top)
                self.rect.bottom = min(HEIGHT, self.rect.bottom)
                self.rect.left = max(self.rect.left, 0)
                self.rect.right = min(self.rect.right, WIDTH)
                
'''
Game Objects Classes
'''
class Shot(Sprite):
    def __init__(self, enemy, human):
        Sprite.__init__(self)
        self.image = pygame.image.load("images/shot.png")
        self.rect = self.image.get_rect()
        # target set will be used to choose a random enemy in the sprite list
        self.targetSet = False
        self.target = None
        self.humx = human.rect.x
        self.humy = human.rect.y
        self.rect.center = (self.humx, self.humy)
        self.x = 0
        self.y = 0
        
    def update(self, enemy_list, enemyRemain, score):
        spritelist = enemy_list.sprites()
        if self.targetSet == False and spritelist:
            # if there hasnt been a target chosen and the enemy list is not empty then choose a target and save that sprite to the instance of this class
            self.target = choice(spritelist)
            self.targetSet = True
            
        elif spritelist and self.targetSet == True:
            # if the enemy list is not empty and there has been a target chosen then move towards the enemy
            prevx = self.x
            prevy = self.y
            self.x = self.target.rect.x
            self.y = self.target.rect.y
            
            if prevx == self.x and prevy == self.y:
                # if the current missile doesnt move then kill itself (used to avoid bugs)
                Sprite.kill(self)
            else:
                diffx = (self.x - self.rect.x)
                diffy = (self.y - self.rect.y)
                z = (((diffx ** 2)+(diffy ** 2)) ** 0.5)

                if diffx != 0 and diffy != 0:
                    self.rect.move_ip((diffx/z) * 4.5, (diffy/z) * 4.5)
                
                hit_list = pygame.sprite.spritecollide(self, enemy_list, True)
                for enemy in hit_list:
                    enemyRemain.decrease()
                    score.enemyScore()
                    Sprite.kill(self)
                # if the missile hits an enemy then remove the enemy sprite along with the missile itself
                
        elif not spritelist and self.targetSet == True:
            self.targetSet = False
            # if the sprite list is empty and a target has been chosen then set the target to be false (this can happen if the player kills the enemy
            # before the missile does

        if self.targetSet == False and not spritelist:
            # if there arent any enemies and the missile doesnt have a target then delete self
            Sprite.kill(self)

            
class NukeExplode(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pygame.Surface([WIDTH, HEIGHT])
        self.rect = self.image.get_rect()
        self.color = "white"
        pygame.draw.rect(self.image, pygame.Color(self.color), self.rect)
        self.explodeTime = pygame.time.get_ticks()
    
    def update(self, human, score, remain):
        time = pygame.time.get_ticks() - self.explodeTime

        # create a white flash on screen and remove all enemies as well as helpers and then kill self

        enemy_list = gameList.getEnemyList()
        
        for enemy in enemy_list:
            remain.decrease()
            score.enemyScore()
        enemy_list.empty()

        eatingEn = gameList.getEnemyEatingList()

        for enemy in eatingEn:
            remain.decrease()
            score.enemyScore()
            
        eatingEn.empty()

        if time >= 400:
            Sprite.kill(self)
            
class Mine(Sprite):
    def __init__(self, width, height):
        Sprite.__init__(self)
        # change the image used if it has been unlocked
        self.upgraded = game.getBomb()
        if self.upgraded == False:
            self.image = pygame.image.load("images/mine.png")
            self.imageExplode = pygame.image.load("images/Explode.png")
        else:
            self.image = pygame.image.load("images/mineUp.png")
            self.imageExplode = pygame.image.load("images/ExplodeUp.png")
        self.rect = self.image.get_rect()
        self.pos = (width, height)
        self.rect.center = self.pos
        self.explode = False
    
    def update(self, enemy_list, enemyRemain, score):
        
        hit_list = pygame.sprite.spritecollide(self, enemy_list, True)
        # check for collisions and remove sprites that have collided
        for enemy in hit_list:
            enemyRemain.decrease()
            score.enemyScore()
        
        if self.explode == False:
            for enemy in hit_list:
                self.image = self.imageExplode             
                self.rect = self.image.get_rect()
                self.rect.center = self.pos
                self.explode = True
                break
        else:
            Sprite.kill(self)

# this class is the display of hearts in the top right hand corner
class Heart(Sprite):
    def __init__(self, heartNo):
        Sprite.__init__(self)
        self.image = pygame.image.load("images/BigHeart.png")
        self.rect = self.image.get_rect()
        self.heartNo = heartNo

    def update(self):
        # for every heart collected, add it to the display using this method
        self.rect.center = (WIDTH - (self.heartNo * 20), 15)

class Light(Sprite):
    def __init__(self, width, height):
        Sprite.__init__(self)
        self.upgraded = game.getLight()
        if self.upgraded == False:
            self.image = pygame.image.load("images/light.png")
        else:
            self.image = pygame.image.load("images/lightUp.png")
        self.rect = self.image.get_rect()
        self.rect.center = (width, height)
        self.time = pygame.time.get_ticks()
        self.target = False
        
    def update(self, enemy_list, time, human, retreat):
        time = pygame.time.get_ticks() - self.time
        # if the current light is the target then update each enemy in the enemy list using the coordinates of this light
        if self.target == True:
            enemy_list.update(self.rect.x, self.rect.y, time, retreat)
            
        hit_list = pygame.sprite.spritecollide(self, enemy_list, False)

        # the light stops after a given time to make it more realistic. if the light is upgraded then make it so that there has to be 4 enemies until
        # it gets destroyed
        if self.upgraded == True:
            if len(hit_list) >= 4:
                game.setDistraction(False)
                self.target = False
                Sprite.kill(self)
                
            if time >= 7200:
                Sprite.kill(self)
                game.setDistraction(False)
                self.target = False
            
        else:   
            for hit in hit_list:
                game.setDistraction(False)
                self.target = False
                Sprite.kill(self)
                break
            
            if time >= 5000:
                Sprite.kill(self)
                game.setDistraction(False)
                self.target = False
        
    def makeTarget(self):
        self.target = True
        
        
class Shop(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pygame.image.load("images/shop.png")
        self.count = pygame.time.get_ticks()
        self.font = pygame.font.SysFont("Impact", 23)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)

    def update(self, human, score, remaining):
        # start the timer from 10
        time = 10 - ((pygame.time.get_ticks() - self.count)/ 1000)
        
        if time >= 0:
             # if the human has collided with the shop then remove the shop and show the shop screen
            if (pygame.sprite.collide_rect(human, self)) == True:
                self.shop(score, human)
                human.resetPosition(WIDTH, HEIGHT)
                Sprite.kill(self)
        else:
            # if the countdown has been reached and the human hasnt interacted with the shop then remove the shop
            Sprite.kill(self)

    def shop(self, score, human):
        screen = game.getScreen()
        self.background = pygame.image.load("images/shopUpgrade.png")
        shop = True
        while shop:
            # this is the shop screen, draw all the shop details onto the background
            pygame.time.Clock().tick(FPS)
            screen.blit(self.background, [0,0])
            self.points(score, screen)
            self.heart(human, screen)
            self.bomb(screen)
            self.invincibility(screen, human)
            self.power(screen)
            self.light(screen)
            self.missile(screen)
            self.helpers(screen)
            pygame.display.update()


            # if a choice has been made then remove the points from the score and do the following action
            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_s:
                        shop = False
                    if event.key==pygame.K_1:
                        if human.life < human.maxLife and score.score >= 10000:
                            human.increaseLife()
                            score.score -= 10000
                    if event.key==pygame.K_2:
                        if score.score >= 50000 and game.getBomb() == False:
                            game.bombUpgrade()
                            score.score -= 50000
                    if event.key==pygame.K_3:
                        if score.score >= 50000 and game.getLight() == False:
                            game.lightUpgrade()
                            score.score -= 50000
                    if event.key==pygame.K_4:
                        if score.score >= 70000 and human.upgraded == False:
                            human.upgraded = True
                            score.score -= 70000
                    if event.key==pygame.K_5:
                        if score.score >= 100000 and game.nuke() == False:
                            game.unlockNuke()
                            score.score -= 100000
                    if event.key==pygame.K_6:
                        if score.score >= 100000 and game.missile() == False:
                            game.unlockMissile()
                            score.score -= 100000
                    if event.key==pygame.K_7:
                        if score.score >= 250000 and game.helper() == False:
                            game.unlockHelp()
                            score.score -= 250000
                elif event.type == pygame.QUIT:
                    shop = False
                    game.stop()


    # the following methods print the details. if an upgrade has been purchased or the max hearts has been reached then set the out of stock message to be
    # displayed
    
    def points(self, score, screen):
        self.score = self.font.render("Score: %d"%(score.score), True, pygame.Color("yellow"))
        screen.blit(self.score, [10,0])

    def heart(self, human, screen):
        if human.life < human.maxLife:
            self.hearts = self.font.render("1. BUY HEART: 10,000 -- Current: %d"%(human.life), True, pygame.Color("yellow"))
        else:
            self.hearts = self.font.render("1. OUT OF STOCK! -- Current: %d"%(human.life), True, pygame.Color("red"))

        screen.blit(self.hearts, [WIDTH * 1/3, HEIGHT * 1/9])

    def bomb(self, screen):
        if game.getBomb() == False:
            self.bombs = self.font.render("2. UPGRADE BOMB: 50,000", True, pygame.Color("yellow"))
        else:
            self.bombs = self.font.render("2. OUT OF STOCK! UPGRADED ALREADY", True, pygame.Color("red"))
            
        screen.blit(self.bombs, [WIDTH * 1/3, HEIGHT * 2/9])

    def light(self, screen):
        if game.getLight() == False:
            self.lights = self.font.render("3. UPGRADE LIGHT: 50,000", True, pygame.Color("yellow"))
        else:
            self.lights = self.font.render("3. OUT OF STOCK! UPGRADED ALREADY", True, pygame.Color("red"))
        screen.blit(self.lights, [WIDTH * 1/3, HEIGHT * 3/9])
        
    def invincibility(self, screen, human):
        if human.upgraded == False:
            self.invin = self.font.render("4. UPGRADE STAR: 70,000", True, pygame.Color("yellow"))
        else:
            self.invin = self.font.render("4. OUT OF STOCK! UPGRADED ALREADY", True, pygame.Color("red"))
        screen.blit(self.invin, [WIDTH * 1/3, HEIGHT * 4/9])
        
    def power(self, screen):
        if game.nuke() == False:
            self.powers = self.font.render("5. UNLOCK NUKE: 100,000", True, pygame.Color("yellow"))
        else:
            self.powers = self.font.render("5. OUT OF STOCK! UNLOCKED ALREADY", True, pygame.Color("red"))
        screen.blit(self.powers, [WIDTH * 1/3, HEIGHT * 5/9])
        
    def missile(self, screen):
        if game.missile() == False:
            self.missiles = self.font.render("6. UNLOCK MISSILES: 100,000", True, pygame.Color("yellow"))
        else:
            self.missiles = self.font.render("6. OUT OF STOCK! UNLOCKED ALREADY", True, pygame.Color("red"))
        screen.blit(self.missiles, [WIDTH * 1/3, HEIGHT * 6/9])
        
    def helpers(self, screen):
        if game.helper() == False:
            self.helper = self.font.render("7. UNLOCK HELPER: 250,000", True, pygame.Color("yellow"))
        else:
            self.helper = self.font.render("7. OUT OF STOCK! UNLOCKED ALREADY", True, pygame.Color("red"))
        screen.blit(self.helper, [WIDTH * 1/3, HEIGHT * 7/9])

    
'''
Human Class
'''

class Human(Sprite):
    def __init__(self, width, height):
        Sprite.__init__(self)
        self.image = pygame.image.load("images/human.png")
        self.rightImage = pygame.image.load("images/righthuman.png")
        self.leftImage = pygame.image.load("images/lefthuman.png")
        self.super = pygame.image.load("images/SuperHuman.png")
        self.rect = self.image.get_rect()
        self.rect.center = (width/2, height/2)
        self.y_cord = 0
        self.x_cord = 0
        self.speed = HUMAN_SPEED
        self.life = HUMAN_LIFE
        self.maxLife = MAX_LIFE
        self.target = True
        self.superHuman = False
        self.upgraded = False
        self.superHumanDuration = SUPER_HUMAN_DURATION
        self.time = 0

    def up(self):
        self.y_cord -= self.speed
    def left(self):
        self.x_cord -= self.speed
    def right(self):
        self.x_cord += self.speed
    def down(self):
        self.y_cord += self.speed

    def update(self, width, height):
        # if the human is not super then add some simple animation
        if self.superHuman == False:
            if self.x_cord > 0:
                self.image = self.rightImage
            elif self.x_cord < 0:
                self.image = self.leftImage
            
        self.rect.move_ip(self.x_cord, self.y_cord)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(height, self.rect.bottom)
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, width)

        # if the human is super then start the timer
        if self.superHuman == True:
            self.timer()

    def timer(self):
        # the extra 20 is so that the player can react to the human changing forms without losing a life
        if self.time > self.superHumanDuration + 20:
            self.superHuman = False
            self.superHumanDuration = SUPER_HUMAN_DURATION
            self.time = 0
        # once the time is up change the image back to the human
        elif self.time == self.superHumanDuration:
            self.image = pygame.image.load("images/human.png")
            loc = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = loc
            
        self.time += 1

    def activateSuperHuman(self):
        # self explanatory - activate superhuman mode
        self.image = self.super
        loc = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = loc
        self.superHuman = True
        if self.upgraded == True:
            # when upgraded player can just keep collecting invincibility powerups and the timer will just keep resetting but the max time will keep increasing
            # until time runs out
            self.superHumanDuration += 150
        # start the time
        self.time = 0

    def getLife(self):
        return self.life

    def getMaxLife(self):
        return self.maxLife

    def getTarget(self):
        return self.target
    
    def setTarget(self, target):
        self.target = target

    def getSuperHuman(self):
        return self.superHuman
    
    def increaseLife(self):
        self.life += 1

    def removeLife(self):
        self.life -= 1

    def resetLife(self):
        self.life = HUMAN_LIFE

    def resetPosition(self, width, height):
        self.rect.center = (width/2, height/2)
        self.y_cord = 0
        self.x_cord = 0
        self.image = pygame.image.load("images/human.png")

# the helper will act like a power eating enemy but instead it will help out the player
        
class Helper(Sprite):
    def __init__(self, human):
        Sprite.__init__(self)
        self.image = pygame.image.load("images/helper.png")
        self.rect = self.image.get_rect()
        self.helper = True
        self.rect.center = human.rect.center
        self.time = self.time = pygame.time.get_ticks()
        
    def update(self, x, y, time, retreat, human):
        time = pygame.time.get_ticks() - self.time
        
        # after 35 seconds remove the helper
        if time >= 35000:
            Sprite.kill(self)

        diffx = (x - self.rect.x)
        diffy = (y - self.rect.y)
        z = (((diffx ** 2)+(diffy ** 2)) ** 0.5)

        if diffx != 0 and diffy != 0:
            self.rect.move_ip((diffx/z) * 5, (diffy/z) * 5)

        # if the helper collides with anything then execute the appropriate action
            
        sprite = pygame.sprite.spritecollideany(self, gameList.getPowerUpList())
        if sprite != None:
        
            if sprite.getType() == 1:
                mine = Mine(self.rect.x, self.rect.y)
                gameList.addToDisposeList(mine)
            
            elif sprite.getType() == 2:
                light = Light(self.rect.x, self.rect.y)
                gameList.addToDistractionList(light)
                human.setTarget(False)
                
            elif sprite.getType() == 4:
                if human.getLife() < human.getMaxLife():
                    human.increaseLife()
                    heart = Heart(human.getLife())
                    gameList.addToHeartList(heart)
                    drawHearts(human)
                
            elif sprite.getType() == 5:
                nuke = NukeExplode()
                gameList.addToSpriteList(nuke)

            elif sprite.getType() == 6:
                for shot in range(4):
                    shot = Shot(gameList.getEnemyList(), human)
                    gameList.addToDisposeList(shot)

            game.setPower(None)    
            Sprite.kill(sprite)
            game.decreasePowerUpCount()


'''
List Class
'''
# this class will hold all the lists in my game
class Lists:
    def __init__(self):
        self.human_list = pygame.sprite.GroupSingle()
        self.coin_list = pygame.sprite.Group()
        self.sprite_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.powerup_list = pygame.sprite.Group()
        self.dispose_list = pygame.sprite.Group()
        self.heart_list = pygame.sprite.Group()
        self.distraction_list = pygame.sprite.Group()
        self.eatingEnemy_list = pygame.sprite.Group()
    
    def getHeartList(self):
        return self.heart_list
    
    def getEnemyList(self):
        return self.enemy_list

    def getCoinList(self):
        return self.coin_list
    
    def getSpriteList(self):
        return self.sprite_list

    def getEnemyEatingList(self):
        return self.eatingEnemy_list
    
    def getPowerUpList(self):
        return self.powerup_list
    
    def getDistractionList(self):
        return self.distraction_list

    def getDisposeList(self):
        return self.dispose_list
    
    def addToHumanList(self, human):
        self.human_list.add(human)

    def addToSpriteList(self, sprite):
        self.sprite_list.add(sprite)

    def addToEnemyList(self, enemy):
        self.enemy_list.add(enemy)

    def addToEnemyEatingList(self, enemy):
        self.eatingEnemy_list.add(enemy)

    def addToHeartList(self, heart):
        self.heart_list.add(heart)

    def addToPowerUpList(self, powerUp):
        self.powerup_list.add(powerUp)

    def addToDisposeList(self, item):
        self.dispose_list.add(item)

    def addToDistractionList(self, distract):
        self.distraction_list.add(distract)

    def updateHeartList(self):
        self.heart_list.update()

    def addToCoinList(self, coin):
        self.coin_list.add(coin)

    def updateEnemyList(self, xcoord, ycoord, time, retreat):
        self.enemy_list.update(xcoord, ycoord, time, retreat)

    def updateEnemyEatingList(self, xcoord, ycoord, time, retreat, human):
        self.eatingEnemy_list.update(xcoord, ycoord, time, retreat, human)

    def updatePowerUpList(self, eatingEnemy, time, retreat, enemy):
        self.powerup_list.update(eatingEnemy, time, retreat, enemy)

    def updateDisposeList(self, enemy, remain, score):
        self.dispose_list.update(enemy, remain, score)

    def updateDistractionList(self, enemy_list, time, human, retreat):
        self.distraction_list.update(enemy_list, time, human, retreat)

    def updatePowerUp(self, sprite, eatingEnemy, time, retreat, enemy, wave, human):
        sprite.update(eatingEnemy, time, retreat, enemy, wave, human)

    def renderText(self, remaining, wave, score):
        remaining.render_text()
        wave.render_text()
        score.render_text()

    def updateScreen(self, screen):
        self.dispose_list.draw(screen)
        self.distraction_list.draw(screen)
        self.powerup_list.draw(screen)
        self.human_list.draw(screen)
        self.coin_list.draw(screen)
        self.enemy_list.draw(screen)
        self.eatingEnemy_list.draw(screen)
        self.heart_list.draw(screen)
        self.sprite_list.draw(screen)
        pygame.display.flip()

    def emptyHeartList(self):
        self.heart_list.empty()

    def emptyLists(self):
        self.coin_list.empty()
        self.enemy_list.empty()
        self.powerup_list.empty()
        self.dispose_list.empty()
        self.distraction_list.empty()
        self.eatingEnemy_list.empty()


'''
Main
'''
#Create new game object
game = Game()
# define all the sprite lists
gameList = Lists()


'''
Methods
'''
def updateLights(human):
    spritelist = gameList.getDistractionList().sprites()
    # chose a random distraction so that the enemy will follow
    if spritelist and game.getDistraction() == False:
        sprite = choice(spritelist)
        sprite.makeTarget()
        game.setDistraction(True)
    elif not spritelist:
        human.setTarget(True)
        game.setDistraction(False)

def checkRemaining(remaining, wave, score, human, background):
    # if there arent any enemies remaining then start the countdown
    if remaining.getRemaining() <= 0:
        if game.getShop() == False:
            count = Countdown()
            shop = Shop()
            gameList.addToSpriteList(count)
            gameList.addToSpriteList(shop)
            score.waveScore()
            game.setShop(True)
        
        elif len(gameList.getSpriteList()) == 3:
            drawHearts(human)
            game.setShop(False)
            remaining.increaseEnemy()
            wave.increaseWave()
            game.resetEnemyCount()
            
        else:
            drawHearts(human)

def chooseRandomPowerUp(wave, human):
    # choose random powerup for power eating zombies to follow
    spritelist = gameList.getPowerUpList().sprites()
    
    if spritelist and game.getPower() == None:
        game.setPower(choice(spritelist))
        
    elif game.getPower() != None and game.getRetreat() == False:
        gameList.updatePowerUp(game.getPower(), gameList.getEnemyEatingList(), game.getTime(), game.getRetreat(), gameList.getEnemyList(), wave, human)
            
def pygameEvents(key_map):
    # check for keyboard and quit events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.stop()
        # if key has been pressed down
        elif event.type == pygame.KEYDOWN and event.key in key_map:
            key_map[event.key][0]()
        # when key is released
        elif event.type == pygame.KEYUP and event.key in key_map:
            key_map[event.key][1]()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            pause()

def powerUpCollision(powerUp, eatingEnemy, human, score):
    # if there has been a collision between the human and powerup then do the required action
    sprite = pygame.sprite.spritecollideany(human, gameList.getPowerUpList())
    if sprite != None:
        
        if sprite.getType() == 1:
            mine = Mine(human.rect.x, human.rect.y)
            gameList.addToDisposeList(mine)
            
        elif sprite.getType() == 2:
            light = Light(human.rect.x, human.rect.y)
            gameList.addToDistractionList(light)
            human.setTarget(False)
                
        elif sprite.getType() == 3:
            human.activateSuperHuman()
                
        elif sprite.getType() == 4:
            if human.getLife() < human.getMaxLife():
                human.increaseLife()
                heart = Heart(human.getLife())
                gameList.addToHeartList(heart)
                drawHearts(human)
                
        elif sprite.getType() == 5:
            nuke = NukeExplode()
            gameList.addToSpriteList(nuke)

        elif sprite.getType() == 6:
            for shot in range(4):
                shot = Shot(gameList.getEnemyList(), human)
                gameList.addToDisposeList(shot)

        elif sprite.getType() == 7:
            helper = Helper(human)
            gameList.addToEnemyEatingList(helper)

        score.powerUpScore()
        game.setPower(None)    
        Sprite.kill(sprite)
        game.decreasePowerUpCount()

    hit_list = pygame.sprite.groupcollide(gameList.getEnemyEatingList(), gameList.getPowerUpList(), False, True)
    # if there has been a collision between the power eating zombie and the powerup then remove the powerup
    for hit in hit_list:
        game.decreasePowerUpCount()
        game.setPower(None)
                
        if game.getRetreat() == True:
            gameList.updateEnemyEatingList(human.rect.x, human.rect.y, game.getTime(), game.getRetreat())

def powerUpSpawn(current, maximum, human):
    # method used to spawn powerups based on probability
    
    currTime = game.getTime()
    spawnTime = game.getPowerUpSpawnTime()
    
    number = random.randrange(0,100)

    if current < maximum and currTime % spawnTime == 0:
        
        if number >= 0 and number < 34:
            bomb = Bomb()
            bomb.spawn(WIDTH, HEIGHT)
            gameList.addToPowerUpList(bomb)
            
        elif number >= 34 and number < 40:
            if game.helper() == True:
                helper = HelperPower()
                helper.spawn(WIDTH, HEIGHT)
                gameList.addToPowerUpList(helper)
            else:
                powerUpSpawn(current, maximum, human)
                game.decreasePowerUpCount()

        elif number >= 40 and number < 50:
            if game.nuke() == True:
                nuke = Nuke()
                nuke.spawn(WIDTH, HEIGHT)
                gameList.addToPowerUpList(nuke)
            else:
                powerUpSpawn(current, maximum, human)
                game.decreasePowerUpCount()
                
        elif number >= 50 and number < 65:
            if game.missile() == True and len(gameList.getEnemyList().sprites()) != 0:
                missile = Missile()
                missile.spawn(WIDTH, HEIGHT)
                gameList.addToPowerUpList(missile)
            else:
                powerUpSpawn(current, maximum, human)
                game.decreasePowerUpCount()
            
        elif number >= 65 and number < 80:
            distraction = Distraction()
            distraction.spawn(WIDTH, HEIGHT)
            gameList.addToPowerUpList(distraction)
                
        elif number >= 80 and number < 95:
            invincible = Invincibility()
            invincible.spawn(WIDTH, HEIGHT)
            gameList.addToPowerUpList(invincible)
            
        else:
            if human.getLife() < human.getMaxLife():
                life = Life()
                life.spawn(WIDTH, HEIGHT)
                gameList.addToPowerUpList(life)
            else:
                powerUpSpawn(current, maximum, human)
                game.decreasePowerUpCount()
            
        game.increasePowerUpCount()
    

def eatingEnemyCollision(human, remaining, score):
    # if the human collides with a power eating enemy then remove the powereating enemy
    hit_list = pygame.sprite.spritecollide(human, gameList.getEnemyEatingList(), False)

    for hit in hit_list:
        if hit.helper == False:
            remaining.decrease()
            score.enemyScore()
            Sprite.kill(hit)
                    
                    
def playSoundtrack():
    # self explanatory
    soundtrack = pygame.mixer.music
    soundtrack.load("sounds/Soundtrack.mp3")
    soundtrack.play(-1)
    
def restart(human, wave, score, remaining):
    wave.reset()
    score.reset()
    remaining.reset()
    gameList.renderText(remaining, wave, score)    
    gameList.emptyLists()
    human.resetLife()
    human.resetPosition(WIDTH, HEIGHT)
    drawHearts(human)
                    
def drawBackground(background):
    game.getScreen().blit(background, [0,0])
                    
def drawHearts(human):
    # draw the heart display to the screen
    gameList.emptyHeartList()
    
    for life in range(human.getLife()):
        life += 1
        heart = Heart(life)
        gameList.addToHeartList(heart)

    gameList.updateHeartList()
                    
def lifeLost(human):
    # when a life has been lost then make the enemies retreat for a set time
    game.setRetreat(True)
    background = pygame.image.load("images/Map" + str(game.getBackNo()) + ".jpg").convert()

    count = 0
    while count <= 40:
        pygame.time.Clock().tick(FPS)
        gameList.updateEnemyList(human.rect.x, human.rect.y, game.getTime(), game.getRetreat())
        drawBackground(background)
        gameList.updateScreen(game.getScreen())
        count += 1

    game.setRetreat(False)

def enemyCollision(human, remaining, wave, score):

    hit_list = pygame.sprite.spritecollide(human, gameList.getEnemyList(), True)
    
    if human.getSuperHuman() == False and len(hit_list) >= 1:
        human.removeLife()
        
        for enemy in hit_list:
            if human.getLife() < 1:
                pygame.mixer.music.pause()
                pygame.mixer.Sound('sounds/gameover.wav').play()
                gameover(game.getScreen())
                pygame.mixer.music.unpause()
                restart(human, wave, score, remaining)
                game.restart()
                remaining.reset()
                game.resetBackNo()
                game.setPower(None)
                break
            else:
                score.enemyScore()
                remaining.decrease()
                drawHearts(human)
                lifeLost(human)
                
    else:
        for enemy in hit_list:
            remaining.decrease()
            score.enemyScore()
                    
def coinCollision(human, score):
    
    hit_list = pygame.sprite.spritecollide(human, gameList.getCoinList(), True)

    for sprite in hit_list:
        game.decreaseCoinCount()
        pygame.mixer.Sound('sounds/coin.wav').play()
        score.coinScore()
                    

def checkTarget(human):
    # this method is just used to either make the enemies retreat or continue to chase the human
    if human.getTarget() == True:
        
        if human.getSuperHuman() == True:
            
            game.setRetreat(True)
            
        else:
            game.setRetreat(False)
            
        gameList.updateEnemyList(human.rect.x, human.rect.y, game.getTime(), game.getRetreat())

    else:
        if human.getSuperHuman() == True:

            game.setRetreat(True)

        else:
            game.setRetreat(False)
        
    human.update(WIDTH, HEIGHT)

def coinSpawn(current, maximum):
    
    currTime = game.getTime()
    spawnTime = game.getCoinSpawnTime()
    
    if current < maximum and currTime % spawnTime == 0:

        coin = Coin()
        coin.spawn(WIDTH, HEIGHT)
        gameList.addToCoinList(coin)
        game.increaseCoinCount()

def enemySpawn(current, maximum, wave):
    # spawn an enemy based on possibility
    currTime = game.getTime()
    spawnTime = game.getSpawnTime(wave.getWave())
    
    if current < maximum and currTime % spawnTime == 0:
        
        number = random.randrange(0,10)
    
        if number >= 0 and number < 6:
            enemy = Enemy(wave.getWave())
            enemy.spawn(WIDTH, HEIGHT)
            gameList.addToEnemyList(enemy)
            
        elif number >= 6 and number < 8:
            enemy = FastEnemy(wave.getWave())
            enemy.spawn(WIDTH, HEIGHT)
            gameList.addToEnemyList(enemy)
            
        else:
            enemy = PowerEatingEnemy(wave.getWave())
            enemy.spawn(WIDTH, HEIGHT)
            gameList.addToEnemyEatingList(enemy)
            
        game.increaseEnemyCount()
        
def gameover(screen):
    font = pygame.font.Font(None, 60)
    image = font.render("GAME OVER!", True, pygame.Color("red"))
    rect = image.get_rect()
    rect.center = ((HEIGHT/2)-30,WIDTH/2)
    screen.blit(image, rect.center)

    font = pygame.font.Font(None, 40)
    image = font.render("press 'r' to restart", True, pygame.Color("yellow"))
    rect = image.get_rect()
    rect.center = ((HEIGHT/2)-15,(WIDTH/2)+40)
    screen.blit(image, rect.center)
    
    pygame.display.update()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_r:
                    pygame.mixer.stop()
                    pygame.mixer.Sound('sounds/start.wav').play()
                    running = False
            elif event.type == pygame.QUIT:
                running = False
                game.stop()

def titleScreen(screen):
    # this is the title screen which displays the pause menu half way through
    background = pygame.image.load("images/Title.jpg").convert()
    screen.blit(background, [0,0])
    pygame.display.update()

    pygame.mixer.music.load('sounds/MenuSong1.mp3')
    pygame.mixer.music.play(-1)
        
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_s:
                    pause()
                    pygame.mixer.Sound('sounds/start.wav').play()
                    menu = False
            elif event.type == pygame.QUIT:
                menu = False
                game.stop()
                
def pause():
    # this method pauses the game
    background = pygame.image.load("images/pause.jpg").convert()
    game.getScreen().blit(background, [0,0])
    pygame.display.update()
        
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_s:
                    menu = False
            elif event.type == pygame.QUIT:
                menu = False
                game.stop()

def getBackground(background):
    if game.backReset == True:
        # used to reset background to a random map image
        background = pygame.image.load("images/Map" + str(game.getBackNo()) + ".jpg").convert()
        game.backReset = False
    return background
                   
'''
Main Code
'''
def main():
    # initialise pygame
    pygame.init()
    # set the size of the screen
    game.setScreen()
    pygame.display.set_caption("UoN Apocalypse " + VERSION)
        
    titleScreen(game.getScreen())
    background = pygame.image.load("images/Map" + str(game.getBackNo()) + ".jpg").convert()
        
    playSoundtrack()

    human = Human(WIDTH, HEIGHT)
    gameList.addToHumanList(human)
        
    drawHearts(human)
        
    score = Score("yellow")
    gameList.addToSpriteList(score)
        
    remaining = Remaining("white", CURRENT_WAVE)
    gameList.addToSpriteList(remaining)

    wave = Waves("white")
    gameList.addToSpriteList(wave)

    clock = pygame.time.Clock()

    key_map = {
        pygame.K_UP: [human.up, human.down],
        pygame.K_DOWN: [human.down, human.up],
        pygame.K_LEFT: [human.left, human.right],
        pygame.K_RIGHT: [human.right, human.left]
        }
        
    while game.getRunning():
            
        clock.tick(FPS)
        pygame.display.set_caption("UoN Apocalypse " + VERSION + " - {0:.2f} fps".format(clock.get_fps()))
        # check if wave is over
        checkRemaining(remaining, wave, score, human, background)
        chooseRandomPowerUp(wave, human)
        # spawn the sprites in the game
        powerUpSpawn(game.getPowerUpCount(), game.getMaxPowerUpCount(), human)
        coinSpawn(game.getCoinCount(), game.getMaxCoinCount())
        enemySpawn(game.getEnemyCount(), remaining.getMaxEnemy(), wave)
        # check for collisions
        powerUpCollision(gameList.getPowerUpList(), gameList.getEnemyEatingList(), human, score)
        coinCollision(human, score)
        enemyCollision(human, remaining, wave, score)
        eatingEnemyCollision(human, remaining, score)
        # check if the main target is the human sprite
        checkTarget(human)
        # update the extra objects such as the light
        gameList.updateDisposeList(gameList.getEnemyList(), remaining, score)
        updateLights(human)
        gameList.updateDistractionList(gameList.getEnemyList(), game.getTime(), human, game.getRetreat())
        # draw background, sprites and text
        background = getBackground(background)
        drawBackground(background)
        gameList.renderText(remaining, wave, score)
        gameList.getSpriteList().update(human, score, remaining)
        gameList.updateScreen(game.getScreen())
        # increase the counter used for timing
        game.increaseTime()
        # keyboard and other events
        pygameEvents(key_map)


# if this module is executed as a script, run the main function
if __name__ == "__main__":
    main()
