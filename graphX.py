import pygame
import sys
import math
import os
from enum import Enum

_engine = None

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

class FatalError(Exception):
    pass

class ErrorHandler:
    def __init__(self):
        self.fatal_error = None
    
    def show_fatal_error(self, screen, message):
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
    
    def _wait_for_exit(self):
        clock = pygame.time.Clock()
        waiting = True
        
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
            
            clock.tick(30)
        
        pygame.quit()
        sys.exit(1)

class AssetManager:
    def __init__(self):
        self.textures = {}
        self.sounds = {}
        self.music = {}
        self.fonts = {}
        self.error_handler = None
        try:
            pygame.mixer.init()
        except Exception:
            pass
    
    def set_error_handler(self, error_handler):
        self.error_handler = error_handler
    
    def _validate_name(self, name):
        if name is not None and not isinstance(name, str):
            raise ValueError(f"Asset name must be a string, got {type(name).__name__}")
        if name == "":
            raise ValueError("Asset name cannot be empty")
    
    def load(self, asset_type, path, name=None, **kwargs):
        global _engine
        
        if not isinstance(asset_type, str):
            error_msg = f"Asset type must be a string, got {type(asset_type).__name__}"
            if self.error_handler:
                self.error_handler.show_fatal_error(_engine.screen if _engine else None, error_msg)
            raise TypeError(error_msg)
        
        if asset_type not in ["texture", "sound", "music", "font"]:
            error_msg = f"Unknown asset type: '{asset_type}'. Valid types: texture, sound, music, font"
            if self.error_handler:
                self.error_handler.show_fatal_error(_engine.screen if _engine else None, error_msg)
            raise ValueError(error_msg)
        
        if not isinstance(path, str) and path is not None:
            error_msg = f"Asset path must be a string, got {type(path).__name__}"
            if self.error_handler:
                self.error_handler.show_fatal_error(_engine.screen if _engine else None, error_msg)
            raise TypeError(error_msg)
        
        if name is None:
            if path is not None:
                name = os.path.basename(path).split('.')[0]
            else:
                name = "default"
        
        self._validate_name(name)
        
        if asset_type == "texture":
            if not os.path.exists(path):
                error_msg = f"Texture file not found: {path}"
                if self.error_handler:
                    self.error_handler.show_fatal_error(_engine.screen if _engine else None, error_msg)
                raise FileNotFoundError(error_msg)
            
            try:
                surface = pygame.image.load(path).convert_alpha()
                self.textures[name] = surface
                return surface
            except pygame.error as e:
                error_msg = f"Failed to load texture: {path}\n{str(e)}"
                if self.error_handler:
                    self.error_handler.show_fatal_error(_engine.screen if _engine else None, error_msg)
                raise
            except Exception as e:
                error_msg = f"Failed to load texture: {path}\n{str(e)}"
                if self.error_handler:
                    self.error_handler.show_fatal_error(_engine.screen if _engine else None, error_msg)
                raise
        
        elif asset_type == "sound":
            if not os.path.exists(path):
                error_msg = f"Sound file not found: {path}"
                if self.error_handler:
                    self.error_handler.show_fatal_error(_engine.screen if _engine else None, error_msg)
                raise FileNotFoundError(error_msg)
            
            try:
                sound = pygame.mixer.Sound(path)
                self.sounds[name] = sound
                return sound
            except pygame.error as e:
                error_msg = f"Failed to load sound: {path}\n{str(e)}"
                if self.error_handler:
                    self.error_handler.show_fatal_error(_engine.screen if _engine else None, error_msg)
                raise
            except Exception as e:
                error_msg = f"Failed to load sound: {path}\n{str(e)}"
                if self.error_handler:
                    self.error_handler.show_fatal_error(_engine.screen if _engine else None, error_msg)
                raise
        
        elif asset_type == "music":
            if not os.path.exists(path):
                error_msg = f"Music file not found: {path}"
                if self.error_handler:
                    self.error_handler.show_fatal_error(_engine.screen if _engine else None, error_msg)
                raise FileNotFoundError(error_msg)
            
            self.music[name] = path
            return path
        
        elif asset_type == "font":
            size = kwargs.get("size", 16)
            
            if not isinstance(size, (int, float)):
                error_msg = f"Font size must be a number, got {type(size).__name__}"
                if self.error_handler:
                    self.error_handler.show_fatal_error(_engine.screen if _engine else None, error_msg)
                raise TypeError(error_msg)
            
            if size <= 0:
                error_msg = f"Font size must be positive, got {size}"
                if self.error_handler:
                    self.error_handler.show_fatal_error(_engine.screen if _engine else None, error_msg)
                raise ValueError(error_msg)
            
            if not pygame.font.get_init():
                pygame.font.init()
            
            if path is None:
                font = pygame.font.Font(None, int(size))
                self.fonts[name] = font
                return font
            
            if not os.path.exists(path):
                font = pygame.font.Font(None, int(size))
                self.fonts[name] = font
                return font
            
            try:
                font = pygame.font.Font(path, int(size))
                self.fonts[name] = font
                return font
            except Exception:
                font = pygame.font.Font(None, int(size))
                self.fonts[name] = font
                return font
    
    def get_texture(self, name):
        global _engine
        
        if name not in self.textures:
            error_msg = f"Texture '{name}' not found"
            if self.error_handler:
                self.error_handler.show_fatal_error(_engine.screen if _engine else None, error_msg)
            raise KeyError(error_msg)
        return self.textures[name]
    
    def get_sound(self, name):
        global _engine
        
        if name not in self.sounds:
            error_msg = f"Sound '{name}' not found"
            if self.error_handler:
                self.error_handler.show_fatal_error(_engine.screen if _engine else None, error_msg)
            raise KeyError(error_msg)
        return self.sounds[name]
    
    def get_music(self, name):
        global _engine
        
        if name not in self.music:
            error_msg = f"Music '{name}' not found"
            if self.error_handler:
                self.error_handler.show_fatal_error(_engine.screen if _engine else None, error_msg)
            raise KeyError(error_msg)
        return self.music[name]
    
    def get_font(self, name):
        global _engine
        
        if name not in self.fonts:
            error_msg = f"Font '{name}' not found"
            if self.error_handler:
                self.error_handler.show_fatal_error(_engine.screen if _engine else None, error_msg)
            raise KeyError(error_msg)
        return self.fonts[name]

class Shape:
    __slots__ = ('id', 'shape_type', 'x', 'y', '_z_index', '_rotation', 
                 '_scale_x', '_scale_y', 'color', 'width', 'height', 'radius', 
                 'radius_x', 'radius_y', 'filled', 'visible', 'texture', '_original_texture')
    
    def __init__(self, shape_id, shape_type, x, y, **kwargs):
        global _engine
        
        self.id = shape_id
        
        valid_types = ["rectangle", "rect", "circle", "circ", "sphere", "oval", "pixel"]
        if shape_type not in valid_types:
            error_msg = f"Invalid shape type: '{shape_type}'"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise ValueError(error_msg)
        
        if shape_type in ["rectangle", "rect"]:
            self.shape_type = "rectangle"
        elif shape_type in ["circle", "circ", "sphere"]:
            self.shape_type = "circle"
        elif shape_type == "oval":
            self.shape_type = "oval"
        elif shape_type == "pixel":
            self.shape_type = "pixel"
        
        if not isinstance(x, (int, float)):
            error_msg = f"Shape x position must be a number"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise TypeError(error_msg)
        
        if not isinstance(y, (int, float)):
            error_msg = f"Shape y position must be a number"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise TypeError(error_msg)
        
        self.x = x
        self.y = y
        
        z_index = kwargs.get("z_index", 0)
        if not isinstance(z_index, (int, float)):
            error_msg = f"z_index must be a number"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise TypeError(error_msg)
        self._z_index = z_index
        
        rotation = kwargs.get("rotation", 0)
        if not isinstance(rotation, (int, float)):
            error_msg = f"rotation must be a number"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise TypeError(error_msg)
        self._rotation = rotation % 360
        
        scale_x = kwargs.get("scale_x", 1.0)
        scale_y = kwargs.get("scale_y", 1.0)
        
        if not isinstance(scale_x, (int, float)):
            error_msg = f"scale_x must be a number"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise TypeError(error_msg)
        
        if not isinstance(scale_y, (int, float)):
            error_msg = f"scale_y must be a number"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise TypeError(error_msg)
        
        if scale_x <= 0 or scale_y <= 0:
            error_msg = f"Scale values must be positive"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise ValueError(error_msg)
        
        self._scale_x = scale_x
        self._scale_y = scale_y
        
        color = kwargs.get("color", (255, 255, 255))
        if not isinstance(color, (tuple, list)) or len(color) != 3:
            error_msg = f"Color must be a tuple of 3 integers (R, G, B)"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise ValueError(error_msg)
        
        for c in color:
            if not isinstance(c, int) or c < 0 or c > 255:
                error_msg = f"Color values must be integers between 0 and 255"
                if _engine and _engine.error_handler:
                    _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
                raise ValueError(error_msg)
        
        self.color = tuple(color)
        
        visible = kwargs.get("visible", True)
        if not isinstance(visible, bool):
            error_msg = f"visible must be a boolean"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise TypeError(error_msg)
        self.visible = visible
        
        self.texture = None
        self._original_texture = None
        
        if self.shape_type == "rectangle":
            width = kwargs.get("width", 50)
            height = kwargs.get("height", 50)
            
            if not isinstance(width, (int, float)) or width <= 0:
                error_msg = f"Rectangle width must be a positive number"
                if _engine and _engine.error_handler:
                    _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
                raise ValueError(error_msg)
            
            if not isinstance(height, (int, float)) or height <= 0:
                error_msg = f"Rectangle height must be a positive number"
                if _engine and _engine.error_handler:
                    _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
                raise ValueError(error_msg)
            
            self.width = width
            self.height = height
            
            filled = kwargs.get("filled", True)
            if not isinstance(filled, bool):
                error_msg = f"filled must be a boolean"
                if _engine and _engine.error_handler:
                    _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
                raise TypeError(error_msg)
            self.filled = filled
            
            self.radius = 0
            self.radius_x = 0
            self.radius_y = 0
        
        elif self.shape_type == "circle":
            if "radius" in kwargs:
                radius = kwargs["radius"]
                if not isinstance(radius, (int, float)) or radius <= 0:
                    error_msg = f"Circle radius must be a positive number"
                    if _engine and _engine.error_handler:
                        _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
                    raise ValueError(error_msg)
                self.radius = radius
                self.radius_x = radius
                self.radius_y = radius
            else:
                width = kwargs.get("width")
                height = kwargs.get("height")
                radius_x = kwargs.get("radius_x")
                radius_y = kwargs.get("radius_y")
                
                if width is not None and height is not None:
                    if not isinstance(width, (int, float)) or width <= 0:
                        error_msg = f"Circle width must be a positive number"
                        if _engine and _engine.error_handler:
                            _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
                        raise ValueError(error_msg)
                    
                    if not isinstance(height, (int, float)) or height <= 0:
                        error_msg = f"Circle height must be a positive number"
                        if _engine and _engine.error_handler:
                            _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
                        raise ValueError(error_msg)
                    
                    if width != height:
                        error_msg = f"Circle cannot have different width and height. Use 'oval' instead."
                        if _engine and _engine.error_handler:
                            _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
                        raise ValueError(error_msg)
                    
                    self.radius = width / 2
                    self.radius_x = self.radius
                    self.radius_y = self.radius
                    
                elif radius_x is not None and radius_y is not None:
                    if not isinstance(radius_x, (int, float)) or radius_x <= 0:
                        error_msg = f"Circle radius_x must be a positive number"
                        if _engine and _engine.error_handler:
                            _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
                        raise ValueError(error_msg)
                    
                    if not isinstance(radius_y, (int, float)) or radius_y <= 0:
                        error_msg = f"Circle radius_y must be a positive number"
                        if _engine and _engine.error_handler:
                            _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
                        raise ValueError(error_msg)
                    
                    if radius_x != radius_y:
                        error_msg = f"Circle cannot have different radius_x and radius_y. Use 'oval' instead."
                        if _engine and _engine.error_handler:
                            _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
                        raise ValueError(error_msg)
                    
                    self.radius_x = radius_x
                    self.radius_y = radius_y
                    self.radius = (radius_x + radius_y) / 2
                else:
                    self.radius = 25
                    self.radius_x = 25
                    self.radius_y = 25
            
            filled = kwargs.get("filled", True)
            if not isinstance(filled, bool):
                error_msg = f"filled must be a boolean"
                if _engine and _engine.error_handler:
                    _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
                raise TypeError(error_msg)
            self.filled = filled
            
            self.width = self.radius_x * 2
            self.height = self.radius_y * 2
        
        elif self.shape_type == "oval":
            if "radius_x" in kwargs and "radius_y" in kwargs:
                radius_x = kwargs["radius_x"]
                radius_y = kwargs["radius_y"]
                
                if not isinstance(radius_x, (int, float)) or radius_x <= 0:
                    error_msg = f"Oval radius_x must be a positive number"
                    if _engine and _engine.error_handler:
                        _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
                    raise ValueError(error_msg)
                
                if not isinstance(radius_y, (int, float)) or radius_y <= 0:
                    error_msg = f"Oval radius_y must be a positive number"
                    if _engine and _engine.error_handler:
                        _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
                    raise ValueError(error_msg)
                
                self.radius_x = radius_x
                self.radius_y = radius_y
                
            elif "width" in kwargs and "height" in kwargs:
                width = kwargs["width"]
                height = kwargs["height"]
                
                if not isinstance(width, (int, float)) or width <= 0:
                    error_msg = f"Oval width must be a positive number"
                    if _engine and _engine.error_handler:
                        _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
                    raise ValueError(error_msg)
                
                if not isinstance(height, (int, float)) or height <= 0:
                    error_msg = f"Oval height must be a positive number"
                    if _engine and _engine.error_handler:
                        _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
                    raise ValueError(error_msg)
                
                self.radius_x = width / 2
                self.radius_y = height / 2
            else:
                self.radius_x = 30
                self.radius_y = 20
            
            self.radius = (self.radius_x + self.radius_y) / 2
            
            filled = kwargs.get("filled", True)
            if not isinstance(filled, bool):
                error_msg = f"filled must be a boolean"
                if _engine and _engine.error_handler:
                    _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
                raise TypeError(error_msg)
            self.filled = filled
            
            self.width = self.radius_x * 2
            self.height = self.radius_y * 2
        
        elif self.shape_type == "pixel":
            self.width = 1
            self.height = 1
            self.radius = 0
            self.radius_x = 0
            self.radius_y = 0
            self.filled = True
    
    @property
    def z_index(self):
        return self._z_index
    
    @z_index.setter
    def z_index(self, value):
        global _engine
        
        if not isinstance(value, (int, float)):
            error_msg = f"z_index must be a number"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise TypeError(error_msg)
        self._z_index = value
        if _engine:
            _engine.shapes[self.id] = self
    
    @property
    def rotation(self):
        return self._rotation
    
    @rotation.setter
    def rotation(self, value):
        global _engine
        
        if not isinstance(value, (int, float)):
            error_msg = f"rotation must be a number"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise TypeError(error_msg)
        self._rotation = value % 360
        self._update_transformed_texture()
    
    @property
    def scale_x(self):
        return self._scale_x
    
    @scale_x.setter
    def scale_x(self, value):
        global _engine
        
        if not isinstance(value, (int, float)):
            error_msg = f"scale_x must be a number"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise TypeError(error_msg)
        if value <= 0:
            error_msg = f"scale_x must be positive"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise ValueError(error_msg)
        self._scale_x = value
        self._update_transformed_texture()
    
    @property
    def scale_y(self):
        return self._scale_y
    
    @scale_y.setter
    def scale_y(self, value):
        global _engine
        
        if not isinstance(value, (int, float)):
            error_msg = f"scale_y must be a number"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise TypeError(error_msg)
        if value <= 0:
            error_msg = f"scale_y must be positive"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise ValueError(error_msg)
        self._scale_y = value
        self._update_transformed_texture()
    
    def apply_texture(self, texture_or_name):
        global _engine
        
        if isinstance(texture_or_name, str):
            if _engine and _engine.assets:
                try:
                    self._original_texture = _engine.assets.get_texture(texture_or_name)
                except KeyError as e:
                    error_msg = f"Failed to apply texture: {str(e)}"
                    if _engine and _engine.error_handler:
                        _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
                    raise
            else:
                error_msg = "Cannot apply texture: Engine not available"
                if _engine and _engine.error_handler:
                    _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
                raise RuntimeError(error_msg)
        else:
            if not isinstance(texture_or_name, pygame.Surface):
                error_msg = f"Texture must be a string name or pygame Surface"
                if _engine and _engine.error_handler:
                    _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
                raise TypeError(error_msg)
            self._original_texture = texture_or_name
        
        self._update_transformed_texture()
    
    def _update_transformed_texture(self):
        global _engine
        
        if not self._original_texture:
            return
        
        width = int(self.width * self._scale_x)
        height = int(self.height * self._scale_y)
        
        if width <= 0 or height <= 0:
            return
        
        try:
            scaled = pygame.transform.scale(self._original_texture, (width, height))
            
            if self._rotation != 0:
                self.texture = pygame.transform.rotate(scaled, self._rotation)
            else:
                self.texture = scaled
        except Exception as e:
            error_msg = f"Failed to transform texture: {str(e)}"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise
    
    def scale(self, sx, sy):
        global _engine
        
        if not isinstance(sx, (int, float)) or not isinstance(sy, (int, float)):
            error_msg = f"Scale values must be numbers"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise TypeError(error_msg)
        
        if sx <= 0 or sy <= 0:
            error_msg = f"Scale values must be positive"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise ValueError(error_msg)
        
        self._scale_x = sx
        self._scale_y = sy
        self._update_transformed_texture()
    
    def get_rect(self):
        if self.shape_type == "rectangle":
            return pygame.Rect(self.x, self.y, self.width * self._scale_x, self.height * self._scale_y)
        elif self.shape_type in ["circle", "oval"]:
            radius_x = (self.radius_x if hasattr(self, 'radius_x') else self.radius) * self._scale_x
            radius_y = (self.radius_y if hasattr(self, 'radius_y') else self.radius) * self._scale_y
            return pygame.Rect(self.x - radius_x, self.y - radius_y, radius_x * 2, radius_y * 2)
        else:
            return pygame.Rect(self.x, self.y, 1, 1)
    
    def get_aabb(self):
        return self.get_rect()

class CollisionInfo:
    def __init__(self):
        self.collided = False
        self.other = None
        self.direction = None
        self.overlap_x = 0
        self.overlap_y = 0
        self.penetration = 0
        self.normal_x = 0
        self.normal_y = 0

class CollisionSystem:
    def __init__(self):
        self.collision_callbacks = []
        self.collision_pairs = set()
    
    def on_collision(self, callback):
        self.collision_callbacks.append(callback)
    
    def rect_rect(self, a, b):
        if not (a.x < b.x + b.width * b.scale_x and
                a.x + a.width * a.scale_x > b.x and
                a.y < b.y + b.height * b.scale_y and
                a.y + a.height * a.scale_y > b.y):
            return None
        
        info = CollisionInfo()
        info.collided = True
        info.other = b
        
        overlap_left = (a.x + a.width * a.scale_x) - b.x
        overlap_right = (b.x + b.width * b.scale_x) - a.x
        overlap_top = (a.y + a.height * a.scale_y) - b.y
        overlap_bottom = (b.y + b.height * b.scale_y) - a.y
        
        info.overlap_x = min(overlap_left, overlap_right)
        info.overlap_y = min(overlap_top, overlap_bottom)
        info.penetration = min(info.overlap_x, info.overlap_y)
        
        if info.overlap_x < info.overlap_y:
            if overlap_left < overlap_right:
                info.direction = "left"
                info.normal_x = -1
            else:
                info.direction = "right"
                info.normal_x = 1
        else:
            if overlap_top < overlap_bottom:
                info.direction = "top"
                info.normal_y = -1
            else:
                info.direction = "bottom"
                info.normal_y = 1
        
        return info
    
    def rect_circle(self, rect, circle):
        radius_x = circle.radius_x if hasattr(circle, 'radius_x') else circle.radius
        radius_y = circle.radius_y if hasattr(circle, 'radius_y') else circle.radius
        radius_x *= circle.scale_x
        radius_y *= circle.scale_y
        
        closest_x = max(rect.x, min(circle.x, rect.x + rect.width * rect.scale_x))
        closest_y = max(rect.y, min(circle.y, rect.y + rect.height * rect.scale_y))
        dx = closest_x - circle.x
        dy = closest_y - circle.y
        
        if (dx * dx) / (radius_x * radius_x) + (dy * dy) / (radius_y * radius_y) > 1:
            return None
        
        info = CollisionInfo()
        info.collided = True
        info.other = rect if rect != circle else circle
        
        dist = math.sqrt(dx * dx + dy * dy)
        if dist > 0:
            info.normal_x = dx / dist
            info.normal_y = dy / dist
            ellipse_dist = math.sqrt((dx / radius_x) ** 2 + (dy / radius_y) ** 2)
            info.penetration = (1 - ellipse_dist) * max(radius_x, radius_y)
        else:
            info.normal_x = 1
            info.normal_y = 0
            info.penetration = max(radius_x, radius_y)
        
        if abs(info.normal_x) > abs(info.normal_y):
            info.direction = "left" if info.normal_x < 0 else "right"
        else:
            info.direction = "top" if info.normal_y < 0 else "bottom"
        
        info.overlap_x = abs(dx)
        info.overlap_y = abs(dy)
        
        return info
    
    def circle_circle(self, a, b):
        dx = a.x - b.x
        dy = a.y - b.y
        
        radius_x_a = a.radius_x if hasattr(a, 'radius_x') else a.radius
        radius_y_a = a.radius_y if hasattr(a, 'radius_y') else a.radius
        radius_x_b = b.radius_x if hasattr(b, 'radius_x') else b.radius
        radius_y_b = b.radius_y if hasattr(b, 'radius_y') else b.radius
        
        radius_x_a *= a.scale_x
        radius_y_a *= a.scale_y
        radius_x_b *= b.scale_x
        radius_y_b *= b.scale_y
        
        dist_sq = dx * dx + dy * dy
        sum_x = radius_x_a + radius_x_b
        sum_y = radius_y_a + radius_y_b
        
        if dist_sq > max(sum_x * sum_x, sum_y * sum_y):
            return None
        
        info = CollisionInfo()
        info.collided = True
        info.other = b
        
        dist = math.sqrt(dist_sq)
        if dist > 0:
            info.normal_x = dx / dist
            info.normal_y = dy / dist
            info.penetration = (radius_x_a + radius_x_b) - dist
        else:
            info.normal_x = 1
            info.normal_y = 0
            info.penetration = radius_x_a + radius_x_b
        
        if abs(info.normal_x) > abs(info.normal_y):
            info.direction = "left" if info.normal_x > 0 else "right"
        else:
            info.direction = "top" if info.normal_y > 0 else "bottom"
        
        info.overlap_x = abs(dx)
        info.overlap_y = abs(dy)
        
        return info
    
    def check(self, shape_a, shape_b):
        global _engine
        
        if not isinstance(shape_a, Shape) or not isinstance(shape_b, Shape):
            return False
        
        if not shape_a.visible or not shape_b.visible:
            return False
        
        if shape_a.shape_type == "rectangle" and shape_b.shape_type == "rectangle":
            return self.rect_rect(shape_a, shape_b) is not None
        elif shape_a.shape_type == "rectangle" and shape_b.shape_type in ["circle", "oval"]:
            return self.rect_circle(shape_a, shape_b) is not None
        elif shape_a.shape_type in ["circle", "oval"] and shape_b.shape_type == "rectangle":
            return self.rect_circle(shape_b, shape_a) is not None
        elif shape_a.shape_type in ["circle", "oval"] and shape_b.shape_type in ["circle", "oval"]:
            return self.circle_circle(shape_a, shape_b) is not None
        
        return False
    
    def get_collision_info(self, shape_a, shape_b):
        if not shape_a.visible or not shape_b.visible:
            return None
        
        if shape_a.shape_type == "rectangle" and shape_b.shape_type == "rectangle":
            return self.rect_rect(shape_a, shape_b)
        elif shape_a.shape_type == "rectangle" and shape_b.shape_type in ["circle", "oval"]:
            return self.rect_circle(shape_a, shape_b)
        elif shape_a.shape_type in ["circle", "oval"] and shape_b.shape_type == "rectangle":
            info = self.rect_circle(shape_b, shape_a)
            if info:
                info.normal_x = -info.normal_x
                info.normal_y = -info.normal_y
                if info.direction == "left":
                    info.direction = "right"
                elif info.direction == "right":
                    info.direction = "left"
                elif info.direction == "top":
                    info.direction = "bottom"
                elif info.direction == "bottom":
                    info.direction = "top"
            return info
        elif shape_a.shape_type in ["circle", "oval"] and shape_b.shape_type in ["circle", "oval"]:
            return self.circle_circle(shape_a, shape_b)
        
        return None
    
    def get_direction(self, shape_a, shape_b):
        info = self.get_collision_info(shape_a, shape_b)
        return info.direction if info else None
    
    def resolve(self, shape_a, shape_b, mass_a=1, mass_b=1):
        info = self.get_collision_info(shape_a, shape_b)
        if not info:
            return False
        
        total_mass = mass_a + mass_b
        if total_mass == 0:
            return False
        
        move_a = mass_b / total_mass
        move_b = mass_a / total_mass
        
        shape_a.x -= info.normal_x * info.penetration * move_a
        shape_a.y -= info.normal_y * info.penetration * move_a
        shape_b.x += info.normal_x * info.penetration * move_b
        shape_b.y += info.normal_y * info.penetration * move_b
        
        return True
    
    def sweep_test(self, shape, velocity_x, velocity_y, other_shapes):
        if not other_shapes:
            return None
        
        steps = max(1, int(math.sqrt(velocity_x * velocity_x + velocity_y * velocity_y) / 5))
        step_x = velocity_x / steps
        step_y = velocity_y / steps
        
        for step in range(steps):
            shape.x += step_x
            shape.y += step_y
            
            for other in other_shapes:
                if shape != other and shape.visible and other.visible:
                    info = self.get_collision_info(shape, other)
                    if info:
                        shape.x -= step_x
                        shape.y -= step_y
                        info.collided = True
                        info.other = other
                        return info
        
        return None
    
    def raycast(self, start_x, start_y, end_x, end_y, shapes, ignore_shape=None):
        dx = end_x - start_x
        dy = end_y - start_y
        dist = math.sqrt(dx * dx + dy * dy)
        
        if dist == 0:
            return None
        
        step_x = dx / dist
        step_y = dy / dist
        current_x = start_x
        current_y = start_y
        
        steps = int(dist)
        for _ in range(steps):
            current_x += step_x
            current_y += step_y
            
            test_point = type('Point', (), {'x': current_x, 'y': current_y})()
            
            for shape in shapes:
                if shape == ignore_shape or not shape.visible:
                    continue
                
                test_point.shape_type = "pixel"
                test_point.get_rect = lambda: pygame.Rect(current_x, current_y, 1, 1)
                test_point.visible = True
                
                if self.check(test_point, shape):
                    info = CollisionInfo()
                    info.collided = True
                    info.other = shape
                    info.normal_x = -step_x
                    info.normal_y = -step_y
                    info.penetration = dist - math.sqrt((current_x - start_x) ** 2 + (current_y - start_y) ** 2)
                    return info
        
        return None
    
    def check_all(self, shapes):
        collisions = []
        shape_list = list(shapes.values()) if isinstance(shapes, dict) else shapes
        
        for i, shape_a in enumerate(shape_list):
            for shape_b in shape_list[i + 1:]:
                info = self.get_collision_info(shape_a, shape_b)
                if info:
                    collisions.append((shape_a, shape_b, info))
                    
                    pair = (min(shape_a.id, shape_b.id), max(shape_a.id, shape_b.id))
                    if pair not in self.collision_pairs:
                        self.collision_pairs.add(pair)
                        for callback in self.collision_callbacks:
                            callback(shape_a, shape_b, info)
                    else:
                        for callback in self.collision_callbacks:
                            callback(shape_a, shape_b, info)
                else:
                    pair = (min(shape_a.id, shape_b.id), max(shape_a.id, shape_b.id))
                    if pair in self.collision_pairs:
                        self.collision_pairs.remove(pair)
        
        return collisions

class SpatialGrid:
    def __init__(self, cell_size=100):
        global _engine
        
        if not isinstance(cell_size, (int, float)) or cell_size <= 0:
            error_msg = f"cell_size must be a positive number"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise ValueError(error_msg)
        self.cell_size = cell_size
        self.grid = {}
    
    def _get_cell(self, x, y):
        return (int(x // self.cell_size), int(y // self.cell_size))
    
    def _get_cells_for_shape(self, shape):
        global _engine
        
        if not isinstance(shape, Shape):
            error_msg = f"SpatialGrid expects Shape objects"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise TypeError(error_msg)
        
        rect = shape.get_aabb()
        start_x = int(rect.left // self.cell_size)
        start_y = int(rect.top // self.cell_size)
        end_x = int(rect.right // self.cell_size)
        end_y = int(rect.bottom // self.cell_size)
        
        cells = []
        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                cells.append((x, y))
        return cells
    
    def add(self, shape):
        cells = self._get_cells_for_shape(shape)
        for cell in cells:
            if cell not in self.grid:
                self.grid[cell] = []
            if shape not in self.grid[cell]:
                self.grid[cell].append(shape)
    
    def remove(self, shape):
        cells = self._get_cells_for_shape(shape)
        for cell in cells:
            if cell in self.grid and shape in self.grid[cell]:
                self.grid[cell].remove(shape)
                if not self.grid[cell]:
                    del self.grid[cell]
    
    def update(self, shape):
        self.remove(shape)
        self.add(shape)
    
    def get_nearby(self, shape, radius=2):
        global _engine
        
        if not isinstance(shape, Shape):
            error_msg = f"SpatialGrid.get_nearby expects Shape object"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise TypeError(error_msg)
        
        if not isinstance(radius, int) or radius < 0:
            error_msg = f"radius must be a non-negative integer"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise ValueError(error_msg)
        
        nearby = set()
        center_cell = self._get_cell(shape.x, shape.y)
        
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                cell = (center_cell[0] + dx, center_cell[1] + dy)
                if cell in self.grid:
                    for s in self.grid[cell]:
                        if s != shape:
                            nearby.add(s)
        return nearby

class InputManager:
    def __init__(self):
        self.key_press_callbacks = {}
        self.key_release_callbacks = {}
        self.mouse_press_callbacks = {1: [], 2: [], 3: []}
        self.mouse_release_callbacks = {1: [], 2: [], 3: []}
        self.mouse_move_callbacks = []
        self.mouse_wheel_callbacks = []
    
    def on_key_press(self, key, callback):
        global _engine
        
        if not callable(callback):
            error_msg = f"Callback must be callable"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise TypeError(error_msg)
        
        if key not in self.key_press_callbacks:
            self.key_press_callbacks[key] = []
        self.key_press_callbacks[key].append(callback)
    
    def on_key_release(self, key, callback):
        global _engine
        
        if not callable(callback):
            error_msg = f"Callback must be callable"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise TypeError(error_msg)
        
        if key not in self.key_release_callbacks:
            self.key_release_callbacks[key] = []
        self.key_release_callbacks[key].append(callback)
    
    def on_mouse_press(self, button, callback):
        global _engine
        
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
    
    def on_mouse_release(self, button, callback):
        global _engine
        
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
    
    def on_mouse_move(self, callback):
        global _engine
        
        if not callable(callback):
            error_msg = f"Callback must be callable"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise TypeError(error_msg)
        
        self.mouse_move_callbacks.append(callback)
    
    def on_mouse_wheel(self, callback):
        global _engine
        
        if not callable(callback):
            error_msg = f"Callback must be callable"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise TypeError(error_msg)
        
        self.mouse_wheel_callbacks.append(callback)
    
    def is_key_down(self, key):
        return pygame.key.get_pressed()[key]
    
    def is_mouse_down(self, button):
        global _engine
        
        if button not in [1, 2, 3]:
            error_msg = f"Invalid mouse button: {button}. Use 1, 2, or 3"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise ValueError(error_msg)
        
        buttons = pygame.mouse.get_pressed()
        if button == 1:
            return buttons[0]
        elif button == 2:
            return buttons[1]
        elif button == 3:
            return buttons[2]
        return False
    
    def get_mouse_position(self):
        return pygame.mouse.get_pos()
    
    def handle_event(self, event):
        global _engine
        
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

class GraphicsEngine:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        try:
            pygame.mixer.init()
        except Exception:
            pass
        
        self.screen = None
        self.width = 0
        self.height = 0
        self.running = False
        self.clock = pygame.time.Clock()
        self.delta_time = 0
        self.fps = 60
        
        self.shapes = {}
        self.next_id = 1
        self.background_color = (0, 0, 0)
        
        self.error_handler = ErrorHandler()
        self.assets = AssetManager()
        self.assets.set_error_handler(self.error_handler)
        self.input = InputManager()
        self.collision = CollisionSystem()
        self.spatial_grid = SpatialGrid()
        
        self.camera_x = 0
        self.camera_y = 0
        
        self._default_fonts = {}
        self.draw_callback = None
    
    def _get_default_font(self, size=24):
        if size not in self._default_fonts:
            self._default_fonts[size] = pygame.font.Font(None, size)
        return self._default_fonts[size]
    
    def set_draw_callback(self, callback):
        if not callable(callback):
            error_msg = "Draw callback must be callable"
            self.error_handler.show_fatal_error(self.screen, error_msg)
            raise TypeError(error_msg)
        self.draw_callback = callback
    
    def create_window(self, title, width, height):
        if not isinstance(title, str):
            error_msg = f"Window title must be a string"
            self.error_handler.show_fatal_error(None, error_msg)
            raise TypeError(error_msg)
        
        if not isinstance(width, int) or width <= 0:
            error_msg = f"Window width must be a positive integer"
            self.error_handler.show_fatal_error(None, error_msg)
            raise ValueError(error_msg)
        
        if not isinstance(height, int) or height <= 0:
            error_msg = f"Window height must be a positive integer"
            self.error_handler.show_fatal_error(None, error_msg)
            raise ValueError(error_msg)
        
        try:
            self.width = width
            self.height = height
            self.screen = pygame.display.set_mode((width, height))
            pygame.display.set_caption(title)
            self.running = True
        except Exception as e:
            error_msg = f"Failed to create window: {str(e)}"
            self.error_handler.show_fatal_error(None, error_msg)
            raise
    
    def set_fps(self, fps):
        if not isinstance(fps, (int, float)) or fps <= 0:
            error_msg = f"FPS must be a positive number"
            self.error_handler.show_fatal_error(self.screen, error_msg)
            raise ValueError(error_msg)
        self.fps = fps
    
    def get_delta_time(self):
        return self.delta_time
    
    def create_shape(self, shape_type, x, y, **kwargs):
        shape_id = self.next_id
        self.next_id += 1
        
        try:
            shape = Shape(shape_id, shape_type, x, y, **kwargs)
            self.shapes[shape_id] = shape
            self.spatial_grid.add(shape)
            return shape
        except Exception as e:
            error_msg = f"Failed to create shape: {str(e)}"
            self.error_handler.show_fatal_error(self.screen, error_msg)
            raise
    
    def delete_shape(self, shape):
        if not isinstance(shape, Shape):
            error_msg = f"delete_shape expects Shape object"
            self.error_handler.show_fatal_error(self.screen, error_msg)
            raise TypeError(error_msg)
        
        if shape.id in self.shapes:
            self.spatial_grid.remove(shape)
            del self.shapes[shape.id]
    
    def get_shape(self, shape_id):
        if not isinstance(shape_id, int):
            error_msg = f"Shape ID must be an integer"
            self.error_handler.show_fatal_error(self.screen, error_msg)
            raise TypeError(error_msg)
        
        return self.shapes.get(shape_id)
    
    def set_camera(self, x, y):
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            error_msg = f"Camera position must be numbers"
            self.error_handler.show_fatal_error(self.screen, error_msg)
            raise TypeError(error_msg)
        
        self.camera_x = x
        self.camera_y = y
    
    def move_camera(self, dx, dy):
        if not isinstance(dx, (int, float)) or not isinstance(dy, (int, float)):
            error_msg = f"Camera movement must be numbers"
            self.error_handler.show_fatal_error(self.screen, error_msg)
            raise TypeError(error_msg)
        
        self.camera_x += dx
        self.camera_y += dy
    
    def fill_screen(self, r, g, b):
        for value, name in [(r, "r"), (g, "g"), (b, "b")]:
            if not isinstance(value, int) or value < 0 or value > 255:
                error_msg = f"Color value must be between 0 and 255"
                self.error_handler.show_fatal_error(self.screen, error_msg)
                raise ValueError(error_msg)
        
        self.background_color = (r, g, b)
    
    def draw_text(self, text, font_name, x, y, color=(255, 255, 255), size=24):
        if not isinstance(text, str):
            error_msg = f"Text must be a string"
            self.error_handler.show_fatal_error(self.screen, error_msg)
            raise TypeError(error_msg)
        
        if font_name is not None and not isinstance(font_name, str):
            error_msg = f"Font name must be a string or None"
            self.error_handler.show_fatal_error(self.screen, error_msg)
            raise TypeError(error_msg)
        
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            error_msg = f"Text position must be numbers"
            self.error_handler.show_fatal_error(self.screen, error_msg)
            raise TypeError(error_msg)
        
        if not isinstance(color, (tuple, list)) or len(color) != 3:
            error_msg = f"Color must be a tuple of 3 integers"
            self.error_handler.show_fatal_error(self.screen, error_msg)
            raise ValueError(error_msg)
        
        if not pygame.font.get_init():
            pygame.font.init()
        
        font = None
        
        if font_name is None:
            font = self._get_default_font(size)
        else:
            try:
                font = self.assets.get_font(font_name)
            except KeyError:
                font = self._get_default_font(size)
        
        if font is None:
            font = self._get_default_font(size)
        
        try:
            text_surface = font.render(text, True, color)
            self.screen.blit(text_surface, (x - self.camera_x, y - self.camera_y))
            return text_surface.get_width()
        except Exception as e:
            error_msg = f"Failed to draw text: {str(e)}"
            self.error_handler.show_fatal_error(self.screen, error_msg)
            raise
    
    def play_sound(self, name, loops=0, maxtime=0, fade_ms=0):
        try:
            sound = self.assets.get_sound(name)
            if sound:
                sound.play(loops, maxtime, fade_ms)
        except Exception as e:
            error_msg = f"Failed to play sound: {str(e)}"
            self.error_handler.show_fatal_error(self.screen, error_msg)
            raise
    
    def play_music(self, name, loops=-1, start=0, fade_ms=0):
        try:
            music_path = self.assets.get_music(name)
            if music_path:
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.play(loops, start, fade_ms)
        except Exception as e:
            error_msg = f"Failed to play music: {str(e)}"
            self.error_handler.show_fatal_error(self.screen, error_msg)
            raise
    
    def stop_music(self):
        pygame.mixer.music.stop()
    
    def get_nearby_shapes(self, shape, radius=2):
        return self.spatial_grid.get_nearby(shape, radius)
    
    def check_collision(self, shape_a, shape_b):
        return self.collision.check(shape_a, shape_b)
    
    def get_collision_direction(self, shape_a, shape_b):
        return self.collision.get_direction(shape_a, shape_b)
    
    def get_collision_info(self, shape_a, shape_b):
        return self.collision.get_collision_info(shape_a, shape_b)
    
    def resolve_collision(self, shape_a, shape_b, mass_a=1, mass_b=1):
        return self.collision.resolve(shape_a, shape_b, mass_a, mass_b)
    
    def sweep_test(self, shape, velocity_x, velocity_y, other_shapes):
        return self.collision.sweep_test(shape, velocity_x, velocity_y, other_shapes)
    
    def raycast(self, start_x, start_y, end_x, end_y, shapes, ignore_shape=None):
        return self.collision.raycast(start_x, start_y, end_x, end_y, shapes, ignore_shape)
    
    def check_all_collisions(self, shapes):
        return self.collision.check_all(shapes)
    
    def update(self):
        self.delta_time = self.clock.tick(self.fps) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            else:
                try:
                    self.input.handle_event(event)
                except Exception as e:
                    error_msg = f"Error handling event: {str(e)}"
                    self.error_handler.show_fatal_error(self.screen, error_msg)
                    raise
        
        if not self.running:
            pygame.quit()
            sys.exit()
        
        self.screen.fill(self.background_color)
        
        sorted_shapes = sorted(self.shapes.values(), key=lambda s: s.z_index)
        
        for shape in sorted_shapes:
            if not shape.visible:
                continue
            
            draw_x = shape.x - self.camera_x
            draw_y = shape.y - self.camera_y
            
            if shape.shape_type == "pixel":
                if 0 <= draw_x < self.width and 0 <= draw_y < self.height:
                    self.screen.set_at((int(draw_x), int(draw_y)), shape.color)
            
            elif shape.shape_type == "rectangle":
                width = shape.width * shape.scale_x
                height = shape.height * shape.scale_y
                rect = pygame.Rect(draw_x, draw_y, width, height)
                
                if shape.texture:
                    self.screen.blit(shape.texture, rect)
                elif shape.filled:
                    pygame.draw.rect(self.screen, shape.color, rect)
                else:
                    pygame.draw.rect(self.screen, shape.color, rect, 1)
            
            elif shape.shape_type in ["circle", "oval"]:
                radius_x = (shape.radius_x if hasattr(shape, 'radius_x') else shape.radius) * shape.scale_x
                radius_y = (shape.radius_y if hasattr(shape, 'radius_y') else shape.radius) * shape.scale_y
                
                if shape.texture and shape.filled:
                    temp_surface = pygame.Surface((int(radius_x * 2), int(radius_y * 2)), pygame.SRCALPHA)
                    pygame.draw.ellipse(temp_surface, (255, 255, 255, 255), 
                                       temp_surface.get_rect())
                    textured_surface = shape.texture.copy()
                    if textured_surface.get_size() != (int(radius_x * 2), int(radius_y * 2)):
                        textured_surface = pygame.transform.scale(textured_surface, (int(radius_x * 2), int(radius_y * 2)))
                    textured_surface.blit(temp_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                    self.screen.blit(textured_surface, (int(draw_x - radius_x), int(draw_y - radius_y)))
                elif shape.filled:
                    pygame.draw.ellipse(self.screen, shape.color, 
                                       pygame.Rect(draw_x - radius_x, draw_y - radius_y, radius_x * 2, radius_y * 2))
                else:
                    pygame.draw.ellipse(self.screen, shape.color, 
                                       pygame.Rect(draw_x - radius_x, draw_y - radius_y, radius_x * 2, radius_y * 2), 1)
        
        if self.draw_callback:
            self.draw_callback()
        
        pygame.display.flip()
    
    def wait(self, ms):
        pygame.time.wait(ms)
    
    def clear_all(self):
        for shape in list(self.shapes.values()):
            self.spatial_grid.remove(shape)
        self.shapes.clear()
        self.next_id = 1
    
    def quit(self):
        self.running = False
        pygame.quit()
        sys.exit()

def get_engine():
    global _engine
    if _engine is None:
        _engine = GraphicsEngine()
    return _engine

def create_window(title, width, height):
    get_engine().create_window(title, width, height)

def create_shape(shape_type, x, y, **kwargs):
    return get_engine().create_shape(shape_type, x, y, **kwargs)

def delete_shape(shape):
    get_engine().delete_shape(shape)

def update():
    get_engine().update()

def is_running():
    return get_engine().running

def fill_screen(r, g, b):
    get_engine().fill_screen(r, g, b)

def set_camera(x, y):
    get_engine().set_camera(x, y)

def move_camera(dx, dy):
    get_engine().move_camera(dx, dy)

def draw_text(text, font_name, x, y, color=(255, 255, 255)):
    return get_engine().draw_text(text, font_name, x, y, color)

def load(asset_type, path, name=None, **kwargs):
    return get_engine().assets.load(asset_type, path, name, **kwargs)

def get_texture(name):
    return get_engine().assets.get_texture(name)

def get_sound(name):
    return get_engine().assets.get_sound(name)

def get_font(name):
    return get_engine().assets.get_font(name)

def play_sound(name, loops=0, maxtime=0, fade_ms=0):
    get_engine().play_sound(name, loops, maxtime, fade_ms)

def play_music(name, loops=-1, start=0, fade_ms=0):
    get_engine().play_music(name, loops, start, fade_ms)

def stop_music():
    get_engine().stop_music()

def on_key_press(key, callback):
    get_engine().input.on_key_press(key, callback)

def on_key_release(key, callback):
    get_engine().input.on_key_release(key, callback)

def on_mouse_press(button, callback):
    get_engine().input.on_mouse_press(button, callback)

def on_mouse_release(button, callback):
    get_engine().input.on_mouse_release(button, callback)

def on_mouse_move(callback):
    get_engine().input.on_mouse_move(callback)

def on_mouse_wheel(callback):
    get_engine().input.on_mouse_wheel(callback)

def is_key_down(key):
    return get_engine().input.is_key_down(key)

def is_mouse_down(button):
    return get_engine().input.is_mouse_down(button)

def get_mouse_position():
    return get_engine().input.get_mouse_position()

def check_collision(shape_a, shape_b):
    return get_engine().check_collision(shape_a, shape_b)

def get_collision_direction(shape_a, shape_b):
    return get_engine().get_collision_direction(shape_a, shape_b)

def get_collision_info(shape_a, shape_b):
    return get_engine().get_collision_info(shape_a, shape_b)

def resolve_collision(shape_a, shape_b, mass_a=1, mass_b=1):
    return get_engine().resolve_collision(shape_a, shape_b, mass_a, mass_b)

def sweep_test(shape, velocity_x, velocity_y, other_shapes):
    return get_engine().sweep_test(shape, velocity_x, velocity_y, other_shapes)

def raycast(start_x, start_y, end_x, end_y, shapes, ignore_shape=None):
    return get_engine().raycast(start_x, start_y, end_x, end_y, shapes, ignore_shape)

def check_all_collisions(shapes):
    return get_engine().check_all_collisions(shapes)

def update_spatial_grid(shape):
    get_engine().spatial_grid.update(shape)

def get_nearby_shapes(shape, radius=2):
    return get_engine().get_nearby_shapes(shape, radius)

def wait(ms):
    get_engine().wait(ms)

def clear_all():
    get_engine().clear_all()

def quit():
    get_engine().quit()

def get_delta_time():
    return get_engine().get_delta_time()

def set_fps(fps):
    get_engine().set_fps(fps)


def set_draw_callback(callback):
    get_engine().set_draw_callback(callback)

def draw_text(text, font_name, x, y, color=(255, 255, 255), size=24):
    return get_engine().draw_text(text, font_name, x, y, color, size)
