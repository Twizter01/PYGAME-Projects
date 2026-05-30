from enum import Enum

class CMD_colors(Enum):
    INTRO_COLOR: str = 'cyan'
    PLAYER_STATS: str = 'yellow'
    ROOM_COLORS: tuple[str, ...] = ("slate_blue3", "medium_purple2", "hot_pink2", "light_goldenrod2", "light_cyan3")
    MESSAGES: str = "medium_spring_green"