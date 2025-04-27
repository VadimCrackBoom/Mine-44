import random
import pygame


class BinaryRain:
    def __init__(self, config):
        self.config = config
        self.binary_chars = ['0', '1']
        self.streams = []
        self.init_streams(150)

    def init_streams(self, count):
        for _ in range(count):
            self.streams.append({
                'x': random.randint(0, self.config.WIDTH),
                'y': random.randint(-1000, 0),
                'speed': random.uniform(5, 20),
                'length': random.randint(10, 40),
                'chars': [random.choice(self.binary_chars) for _ in range(random.randint(10, 40))]
            })

    def update(self):
        for stream in self.streams:
            stream['y'] += stream['speed']
            if stream['y'] > self.config.HEIGHT:
                stream['y'] = random.randint(-1000, -100)
                stream['chars'] = [random.choice(self.binary_chars) for _ in range(stream['length'])]

    def draw(self, surface):
        for stream in self.streams:
            for i, char in enumerate(stream['chars']):
                # Исправлено: цвет теперь передается как кортеж RGB
                alpha = min(255, max(0, 255 - i * (255 // stream['length'])))
                color = (alpha, alpha, alpha)

                if random.random() > 0.1:
                    try:
                        text = self.config.small_font.render(char, True, color)
                        surface.blit(text, (stream['x'], stream['y'] + i * 20))
                    except:
                        # Fallback на белый цвет в случае ошибки
                        text = self.config.small_font.render(char, True, (255, 255, 255))
                        surface.blit(text, (stream['x'], stream['y'] + i * 20))