from cmu_graphics import *
from objects import *
import math

# The Angry Birds LOGO image was taken from the Angry Birds WIKI:
# Link: https://logos.fandom.com/wiki/Angry_Birds/Logo_Variations

# All other images including birds, pigs, home button, background, stars, and blocks were taken from github user "estevaofon"
# Link:https://github.com/estevaofon/angry-birds-python/tree/master/resources/images
# No Artwork used in this project is Original


def distance(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


def drawGrid(app):
    rows = app.height//app.tile
    cols = app.width//app.tile
    for row in range(rows):
        y = row * app.tile    
        drawLine(0, y, app.width, y, lineWidth = 1, opacity = 10)
    for col in range(cols):
        x = col * app.tile
        drawLine(x, 0, x, app.height, lineWidth = 1, opacity = 10)


def loadLevel(app, level):
    #------------------------------------------------------------------------------------------------------
    if level == 1:
        #-----------------------------------------default
        app.screen = 'level1'
        app.homeButtonX = 50
        app.homeButtonY = 50  
        app.won = False
        app.loss = False
        app.drag = False
        app.fly = False
        app.score = 0
        app.oneStar = 800
        app.twoStar = 1100
        app.threeStar = 1300

        #----------------------------------sling
        app.slingX = 200
        app.slingY = 600
        app.slingMax = 150
        app.initBirdX = app.slingX - 10
        app.initBirdY = app.slingY - 75

        #--------------------------lists
        app.birdSit = []
        app.birdThrow = []
        app.pig = []
        app.object = []

        yellow1 = Bird(app.initBirdX, app.initBirdY, 'yellow')
        red2 = Bird(app.initBirdX - 50, app.floor - 20, 'red')
        red3 = Bird(app.initBirdX - 100, app.floor - 20, 'red')
        app.birdSit.append(yellow1)
        app.birdSit.append(red2)
        app.birdSit.append(red3)

        pig1 = Object(app, 'pig', 600, 300, 0, 'flesh')
        pig2 = Object(app, 'pig', 800, 400, 0, 'flesh')
        pig3 = Object(app, 'pig', 1000, 500, 0, 'flesh')
        app.pig.append(pig1)
        app.pig.append(pig2)
        app.pig.append(pig3)

        object1 = Object(app, 'box', 1000, 600, 0, 'wood')
        object2 = Object(app, 'box', 800, 600, 0, 'wood')
        object3 = Object(app, 'box', 800, 500, 0, 'wood')
        object4 = Object(app, 'box', 600, 600, 0, 'stone')
        object5 = Object(app, 'box', 600, 500, 0, 'stone')
        object6 = Object(app, 'box', 600, 400, 0, 'wood')
        
        app.object.append(object1)
        app.object.append(object2)
        app.object.append(object3)
        app.object.append(object4)
        app.object.append(object5)
        app.object.append(object6)
    #------------------------------------------------------------------------------------------------------
    if level == 2:
        #-----------------------------------------default
        app.screen = 'level2'
        app.homeButtonX = 50
        app.homeButtonY = 50  
        app.won = False
        app.loss = False
        app.drag = False
        app.fly = False
        app.score = 0
        app.oneStar = 600
        app.twoStar = 1000
        app.threeStar = 700

        #----------------------------------sling
        app.slingX = 200
        app.slingY = 600
        app.slingMax = 150
        app.initBirdX = app.slingX - 10
        app.initBirdY = app.slingY - 75

        #--------------------------lists
        app.birdSit = []
        app.birdThrow = []
        app.pig = []
        app.object = []

        yellow1 = Bird(app.initBirdX, app.initBirdY, 'yellow')
        red2 = Bird(app.initBirdX - 50, app.floor - 20, 'red')
        red3 = Bird(app.initBirdX - 100, app.floor - 20, 'red')
        app.birdSit.append(yellow1)
        app.birdSit.append(red2)
        app.birdSit.append(red3)

        pig1 = Object(app, 'pig', 650, 100, 0, 'flesh')
        pig2 = Object(app, 'pig', 1200, 100, 0, 'flesh')
        app.pig.append(pig1)
        app.pig.append(pig2)

        object1 = Object(app, 'column', 400, 200, 0, 'wood')
        object2 = Object(app, 'column', 1000, 200, 0, 'stone')
        app.object.append(object1)
        app.object.append(object2)
    #------------------------------------------------------------------------------------------------------
    if level == 3:
        #-----------------------------------------default
        app.screen = 'level3'
        app.homeButtonX = 50
        app.homeButtonY = 50  
        app.won = False
        app.loss = False
        app.drag = False
        app.fly = False
        app.score = 0
        app.oneStar = 600
        app.twoStar = 700
        app.threeStar = 800

        #----------------------------------sling
        app.slingX = 200
        app.slingY = 600
        app.slingMax = 150
        app.initBirdX = app.slingX - 10
        app.initBirdY = app.slingY - 75

        #--------------------------lists
        app.birdSit = []
        app.birdThrow = []
        app.pig = []
        app.object = []

        red1 = Bird(app.initBirdX, app.initBirdY, 'red')
        red2 = Bird(app.initBirdX - 50, app.floor - 20, 'red')
        app.birdSit.append(red1)
        app.birdSit.append(red2)

        pig1 = Object(app, 'pig', 700, 500, 0, 'flesh')
        pig2 = Object(app, 'pig', 1000, 500, 0, 'flesh')
        app.pig.append(pig1)
        app.pig.append(pig2)

        object1 = Object(app, 'wheel', 500, 500, 0, 'wood')
        app.object.append(object1)
    #------------------------------------------------------------------------------------------------------
    if level == 'builder':
        #-----------------------------------------default
        app.screen = 'builder'
        app.homeButtonX = 50
        app.homeButtonY = 50  
        app.won = False
        app.loss = False
        app.drag = False
        app.fly = False
        app.score = 0
        app.playBuilder = False
        app.selecting = 'main'
        app.selectList = []
        app.draggingItem = False
        app.draggedItem = None
        app.objectNum = 1
        app.objectDict = {}
        app.mouseX = 0
        app.mouseY = 0

        #----------------------------------sling
        app.slingX = 200
        app.slingY = 600
        app.slingMax = 150
        app.initBirdX = app.slingX - 10
        app.initBirdY = app.slingY - 75

        #--------------------------lists
        app.birdSit = []
        app.birdThrow = []
        app.pig = []
        app.object = []


def onAppStart(app):
    #Default
    app.width = 1500
    app.height = 900
    app.tile = 50
    app.floor = 700
    app.gravity = 9.81
    app.stepsPerSecond = 120
    app.screen = 'home'

    #Level Button Coordinates
    app.lvlButtonWidth = app.width/4
    app.lvlButtonHeight = app.height/4
    app.lvl1ButtonX = app.width/2
    app.lvl1ButtonY = 200
    app.lvl2ButtonX = app.width/2
    app.lvl2ButtonY = 450
    app.lvl3ButtonX = app.width/2
    app.lvl3ButtonY = 700
    app.buildButtonX = app.width/2 + app.width/4 + 50
    app.buildButtonY = 325

    app.icon1 = (app.width - 75, app.height - 75)
    app.icon2 = (app.width - 225, app.height - 75)
    app.icon3 = (app.width - 375, app.height - 75)
    app.icon4 = (app.width - 525, app.height - 75)
    app.undoIcon = (app.width - 650, app.height - 75)


def redrawAll(app):
    if app.screen == 'home':
        #Background
        drawImage('images\\background.png', 0, 0, width = app.width, height = app.height)

        #Title
        drawImage('images\\Title.png', 275, 275, width = 450, height = 200, align = 'center')
        drawLabel('Controls:', 275, 375, size = 40, bold = True, align = 'center')
        drawLabel('Space - Activate Skill', 275, 415, size = 40, bold = True, align = 'center')

        drawRect(app.lvl1ButtonX, app.lvl1ButtonY, app.lvlButtonWidth, app.lvlButtonHeight, align = 'center', fill = 'gray', opacity = 65)
        drawLabel('Level 1', app.lvl1ButtonX, app.lvl1ButtonY, size = 50)
        drawRect(app.lvl2ButtonX, app.lvl2ButtonY, app.lvlButtonWidth, app.lvlButtonHeight, align = 'center', fill = 'gray', opacity = 65)
        drawLabel('Level 2', app.lvl2ButtonX, app.lvl2ButtonY, size = 50)
        drawRect(app.lvl3ButtonX, app.lvl3ButtonY, app.lvlButtonWidth, app.lvlButtonHeight, align = 'center', fill = 'gray', opacity = 65)
        drawLabel('Level 3', app.lvl3ButtonX, app.lvl3ButtonY, size = 50)
        drawRect(app.buildButtonX, app.buildButtonY, app.lvlButtonWidth, app.lvlButtonHeight, align = 'center', fill = 'gray', opacity = 65)
        drawLabel('Builder Mode', app.buildButtonX, app.buildButtonY, size = 50)
        
    elif app.screen[:5] == 'level' or app.screen == 'builder':
        #Home Button
        drawImage('images\\home_button.png', app.homeButtonX, app.homeButtonY, align = 'center', width = 60, height = 60)

        #Score
        if app.score < 0:
            score = 0
        else:
            score = app.score
        drawLabel(f'Score: {score}', app.width - 150, 50, size = 30, align = 'center')

        #Floor
        drawLine(0, app.floor, app.width, app.floor)

        #Sling
        drawImage('images\\sling.png', app.slingX, app.slingY, align = 'center')
        if app.drag and not app.loss and not app.won: #-------------------------------------------Note: Fix buggy slingshot
            drawLine(app.initBirdX, app.initBirdY, app.birdSit[0].x, app.birdSit[0].y, lineWidth = 20)
            #Trajectory
            for point in app.birdSit[0].drawTrajectory(app, 1/2)[0:-1]:
                drawCircle(point[0], point[1], 5, fill = 'blue')

        #Birds
        for bird in app.birdThrow:
            drawImage(bird.img, bird.x, bird.y, align = 'center')
        for bird in app.birdSit:
            drawImage(bird.img, bird.x, bird.y, align = 'center')

        #Objects
        for pig in app.pig:
            drawImage(pig.img, pig.x, pig.y, align = 'center')  
        for object in app.object:
            drawImage(object.img, object.x, object.y, rotateAngle = object.angle, align = 'center')  

        #Display Game Over Message If Loss
        if app.loss:
            drawLabel('GAME OVER!', app.width//2, app.height//2, size = 50)
        if app.won:
            drawLabel('YOU WIN!', app.width//2, app.height//2 - 250, size = 50)
            if app.screen[:5] == 'level':
                if app.score >= app.threeStar:
                    img = 'images\\three_star.png'
                    drawImage(img, app.width/2 - 315, app.height//2 - 175)
                elif app.score >= app.twoStar:
                    img = 'images\\two_star.png'
                    drawImage(img, app.width/2 - 315, app.height//2 - 175)
                elif app.score >= app.oneStar:
                    img = 'images\\one_star.png'
                    drawImage(img, app.width/2 - 315, app.height//2 - 175)

        
        #Grid
        drawGrid(app)

        #Builder Mode
        if app.screen == 'builder' and app.playBuilder == False:
            drawRect(*app.icon1, 125, 125, fill = 'lightBlue', align = 'center')
            drawRect(*app.icon2, 125, 125, fill = 'lightBlue', align = 'center')
            drawRect(*app.icon3, 125, 125, fill = 'lightBlue', align = 'center')
            drawRect(*app.icon4, 125, 125, fill = 'lightBlue', align = 'center')

            drawImage('images\\back_button.png', *app.undoIcon, width = 60, height = 60, align = 'center')

            drawCircle(app.width - 500, app.height - 170, 20, fill = 'red', align = 'center')
            drawLabel('RESET', app.width - 420, app.height - 170, size = 20, bold = True)
            drawCircle(app.width - 250, app.height - 170, 20, fill = 'green', align = 'center')
            drawLabel('PLAY', app.width - 170, app.height - 170, size = 20, bold = True)

            if app.selecting == 'main':
                birds = 'images\\red-bird.png'
                pigs = 'images\\pig_failed.png'
                blocks = 'images\\wood_box.png'
                drawImage(birds, *app.icon1, width = 125, height = 125, align = 'center')
                drawImage(pigs, *app.icon2, width = 125, height = 125, align = 'center')
                drawImage(blocks, *app.icon3, width = 100, height = 100, align = 'center')

            elif app.selecting == 'birds':
                bird1 = 'images\\red-bird.png'
                bird2 = 'images\\yellow-bird.png'
                drawImage(bird1, *app.icon1, width = 125, height = 125, align = 'center')
                drawImage(bird2, *app.icon2, width = 100, height = 80, align = 'center')
                if app.birdSit:
                    red = 0
                    yellow = 0
                    for bird in app.birdSit:
                        if bird.type == 'red':
                            red += 1
                        elif bird.type == 'yellow':
                            yellow += 1
                    if red > 0:
                        drawLabel(f'{red}x Red Birds', 170, 785, size = 20, bold = True)
                    if yellow > 0:
                        drawLabel(f'{yellow}x Yellow Birds', 170, 815, size = 20, bold = True)
                    drawLabel('RESET', 170, 750, size = 20, bold = True)
                    drawCircle(100, 750, 15, fill = 'red')

            elif app.selecting == 'pigs':
                pig1 = 'images\\pig.png'
                drawImage(pig1, *app.icon1, width = 100, height = 100, align = 'center')

            elif app.selecting == 'blocks':
                box = 'images\\wood_box.png'
                wheel = 'images\\wood_wheel.png'
                column = 'images\\wood_column.png'
                drawImage(box, *app.icon1, width = 100, height = 100, align = 'center')
                drawImage(wheel, *app.icon2, width = 100, height = 100, align = 'center')
                drawImage(column, *app.icon3, width = 10, height = 100, align = 'center')

            elif app.selecting == 'boxes':
                wood = 'images\\wood_box.png'
                stone = 'images\\stone_box.png'
                drawImage(wood, *app.icon1, width = 100, height = 100, align = 'center')
                drawImage(stone, *app.icon2, width = 100, height = 100, align = 'center')

            elif app.selecting == 'wheels':
                wood = 'images\\wood_wheel.png'
                stone = 'images\\stone_wheel.png'
                drawImage(wood, *app.icon1, width = 100, height = 100, align = 'center')
                drawImage(stone, *app.icon2, width = 100, height = 100, align = 'center')

            elif app.selecting == 'columns':
                wood = 'images\\wood_column.png'
                stone = 'images\\stone_column.png'
                drawImage(wood, *app.icon1, width = 10, height = 100, align = 'center')
                drawImage(stone, *app.icon2, width = 10, height = 100, align = 'center')
            
            if app.draggingItem:
                if app.draggedItem == 'pig1':
                    img = 'images\\pig.png'
                elif app.draggedItem == 'wood_box':
                    img = 'images\\wood_box.png'
                elif app.draggedItem == 'stone_box':
                    img = 'images\\stone_box.png'
                elif app.draggedItem == 'wood_wheel':
                    img = 'images\\wood_wheel.png'
                elif app.draggedItem == 'stone_wheel':
                    img = 'images\\stone_wheel.png'
                elif app.draggedItem == 'wood_column':
                    img = 'images\\wood_column.png'
                elif app.draggedItem == 'stone_column':
                    img = 'images\\stone_column.png'
                drawImage(img, app.mouseX, app.mouseY, opacity = 75, align = 'center')


def onMousePress(app, mouseX, mouseY):
    if app.screen == 'home':
        if (app.lvl1ButtonX - app.lvlButtonWidth/2 < mouseX < app.lvl1ButtonX + app.lvlButtonWidth/2 and
            app.lvl1ButtonY - app.lvlButtonHeight/2 < mouseY < app.lvl1ButtonY + app.lvlButtonHeight/2):
            loadLevel(app, 1)
        elif (app.lvl2ButtonX - app.lvlButtonWidth/2 < mouseX < app.lvl2ButtonX + app.lvlButtonWidth/2 and
            app.lvl2ButtonY - app.lvlButtonHeight/2 < mouseY < app.lvl2ButtonY + app.lvlButtonHeight/2):
            loadLevel(app, 2)
        elif (app.lvl3ButtonX - app.lvlButtonWidth/2 < mouseX < app.lvl3ButtonX + app.lvlButtonWidth/2 and
            app.lvl3ButtonY - app.lvlButtonHeight/2 < mouseY < app.lvl3ButtonY + app.lvlButtonHeight/2):
            loadLevel(app, 3)
        elif (app.buildButtonX - app.lvlButtonWidth/2 < mouseX < app.buildButtonX + app.lvlButtonWidth/2 and
            app.buildButtonY - app.lvlButtonHeight/2 < mouseY < app.buildButtonY + app.lvlButtonHeight/2):
            loadLevel(app, 'builder')
    
    elif app.screen[:5] == 'level':
        if distance(app.initBirdX, app.initBirdY, mouseX, mouseY) < 50 and not app.fly:
            app.drag = True
        if distance(mouseX, mouseY, app.homeButtonX, app.homeButtonY) < 30:
            app.screen = 'home'

    elif app.screen == 'builder':
        if not app.playBuilder:

            app.mouseX, app.mouseY = mouseX, mouseY

            if distance(mouseX, mouseY, app.width - 500, app.height - 170) < 20:
                app.pig = []
                app.object = []
            
            if distance(mouseX, mouseY, app.width - 250, app.height - 170) < 20:
                app.playBuilder = True

            if distance(mouseX, mouseY, *app.undoIcon) <= 30 and app.selectList:
                app.selecting = f'{app.selectList.pop()}'

            if app.selecting == 'main':
                if abs(mouseX - app.icon1[0]) <= 125/2 and abs(mouseY - app.icon1[1]) <= 125/2:
                    app.selectList.append(app.selecting)
                    app.selecting = 'birds'
                elif abs(mouseX - app.icon2[0]) <= 125/2 and abs(mouseY - app.icon2[1]) <= 125/2:
                    app.selectList.append(app.selecting)
                    app.selecting = 'pigs'
                elif abs(mouseX - app.icon3[0]) <= 125/2 and abs(mouseY - app.icon3[1]) <= 125/2:
                    app.selectList.append(app.selecting)
                    app.selecting = 'blocks'

            elif app.selecting == 'blocks':
                if abs(mouseX - app.icon1[0]) <= 125/2 and abs(mouseY - app.icon1[1]) <= 125/2:
                    app.selectList.append(app.selecting)
                    app.selecting = 'boxes'
                elif abs(mouseX - app.icon2[0]) <= 125/2 and abs(mouseY - app.icon2[1]) <= 125/2:
                    app.selectList.append(app.selecting)
                    app.selecting = 'wheels'
                elif abs(mouseX - app.icon3[0]) <= 125/2 and abs(mouseY - app.icon3[1]) <= 125/2:
                    app.selectList.append(app.selecting)
                    app.selecting = 'columns'

            elif app.selecting == 'birds':
                    if distance(mouseX, mouseY, 100, 750) <= 15:
                        app.birdSit = []
                    if abs(mouseX - app.icon1[0]) <= 125/2 and abs(mouseY - app.icon1[1]) <= 125/2:
                        if len(app.birdSit) == 0:
                            locals()[f'bird{app.objectNum}'] = Bird(app.initBirdX, app.initBirdY, 'red')
                        else:
                            locals()[f'bird{app.objectNum}'] = Bird(app.initBirdX - 50 * len(app.birdSit), app.floor - 20, 'red')
                        app.objectDict[app.objectNum] = locals()[f'bird{app.objectNum}']
                        app.birdSit.append(app.objectDict[app.objectNum])
                        app.objectNum += 1
                    elif abs(mouseX - app.icon2[0]) <= 125/2 and abs(mouseY - app.icon2[1]) <= 125/2:
                        if len(app.birdSit) == 0:
                            locals()[f'bird{app.objectNum}'] = Bird(app.initBirdX, app.initBirdY, 'yellow')
                        else:
                            locals()[f'bird{app.objectNum}'] = Bird(app.initBirdX - 50 * len(app.birdSit), app.floor - 20, 'yellow')
                        app.objectDict[app.objectNum] = locals()[f'bird{app.objectNum}']
                        app.birdSit.append(app.objectDict[app.objectNum])
                        app.objectNum += 1
                    
            elif app.selecting == 'pigs':
                if abs(mouseX - app.icon1[0]) <= 125/2 and abs(mouseY - app.icon1[1]) <= 125/2:
                    app.draggedItem = 'pig1'
                    app.draggingItem = True

            elif app.selecting == 'boxes':
                if abs(mouseX - app.icon1[0]) <= 125/2 and abs(mouseY - app.icon1[1]) <= 125/2:
                    app.draggedItem = 'wood_box'
                    app.draggingItem = True
                elif abs(mouseX - app.icon2[0]) <= 125/2 and abs(mouseY - app.icon1[1]) <= 125/2:
                    app.draggedItem = 'stone_box'
                    app.draggingItem = True

            elif app.selecting == 'wheels':
                if abs(mouseX - app.icon1[0]) <= 125/2 and abs(mouseY - app.icon1[1]) <= 125/2:
                    app.draggedItem = 'wood_wheel'
                    app.draggingItem = True
                elif abs(mouseX - app.icon2[0]) <= 125/2 and abs(mouseY - app.icon1[1]) <= 125/2:
                    app.draggedItem = 'stone_wheel'
                    app.draggingItem = True
        
            elif app.selecting == 'columns':
                if abs(mouseX - app.icon1[0]) <= 125/2 and abs(mouseY - app.icon1[1]) <= 125/2:
                    app.draggedItem = 'wood_column'
                    app.draggingItem = True
                elif abs(mouseX - app.icon2[0]) <= 125/2 and abs(mouseY - app.icon1[1]) <= 125/2:
                    app.draggedItem = 'stone_column'
                    app.draggingItem = True

        else:
            if distance(app.initBirdX, app.initBirdY, mouseX, mouseY) < 50 and not app.fly:
                app.drag = True
    
    if distance(mouseX, mouseY, app.homeButtonX, app.homeButtonY) <= 30:
        app.screen = 'home'
        app.playBuilder = False
        app.selectList = []
        app.selecting = 'main'
        app.draggingItem = False
        app.dragedItem = None
        app.objectNum = 0
        app.objectDict = {}

            
def onMouseDrag(app, mouseX, mouseY):
    if app.screen[:5] == 'level':
        if app.drag and not app.loss and not app.won:
            app.trajList = []
            if distance(app.initBirdX, app.initBirdY, mouseX, mouseY) <= app.slingMax:
                app.birdSit[0].x = mouseX
                app.birdSit[0].y = mouseY
            else:
                try:
                    app.angle = math.tanh(-(app.initBirdY - mouseY)/-(app.initBirdX - mouseX))
                    app.birdSit[0].x = app.initBirdX  - app.slingMax * math.cos(app.angle)
                    app.birdSit[0].y = app.initBirdY  - app.slingMax * math.sin(app.angle)
                except Exception:
                    pass
    
    if app.screen == 'builder':
        if not app.playBuilder:
            app.mouseX, app.mouseY = mouseX, mouseY

        else:
            if app.drag and not app.loss and not app.won:
                app.trajList = []
                if distance(app.initBirdX, app.initBirdY, mouseX, mouseY) <= app.slingMax:
                    app.birdSit[0].x = mouseX
                    app.birdSit[0].y = mouseY
                else:
                    try:
                        app.angle = math.tanh(-(app.initBirdY - mouseY)/-(app.initBirdX - mouseX))
                        app.birdSit[0].x = app.initBirdX  - app.slingMax * math.cos(app.angle)
                        app.birdSit[0].y = app.initBirdY  - app.slingMax * math.sin(app.angle)
                    except Exception:
                        pass


def onMouseRelease(app, mouseX, mouseY):
    if app.screen == 'home':
        pass
    
    elif app.screen[:5] == 'level':
        if app.drag and not app.loss and not app.won:
            app.drag = False
            app.fly = True
            app.trajList = app.birdSit[0].drawTrajectory(app, 1/3)
            if app.birdThrow:
                app.birdThrow.pop()
            app.birdThrow.append(app.birdSit.pop(0))
            app.score -= 200

    elif app.screen == 'builder':
        if not app.playBuilder:
            if app.draggingItem:
                if app.draggedItem == 'pig1':
                    if mouseY < app.floor - 30:
                        locals()[f'object{app.objectNum}'] = Object(app, 'pig', app.mouseX, app.mouseY, 0, 'flesh')
                        app.objectDict[app.objectNum] = locals()[f'object{app.objectNum}']
                        app.pig.append(app.objectDict[app.objectNum])
                        app.objectNum += 1
                elif app.draggedItem == 'wood_box':
                    if mouseY < app.floor - getImageSize('images\\wood_box.png')[1]/2:
                        locals()[f'object{app.objectNum}'] = Object(app, 'box', app.mouseX, app.mouseY, 0, 'wood')
                        app.objectDict[app.objectNum] = locals()[f'object{app.objectNum}']
                        app.object.append(app.objectDict[app.objectNum])
                        app.objectNum += 1
                elif app.draggedItem == 'stone_box':
                    if mouseY < app.floor - getImageSize('images\\stone_box.png')[1]/2:
                        locals()[f'object{app.objectNum}'] = Object(app, 'box', app.mouseX, app.mouseY, 0, 'stone')
                        app.objectDict[app.objectNum] = locals()[f'object{app.objectNum}']
                        app.object.append(app.objectDict[app.objectNum])
                        app.objectNum += 1
                elif app.draggedItem == 'wood_wheel':
                    if mouseY < app.floor - getImageSize('images\\wood_wheel.png')[1]/2:
                        locals()[f'object{app.objectNum}'] = Object(app, 'wheel', app.mouseX, app.mouseY, 0, 'wood')
                        app.objectDict[app.objectNum] = locals()[f'object{app.objectNum}']
                        app.object.append(app.objectDict[app.objectNum])
                        app.objectNum += 1
                elif app.draggedItem == 'stone_wheel':
                    if mouseY < app.floor - getImageSize('images\\stone_wheel.png')[1]/2:
                        locals()[f'object{app.objectNum}'] = Object(app, 'wheel', app.mouseX, app.mouseY, 0, 'stone')
                        app.objectDict[app.objectNum] = locals()[f'object{app.objectNum}']
                        app.object.append(app.objectDict[app.objectNum])
                        app.objectNum += 1
                elif app.draggedItem == 'wood_column':
                    if mouseY < app.floor - getImageSize('images\\wood_column.png')[1]/2:
                        locals()[f'object{app.objectNum}'] = Object(app, 'column', app.mouseX, app.mouseY, 0, 'wood')
                        app.objectDict[app.objectNum] = locals()[f'object{app.objectNum}']
                        app.object.append(app.objectDict[app.objectNum])
                        app.objectNum += 1
                elif app.draggedItem == 'stone_column':
                    if mouseY < app.floor - getImageSize('images\\stone_column.png')[1]/2:
                        locals()[f'object{app.objectNum}'] = Object(app, 'column', app.mouseX, app.mouseY, 0, 'stone')
                        app.objectDict[app.objectNum] = locals()[f'object{app.objectNum}']
                        app.object.append(app.objectDict[app.objectNum])
                        app.objectNum += 1
            app.draggingItem = False
            app.draggedItem = None

        else:
            if app.drag and not app.loss and not app.won:
                app.drag = False
                app.fly = True
                app.trajList = app.birdSit[0].drawTrajectory(app, 1/3)
                app.birdThrow.append(app.birdSit.pop(0))
                app.score -= 200


def onKeyPress(app, key):
    if key == 'space' and app.birdThrow:
        if app.fly and app.birdThrow[-1].type == 'yellow':
            app.birdThrow[-1].speedUpTraj(app)
            app.birdThrow[-1].abilityUsed = True


def onStep(app):
    if app.screen == 'home':
        pass

    elif app.screen[:5] == 'level' or (app.screen == 'builder' and app.playBuilder):
        #Game Over/ Game Won
        count = 0
        if not app.pig:
            app.won = True
            app.birdThrow = []
        elif not app.birdSit and not app.fly and app.pig:
            for pig in app.pig:
                if pig.velocityY > 0:
                    count += 1
            if app.object:
                for object in app.object:
                    if object.velocityX != 0:
                        count += 1
                    if object.isRotating:
                        count += 1
            if count == 0:
                app.loss = True
                app.birdThrow = []
                
        #Bird Flying
        if app.fly:
            if app.birdThrow:
                app.birdThrow[-1].fly(app)
            else:
                shiftBirds(app)

        #Collisions Bird x Pig/Object
        for pig in app.pig:
            if app.birdThrow:
                pig.collision(app, app.birdThrow[-1])
        for object in app.object:
            if app.birdThrow:
                object.collision(app, app.birdThrow[-1])
                
        #Collisions Pigs X Objects
        if app.pig and app.object:
            for pig in app.pig:
                count = 0
                for object in app.object:
                    if pig.collision(app, object):
                        count += 1
                if count < 1:   
                    pig.grounded = False
                    pig.floor = app.floor
        
        #Collisions Objects X Objects
        if len(app.object) > 1:
            for object1 in app.object:
                count = 0
                for object2 in app.object:
                    if object1 != object2:
                        if object1.collision(app, object2) and (object1.y < object2.y):
                            count += 1
                if count < 1:
                    object1.grounded = False
                    object1.floor = app.floor
        else: 
            for object1 in app.object:
                object1.grounded = False
                object1.floor = app.floor

        #Rotation And Moving Animation
        for object in app.object:
            if object.isRotating:
                object.rotate(object.rotateInfo[0], object.rotateInfo[1])
            object.move(1/3)
            if object.velocityX == 0 and object.velocityY/2 == 0:
                object.moving = False
                
        #Gravity And Other Passives
        if app.pig:
            for pig in app.pig:
                pig.obeyGravity(app, 1/3)
        if app.object:
            for object in app.object:
                object.obeyGravity(app, 1/3)
                object.spinWheel()

            
def main():
    runApp()
main()