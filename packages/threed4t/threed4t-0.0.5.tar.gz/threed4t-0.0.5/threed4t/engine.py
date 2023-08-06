from inspect import signature

from ursina import *
from ursina.scene import instance as scene
from direct.showbase.ShowBase import ShowBase

from . import common
from .repl_panda import Repl
from .entity4t import Entity4t
from .text4t import Text4t
from .assist import CorAssist


import __main__

class Engine3D(Ursina, Repl):
    __single = None
    __first_time = True

    def __new__(clz, *args, **kwargs):
        # Singleton
        if not Engine3D.__single:
            Engine3D.__single = object.__new__(clz)
        else:
            print("模擬3D舞台已存在")

        return Engine3D.__single

    def __init__(self, *args, **kwargs):
        # check module level default physics engine
        if Engine3D.__first_time:
            self.do_init(*args, **kwargs)
            Engine3D.__first_time = False


        

    def do_init(self, 寬=common.WIN_WIDTH, 
                       高=common.WIN_HEIGHT, 
                       title=common.TITLE):  

        common.stage = self
        common.舞台 = self        
        common.is_engine_created = True
        __main__.stage = self
        __main__.舞台 = self

        #ursina 
        self.window = window
        

        if common.WIN_MIN_WIDTH < 寬 < common.WIN_MAX_WIDTH:
            self.win_width = round(寬,0)
        elif 寬 < common.WIN_MIN_WIDTH :
            self.win_width = common.WIN_MIN_WIDTH
        elif 寬 > common.WIN_MAX_WIDTH :
            self.win_width = common.WIN_MAX_WIDTH
        else:
            self.win_width = common.WIN_WIDTH

        if common.WIN_MIN_HEIGHT < 高 < common.WIN_MAX_HEIGHT:
            self.win_height = round(高,0)
        elif 高 < common.WIN_MIN_HEIGHT :
            self.win_height = common.WIN_MIN_HEIGHT
        elif 高 > common.WIN_MAX_HEIGHT :
            self.win_height = common.WIN_MAX_HEIGHT   
        else:
            self.win_height = common.WIN_HEIGHT    


        Ursina.__init__(self)

        self.window.windowed_size = Vec2(self.win_width,self.win_height)
        self.window.title = title
        self.window.borderless = False
        self.window.fullscreen = False
        self.window.fps_counter.enabled = False
        self.window.exit_button.visible = False
        self.window.cog_button.enabled = False
        
        self.window.position = (50, 50)

        print(f"建立舞台(寬{self.win_width}x高{self.win_height})")

        self.scene = scene
        self.camera_ui = camera.ui

        

        #editor camera
        self.editor_camera = EditorCamera()
        #self.editor_camera.gizmo.enabled = False

        # custom event handler
        self.user_update_handler = None 
        self.user_key_press_handler = None
        self.user_key_release_handler = None
        #self.user_key_hold_handler = None

        #cor assist 
        self.cor_assist = CorAssist()

    def input_up(self, key):
        if self.user_key_release_handler:
            if key in self._input_name_changes:
                k = self._input_name_changes[key]
                self.user_key_release_handler(k)
            else:
                self.user_key_release_handler(key)
        Ursina.input_up(self, key)

    # def input_hold(self, key):
    #     if self.user_key_hold_handler:
    #         self.user_key_hold_handler(key)

    #     Ursina.input_hold(self, key)

    def _update(self, task):
        if self.user_update_handler:
            dt = globalClock.getDt() * application.time_scale
            self.user_update_handler(dt)
        
        return Ursina._update(self, task)

    def input(self, key):
        if key == 'control':
            self.cor_assist.enabled = not self.cor_assist.enabled

        if key == 'escape' :
            application.quit()

        if self.user_key_press_handler :
            #print('do key press')
            if key in self._input_name_changes:
                k = self._input_name_changes[key]
                self.user_key_press_handler(k)
            else:
                self.user_key_press_handler(key)

        #print('my input:', key)
        Ursina.input(self, key)




    def collect_user_event_handlers(self):
        if hasattr(__main__, '當按下時'):
            # check number of parameters
            sig = signature(__main__.當按下時)
            if len(sig.parameters) == 1:
                 
                self.user_key_press_handler = __main__.當按下時
                print( '登錄事件函式：當按下時' )
            else:
                print('事件函式錯誤: 當按下時 需要1個參數')
                sys.exit()

        if hasattr(__main__, '當放開時'):
            # check number of parameters
            sig = signature(__main__.當放開時)
            if len(sig.parameters) == 1:
                 
                self.user_key_release_handler = __main__.當放開時
                print( '登錄事件函式：當放開時' )
            else:
                print('事件函式錯誤: 當放開時 需要1個參數')
                sys.exit()


        if hasattr(__main__, '當更新時'):
            # check number of parameters
            sig = signature(__main__.當更新時)
            if len(sig.parameters) == 1:
                  
                self.user_update_handler = __main__.當更新時
                print( '登錄事件函式：當更新時' )
            else:
                print('事件函式錯誤: 當更新時 需要1個參數')
                sys.exit()

    # def input_up(self, key):
    #     print('my input up:', key)
    #     Ursina.input_up(self, key)

    # def input_hold(self, key):
    #     print('my input hold:', key)
    #     Ursina.input_hold(self, key)

    def simulate(self):
        
        #self.lazy_setup()
        self.collect_user_event_handlers()
        #self.start_repl()

        

        # try cursor
        #cur = self.get_system_mouse_cursor('crosshair')
        #cur = self.get_system_mouse_cursor('help')
        # set cursor to default
        #cur = self.get_system_mouse_cursor('help')
        #self.set_mouse_cursor(None)

        self.is_engine_running = True

        
        ShowBase.run(self)    

    # add basic model

    def add_cube(self, *args, **kwargs):
        e = Entity4t(model='cube', *args, **kwargs)
        return e

    def add_entity(self, *args, **kwargs):
        e = Entity4t( *args, **kwargs)
        return e

    def add_sphere(self, *args, **kwargs):
        e = Entity4t(model='sphere', *args, **kwargs)
        return e

    def add_cylinder(self, *args, **kwargs):
        e = Entity4t(model='cylinder', *args, **kwargs)
        return e

    def add_prism(self, side, *args, **kwargs):
        e = Entity4t(model='prism', side=side, *args, **kwargs)
        return e

    def add_polygon(self, side, *args, **kwargs):
        e = Entity4t(model='polygon', side=side, *args, **kwargs)
        return e

    def add_polygon_line(self, side, *args, **kwargs):
        e = Entity4t(model='polygon_line', side=side, *args, **kwargs)
        return e

    def add_quad(self, *args, **kwargs):
        e = Entity4t(model='quad', *args, **kwargs)
        return e

    def add_circle(self, *args, **kwargs):
        e = Entity4t(model='circle', *args, **kwargs)
        return e

    def add_arrow(self, *args, **kwargs):
        e = Entity4t(model='arrow', *args, **kwargs)
        return e

    def add_diamond(self, *args, **kwargs):
        e = Entity4t(model='diamond', *args, **kwargs)
        return e


    # add special model

    def add_cubic6(self, *args, **kwargs):
        e = Entity4t(model='cubic_six_faces', *args, **kwargs)
        return e

    def add_sphere_inward(self, *args, **kwargs):
        e = Entity4t(model='sphere_inward', *args, **kwargs)
        return e

    def add_wireframe_cube(self, *args, **kwargs):
        e = Entity4t(model='wireframe_cube', *args, **kwargs)
        return e

    def add_wireframe_quad(self, *args, **kwargs):
        e = Entity4t(model='wireframe_quad', *args, **kwargs)
        return e

    def add_line(self, length, thickness, *args, **kwargs):
        e = Entity4t(model='line', length=length, thickness=thickness,  *args, **kwargs)
        return e

    
    def add_text(self, *args, **kwargs):
        t = Text4t(*args, **kwargs)
        return t




    ## property
    @property
    def 全螢幕(self):
        return self.window.fullscreen 

    @全螢幕.setter
    def 全螢幕(self, value):
        self.window.fullscreen = value


    @property
    def 視窗邊框(self):
        return not self.window.borderless 

    @視窗邊框.setter
    def 視窗邊框(self, value):
       self.window.borderless = not value 

    @property
    def 背景顏色(self):
        return self.window.color 

    @背景顏色.setter
    def 背景顏色(self, value):
        self.window.color = value

    @property
    def 介面上邊(self):
        return self.window.top 

    @property
    def 介面中心(self):
        return self.window.center 

    @property
    def 介面下邊(self):
        return Vec2(0, -.5) 

    @property
    def 介面左邊(self):
        return self.window.left 

    @property
    def 介面右邊(self):
        return self.window.right

    @property
    def 介面右上(self):
        return self.window.top_right

    @property
    def 介面左上(self):
        return self.window.top_left

    @property
    def 介面右下(self):
        return self.window.bottom_right

    @property
    def 介面左下(self):
        return self.window.bottom_left

    @property
    def 空間場景(self):
        return self.scene

    @property
    def 使用者介面(self):
        return self.camera_ui