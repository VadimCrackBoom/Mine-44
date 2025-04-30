import pygame
import sys
from terminal import Terminal
from binary_rain import BinaryRain
from commands import CommandHandler
from config import Config


class HackerTerminal:
    def __init__(self):
        # Инициализация pygame
        pygame.init()

        # Конфигурация (шрифты инициализируются внутри Config)
        self.config = Config()

        # Настройка экрана
        self.screen = pygame.display.set_mode((self.config.WIDTH, self.config.HEIGHT))
        pygame.display.set_caption("Hacker Terminal Simulator")

        # Компоненты системы
        self.terminal = Terminal(self.config)
        self.binary_rain = BinaryRain(self.config)
        self.clock = pygame.time.Clock()
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.USEREVENT:
                self.terminal.show_progress = False
                pygame.time.set_timer(pygame.USEREVENT, 0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.process_command()
                elif event.key == pygame.K_BACKSPACE:
                    self.terminal.current_command = self.terminal.current_command[:-1]
                else:
                    self.terminal.current_command += event.unicode

    def process_command(self):
        if self.terminal.current_command.startswith("page "):
            try:
                page_num = int(self.terminal.current_command.split()[1])
                if 1 <= page_num <= self.terminal.total_pages:
                    self.terminal.current_page = page_num
            except (ValueError, IndexError):
                pass

        self.running = CommandHandler.execute(self.terminal.current_command, self.terminal)
        self.terminal.current_command = ""

    def update(self):
        self.terminal.update_cursor()
        self.terminal.update_progress()
        self.binary_rain.update()

    def draw(self):
        self.screen.fill(self.config.BLACK)
        self.binary_rain.draw(self.screen)
        self.terminal.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(30)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    app = HackerTerminal()
    app.run()