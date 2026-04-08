import pygame
import math
from typing import Optional, Union, Tuple
from ..globals import get_engine

class Shape:
    __slots__ = ('id', 'shape_type', 'x', 'y', '_z_index', '_rotation', 
                 '_scale_x', '_scale_y', 'color', 'width', 'height', 'radius', 
                 'radius_x', 'radius_y', 'filled', 'visible', 'texture', 
                 '_original_texture', '_needs_update', '_rotated_width', '_rotated_height')
    
    def __init__(self, shape_id: int, shape_type: str, x: float, y: float, **kwargs):
        global _engine
        _engine = get_engine()
        
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
        else:
            self.shape_type = "pixel"
        
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            error_msg = f"Shape position must be numbers"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise TypeError(error_msg)
        
        self.x = float(x)
        self.y = float(y)
        
        z_index = kwargs.get("z_index", 0)
        if not isinstance(z_index, (int, float)):
            error_msg = f"z_index must be a number"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise TypeError(error_msg)
        self._z_index = float(z_index)
        
        rotation = kwargs.get("rotation", 0)
        if not isinstance(rotation, (int, float)):
            error_msg = f"rotation must be a number"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise TypeError(error_msg)
        
        if self.shape_type in ["circle", "pixel"]:
            self._rotation = 0.0
        else:
            self._rotation = float(rotation) % 360
        
        scale_x = kwargs.get("scale_x", 1.0)
        scale_y = kwargs.get("scale_y", 1.0)
        
        if not isinstance(scale_x, (int, float)) or not isinstance(scale_y, (int, float)):
            error_msg = f"scale values must be numbers"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise TypeError(error_msg)
        
        if scale_x <= 0 or scale_y <= 0:
            error_msg = f"Scale values must be positive"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise ValueError(error_msg)
        
        self._scale_x = float(scale_x)
        self._scale_y = float(scale_y)
        
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
        self._needs_update = False
        self._rotated_width = 0
        self._rotated_height = 0
        
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
            
            self.width = float(width)
            self.height = float(height)
            
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
                self.radius = float(radius)
                self.radius_x = float(radius)
                self.radius_y = float(radius)
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
                    
                    self.radius_x = float(radius_x)
                    self.radius_y = float(radius_y)
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
                
                self.radius_x = float(radius_x)
                self.radius_y = float(radius_y)
                
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
        
        else:
            self.width = 1
            self.height = 1
            self.radius = 0
            self.radius_x = 0
            self.radius_y = 0
            self.filled = True
    
    @property
    def z_index(self) -> float:
        return self._z_index
    
    @z_index.setter
    def z_index(self, value: float) -> None:
        global _engine
        _engine = get_engine()
        
        if not isinstance(value, (int, float)):
            error_msg = f"z_index must be a number"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise TypeError(error_msg)
        self._z_index = float(value)
        if _engine:
            _engine.shapes[self.id] = self
    
    @property
    def rotation(self) -> float:
        return self._rotation
    
    @rotation.setter
    def rotation(self, value: float) -> None:
        global _engine
        _engine = get_engine()
        
        if not isinstance(value, (int, float)):
            error_msg = f"rotation must be a number"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise TypeError(error_msg)
        
        if self.shape_type in ["pixel"]:
            return
        
        self._rotation = float(value) % 360
        self._needs_update = True
    
    @property
    def scale_x(self) -> float:
        return self._scale_x
    
    @scale_x.setter
    def scale_x(self, value: float) -> None:
        global _engine
        _engine = get_engine()
        
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
        self._scale_x = float(value)
        self._needs_update = True
    
    @property
    def scale_y(self) -> float:
        return self._scale_y
    
    @scale_y.setter
    def scale_y(self, value: float) -> None:
        global _engine
        _engine = get_engine()
        
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
        self._scale_y = float(value)
        self._needs_update = True
    
    def apply_texture(self, texture_or_name: Union[str, pygame.Surface]) -> None:
        global _engine
        _engine = get_engine()
        
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
        
        self._needs_update = True
        self._update_transformed_texture()
    
    def _update_transformed_texture(self) -> None:
        if not self._original_texture:
            return
        
        if not self._needs_update:
            return
        
        width = int(self.width * self._scale_x)
        height = int(self.height * self._scale_y)
        
        if width <= 0 or height <= 0:
            return
        
        try:
            scaled = pygame.transform.scale(self._original_texture, (width, height))
            
            if self._rotation != 0:
                self.texture = pygame.transform.rotate(scaled, self._rotation)
                self._rotated_width, self._rotated_height = self.texture.get_size()
            else:
                self.texture = scaled
                self._rotated_width = width
                self._rotated_height = height
            
            self._needs_update = False
        except Exception as e:
            error_msg = f"Failed to transform texture: {str(e)}"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise
    
    def scale(self, sx: float, sy: float) -> None:
        global _engine
        _engine = get_engine()
        
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
        
        self._scale_x = float(sx)
        self._scale_y = float(sy)
        self._needs_update = True
        self._update_transformed_texture()
    
    def get_rect(self) -> pygame.Rect:
        if self.shape_type == "rectangle":
            return pygame.Rect(self.x, self.y, self.width * self._scale_x, self.height * self._scale_y)
        elif self.shape_type in ["circle", "oval"]:
            radius_x = (self.radius_x if hasattr(self, 'radius_x') else self.radius) * self._scale_x
            radius_y = (self.radius_y if hasattr(self, 'radius_y') else self.radius) * self._scale_y
            return pygame.Rect(self.x - radius_x, self.y - radius_y, radius_x * 2, radius_y * 2)
        else:
            return pygame.Rect(self.x, self.y, 1, 1)
    
    def get_aabb(self) -> pygame.Rect:
        return self.get_rect()
    
    def get_draw_offset(self) -> Tuple[float, float]:
        if not self.texture or not self._original_texture:
            return (self.x, self.y)
        
        offset_x = self.x - (self._rotated_width / 2)
        offset_y = self.y - (self._rotated_height / 2)
        
        return (offset_x, offset_y)