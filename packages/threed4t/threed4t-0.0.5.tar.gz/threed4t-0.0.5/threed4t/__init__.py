
from ursina import *
from ursina.shaders import  lit_with_shadows_shader, normals_shader
#Entity.default_shader = basic_lighting_shader
#Entity.default_shader = lit_with_shadows_shader
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.platformer_controller_2d import PlatformerController2d
from . import common
from .engine import Engine3D
from .mouse4t import Mouse4T
from .sequence4t import 動畫組合
from .audio4t import 載入聲音
from .light4t import PointLight4t, DirectionalLight4t, AmbientLight4t

模擬3D引擎 = Engine3D

__all__ = [ 
            '模擬3D引擎', 'Entity', 'EditorCamera', '載入聲音',
            '模擬進行中','模擬主迴圈', '色彩','color','Vec3','Vec4','Vec2',
            '按住的鍵', '滑鼠', '新增立方體', '新增6面貼圖方塊',
            '新增內面貼圖球體','新增球體', '新增物體', '新增方形平面', '新增直線',
            '新增圓形平面', '新增箭頭', '新增菱形體',
            '預約執行', '新增文字', '新增立方體線框', '新增方形線框',
            '動畫組合', '動作', '光影著色器', '法線著色器','刪除',
            '第1人稱視角操作', '複製', '點光源', '平行光', '環境光', '平台跳躍2D操作',
            '新增圓柱', '新增角柱', '新增多邊形平面', '新增多邊形線',
            ]


Text.default_font = common.msjh_font_path
print('字形設定: ', Text.default_font)

# shader
光影著色器 = lit_with_shadows_shader
法線著色器 = normals_shader

#動畫組合 = Sequence
動作 = Func

# color
色彩 = color


按住的鍵 = held_keys
滑鼠 = Mouse4T()

######## top level function
# import __main__
# __main__.按住的鍵 = held_keys



def 第1人稱視角操作():
    if not common.is_engine_created:
        Engine3D()

    common.stage.editor_camera.enabled = False
    common.player = FirstPersonController(y=2, origin_y=-.5) 

    return common.player


def 平台跳躍2D操作(圖片=''): 
    if not common.is_engine_created:
        Engine3D()


    #common.stage.editor_camera.enabled = False
    if 圖片 == '':
        common.player = PlatformerController2d(y=2, scale_y=1, max_jumps=2)
    else:
        common.player = PlatformerController2d(model='quad', texture=圖片,z=0.1, y=2, 
                                        scale_y=1, max_jumps=2, origin_y=-.5,  double_sided=True)

    return common.player


def simulate():
    if not common.is_engine_created:
        Engine3D()

    common.stage.simulate()


模擬主迴圈 = simulate
模擬進行中 = simulate

######## top level function

def add_cube(*args, **kwargs):
    if not common.is_engine_created:
        Engine3D()
    return common.stage.add_cube(*args, **kwargs)
新增立方體 = add_cube

def add_entity(*args, **kwargs):
    if not common.is_engine_created:
        Engine3D()
    return common.stage.add_entity(*args, **kwargs)
新增物體 = add_entity

def add_sphere(*args, **kwargs):
    if not common.is_engine_created:
        Engine3D()
    return common.stage.add_sphere(*args, **kwargs)
新增球體 = add_sphere

def add_cylinder(*args, **kwargs):
    if not common.is_engine_created:
        Engine3D()
    return common.stage.add_cylinder(*args, **kwargs)
新增圓柱 = add_cylinder

def add_prism(角=5, *args, **kwargs):
    if not common.is_engine_created:
        Engine3D()
    return common.stage.add_prism(side=角, *args, **kwargs)
新增角柱 = add_prism

def add_wireframe_cube(*args, **kwargs):
    if not common.is_engine_created:
        Engine3D()
    return common.stage.add_wireframe_cube(*args, **kwargs)
新增立方體線框 = add_wireframe_cube

def add_wireframe_quad(*args, **kwargs):
    if not common.is_engine_created:
        Engine3D()
    return common.stage.add_wireframe_quad(*args, **kwargs)
新增方形線框 = add_wireframe_quad


def add_polygon_line(邊=5, *args, **kwargs):
    if not common.is_engine_created:
        Engine3D()
    return common.stage.add_polygon_line(side=邊, *args, **kwargs)
新增多邊形線 = add_polygon_line

def add_line(長=10, 寬=3, *args, **kwargs):
    if not common.is_engine_created:
        Engine3D()
    return common.stage.add_line(length=長, thickness=寬, *args, **kwargs)
新增直線 = add_line


def add_quad(*args, **kwargs):
    if not common.is_engine_created:
        Engine3D()
    return common.stage.add_quad(*args, **kwargs)
新增方形平面 = add_quad

def add_polygon(邊=5, *args, **kwargs):
    if not common.is_engine_created:
        Engine3D()
    return common.stage.add_polygon(side=邊, *args, **kwargs)
新增多邊形平面 = add_polygon

def add_circle(*args, **kwargs):
    if not common.is_engine_created:
        Engine3D()
    return common.stage.add_circle(*args, **kwargs)
新增圓形平面 = add_circle

def add_arrow(*args, **kwargs):
    if not common.is_engine_created:
        Engine3D()
    return common.stage.add_arrow(*args, **kwargs)
新增箭頭 = add_arrow

def add_diamond(*args, **kwargs):
    if not common.is_engine_created:
        Engine3D()
    return common.stage.add_diamond(*args, **kwargs)
新增菱形體 = add_diamond


def add_cubic6(*args, **kwargs):
    if not common.is_engine_created:
        Engine3D()
    return common.stage.add_cubic6(*args, **kwargs)
新增6面貼圖方塊 = add_cubic6

def add_sphere_inward(*args, **kwargs):
    if not common.is_engine_created:
        Engine3D()
    return common.stage.add_sphere_inward(*args, **kwargs)
新增內面貼圖球體 = add_sphere_inward

def add_text(文字, *args, **kwargs):
    if not common.is_engine_created:
        Engine3D()
    kwargs['text'] = 文字
    return common.stage.add_text(*args, **kwargs)
新增文字 = add_text

複製 = duplicate
刪除 = destroy
#結合 = combine


點光源 = PointLight4t
平行光 = DirectionalLight4t
環境光 = AmbientLight4t
#聚光燈 = SpotLight

def 預約執行(函式, *args, 時間=1, **kwargs):
    kwargs['delay'] = 時間
    invoke(函式, *args, **kwargs)



if __name__ == '__main__' :
    pass
    
