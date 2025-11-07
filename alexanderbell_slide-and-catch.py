'''
Alexander Bell
2D game where the player dodges certain obstacles, and hitting others
Nov-07
'''
import pygame, simpleGE, random


class Introductions(simpleGE.Scene):
    def __init__(self,score=0):
        super().__init__()

        self.score = score 

        self.setImage("white.png")
        self.response = "Quit"

        self.directions = simpleGE.MultiLabel()
        self.directions.textLines = [
        "You are the pilot of a small spacecraft.",
        "Move left and right using the arrow keys.",
        "Avoid asteroids (gray) and hit fuel cells (blue & red)"
        ]
        self.directions.center = (320,200)
        self.directions.size = (550,200)

        self.btnPlay = simpleGE.Button()
        self.btnPlay.text = "Start"
        self.btnPlay.center = (100,400)
        
        self.btnQuit = simpleGE.Button()
        self.btnQuit.text = "Quit"
        self.btnQuit.center = (540,400)

        self.lblScore = simpleGE.Label()
        self.lblScore.center = (320,400)
        self.lblScore.size = (275,50)
        self.lblScore.text = f"Previous Score: {self.score}"
        self.lblScore.bgColor = "black"

        self.sprites = [
        self.directions,
        self.btnPlay,
        self.btnQuit,
        self.lblScore
        ]
    def process(self):
        if self.btnPlay.clicked:
            self.response = "play"
            self.stop()
        if self.btnQuit.clicked:
            self.response = "quit"
            self.stop()


class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()

        self.setImage("black.png")

        self.timer = simpleGE.Timer()
        self.timer.totalTime = 30
        self.lblTime = LblTime() 

        self.numAsteroids = 4
        self.score = 0
        self.lblScore = LblScore()

        self.ship = Ship(self)

        self.fuelcell = FuelCell(self)

        self.asteroids = []
        for x in range(self.numAsteroids):
            self.asteroids.append(Asteroid(self))

        self.sprites = [
        self.lblTime,
        self.lblScore,
        self.ship,
        self.fuelcell
        ] + self.asteroids

    def process(self):
        for asteroid in self.asteroids:
            if asteroid.collidesWith(self.ship):
                asteroid.reset()
                self.score -= 1
                self.lblScore.text = f"SCORE {self.score}"
        if self.fuelcell.collidesWith(self.ship):
                self.fuelcell.reset()
                self.score += 1
                self.lblScore.text = f"SCORE {self.score}"
#                self.timer += 300
        self.lblTime.text = f"Time Left: {self.timer.getTimeLeft():.1f}"
        if self.timer.getTimeLeft() < 0:
            print(f"SCORE: {self.score}")
            self.stop()

class Ship(simpleGE.Sprite):
    def __init__(self,scene):
        super().__init__(scene)
        self.setImage("ship.png")
        self.setSize(50,100)
        self.position = (320,400)
        self.moveSpeed = 7

    def process(self):
        if self.isKeyPressed(pygame.K_LEFT):
            self.x -= self.moveSpeed
        if self.isKeyPressed(pygame.K_RIGHT):
            self.x += self.moveSpeed

class Asteroid(simpleGE.Sprite):
    def __init__(self,scene):
        super().__init__(scene)
        self.setImage("asteroid.png")
        self.setSize(50,50)
        self.minSpeed = 4
        self.maxSpeed = 10
        self.reset()

    def reset(self):
        self.y = 10
        self.x = random.randint (0,self.screenWidth)

        self.dy = random.randint(self.minSpeed, self.maxSpeed)
    def checkBounds(self):
        if self.bottom > self.screenHeight:
            self.reset()



class FuelCell(simpleGE.Sprite):
    def __init__(self,scene):
        super().__init__(scene)
        self.setImage("fuel_cell.png")
        self.setSize(30,30)
        self.minSpeed = 4
        self.maxSpeed = 6
        self.reset()

    def reset(self):
        self.y = 10
        self.x = random.randint (0,self.screenWidth)

        self.dy = random.randint(self.minSpeed, self.maxSpeed)
    def checkBounds(self):
        if self.bottom > self.screenHeight:
            self.reset()
 


class LblScore(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "SCORE: 0"
        self.center = (100,30)


class LblTime(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "TIME LEFT: 30"
        self.center = (500,30)
#        self.size = (200,200)
#        self.bgColor = "red"



def main():
    keepGoing = True
    lastScore = 0
    while keepGoing:
        instructions = Introductions(lastScore)
        instructions.start()

        if instructions.response == "play":
            game = Game()
            game.start()
            lastScore = game.score
        else:
            keepGoing = False
if __name__ == "__main__":
    main()





