import supervisely as sly
import os

from supervisely.app.widgets import Container

from src.ui.check_source import card_0
from src.ui.download import card_1
from src.ui.trim import card_2
from src.ui.upload import card_3


layout = Container(
    widgets=[card_0, card_1, card_2, card_3], 
    direction="vertical"
)

if not os.path.exists('src/videos/'):
    os.makedirs('src/videos/')

app = sly.Application(layout=layout, static_dir='src/videos/')
