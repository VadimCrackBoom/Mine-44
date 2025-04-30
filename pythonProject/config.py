import pygame
import os


class Config:
    def __init__(self):
        # Инициализация цветов
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.DARK_GREEN = (0, 100, 0)

        # Размеры
        self.WIDTH = 1920
        self.HEIGHT = 1080
        self.TERMINAL_MARGIN = 50
        self.LINE_SPACING = 30
        self.CURSOR_HEIGHT = 30
        self.PROGRESS_BAR_HEIGHT = 20

        # Настройки терминала
        self.MAX_HISTORY_LINES = 100
        self.VISIBLE_LINES = 20
        self.CURSOR_BLINK_RATE = 30
        self.PROGRESS_SPEED = 0.005

        # Шрифты
        self.font_path = os.path.join('fonts', 'couriernew.ttf')
        self.small_font = None
        self.medium_font = None
        self.large_font = None

        # Инициализируем шрифты сразу
        self.initialize_fonts()

    def initialize_fonts(self):
        """Инициализировать шрифты"""
        try:
            # Проверка существования файла шрифта
            if not os.path.exists(self.font_path):
                raise FileNotFoundError(f"Font file not found: {self.font_path}")

            # Загрузка шрифтов
            self.small_font = pygame.font.Font(self.font_path, 16)
            self.medium_font = pygame.font.Font(self.font_path, 24)
            self.large_font = pygame.font.Font(self.font_path, 32)

            # Проверка что шрифты загрузились
            if not all([self.small_font, self.medium_font, self.large_font]):
                raise RuntimeError("Failed to load one or more fonts")

        except Exception as e:
            print(f"Error loading custom fonts: {e}")
            print("Falling back to system fonts...")
            self.small_font = pygame.font.SysFont('courier', 16)
            self.medium_font = pygame.font.SysFont('courier', 24)
            self.large_font = pygame.font.SysFont('courier', 32)