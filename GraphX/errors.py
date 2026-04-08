import pygame
import sys
from typing import Optional

class FatalError(Exception):
    pass

class ErrorHandler:
    def __init__(self) -> None:
        self.fatal_error: Optional[bool] = None
    
    def show_fatal_error(self, screen: Optional[pygame.Surface], message: str) -> None:
        if screen is None:
            pygame.quit()
            sys.exit(1)
        
        if not pygame.font.get_init():
            pygame.font.init()
        
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)
        
        lines = message.split('\n')
        wrapped_lines = []
        
        for line in lines:
            if not line.strip():
                wrapped_lines.append('')
                continue
                
            words = line.split()
            current_line = []
            
            for word in words:
                current_line.append(word)
                test_line = ' '.join(current_line)
                if font.size(test_line)[0] > screen.get_width() - 100:
                    if len(current_line) > 1:
                        current_line.pop()
                        wrapped_lines.append(' '.join(current_line))
                        current_line = [word]
                    else:
                        wrapped_lines.append(test_line)
                        current_line = []
            
            if current_line:
                wrapped_lines.append(' '.join(current_line))
        
        line_height = 40
        total_height = len(wrapped_lines) * line_height
        start_y = (screen.get_height() - total_height) // 2
        
        for i, line in enumerate(wrapped_lines):
            if line:
                text_surface = font.render(line, True, (255, 0, 0))
                text_rect = text_surface.get_rect(center=(screen.get_width() // 2, start_y + i * line_height))
                screen.blit(text_surface, text_rect)
        
        pygame.display.flip()
        
        self.fatal_error = True
        self._wait_for_exit()
    
    def _wait_for_exit(self) -> None:
        clock = pygame.time.Clock()
        waiting = True
        
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
            clock.tick(30)
        
        pygame.quit()
        sys.exit(1)