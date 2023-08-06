from panda3d.core import Texture
import os 
from pathlib import Path

WIN_WIDTH = 400
WIN_HEIGHT = 600

###

WIN_MIN_WIDTH = 300
WIN_MIN_HEIGHT = 300
WIN_MAX_WIDTH = 1600
WIN_MAX_HEIGHT = 1000


TITLE = '模擬3D程式'

### common var
is_engine_created = False

# stage is a 3d engine
stage = None
舞台 = None
cor_assist = None

# path
from pathlib import Path

package_folder = Path(__file__).parent
model4t_folder = package_folder / 'model4t/'
texture4t_folder = package_folder / 'texture4t/'

# ndarray_texure
ndarray_texure = Texture()

# windows font path
drive_letter = os.getenv('SystemDrive')[0].lower() 
msjh_font_path =  '/{}/Windows/Fonts/msjh.ttc'.format(drive_letter)