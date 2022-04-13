from cmu_cs3_graphics import *

def onAppStart(app):
    app.label = 'hello'



def redrawAll(app):
    drawRect(200, 200, 200, 200)
    drawLabel(app.label, 10, 10)

runApp()