from kivy.app import App, runTouchApp
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.lang.builder import Builder


kv="""
#: import Window kivy.core.window.Window

<Bird>:
    size_hint: .08, None
    height: self.width
    pos_hint: {"x": .3}
    
    canvas:
        Rectangle:
            size: root.size
            pos: root.pos
            source: root.image

<PipeUp>:
    canvas: 
        
        Rectangle:
            size: root.size
            pos: root.pos
            source: root.image
            
<PipeDown>:
    canvas:
        Rectangle:
            size: root.size
            pos: root.pos[0], root.pos[1]
            source: root.image
            
        

<Pipes>:
    orientation: "vertical"
    size_hint: None, None
    size: Window.height*26/320, Window.height+root.gap
    canvas:
        Ellipse:
            size: (10,10)
            pos: root.center
    
    PipeUp:
    Widget:
        size_hint: None, None
        height: root.gap #*Window.height
    PipeDown:
        
        
<Ground>:
    canvas:
        Rectangle:
            size: root.size
            pos: root.pos
            source: root.image
            
<World>:
    Ground:
    
"""

Builder.load_string(kv)


class PipeUp(Widget):
    tag = "danger"
    image="assets/images/pipe-green-down.png"
    
    
class PipeDown(Widget):
    tag = "danger"
    image="assets/images/pipe-green-up.png"
    
    
class Pipes(BoxLayout):
    gap=.1*Window.height
    gap_pos=(0.5, 0.5)
    
    def move(self, dt):
        pass
    
    
class Bird(Widget):
    tag="player"
    images=["assets/images/bluebird-upflap.png", "assets/images/bluebird-midflap.png", "assets/images/bluebird-downflap.png"]
    image=images[0]
    
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pos=[self.pos[0],Window.height/2]
        velocity=0

    
class Ground(Widget):
    size_hint=(1,.1)
    image="assets/images/base.png"
    
    
class World(FloatLayout):
    pass
    
    
runTouchApp(World())
    