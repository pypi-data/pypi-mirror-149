from ursina import *
#from ursina.shaders import lit_with_shadows_shader
from panda3d.core import Texture
from . import common
import cv2



class Entity4t(Entity):
    def __init__(self, *args, **kwargs):
        # handle default model and texture
        #custom model
        
        
        #if not 'model' in kwargs or kwargs['model'] == 'cube':
        if not 'model' in kwargs:
            # add_entity
            pass
        elif kwargs['model'] == 'cube':
            # default cube model 
            kwargs['model'] = 'cube'
            kwargs['texture'] = 'white_cube.png'
        elif kwargs['model'] == 'sphere':
            kwargs['texture'] = load_texture('white_gradient',common.texture4t_folder)
            

        elif kwargs['model'] == 'quad':
            kwargs['double_sided'] = True

        elif kwargs['model'] == 'circle':
            kwargs['double_sided'] = True

        elif kwargs['model'] == 'cylinder':
            kwargs['model'] = Cylinder(20, start=-0.5) 

        elif kwargs['model'] == 'polygon':
            side = int(kwargs['side'])
            if side < 3 :
                print('多邊形的邊需大於3')
                return
            kwargs['model'] = Circle(side) 

        elif kwargs['model'] == 'polygon_line':
            side = int(kwargs['side'])
            if side < 3 :
                print('多邊形線的邊需大於3')
                return
            kwargs['model'] = Circle(side, mode='line', thickness=3)

        elif kwargs['model'] == 'prism':
            side = int(kwargs['side'])
            if side < 3 :
                print('角柱的邊需大於3')
                return
            kwargs['model'] = Cylinder(side, start=-0.5)  

        elif kwargs['model'] == 'cubic_six_faces':
            # cubic with 6 face texture
            kwargs['model'] = load_model('cubic6', common.model4t_folder)
            kwargs['texture'] = load_texture('cubic6_colors',common.texture4t_folder)
            #print(self._texture)
            #print('here')
        elif kwargs['model'] == 'sphere_inward':
            kwargs['model'] = load_model('sphere_inward', common.model4t_folder)
            kwargs['texture'] = load_texture('test_grid.jpg',common.texture4t_folder)
        elif kwargs['model'] == 'line':
            length = kwargs['length']
            thickness = kwargs['thickness']
            # line mesh
            if length <= 0 or thickness <= 0 :
                print('線長及線寬需大於0')
                return
            half_length = length / 2
            verts = (Vec3(0, half_length, 0), Vec3(0, -half_length, 0))
            tris = ((0,1), )
            kwargs['model'] = Mesh(vertices=verts, triangles=tris, mode='line', thickness=thickness)


        else:
            pass

        if not 'collider' in kwargs:
           kwargs['collider'] = 'box'
        



        super().__init__(*args, **kwargs)

    def 位置動畫(self, 座標, 延遲=0, 持續=1):
        #座標 = Vec3(座標差[0], 座標差[1], 座標差[2],) + self.position
        self.animate_position(座標, delay=延遲 ,duration=持續, curve=curve.linear)

    def 旋轉動畫(self, 角度, 延遲=0, 持續=1):    
        self.animate_rotation(角度, delay=延遲 ,duration=持續, curve=curve.linear)

    def 縮放動畫(self, 比例, 延遲=0, 持續=1):    
        self.animate_scale(比例, delay=延遲 ,duration=持續, curve=curve.linear)

    def 顏色動畫(self, 顏色, 延遲=0, 持續=1):    
        self.animate_color(顏色, delay=延遲 ,duration=持續, curve=curve.linear)

    def 淡出(self, 持續=1):
        self.fade_out(duration=持續)

    def 淡入(self, 持續=1):
        self.fade_in(duration=持續, curve=curve.linear)

    def 閃爍(self, 持續=0.5):
        self.blink(duration=持續, curve=curve.linear)

    def 晃動(self):
        self.shake()

    def 面朝(self, target, 軸='forward'):
        self.look_at(target, 軸)

    def 結合子代(self):
        self.combine()

    @property
    def 模型(self):
        return self.model 

    @模型.setter
    def 模型(self, value):
        self.model = value 
        # remove previous texture
        #self._texture = None
        #self.setTextureOff(True)

    @property
    def 材質貼圖(self):
        self.setTextureOff(True)
        return self.texture 

    @材質貼圖.setter
    def 材質貼圖(self, value):
        self.texture = value

    @property
    def 多維陣列貼圖(self):
        self.setTextureOff(True)
        return self.texture 

    @多維陣列貼圖.setter
    def 多維陣列貼圖(self, buf):
        buf = cv2.flip(buf, -1)
        width = buf.shape[1]
        height = buf.shape[0]
        #print(width, height)

        
        common.ndarray_texure.setup2dTexture(width,height,
                Texture.T_unsigned_byte,Texture.F_rgb8)
        common.ndarray_texure.setRamImage(buf)
        
        # remove texture
        self.texture = None

        self.setTexture(common.ndarray_texure, True)
        #print('tex ',common.ndarray_texure)
        #self.texture = tex

    @property
    def 動畫清單(self):
        return self.animations 



    @property
    def 上層物件(self):
        return self.parent

    @上層物件.setter
    def 上層物件(self, value):
        self.parent = value

    @property
    def 親代(self):
        return self.parent

    @親代.setter
    def 親代(self, value):
        self.parent = value


    # enabled
    @property
    def 有效狀態(self):
        return self.enabled

    @有效狀態.setter
    def 有效狀態(self, value):
        self.enabled = value

    # color
    @property
    def 顏色(self):
        return self.color 

    @顏色.setter
    def 顏色(self, value):
        self.color = value

    # origin
    @property
    def 中心點偏移(self):
        return self.origin 

    @中心點偏移.setter
    def 中心點偏移(self, value):
        self.origin = value

    # position
    @property
    def 位置(self):
        return self.position 

    @位置.setter
    def 位置(self, value):
        self.position = value  

    @property
    def 位置x(self):
        return self.x 

    @位置x.setter
    def 位置x(self, value):
        self.x = value 

    @property
    def 位置y(self):
        return self.y 

    @位置y.setter
    def 位置y(self, value):
        self.y = value 

    @property
    def 位置z(self):
        return self.z 

    @位置z.setter
    def 位置z(self, value):
        self.z = value 

    @property
    def 全域位置(self):
        return self.world_position 

    @全域位置.setter
    def 全域位置(self, value):
        self.world_position = value 

    @property
    def 全域位置x(self):
        return self.world_x 

    @全域位置x.setter
    def 全域位置x(self, value):
        self.world_x = value 

    @property
    def 全域位置y(self):
        return self.world_y 

    @全域位置y.setter
    def 全域位置y(self, value):
        self.world_y = value 

    @property
    def 全域位置z(self):
        return self.world_z 

    @全域位置z.setter
    def 全域位置z(self, value):
        self.world_z = value 

    # rotation
    @property
    def 旋轉(self):
        return self.rotation 

    @旋轉.setter
    def 旋轉(self, value):
        self.rotation = value 

    @property
    def 旋轉x(self):
        return self.rotation_x 

    @旋轉x.setter
    def 旋轉x(self, value):
        self.rotation_x = value 

    @property
    def 旋轉y(self):
        return self.rotation_y 

    @旋轉y.setter
    def 旋轉y(self, value):
        self.rotation_y = value 

    @property
    def 旋轉z(self):
        return self.rotation_z 

    @旋轉z.setter
    def 旋轉z(self, value):
        self.rotation_z = value

    # @property
    # def 全域旋轉(self):
    #     return self.world_rotation 

    # @全域旋轉.setter
    # def 全域旋轉(self, value):
    #     self.world_rotation = value

    # @property
    # def 全域旋轉x(self):
    #     return self.world_rotation_x 

    # @全域旋轉x.setter
    # def 全域旋轉x(self, value):
    #     self.world_rotation_x = value

    # @property
    # def 全域旋轉y(self):
    #     return self.world_rotation_y 

    # @全域旋轉y.setter
    # def 全域旋轉y(self, value):
    #     self.world_rotation_y = value

    # @property
    # def 全域旋轉z(self):
    #     return self.world_rotation_z 

    # @全域旋轉z.setter
    # def 全域旋轉z(self, value):
    #     self.world_rotation_z = value

    # scale
    @property
    def 縮放(self):
        return self.scale 

    @縮放.setter
    def 縮放(self, value):
        self.scale = value 

    @property
    def 縮放x(self):
        return self.scale_x 

    @縮放x.setter
    def 縮放x(self, value):
        self.scale_x = value  

    @property
    def 縮放y(self):
        return self.scale_y 

    @縮放y.setter
    def 縮放y(self, value):
        self.scale_y = value 

    @property
    def 縮放z(self):
        return self.scale_z 

    @縮放z.setter
    def 縮放z(self, value):
        self.scale_z = value 

    @property
    def 全域縮放(self):
        return self.world_scale 

    @全域縮放.setter
    def 全域縮放(self, value):
        self.world_scale = value 

    @property
    def 全域縮放x(self):
        return self.world_scale_x 

    @全域縮放x.setter
    def 全域縮放x(self, value):
        self.world_scale_x = value 

    @property
    def 全域縮放y(self):
        return self.world_scale_y 

    @全域縮放y.setter
    def 全域縮放y(self, value):
        self.world_scale_y = value 

    @property
    def 全域縮放z(self):
        return self.world_scale_z 

    @全域縮放z.setter
    def 全域縮放z(self, value):
        self.world_scale_z = value 

    @property
    def 兩面貼圖(self):
        return self.double_sided 

    @兩面貼圖.setter
    def 兩面貼圖(self, value):
        self.double_sided = value

    @property
    def 著色器(self):
        return self.shader 

    @著色器.setter
    def 著色器(self, value):
        self.shader = value

    @property
    def 不可刪除(self):
        return self.eternal

    @不可刪除.setter
    def 不可刪除(self, value):
        self.eternal = value    