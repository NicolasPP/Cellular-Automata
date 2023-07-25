CELL_SIZE: int = 11
WINDOW_HEIGHT: int = 900
WINDOW_WIDTH: int = 980
IT_DELAY: float = 0.1  # seconds
BOARD_SIZE: tuple[int, int] = 700, 700
BACKGROUND: tuple[int, int, int] = 27, 32, 39
ALIVE_COLOR: tuple[int, int, int] = 170, 79, 30
DEAD_COLOR: tuple[int, int, int] = 35, 40, 49
BLOCK_FONT: str = "data/fonts/block_font.TTF"
TITLE_FONT_SIZE: int = 30
DEFAULT_PAD: int = 15
RIGHT_ARROW: str = ">"
LEFT_ARROW: str = "<"
MOUSECLICK_LEFT: int = 1
HOVER_COLOR: tuple[int, int, int] = 255, 255, 255
HOVER_ALPHA: int = 20
CELL_HOVER_ALPHA: int = 100
SPEED_STEP: float = 1.1

# -- JSON --
JSON_FILE_MODE: str = "r"
RULES_JSON: str = "data/variations.json"
DATA: str = "Data"
NAME: str = "Name"
BIRTH: str = "Birth"
SURVIVAL: str = "Survival"
