from pygame.font import SysFont
from pygame import init

init()

# Set the size of the window
XWIN, YWIN = 600, 800

# Find the center
HALF_XWIN, HALF_YWIN = XWIN / 2, YWIN / 2

# Create the display
DISPLAY = (XWIN, YWIN)

# Fullscreen
FLAGS = 0

# Frame render rate
FPS = 60

# Set color codes
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)

# Set player settings
PLAYER_SIZE = (25, 35)
PLAYER_COLOR = GRAY
PLAYER_MAX_SPEED = 20
PLAYER_JUMPFORCE = 20
PLAYER_BONUS_JUMPFORCE = 70
GRAVITY = 0.98

# Set platform settings
PLATFORM_COLOR = BLACK
PLATFORM_COLOR_LIGHT = GRAY
PLATFORM_SIZE = (100, 10)
PLATFORM_DISTANCE_GAP = (50, 210)
MAX_PLATFORM_NUMBER = 10
BONUS_SPAWN_CHANCE = 10
BREAKABLE_PLATFORM_CHANCE = 12

# Set the fonts
LARGE_FONT = SysFont("", 128)
SMALL_FONT = SysFont("arial", 24)
