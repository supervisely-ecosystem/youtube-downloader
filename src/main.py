import supervisely as sly

from supervisely.app.widgets import Container

from src.ui.download import card_1
from src.ui.trim import card_2
from src.ui.upload import card_3


layout = Container(
    widgets=[card_1, card_2, card_3], 
    direction="vertical"
)
app = sly.Application(layout=layout)
