import random , pygame , sys
from pygame.locals import *

FPS=15
windowWidth=640
windowHeight=480
cellSize=20
assert windowHeight%cellSize==0 , "Window height must be multipe of cell size"
assert windowWidth%cellSize==0 , "Window width must be multipe of cell size"
cellAlongWidth=int(windowWidth/cellSize)
cellAlongHeight=int(windowHeight/cellSize)

RED=(255 , 0 , 0)
GREEN=(0,255,0)
BLUE=(0,0,255)
BLACK=(0,0,0)
WHITE=(255,255,255)
DARKGREEN=(0,155,0)
head=0

def main():
    global fpsClock , dispSurface , basicFont
    pygame.init()
    fpsClock=pygame.time.Clock()
    dispSurface = pygame.display.set_mode((windowWidth, windowHeight))
    basicFont = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Python By Anshul')
    startScreen()
    while True:
        runGame()
        gameoverScreen()


def runGame():
    startX=random.randint(5,cellAlongWidth-5)
    startY=random.randint(5,cellAlongHeight-5)
    wormBody=[{'x':startX , 'y':startY},{'x':startX-1 , 'y':startY-1},{'x':startX-2 , 'y':startY-2}]
    currentDirection='RIGHT'
    appleLocation=getRandomLocation()
    while True:
        #CHECKING FOR THE KEY PRESSED
        for event in pygame.event.get():
            if event.type==QUIT:
                terminate()
            elif event.type==KEYDOWN:
                if( event.key==K_LEFT or event.key==K_a) and currentDirection!='RIGHT':
                    currentDirection='LEFT'
                elif ( event.key==K_RIGHT or event.key==K_d) and currentDirection!='LEFT':
                    currentDirection='RIGHT'
                elif ( event.key==K_UP or event.key==K_w) and currentDirection!='DOWN':
                    currentDirection='UP'
                elif ( event.key==K_DOWN or event.key==K_s) and currentDirection!='UP':
                    currentDirection='DOWN'
                elif ( event.key==K_ESCAPE):
                    terminate()
        #CHECKING FOR COLLISION DETECTION WITH WALLS
        if wormBody[head]['x']==-1 or wormBody[head]['x']==cellAlongWidth or wormBody[head]['y']==-1 or wormBody[head]['y']==cellAlongHeight:
            return
        #CHECKING FOR COLLISION DETECTION WITH ITSELF
        for wormSegment in wormBody[1:]:
            if wormSegment['x']==wormBody[head]['x'] and wormSegment['y']==wormBody[head]['y']:
                return
        #CHECKING COLISION WITH APPLE
        if currentDirection == 'UP':
            newHead = {'x': wormBody[head]['x'], 'y': wormBody[head]['y'] - 1}
        elif currentDirection == 'DOWN':
            newHead = {'x': wormBody[head]['x'], 'y': wormBody[head]['y'] + 1}
        elif currentDirection == 'RIGHT':
            newHead = {'x': wormBody[head]['x'] + 1, 'y': wormBody[head]['y']}
        elif currentDirection == 'LEFT':
            newHead = {'x': wormBody[head]['x'] - 1, 'y': wormBody[head]['y']}

        if wormBody[head]['x']==appleLocation['x'] and wormBody[head]['y']==appleLocation['y']:
            appleLocation=getRandomLocation()
        else:
            del wormBody[-1]

        wormBody.insert(0,newHead)

        dispSurface.fill(WHITE)
        #drawGrid()
        drawWorm(wormBody)
        drawApple(appleLocation)
        drawScore(len(wormBody)-3)
        pygame.display.update()
        fpsClock.tick(FPS)

def drawMessage():
    message=basicFont.render('Press a key to play!',True,BLUE)
    messageRect=message.get_rect()
    messageRect.center=(windowWidth/2 , windowHeight-20)
    dispSurface.blit(message,messageRect)

def checkPressKey():
    if len(pygame.event.get(QUIT))>0:
        terminate()
    keyupevent=pygame.event.get(KEYUP)
    if len(keyupevent)== 0:
        return None
    if keyupevent[0] == K_ESCAPE:
        terminate()
    return keyupevent[0].key

def startScreen():
    titleFont=pygame.font.Font('freesansbold.ttf',50)
    titleMessasge1=titleFont.render('Python\'s Revenge',True,RED)
    titleMessasge2 = titleFont.render('Python\'s Revenge', True,GREEN)
    degree1=0
    degree2=0
    while True:
        dispSurface.fill(BLACK)
        rotatedSurface1=pygame.transform.rotate(titleMessasge1,degree1)
        rotatedRect1=rotatedSurface1.get_rect()
        rotatedRect1.center=(windowWidth/2 , 100)
        dispSurface.blit(rotatedSurface1,rotatedRect1)

        rotatedSurface2 = pygame.transform.rotate(titleMessasge2, degree2)
        rotatedRect2 = rotatedSurface2.get_rect()
        rotatedRect2.center=(windowWidth/2 , 300)
        dispSurface.blit(rotatedSurface2, rotatedRect2)

        drawMessage()

        if checkPressKey():
            pygame.event.get()
            return
        pygame.display.update()
        fpsClock.tick(FPS)
        degree1+=3
        degree2+=5

def terminate():
    pygame.quit()
    sys.exit()

def getRandomLocation():
    return {'x':random.randint(0,cellAlongWidth-1) , 'y':random.randint(0,cellAlongHeight-1)}

def gameoverScreen():
    gameoverFont=pygame.font.Font('freesansbold.ttf',50)
    gameoverMessage=gameoverFont.render('GAME OVER!!',True,RED)
    gameoverRect=gameoverMessage.get_rect()
    gameoverRect.center=(windowWidth/2,windowHeight/2)
    dispSurface.blit(gameoverMessage,gameoverRect)

    drawMessage()

    pygame.display.update()

    pygame.time.wait(500)

    checkPressKey()

    while True:
        if checkPressKey():
            pygame.event.get()
            return

def drawScore(score):
    scoreMessage=basicFont.render('Score: %s'%(score) , True ,BLACK)
    scoreRect=scoreMessage.get_rect()
    scoreRect.topleft=(windowWidth-120,10)
    dispSurface.blit(scoreMessage,scoreRect)

def drawWorm(body):
    for coord in body:
        x=coord['x']*cellSize
        y=coord['y']*cellSize
        wormSegmentRect=pygame.Rect(x,y,cellSize,cellSize)
        pygame.draw.rect(dispSurface,GREEN,wormSegmentRect)
        wormInnerSegmentRect=pygame.Rect(x+4 , y+4 , cellSize-8,cellSize-8)
        pygame.draw.rect(dispSurface,DARKGREEN,wormInnerSegmentRect)

def drawApple(coord):
    x=coord['x']*cellSize
    y=coord['y']*cellSize
    appleRect=pygame.Rect(x,y,cellSize,cellSize)
    pygame.draw.rect(dispSurface,RED,appleRect)

#def drawGrid():
if __name__== '__main__':
    main()


















