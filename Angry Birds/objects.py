from cmu_graphics import *
import math

def shiftBirds(app):
        app.fly = False
        for i in range(len(app.birdSit)):
                if i == 0:
                    app.birdSit[i].x = app.initBirdX
                    app.birdSit[i].y = app.initBirdY
                else:
                    app.birdSit[i].x += 50


class Bird:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.velocityX = 0
        self.velocityY = 0
        self.velocityT = 0
        self.type = type
        self.material = 'bird'
        self.floor = app.floor
        self.grounded = False
        self.weight = 0.5
        self.abilityUsed = False

        if self.type == 'red':
            self.img = 'images\\red-bird.png'
        elif self.type == 'yellow':
            self.img = 'images\\yellow-bird.png'

    def drawTrajectory(self, app, dt):
        #Parametric For Calculating Trajectory Of Bird
        self.velocityX = (app.initBirdX - self.x)
        self.velocityY = (app.initBirdY - self.y)
        t = 0
        L = []
        trajX = self.x
        trajY = self.y
        while trajY + 30 <= app.floor:
            L.append((trajX, trajY, self.velocityT))
            t += dt
            trajX = self.x + t * self.velocityX
            trajY = self.y + t * self.velocityY + (app.gravity//2 * (t ** 2))
            self.velocityT = (self.velocityX ** 2 + (self.velocityY + app.gravity * t) ** 2) ** (1/2)
        trajY = app.floor - 30
        L.append((trajX, trajY, self.velocityT))
        return L


    def fly(self, app):
        #Animates Birds Thrown In Air
        if app.trajList == []:
            self.velocityT = 0
            shiftBirds(app)
            return
        if self.grounded:
            app.trajList = []
            self.y = self.floor
            return
        self.x = app.trajList[0][0]
        self.y = app.trajList[0][1]
        if self.type == 'yellow' and self.abilityUsed:
            self.velocityT = app.trajList[0][2] * 10
            self.velocityX *= 2
            self.velocityY *= 2
        else:
            self.velocityT = app.trajList[0][2]
        app.trajList.pop(0)


    #Yellow Bird Ability
    def speedUpTraj(self, app):
        count = 0
        for value in app.trajList:
            if count % 5 != 0:
                app.trajList.remove(value)
            count += 1


class Object:
    def __init__(self, app, type, x, y, angle, material):
        self.type = type
        self.x = x
        self.rotateX = x
        self.y = y
        self.material = material
        self.weight = 1
        self.floor = app.floor
        
        if self.material == 'flesh':
            self.hp = 50
            self.weight = 1/2
        elif material == 'wood':
            self.hp = 100
            self.weight = 1
        elif material == 'stone':
            self.hp = 500
            self.weight = 3

        self.velocityX = 0
        self.velocityY = 0
        self.angle = angle
        self.isRotating = False
        self.rotateInfo = (0, 0)
        self.rotateCount = 0
        self.elevation = 0
        self.grounded = False
        if self.type == 'wheel':
            self.friction = 2
        else:
            self.friction = 10

        if self.type == 'pig':
            self.img = 'images\\pig.png'
        elif self.type == 'box':
            if self.material == 'wood':
                self.img = 'images\\wood_box.png'
            elif self.material == 'stone':
                self.img = 'images\\stone_box.png'
        elif self.type == 'column':
            if self.material == 'wood':
                self.img = 'images\\wood_column.png'
            elif self.material == 'stone':
                self.img = 'images\\stone_column.png'
        elif self.type == 'wheel':
            if self.material == 'wood':
                self.img = 'images\\wood_wheel.png'
            elif self.material == 'stone':
                self.img = 'images\\stone_wheel.png'
        
        self.width = getImageSize(self.img)[0]
        self.height = getImageSize(self.img)[1]
        self.angleWidth = getImageSize(self.img)[0]
        self.angleHeight = getImageSize(self.img)[1]


    #Function Apply Gravity To Class
    def obeyGravity(self, app, dt):
        if self.type == 'pig':
            if self.y < self.floor:
                if self.y + self.velocityY * dt < self.floor - 30:
                    self.y += self.velocityY * dt
                    self.velocityY += app.gravity * self.weight * dt
                else:
                    self.y = self.floor - 30
                    self.velocityY = 0
        elif self.type == 'box':
            self.elevation = self.height/2 + abs((self.height/2 * (2 ** (1/2))- self.height/2) * math.sin(math.radians(2 * self.angle)))
            if self.y < self.floor:
                if self.y + self.velocityY * dt < self.floor - self.elevation:
                    self.y += self.velocityY * dt
                    self.velocityY += app.gravity * self.weight * dt
                else:
                    self.y = self.floor - self.elevation
                    self.velocityY = app.gravity
        elif self.type == 'column':
            self.elevation = self.width/2 * abs(math.sin(math.radians(self.angle))) + self.height/2 * abs(math.cos(math.radians(self.angle)))
            if self.y < self.floor:
                if self.y + self.velocityY * dt < self.floor - self.elevation:
                    self.y += self.velocityY * dt
                    self.velocityY += app.gravity * self.weight * dt
                else:
                    self.y = self.floor - self.elevation
                    self.velocityY = app.gravity
        elif self.type == 'wheel':
            self.elevation = self.height/2 + abs((self.height/2 * (2 ** (1/2))- self.height/2) * math.sin(math.radians(2 * self.angle)))
            if self.y < self.floor:
                if self.y + self.velocityY * dt < self.floor - self.elevation:
                    self.y += self.velocityY * dt
                    self.velocityY += app.gravity * self.weight * dt
                else:
                    self.y = self.floor - self.elevation
                    self.velocityY = app.gravity


    #Defines What Happens When Two Objects (Or Object And Bird) Intersect
    def collision(self, app, otherObject):
        if otherObject.material == 'bird':
            #Bird And Pig
            if self.type == 'pig' and distance(self.x, self.y, otherObject.x, otherObject.y) < 60: #bird and pig
                app.pig.remove(self)
                app.score += 500
                return True

            #Bird And Box
            elif self.type == 'box':
                if ((abs(self.x - otherObject.x) <= 30 + self.width/2) and 
                    (abs(self.y - otherObject.y) <= 30 + self.height/2)):
                    if (otherObject.x <= self.x - self.width/2 or self.x + self.width/2 <= otherObject.x) and otherObject.velocityT != 0:
                        self.velocityX += otherObject.velocityX/self.weight
                        otherObject.velocityX -= self.hp * abs(otherObject.velocityX/otherObject.velocityT)
                        if otherObject.velocityX < 0:
                            otherObject.velocityX = 0
                    elif (otherObject.y <= self.y - self.height/2 or self.y + self.height/2 <= otherObject.y) and otherObject.velocityT != 0:
                        self.velocityY -= otherObject.velocityY/self.weight
                        otherObject.velocityY -= self.hp * abs(otherObject.velocityY/otherObject.velocityT)
                        if otherObject.velocityY < 0:
                            otherObject.velocityY = 0
                    self.hp, otherObject.velocityT = self.hp - otherObject.velocityT, otherObject.velocityT - self.hp
                    if otherObject.velocityT < 0:
                        otherObject.velocityT = 0
                    if self.hp <= 0:
                        app.object.remove(self)
                        app.score += 100
                    else:
                        app.birdThrow.remove(otherObject)
                    return True

            #Bird And Column
            elif self.type == 'column':
                if ((abs(self.x - otherObject.x) <= 30 + self.width/2) and 
                    (abs(self.y - otherObject.y) <= 30 + self.height/2)):
                    if self.angle == 0:
                        if otherObject.y > self.y:
                            self.isRotating = True
                            self.rotateInfo = (-5, -90)
                        elif otherObject.y < self.y:
                            self.isRotating = True
                            self.rotateInfo = (5, 90)
                        self.velocityX += otherObject.velocityX/self.weight
                        if otherObject.velocityT != 0:
                            otherObject.velocityX -= self.hp * abs(otherObject.velocityX/otherObject.velocityT)
                            otherObject.velocityY -= self.hp * abs(otherObject.velocityY/otherObject.velocityT)
                    self.hp -= otherObject.velocityT
                    if self.hp <= 0:
                        app.object.remove(self)
                        app.score += 100
                    else:
                        app.birdThrow.remove(otherObject)
                    return True
                    
            #Bird And Wheel
            elif self.type == 'wheel':
                if ((abs(self.x - otherObject.x) <= 30 + self.width/2) and 
                    (abs(self.y - otherObject.y) <= 30 + self.height/2)):
                    
                    self.velocityX += otherObject.velocityX/self.weight
                    if otherObject.velocityT != 0:
                        otherObject.velocityX -= self.hp * abs(otherObject.velocityX/otherObject.velocityT)
                        if otherObject.velocityX < 0:
                            otherObject.velocityX = 0
                        self.velocityY -= otherObject.velocityY/self.weight
                        otherObject.velocityY -= self.hp * abs(otherObject.velocityY/otherObject.velocityT)
                    if otherObject.velocityY < 0:
                        otherObject.velocityY = 0
                    self.hp, otherObject.velocityT = self.hp - otherObject.velocityT, otherObject.velocityT - self.hp
                    if otherObject.velocityT < 0:
                        otherObject.velocityT = 0
                    if self.hp <= 0:
                        app.object.remove(self)
                        app.score += 100
                    else:
                        app.birdThrow.remove(otherObject)
                    return True


        elif self.type == 'pig':
            #Pig And Box
            if otherObject.type == 'box':
                if ((abs(otherObject.x - self.x) <= 30 + otherObject.width/2) and 
                    (abs(otherObject.y - self.y) <= 30 + otherObject.height/2)):
                    if self.y < otherObject.y:
                        self.floor = otherObject.y - otherObject.height/2
                        self.grounded = True
                    elif self.y > otherObject.y:
                        app.pig.remove(self)
                        app.score += 500
                    return True    
            
            #Pig And Column
            elif otherObject.type == 'column':
                if otherObject.isRotating:
                    floorPoint = (otherObject.x - (otherObject.height/2 * abs(math.sin(math.radians(otherObject.angle)))) 
                                + otherObject.width/2 * abs(math.cos(math.radians(otherObject.angle))))   
                    if abs(self.x - floorPoint) <= otherObject.height + 30:
                        xCollision = floorPoint + (self.x - floorPoint) * abs(math.sin(math.radians(otherObject.angle)))
                        yCollision = otherObject.y - (self.x - floorPoint - otherObject.height/2) * abs(math.cos(math.radians(otherObject.angle)))
                        if abs(distance(xCollision, yCollision, self.x, self.y)) < otherObject.width/2 + 30:
                            if yCollision < self.y:
                                app.pig.remove(self)
                                app.score += 500
                            return True
                elif otherObject.angle == 0:
                    if ((abs(otherObject.x - self.x) <= 30 + otherObject.width/2) and 
                        (abs(otherObject.y - self.y) <= 30 + otherObject.height/2)):
                        if self.y < otherObject.y:
                            self.floor = otherObject.y - otherObject.height/2
                            self.grounded = True
                        elif self.y > otherObject.y:
                            app.pig.remove(self)
                            app.score += 500
                        return True     
                else: 
                    if ((abs(otherObject.x - self.x) <= self.width/2 + otherObject.angleWidth/2) and 
                        (abs(otherObject.y - self.y) <= self.height/2 + otherObject.angleHeight/2)):
                        if self.y + self.height/2 <= otherObject.y - (otherObject.angleHeight/2 - self.velocityY/3):
                            self.floor = otherObject.y - otherObject.angleHeight/2
                            self.grounded = True
                        return True

            #Pig And Wheel
            elif otherObject.type == 'wheel':
                if ((abs(otherObject.x - self.x) <= 30 + otherObject.width/2) and 
                    (abs(otherObject.y - self.y) <= 30 + otherObject.height/2)):
                    if self.y > otherObject.y:
                        app.pig.remove(self)
                        app.score += 500
                        return True    
                    else:
                        if self.x < otherObject.x:
                            otherObject.velocityX += self.velocityY/10
                            self.velocityY -= self.velocityY/10
                        elif self.x >= otherObject.x:
                            otherObject.velocityX -= self.velocityY/10
                            self.velocityY -= self.velocityY/10
                        return True


        elif self.type == 'box':
            #Box And Box
            if otherObject.type == 'box':
                if ((abs(otherObject.x - self.x) <= self.width/2 + otherObject.width/2) and 
                    (abs(otherObject.y - self.y) <= self.height/2 + otherObject.height/2)):
                    if self.y + self.height/2 <= otherObject.y - (otherObject.height/2 - self.velocityY/3):
                        self.floor = otherObject.y - otherObject.height/2
                        self.grounded = True
                    else:
                        if self.x <= otherObject.x - otherObject.width/2 + self.velocityX - self.width/2:
                            newVelocity = (self.velocityX + otherObject.velocityX)/(self.weight + otherObject.weight)
                            self.velocityX = newVelocity
                            otherObject.velocityX = newVelocity
                            self.x = otherObject.x - otherObject.width/2 - self.width/2 - 1
                    return True
                
            #Box And Column
            elif otherObject.type == 'column':
                if otherObject.angle == 0:
                    if ((abs(otherObject.x - self.x) <= self.width/2 + otherObject.width/2) and 
                        (abs(otherObject.y - self.y) <= self.height/2 + otherObject.height/2)):
                        if self.y + self.height/2 <= otherObject.y - (otherObject.height/2 - self.velocityY/3):
                            self.floor = otherObject.y - otherObject.height/2
                            self.grounded = True
                        else:
                            if self.x <= otherObject.x - otherObject.width/2 + self.velocityX - self.width/2:
                                newVelocity = (self.velocityX + otherObject.velocityX)/(self.weight + otherObject.weight)
                                self.velocityX = newVelocity
                                otherObject.velocityX = newVelocity
                                self.x = otherObject.x - otherObject.width/2 - self.width/2 - 1
                        return True
                else: 
                    if ((abs(otherObject.x - self.x) <= self.width/2 + otherObject.angleWidth/2) and 
                        (abs(otherObject.y - self.y) <= self.height/2 + otherObject.angleHeight/2)):
                        if self.y + self.height/2 <= otherObject.y - (otherObject.angleHeight/2 - self.velocityY/3):
                            self.floor = otherObject.y - otherObject.angleHeight/2
                            self.grounded = True
                        else:
                            if self.x <= otherObject.x - otherObject.angleWidth/2 + self.velocityX - self.width/2:
                                newVelocity = (self.velocityX + otherObject.velocityX)/(self.weight + otherObject.weight)
                                self.velocityX = newVelocity
                                otherObject.velocityX = newVelocity
                                self.x = otherObject.x - otherObject.angleWidth/2 - self.width/2 - 1
                        return True
                    
            #Box And Wheel
            elif otherObject.type == 'wheel':
                if ((abs(otherObject.x - self.x) <= self.width/2 + otherObject.angleWidth/2) and 
                    (abs(otherObject.y - self.y) <= self.height/2 + otherObject.angleHeight/2)):
                    if self.y < otherObject.y:
                        if self.x < otherObject.x:
                            otherObject.velocityX += self.velocityY/10
                            self.velocityY -= self.velocityY/10
                        elif self.x > otherObject.x:
                            otherObject.velocityX -= self.velocityY/10
                            self.velocityY -= self.velocityY/10
                    return True
                          
                    
        elif self.type == 'column':
            #Column And Column
            #Columns And Other Columns Fall Next To Each Other Instead Of Onto Each Other As Of TP3
            if otherObject.type == 'column':
                if otherObject.angle == 0:
                    if ((abs(otherObject.x - self.x) <= self.width/2 + otherObject.width/2) and 
                        (abs(otherObject.y - self.y) <= self.height/2 + otherObject.height/2)):
                        if self.y + self.height/2 <= otherObject.y - (otherObject.height/2 - self.velocityY/3):
                            self.floor = otherObject.y - otherObject.height/2
                            self.grounded = True
                        else:
                            if self.x <= otherObject.x - otherObject.width/2 + self.velocityX - self.width/2:
                                newVelocity = (self.velocityX + otherObject.velocityX)/(self.weight + otherObject.weight)
                                self.velocityX = newVelocity
                                otherObject.velocityX = newVelocity
                                self.x = otherObject.x - otherObject.width/2 - self.width/2 - 1
                        return True
                else: 
                    if ((abs(otherObject.x - self.x) <= self.width/2 + otherObject.angleWidth/2) and 
                        (abs(otherObject.y - self.y) <= self.height/2 + otherObject.angleHeight/2)):
                        if self.y + self.height/2 <= otherObject.y - (otherObject.angleHeight/2 - self.velocityY/3):
                            self.floor = otherObject.y - otherObject.angleHeight/2
                            self.grounded = True
                        else:
                            if self.x <= otherObject.x - otherObject.angleWidth/2 + self.velocityX - self.width/2:
                                newVelocity = (self.velocityX + otherObject.velocityX)/(self.weight + otherObject.weight)
                                self.velocityX = newVelocity
                                otherObject.velocityX = newVelocity
                                self.x = otherObject.x - otherObject.angleWidth/2 - self.width/2 - 1
                        return True

            #Column And Box
            elif otherObject.type == 'box':
                if self.angle == 0:
                    if ((abs(otherObject.x - self.x) <= self.width/2 + otherObject.width/2) and 
                        (abs(otherObject.y - self.y) <= self.height/2 + otherObject.height/2)):
                        if self.y + self.height/2 <= otherObject.y - (otherObject.height/2 - self.velocityY/3):
                            self.floor = otherObject.y - otherObject.height/2
                            self.grounded = True
                        else:
                            if self.x <= otherObject.x - otherObject.width/2 + self.velocityX - self.width/2:
                                newVelocity = (self.velocityX + otherObject.velocityX)/(self.weight + otherObject.weight)
                                self.velocityX = newVelocity
                                otherObject.velocityX = newVelocity
                                self.x = otherObject.x - otherObject.width/2 - self.width/2 - 1
                        return True
                else: 
                    if ((abs(otherObject.x - self.x) <= self.width/2 + otherObject.angleWidth/2) and 
                        (abs(otherObject.y - self.y) <= self.height/2 + otherObject.angleHeight/2)):
                        if self.y + self.height/2 <= otherObject.y - (otherObject.angleHeight/2 - self.velocityY/3):
                            self.floor = otherObject.y - otherObject.angleHeight/2
                            self.grounded = True
                        else:
                            if self.x <= otherObject.x - otherObject.angleWidth/2 + self.velocityX - self.width/2:
                                newVelocity = (self.velocityX + otherObject.velocityX)/(self.weight + otherObject.weight)
                                self.velocityX = newVelocity
                                otherObject.velocityX = newVelocity
                                self.x = otherObject.x - otherObject.angleWidth/2 - self.width/2 - 1
                        return True


        elif self.type == 'wheel':
            #Wheel And Wheel
            if otherObject.type == 'wheel':
                if ((abs(otherObject.x - self.x) <= self.width/2 + otherObject.width/2) and 
                    (abs(otherObject.y - self.y) <= self.height/2 + otherObject.height/2)):
                    if self.x < otherObject.x and abs(self.y - otherObject.y) < otherObject.height/2:
                        self.x = otherObject.x - otherObject.width/2 - self.width/2
                        newVelocity = (self.velocityX + otherObject.velocityX)/2
                        self.velocityX, otherObject.velocityX = newVelocity, newVelocity
                    elif self.x > otherObject.x and abs(self.y - otherObject.y) < otherObject.height/2: 
                        self.x = otherObject.x + otherObject.width/2 + self.width/2
                        newVelocity = (self.velocityX + otherObject.velocityX)/2
                        self.velocityX, otherObject.velocityX = newVelocity, newVelocity
            
            #Wheel And Box
            elif otherObject.type == 'box':
                if ((abs(otherObject.x - self.x) <= self.width/2 + otherObject.width/2) and 
                    (abs(otherObject.y - self.y) <= self.height/2 + otherObject.height/2)):
                    if self.x < otherObject.x and abs(self.y - otherObject.y) < otherObject.height/2:
                        self.x = otherObject.x - otherObject.width/2 - self.width/2 - 1
                        newVelocity = (self.velocityX + otherObject.velocityX)/2
                        self.velocityX, otherObject.velocityX = newVelocity, newVelocity
                    elif self.x > otherObject.x and abs(self.y - otherObject.y) < otherObject.height/2: 
                        self.x = otherObject.x + otherObject.width/2 + self.width/2 + 1
                        newVelocity = (self.velocityX + otherObject.velocityX)/2
                        self.velocityX, otherObject.velocityX = newVelocity, newVelocity
                    elif self.y < otherObject.y and abs(self.x - otherObject.x) < otherObject.width/2 + self.width/2:
                        self.floor = otherObject.y - otherObject.height/2
                        self.grounded = True
                        if self.x > otherObject.x + otherObject.width/2:
                            self.velocityX += self.velocityY/2
                        elif self.x < otherObject.x - otherObject.width/2:
                            self.velocityX -= self.velocityY/2
                    return True
                
            #Wheel And Column
            #Wheels And Columns Fall Side To Side Instead Of Onto Each Other As Of TP3


    def spinWheel(self):
        if self.type == 'wheel':
            if self.velocityX > 0:
                self.angle += 3
            elif self.velocityX < 0:
                self.angle -= 3
            else: 
                self.angle = 0


    def rotate(self, rotateSpeed, rotateAngle):
        if self.rotateCount == rotateAngle:
            self.isRotating = False
            self.rotateCount = 0
        else:
            self.angle += rotateSpeed
            self.rotateCount += rotateSpeed
            self.x += (self.height/2 * math.sin(math.radians(self.angle)) - 
                       self.height/2 * math.sin(math.radians(self.angle - rotateSpeed)))
            if self.type == 'column':
                self.angleWidth = self.width * abs(math.cos(math.radians(self.angle))) + self.height * abs(math.sin(math.radians(self.angle))) 
                self.angleHeight = self.width * abs(math.sin(math.radians(self.angle))) + self.height * abs(math.cos(math.radians(self.angle))) 


    def move(self, dt):
        self.x += self.velocityX * dt
        if self.type == 'wheel':
            if self.velocityX > (self.friction * self.weight * dt)/2:
                self.velocityX -= (self.friction * self.weight * dt)/2
            elif self.velocityX < -(self.friction * self.weight * dt)/2:
                self.velocityX += (self.friction * self.weight * dt)/2
            else:
                self.velocityX = 0
        elif self.velocityX > self.friction * self.weight * dt:
            self.velocityX -= self.friction * self.weight * dt
        else:
            self.velocityX = 0
        # self.y += self.velocityY
        # if self.velocityY > 0:
        #     self.velocityY -= app.gravity
        # else:
        #     self.velocityX = 0