import pygame


class Terminal:
    def __init__(self, config):
        self.config = config
        self.output_lines = [
            "Terminal initialized. Type 'help' for available commands.",
            "System ready. All protocols nominal.",
            ""
        ]
        self.current_command = ""
        self.cursor_visible = True
        self.cursor_timer = 0
        self.show_progress = False
        self.progress_value = 0
        self.progress_complete = False
        self.current_page = 1
        self.total_pages = 1

    def add_to_output(self, text):
        """Добавляет текст в вывод терминала"""
        self.output_lines.append(text)
        if len(self.output_lines) > self.config.MAX_HISTORY_LINES:
            self.output_lines.pop(0)
        self.update_pagination()

    def clear_output(self):
        """Очищает вывод терминала"""
        self.output_lines.clear()
        self.update_pagination()
        self.add_to_output("Terminal output cleared.")
        self.add_to_output("")

    def start_progress(self):
        """Запускает progress bar"""
        self.show_progress = True
        self.progress_value = 0
        self.progress_complete = False

    def update_cursor(self):
        """Обновляет состояние мигающего курсора"""
        self.cursor_timer += 1
        if self.cursor_timer >= self.config.CURSOR_BLINK_RATE:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0

    def update_progress(self):
        """Обновляет progress bar"""
        if self.show_progress and not self.progress_complete:
            self.progress_value += self.config.PROGRESS_SPEED
            if self.progress_value >= 1:
                self.progress_value = 1
                self.progress_complete = True
                self.add_to_output("System protocol initialized successfully!")
                self.add_to_output("All systems operational.")
                self.add_to_output("")
                pygame.time.set_timer(pygame.USEREVENT, 2000)

    def update_pagination(self):
        """Обновляет информацию о пагинации"""
        self.total_pages = max(1, (len(self.output_lines) - 1) // self.config.VISIBLE_LINES + 1)
        if self.current_page > self.total_pages:
            self.current_page = self.total_pages

    def get_visible_lines(self):
        """Возвращает строки для текущей страницы"""
        start_idx = (self.current_page - 1) * self.config.VISIBLE_LINES
        end_idx = start_idx + self.config.VISIBLE_LINES
        return self.output_lines[start_idx:end_idx]

    def draw(self, surface):
        """Отрисовывает терминал на поверхности"""
        # Отрисовка области терминала
        terminal_rect = pygame.Rect(
            self.config.TERMINAL_MARGIN,
            self.config.TERMINAL_MARGIN,
            self.config.WIDTH - 2 * self.config.TERMINAL_MARGIN,
            self.config.HEIGHT - 2 * self.config.TERMINAL_MARGIN
        )
        pygame.draw.rect(surface, self.config.BLACK, terminal_rect)
        pygame.draw.rect(surface, self.config.WHITE, terminal_rect, 2)

        # Отрисовка истории команд и вывода
        visible_lines = self.get_visible_lines()
        for i, line in enumerate(visible_lines):
            try:
                text = self.config.medium_font.render(line, True, self.config.WHITE)
                surface.blit(text, (
                    self.config.TERMINAL_MARGIN + 20,
                    self.config.TERMINAL_MARGIN + 20 + i * self.config.LINE_SPACING
                ))
            except:
                # Fallback на системный шрифт в случае ошибки
                fallback_font = pygame.font.SysFont('courier', 24)
                text = fallback_font.render(line, True, self.config.WHITE)
                surface.blit(text, (
                    self.config.TERMINAL_MARGIN + 20,
                    self.config.TERMINAL_MARGIN + 20 + i * self.config.LINE_SPACING
                ))

        # Отрисовка текущей команды
        prompt_text = "> "
        try:
            prompt = self.config.medium_font.render(prompt_text, True, self.config.GREEN)
            command_text = self.config.medium_font.render(self.current_command, True, self.config.WHITE)
        except:
            fallback_font = pygame.font.SysFont('courier', 24)
            prompt = fallback_font.render(prompt_text, True, self.config.GREEN)
            command_text = fallback_font.render(self.current_command, True, self.config.WHITE)

        surface.blit(prompt, (
            self.config.TERMINAL_MARGIN + 20,
            self.config.HEIGHT - self.config.TERMINAL_MARGIN - 50
        ))
        surface.blit(command_text, (
            self.config.TERMINAL_MARGIN + 20 + prompt.get_width(),
            self.config.HEIGHT - self.config.TERMINAL_MARGIN - 50
        ))

        # Отрисовка курсора
        if self.cursor_visible:
            cursor_x = self.config.TERMINAL_MARGIN + 20 + prompt.get_width() + command_text.get_width()
            pygame.draw.line(
                surface, self.config.WHITE,
                (cursor_x, self.config.HEIGHT - self.config.TERMINAL_MARGIN - 50),
                (cursor_x, self.config.HEIGHT - self.config.TERMINAL_MARGIN - 50 + self.config.CURSOR_HEIGHT),
                2
            )

        # Отрисовка progress bar если нужно
        if self.show_progress:
            progress_width = self.config.WIDTH - 2 * self.config.TERMINAL_MARGIN - 40

            # Рамка progress bar
            pygame.draw.rect(
                surface,
                self.config.WHITE,
                (
                    self.config.TERMINAL_MARGIN + 20,
                    self.config.HEIGHT - self.config.TERMINAL_MARGIN - 100,
                    progress_width,
                    self.config.PROGRESS_BAR_HEIGHT
                ),
                1
            )

            # Заливка progress bar
            pygame.draw.rect(
                surface,
                self.config.WHITE,
                (
                    self.config.TERMINAL_MARGIN + 20,
                    self.config.HEIGHT - self.config.TERMINAL_MARGIN - 100,
                    int(progress_width * self.progress_value),
                    self.config.PROGRESS_BAR_HEIGHT
                )
            )

            # Текст прогресса
            progress_text = "Initializing system protocol..."
            percent_text = f"{int(self.progress_value * 100)}%"
            try:
                progress_render = self.config.medium_font.render(progress_text, True, self.config.WHITE)
                percent_render = self.config.medium_font.render(percent_text, True, self.config.WHITE)
            except:
                fallback_font = pygame.font.SysFont('courier', 24)
                progress_render = fallback_font.render(progress_text, True, self.config.WHITE)
                percent_render = fallback_font.render(percent_text, True, self.config.WHITE)

            surface.blit(progress_render, (
                self.config.TERMINAL_MARGIN + 20,
                self.config.HEIGHT - self.config.TERMINAL_MARGIN - 130
            ))
            surface.blit(percent_render, (
                self.config.WIDTH - self.config.TERMINAL_MARGIN - 70,
                self.config.HEIGHT - self.config.TERMINAL_MARGIN - 130
            ))

        # Отрисовка пагинации
        page_text = f"Page {self.current_page}/{self.total_pages}"
        try:
            page_render = self.config.medium_font.render(page_text, True, self.config.GREEN)
        except:
            fallback_font = pygame.font.SysFont('courier', 24)
            page_render = fallback_font.render(page_text, True, self.config.GREEN)

        surface.blit(page_render, (
            self.config.WIDTH - self.config.TERMINAL_MARGIN - 100,
            self.config.TERMINAL_MARGIN + 20
        ))