# Next order of business: add button to explanation page
# The next button isn't showing up right now

from cmu_cs3_graphics import *
import encryptDecrypt
import string

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
    app.encrypting = False

    app.encInstructsVisible = False
    app.processMessageInstructsVisible = False
    app.makeGridInstructsVisible = False
    app.digraphEncInstructsVisible = False
    app.encSummaryVisible = False
    app.nextButtonVisible = False
    app.backButtonVisible = False
    
    

    app.background = 'mintCream'
    
    initializeGridVars(app)
    initializeButtons(app)
    initializeMessageVars(app)
    initializeTextVars(app)




def initializeGridVars(app):
    app.rowsCols = 5
    app.gridDim = min(app.width, app.height) / 2
    app.boxDim = app.gridDim / app.rowsCols
    app.margin = 10
    app.gridLeft = app.margin
    app.gridTop = app.height / 2 - app.gridDim / 2

    app.keyTable = None

def initializeButtons(app):
    app.buttons = []
    app.buttonWidth = min(3 * app.boxDim, app.width / 4.2)
    app.buttonHeight = app.boxDim
    width, height = app.buttonWidth, app.buttonHeight
    
    initializeIntroButtons(app)
    initializeEncryptButtons(app)
    initializeBackAndNextButtons(app)
    
    
    

# Make the buttons that appear on the intro screen
def initializeIntroButtons(app):
    width, height = app.buttonWidth, app.buttonHeight
    
    # Encrypt button on intro screen
    app.encButton = Button(app.width / 4, app.height * 3/4, width, height, 
                           'Encrypt', 'intro')
    app.buttons.append(app.encButton)

# Make the buttons that appear on the first encryption screen
def initializeEncryptButtons(app):
    width, height = app.buttonWidth, app.buttonHeight
    
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
    app.submitMessageKeyButton.on = False
    app.buttons.extend([app.enterMessageButton, app.enterKeyButton,
                       app.submitMessageKeyButton, app.defaultMessageKeyButton])

def initializeBackAndNextButtons(app):
    # Make these buttons smaller than the defaults
    backNextHeight  = 0.5 * app.buttonHeight 
    backNextWidth = 0.75 * app.buttonWidth
    
    cy = app.height - 0.6 * backNextHeight
    cx = app.width - 0.6 * backNextWidth
    app.nextButton = Button(cx, cy, backNextWidth, backNextHeight, 
                            'Next', 'next')
    app.buttons.append(app.nextButton)

    
    cx = 0.6 * backNextWidth
    app.backButton = Button(cx, cy, backNextWidth, backNextHeight, 
                            'Back', 'back')
    app.buttons.append(app.backButton)




def initializeMessageVars(app):
    app.plaintext = ''
    app.key = ''
    app.ciphertext = ''
    app.defaultPlaintext = 'This is a secret message to encrypt. Enjoy.'
    app.defaultKey = 'Playfair'
    app.defaultCiphertext = encryptDecrypt.encDecPlayfair(app.defaultPlaintext, 
                                                          app.defaultKey)

def initializeTextVars(app):
    app.font = 'monospace'
    app.fontWidthToHeightRatio = 0.6
    app.fontSize = app.height / 25
    app.headingCx = app.width / 2
    app.headingHeight = 2 * app.fontSize
    app.headingCy = app.margin + 0.5 * app.headingHeight
    app.inputColor = 'purple'
    app.lineSpace = 1.15
    app.parSpace = 0.5 * app.fontSize
    
                                  

# Based on Lecture 3 Animations Case Studies Notes
# Returns left, top of box in given row and col
def getCellBounds(app, row, col):
    left = app.gridLeft + col * app.boxDim
    top = app.gridTop + row * app.boxDim

    return (left, top)


########################################################
#                      Control
########################################################


#-------------------onMousePress and helpers-----------------

def onMousePress(app, mouseX, mouseY):
    encButtonClicked(mouseX, mouseY, app)
    
    # Encryption screen buttons
    enterMessageButtonClicked(mouseX, mouseY, app)
    enterKeyButtonClicked(mouseX, mouseY, app)
    submitMessageKeyButtonClicked(mouseX, mouseY, app)
    defaultMessageKeyButtonClicked(mouseX, mouseY, app)
    
    nextButtonClicked(mouseX, mouseY, app)

# Checks if click was in encryption button, and starts if encryption if so
def encButtonClicked(mouseX, mouseY, app):
    if mouseInButton(mouseX, mouseY, app.encButton):
        app.introVisible = False
        app.encInstructsVisible = True

# Checks if click was in the enterMessage button, and if so opens window for
# user input.
def enterMessageButtonClicked(mouseX, mouseY, app):
    if (mouseInButton(mouseX, mouseY, app.enterMessageButton) and
          app.encInstructsVisible):
        app.plaintext = app.getTextInput('Please enter your message.')
        if (app.plaintext != ''): app.enterMessageButton.on = False
        if app.key != '' and app.plaintext != '':
            app.submitMessageKeyButton.on = True

# Checks if click was in the enterKey button, and if so opens window for
# user input.
def enterKeyButtonClicked(mouseX, mouseY, app):
    if (mouseInButton(mouseX, mouseY, app.enterKeyButton) and
          app.encInstructsVisible):
        app.key = app.getTextInput('Please enter the keyword.')
        if (app.key != ''): app.enterKeyButton.on = False
        if app.key != '' and app.plaintext != '':
            app.submitMessageKeyButton.on = True
    
# Moves on to explaining message processing if message and key are submitted
def submitMessageKeyButtonClicked(mouseX, mouseY, app):  
    if (mouseInButton(mouseX, mouseY, app.submitMessageKeyButton) and
          app.encInstructsVisible):
          startEncryption(app)

# Moves on to explaining message processing if user opts to use default
def defaultMessageKeyButtonClicked(mouseX, mouseY, app):  
    if (mouseInButton(mouseX, mouseY, app.defaultMessageKeyButton) and
          app.encInstructsVisible):
          app.plaintext = app.defaultPlaintext
          app.key = app.defaultKey
          startEncryption(app)

# Brings user to the next page when they click the next button
def nextButtonClicked(mouseX, mouseY, app):
    if (not mouseInButton(mouseX, mouseY, app.nextButton) or 
        not app.nextButtonVisible):
        return
    
    if app.processMessageInstructsVisible == True:
        app.processMessageInstructsVisible = False
        app.makeGridInstructsVisible = True
    
def backButtonClicked(mouseX, mouseY, app):
    if (not mouseInButton(mouseX, mouseY, app.backButton) or 
        not app.backButtonVisible):
        return
    
    if app.processMessageInstructsVisible == True:
        app.processMessageInstructsVisible = False
        app.encInstructsVisible = True

#---------------------onMouseMove and helpers------


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

#------------------onKeyPress -------------------

def onKeyPress(app, key):
    if key == 'g':
        app.plaintext = 'How are you doing?'
        app.key = 'computer'
        app.introVisible = False
        app.gridVisible = True
        app.encInstructionsVisible = False
        startEncryption(app)
    
    if key == 'p':
        app.plaintext = app.defaultPlaintext + 'more letters here for length'
        app.key = app.defaultKey
        app.introVisible = False
        startEncryption(app)



# Sets things to stuff TODO fix this explanation
def startEncryption(app):
    app.encrypting = True
    app.encInstructsVisible = False
    app.processMessageInstructsVisible = True
    app.nextButtonVisible = True
    app.backButtonVisible = True


    
    
    # fillGridExplanation(app)
    

    
    pass



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
    
    if app.processMessageInstructsVisible:
        processMessageExplanation(app)
    
    drawButtons(app)

# Draws the first screen the user sees
def drawIntroScreen(app):
    # Intro message
    text = 'Playfair Cipher!'
    drawHeading(app, text)
    
    topY = app.height / 2
    text = 'Click on one of the buttons below to get started'
    drawTextbox(app, text, topY)

# Draws the button
def drawButtons(app):
    for button in app.buttons:
        if ((button.use == 'intro' and app.introVisible) or
            (button.use == 'encInstructions' and app.encInstructsVisible) or
            (button.use == 'next' and app.nextButtonVisible) or
            (button.use == 'back' and app.backButtonVisible)): 
            if button.hovering or not button.on:
                fill = None
                textCol = 'black'
            else:
                fill = 'black'
                textCol = app.background

            drawRect(button.cx, button.cy, button.width, button.height, 
                    align = 'center', fill = fill, border = 'black')
            
            # Find font size so that label fits in width of button
            charWidth = 0.9 * button.width / len(button.label)
            widthSize = charWidth / app.fontWidthToHeightRatio
            heightSize = 0.9 * button.height # So that fits in height

            # Take the min
            labelSize = min(widthSize, heightSize)
            
            drawLabel(button.label, button.cx, button.cy, 
                      size = labelSize, fill = textCol, font = app.font)

# Draws the instructions for encryption
def drawEncryptionInstructions(app):
    # Intro message
    text = 'Encryption'
    cx = app.width / 2
    textHeight = 2 * app.fontSize
    cy = app.margin + 0.5*textHeight
    #drawLabel(text, app.headingCx, app.headingCy, size = textHeight, font = app.font)
    drawHeading(app, text)

    leftX = app.margin
    topY = app.height * 1/3 -  app.buttonHeight - 0.5 * app.fontSize
    text = 'Please enter your message and keywords and then click start.'
    drawTextbox(app, text, topY)

    topY = app.height * 2/3 -  app.buttonHeight - 0.5* app.fontSize
    text = 'Or if you prefer, click below to use the default message and key.'
    drawTextbox(app, text, topY)

# Explains how plaintext is prepared for encryption
def processMessageExplanation(app):
    drawHeading(app, 'Processing Message')

    # Line shows entered message in black and then message in purple
    text = 'Entered Message: '
    topY = app.margin + app.headingHeight + 0.5 * app.fontSize
    drawTextbox(app, text, topY)
    widthOfText = len(text) * app.fontSize * app.fontWidthToHeightRatio
    message = app.plaintext if (app.encrypting) else app.ciphertext
    width = app.width - widthOfText
    drawWithElipses(app, message, topY, left = widthOfText + app.margin, 
                    width = width, color = app.inputColor)
    topY += app.lineSpace * app.fontSize + app.parSpace

    # Explain why and then print upper case, only letters, message
    text = ('Before we can start encryption, we need to prepare the message. '
            + 'First, we must make everything uppercase and remove all '
            +'non-letter characters. This yields:')
    uppercaseMessage = encryptDecrypt.removeNonAlphas(app.plaintext.upper())
    topY = drawExplanationPlusOneLine(app, text, uppercaseMessage, topY)

    # Explain why and then display message split into pairs of two with all 
    # J's turned into I's
    text = ('The playfair cipher uses a 5x5 grid, so instead of using our 26' +
            " letter alphabet, we will treat all J’s like I’s to have 25 " +
            'letters. Also, the cipher encrypts digraphs, or pairs of letters,'
            ' so we will split the message up into pairs:')
    spacedMessage = putSpacesInAndKillJs(uppercaseMessage)
    topY = drawExplanationPlusOneLine(app, text, spacedMessage, topY)
    # TODO: Make it so that all J's turned into I's are colored

    # Explain why and then display the final set of digraphs ready for encrypt
    # Left off here

    text = ("Finally if a pair has two of the same letter, we replace the " +
            "second letter with an X. Also, if the last letter doesn’t have" + 
            " a pair, we add an ‘X’ to the end (this is called padding).")
    if len(uppercaseMessage) % 2 == 1:
        portion = 'we did'    
    else:
        portion =  " we didn't "   
    text += f'In your case, {portion} have to pad. So we get: '
    messageByDigraph = turnDigraphListToString(app)
    topY = drawExplanationPlusOneLine(app, text, messageByDigraph, topY)

    
# Puts the explanation in a textbox and then the user input in a line below
# Returns the y-coordinate where next line should be
def drawExplanationPlusOneLine(app, explanation, line, top):
    lines = drawTextbox(app, explanation, top)
    topY = top + lines * app.lineSpace * app.fontSize + app.parSpace 
    # To end up below textbox
    
    drawWithElipses(app, line, topY, color = app.inputColor)
    topY += app.lineSpace * app.fontSize + app.parSpace

    return topY

   
    
    
    pass

# Adds spaces to message and replaces J's with I's
def putSpacesInAndKillJs(message):
    result = ''
    while len(message) > 1:
        newPair = message[:2].replace('J', 'I')
        result += newPair + ' '
        message = message[2:]
    if len(message) == 1:
        result += message.replace('J', 'I')
    else:
        result = result[:-1] # to remove ending space

    return result

# Turns the digraph list to a printable readable string
def turnDigraphListToString(app):
    digraphList = encryptDecrypt.makeDigraphL(app.plaintext)
    result = ''
    for digraph in digraphList:
        result += digraph.let1 + digraph.let2 + ' '

    # To remove last space
    result = result[:-1]

    return result



# Very incomplete
def fillGridExplanation(app):
    app.gridVisible = True


    # Data needed for making grid
    key = app.key
    strippedKey = encryptDecrypt.removeNonAlphas(key.upper())
    keyWithoutJ = strippedKey.replace('J', 'I')
    wholeToPlace = keyWithoutJ + string.ascii_uppercase.replace('I', 'J')
    wholeToPlace = encryptDecrypt.removeStringDuplicates(wholeToPlace)
    restToPlace = wholeToPlace[len(keyWithoutJ):]
    app.keyTable = encryptDecrypt.makeKeyTable(key)
    
   

# Wraps text in a label around, returns how many lines long it was
def drawTextbox(app, text, top, left = None, width = None, fontSize = None, 
                color = 'black'):
    if (left == None): left = app.margin
    if (width == None): width = app.width
    if (fontSize == None): fontSize = app.fontSize
    widthToHeightRatio = app.fontWidthToHeightRatio
    fontWidth = fontSize * widthToHeightRatio
    blockingLength = int(width / fontWidth)
    
    lines = 0
    while (len(text) > 0):
        if len(text) <= blockingLength:
            firstBlock = text
            text = []
        else:
            firstBlock = text[:blockingLength] 
            while firstBlock[-1] != ' ':
                firstBlock = firstBlock[:-1]
            text = text[len(firstBlock): ]
        drawLabel(firstBlock, left, top, align='left-top', size=fontSize, 
                  font=app.font, fill = color)
        
        top += app.lineSpace * fontSize
        lines += 1
        
    
    return lines

# Makes a one line label. If text is too long, puts ... at end to indicate that
# not the whole text is being seen
def drawWithElipses(app, text, top, left = None, width = None, fontSize = None,
                    color = 'black'):
    # This is to get around not being able to have app.margin as default value
    if (left == None): left = app.margin
    if (width == None): width = app.width
    if (fontSize == None): fontSize = app.fontSize

    # How wide in pixels one character of font is
    fontWidth = fontSize * app.fontWidthToHeightRatio

    # How many characters long the line can be
    blockingLength = int(width / fontWidth)

    # Add elipses at right location if text too long
    if len(text) > blockingLength:
        text = text[:blockingLength - 3] + '...'

    drawLabel(text, left, top, align='left-top', size=fontSize, 
                  font=app.font, fill = color)


# Draws the 5 x 5 encryption grid (without letters)
def drawGrid(app):
    # Modified from Lecture 3 Animations Case Studies Notes
    for row in range(app.rowsCols):
        for col in range(app.rowsCols):
            left, top = getCellBounds(app, row, col)
            fill = None
            drawRect(left, top, app.boxDim, app.boxDim, fill=fill, 
                     borderWidth=1, border='black')
            
            if app.keyTable != None:
                letter = app.keyTable[row][col]
                cx, cy = left + app.boxDim / 2, top + app.boxDim / 2
                drawLabel(letter, cx, cy, size = app.boxDim, font = app.font)

# Puts the heading at top of page
def drawHeading(app, text):
    drawLabel(text, app.headingCx, app.headingCy, size = app.headingHeight, 
              font = app.font)




runApp(600, 400)