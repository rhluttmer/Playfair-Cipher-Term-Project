'''
Note: just to be very clear, I did not make this. This was provided the 15112
staff for use with CMu graphics. None of the work here is mine.
'''

from cmu_graphics.cmu_graphics import *
from cmu_graphics.shape_logic import PILWrapper as CMUImage
import threading, traceback, types, inspect, copy, sys
import atexit

class MvcException(Exception): pass

class AppWrapper(object):
    readOnlyAttrs = set(['bottom','centerX', 'centerY',
                         'getTextInput', 'left', 'quit', 'right',
                         'run', 'stop', 'top', 'setMaxShapeCount' ])
    readWriteAttrs = set(['height', 'paused', 'stepsPerSecond',
                          'title', 'width', 'mode', 'background'])
    allAttrs = readOnlyAttrs | readWriteAttrs
    def __init__(self, app):
        self._app = app
        app._app = app
        app.hasException = False
        app.mode = ''
    def __dir__(self):
        fields = copy.copy(AppWrapper.allAttrs)
        for field in self.__dict__:
            if field not in self._app.__dict__:
                fields.add(field)
        return sorted(fields)
    def __getattribute__(self, attr):
        if (attr == '_app'):
            return super().__getattribute__(attr)
        if (attr in AppWrapper.allAttrs):
            result = self._app.__getattribute__(attr)
        else:
            result = super().__getattribute__(attr)
        return result
    def __setattr__(self, attr, value):
        if (attr != '_app') and (self._app.inRedrawAll):
            raise MvcException(f'Cannot change app.{attr} in redrawAll')
        if (attr in AppWrapper.readOnlyAttrs):
            raise Exception(f'app.{attr} is read-only')
        elif (attr in AppWrapper.readWriteAttrs):
            return self._app.__setattr__(attr, value)
        else:
            return super().__setattr__(attr, value)

def drawExceptionWarning():
    if app.hasException: return
    app.hasException = True
    drawRect(0, 0, app.width, app.height, fill=None, border='red', borderWidth=5)
    drawRect(10, app.height-50, app.width-20, 40, fill='white', border='red', borderWidth=4)
    drawLabel('Exception! App Stopped!', app.width/2, app.height-37, fill='red', bold=True)
    drawLabel('See console for details', app.width/2, app.height-23, fill='red', bold=True)

def callUserFn(self, fnName, args):
    # replacement for App.callUserFn()
    fnName0 = fnName
    if app.hasException: return
    if app.mode not in [None, '']:
        fnName = app.mode + fnName[0].upper() + fnName[1:]
    if fnName in self.userGlobals:
        try:
            (self.userGlobals[fnName])(app.appWrapper, *args)
            if (not fnName0.endswith('redrawAll')): redrawAllWrapper(self)
        except Exception as e:
            sys.excepthook(*sys.exc_info())
            drawExceptionWarning()
    elif fnName0.endswith('redrawAll'):
        drawLabel(f'{fnName}()', app.centerX, app.centerY-20, size=20)
        drawLabel('not defined', app.centerX, app.centerY+20, size=20)

def redrawAllWrapper(app):
    app.group.clear()
    try: app.inRedrawAll = True; callUserFn(app, 'redrawAll', [ ])
    finally: app.inRedrawAll = False

def runApp(width=400, height=400, **kwargs):
    kwargs.update({'width': width, 'height': height})
    for kw in kwargs:
        setattr(app.appWrapper, kw, kwargs[kw])
    callUserFn(app, 'onAppStart', [ ])
    redrawAllWrapper(app)
    run()

def setupMvc():
    global app
    app = app._app
    atexit.unregister(run)
    exports = ['MvcException', 'runApp', 'gradient', 'rgb', 'Sound', 'CMUImage' ]
    app.appWrapper = AppWrapper(app)
    app.inRedrawAll = False
    shapes = [ Arc, Circle, Image, Label, Line, Oval,
               Polygon, Rect, RegularPolygon, Star, ]
    def makeDrawFn(shape):
        def drawFn(*args, **kwargs):
            if (not app.inRedrawAll) and (not app.hasException):
                raise MvcException('Cannot draw outside of redrawAll()')
            shape(*args, **kwargs)
        return drawFn
    def makeInvisibleConstructor(shape):
        def constructor(*args, **kwargs):
            result = shape(*args, **kwargs)
            result.visible = False
            return result
        return constructor
    def delUserGlobal(var):
        if (var in app.userGlobals):
            del app.userGlobals[var]
    def addExportedGlobal(var, value):
        globals()[var] = value
        exports.append(var)
    for shape in shapes:
        delUserGlobal(shape.__name__)
        addExportedGlobal(shape.__name__ + 'Shape', makeInvisibleConstructor(shape))
        addExportedGlobal('draw' + shape.__name__, makeDrawFn(shape))
    App.callUserFn = callUserFn
    for var in ['Group', 'app']:
        delUserGlobal(var) # de-globalize these if present
    global __all__
    __all__ = exports

setupMvc()