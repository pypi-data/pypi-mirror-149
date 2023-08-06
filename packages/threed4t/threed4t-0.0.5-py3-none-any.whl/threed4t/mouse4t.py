from ursina import mouse


class Mouse4T:
    @property
    def 位置x(self):
        return mouse.x 

    @property
    def 位置y(self):
        return mouse.y

    @property
    def 位置(self):
        return mouse.position

    @property
    def 接觸物體(self):
        return mouse.hovered_entity 

    @property
    def 接觸點(self):
        return mouse.point 

    @property
    def 按下左鍵(self):
        return mouse.left

    @property
    def 接觸面法線(self):
        return mouse.normal
