# Harshil Parikh
# 15/03/15 

# Imports
from tkinter import *
from time import *
from datetime import datetime
import math


# Window Initialization
root = Tk()
root.title("DNA Molecule")

width = root.winfo_screenwidth()-100
height = root.winfo_screenheight()-100
diagonal = math.sqrt(width**2+height**2)

screen = Canvas(root, width=width, height=height)
screen.pack()

# Global Constants
middle = height / 2
sinWaveWidth = 10

DNAStrandSpacing  = 7

targetFPS = 60

# Using Sin Function to get X and Y Values of the DNA Molecule
def defineSinWave(lowerSinX, upperSinX, lowerSinY, upperSinY, ps):
    x = 0
    degree = 25
    rotation = (degree/180) * math.pi
    
    while x <= diagonal:
        x += 10
        lowerYValue = 100*math.sin(1/100*(x+ps))
        upperYValue = -100*math.sin(1/100*(x+ps))

        lowerSinXCoor = x*math.cos(rotation) - lowerYValue*math.sin(rotation)
        lowerSinYCoor = x*math.sin(rotation) + lowerYValue*math.cos(rotation)

        upperSinXCoor = x*math.cos(rotation) - upperYValue*math.sin(rotation)
        upperSinYCoor = x*math.sin(rotation) + upperYValue*math.cos(rotation)
        

        lowerSinX.append(lowerSinXCoor)
        lowerSinY.append(lowerSinYCoor)

        upperSinX.append(upperSinXCoor)
        upperSinY.append(upperSinYCoor)


    return lowerSinX, upperSinX, lowerSinY, upperSinY


# Time from the Start of the Program
def deltaTime(startTime):

    delta = datetime.now() - startTime

    return delta.total_seconds()


# Main
def mainLoop():
    
    ps = 0
    startTime = datetime.now()
    fpsLabel = screen.create_text(35, height-20, text = "FPS: 0")
    frames = 1

    # Loop Through Animation Forever
    while True:

        # Get Initial Values
        lowerSinX = []
        upperSinX = []
        
        lowerSinY = []
        upperSinY = []
        
        upperSinOval = []
        lowerSinOval = []
        dnaSegment = []
        
        ps -= 3.14

        lowerSinX, upperSinX, lowerSinY, upperSinY = defineSinWave(lowerSinX, upperSinX, lowerSinY, upperSinY, ps)            

        # Create an Array of Polygons to Draw
        for sinXValues in range(len(lowerSinX)):
            if sinXValues % DNAStrandSpacing == 0:
               dnaSegment.append(screen.create_polygon(lowerSinX[sinXValues],lowerSinY[sinXValues], upperSinX[sinXValues],upperSinY[sinXValues], sinWaveWidth+upperSinX[sinXValues],sinWaveWidth+upperSinY[sinXValues], sinWaveWidth+lowerSinX[sinXValues],sinWaveWidth+lowerSinY[sinXValues],
                                                       fill="black"))

        # Create an Array of Ovals to Draw
        for sinXValues in range(len(lowerSinX)):
            lowerSinOval.append(screen.create_oval(lowerSinX[sinXValues],lowerSinY[sinXValues], sinWaveWidth+lowerSinX[sinXValues],sinWaveWidth+lowerSinY[sinXValues], fill="red", outline="red"))
            upperSinOval.append(screen.create_oval(upperSinX[sinXValues],upperSinY[sinXValues], sinWaveWidth+upperSinX[sinXValues],sinWaveWidth+upperSinY[sinXValues], fill="blue", outline="blue"))


        #Calculations for FPS
        elapsedTime = deltaTime(startTime)

        sleepTime = (1/targetFPS) - elapsedTime

        if sleepTime < 0:
            sleepTime = 0

        # Update FPS every 10 frames
        if frames % 10 == 0:
            screen.delete(fpsLabel)
            fpsLabel = screen.create_text(35, height-20, text = "FPS: " + str(int(1/(sleepTime+elapsedTime))))

        # Update Screen
        screen.update()
        sleep(sleepTime)

        # Time for next Frame
        startTime = datetime.now()

        # Delete Screem For Next Frame
        for sinXValues in range(len(lowerSinX)):
            screen.delete(lowerSinOval[sinXValues], upperSinOval[sinXValues])
            if sinXValues % DNAStrandSpacing == 0:
                screen.delete(dnaSegment[int(sinXValues/DNAStrandSpacing)])

        # Continue Adding to Frames
        frames += 1

mainLoop()
