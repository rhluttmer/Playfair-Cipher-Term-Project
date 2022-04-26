# Rose Luttmer
'''
This is the primary file of the Playfair cipher project. Running this
will open up an app in which the user can enter messages to encrypt,
decrypt, or crack. The graphics also walkthrough how the Playfair cipher works.

'''

from cmu_cs3_graphics import *
import encryptDecrypt
import crackTable2

class Button(object):
    def __init__(self, cx, cy, width, height, label, use):
        self.cx = cx
        self.cy = cy
        self.width = width
        self.height = height
        self.label = label
        self.hovering = False # whether mouse hovering over it
        self.on = True # whether can be clicked. if off, colored white and
        # can't be clicked.
        self.satisfied = False # whether something has been entered.
        # key entry buttons turn white once satisfied but unlike being off
        # they can still be clicked.
        self.use = use

class KeyLetter(object):
    def __init__(self, name, color, fill = None):
        self.name = name
        self.color = color
        self.fill = fill
        self.border = 'black'
    
    def __repr__(self):
        return f'{self.name}:{self.color}'

########################################################
#                      Model
########################################################

def onAppStart(app):

    turnOffAllStates(app)
    app.introVisible = True
    
    app.mustFindKey = False
    app.background = 'mintCream'
    app.stepsPerSecond = 1
    
    initializeGridVars(app)
    initializeButtons(app)
    initializeMessageVars(app)
    initializeTextVars(app)

# Makes every state false
def turnOffAllStates(app):
    app.introVisible = False
    app.encrypting = False
    app.encInstructsVisible = False
    app.processMessageInstructsVisible = False
    app.makeGridInstructsVisible = False
    app.digraphEncInstructsVisible = False
    app.encSummaryVisible = False

    app.decInstructsVisible = False
    app.decPrepVisible = False
    app.digraphDecInstructsVisible = False
    app.decSummaryVisible = False

    app.crackInstructsVisible = False
    app.crackingSetupVisible = False
    app.crackingResultVisible = False
    app.crackErrorExplanationVisible = False
    app.crackError = False

    app.nextButtonVisible = False
    app.backButtonVisible = False
    app.mainMenuButtonVisible = False
    
    app.jumpingToDec = False
   
# Makes every isVisible state false but then turns the next and back buttons on
def turnOffAllStatesButBackNextButtons(app):
    turnOffAllStates(app)
    app.nextButtonVisible = True
    app.backButtonVisible = True

# Initializes parameter relating to grid, including box width and grid dimension
def initializeGridVars(app):
    app.rowsCols = 5
    app.gridDim = min(app.width, app.height) / 2
    app.boxDim = app.gridDim / app.rowsCols
    app.margin = 10
    app.defaultGridLeft = app.margin
    app.defaultGridTop = app.height / 2 - app.gridDim / 2

    app.keyTable = None

    # These are colors that boxes in the key grid can be filled
    app.colFillColor = 'salmon'
    app.rectColor = 'green'
    app.rectFillColor = 'lightGreen'
    app.resultFillColor = 'lemonChiffon'

# Initializes variables related to the plaintext / key / ciphertext
# Encluding their default values
def initializeMessageVars(app):
    app.plaintext = ''
    app.key = ''
    app.ciphertext = ''
    app.defaultPlaintext = ("This is a secret message to encrypt. " +
                            "Enjoy. This is a sentence that I wrote "+
                            "so that cracking would finish faster!")
    app.defaultKey = 'Playfair'
    app.defaultCiphertext = encryptDecrypt.encDecPlayfair(app.defaultPlaintext, 
                                                          app.defaultKey)
    app.plaintextByDigraph = ''
    app.ciphertextByDigraph = ''

# Initializes variables related to the font, including font, size, font colors
def initializeTextVars(app):
    # This is used so that I know how wide a message will be
    # With non-monospace font, the textbox function wouldn't work well
    app.font = 'monospace'

    # I couldn't find it on the CS academy docs, so I used this source
    # to find the width to height ratio https://code-examples.net/en/q/123a6fd
    app.fontWidthToHeightRatio = 0.6

    app.fontSize = app.height / 25
    app.headingCx = app.width / 2
    app.headingHeight = 2 * app.fontSize
    app.headingCy = app.margin + 0.5 * app.headingHeight
    app.inputColor = 'purple'
    app.inputColor2 = 'green'
    app.rowColor = 'blue'
    app.rowFillColor = 'lightSkyBlue'
    app.colColor = 'red'
    app.lineSpace = 1.15
    app.parSpace = 0.5 * app.fontSize
             
#-------------------Buttons---------------------

# Create all buttons
def initializeButtons(app):
    app.buttons = []
    app.buttonWidth = min(3 * app.boxDim, app.width / 4.2)
    app.buttonHeight = app.boxDim
    
    initializeIntroButtons(app)
    initializeEncryptButtons(app)
    initializeDecryptButtons(app)
    initializeCrackButtons(app)
    initializeBackNextJumpButtons(app)
    initializeEncSummaryButtons(app)
    initializeDecPrepButtons(app)
    initializeDecSummaryButtons(app)
    initializeCrackErrorButtons(app)
    
# Make the buttons that appear on the intro screen
def initializeIntroButtons(app):
    width, height = app.buttonWidth, app.buttonHeight
    cy = app.height - app.margin - 0.5 * height
    
    # Encrypt button on intro screen
    app.encButton = Button(app.width / 4, cy, width, height, 
                           'Encrypt', 'intro')
    app.buttons.append(app.encButton)

    # Decrypt button on intro screen
    app.decButton = Button(app.width / 2, cy, width, height, 
                           'Decrypt', 'intro')
    app.buttons.append(app.decButton)

    # Encrypt button on intro screen
    app.crackButton = Button(app.width * 3/4, cy, width, height, 
                           'Crack', 'intro')
    app.buttons.append(app.crackButton)

# Make the buttons that appear on the first encryption screen
def initializeEncryptButtons(app):
    width, height = app.buttonWidth, app.buttonHeight
    
    cy = app.height * 2/5
    # Enter message button for use in encryption
    app.enterMessageButton = Button(app.width / 4, cy, width, 
                                    height, 'Enter message', 'encInstructions')
    app.enterKeyButton = Button(app.width / 2, cy, width, 
                                height, 'Enter keyword', 'encInstructions')
    app.startEncButton = Button(app.width * 3/4, cy, width, 
                                        height, 'Start encryption', 
                                        'encInstructions')
    cy = app.height * 2/3
    app.useDefaultsEncButton = Button(app.width * 0.5, cy, width, 
                                         height, 'Use defaults', 
                                         'encInstructions')
    app.startEncButton.on = False
    app.buttons.extend([app.enterMessageButton, app.enterKeyButton,
                       app.startEncButton, app.useDefaultsEncButton])

# Make the buttons that appear on the first decryption screen
def initializeDecryptButtons(app):
    width, height = app.buttonWidth, app.buttonHeight
    
    cy = app.height * 2/5
    # Enter message button for use in encryption
    app.enterMessageDecButton = Button(app.width / 4, cy, width, 
                                       height, 'Enter encrypted message', 
                                       'decInstructions')
    app.enterKeyDecButton = Button(app.width / 2, cy, width, 
                                height, 'Enter keyword', 'decInstructions')
    app.startDecButton = Button(app.width * 3/4, cy, width, 
                                           height, 'Start decryption', 
                                           'decInstructions')
    cy = app.height * 2/3
    app.useDefaultsDecButton = Button(app.width * 0.5, cy, width, 
                                      height, 'Use defaults', 
                                      'decInstructions')
    app.startDecButton.on = False
    app.buttons.extend([app.enterMessageDecButton, app.enterKeyDecButton,
                       app.startDecButton, app.useDefaultsDecButton])

# Make the buttons that appear on the first cracking screen
def initializeCrackButtons(app):
    width, height = app.buttonWidth, app.buttonHeight
    
    cy = app.height * 2/5
    # Enter message button for use in encryption
    app.enterMessageCrackButton = Button(app.width / 4, cy, width, 
                                         height, 'Enter original message', 
                                         'crackInstructions')
    app.enterEncMessageCrackButton = Button(app.width / 2, cy, width, 
                                            height, 'Enter encrypted message', 
                                            'crackInstructions')
    app.startCrackButton = Button(app.width * 3/4, cy, width, height, 
                                  'Start cracking', 'crackInstructions')
    cy = app.height * 2/3
    app.useDefaultsCrackButton = Button(app.width * 0.5, cy, width, 
                                        height, 'Use defaults', 
                                        'crackInstructions')
    app.startCrackButton.on = False
    app.buttons.extend([app.enterMessageCrackButton,
                        app.enterEncMessageCrackButton, app.startCrackButton, 
                        app.useDefaultsCrackButton])

# Make the back, next, jump, and menu buttons
# (Basically, this is meant for buttons that show up on multiple screens)
def initializeBackNextJumpButtons(app):
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

    cx = app.width / 2
    app.jumpButton = Button(cx, cy, 2*backNextWidth, backNextHeight,
                            'Back to Decryption', 'jumpingToDec')
    app.buttons.append(app.jumpButton)

    cx = app.nextX
    app.mainMenuButton = Button(cx, cy, backNextWidth, backNextHeight, 
                       'Main Menu', 'main')
    app.buttons.append(app.mainMenuButton)

# Makes buttons for the last encryption screen (where users can take the
# same message and see how it would be decrypted or cracked)
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

# Makes buttons for the decryption screen (where users can choose to see
# how their message would have encrypted or how to crack it)
def initializeDecSummaryButtons(app):
    # Make these buttons smaller than the defaults
    buttonHeight  = 0.5 * app.buttonHeight 
    buttonWidth = 0.75 * app.buttonWidth

    cy = app.height - buttonHeight / 2 - app.margin / 2
    buttonSpace = (app.nextX - app.backX) / 3

    cx = app.backX + buttonSpace
    app.decSummaryEncButton = Button(cx, cy, buttonWidth, buttonHeight, 
                                    'Encrypt', 'decSummary')
    app.buttons.append(app.decSummaryEncButton)
    
    cx += buttonSpace
    app.decSummaryCrackButton = Button(cx, cy, buttonWidth, buttonHeight, 
                                       'Crack', 'decSummary')
    app.buttons.append(app.decSummaryCrackButton)

# On the decryption screen, users can opt to see more in-depth views of how
# the keygrid or message are prepared. By clicking on these buttons,
# they are taken to the more detailed screens
def initializeDecPrepButtons(app):
    # Make these buttons smaller than the defaults
    buttonWidth = (app.width - app.gridDim - 4 * app.margin) / 2
    buttonHeight = app.buttonHeight
    
    cy = app.height - 2 * app.buttonHeight
    cx = 2 * app.margin + app.gridDim + 0.5 * buttonWidth
    app.decPrepMessageButton = Button(cx, cy, buttonWidth, buttonHeight, 
                                      'Prepare Message', 'decPrep')
    app.buttons.append(app.decPrepMessageButton)
    
    cx = app.width - app.margin - 0.5 * buttonWidth
    app.decPrepKeyButton = Button(cx, cy, buttonWidth, buttonHeight, 
                                  'Make Key Grid', 'decPrep')
    app.buttons.append(app.decPrepKeyButton)

# Makes the button that will appear if the message couldn't be cracked
def initializeCrackErrorButtons(app):
    # Make these buttons short but wide
    buttonHeight  = 0.5 * app.buttonHeight 
    buttonWidth = 1.5 * app.buttonWidth

    cy = app.height - buttonHeight / 2 - app.margin / 2
    cx = app.width / 2
    app.crackErrorButton = Button(cx, cy, buttonWidth, buttonHeight,
                                  "Understand Error", 'crackError')
    app.buttons.append(app.crackErrorButton)
    
     
########################################################
#                      Control
########################################################

#-------------------onMousePress and helpers-----------------

# Deals with all buttons clicks, calling many helpers
def onMousePress(app, mouseX, mouseY):
    
    # Have an or statment so that through short circuit evaluation, 
    # only one will be returned
    return (introButtonsClicked(mouseX, mouseY, app) or
    
            # Encryption screen buttons
            encInstructsButtonsClicked(mouseX, mouseY, app) or
            encSummaryButtonsClicked(mouseX, mouseY, app) or
            
            nextButtonClicked(mouseX, mouseY, app) or 
            backButtonClicked(mouseX, mouseY, app) or 
            mainMenuButtonClicked(mouseX, mouseY, app) or 

            decInstructsButtonsClicked(mouseX, mouseY, app) or
            decSummaryButtonsClicked(mouseX, mouseY, app) or

            crackInstructsButtonsClicked(mouseX, mouseY, app) or
            crackErrorButtonsClicked(mouseX, mouseY, app) or
            
            jumpButtonsClicked(mouseX, mouseY, app))

# Checks if click was in any button on intro screen, starts necessary actions
def introButtonsClicked(mouseX, mouseY, app):
    if not app.introVisible:
        return False
    
    
    if mouseInButton(mouseX, mouseY, app.encButton):
        startEncInstructs(app)
        return True
        

    elif mouseInButton(mouseX, mouseY, app.decButton):
        startDecInstructs(app)
        return True
        
    
    elif mouseInButton(mouseX, mouseY, app.crackButton):
        startCrackInstructs(app)
        return True

    return False

# Will reprompt user for entry until the entry has at least one letter
def getValidInput(app, name):
    entry = app.getTextInput(f'Please enter your {name}.')

    while encryptDecrypt.removeNonAlphas(entry.upper()) == '':
        prompt = (f"Please re-enter your {name} making sure it " + 
                   "conatains at least one letter!")
        entry = app.getTextInput(prompt)

    return entry
    
# Returns True if click was in any active button on encryption instructions
# screen, initiates needed actions
def encInstructsButtonsClicked(mouseX, mouseY, app):
    if not app.encInstructsVisible:
        return False

    # Enter plaintext
    if (mouseInButton(mouseX, mouseY, app.enterMessageButton)):
        app.plaintext = getValidInput(app, 'message')
        
        app.enterMessageButton.satisfied = True

        if app.enterMessageButton.satisfied and app.enterKeyButton.satisfied:
            app.startEncButton.on = True
        
        return True

    # Enter key
    elif (mouseInButton(mouseX, mouseY, app.enterKeyButton)):
        app.key = getValidInput(app, 'keyword')
        
        app.enterKeyButton.satisfied = True

        if app.enterMessageButton.satisfied and app.enterKeyButton.satisfied:
            app.startEncButton.on = True

        return True
        
    # Start encryption once plaintext and key entered
    elif (mouseInButton(mouseX, mouseY, app.startEncButton)):
          startProcessMessageInstructs(app)
          return True

    # Start encryption using default plaintext and key
    elif (mouseInButton(mouseX, mouseY, app.useDefaultsEncButton)):
          app.plaintext = app.defaultPlaintext
          app.key = app.defaultKey
          startProcessMessageInstructs(app)
          return True

    return False

# Returns True if click was in the 'Crack' or 'Decrypt' buttons on the
# encryption screen (the ones that will run crack or decrypt using what
# the user had previously entered to encrypt)
def encSummaryButtonsClicked(mouseX, mouseY, app):
    if not app.encSummaryVisible:
        return False

    if mouseInButton(mouseX, mouseY, app.encSummaryDecButton):
        startDecPrep(app)
        return True
        
    if mouseInButton(mouseX, mouseY, app.encSummaryCrackButton):
        startCrackingSetup(app)
        return True
        
# Returns True if click was in any active button on decryption instructions
# screen, initiates needed actions
def decInstructsButtonsClicked(mouseX, mouseY, app):
    if not app.decInstructsVisible:
        return False

    # Enter encrypted message
    if (mouseInButton(mouseX, mouseY, app.enterMessageDecButton)):
        app.ciphertext = getValidInput(app, 'encrypted message')
        app.enterMessageDecButton.satisfied = True

        if (app.enterMessageDecButton.satisfied and 
            app.enterKeyDecButton.satisfied):
            app.startDecButton.on = True
        return True

    # Enter key
    elif (mouseInButton(mouseX, mouseY, app.enterKeyDecButton)):
        app.key = getValidInput(app, 'keyword')
        app.enterKeyDecButton.satisfied = True
        if (app.enterMessageDecButton.satisfied and 
            app.enterKeyDecButton.satisfied):
            app.startDecButton.on = True
        return True
        
    # Start decryption once ciphertext and key entered
    elif (mouseInButton(mouseX, mouseY, app.startDecButton)):
          startDecPrep(app)
          return True

    # Start decryption using default ciphertext and key
    elif (mouseInButton(mouseX, mouseY, app.useDefaultsDecButton)):
          app.ciphertext = app.defaultCiphertext
          app.key = app.defaultKey
          startDecPrep(app)
          return True

    return False

# Returns True if button on the decryption summary screen was clicked
def decSummaryButtonsClicked(mouseX, mouseY, app):
    if not app.decSummaryVisible:
        return False

    if mouseInButton(mouseX, mouseY, app.decSummaryEncButton):
        startProcessMessageInstructs(app)
        return True
        
    if mouseInButton(mouseX, mouseY, app.encSummaryCrackButton):
        startCrackingSetup(app)
        return True
   
# Returns True if click was in any active button on crack instructions
# screen, initiates needed actions
def crackInstructsButtonsClicked(mouseX, mouseY, app):
    if not app.crackInstructsVisible:
        return False

    # Enter encrypted message
    if (mouseInButton(mouseX, mouseY, app.enterMessageCrackButton)):
        app.plaintext = getValidInput(app, 'original message')
        app.enterMessageCrackButton.satisfied = True

        if (app.enterMessageCrackButton.satisfied and 
            app.enterEncMessageCrackButton.satisfied):
            app.startCrackButton.on = True
        return True

    # Enter key
    elif (mouseInButton(mouseX, mouseY, app.enterEncMessageCrackButton)):
        app.ciphertext = getValidInput(app, 'encrypted message')
        app.enterEncMessageCrackButton.satisfied = True

        if (app.enterMessageCrackButton.satisfied and 
            app.enterEncMessageCrackButton.satisfied):
            app.startCrackButton.on = True
        return True
        
    # Start decryption once ciphertext and key entered
    elif (mouseInButton(mouseX, mouseY, app.startCrackButton)):
          startCrackingSetup(app)
          return True

    # Start decryption using default ciphertext and key
    elif (mouseInButton(mouseX, mouseY, app.useDefaultsCrackButton)):
          app.ciphertext = app.defaultCiphertext
          app.plaintext = app.defaultPlaintext
          startCrackingSetup(app)
          return True

    return False

# Returns True if click was in the explain error button, initiates needed action
def crackErrorButtonsClicked(mouseX, mouseY, app):
    if app.crackError and mouseInButton(mouseX, mouseY, app.crackErrorButton):
        startCrackErrorExplanation(app)
        return True
    
    return False
        
# Brings user to the next page when they click the next button
def nextButtonClicked(mouseX, mouseY, app):
    if (not mouseInButton(mouseX, mouseY, app.nextButton) or 
        not app.nextButtonVisible):
        return False
    
    if app.processMessageInstructsVisible:
        startMakeGridInstructs(app)

    elif app.makeGridInstructsVisible:
        startDigraphEncInstructs(app)

    elif app.digraphEncInstructsVisible:
        startEncSummary(app)

    elif app.decPrepVisible:
        startDigraphDecInstructs(app)
    
    elif app.digraphDecInstructsVisible:
        startDecSummary(app)
    
    elif app.crackingSetupVisible:
        startCrackingResult(app)

    
    
    return True
    
# Brings user to the previous page  
def backButtonClicked(mouseX, mouseY, app):

    if (not mouseInButton(mouseX, mouseY, app.backButton) or 
        not app.backButtonVisible):
        return False
    
    if app.processMessageInstructsVisible == True:
        startEncInstructs(app)
    
    elif app.makeGridInstructsVisible:
        startProcessMessageInstructs(app)
    
    elif app.digraphEncInstructsVisible:
        startMakeGridInstructs(app)

    elif app.encSummaryVisible:
        startDigraphEncInstructs(app)

    elif app.decPrepVisible:
        startDecInstructs(app)
    
    elif app.digraphDecInstructsVisible:
        startDecPrep(app)

    elif app.decSummaryVisible:
        startDigraphDecInstructs(app)

    elif app.crackingSetupVisible:
        startCrackInstructs(app)
    
    elif app.crackingResultVisible:
        startCrackingSetup(app)

    elif app.crackErrorExplanationVisible:
        # Doesn't call startCrackingResults so that not all the computation
        # has to be repeated
        app.crackErrorExplanationVisible = False
        app.crackError = True
        app.crackingResultVisible = True
    
    return True

# Brings user back to main menu, returns True if button was clicked and active
def mainMenuButtonClicked(mouseX, mouseY, app):
    if (mouseInButton(mouseX, mouseY, app.mainMenuButton) and 
        app.mainMenuButtonVisible):
        turnOffAllStates(app)
        app.introVisible = True
        return True
        
    return False
 
 # Makes the user 'jump' back to the decryption screen
def jumpButtonsClicked(mouseX, mouseY, app):
    if (mouseInButton(mouseX, mouseY, app.decPrepMessageButton) and
        app.decPrepVisible): 
        
       
        startProcessMessageInstructs(app, mode='decrypt')
        app.jumpingToDec = True
        app.backButtonVisible = False
        app.nextButtonVisible = False
    
        return True

    elif (mouseInButton(mouseX, mouseY, app.decPrepKeyButton)):
        startMakeGridInstructs(app)
        app.jumpingToDec = True
        app.backButtonVisible = False
        app.nextButtonVisible = False
        return True
    
    elif (mouseInButton(mouseX, mouseY, app.jumpButton) and app.jumpingToDec):
        startDecPrep(app)
        return True
    
    return False

 # Helper function to determine whether the click falls into a button or not   
def mouseInButton(mouseX, mouseY, button):
    if not button.on:
        return False

    left = button.cx - button.width / 2
    right = button.cx + button.width / 2
    top = button.cy - button.height / 2
    bottom = button.cy + button.height / 2
    return left <= mouseX <= right and top <= mouseY <= bottom

#------------onMouseMove and onKeyPress------

# Used to change the button color when a mouse hovers over it
def onMouseMove(app, mouseX, mouseY):
    for button in app.buttons:
        if not button.on:
            continue
        elif mouseInButton(mouseX, mouseY, button):
            button.hovering = True
        else:
            button.hovering = False
    
# Used for cheats
def onKeyPress(app, key):
    # Brings user to main menu
    if key == 'm':
        turnOffAllStates(app)
        app.introVisible = True

    # Restarts whole app
    elif key == 'r':
        onAppStart(app)     

    # To test crack error screen
    elif key == 'e':
        # These are inputs that oobviously creat an error
        app.plaintext = 'hello'
        app.ciphertext = 'melon'
        startCrackingResult(app)


#----------Start State Functions and their helpers----------
# They set the correct state and make all variables needed for drawing

# Makes screeen where user enters encryption inputs visible
def startEncInstructs(app):
    turnOffAllStates(app)
    app.encInstructsVisible = True
    
# Prepares state for the screen that shows how text of a message is processed
# to prepare for encryption / decryption
def startProcessMessageInstructs(app, mode = 'encrypt'):
    turnOffAllStatesButBackNextButtons(app)

    if mode == 'encrypt':
        app.encrypting = True
    else:
        app.encrypting = False
    app.processMessageInstructsVisible = True
    
# Prepares for the state that shows how the keyword is put into a grid
def startMakeGridInstructs(app):
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
                color = app.inputColor2
            
            newRowList.append(KeyLetter(letter, color))
        
        newTable.append(newRowList)
    
    app.keyTable = newTable
    app.oldKeyTable = oldKeyTable

# Prepares for the state that shows how each digraph is encrypted
def startDigraphEncInstructs(app):
    turnOffAllStatesButBackNextButtons(app)
    resetKeyTable(app)

    if app.plaintextByDigraph == '':
        app.plaintextByDigraph = makeDigraphString(app.plaintext)

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
def startEncSummary(app):
    turnOffAllStates(app)
    app.backButtonVisible = True
    app.mainMenuButtonVisible = True
    

    app.plaintextByDigraph = makeDigraphString(app.plaintext)

    app.ciphertext = encryptDecrypt.encDecPlayfair(app.plaintext, app.key,
                                                   mode = 'encrypt')

    app.encSummaryVisible = True 

# Makes the screen that letters the user enter decryption inputs visible
def startDecInstructs(app):
    turnOffAllStates(app)
    app.decInstructsVisible = True
    
# Makes the screen that explains how the ciphertext and keygrid are prepared
# for encryption visible
def startDecPrep(app):
    turnOffAllStatesButBackNextButtons(app)

    if app.ciphertextByDigraph == '':
        app.ciphertextByDigraph = makeDigraphString(app.ciphertext)
    
    
    makeAppKeyTable(app, app.key)
    

    app.decPrepVisible = True

# Prepares for the state that explains how to decrypt digraphs 
def startDigraphDecInstructs(app):
    turnOffAllStatesButBackNextButtons(app)

    if app.ciphertextByDigraph == '':
        app.ciphertextByDigraph = makeDigraphString(app.ciphertext)

    app.plaintext = encryptDecrypt.encDecPlayfair(app.ciphertext, app.key,
                                                  mode = 'decrypt')
    app.plaintextByDigraph = putSpacesInAndKillJs(app.plaintext)

    resetKeyTable(app)
    app.digraphDecInstructsVisible = True

# Prepares for the state that explains how decryption was done and what
# the obtained plaintext was  
def startDecSummary(app):
    turnOffAllStates(app)
    app.backButtonVisible = True
    app.mainMenuButtonVisible = True

    app.plaintext = encryptDecrypt.encDecPlayfair(app.ciphertext, app.key, 
                                                      mode = 'decrypt')
    app.decSummaryVisible = True 

# Makes the screen where the user enters inputs for the crack function visible
def startCrackInstructs(app):
    turnOffAllStates(app)
    app.crackInstructsVisible = True
    
# Makes screen that explains how to set up digraph pairs for cracking visible
def startCrackingSetup(app):
    turnOffAllStatesButBackNextButtons(app)
    app.plaintextByDigraph = makeDigraphString(app.plaintext)
    app.ciphertextByDigraph = makeDigraphString(app.ciphertext)

    app.crackingSetupVisible = True

# Makes screen that shows the cracked key grid visible
# Importantly, this function does not actually start trying to crack,
# for that onStep (below) is used
def startCrackingResult(app):
    turnOffAllStates(app)
    app.backButtonVisible = True
    app.mainMenuButtonVisible = True
    app.keyTable = None
    app.crackingResultVisible = True
    app.mustFindKey = True
    app.crackError = False
    
# This is used for cracking. If in startCrackResults we immediately call
# crackTable2, then the graphics don't show the next screen until the result
# is found. By waiting for a step (1 second) to start trying to crack, the
# screen with the explanation loads first, and then once cracked, the keygrid
# will appear
def onStep(app):
    # mustFindKey is used so that we don't restart the cracking process
    # every second, we only want to call it once
    if app.crackingResultVisible and app.mustFindKey:
        app.mustFindKey = False
        makeCrackKeyTable(app)

# This finds the result and turns it into a form that the drawGrid function
# can interperet (it needs to be a list of KeyLetter instances)
def makeCrackKeyTable(app):
    boardDim = 5

    crackedResult = crackTable2.crackKeyTable(app.plaintext, app.ciphertext)
    
    # Deal with case for no solution
    if isinstance(crackedResult, str):
        app.crackError = True # Shows that could not be cracked
        L = list(crackedResult)
        table = []
        for i in range(boardDim):
            rowList = []
            for letter in L[boardDim * i: boardDim * (i+1)]:
                rowList.append(KeyLetter(letter, 'black', fill = 'red'))
            table.append(rowList)
        app.keyTable = table
        return
        
    # Deal with normal case (a key grid was found)
    endRow, endCol = findEndOfKeyWord(crackedResult)
    inKeyWord = True # stays true until we reach a letter no longer in key
    newTable = []
    for row in range(len(crackedResult)):
        newRowList = []
        for col in range(len(crackedResult[0])):
            if row == endRow and col == endCol:
                inKeyWord = False
            letter = crackedResult[row][col]
            # Fill the keyword yellow
            fill = app.resultFillColor if (inKeyWord) else None
            newRowList.append(KeyLetter(letter, 'black', fill = fill))
        
        newTable.append(newRowList)

    app.keyTable = newTable
   
# Returns the row and column after which everything is in alphabetical order
# This is likely the row and column right after the key word, where we start
# filling the grid alphabetically. Helper for makeCrackKeyTable
def findEndOfKeyWord(L):
    lastLetter = chr(ord('A') - 1)
    afterEndRow = 0
    afterEndCol = 0

    for row in range(len(L)):
        for col in range(len(L[0])):
            newLetter = L[row][col]
            if newLetter < lastLetter:
                afterEndRow, afterEndCol = row, col
            lastLetter = newLetter
    
    return afterEndRow, afterEndCol

# Prepares for screen that will explain why the cracking didn't work 
def startCrackErrorExplanation(app):
    turnOffAllStates(app)
    app.backButtonVisible = True
    app.mainMenuButtonVisible = True
    app.crackErrorExplanationVisible = True
    
########################################################
#                      View
########################################################

# Calls all drawing helper functions
def redrawAll(app):
    if app.introVisible: drawIntroScreen(app)
    
    elif app.encInstructsVisible: drawEncInstructs(app)
    
    elif app.processMessageInstructsVisible: drawProcessMessageInstructs(app)
    
    elif app.makeGridInstructsVisible: drawMakeGridInstructs(app)

    elif app.digraphEncInstructsVisible: drawDigraphEncInstructs(app)

    elif app.encSummaryVisible: drawEncSummary(app)

    elif app.decInstructsVisible: drawDecInstructs(app)

    elif app.decPrepVisible: drawDecPrep(app)

    elif app.digraphDecInstructsVisible: drawDigraphDecInstructs(app)

    elif app.decSummaryVisible: drawDecSummary(app)

    elif app.crackInstructsVisible: drawCrackInstructs(app)
    
    elif app.crackingSetupVisible: drawCrackingSetup(app)

    elif app.crackingResultVisible: drawCrackingResults(app)

    elif app.crackErrorExplanationVisible: drawCrackErrorExplanation(app)

 
    
    drawButtons(app)

# Draws the first screen the user sees
def drawIntroScreen(app):
    # Intro message
    text = 'The Playfair Cipher!'
    topY = drawHeading(app, text)
    # Source: https://www.extremetech.com/extreme/287094-quantum-cryptography
    url = ('https://www.extremetech.com/wp-content/uploads/' + 
           '2019/03/Quantum-crypto-image-from-iStock.jpg')
    imageWidth = app.width * 0.7
    imageHeight = imageWidth / 2
    leftX = app.width / 2 - imageWidth / 2
    drawImage(url, leftX, topY, width = imageWidth, height = imageHeight)
    # Learned how to use images through CS Academy Docs
    # https://cs3.academy.cs.cmu.edu/docs

    topY += imageHeight + app.margin
    text = ("Click on one of the buttons below to get started. If you " +
            "don't know how to use Playfair, it's recommended to start " +
            "with encrypting, as both the decrypt and crack modes will " +
            "require you to enter an encrypted message.")
    drawTextbox(app, text, topY)

# Draws the buttons
def drawButtons(app):
    for button in app.buttons:
        if buttonVisible(app, button): 
            if button.hovering or not button.on or button.satisfied:
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
            bold = True if (labelSize <= 12) else False
            
            drawLabel(button.label, button.cx, button.cy, size = labelSize, 
                      fill = textCol, font = app.font, bold = bold)

# Returns whether button is currently being displayed
# Helper for drawButtons
def buttonVisible(app, button):
    return ((button.use == 'intro' and app.introVisible) or
            (button.use == 'encInstructions' and app.encInstructsVisible) or
            (button.use == 'next' and app.nextButtonVisible) or
            (button.use == 'back' and app.backButtonVisible) or
            (button.use == 'encSummary' and app.encSummaryVisible) or
            (button.use == 'decInstructions' and app.decInstructsVisible) or
            (button.use == 'crackInstructions' and app.crackInstructsVisible) or
            (button.use == 'decPrep' and app.decPrepVisible) or
            (button.use == 'decSummary' and app.decSummaryVisible) or
            (button.use == 'jumpingToDec' and app.jumpingToDec) or
            (button.use == 'main' and app.mainMenuButtonVisible) or
            (button.use == 'crackError' and app.crackError))
  
#---------------Encryption Screens-----------------------

# Draws the instructions for encryption (the screen where the user enters input)
def drawEncInstructs(app):
    heading = 'Encryption'
    text1 = ('Please enter your message and keywords and then click start.'+
             " The 'Start' button will become active once both the " +
             "message and the keyword contain at least one letter.")
    
    text2 = 'Or if you prefer, click below to use the default message and key.'
    
    drawInstructionsPage(app, heading, text1, text2)

# Explains how plaintext is prepared for encryption
def drawProcessMessageInstructs(app):
    topY = drawHeading(app, 'Processing Message')

    # Line shows entered message in black and then message in purple
    text = 'Entered Message: '
    message = app.plaintext if (app.encrypting) else app.ciphertext
    topY = drawEnteredPlusInput(app, topY, text, message)

    # Explain why and then print upper case, only letters, message
    text = ('Before we can start encrypting or decrypting, we need to prepare '
            + 'the message. First, we must make everything uppercase and '
            +'remove all non-letter characters. This yields:')
    uppercaseMessage = encryptDecrypt.removeNonAlphas(message.upper())
    topY = drawExplanationPlusOneLine(app, text, uppercaseMessage, topY)

    # Explain why and then display message split into pairs of two with all 
    # J's turned into I's
    text = ('The playfair cipher uses a 5x5 grid, so instead of using our 26' +
            " letter alphabet, we will treat all J’s like I’s to have 25 " +
            'letters. Also, the cipher encrypts digraphs, or pairs of letters,'
            ' so we will split the message up into pairs:')
    spacedMessage = putSpacesInAndKillJs(uppercaseMessage)
    topY = drawExplanationPlusOneLine(app, text, spacedMessage, topY)

    # Explain why and then display the final set of digraphs ready for encrypt
    # Left off here

    text = ("Finally if a pair has two of the same letter, we replace the " +
            "second letter with an X. Also, if the last letter doesn’t have" + 
            " a pair, we add an ‘X’ to the end (this is called padding).")
    if len(uppercaseMessage) % 2 == 1:
        portion = 'we did'    
    else:
        portion =  " we didn't "   
    text += f' In your case, {portion} have to pad. So we get: '
    finalMessage = makeDigraphString(message)
    topY = drawExplanationPlusOneLine(app, text, finalMessage, topY)

# Makes screen that explains how keyword becomes a grid
def drawMakeGridInstructs(app):
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

# Makes screen that explains three rules for encryption
def drawDigraphEncInstructs(app):
    # Draw heading, user input, and grid
    topY = drawHeading(app, 'Encrypting Pairs of Letters')
    topY = drawEnteredPlusInput(app, topY, 'Message: ', app.plaintextByDigraph)
    gridRight, gridBottom = drawGrid(app, gridTop = topY)

    # Explain encryption rules
    text = "We encrypt two letters at a time with the following rules:"
    topY = drawTextbox(app, text, topY, gridRight)

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
    
    drawWithElipses(app, app.ciphertextByDigraph, finalTopY, 
                    color = app.inputColor)

# Makes a screen summarizing the encryption steps taken
def drawEncSummary(app):
    topY = drawHeading(app, 'Encryption Summary')
    
    text = "So we started with a message and a key, which were: "
    topY = drawTextbox(app, text, topY)
    text = 'Key: '
    drawEnteredPlusInput(app, topY, text, app.key)
    letterWidth = app.fontSize * app.fontWidthToHeightRatio
    widthOfText = (len(text) + len(app.key) + 1) * letterWidth
    left = widthOfText + app.margin
    topY = drawEnteredPlusInput(app, topY, 'Message: ', app.plaintext, 
                                left = left)
    

    text = ("Before encrypting, we processed the text, yielding: " )
    topY = drawExplanationPlusOneLine(app, text, app.plaintextByDigraph, topY)
    

    text = ("With our key, we made a key grid which was used to encrypt one " +
            "pair of letters at a time. We did this with all pairs and ended " +
            "up with: ")
    topY = drawTextbox(app, text, topY)
    topY = drawTextbox(app, app.ciphertext, topY, color = app.inputColor)

    text = ("Now to see how one would decrypt or crack this message (using " +
            "the message and what it encrypt to in order to figure out the " +
            "key grid), click the 'Decrypt' or 'Crack' buttons below. Or, " +
            "click the button on the right to return to the main menu where " +
            "you can enter new text into either the Encrypt, Decrypt, or " +
            "Crack functions.")
    topY = drawTextbox(app, text, topY)

#---------------Decryption screens---------------
# Draws the instructions for decryption
def drawDecInstructs(app):
    # Intro message
    heading = 'Decryption'
    text1 = ('Please enter the encrypted message and keyword and then click ' +
             "start. The 'Start' button will become active once both the " +
             "message and the keyword contain at least one letter.")
    text2 = 'Or if you prefer, click below to use the default message and key.'
    drawInstructionsPage(app, heading, text1, text2)

# Draws the screen to say how the message was processed and keygrid was made
def drawDecPrep(app):
    topY = drawHeading(app, 'Preparing Message and Key')

    text = ("As was done with encryption, we first prepare the encoded " +
            "message for decryption by taking away all non-letters, " +
            "replacing ‘J’s with ‘I’s, and adding ‘X’s for double letters " +
            "and at the end of an odd-length message. We also made the key " + 
            "grid using the keyword, just like with encryption.")
    topY = drawTextbox(app, text, topY)

    topY = drawEnteredPlusInput(app, topY, 'Message: ', app.ciphertextByDigraph)

    gridTop = topY - 0.5 * app.parSpace # Otherwise grid too close to bottom
    gridRight, gridBottom = drawGrid(app, gridTop = gridTop)


    text = ("To see how these were made, click the ‘Prepare Message’ " + 
            "or ‘Make Key Grid’ buttons below. Otherwise if you’re good, " + 
            "click the ‘next’ button to proceed.")
    topY = drawTextbox(app, text, gridTop, left = gridRight)

# Makes screen that explains three rules for decryption
def drawDigraphDecInstructs(app):
    # Draw heading, user input, and grid
    topY = drawHeading(app, 'Decrypting Digraphs')
    topY = drawEnteredPlusInput(app, topY, 'Message: ', app.ciphertextByDigraph)
    gridRight, gridBottom = drawGrid(app, gridTop = topY)

    # Explain decryption rules
    text = "We decrypt two letters at a time with the following rules:"
    topY = drawTextbox(app, text, topY, gridRight)

    # In rows
    text = ("1. Letters in the same row decrypt to the letters to their " +
            "left (and there's wrap around). For example, ")
    p1, p2, c1, c2 = colorChosenDigraph(app, 1, 2, 1, 0, 1, 1, 1, 4,  
                                        app.rowFillColor, app.rowColor)
    coloredText = f"{p1}{p2} becomes {c1}{c2}."
    topY =drawEnteredPlusInputNoElipses(app, topY, text, coloredText, 
                                  left = gridRight, inputColor = app.rowColor)
    # In same col
    text = ("2. Letters in the same column decrypt to the letters directly " +
            "above them. For example, ")
    p1, p2, c1, c2 = colorChosenDigraph(app, 2, 3, 1, 3, 1, 3, 0, 3,  
                                        app.colFillColor, app.colColor)
    coloredText = f"{p1}{p2} becomes {c1}{c2}."
    topY = drawEnteredPlusInputNoElipses(app, topY, text, coloredText, 
                                  left = gridRight, inputColor = app.colColor)

    # In rectangle
    text = ("3. Otherwise, each letter decrypts to the letter in the same " +
            "row as it but in a column with the other letter. So, ")
    p1, p2, c1, c2 = colorChosenDigraph(app, 3, 2, 4, 0, 3, 0, 4, 2,  
                                        app.rectFillColor, app.rectColor)
    coloredText = f"{p1}{p2} becomes {c1}{c2}."
    topY = drawEnteredPlusInputNoElipses(app, topY, text, coloredText, 
                                  left = gridRight, inputColor = app.rectColor)

    text = "By applying these rules, we get the message: "
    topY2 = drawTextbox(app, text, gridBottom, width = app.gridDim)

    finalTopY = max(topY, topY2)
    
    drawWithElipses(app, app.plaintextByDigraph, finalTopY, 
                    color = app.inputColor)

# Draws the screen showing the decrypted message and explaining how to
# interperet it
def drawDecSummary(app):
    topY = drawHeading(app, 'Decryption Summary')
    text = 'So we end up with the decoded message: '
    topY = drawTextbox(app, text, topY)
    topY = drawTextbox(app, app.plaintext, topY, color = app.inputColor)

    text = ("Note that there may be a few letters that don’t make " + 
            "sense. Since the Playfair cipher doesn’t use ‘J’s, all " + 
            "‘J’s were replaced with ‘I’s when encoding, so if you see an " + 
            "‘I’ where it doesn’t make sense, it might really be a ‘J’. " + 
            "Also, when encrypting, any digraph with two of the same " +
            "letter had the second letter replaced by an 'X'. So if you see " +
            "a seemingly out of place ‘X’ in the middle of a message, " +
            "replace the ‘X’ with the letter before it. Finally, if the " +
            "message had an odd number of letters, we added an ‘X’ at the " +
            "end, so ignore trailing 'X's that don't make sense.")
    topY = drawTextbox(app, text, topY)

    text = ("Click on the ‘Encrypt’ button to see how to encrypt his message. "+ 
            "Click on the ‘Crack’ button to see how to find the key grid from "+
            "the message and its encryption.")
    topY = drawTextbox(app, text, topY)
    
    
#-------------------Cracking screens-----------
# Makes the screen where the user enter inputs for the cracking program
def drawCrackInstructs(app):
    heading = 'Cracking the Cipher'
    text1 = ('Please enter the message and its encryption and then click '+
            "start. The 'Start' button will become active once both the " +
             "message and its encryption contain at least one letter.")
    text2 = 'Or if you prefer, click below to use the default message and encryption.'
    
    drawInstructionsPage(app, heading, text1, text2)

# Shows how to set up for cracking
def drawCrackingSetup(app):
    topY = drawHeading(app, 'Cracking Set Up')
    text = ("First we prepare the plain ciphertexts by removing illegal " + 
            "characters, adding 'X's, and splitting them into " +
            "digraphs.")
    topY = drawTextbox(app, text, topY)
    topY = drawEnteredPlusInput(app, topY, 'Entered message ', app.plaintext)
    topY -= app.parSpace
    topY = drawEnteredPlusInput(app, topY, 'becomes: ', app.plaintextByDigraph)
    topY = drawEnteredPlusInput(app, topY, 'Entered ciphertext ', 
                                app.ciphertext, inputColor = app.inputColor2)
    topY -= app.parSpace
    topY = drawEnteredPlusInput(app, topY, 'becomes: ', app.ciphertextByDigraph, 
                                inputColor = app.inputColor2)

    
    text = ("We then map which plaintext digraphs (pairs of letters) encrypt " +
            "to which ciphertext digraphs.  So for example we get:")
    topY = drawTextbox(app, text, topY)
    topY = drawDigraphPairs(app, topY)

    text = ("Based on how Playfair works, we can gather information " +
            "from these pairs. For example if AB becomes BC then there must " +
            "be a row or column that contains ‘ABC’. If AB becomes CD and " +
            "CD encrypts to AB, then these pairs must be found in a " +
            "rectangle, so A/C and B/D share rows, and A/D and B/C " +
            "each share a column.")
    drawTextbox(app, text, topY)

# On the cracking srtup screen, draws pairs of plaintext digraphs and the
# ciphertext digraphs they encrypt to. Returns top of new line
def drawDigraphPairs(app, topY):
    # Figure out how many pairs total can be drawn
    leftX = app.margin
    blockLen = 2 + 1 + 2 + 2
    letterWidth = app.fontSize * app.fontWidthToHeightRatio
    blockWidth = letterWidth * blockLen
    blocks = int((app.width - 2 * app.margin - 3 * letterWidth) / blockWidth)
    # So that if there are fewer than 'blocks' digraph, we only print the 
    # existing digraphs
    blocks = min(blocks, len(app.plaintextByDigraph) // 2, 
                 len(app.ciphertextByDigraph) // 2)

    # Helper function to draw one colored text and return end position
    def drawLabelReturnX(text, leftX, topY, color = 'black'):
        drawLabel(text, leftX, topY, fill = color, align = 'left-top', 
                  font = app.font, size = app.fontSize)
        return leftX + letterWidth * len(text)


    # Actually draws blocks
    for i in range(blocks):
        digraphStart = 3 * i
        plainDigraph = app.plaintextByDigraph[digraphStart:digraphStart+2]
        cipherDigraph = app.ciphertextByDigraph[digraphStart:digraphStart+2]

        leftX = drawLabelReturnX(plainDigraph, leftX, topY, 
                                 color = app.inputColor)
        leftX = drawLabelReturnX(':', leftX, topY)
        leftX = drawLabelReturnX(cipherDigraph, leftX, topY, 
                                 color = app.inputColor2)
        leftX = drawLabelReturnX(' '*2, leftX, topY)

    drawLabelReturnX('etc', leftX, topY)

    # Return the top of the new line
    return topY + app.fontSize * app.lineSpace + app.parSpace

# Draws the screen that displays the cracked key grid
def drawCrackingResults(app):
    topY = drawHeading(app, 'Cracking Results')
    text = ("By using the strategies outlined in the last screen, we get a " +
            "lot of information about which letters are in rows or columns " +
            "together. We use this information to play around " +
            "with placing letters, kind of like what is done in a Sudoku. " +
            "We end up with this grid: (it will display once found but "+
            "may take some time, it turns red if there's no solution)")
    topY = drawTextbox(app, text, topY)

    gridRight, gridBottom = drawGrid(app, gridTop = topY)

    text = ("On the grid, a possible key word is highlighted. "+
            "This may not be the grid used to encrypt the message. "+
            "This is because in Playfair, there are many grids that yield the "+
            "same encryption (there are at least 24 grids besides this one " +
            "that would work). Nevertheless, this is a 'correct' grid, " +
            "meaning that using this grid to encrypt your original message, "+
            "will yield the coded message you entered.")
    drawTextbox(app, text, topY, left = gridRight)

# If there is no result from cracking, will explain what the error message meant
def drawCrackErrorExplanation(app):
    topY = drawHeading(app, 'Explanation of Errors')
    
    text = ("There are several different error messages: " )
    topY = drawTextbox(app, text, topY)

    text = ("If you got the message 'Inputs not compatible', this means your "+ 
            "plaintext and ciphertext were different lengths, so they can't " +
            "be the same message.")
    topY = drawTextbox(app, text, topY)

    text = ("If you got the message saying 'L encrypts to itself' this is " +
            "an error because the way Playfair works, a letter will always " +
            "encrypt to a different letter.")
    topY = drawTextbox(app, text, topY)

    text = ("If you got the message 'AB becomes CD and EF' or 'AB & CD " +
            "map to EF' this is an error because each pair in Playfair " +
            "encrypts to exactly one pair and has exactly one pair that " + 
            "encrypts to it ")
    topY = drawTextbox(app, text, topY)

    text = ("Finally, if you got the message 'There is no solution' this " + 
            "means that there was nothing obviously wrong with your inputs, "+
            "but that we went through all possibilities of key tables and "+
            "none worked. Recheck your inputs.")
    topY = drawTextbox(app, text, topY)


#----------------Drawing functions used in multiple modes---------

# Puts text in the right spot for the encryption, decryption, and cracking
# instruction pages
def drawInstructionsPage(app, heading, text1, text2):
    drawHeading(app, heading)

    topY = app.height * 1/3 -  app.buttonHeight - 2 * app.fontSize
    drawTextbox(app, text1, topY)

    topY = app.height * 2/3 -  app.buttonHeight - 2 * app.fontSize
    drawTextbox(app, text2, topY)

# Draws the 5 x 5 encryption grid (without letters)
# Returns right and bottom sides of grid, with margin
def drawGrid(app, gridLeft = None, gridTop = None, keyTable = None):
    if (gridLeft == None): gridLeft = app.defaultGridLeft
    if (gridTop == None): gridTop = app.defaultGridTop
    if (keyTable == None): keyTable = app.keyTable

    # Modified from Lecture 3 Animations Case Studies Notes
    # (https://www.cs.cmu.edu/~112/lecture3/notes/notes-animations-part2.html)
    for row in range(app.rowsCols):
        for col in range(app.rowsCols):
            cellLeft, cellTop = getCellBounds(app, row, col, gridLeft, gridTop)
            
            if keyTable != None:
                fill = keyTable[row][col].fill
                border = keyTable[row][col].border
            else:
                fill = None
                border = 'black'
            
            borderWidth = 1 if (border == 'black') else 3
            

            drawRect(cellLeft, cellTop, app.boxDim, app.boxDim, fill=fill, 
                     borderWidth = borderWidth, border = border)
            
            # Put letters in grid if we know the letters
            if keyTable != None:
                letter = keyTable[row][col]
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
            if ' ' in firstBlock:
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

# This works like drawEnteredPlusInput except doesn't add ellipses at end 
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
        topY = drawTextbox(app, partialLine, endYTop, left=endX, width=width, 
                           color=inputColor) - app.parSpace

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

# Turns the message into a digraph list (which removes everything bad)
# Turns the digraph list to a printable readable string
def makeDigraphString(message):
    digraphList = encryptDecrypt.makeDigraphL(message)
    result = ''
    for digraph in digraphList:
        result += digraph.let1 + digraph.let2 + ' '

    # To remove last space
    result = result[:-1]

    return result

# Based on Lecture 3 Animations Case Studies Notes
# (https://www.cs.cmu.edu/~112/lecture3/notes/notes-animations-part2.html)
# Returns left, top of box in given row and col
def getCellBounds(app, row, col, gridLeft, gridTop):
    left = gridLeft + col * app.boxDim
    top = gridTop + row * app.boxDim

    return (left, top)

# Makes a string describing all duplicate letters in key
# For example is key = TOMORROW returns 'one O and one M'
def makeDuplicateLetterString(key):
    seen = set()
    duplicatesList = []
    duplicatesDict = {}
    for letter in key:
        if letter in seen:
            duplicatesDict[letter] = duplicatesDict.get(letter, 0) + 1
        else:
            seen.add(letter)
    
    if len(duplicatesDict) == 0:
        return 'nothing'

    duplicatesList = []
    for letter in duplicatesDict:
        letterCount = duplicatesDict[letter]
        if letterCount == 1:
            duplicatesList.append(f'one {letter}')
        else:
            duplicatesList.append(f"{letterCount} {letter}'s")


    duplicatesString = ' and '.join(duplicatesList)
    return duplicatesString



runApp(600, 400)