import pygame
from typing import Dict, List, Callable, Tuple
from enum import Enum
from .globals import get_engine

class MouseButton(Enum):
    LEFT = 1
    MIDDLE = 2
    RIGHT = 3

class KeyCode:
    SPACE = pygame.K_SPACE
    RETURN = pygame.K_RETURN
    ESCAPE = pygame.K_ESCAPE
    BACKSPACE = pygame.K_BACKSPACE
    TAB = pygame.K_TAB
    DELETE = pygame.K_DELETE
    INSERT = pygame.K_INSERT
    HOME = pygame.K_HOME
    END = pygame.K_END
    PAGE_UP = pygame.K_PAGEUP
    PAGE_DOWN = pygame.K_PAGEDOWN
    
    UP = pygame.K_UP
    DOWN = pygame.K_DOWN
    LEFT = pygame.K_LEFT
    RIGHT = pygame.K_RIGHT
    
    A = pygame.K_a
    B = pygame.K_b
    C = pygame.K_c
    D = pygame.K_d
    E = pygame.K_e
    F = pygame.K_f
    G = pygame.K_g
    H = pygame.K_h
    I = pygame.K_i
    J = pygame.K_j
    K = pygame.K_k
    L = pygame.K_l
    M = pygame.K_m
    N = pygame.K_n
    O = pygame.K_o
    P = pygame.K_p
    Q = pygame.K_q
    R = pygame.K_r
    S = pygame.K_s
    T = pygame.K_t
    U = pygame.K_u
    V = pygame.K_v
    W = pygame.K_w
    X = pygame.K_x
    Y = pygame.K_y
    Z = pygame.K_z
    
    ONE = pygame.K_1
    TWO = pygame.K_2
    THREE = pygame.K_3
    FOUR = pygame.K_4
    FIVE = pygame.K_5
    SIX = pygame.K_6
    SEVEN = pygame.K_7
    EIGHT = pygame.K_8
    NINE = pygame.K_9
    ZERO = pygame.K_0
    
    F1 = pygame.K_F1
    F2 = pygame.K_F2
    F3 = pygame.K_F3
    F4 = pygame.K_F4
    F5 = pygame.K_F5
    F6 = pygame.K_F6
    F7 = pygame.K_F7
    F8 = pygame.K_F8
    F9 = pygame.K_F9
    F10 = pygame.K_F10
    F11 = pygame.K_F11
    F12 = pygame.K_F12
    
    LSHIFT = pygame.K_LSHIFT
    RSHIFT = pygame.K_RSHIFT
    LCTRL = pygame.K_LCTRL
    RCTRL = pygame.K_RCTRL
    LALT = pygame.K_LALT
    RALT = pygame.K_RALT

class InputManager:
    def __init__(self) -> None:
        self.key_press_callbacks: Dict[int, List[Callable]] = {}
        self.key_release_callbacks: Dict[int, List[Callable]] = {}
        self.mouse_press_callbacks: Dict[int, List[Callable]] = {1: [], 2: [], 3: []}
        self.mouse_release_callbacks: Dict[int, List[Callable]] = {1: [], 2: [], 3: []}
        self.mouse_move_callbacks: List[Callable] = []
        self.mouse_wheel_callbacks: List[Callable] = []
    
    def on_key_press(self, key: int, callback: Callable) -> None:
        global _engine
        from .globals import get_engine
        _engine = get_engine()
        
        if not callable(callback):
            error_msg = f"Callback must be callable"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise TypeError(error_msg)
        
        if key not in self.key_press_callbacks:
            self.key_press_callbacks[key] = []
        self.key_press_callbacks[key].append(callback)
    
    def on_key_release(self, key: int, callback: Callable) -> None:
        global _engine
        from .globals import get_engine
        _engine = get_engine()
        
        if not callable(callback):
            error_msg = f"Callback must be callable"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise TypeError(error_msg)
        
        if key not in self.key_release_callbacks:
            self.key_release_callbacks[key] = []
        self.key_release_callbacks[key].append(callback)
    
    def on_mouse_press(self, button: int, callback: Callable) -> None:
        global _engine
        from .globals import get_engine
        _engine = get_engine()
        
        if not callable(callback):
            error_msg = f"Callback must be callable"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise TypeError(error_msg)
        
        if button not in self.mouse_press_callbacks:
            error_msg = f"Invalid mouse button: {button}. Use 1, 2, or 3"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise ValueError(error_msg)
        
        self.mouse_press_callbacks[button].append(callback)
    
    def on_mouse_release(self, button: int, callback: Callable) -> None:
        global _engine
        from .globals import get_engine
        _engine = get_engine()
        
        if not callable(callback):
            error_msg = f"Callback must be callable"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise TypeError(error_msg)
        
        if button not in self.mouse_release_callbacks:
            error_msg = f"Invalid mouse button: {button}. Use 1, 2, or 3"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise ValueError(error_msg)
        
        self.mouse_release_callbacks[button].append(callback)
    
    def on_mouse_move(self, callback: Callable) -> None:
        global _engine
        from .globals import get_engine
        _engine = get_engine()
        
        if not callable(callback):
            error_msg = f"Callback must be callable"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise TypeError(error_msg)
        
        self.mouse_move_callbacks.append(callback)
    
    def on_mouse_wheel(self, callback: Callable) -> None:
        global _engine
        from .globals import get_engine
        _engine = get_engine()
        
        if not callable(callback):
            error_msg = f"Callback must be callable"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise TypeError(error_msg)
        
        self.mouse_wheel_callbacks.append(callback)
    
    def is_key_down(self, key: int) -> bool:
        return pygame.key.get_pressed()[key]
    
    def is_mouse_down(self, button: int) -> bool:
        global _engine
        from .globals import get_engine
        _engine = get_engine()
        
        if button not in [1, 2, 3]:
            error_msg = f"Invalid mouse button: {button}. Use 1, 2, or 3"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise ValueError(error_msg)
        
        buttons = pygame.mouse.get_pressed()
        return buttons[button - 1]
    
    def get_mouse_position(self) -> Tuple[int, int]:
        return pygame.mouse.get_pos()
    
    def handle_event(self, event: pygame.event.Event) -> None:
        global _engine
        from .globals import get_engine
        _engine = get_engine()
        
        if event.type == pygame.KEYDOWN:
            if event.key in self.key_press_callbacks:
                for callback in self.key_press_callbacks[event.key]:
                    try:
                        callback()
                    except Exception as e:
                        error_msg = f"Error in key press callback: {str(e)}"
                        if _engine and _engine.error_handler:
                            _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
                        raise
        
        elif event.type == pygame.KEYUP:
            if event.key in self.key_release_callbacks:
                for callback in self.key_release_callbacks[event.key]:
                    try:
                        callback()
                    except Exception as e:
                        error_msg = f"Error in key release callback: {str(e)}"
                        if _engine and _engine.error_handler:
                            _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
                        raise
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in self.mouse_press_callbacks:
                for callback in self.mouse_press_callbacks[event.button]:
                    try:
                        callback(event.pos[0], event.pos[1])
                    except Exception as e:
                        error_msg = f"Error in mouse press callback: {str(e)}"
                        if _engine and _engine.error_handler:
                            _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
                        raise
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button in self.mouse_release_callbacks:
                for callback in self.mouse_release_callbacks[event.button]:
                    try:
                        callback(event.pos[0], event.pos[1])
                    except Exception as e:
                        error_msg = f"Error in mouse release callback: {str(e)}"
                        if _engine and _engine.error_handler:
                            _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
                        raise
        
        elif event.type == pygame.MOUSEWHEEL:
            for callback in self.mouse_wheel_callbacks:
                try:
                    callback(event.x, event.y)
                except Exception as e:
                    error_msg = f"Error in mouse wheel callback: {str(e)}"
                    if _engine and _engine.error_handler:
                        _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
                    raise
        
        elif event.type == pygame.MOUSEMOTION:
            for callback in self.mouse_move_callbacks:
                try:
                    callback(event.pos[0], event.pos[1])
                except Exception as e:
                    error_msg = f"Error in mouse move callback: {str(e)}"
                    if _engine and _engine.error_handler:
                        _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
                    raise