import numpy
import sounddevice as sd
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.dropdown import DropDown
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.gridlayout import GridLayout

class F( App ):

    def build( self ):
        t = GridLayout()
        layout = GridLayout(cols=2, row_force_default=True, row_default_height=40)
        layout.add_widget(Button(text='Hello 1', size_hint_x=None, width=100))
        layout.add_widget(Button(text='World 1'))
        layout.add_widget(Button(text='Hello 2', size_hint_x=None, width=100))
        layout.add_widget(Button(text='World 2'))
        t.add_widget( layout )
        layout.cols=2 
        layout.row_force_default=True 
        layout.row_default_height=40
        return layout
F().run()
