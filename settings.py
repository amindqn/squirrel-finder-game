# settings.py

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Base Difficulty settings
BASE_DIFFICULTY_SETTINGS = {
    "Easy": {"player_speed": 5, "obstacle_speed": 3, "spawn_rate": 2000},
    "Medium": {"player_speed": 7, "obstacle_speed": 5, "spawn_rate": 1500},
    "Hard": {"player_speed": 10, "obstacle_speed": 7, "spawn_rate": 1000},
}

# Frame rate
FPS = 60

# Image sizes
SPRITE_SIZE = (40, 40)
