

from cmu_cs3_graphics import *
import encryptDecrypt
import string
import classes

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

class KeyLetter(object):
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.fill = None
        self.border = 'black'
    
    def __repr__(self):
        return f'{self.name}:{self.color}'

########################################################
#                      Model
########################################################

def onAppStart(app):

    turnOffAllStates(app)
    app.introVisible = True
    

    app.background = 'mintCream'
    
    initializeGridVars(app)
    initializeButtons(app)
    initializeMessageVars(app)
    initializeTextVars(app)


# Makes every isVisible state false
def turnOffAllStates(app):
    app.introVisible = False
    app.encrypting = False
    app.encInstructsVisible = False
    app.processMessageInstructsVisible = False
    app.makeGridInstructsVisible = False
    app.digraphEncInstructsVisible = False
    app.encSummaryVisible = False

    app.decryptionPrepVisible = False

    app.crackingSetupVisible = False

    app.nextButtonVisible = False
    app.backButtonVisible = False

# Makes every isVisible state false but then turns the next and back buttons on
def turnOffAllStatesButBackNextButtons(app):
    turnOffAllStates(app)
    app.nextButtonVisible = True
    app.backButtonVisible = True


def initializeGridVars(app):
    app.rowsCols = 5
    app.gridDim = min(app.width, app.height) / 2
    app.boxDim = app.gridDim / app.rowsCols
    app.margin = 10
    app.defaultGridLeft = app.margin
    app.defaultGridTop = app.height / 2 - app.gridDim / 2

    app.keyTable = None

#-------------------Buttons---------------------



# Create all buttons
def initializeButtons(app):
    app.buttons = []
    app.buttonWidth = min(3 * app.boxDim, app.width / 4.2)
    app.buttonHeight = app.boxDim
    width, height = app.buttonWidth, app.buttonHeight
    
    initializeIntroButtons(app)
    initializeEncryptButtons(app)
    initializeBackAndNextButtons(app)
    initializeEncSummaryButtons(app)
    
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
    
    cy = app.height - 0.5 * backNextHeight - app.margin / 2
    cx = app.width - 0.5 * backNextWidth - app.margin / 2
    app.nextButton = Button(cx, cy, backNextWidth, backNextHeight, 
                            'Next', 'next')
    app.buttons.append(app.nextButton)
    app.nextX = cx

    
    cx = 0.5 * backNextWidth + app.margin / 2
    app.backButton = Button(cx, cy, backNextWidth, backNextHeight, 
                            'Back', 'back')
    app.buttons.append(app.backButton)
    app.backX = cx


def initializeEncSummaryButtons(app):
    # Make these buttons smaller than the defaults
    buttonHeight  = 0.5 * app.buttonHeight 
    buttonWidth = 0.75 * app.buttonWidth

    cy = app.height - buttonHeight / 2 - app.margin / 2
    buttonSpace = (app.nextX - app.backX) / 3

    cx = app.backX + buttonSpace
    app.encSummaryDecButton = Button(cx, cy, buttonWidth, buttonHeight, 
                                    'Decrypt', 'encSummary')
    app.buttons.append(app.encSummaryDecButton)
    
    cx += buttonSpace
    app.encSummaryCrackButton = Button(cx, cy, buttonWidth, buttonHeight, 
                                       'Crack', 'encSummary')
    app.buttons.append(app.encSummaryCrackButton)

    cx = app.nextX
    app.mainMenuButton = Button(cx, cy, buttonWidth, buttonHeight, 
                       'Main Menu', 'encSummary')
    app.buttons.append(app.mainMenuButton)

    

    




def initializeMessageVars(app):
    app.plaintext = ''
    app.key = ''
    app.ciphertext = ''
    app.defaultPlaintext = 'This is a secret message to encrypt. Enjoy.'
    app.defaultKey = 'Playfair'
    app.defaultCiphertext = encryptDecrypt.encDecPlayfair(app.defaultPlaintext, 
                                                          app.defaultKey)
    app.messageByDigraph = None

def initializeTextVars(app):
    app.font = 'monospace'

    # I couldn't find it on the CS academy docs, so I used this source
    # to find the width to height ratio https://code-examples.net/en/q/123a6fd
    app.fontWidthToHeightRatio = 0.6

    app.fontSize = app.height / 25
    app.headingCx = app.width / 2
    app.headingHeight = 2 * app.fontSize
    app.headingCy = app.margin + 0.5 * app.headingHeight
    app.inputColor = 'purple'
    app.color2 = 'green'
    app.rowColor = 'blue'
    app.rowFillColor = 'lightSkyBlue'
    app.colColor = 'red'
    app.colFillColor = 'salmon'
    app.rectColor = 'green'
    app.rectFillColor = 'lightGreen'
    app.resultFillColor = 'lemonChiffon'
    app.lineSpace = 1.15
    app.parSpace = 0.5 * app.fontSize
    
                                  

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
    backButtonClicked(mouseX, mouseY, app)

    encSummaryButtonsClicked(mouseX, mouseY, app)

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
          startProcessMessage(app)

# Moves on to explaining message processing if user opts to use default
def defaultMessageKeyButtonClicked(mouseX, mouseY, app):  
    if (mouseInButton(mouseX, mouseY, app.defaultMessageKeyButton) and
          app.encInstructsVisible):
          app.plaintext = app.defaultPlaintext
          app.key = app.defaultKey
          startProcessMessage(app)

def encSummaryButtonsClicked(mouseX, mouseY, app):
    if not app.encSummaryVisible:
        return

    if mouseInButton(mouseX, mouseY, app.encSummaryDecButton):
        startDecryptionPrep(app)
        
    elif mouseInButton(mouseX, mouseY, app.encSummaryCrackButton):
        startCrackingSetup(app)
    
    # TODO: Fix bug
    elif mouseInButton(mouseX, mouseY, app.mainMenuButton):
        #turnOffAllStates(app)
        app.introVisible = True
        


# Brings user to the next page when they click the next button
def nextButtonClicked(mouseX, mouseY, app):
    if (not mouseInButton(mouseX, mouseY, app.nextButton) or 
        not app.nextButtonVisible):
        return
    
    if app.processMessageInstructsVisible:
        startMakeKeyGridExplanation(app)

    elif app.makeGridInstructsVisible:
        startEncryptingDigraphs(app)

    elif app.digraphEncInstructsVisible:
        startEncryptionSummary(app)

        
# Brings user to the previous page  
def backButtonClicked(mouseX, mouseY, app):
    if (not mouseInButton(mouseX, mouseY, app.backButton) or 
        not app.backButtonVisible):
        return
    
    if app.processMessageInstructsVisible == True:
        turnOffAllStates(app)
        app.encInstructsVisible = True
        resetEncEnteringButtons(app)
    
    elif app.makeGridInstructsVisible:
        startProcessMessage(app)
    
    elif app.digraphEncInstructsVisible:
        startMakeKeyGridExplanation(app)

    elif app.encSummaryVisible:
        startEncryptingDigraphs(app)
        
# Resets the buttons on the entering key/message screen
def resetEncEnteringButtons(app):
    # So that user doesn't have to resubmit stuff if they don't want to
    if app.plaintext.strip() != '' and app.key.strip() != '':
        app.submitMessageKeyButton.on = True
    else:
        app.submitMessageKeyButton.on = False
    app.enterMessageButton.on = True
    app.enterKeyButton.on = True



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

        
        
        startMakeKeyGridExplanation(app)
        
        
    
    if key == 'p':
        app.plaintext = app.defaultPlaintext + 'more letters here for length'
        app.key = app.defaultKey
        app.introVisible = False
        app.makeGridInstructsVisible = False
        startProcessMessage(app)



#----------Start State Functions and their helpers----------
# They set the correct state and make all variables needed for drawing

# Prepares state for the screen that shows how text of a message is processed
# to prepare for encryption / decryption
def startProcessMessage(app):
    turnOffAllStatesButBackNextButtons(app)
    app.encrypting = True
    app.processMessageInstructsVisible = True
    
    app.messageByDigraph = turnDigraphListToString(app)

# Prepares for the state that shows how the keyword is put into a grid
def startMakeKeyGridExplanation(app):
    turnOffAllStatesButBackNextButtons(app)
   
    makeAppKeyTable(app, app.key)

    app.makeGridInstructsVisible = True

# Takes the keyTable output by the encryptDecrypt file, and makes a new
# key table with keyLetter instances, which keep track of the color of 
# text the letter is being written in, its background color, etc
# Mutating method
def makeAppKeyTable(app, key):
    oldKeyTable = encryptDecrypt.makeKeyTable(key)

    newTable = []
    for rowList in oldKeyTable:
        newRowList = []
        for letter in rowList:
            if letter in app.key.upper().replace('J', 'I'):
                color = app.inputColor
            else:
                color = app.color2
            
            newRowList.append(KeyLetter(letter, color))
        
        newTable.append(newRowList)
    
    app.keyTable = newTable
    app.oldKeyTable = oldKeyTable

# Prepares for the state that shows how each digraph is encrypted
def startEncryptingDigraphs(app):
    turnOffAllStatesButBackNextButtons(app)
    resetKeyTable(app)

    app.messageByDigraph = turnDigraphListToString(app)

    if app.keyTable == None:
        makeAppKeyTable(app, app.key)

    app.digraphEncInstructsVisible = True

    app.ciphertext = encryptDecrypt.encDecPlayfair(app.plaintext, app.key, 
                                                    mode = 'encrypt')
    app.ciphertextByDigraph = putSpacesInAndKillJs(app.ciphertext)

# Makes all letters black again, mutating method
def resetKeyTable(app):
    for rowList in app.keyTable:
        for letter in rowList:
            letter.color = 'black'

# Prepares for the state that summarizes the steps taken during encryption 
def startEncryptionSummary(app):
    turnOffAllStates(app)
    app.backButtonVisible = True
    

    if app.messageByDigraph == '':
        app.messageByDigraph = turnDigraphListToString(app)

    if app.ciphertext == '':
        app.ciphertext = encryptDecrypt.encDecPlayfair(app.plaintext, app.key,
                                                       mode = 'encrypt')

    app.encSummaryVisible = True 
    
    
def startDecryptionPrep(app):
    turnOffAllStatesButBackNextButtons(app)

    app.decryptionPrepVisible = True

def startCrackingSetup(app):
    turnOffAllStatesButBackNextButtons(app)

    app.crackingSetupVisible = True

########################################################
#                      View
########################################################


def redrawAll(app):
    if app.introVisible:
        drawIntroScreen(app)
    
    elif app.makeGridInstructsVisible:
        drawGridExplanation(app)
    
    elif app.encInstructsVisible:
        drawEncryptionInstructions(app)
    
    elif app.processMessageInstructsVisible:
        processMessageExplanation(app)

    elif app.digraphEncInstructsVisible:
        drawEncryptDigraphInstructions(app)

    elif app.encSummaryVisible:
        drawEncSummary(app)

    elif app.decryptionPrepVisible:
        drawDecryptionPrep(app)
    
    elif app.crackingSetupVisible:
        drawCrackingSetup(app)
 
    
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
            (button.use == 'back' and app.backButtonVisible) or
            (button.use == 'encSummary' and app.encSummaryVisible)): 
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
    topY = drawHeading(app, 'Processing Message')

    # Line shows entered message in black and then message in purple
    text = 'Entered Message: '
    message = app.plaintext if (app.encrypting) else app.ciphertext
    topY = drawEnteredPlusInput(app, topY, text, message)

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
    topY = drawExplanationPlusOneLine(app, text, app.messageByDigraph, topY)

# Makes screen that explains how keyword becomes a grid
def drawGridExplanation(app):
    topY = drawHeading(app, 'Making Key Grid')
    topY = drawEnteredPlusInput(app, topY, 'Entered Key: ', app.key)
    
    text = ('Just like with the message, all letters must be capital and all' +
            " J's must be replaced with I's. When we do this, " +
            "we get the keyword: ")
    upperKey = encryptDecrypt.removeNonAlphas(app.key.upper().replace('J', 'I'))
    endX, endY = drawTextbox(app, text, topY, returnNewLineTop = False)
    topY = drawWithElipses(app, upperKey, endY, left=endX, color=app.inputColor)

    gridRight, gridBottom = drawGrid(app, gridTop = topY)

    duplicateLetterString = makeDuplicateLetterString(upperKey)
    text = ("We now put the keyword in the grid, making sure every letter " + 
            "appears only once. If a letter would appear more than once, " +
            "we delete all but the first instance. In this case, " +
            f"we deleted {duplicateLetterString}.")
    topY = drawTextbox(app, text, topY, left = gridRight)
    
    text = ("Finally, we put the rest of the alphabet into the grid " +
            "alphabetically, filling each row from left to right and then " + 
            "the rows from top to bottom.")
    drawTextbox(app, text, topY, left = gridRight)

    text = "Now that we have our keygrid and our message, we can encrypt."
    drawTextbox(app, text, gridBottom)

# Draws the 5 x 5 encryption grid (without letters)
# Returns right and bottom sides of grid, with margin
def drawGrid(app, gridLeft = None, gridTop = None):
    if (gridLeft == None): gridLeft = app.defaultGridLeft
    if (gridTop == None): gridTop = app.defaultGridTop

    # Modified from Lecture 3 Animations Case Studies Notes
    for row in range(app.rowsCols):
        for col in range(app.rowsCols):
            cellLeft, cellTop = getCellBounds(app, row, col, gridLeft, gridTop)
            
            if app.keyTable != None:
                fill = app.keyTable[row][col].fill
                border = app.keyTable[row][col].border
            else:
                fill = None
                border = 'black'
            
            borderWidth = 1 if (border == 'black') else 3
            

            drawRect(cellLeft, cellTop, app.boxDim, app.boxDim, fill=fill, 
                     borderWidth = borderWidth, border = border)
            
            # Put letters in grid if we know the letters
            if app.keyTable != None:
                letter = app.keyTable[row][col]
                cx, cy = cellLeft + app.boxDim / 2, cellTop + app.boxDim / 2
                drawLabel(letter.name, cx, cy, size = app.boxDim, 
                          font = app.font, fill = letter.color)
    
    return findGridRightAndBottom(app, gridLeft, gridTop)

# Finds the right and bottom sides of grid, with app.margin added
# This is where new text can start
def findGridRightAndBottom(app, gridLeft, gridTop):
    gridBottom = gridTop + app.gridDim + app.margin
    gridRight = gridLeft + app.gridDim + app.margin

    return gridRight, gridBottom

# Makes screen that explains three rules for encryption
def drawEncryptDigraphInstructions(app):
    # Draw heading, user input, and grid
    topY = drawHeading(app, 'Encrypting Digraphs')
    topY = drawEnteredPlusInput(app, topY, 'Message: ', app.messageByDigraph)
    gridRight, gridBottom = drawGrid(app, gridTop = topY)

    # Explain encryption rules
    text = "We encrypt two letters at a time with the following rules:"
    topY = drawTextbox(app, text, topY, gridRight)

    # TODO: Add arrows onto digraph

    # In rows
    text = ("1. Letters in the same row encrypt to the letters to their " +
            "right (and there's wrap around). For example, ")
    p1, p2, c1, c2 = colorChosenDigraph(app, 1, 1, 1, 4, 1, 2, 1, 0, 
                                        app.rowFillColor, app.rowColor)
    coloredText = f"{p1}{p2} becomes {c1}{c2}."
    topY =drawEnteredPlusInputNoElipses(app, topY, text, coloredText, 
                                  left = gridRight, inputColor = app.rowColor)
    # In same col
    text = ("2. Letters in the same column encrypt to the letters directly " +
            "below them. For example, ")
    p1, p2, c1, c2 = colorChosenDigraph(app, 1, 3, 0, 3, 2, 3, 1, 3, 
                                        app.colFillColor, app.colColor)
    coloredText = f"{p1}{p2} becomes {c1}{c2}."
    topY = drawEnteredPlusInputNoElipses(app, topY, text, coloredText, 
                                  left = gridRight, inputColor = app.colColor)

    # In rectangle
    text = ("3. Otherwise, each letter encrypts to the letter in the same " +
            "row as it but in a column with the other letter. So, ")
    p1, p2, c1, c2 = colorChosenDigraph(app, 3, 0, 4, 2, 3, 2, 4, 0, 
                                        app.rectFillColor, app.rectColor)
    coloredText = f"{p1}{p2} becomes {c1}{c2}."
    topY = drawEnteredPlusInputNoElipses(app, topY, text, coloredText, 
                                  left = gridRight, inputColor = app.rectColor)

    text = "By applying these rules, our message becomes: "
    topY2 = drawTextbox(app, text, gridBottom, width = app.gridDim)

    finalTopY = max(topY, topY2)
    
    # TODO, make each digraph colored by strategy used to encrypt it
    drawWithElipses(app, app.ciphertextByDigraph, finalTopY, 
                    color = app.inputColor)

# Colors certain digraphs on the grid to make it clearer for users
def colorChosenDigraph(app, plain1Row, plain1Col, plain2Row, plain2Col,
                       cipher1Row, cipher1Col, cipher2Row, cipher2Col, 
                       fillColor, borderColor):
    
    plain1 = app.keyTable[plain1Row][plain1Col]
    plain2 = app.keyTable[plain2Row][plain2Col]
    cipher1 = app.keyTable[cipher1Row][cipher1Col]
    cipher2 = app.keyTable[cipher2Row][cipher2Col]
    
    # Color cipher letters first so that if a letter is a plain and cipher
    # letter, it gets the plain color
    cipher1.fill = app.resultFillColor
    cipher1.border = borderColor
    
    cipher2.fill = app.resultFillColor
    cipher2.border = borderColor
    
    plain1.fill = fillColor
    plain1.border = borderColor
    
    plain2.fill = fillColor
    plain2.border = borderColor
    
    

    return plain1.name, plain2.name, cipher1.name, cipher2.name

def drawEncSummary(app):
    topY = drawHeading(app, 'Encryption Summary')
    
    text = "So we started with a message in a key, which were: "
    topY = drawTextbox(app, text, topY)
    text = 'Key: '
    drawEnteredPlusInput(app, topY, text, app.key)
    letterWidth = app.fontSize * app.fontWidthToHeightRatio
    widthOfText = (len(text) + len(app.key) + 1) * letterWidth
    left = widthOfText + app.margin
    topY = drawEnteredPlusInput(app, topY, 'Message: ', app.plaintext, 
                                left = left)
    

    text = ("Before encrypting, we processed the text, yielding: " )
    topY = drawExplanationPlusOneLine(app, text, app.messageByDigraph, topY)
    

    text = ("With our key, we made a key grid which was used to encrypt one " +
            "pair of letters at a time. We did this with all pairs and ended " +
            "up with: ")
    topY = drawTextbox(app, text, topY)
    topY = drawTextbox(app, app.ciphertext, topY, color = app.inputColor)

    text = ("Now to see how one would decrypt or crack this message (using " +
            "the message amd what it encrypt to in order to figure out the " +
            "key grid), click the 'Decrypt' or 'Crack' buttons below. Or, " +
            "click the button on the right to return to the main menu where " +
            "you can enter new text into either the Encrypt, Decrypt, or " +
            "Crack functions.")
    topY = drawTextbox(app, text, topY)

def drawDecryptionPrep(app):
    topY = drawHeading(app, 'Preparing Message and Key')

def drawCrackingSetup(app):
    topY = drawHeading(app, 'Cracking Set Up')


#------------------Helpers to help with drawing text----------------
 
# Puts the heading at top of page, returns y-coordinate to start next line at
def drawHeading(app, text):
    drawLabel(text, app.headingCx, app.headingCy, size = app.headingHeight, 
              font = app.font)
    topY = app.margin + app.headingHeight + 0.5 * app.fontSize
    return topY
  
# Puts the explanation in a textbox and then the user input in a line below
# Returns the y-coordinate where next line should be
def drawExplanationPlusOneLine(app, explanation, line, top):
    topY = drawTextbox(app, explanation, top)
    # To end up below textbox
    
    drawWithElipses(app, line, topY, color = app.inputColor)
    topY += app.lineSpace * app.fontSize + app.parSpace

    return topY

# Wraps text in a label around, returns top of new line
def drawTextbox(app, text, top, left = None, width = None, fontSize = None, 
                color = 'black', returnNewLineTop = True):
    if (left == None): left = app.margin
    if (width == None): width = app.width - left
    if (fontSize == None): fontSize = app.fontSize
    
    fontWidth = fontSize * app.fontWidthToHeightRatio
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
        
    if returnNewLineTop:
        return top + app.parSpace
    
    else:
        endYTop = top - app.lineSpace * fontSize
        endX = left + len(firstBlock) * fontWidth
        return endX, endYTop

# Makes a one line label. If text is too long, puts ... at end to indicate that
# not the whole text is being seen. Returns top of next line
def drawWithElipses(app, text, top, left = None, width = None, fontSize = None,
                    color = 'black'):
    # This is to get around not being able to have app.margin as default value
    if (left == None): left = app.margin
    if (width == None): width = app.width - left - app.margin
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
    
    return top + app.lineSpace * fontSize + app.parSpace

# Draws blackText first in black, and then the user's input text on the 
# same line but in a different color. Returns new topY
def drawEnteredPlusInput(app, topY, blackText, inputText, fontSize = None, 
                         left = None, inputColor = None):
    if (fontSize == None): fontSize = app.fontSize
    if (left == None): left = app.margin
    if (inputColor == None): inputColor = app.inputColor

    endX, endYTop = drawTextbox(app, blackText, topY, left=left, 
                                returnNewLineTop = False)

    width = app.width - app.margin - endX # Width for input text
    drawWithElipses(app, inputText, endYTop, left = endX, 
                    width = width, color = inputColor)
    return topY + app.lineSpace * fontSize + app.parSpace
    
def drawEnteredPlusInputNoElipses(app, topY, blackText, inputText, 
                                  fontSize=None, left=None, inputColor=None):
    if (fontSize == None): fontSize = app.fontSize
    if (left == None): left = app.margin
    if (inputColor == None): inputColor = app.inputColor

    endX, endYTop = drawTextbox(app, blackText, topY, left=left, 
                                returnNewLineTop = False)

    width = app.width - app.margin - endX # Width for input text
    
    fontWidth = fontSize * app.fontWidthToHeightRatio
    
    if fontWidth * len(inputText) <= width:
        topY = drawTextbox(app, inputText, endYTop, left = endX, width = width, 
                           color = inputColor)
        
        return topY
    
    firstLineStop = int(width / fontWidth)
    partialLine = inputText[:firstLineStop]
    
    if ' ' not in partialLine:
        topY = endYTop + fontSize * app.lineSpace
        rest = inputText
    else:
        while partialLine[-1] != ' ':
            partialLine = partialLine[:-1]
        rest = inputText[len(partialLine):]
        topY = drawTextbox(app, partialLine, endYTop, left = endX, width = width, 
                           color = inputColor) - app.parSpace

    topY = drawTextbox(app, rest, topY, left = left, color = inputColor)
    return topY


#-------------Helpers to show intermediate message----------------

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

# Based on Lecture 3 Animations Case Studies Notes
# Returns left, top of box in given row and col
def getCellBounds(app, row, col, gridLeft, gridTop):
    left = gridLeft + col * app.boxDim
    top = gridTop + row * app.boxDim

    return (left, top)

# Makes a string describing all duplicate letters in key
# For example is key = tommorow returns 'o and m'
def makeDuplicateLetterString(key):
    seen = set()
    duplicatesList = []
    for letter in key:
        if letter in seen:
            duplicatesList.append(letter)
        else:
            seen.add(letter)
    
    if len(duplicatesList) == 0:
        return 'nothing'

    duplicatesString = ' and '.join(duplicatesList)
    return duplicatesString





runApp(600, 400)