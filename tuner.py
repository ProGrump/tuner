import i, X

#indies call onChildPress
#notifies owner
class Indicator( i.Button ):

    def __init__(
       self,
       owner,
       **kwargs
    ):
        super(
            i.Button , self
        ).__init__(**kwargs)

        self.owner = owner
        self.isPostInit = False
        x = bool(type(self.owner) == SelectorWrapper)
        y = bool(type(self.owner) == IndicatorWrapper)

        assert ( x or y )

        self.data = None
        self.text = ''
        self.font_size = 48

        self.background_normal = ''
        self.background_color = X.GREY

    def on_press( self ):
        self.owner.onChildPress( 
            kid = self
        )
    
    def update( self ):

        self.text = ( str(self.data) )
        return self.text

#wrpapper classes act on notification
class IndicatorWrapper( i.GridLayout ):

    def __init__( 
        self,
        **kwargs 
    ):

        super( i.GridLayout, self ).__init__(**kwargs)

        self.nameOfNote = None
        self.pitchOfNote = None
        self.error = None
        self.temp = None

        self.createIndies( )
        self.setLayout( )

    def createIndies( self ):

        self.nameOfNote = Indicator(
            owner = self
        )
        self.pitchOfNote = Indicator(
            owner = self
        )
        self.error = Indicator(
            owner = self
        )
        self.error.dataUnits = 'hz'
        self.add_widget( self.nameOfNote )
        self.add_widget( self.pitchOfNote )
        self.add_widget( self.error )
        return [
            self.nameOfNote, 
            self.pitchOfNote, 
            self.error
        ]

    def setLayout( self ):

        self.nameOfNote.pos=(800,800)

    def set(  self, audioBuffer, o, f, t  ):
        
        self.temp = audioBuffer

        hz = X.toHz( self.temp )
        self.pitch = int( hz )
        
        noteHz = X.getClosest( 
            self.pitch ,
            X.HZ_NOTE_DICT
        )
        self.pitchOfNote.data = float( noteHz ) 
        note = X.toNote( 
            noteHz, 
            X.HZ_NOTE_DICT 
        )
        self.nameOfNote.data = str( note ) 
        self.error.data = int( self.pitchOfNote.data - self.pitch ) 

    def onChildPress( self,  kid ):
        pass

class SelectorWrapper( i.GridLayout ):

    LEFT = '<'
    RIGHT = '>'

    def __init__( 
        self,
        **kwargs 
    ):

        super( i.GridLayout, self ).__init__(**kwargs)

        self.isPostInit = False

        self.leftButton = Indicator(
            owner = self
        )
        self.leftButton.data = SelectorWrapper.LEFT

        self.rightButton = Indicator(
            owner = self
        )
        self.rightButton.data = SelectorWrapper.RIGHT

        self.current =  Indicator(
            owner = self
        )
        self.current.data = ' 0 '
        self.current.font_size = 14

        self.__indieArr = [ 
            self.leftButton,
            self.rightButton,
            self.current 
        ]
        self.knownMics = list()
        self.currentMicIndex = 0

        self.update();
        X.addWidgetGroup( self, self.__indieArr )

    def getInputDevices( self ):

        self.knownMics = list()
        #so we don't have duplicates

        devices = i.sd.query_devices()
        #array of dicts

        for z in devices:
            
            if( int(z['max_input_channels']) > 0 ):
                self.knownMics.append( z["name"] )

    def micQuery( self ):

        assert len( self.knownMics ) > 0

        self.currentMicIndex = device = i.sd.default.device[0]

    def setMic( self, change ):
        #change = movement left or right (or none)

        if( change == -1 ):
            self.currentMicIndex -= 1
        elif( change == -1 ):
            self.currentMicIndex -= 1
        self.current.data = (
            self.knownMics[ self.currentMicIndex ]
        )

    def onChildPress( self,  kid ):

        if( not kid.isPostInit ):
            kid.isPostInit = True
            return

        print( 'user changed mic' )
        self.update()
        if( kid.data == SelectorWrapper.LEFT ):
            self.currentMicIndex -=1

        elif( kid.data == SelectorWrapper.RIGHT ):
            self.currentMicIndex +=1
        print( self.current.data )
        
    # call when you need to change
    #active mic
    def update( self ):
        
        self.updateKids()
        self.getInputDevices()
        #ghives us all known mics

        self.micQuery()
        #sets index of current/default mic 

        self.setMic(None)

    def updateKids( self ):
        for child in self.children:
            child.update() 
#calls update on children
class Manager( 
    i.GridLayout 
):

    def __init__( self, **kwargs ):

        super(i.GridLayout, self ).__init__(**kwargs)

        self.pitch = 0.0
        self.temp = i.numpy.ones( (10 ** 6, 2) )
        self.hzNoteDict = X.initMap( True )

        self.iWrapper = IndicatorWrapper( )
        self.sWrapper = SelectorWrapper( ) 

        self.S_WRAP_BTTN_WIDTH = 1/6
        self.S_WRAP_HEIGHT = X.WIN_HEIGHT * 1/6
        self.S_WRAP_BTTN_SPACING = X.WIN_WIDTH * 1/30

        self.add_widget( self.iWrapper )
        self.add_widget( self.sWrapper )

        self.layoutIWrapper( )
        self.layoutSWrapper( )

    def layoutLeftButton( self ):

        self.sWrapper.leftButton.pos = ( 
            (
                X.WIN_WIDTH * 4/6 + 
                self.S_WRAP_BTTN_SPACING
            ), 
            self.sWrapper.pos[1]
        )
        self.sWrapper.leftButton.size = (
            self.S_WRAP_BTTN_WIDTH,
            self.S_WRAP_HEIGHT
        )

    def layoutCurrent( self ):

        self.sWrapper.current.pos = ( 
            (
                self.sWrapper.leftButton.pos[0] + 
                self.sWrapper.leftButton.size[0] + 
                self.S_WRAP_BTTN_SPACING
            ),
            self.sWrapper.pos[1]
        ) 
        self.sWrapper.current.size  = ( 
            X.WIN_WIDTH * 1/6 ,
            self.S_WRAP_HEIGHT
        )

    def layoutRightButton( self ):

        self.sWrapper.rightButton.pos = ( 
            (
                self.sWrapper.current.size[0] +
                self.sWrapper.current.pos[0] + 
                self.S_WRAP_BTTN_SPACING
            ),
            self.sWrapper.pos[1]
        )
        self.sWrapper.rightButton.size = (
            self.S_WRAP_BTTN_WIDTH,
            self.S_WRAP_HEIGHT
        )

    def layoutIWrapper( self ):

        self.iWrapper.pos = ( 400, 400 )
        self.iWrapper.size = ( 
            X.WIN_WIDTH * 2/3, 
            X.WIN_HEIGHT
        )

        nKids = len( self.iWrapper.children )

        for index in range( 0, nKids ):

            k = self.iWrapper.children[index]
            k.size = (
                self.iWrapper.size[0],
                ( self.iWrapper.size[1] / nKids )
            )
            k.pos = ( 
                0, 
                index * 1/nKids * self.iWrapper.size[1]
            )

    def layoutSWrapper( self ):

        self.sWrapper.pos = ( 400, 400 )
        self.sWrapper.size = ( 800, 800 )

        self.layoutLeftButton()
        self.layoutCurrent()
        self.layoutRightButton()

    def sanityCheck( self ):
        assert len( self.iWrapper.children ) > 0 
        assert len(self.sWrapper.children) > 0 
        #assert len(self.children.length) == 2
 
    def getInput( self ):
        
        with i.sd.InputStream(
            channels=1, 
            callback = self.iWrapper.set
        ):
            i.sd.sleep( 1000 )

    def update( self ):
        
        self.getInput( )
        #self.iWrapper.update() not implemented
        self.sWrapper.update()
        
#app main; holds loop   
class Tuner( i.App ):

    def __init__(self, **kwargs):

        super( ).__init__(**kwargs)

    def build( self ):

        manager = Manager( )
        #manager.postInit( )
        i.Window.size = (
            X.WIN_WIDTH, 
            X.WIN_HEIGHT
        )
        FRAME_SIZE = 1

        i.Clock.schedule_interval(lambda dt: manager.update( ), FRAME_SIZE)

        return manager

#DO NOT SET PROPERTY NAMED 'CHILDREN'
#ON ANY CLASS
if __name__ == "__main__":
    Tuner().run( )
#DUDE, IT ALMOST WORKS!
#todo: control button text overflow
#set background images for button
#find a good window size
# set position of window on screen