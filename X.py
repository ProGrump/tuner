
import i


#the perfect pitches of note names
#returns dict of notes2Pitch {(34.6): ('c#')}
def initMap( isSharp ):
    hzTable = [
    [32.7, 34.6, 36.7, 38.9, 41.2, 43.7, 46.2, 49.0, 51.9, 55.0, 58.3, 61.7],
    [65.4, 69.2, 73.4, 77.8, 82.4, 87.4, 92.4, 98.0, 103.8, 110.0, 116.6, 123.4],
    [130.8, 138.4, 146.8, 155.6, 164.8, 174.8, 184.8, 196.0, 207.6, 220.0, 233.2, 246.8],
    [261.6, 276.8, 293.6, 311.2, 329.6, 349.6, 369.6, 392.0, 415.2, 440.0, 466.4, 493.6],
    [523.2, 553.6, 587.2, 622.4, 659.2, 699.2, 739.2, 784.0, 830.4, 880.0, 932.8, 987.2],
    [1046.4, 1107.2, 1174.4, 1244.8, 1318.4, 1398.4, 1478.4, 1568.0, 1660.8, 1760.0, 1865.6, 1974.4] ,
    [2092.8, 2214.4, 2348.8, 2489.6, 2636.8, 2796.8, 2956.8, 3136.0, 3321.6, 3520.0, 3731.2, 3948.8]
    ]
    sharpNotes = [ 'C', 'C#', 'D', 'D#', 'E', 'F','F#', 'G', 'G#', 'A', 'A', 'A#', 'B' ]
    flatNotes = [ 'C', 'Db', 'D', 'Eb', 'E', 'F','Gb', 'G', 'Ab', 'A', 'Bb', 'B' ]

    hzNoteDict = {} 

    if( isSharp ):
        toUse = sharpNotes
    else:
        toUse = flatNotes

    for octave in hzTable:
        for i in range(0, 12):
            pitch = octave[i]
            note = toUse[i]
            hzNoteDict[ pitch ] = note
            
    return hzNoteDict

def makeWav( name ):
    
    return open( name + ".wav", "r+" )

def toHz( rawIn ):

    hz = i.numpy.mean( rawIn )

    if( hz > HIGHEST_PITCH ):
        return 3600.0
    elif( hz < LOWEST_PITCH):
        return 32.7
    return float( hz )

def getErr( inputHz, targetHz ):
    return targetHz - inputHz

#where inputHz is hz of a noteName (e.g., Bb)
def getClosest( inputHz, hzNoteDict ):

        pitches = list(
            hzNoteDict.keys()
        )
        high = len( pitches ) - 1
        low, i = 0, 0

        while( high >= low ):   

            i = int( (high + low) / 2 )

            if( pitches[i] < inputHz ): 
                low = i + 1

            elif( pitches[i] > inputHz ): 
                high = i - 1

            else: break
        return pitches[ i ] #hz of some note
        
def toNote( inputHz, hzNoteDict ):
    
    return hzNoteDict[ inputHz ]

def addWidgetGroup( root, widgets ):
    
    for i in widgets:
        root.add_widget( i )

LOWEST_PITCH = 32.7
HIGHEST_PITCH = 3520.0

WIN_WIDTH = int(900)
WIN_HEIGHT = int(900)

GREY = [0.3, 0.3, 0.3, 1]

HZ_NOTE_DICT = initMap( True )