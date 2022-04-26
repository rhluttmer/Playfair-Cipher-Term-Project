Project Name:
Playfair Cipher

Description: 
This project allows users to encrypt, decrypts, and crack messages 
using the Playfair Cipher. For encryption and decryption, the user inputs a 
message (either a normal message or one that has already been encoded) and a 
key word. Then there are graphics that walk the user through how the cipher 
works. These graphics show how the key is used to build the encryption / 
decryption grid, and then how the grid is used to encrypt/decrypt the message.
For cracking, the user enters the message and its encoded version. The program 
then returns an encryption grid that would yield the proper encryption.

How to run the project:
Run the encDecGraphics file. This will open up the interactive user interface,
and then simply follow the instructions on screen. Interacting with the app
will automatically run any other file that is needed for you. Likewise,
there is no data entry that needs to be done ahead of time, all inputs will
be collected through the unteractive user interface.

Libraries that need to be installed:
This program uses CMU_CS3_Graphics. So in order to run, the cmu_graphics
folder must be downloaded and unzipped from (https://academy.cs.cmu.edu/desktop)
and then placed into the TP directory. I have left the cmu_cs_graphics.py
file in the directory, otherwise that would have to be added as well.

Shortcut commands:
Both of these keys can be pressed once in the interactive app.
- m: brings user to main menu. It doesn't completely reset the app, so it
will still remember your previous input. 
- r: restarts app and brings user to main menu. This makes the app forget
all previous inputs
- e: brings user to Crack Results screen on an input that created an error


Description of files:
-encDecGraphics.py: again, this is the main file to run. All code related
to graphics is kept in this file
-encryptDecrypt.py : has all helpers for encrypting and decrypting the
playfair cipher
-crackTable2.py : this holds all functions used to crack the cipher (to find
the key table when the user enters a plaintext and ciphertext)
-classes.py : holds definition of classes for all the algorithms. Note,
there are some classes only for drawing, and these are in the graphics file
-letterDictHelpers.py : at the beginning of crackTable2, a letter dict is made
to store a bunch of info about the letters, what they are in rows/cols with,
their neighbors, etc. This file holds the helper functions for that.
-design proposal / storyboard: the required tp design proposal and storyboard



