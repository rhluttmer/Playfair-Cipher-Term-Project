from cmu_cs3_graphics import *
import encryptDecrypt

class Button(object):
    def __init__(self, cx, cy, width, height, label):
        self.cx = cx
        self.cy = cy
        self.width = width
        self.height = height
        self.label = label
        self.on = False

d1 = Button(10, 10, 10, 10, 'hello')
print(d1)
########################################################
#                      Model
########################################################

def onAppStart(app):
    app.introVisible = True
    app.gridVisible = False
    app.background = 'mintCream'

    initializeGridVars(app)
    initializeIntoButtonVars(app)


def initializeGridVars(app):
    app.rowsCols = 5
    app.gridDim = min(app.width, app.height) / 2
    app.boxDim = app.gridDim / app.rowsCols
    app.margin = 10
    app.gridLeft = app.margin
    app.gridTop = app.height / 2 - app.gridDim / 2

def initializeIntoButtonVars(app):
    app.buttons = []
    
    cx = app.width / 4
    cy = app.height * 3/4
    width = 3 * app.boxDim
    height = app.boxDim
    label = 'Encrypt'
    app.encButton = Button(cx, cy, width, height, label)
    app.buttons.append(app.encButton)
    



# Based on Lecture 3 Animations Case Studies Notes
# Returns left, top of box in given row and col
def getCellBounds(app, row, col):
    left = app.gridLeft + col * app.boxDim
    top = app.gridTop + row * app.boxDim

    return (left, top)


########################################################
#                      Control
########################################################


def onMousePress(app, mouseX, mouseY):
    app.gridVisible = not app.gridVisible


########################################################
#                      View
########################################################

def redrawAll(app):
    if app.introVisible:
        drawIntroScreen(app)
    
    if app.gridVisible == True:
        drawGrid(app)

# Draws the first screen the user sees
def drawIntroScreen(app):
    # Intro message
    text = 'Welcome to the Playfair Cipher Program!'
    cx = app.width / 2
    cy = app.height / 7
    textHeight = 2*app.width / len(text)
    drawLabel(text, cx, cy, size = textHeight)
    cy = cy + 2 * textHeight
    text = 'Click on one of the buttons below to get started'
    textHeight /= 2
    drawLabel(text, cx, cy, size = textHeight)

    drawIntroButtons(app)


# Draws the buttons on the intro screen 
def drawIntroButtons(app):
    for button in app.buttons:
        if button.on:
            fill = 'black'
            textCol = app.background
        else:
            fill = None
            textCol = 'black'

        drawRect(button.cx, button.cy, button.width, button.height, 
                 align = 'center', fill = fill, border = 'black')
        labelSize = button.height / 2
        drawLabel(button.label, button.cx, button.cy, size = labelSize, fill = textCol)

    

# Draws the 5 x 5 encryption grid (without letters)
def drawGrid(app):
    # Modified from Lecture 3 Animations Case Studies Notes
    for row in range(app.rowsCols):
        for col in range(app.rowsCols):
            left, top = getCellBounds(app, row, col)
            fill = None
            drawRect(left, top, app.boxDim, app.boxDim, fill=fill, 
                     borderWidth=1, border='black')






runApp(800, 400)