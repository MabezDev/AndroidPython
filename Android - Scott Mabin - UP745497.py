from graphics import *
from math import sqrt
from random import random
from time import clock
import sys


#Global variables

''' Dictionaries sharing the same key, to make them easily serviceable. '''
#B pls

ACTIVE = {"REFLECT":False,"SPEED":False,"DOUBLE-POINTS":False,"MAGNET":False,"REVERSE":False}
TIMER_DEFAULTS = {"REFLECT":10,"SPEED":15,"DOUBLE-POINTS":20,"MAGNET":10,"REVERSE":10}
ACTIVE_TIMES = {"REFLECT":0,"SPEED":0,"DOUBLE-POINTS":0,"MAGNET":0,"REVERSE":0}
ACTIVE_TEXT_OBJECTS = {"REFLECT":None,"SPEED":None,"DOUBLE-POINTS":None,"MAGNET":None,"REVERSE":None}

HIGH_SCORES_FILE = "hs.txt"

DEBUGGING = False


'''

    Apple types:

    REFLECT:GREEN
    SPEED:ORANGE
    DOUBLE_POINTS:BLUE
    EXPLOSIVE:BLACK
    MAGNET:PURPLE
    REVERSE:YELLOW

'''

HIGH_SCORES = []
HIGH_SCORES_NAMES = []

##To do, add one more buff then draw the buff icon 3 on each ide of the screen

def main(win,name=None,menuDone=False):

    ''' Main program function. '''

    #clear array so no values are left when creating a new game
    HIGH_SCORES_NAMES.clear()
    HIGH_SCORES.clear()

    if(name==None):
        name = getName(win)
    #load scores into memory
    loadHighScores()

    #main loop
    while menuDone == False:
        menuDone = drawMenu(win)
    else:
        Score = 0
        numberOfApples = 8
        android, apples, scoreDisplay = drawScene(numberOfApples, Score,win)
        #playGame returns whether a certain player wishes to play again
        again = playGame(win, android, apples, scoreDisplay, name)
    #If yes, start again with this name, else start again ith new name(has option to exit)
    if(again==True):
        main(win,name,True)
    elif(again==False):
        main(win)

def getName(win):

    ''' returns the name of the player currently playing, also gives the option to exit game. '''

    print("Going to getNameState.")

    valid = False
    enterName = generateMessage("Enter Name and click the screen once entered",0.5,0.8)
    exitButton = generateMessage("EXIT",0.85,0.05,"red")
    exitButton.draw(win)
    get = Entry(Point(0.5,0.45),10)
    get.draw(win)
    enterName.draw(win)
    while valid ==False:
        clicks = win.getMouse()
        if(clicks.x >= 0.8 and clicks.x <= 0.9 and clicks.y >= 0 and clicks.y <= 0.1):
            win.close()
            sys.exit()
        else:
            name = get.getText()
            if(len(name)>0):
                break
    get.undraw()
    enterName.undraw()
    exitButton.undraw()
    return name

def drawScene(numberOfApples, Score,win):

    ''' Sets up playState Scene, incluing drawing player, score display and starting apples. '''

    android = drawAndroid(win)
    apples = drawApples(win, numberOfApples)
    string = "Score: "+str(Score)
    scoreDisplay = Text(Point(0.5, 0.95), string)
    scoreDisplay.setSize(20)
    scoreDisplay.setFill("brown")
    scoreDisplay.setStyle("bold")
    scoreDisplay.setFace("arial")
    scoreDisplay.draw(win)
    return android, apples, scoreDisplay

def drawAndroid(win):

    ''' Generates and draws player(android). '''

    head = Circle(Point(0.5, 0.50), 0.03)
    magnetCircle = Circle(Point(0.50,0.5),0.15)
    body = Rectangle(Point(0.47, 0.45), Point(0.53, 0.5))
    leg1 = Rectangle(Point(0.48, 0.42), Point(0.49, 0.45))
    leg2 = Rectangle(Point(0.52, 0.42), Point(0.51, 0.45))
    arm1 = Rectangle(Point(0.53, 0.46), Point(0.54, 0.5))
    arm2 = Rectangle(Point(0.46, 0.46), Point(0.47, 0.5))
    eye1 = Circle(Point(0.49, 0.51), 0.005)
    eye2 = Circle(Point(0.51, 0.51), 0.005)
    android = [head, body, leg1, leg2, arm1, arm2, eye1, eye2,magnetCircle]
    for part in android:
        if part == eye1 or part == eye2:
            colour = "white"
        else:
            colour = "green"
        if(part == magnetCircle):
            part.setOutline(colour)
            continue
        part.setFill(colour)
        part.setOutline(colour)
        part.draw(win)
    return android

def drawApples(win, numApples):

    ''' Generates the starting apples. '''

    apples = []
    for i in range(numApples):
        x = random()
        y = random()
        apple = Circle(Point(x, y), 0.02)
        apple.setFill("red")
        apple.setOutline("red")
        apple.draw(win)
        apples.append(apple)
    return apples

def addApple(win,colour):

    ''' Adds a apple to the scene with a specific colour. '''

    x = random()
    y = random()
    apple = Circle(Point(x, y), 0.02)
    apple.setFill(colour)
    apple.setOutline(colour)
    apple.draw(win)
    return apple





def playGame(win, android, apples, scoreDisplay, name):

    ''' Main game function, handles the game state, including ACTIVE buffs and Scores.
    Return boolean base on if the player is playing again. '''

    Score = 0
    speedX = 0
    speedY = 0
    speedChange = 0.00003
    retardation = 0.00000001
    Max_Apples = 8
    lost = False

    print("Going to playState.")

    while not lost:

        # move android
        for part in android:
            part.move(speedX, speedY)
        centre = android[0].getCenter()


        currentTime = int(clock())

        #handles buffs and debuffs
        for key in ACTIVE_TIMES:
            difference = (currentTime - ACTIVE_TIMES[key])

            #Five Seconds left checker
            if difference > (TIMER_DEFAULTS[key] - 5) and ACTIVE[key]==True:
                #Sanity check
                if(ACTIVE_TEXT_OBJECTS[key]!=None):
                    ACTIVE_TEXT_OBJECTS[key].setFill("red")
            #50% left checker
            if difference > (TIMER_DEFAULTS[key] - TIMER_DEFAULTS[key]/2) and not difference > (TIMER_DEFAULTS[key] - 5) and ACTIVE[key]==True:
                #Sanity check
                if(ACTIVE_TEXT_OBJECTS[key]!=None):
                    ACTIVE_TEXT_OBJECTS[key].setFill("orange")

            #Generate and draw Active Text Object
            if ACTIVE[key] and ACTIVE_TEXT_OBJECTS[key]==None:
                if(key=="REFLECT"):
                    ACTIVE_TEXT_OBJECTS[key] = generateMessage(key,0.1,0.95)
                elif(key=="SPEED"):
                    ACTIVE_TEXT_OBJECTS[key] = generateMessage(key,0.1,0.9)
                elif(key=="DOUBLE-POINTS"):
                    print("Double Points")
                    ACTIVE_TEXT_OBJECTS[key] = generateMessage(key,0.15,0.85)
                elif(key=="MAGNET"):
                    ACTIVE_TEXT_OBJECTS[key] = generateMessage(key,0.10,0.80)
                elif(key=="REVERSE"):
                    ACTIVE_TEXT_OBJECTS[key] = generateMessage(key,0.10,0.75)

                ACTIVE_TEXT_OBJECTS[key].draw(win)
            #Active has finished.
            if  difference > TIMER_DEFAULTS[key] and ACTIVE[key]==True:
                ACTIVE[key] = False
                ACTIVE_TEXT_OBJECTS[key].undraw()
                ACTIVE_TEXT_OBJECTS[key] = None
                if(key=="MAGNET"):
                    #specific case for efficiency in otherwise we have to try and undraw every time when checking for apples
                    android[len(android)-1].undraw()
                print(key, " bonus has ended!")
            # Keep time updated on object that aren't active.
            if ACTIVE[key]==False:
                ACTIVE_TIMES[key] = currentTime


        if(ACTIVE["SPEED"]):
            speedChange = 0.00009
            retardation = 0.0000001
        else:
            speedChange = 0.00003
            retardation = 0.00000001

        if(ACTIVE["DOUBLE-POINTS"]):
            multiplyer = 20
        else:
            multiplyer = 10

        # handle speed change
        point = win.checkMouse()
        if point != None:
            if(ACTIVE["REVERSE"]):
                if point.getX() < 0.3:
                    speedX = speedX + speedChange
                elif point.getX() > 0.7:
                    speedX = speedX - speedChange
                if point.getY() < 0.3:
                    speedY = speedY + speedChange
                elif point.getY() > 0.7:
                    speedY = speedY - speedChange
            else:
                if point.getX() < 0.3:
                    speedX = speedX - speedChange
                elif point.getX() > 0.7:
                    speedX = speedX + speedChange
                if point.getY() < 0.3:
                    speedY = speedY - speedChange
                elif point.getY() > 0.7:
                    speedY = speedY + speedChange

        #handle retardation (drag/slowing down)
        if(speedX!=0):
            if (speedX > 0):
                speedX = speedX - retardation
            elif(speedX < 0):
                speedX = speedX + retardation
        if(speedY!=0):
            if(speedY > 0):
                speed = speedY - retardation
            elif(speedY < 0):
                speed = speedY + retardation


        if(ACTIVE["REFLECT"]):
            #Bounce of the walls (Invincibility)
            reflectX = sqrt((speedX*speedX))*1.3
            reflectY = sqrt((speedY*speedY))*1.3
            if(centre.x > 1):
                speedX = speedX - reflectX
            elif(centre.x < 0):
                speedX = speedX + reflectX
            if(centre.y > 1):
                speedY = speedY - reflectY
            elif(centre.y < 0):
                speedY = speedY + reflectY
        else:
            # have we hit an edge
            if centre.getX() < 0 or centre.getX() > 1 or \
                centre.getY() < 0 or centre.getY() > 1:
                lost = True

        # have we hit an apple?
        for apple in apples:
            appleCentre = apple.getCenter()

            if(ACTIVE["MAGNET"]):
                grabDistance = 0.15
            else:
                grabDistance = 0.05

            if distanceBetweenPoints(appleCentre, centre) < grabDistance:
                #Colour check to see if its bonus apple to add buffs
                if(apple.config["fill"]=="green"):
                    ACTIVE["REFLECT"] = True
                    print("REFLECT Bonus has Started!")
                elif(apple.config["fill"]=="orange"):
                    ACTIVE["SPEED"] = True
                    print("SPEED Bonus has Started!")
                elif(apple.config["fill"]=="blue"):
                    ACTIVE["DOUBLE-POINTS"]=True
                    print("DOUBLE-POINTS Bonus has Started!")
                elif(apple.config["fill"]=="purple"):
                    #draw effect for the android
                    try:
                        android[len(android)-1].draw(win)
                    except Exception:
                        pass
                    ACTIVE["MAGNET"] = True
                    print("MAGNET Bonus has started!")
                elif(apple.config["fill"]=="yellow"):
                    ACTIVE["REVERSE"] = True
                    print("REVERSE de-buff started!")
                elif(apple.config["fill"]=="black"):
                    #handle explosion
                    speedX *= -1
                    speedY *= -1


                apple.undraw()
                apples.remove(apple)
                Score += 5 * multiplyer

        # random bonus apples
        if len(apples) < Max_Apples:# max apples on screen should be 8
            apples.append(spawnBonusApple(win))
        scoreDisplay.setText("Score: "+(str(Score)))

    message = Text(Point(0.5, 0.5), "")
    message.setSize(20)
    message.setFace("arial")
    message.setFill("brown")
    message.setStyle("bold")



    message.setText("Game over! Your Score was: "+str(Score))
    print("Score : ",Score)
    message.draw(win)

    #finally save Score.
    wasHighScore = saveHighScore(Score,name)
    newHS = None
    if(wasHighScore):
        newHS = generateMessage("New High Score! Well Done!",0.5,0.3,"brown",28)
        newHS.draw(win)
    win.getMouse()

    #clean up for next game.
    for part in android:
        part.undraw()
    for apple in apples:
        apple.undraw()
    for key in ACTIVE_TEXT_OBJECTS:
        if(ACTIVE_TEXT_OBJECTS[key]!=None):
            ACTIVE_TEXT_OBJECTS[key].undraw()
            ACTIVE_TEXT_OBJECTS[key] = None
        #reset buffs
        if(ACTIVE[key]):
            ACTIVE[key] = False
    if(newHS!=None):
        newHS.undraw()
    scoreDisplay.undraw()
    message.undraw()


    #Ask player if they want to play again.
    playAgain = None
    while playAgain == None:
        playAgain = retry(win)
    if(playAgain==True):
        return True
    elif(playAgain==False):
        return False


def retry(win):

    ''' Scene for asking player if they want to play again. '''

    print("Going to retryState.")

    myObjects = []
    myObjects.append(generateMessage("Play again?",0.5,0.8,"red",36))
    myObjects.append(generateMessage("Yes",0.25,0.5))
    myObjects.append(generateMessage("No",0.75,0.5))
    for obj in myObjects:
        obj.draw(win)
    gotAnswer = False
    while gotAnswer == False:
        #check clicks
        clicks = win.getMouse()
        if(clicks.x >= 0.2 and clicks.x <= 0.3 and clicks.y >= 0.45 and clicks.y <= 0.55):
            #cleanUp
            for obj in myObjects:
                obj.undraw()
            gotAnswer = True
            return True
        if(clicks.x >= 0.7 and clicks.x <= 0.8 and clicks.y >= 0.45 and clicks.y <= 0.55):
            #cleanUp
            for obj in myObjects:
                obj.undraw()
            gotAnswer = True
            return False


def spawnBonusApple(win):

    ''' Randomly generates apples, with a chance to spawn bonus apples. '''

    colour = ""

    if(DEBUGGING==False):
        random1 = random()
        if(random1 <= 0.03):
            colour = "orange" #Speed Bonus
        elif(random1 <= 0.06 and random1 >=0.03):
            colour = "green" #Reflect Bonus
        elif(random1 <= 0.09 and random1 >=0.06):
            colour = "blue" #DOUBLE-POINTS
        elif(random1 <= 0.12 and random1 >=0.09):
            colour = "black" #Explosive apple
        elif(random1 <= 0.15 and random1 >=0.12):
            colour = "purple" #Magnet apple
        elif(random1 <= 0.18 and random1 >=0.15):
            colour = "yellow" #Reverse controls apple
        else:
            colour="red"
    elif(DEBUGGING==True):
        random1 = random()
        if(random1 <= 0.15):
            colour = "orange" #Speed Bonus
        elif(random1 <= 0.30 and random1 >=0.15):
            colour = "green" #Reflect Bonus
        elif(random1 <= 0.45 and random1 >=0.30):
            colour = "blue" #DOUBLE-POINTS
        elif(random1 <= 0.60 and random1 >=0.45):
            colour = "black" #Explosive apple
        elif(random1 <= 0.75 and random1 >=0.60):
            colour = "purple" #Magnet apple
        elif(random1 <= 0.90 and random1 >=0.75):
            colour = "yellow" #Reverse controls apple
        else:
            colour="red"
    #print("Adding {0} apple.".format(colour))
    return addApple(win,colour)


def distanceBetweenPoints(p1, p2):

    ''' Returns the distance between two points. '''

    return sqrt((p1.getX() - p2.getX()) ** 2 +
                     (p1.getY() - p2.getY()) ** 2)

def generateMessage(text,x,y,colour="green",size=None):

    ''' Generates a Text Object, Required parameters are Text, x and y.
    Other parameters are optional and have defaults in place '''

    message = Text(Point(x,y),text)
    if(size!=None):
        message.setSize(size)
    message.setFace("arial")
    message.setStyle("bold")
    message.setFill(colour)
    return message


def loadHighScores():

    ''' Loads high scores in from HIGH_SCORES_FILE into memory for viewing and manipulation. '''

    try:
        highScoreFile = open(HIGH_SCORES_FILE,"r")
    except Exception:
        print("No Hs file found, creating one now.")
        highScoreFile = open(HIGH_SCORES_FILE,"w")
        time.sleep(0.2)
        highScoreFile = open(HIGH_SCORES_FILE,"r")
    lines = highScoreFile.readlines()
    if(len(lines) > 0):
        for line in lines:
            vars = line.strip("\n").split(",")
            HIGH_SCORES.append(int(vars[1]))
            HIGH_SCORES_NAMES.append(vars[0])
        print("Loaded scores from HIGH_SCORES_FILE")
    else:
        print("No Scores Found")
    highScoreFile.close()
    #Sorts whilst in the main menu to reduce processing time at the end of the game.
    sortScores()


def saveHighScore(Score,Name):

    ''' Saves the high scores in a csv type format, then returns if the score entered was a high score or not.
        Returns high score even if it wasn't the highest score, as long as it made it to the score board.
        Each line writing contains a carriage return at the end which must be stripped then loading the file.
        Example line in file: 'Joe,150'
    '''

    newHiScore = False
    #check if new HS
    try:
        #blank the file
        open(HIGH_SCORES_FILE, 'w').close()
        time.sleep(0.5)
        file = open(HIGH_SCORES_FILE,"w")
    except Exception:
        print("No HS File")
    #Sort the scores so we only have to check the lowest score to see if can be added
    sortScores()
    #Make sure there are high scores to compare, if not just write this new score to the file
    if(len(HIGH_SCORES) > 0):
            #check if its a high score
            #check highest score, or check lowest score?
            #I chose lowest high score, as it will get replaced if its not a good enough high score
            if(HIGH_SCORES[0] < Score):
                #remove last score if max scores is reached
                print("New High Score!")
                newHiScore = True
                if(len(HIGH_SCORES) >= 10):
                    HIGH_SCORES.pop(0)
                    HIGH_SCORES_NAMES.pop(0)
                #add new score
                HIGH_SCORES.append(Score)
                HIGH_SCORES_NAMES.append(Name)
    else:
        # No scores found in file, must write this one proving it is greater than 0
        if(Score > 0):
            newHiScore = True
            file.write(Name+","+str(Score))
    #Write the scores in memory, back into the file.
    for j in range(len(HIGH_SCORES)):
        string = HIGH_SCORES_NAMES[j]+","+str(HIGH_SCORES[j])+"\n"
        file.write(string)
    file.close()

    print("Saved scores to HIGH_SCORES_FILE successfully.")

    return newHiScore


def drawMenu(win):

    ''' Main menu function, return true when the game is ready to play. '''

    print("Going to menuState.")

    x = 0.5
    myObjects = []
    myObjects.append(generateMessage("Play!",x,0.55))
    myObjects.append(generateMessage("Apples!",x,0.75,"red",28))
    myObjects.append(generateMessage("HighScores",x,0.45))
    myObjects.append(generateMessage("Exit",x,0.35))
    done= False
    while done == False:
        for text in myObjects:
            try:
                text.draw(win)
            except GraphicsError:
                pass
        clicks = win.getMouse()
        if(clicks.x >= (x - 0.5) and clicks.x < (x + 0.7) and clicks.y >= 0.50 and clicks.y <= 0.6):
            done = True
            for text in myObjects:
                text.undraw()
            return True
        elif(clicks.x >= (x-0.5) and clicks.x < (x + 0.7) and clicks.y >= 0.40 and clicks.y <= 0.5):
            for text in myObjects:
                text.undraw()

            highScoresDone = False
            print("Going to highScoreState.")
            while highScoresDone == False:
                highScoresDone = showHighScore(win)
        elif(clicks.x >= (x-0.5) and clicks.x < (x + 0.7) and clicks.y >= 0.30 and clicks.y <= 0.4):
            win.close()
            sys.exit()

def sortScores():
    ''' Simple bubble sort to arrange the scores in ascending order. '''
    for passnum in range(len(HIGH_SCORES)-1,0,-1):
        for i in range(passnum):
            if HIGH_SCORES[i]>HIGH_SCORES[i+1]:
                temp = HIGH_SCORES[i]
                tempName = HIGH_SCORES_NAMES[i]
                HIGH_SCORES[i] = HIGH_SCORES[i+1]
                HIGH_SCORES_NAMES[i] = HIGH_SCORES_NAMES[i+1]
                HIGH_SCORES[i+1] = temp
                HIGH_SCORES_NAMES[i+1] = tempName

def showHighScore(win):

    ''' Scene to display the scores in a numbered format from high to low, that is easy to read. '''

    myObjects = []
    gap = 0.05
    x = 0.45
    y = 0.8
    tableName = generateMessage("Name : Score",x,y+0.05,"red")
    tableName.draw(win)
    for i in range(len(HIGH_SCORES)-1,-1,-1):
        y -= gap
        string  = "{0}. {1} : {2}".format((len(HIGH_SCORES)-i),HIGH_SCORES_NAMES[i],HIGH_SCORES[i])
        scorePrint = generateMessage(string,x,y)
        scorePrint.draw(win)
        myObjects.append(scorePrint)
    win.getMouse()
    tableName.undraw()
    #Clean up scene
    for obj in myObjects:
        obj.undraw()
    return True






if __name__=="__main__":
    #Create the graphWin object and pass it into the main function
    win = GraphWin("Android Game - Scott Mabin - UP745497", 500, 500)
    win.setCoords(0,0,1,1)
    main(win)
