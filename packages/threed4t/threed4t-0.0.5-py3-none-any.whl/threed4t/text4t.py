from ursina import *
from panda3d.core import Texture
from . import common
from .entity4t import Entity4t


class Text4t(Text, Entity4t):
    def __init__(self, *args, **kwargs):
        # handle default model and texture
        #custom model

        if '尺寸' in kwargs:
            if kwargs['尺寸'] == '最大':
                Text.size = .2
            elif kwargs['尺寸'] == '大':
                Text.size = .15
            elif kwargs['尺寸'] == '小':
                Text.size = .05
            elif kwargs['尺寸'] == '最小':
                Text.size = .025
            else:
                Text.size = .1  # 中
        else:
            Text.size = .1  # default 中

        

        print('Text.size :', Text.size)

        Text.default_resolution = 1080 * Text.size
        

        #kwargs['font'] = common.msjh_font_path
        #print(kwargs['font'])
        Text.__init__(self,  *args, **kwargs)

        #self._font.setPageSize(256, 256)
        #self._font.setPixelsPerUnit(120)
        #self.text = '11中文測試'

    # def 位置動畫(self, 座標, 延遲=0, 持續=1):
    #     #座標 = Vec3(座標差[0], 座標差[1], 座標差[2],) + self.position
    #     self.animate_position(座標, delay=延遲 ,duration=持續)

    # def 旋轉動畫(self, 角度, 延遲=0, 持續=1):    
    #     self.animate_rotation(角度, delay=延遲 ,duration=持續)

    # def 縮放動畫(self, 比例, 延遲=0, 持續=1):    
    #     self.animate_scale(比例, delay=延遲 ,duration=持續)

    # def 顏色動畫(self, 顏色, 延遲=0, 持續=1):    
    #     self.animate_color(顏色, delay=延遲 ,duration=持續)

    # def 淡出(self, 持續=1):
    #     self.fade_out(duration=持續)

    # def 淡入(self, 持續=1):
    #     self.fade_in(duration=持續)

    def 逐字動畫(self, 速度=0.2):
        self.appear(speed=速度)

    @property
    def 背景(self):
        return self.background

    @背景.setter
    def 背景(self, value):
        self.background = value 


    @property
    def 文字(self):
        return self.text

    @文字.setter
    def 文字(self, value):
        self.text = value 
        # remove previous texture
        #self._texture = None
        #self.setTextureOff(True)

    # @property
    # def 模型(self):
    #     return self.model 

    # @模型.setter
    # def 模型(self, value):
    #     self.model = value 
    #     # remove previous texture
    #     #self._texture = None
    #     #self.setTextureOff(True)

    # @property
    # def 材質貼圖(self):
    #     self.setTextureOff(True)
    #     return self.texture 

    # @模型.setter
    # def 材質貼圖(self, value):
    #     self.texture = value

    # @property
    # def 多維陣列貼圖(self):
    #     self.setTextureOff(True)
    #     return self.texture 

    # @模型.setter
    # def 多維陣列貼圖(self, buf):
    #     buf = cv2.flip(buf, -1)
    #     width = buf.shape[1]
    #     height = buf.shape[0]
    #     #print(width, height)

        
    #     common.ndarray_texure.setup2dTexture(width,height,
    #             Texture.T_unsigned_byte,Texture.F_rgb8)
    #     common.ndarray_texure.setRamImage(buf)
        
    #     # remove texture
    #     self.texture = None

    #     self.setTexture(common.ndarray_texure, True)
    #     #print('tex ',common.ndarray_texure)
    #     #self.texture = tex

    # @property
    # def 動畫清單(self):
    #     return self.animations 



    # @property
    # def 上層物件(self):
    #     return self.parent

    # @模型.setter
    # def 上層物件(self, value):
    #     self.parent = value

    # # enabled
    # @property
    # def 有效狀態(self):
    #     return self.enabled

    # @有效狀態.setter
    # def 有效狀態(self, value):
    #     self.enabled = value

    # # color
    # @property
    # def 顏色(self):
    #     return self.color 

    # @顏色.setter
    # def 顏色(self, value):
    #     self.color = value

    # # origin
    # @property
    # def 中心點偏移(self):
    #     return self.origin 

    # @中心點偏移.setter
    # def 中心點偏移(self, value):
    #     self.origin = value

    # # position
    # @property
    # def 位置(self):
    #     return self.position 

    # @位置.setter
    # def 位置(self, value):
    #     self.position = value  

    # @property
    # def 位置x(self):
    #     return self.x 

    # @位置x.setter
    # def 位置x(self, value):
    #     self.x = value 

    # @property
    # def 位置y(self):
    #     return self.y 

    # @位置y.setter
    # def 位置y(self, value):
    #     self.y = value 

    # @property
    # def 位置z(self):
    #     return self.z 

    # @位置z.setter
    # def 位置z(self, value):
    #     self.z = value 

    # @property
    # def 全域位置(self):
    #     return self.world_position 

    # @全域位置.setter
    # def 全域位置(self, value):
    #     self.world_position = value 

    # @property
    # def 全域位置x(self):
    #     return self.world_x 

    # @全域位置x.setter
    # def 全域位置x(self, value):
    #     self.world_x = value 

    # @property
    # def 全域位置y(self):
    #     return self.world_y 

    # @全域位置y.setter
    # def 全域位置y(self, value):
    #     self.world_y = value 

    # @property
    # def 全域位置z(self):
    #     return self.world_z 

    # @全域位置z.setter
    # def 全域位置z(self, value):
    #     self.world_z = value 

    # # rotation
    # @property
    # def 旋轉(self):
    #     return self.rotation 

    # @旋轉.setter
    # def 旋轉(self, value):
    #     self.rotation = value 

    # @property
    # def 旋轉x(self):
    #     return self.rotation_x 

    # @旋轉x.setter
    # def 旋轉x(self, value):
    #     self.rotation_x = value 

    # @property
    # def 旋轉y(self):
    #     return self.rotation_y 

    # @旋轉y.setter
    # def 旋轉y(self, value):
    #     self.rotation_y = value 

    # @property
    # def 旋轉z(self):
    #     return self.rotation_z 

    # @旋轉z.setter
    # def 旋轉z(self, value):
    #     self.rotation_z = value

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

    # # scale
    # @property
    # def 縮放(self):
    #     return self.scale 

    # @縮放.setter
    # def 縮放(self, value):
    #     self.scale = value 

    # @property
    # def 縮放x(self):
    #     return self.scale_x 

    # @縮放x.setter
    # def 縮放x(self, value):
    #     self.scale_x = value  

    # @property
    # def 縮放y(self):
    #     return self.scale_y 

    # @縮放y.setter
    # def 縮放y(self, value):
    #     self.scale_y = value 

    # @property
    # def 縮放z(self):
    #     return self.scale_z 

    # @縮放z.setter
    # def 縮放z(self, value):
    #     self.scale_z = value 

    # @property
    # def 全域縮放(self):
    #     return self.world_scale 

    # @全域縮放.setter
    # def 全域縮放(self, value):
    #     self.world_scale = value 

    # @property
    # def 全域縮放x(self):
    #     return self.world_scale_x 

    # @全域縮放x.setter
    # def 全域縮放x(self, value):
    #     self.world_scale_x = value 

    # @property
    # def 全域縮放y(self):
    #     return self.world_scale_y 

    # @全域縮放y.setter
    # def 全域縮放y(self, value):
    #     self.world_scale_y = value 

    # @property
    # def 全域縮放z(self):
    #     return self.world_scale_z 

    # @全域縮放z.setter
    # def 全域縮放z(self, value):
    #     self.world_scale_z = value 

    # @property
    # def 兩面貼圖(self):
    #     return self.double_sided 

    # @兩面貼圖.setter
    # def 兩面貼圖(self, value):
    #     self.double_sided = value
    