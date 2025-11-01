'''
Alexander Bell
2D game where the player dodges certain obstacles, and hitting others
Oct-31
'''
import pygame, simpleGE, random


class Introductions(simpleGE.Scene):
    def __init__(self):
        super().__init__()

        self.setImage("white.png")
        self.response = "Quit"

        self.directions = simpleGE.MultiLabel()
        self.directions.textLines = [
        "You are the pilot of a small spacecraft.",
        "Move left and right using the arrow keys.",
        "Avoid asteroids (gray) and hit fuel cells (green)"
        ]
        self.directions.center = (320,200)
        self.directions.size = (500,300)

        self.btnPlay = simpleGE.Button()
        self.btnPlay.text = "Start"
        self.btnPlay.center = (100,400)
        
        self.btnQuit = simpleGE.Button()
        self.btnQuit.text = "Quit"
        self.btnQuit.center = (540,400)

        self.sprites = [
        self.directions,
        self.btnPlay,
        self.btnQuit
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
        self.timer.totalTime = 15
        self.lblTime = LblTime()

        self.numAsteroids = 3
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
        self.lblTime.text = f"TIME LEFT: {self.timer.getTimeLeft()}"
        if self.timer.getTimeLeft() < 0:
            print(f"SCORE: {self.score}")
            self.stop()

class Ship(simpleGE.Sprite):
    def __init__(self,scene):
        super().__init__(scene)
        self.setImage("ship.jpg")
        self.setSize(50,50)
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
        self.setImage("asteroid.jpg")
        self.setSize(25,25)
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
        self.setImage("fuelcell.jpg")
        self.setSize(20,20)
        self.minSpeed = 8
        self.maxSpeed = 15
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
        self.text = "TIME LEFT: 15"
        self.center = (500,30)



def main():
    keepGoing = True
    score = 0
    while keepGoing:
        instructions = Introductions()
        instructions.start()

        if instructions.response == "play":
            game = Game()
            game.start()
        else:
            keepGoing = False
if __name__ == "__main__":
    main()





