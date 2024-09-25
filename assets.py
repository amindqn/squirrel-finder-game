# assets.py

from utils import load_image
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, SPRITE_SIZE

# Initialize image variables
koala_img = None
strawberry_img = None
squirrel_img = None
rock_img = None
background_img = None


def load_assets():
    global koala_img, strawberry_img, squirrel_img, rock_img, background_img
    koala_img = load_image("images/koala.png", SPRITE_SIZE)
    strawberry_img = load_image("images/strawberry.png", SPRITE_SIZE)
    squirrel_img = load_image("images/squirrel.png", SPRITE_SIZE)
    rock_img = load_image("images/rock.png", SPRITE_SIZE)
    background_img = load_image("images/background.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
