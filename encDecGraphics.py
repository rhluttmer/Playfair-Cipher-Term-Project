from cmu_cs3_graphics import *
import encryptDecrypt

class Button(object):
    def __init__(self, cx, cy, width, height, label, use):
        self.cx = cx
        self.cy = cy
        self.width = width
        self.height = height
        self.label = label
        self.hovering = False
        self.on = True
        self.use = use

########################################################
#                      Model
########################################################

def onAppStart(app):
    app.introVisible = True
    app.gridVisible = False
    app.encInstructsVisible = False
    app.background = 'mintCream'

    initializeGridVars(app)
    initializeButtons(app)

    app.message = ''
    app.keyword = ''


def initializeGridVars(app):
    app.rowsCols = 5
    app.gridDim = min(app.width, app.height) / 2
    app.boxDim = app.gridDim / app.rowsCols
    app.margin = 10
    app.gridLeft = app.margin
    app.gridTop = app.height / 2 - app.gridDim / 2

def initializeButtons(app):
    app.buttons = []
    app.buttonWidth = min(3 * app.boxDim, app.width / 4.2)
    app.buttonHeight = app.boxDim
    width, height = app.buttonWidth, app.buttonHeight
    
    # Encrypt button
    app.encButton = Button(app.width / 4, app.height * 3/4, width, height, 
                           'Encrypt', 'intro')
    app.buttons.append(app.encButton)

    cy = app.height * 1/3
    # Enter message button for use in encryption
    app.enterMessageButton = Button(app.width / 4, cy, width, 
                                    height, 'Enter message', 'encInstructions')
    app.enterKeyButton = Button(app.width / 2, cy, width, 
                                height, 'Enter keyword', 'encInstructions')
    app.submitMessageKeyButton = Button(app.width * 3/4, cy, width, 
                                        height, 'Start encryption', 
                                        'encInstructions')
    cy = app.height * 2/3
    app.defaultMessageKeyButton = Button(app.width * 0.5, cy, width, 
                                         height, 'Use defaults', 
                                         'encInstructions')
    
    app.buttons.extend([app.enterMessageButton, app.enterKeyButton,
                       app.submitMessageKeyButton, app.defaultMessageKeyButton])


    



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
    if mouseInButton(mouseX, mouseY, app.encButton):
        app.introVisible = False
        app.encInstructsVisible = True
    elif (mouseInButton(mouseX, mouseY, app.enterMessageButton) and
          app.encInstructsVisible):
        app.message = app.getTextInput('Please enter your message.')
        app.enterMessageButton.on = False
    elif (mouseInButton(mouseX, mouseY, app.enterMessageButton) and
          app.encInstructsVisible):
        app.key = app.getTextInput('Please enter the keyword.')
    elif (mouseInButton(mouseX, mouseY, app.enterMessageButton) and
          app.encInstructsVisible):
          startEncryption(app)



def onMouseMove(app, mouseX, mouseY):
    for button in app.buttons:
        if not button.on:
            continue
        elif mouseInButton(mouseX, mouseY, button):
            button.hovering = True
        else:
            button.hovering = False
    
def mouseInButton(mouseX, mouseY, button):
    if not button.on:
        return False

    left = button.cx - button.width / 2
    right = button.cx + button.width / 2
    top = button.cy - button.height / 2
    bottom = button.cy + button.height / 2
    return left <= mouseX <= right and top <= mouseY <= bottom


def startEncryption(app):
    
    
    pass

    # keytext = app.getTextInput('Enter your message')



########################################################
#                      View
########################################################

def redrawAll(app):
    if app.introVisible:
        drawIntroScreen(app)
    
    if app.gridVisible == True:
        drawGrid(app)
    
    if app.encInstructsVisible == True:
        drawEncryptionInstructions(app)
    
    drawButtons(app)

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



# Draws the buttons on the intro screen 
def drawButtons(app):
    for button in app.buttons:
        if ((button.use == 'intro' and app.introVisible) or
            (button.use == 'encInstructions' and app.encInstructsVisible)): 
            if button.hovering:
                fill = 'black'
                textCol = app.background
            else:
                fill = None
                textCol = 'black'

            drawRect(button.cx, button.cy, button.width, button.height, 
                    align = 'center', fill = fill, border = 'black')
            labelSize = 1.5 * button.width / len(button.label)
            drawLabel(button.label, button.cx, button.cy, 
                      size = labelSize, fill = textCol)

    
# Draws the instructions for encryption
def drawEncryptionInstructions(app):
    # Intro message
    text = 'Encryption'
    cx = app.width / 2
    textHeight = min(30, app.width / len(text))
    cy = app.margin + 0.5*textHeight
    drawLabel(text, cx, cy, size = textHeight)
    
    cy = app.height * 1/3 - .75 * app.buttonHeight
    text = 'Please enter your message and keywords and then click start.'
    textHeight = min(textHeight / 2 , 2*app.width / len(text))
    drawLabel(text, cx, cy, size = textHeight)

    cy = app.height * 2/3 - 0.75 * app.buttonHeight
    text = 'Or if you prefer, click below to use the default message and key.'
    drawLabel(text, cx, cy, size = textHeight)

    # drawEncryptionButtons(app)




# Draws the 5 x 5 encryption grid (without letters)
def drawGrid(app):
    # Modified from Lecture 3 Animations Case Studies Notes
    for row in range(app.rowsCols):
        for col in range(app.rowsCols):
            left, top = getCellBounds(app, row, col)
            fill = None
            drawRect(left, top, app.boxDim, app.boxDim, fill=fill, 
                     borderWidth=1, border='black')






runApp(400, 400)