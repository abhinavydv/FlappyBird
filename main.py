from kivy.app import App, runTouchApp
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.clock import Clock
import random


kv="""
#: import Window kivy.core.window.Window

<Bird>:
    size_hint: root.normal_size_hint
    height: self.width
    pos_hint: {"x": .3}
    
    canvas:
        Rectangle:
            size: root.size
            pos: root.pos
            source: root.image

<PipeUp>:
    canvas.before: 
        
        Rectangle:
            size: root.size
            pos: root.pos
            source: root.image
            
<PipeDown>:
    canvas.before:
        Rectangle:
            size: root.size
            pos: root.pos[0], root.pos[1]
            source: root.image
            
        

<Pipes>:
    up: up
    down: down
    orientation: "vertical"
    size_hint: None, None
    size: Window.height*26/320, Window.height*2+root.gap
    canvas:
        Ellipse:
            size: (10,10)
            pos: root.center
    
    PipeUp:
        id: up
    Widget:
        size_hint: None, None
        height: root.gap #*Window.height
    PipeDown:
        id: down
        
        
<Ground>:
    canvas.after:
        Rectangle:
            size: root.size
            pos: root.pos
            source: root.image
            
<World>:
    ground: ground
    bird: bird
    score_lbl: score_lbl
    canvas.before:
        Rectangle:
            size: root.size
            pos: root.pos
            source: "assets/images/background-day.png"
    Ground:
        id: ground
    Label:
        id: score_lbl
        text: root.score
        pos_hint: {'x': .5, 'y': .8}
        font_size: 100
        size_hint: .1, .1
    Bird:
        id: bird
        pos_hint_x: .3
    
"""

Builder.load_string(kv)


class PipeUp(Widget):
    tag = "danger"
    image="assets/images/pipe-green-down.png"
    
    
class PipeDown(Widget):
    tag = "danger"
    image="assets/images/pipe-green-up.png"
    
    
class Pipes(BoxLayout):
    gap=.2*Window.height
    gap_pos=(0.5, 0.5)
    
    def move(self, v):
        self.x+=v
    
    
class Bird(Widget):
    tag="player"
    images=["assets/images/bluebird-upflap.png", "assets/images/bluebird-midflap.png", "assets/images/bluebird-downflap.png"]
    image=images[0]
    normal_size_hint=[0.08, None]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.velocity=[0,0]
        self.y=Window.height/2
        self.initial_g=-4000
        self.g=self.initial_g 
        self.status="alive"
        
    def fly(self):
        if self.status=="alive":
            self.velocity[1]=1000
        
    def update(self, dt):
        self.pos[0]+=self.velocity[0]*dt
        self.pos[1]+=self.velocity[1]*dt
        self.velocity[1]+=self.g*dt

    def die(self, dt):
        self.update(dt)

    
class Ground(Widget):
    size_hint=(1,.1)
    image="assets/images/base.png"
 

class Spawner:
    def __init__(self, world, **kwargs):
        super().__init__(**kwargs)
        self.world = world
        self.pipes=[]
        self.initial_v=-100
        self.velocity=self.initial_v
        self.initial_t=4
        self.timer=self.initial_t
        self.time=self.timer
                 
    def spawn(self, dt):
        if self.time> self.timer:
            self.time=0
            pipe = Pipes()
            self.pipes.append(pipe)
            pipe.center=[Window.width+pipe.width, random.randint(int(pipe.gap+self.world.ground.height), int(Window.height-pipe.gap))]
            self.world.add_widget(pipe)
        self.time+=dt

    def collides(self):
        if self.world.bird.status!="collided":
            for i in self.pipes:
                if i.up.collide_widget(self.world.bird) or  i.down.collide_widget(self.world.bird):
                    return True 
        if self.world.ground.collide_widget(self.world.bird):
                self.world.bird.fly()
                self.world.bird.y=self.world.ground.height+2
                return True
                
    def clear(self):
        for i in self.pipes:
            self.world.remove_widget(i)
        self.pipes.clear()
        
  
    def update(self, dt):
        c=0
        bird=self.world.bird
        if self.collides():
            if self.world.bird.status=="collided":
                self.world.status="stopped"
                return
            self.world.bird.status="collided"
            self.world.bird.size_hint_x*=2
        
        for i in self.pipes:
            if i.center>=bird.center:
                c=1
            i.move(self.velocity*dt)
            if i.center<bird.center and c==1:
                self.world.increase_score()
            c=0
            if i.x<-i.width:
                self.pipes.remove(i)
                self.world.remove_widget(i)
    
                
class World(FloatLayout):
    score="0"
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.spawner = Spawner(self)
        self.status="waiting"
        self.score=0

    def on_touch_down(self, touch):
        self.touched()
        
    def touched(self):
        if self.status=="waiting":
            self.status = "running"
            Clock.schedule_interval(self.update, .01)
            self.bird.fly()
        elif self.status=="stopped":
            self.spawner.clear()
            self.score=-1
            self.increase_score()
            self.status="running"
            self.bird.y=Window.height/2
            self.bird.status="alive"
            self.bird.fly()
            self.bird.g=self.bird.initial_g
            self.spawner.timer=self.spawner.initial_t
            self.spawner.time=self.spawner.timer
            self.spawner.velocity=self.spawner.initial_v
            self.bird.size_hint=self.bird.normal_size_hint
        elif self.status=="running":
            self.bird.fly()
        
    def update(self, dt):
        if self.status == "running":
            self.bird.update(dt)
            self.spawner.update(dt)
            self.spawner.spawn(dt)
            self.bird.g-=10*dt
            self.spawner.velocity-=3*dt
            if self.spawner.timer>0.5:
                self.spawner.timer=self.spawner.initial_v*self.spawner.initial_t/self.spawner.velocity
        elif self.status=="collided":
            self.bird.die(dt)
                
    def increase_score(self):
        self.score+=1
        self.score_lbl.text=str(self.score)

    
runTouchApp(World())
    