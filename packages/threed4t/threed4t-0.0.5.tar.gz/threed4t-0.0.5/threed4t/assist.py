#from panda3d.core import PerspectiveLens, OrthographicLens, LensNode, NodePath

from ursina import *
from . import common

# class CompassCube(Entity):
#     def __init__(self):
#         Entity.__init__(self, parent=camera.ui, model='cube', texture='white_cube',scale=0.1)
#         self.x = .4 * window.aspect_ratio
#         self.y = -.4

#     def update(self):
#         print('camara world position', camera.world_rotation)
#         self.rotation = camera.world_rotation * Vec3(-1,-1,-1)

class CorMark(Text):
    def __init__(self, axis_name):
        Text.size = 0.04
        Text.default_resolution = 1080 * Text.size
        super().__init__(text=axis_name)
        #self.color = color.gray
        self.axis_name = axis_name
        # enable update methon of entity
        self.ignore = False
        

        if self.axis_name == 'x':
            self.cone = common.cor_assist.cone_x
        elif self.axis_name == 'y':
            self.cone = common.cor_assist.cone_y
        else :
            self.cone = common.cor_assist.cone_z

    def update(self):        
        self.position = self.cone.screen_position
        #self.position = (0,0.3,0)
        
        #print(self.position)


class CorAssist:
    def __init__(self):
        # keep ref in common
        common.cor_assist = self

        self._enabled = False
        self.grid = Entity(model=Grid(40, 40), scale=40, 
                            rotation=(90, 0, 0), color=color.rgba(150,150,150,150))
        # self.grid2 = Entity(model=Grid(40, 40), scale=40, 
        #                     rotation=(90, 0, 0), color=color.rgb(100,100,100, 200))

        # line mesh 
        verts = (Vec3(5,0,0), Vec3(-5,0,0))
        tris = ((0,1), )
        self.line_x = Entity(model=Mesh(vertices=verts, triangles=tris, mode='line', thickness=2),
                             color=color.rgba(120, 239, 255))

        verts = (Vec3(0,5,0), Vec3(0,-5,0))
        tris = ((0,1), )
        self.line_y = Entity(model=Mesh(vertices=verts, triangles=tris, mode='line', thickness=2),
                             color=color.rgba(105, 255, 145))

        verts = (Vec3(0,0,5), Vec3(0,0,-5))
        tris = ((0,1), )
        self.line_z = Entity(model=Mesh(vertices=verts, triangles=tris, mode='line', thickness=2),
                             color=color.rgba(255, 123, 99))



        self.dots = []
        for i in range(-5, 6):
            if i != 0:
                #e = Entity(model='cube', scale=0.1, color=color.rgba(255,165,0,150),position=(i,0,0))
                #self.dots.append(e)

            
                e = Entity(model='cube', scale=0.1, color=color.rgba(0,255,0,150),position=(0,i,0))
                self.dots.append(e)

                #e = Entity(model='cube', scale=0.1, color=color.rgba(255,0,0,150),position=(0,0,i))
                #self.dots.append(e)




        # self.compass_cube = CompassCube()

        #cone
        self.cone_x = Entity(model=Cone(4, direction=(1,0,0)), color=color.rgba(255,165,0,150),position=(5,0,0),scale=0.5)
        self.cone_y = Entity(model=Cone(4, direction=(0,1,0)), color=color.rgba(0,255,0,150),position=(0,5,0),scale=0.5)
        self.cone_z = Entity(model=Cone(4, direction=(0,0,1)), color=color.rgba(255,0,0,150),position=(0,0,5),scale=0.5)

        # cor mark 
        self.mark_x = CorMark('x')
        self.mark_y = CorMark('y')
        self.mark_z = CorMark('z')

        self.disable_gizmo()

    def enable_gizmo(self):
        self.grid.enabled = True
        self.line_x.enabled = True
        self.line_y.enabled = True
        self.line_z.enabled = True
        for d in self.dots:
            d.enabled = True
        # self.compass_cube.enabled = True
        self.cone_x.enabled = True
        self.cone_y.enabled = True
        self.cone_z.enabled = True
        self.mark_x.enabled = True
        self.mark_y.enabled = True
        self.mark_z.enabled = True

    def disable_gizmo(self):
        self.grid.enabled = False
        self.line_x.enabled = False
        self.line_y.enabled = False
        self.line_z.enabled = False
        for d in self.dots:
            d.enabled = False
        # self.compass_cube.enabled = False
        self.cone_x.enabled = False
        self.cone_y.enabled = False
        self.cone_z.enabled = False
        self.mark_x.enabled = False
        self.mark_y.enabled = False
        self.mark_z.enabled = False



    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        if value :
            self._enabled = True
            self.enable_gizmo()
        else:
            self._enabled = False
            self.disable_gizmo()

            
               