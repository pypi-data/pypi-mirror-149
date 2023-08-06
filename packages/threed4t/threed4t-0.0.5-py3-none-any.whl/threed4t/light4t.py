from ursina import *

class PointLight4t(PointLight):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def 顏色(self):
        return self.color 

    @顏色.setter
    def 顏色(self, value):
        self.color = value

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

    def 面朝(self, target, 軸='forward'):
        self.look_at(target, 軸)


class DirectionalLight4t(DirectionalLight):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def 顏色(self):
        return self.color 

    @顏色.setter
    def 顏色(self, value):
        self.color = value

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

    def 面朝(self, target, 軸='forward'):
        self.look_at(target, 軸)

class AmbientLight4t(AmbientLight):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def 顏色(self):
        return self.color 

    @顏色.setter
    def 顏色(self, value):
        self.color = value

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

    def 面朝(self, target, 軸='forward'):
        self.look_at(target, 軸)