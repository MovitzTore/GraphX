import pygame
import sys
from typing import Optional, Dict, List, Tuple, Callable, Union
from .globals import get_engine, set_engine
from .errors import ErrorHandler
from .input_manager import InputManager, KeyCode, MouseButton
from .spatial import SpatialGrid
from .shapes.shape import Shape
from .shapes.collision import CollisionSystem, CollisionInfo
from .utils.helpers import AssetManager

class Group:
    """A group of shapes that can be controlled together."""
    
    def __init__(self, name: str):
        self.name = name
        self._shapes: List[Shape] = []
    
    def add(self, shape: Shape) -> None:
        """Add a shape to the group."""
        if shape not in self._shapes:
            self._shapes.append(shape)
    
    def remove(self, shape: Shape) -> None:
        """Remove a shape from the group."""
        if shape in self._shapes:
            self._shapes.remove(shape)
    
    def clear(self) -> None:
        """Remove all shapes from the group."""
        self._shapes.clear()
    
    @property
    def shapes(self) -> List[Shape]:
        """Get all shapes in the group."""
        return self._shapes.copy()
    
    @property
    def visible(self) -> bool:
        """Get visibility of first shape (assumes all same)."""
        if self._shapes:
            return self._shapes[0].visible
        return False
    
    @visible.setter
    def visible(self, value: bool) -> None:
        """Show or hide all shapes in the group."""
        for shape in self._shapes:
            shape.visible = value
    
    @property
    def x(self) -> float:
        """Get x of first shape."""
        if self._shapes:
            return self._shapes[0].x
        return 0
    
    @x.setter
    def x(self, value: float) -> None:
        """Move all shapes horizontally."""
        dx = value - self.x if self._shapes else 0
        for shape in self._shapes:
            shape.x += dx
    
    @property
    def y(self) -> float:
        """Get y of first shape."""
        if self._shapes:
            return self._shapes[0].y
        return 0
    
    @y.setter
    def y(self, value: float) -> None:
        """Move all shapes vertically."""
        dy = value - self.y if self._shapes else 0
        for shape in self._shapes:
            shape.y += dy
    
    def move(self, dx: float, dy: float) -> None:
        """Move all shapes by dx, dy."""
        for shape in self._shapes:
            shape.x += dx
            shape.y += dy
    
    def set_color(self, color: Tuple[int, int, int]) -> None:
        """Set color for all shapes in the group."""
        for shape in self._shapes:
            shape.color = color
    
    def delete(self) -> None:
        """Delete all shapes in the group."""
        for shape in self._shapes[:]:
            delete_shape(shape)
        self._shapes.clear()
    
    def is_touching(self, other) -> bool:
        """Check if any shape in group touches another shape or borders."""
        for shape in self._shapes:
            if shape.is_touching(other):
                return True
        return False
    
    def is_touching_group(self, other_group: 'Group') -> bool:
        """Check if any shape in this group touches any shape in another group."""
        for shape in self._shapes:
            for other_shape in other_group._shapes:
                if shape.is_touching(other_shape):
                    return True
        return False
    
    def get_touching(self, other):
        """Return first shape that touches another shape or borders."""
        for shape in self._shapes:
            if shape.is_touching(other):
                return shape
        return None
    
    @property
    def count(self) -> int:
        """Number of shapes in the group."""
        return len(self._shapes)

class Mouse:
    @property
    def x(self) -> int:
        return pygame.mouse.get_pos()[0]
    
    @property
    def y(self) -> int:
        return pygame.mouse.get_pos()[1]
    
    @property
    def pos(self) -> Tuple[int, int]:
        return pygame.mouse.get_pos()
    
    def is_down(self, button: int = 1) -> bool:
        buttons = pygame.mouse.get_pressed()
        return buttons[button - 1]

mouse = Mouse()

class GraphicsEngine:
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        try:
            pygame.mixer.init()
        except Exception:
            pass
        
        self.screen: Optional[pygame.Surface] = None
        self.width: int = 0
        self.height: int = 0
        self.running: bool = False
        self.clock = pygame.time.Clock()
        self.delta_time: float = 0
        self.fps: int = 60
        
        self.shapes: Dict[int, Shape] = {}
        self.next_id: int = 1
        self.background_color: Tuple[int, int, int] = (0, 0, 0)
        
        self.error_handler = ErrorHandler()
        self.assets = AssetManager()
        self.assets.set_error_handler(self.error_handler)
        self.input = InputManager()
        self.collision = CollisionSystem()
        self.spatial_grid = SpatialGrid()
        
        self.camera_x: float = 0
        self.camera_y: float = 0
        
        self._default_fonts: Dict[int, pygame.font.Font] = {}
        self.draw_callback: Optional[Callable] = None
        
        self._sorted_shapes_cache: List[Shape] = []
        self._shapes_dirty: bool = True
        
        self.groups: Dict[str, Group] = {}
        
        set_engine(self)
    
    def _get_default_font(self, size: int = 24) -> pygame.font.Font:
        if size not in self._default_fonts:
            self._default_fonts[size] = pygame.font.Font(None, size)
        return self._default_fonts[size]
    
    def set_draw_callback(self, callback: Callable) -> None:
        if not callable(callback):
            error_msg = "Draw callback must be callable"
            self.error_handler.show_fatal_error(self.screen, error_msg)
            raise TypeError(error_msg)
        self.draw_callback = callback
    
    def create_window(self, title: str, width: int, height: int) -> None:
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
    
    def set_fps(self, fps: float) -> None:
        if not isinstance(fps, (int, float)) or fps <= 0:
            error_msg = f"FPS must be a positive number"
            self.error_handler.show_fatal_error(self.screen, error_msg)
            raise ValueError(error_msg)
        self.fps = int(fps)
    
    def get_delta_time(self) -> float:
        return self.delta_time
    
    def create_shape(self, shape_type: str, x: float, y: float, **kwargs) -> Shape:
        shape_id = self.next_id
        self.next_id += 1
        
        try:
            shape = Shape(shape_id, shape_type, x, y, **kwargs)
            self.shapes[shape_id] = shape
            self.spatial_grid.add(shape)
            self._shapes_dirty = True
            return shape
        except Exception as e:
            error_msg = f"Failed to create shape: {str(e)}"
            self.error_handler.show_fatal_error(self.screen, error_msg)
            raise
    
    def delete_shape(self, shape: Shape) -> None:
        if not isinstance(shape, Shape):
            error_msg = f"delete_shape expects Shape object"
            self.error_handler.show_fatal_error(self.screen, error_msg)
            raise TypeError(error_msg)
        
        if shape.id in self.shapes:
            for group in self.groups.values():
                if shape in group._shapes:
                    group._shapes.remove(shape)
            self.spatial_grid.remove(shape)
            del self.shapes[shape.id]
            self._shapes_dirty = True
    
    def get_shape(self, shape_id: int) -> Optional[Shape]:
        if not isinstance(shape_id, int):
            error_msg = f"Shape ID must be an integer"
            self.error_handler.show_fatal_error(self.screen, error_msg)
            raise TypeError(error_msg)
        
        return self.shapes.get(shape_id)
    
    def set_camera(self, x: float, y: float) -> None:
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            error_msg = f"Camera position must be numbers"
            self.error_handler.show_fatal_error(self.screen, error_msg)
            raise TypeError(error_msg)
        
        self.camera_x = float(x)
        self.camera_y = float(y)
    
    def get_all_shapes(self) -> List[Shape]:
        return list(self.shapes.values())
    
    def get_shape_position(self, shape: Shape) -> Tuple[float, float]:
        if not isinstance(shape, Shape):
            error_msg = f"get_shape_position expects Shape object, got {type(shape).__name__}"
            self.error_handler.show_fatal_error(self.screen, error_msg)
            raise TypeError(error_msg)
        return (shape.x, shape.y)
    
    def move_camera(self, dx: float, dy: float) -> None:
        if not isinstance(dx, (int, float)) or not isinstance(dy, (int, float)):
            error_msg = f"Camera movement must be numbers"
            self.error_handler.show_fatal_error(self.screen, error_msg)
            raise TypeError(error_msg)
        
        self.camera_x += dx
        self.camera_y += dy
    
    def fill_screen(self, r: int, g: int, b: int) -> None:
        for value in [r, g, b]:
            if not isinstance(value, int) or value < 0 or value > 255:
                error_msg = f"Color value must be between 0 and 255"
                self.error_handler.show_fatal_error(self.screen, error_msg)
                raise ValueError(error_msg)
        
        self.background_color = (r, g, b)
    
    def draw_text(self, text: str, font_name: Optional[str], x: float, y: float, 
                  color: Tuple[int, int, int] = (255, 255, 255), size: int = 24) -> int:
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
    
    def play_sound(self, name: str, loops: int = 0, maxtime: int = 0, fade_ms: int = 0) -> None:
        try:
            sound = self.assets.get_sound(name)
            if sound:
                sound.play(loops, maxtime, fade_ms)
        except Exception as e:
            error_msg = f"Failed to play sound: {str(e)}"
            self.error_handler.show_fatal_error(self.screen, error_msg)
            raise
    
    def play_music(self, name: str, loops: int = -1, start: float = 0, fade_ms: int = 0) -> None:
        try:
            music_path = self.assets.get_music(name)
            if music_path:
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.play(loops, start, fade_ms)
        except Exception as e:
            error_msg = f"Failed to play music: {str(e)}"
            self.error_handler.show_fatal_error(self.screen, error_msg)
            raise
    
    def stop_music(self) -> None:
        pygame.mixer.music.stop()
    
    def get_nearby_shapes(self, shape: Shape, radius: int = 2) -> List[Shape]:
        return self.spatial_grid.get_nearby(shape, radius)
    
    def check_collision(self, shape_a: Shape, shape_b: Shape) -> bool:
        return self.collision.check(shape_a, shape_b)
    
    def get_collision_direction(self, shape_a: Shape, shape_b: Shape) -> Optional[str]:
        return self.collision.get_direction(shape_a, shape_b)
    
    def get_collision_info(self, shape_a: Shape, shape_b: Shape) -> Optional[CollisionInfo]:
        return self.collision.get_collision_info(shape_a, shape_b)
    
    def resolve_collision(self, shape_a: Shape, shape_b: Shape, mass_a: float = 1, mass_b: float = 1) -> bool:
        return self.collision.resolve(shape_a, shape_b, mass_a, mass_b)
    
    def sweep_test(self, shape: Shape, velocity_x: float, velocity_y: float, 
                   other_shapes: List[Shape]) -> Optional[CollisionInfo]:
        return self.collision.sweep_test(shape, velocity_x, velocity_y, other_shapes)
    
    def raycast(self, start_x: float, start_y: float, end_x: float, end_y: float, 
                shapes: List[Shape], ignore_shape: Optional[Shape] = None) -> Optional[CollisionInfo]:
        return self.collision.raycast(start_x, start_y, end_x, end_y, shapes, ignore_shape)
    
    def check_all_collisions(self, shapes: Dict[int, Shape]) -> List[Tuple[Shape, Shape, CollisionInfo]]:
        return self.collision.check_all(shapes)
    
    def create_group(self, name: str) -> Group:
        if name in self.groups:
            error_msg = f"Group '{name}' already exists"
            self.error_handler.show_fatal_error(self.screen, error_msg)
            raise ValueError(error_msg)
        
        group = Group(name)
        self.groups[name] = group
        return group
    
    def get_group(self, name: str) -> Optional[Group]:
        return self.groups.get(name)
    
    def delete_group(self, name: str) -> None:
        if name in self.groups:
            self.groups[name].delete()
            del self.groups[name]
    
    def update(self) -> None:
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
        
        if self.screen is None:
            return
        
        self.screen.fill(self.background_color)
        
        if self._shapes_dirty:
            self._sorted_shapes_cache = sorted(self.shapes.values(), key=lambda s: s.z_index)
            self._shapes_dirty = False
        
        for shape in self._sorted_shapes_cache:
            if not shape.visible:
                continue
            
            if shape._needs_update and shape._original_texture:
                shape._update_transformed_texture()
            
            if shape.shape_type == "pixel":
                draw_x = shape.x - self.camera_x
                draw_y = shape.y - self.camera_y
                if 0 <= draw_x < self.width and 0 <= draw_y < self.height:
                    self.screen.set_at((int(draw_x), int(draw_y)), shape.color)
            
            elif shape.shape_type == "rectangle":
                width = shape.width * shape.scale_x
                height = shape.height * shape.scale_y
                
                if shape.texture:
                    offset_x, offset_y = shape.get_draw_offset()
                    draw_x = offset_x - self.camera_x
                    draw_y = offset_y - self.camera_y
                    self.screen.blit(shape.texture, (draw_x, draw_y))
                elif shape.filled:
                    draw_x = shape.x - self.camera_x
                    draw_y = shape.y - self.camera_y
                    rect = pygame.Rect(draw_x, draw_y, width, height)
                    pygame.draw.rect(self.screen, shape.color, rect)
                else:
                    draw_x = shape.x - self.camera_x
                    draw_y = shape.y - self.camera_y
                    rect = pygame.Rect(draw_x, draw_y, width, height)
                    pygame.draw.rect(self.screen, shape.color, rect, 1)
            
            elif shape.shape_type in ["circle", "oval"]:
                radius_x = (shape.radius_x if hasattr(shape, 'radius_x') else shape.radius) * shape.scale_x
                radius_y = (shape.radius_y if hasattr(shape, 'radius_y') else shape.radius) * shape.scale_y
                
                if shape.texture and shape.filled:
                    offset_x, offset_y = shape.get_draw_offset()
                    draw_x = offset_x - self.camera_x
                    draw_y = offset_y - self.camera_y
                    self.screen.blit(shape.texture, (draw_x, draw_y))
                elif shape.filled:
                    draw_x = shape.x - self.camera_x
                    draw_y = shape.y - self.camera_y
                    pygame.draw.ellipse(self.screen, shape.color, 
                                       pygame.Rect(draw_x - radius_x, draw_y - radius_y, radius_x * 2, radius_y * 2))
                else:
                    draw_x = shape.x - self.camera_x
                    draw_y = shape.y - self.camera_y
                    pygame.draw.ellipse(self.screen, shape.color, 
                                       pygame.Rect(draw_x - radius_x, draw_y - radius_y, radius_x * 2, radius_y * 2), 1)
        
        if self.draw_callback:
            self.draw_callback()
        
        pygame.display.flip()
    
    def wait(self, ms: int) -> None:
        pygame.time.wait(ms)
    
    def clear_all(self) -> None:
        for shape in list(self.shapes.values()):
            self.spatial_grid.remove(shape)
        self.shapes.clear()
        self.groups.clear()
        self.next_id = 1
        self._shapes_dirty = True
    
    def quit(self) -> None:
        self.running = False
        pygame.quit()
        sys.exit()

_engine = None

def get_engine() -> GraphicsEngine:
    global _engine
    if _engine is None:
        _engine = GraphicsEngine()
    return _engine

def create_window(title: str, width: int, height: int) -> None:
    get_engine().create_window(title, width, height)

def create_shape(shape_type: str, x: float, y: float, **kwargs) -> Shape:
    return get_engine().create_shape(shape_type, x, y, **kwargs)

def delete_shape(shape: Shape) -> None:
    get_engine().delete_shape(shape)

def update() -> None:
    get_engine().update()

def is_running() -> bool:
    return get_engine().running

def fill_screen(r: int, g: int, b: int) -> None:
    get_engine().fill_screen(r, g, b)

def get_all_shapes() -> List[Shape]:
    return get_engine().get_all_shapes()

def set_camera(x: float, y: float) -> None:
    get_engine().set_camera(x, y)

def move_camera(dx: float, dy: float) -> None:
    get_engine().move_camera(dx, dy)

def draw_text(text: str, font_name: Optional[str], x: float, y: float, 
              color: Tuple[int, int, int] = (255, 255, 255), size: int = 24) -> int:
    return get_engine().draw_text(text, font_name, x, y, color, size)

def load(asset_type: str, path: Optional[str], name: Optional[str] = None, **kwargs) -> Union[pygame.Surface, pygame.mixer.Sound, str, pygame.font.Font]:
    return get_engine().assets.load(asset_type, path, name, **kwargs)

def get_texture(name: str) -> pygame.Surface:
    return get_engine().assets.get_texture(name)

def get_sound(name: str) -> pygame.mixer.Sound:
    return get_engine().assets.get_sound(name)

def get_font(name: str) -> pygame.font.Font:
    return get_engine().assets.get_font(name)

def play_sound(name: str, loops: int = 0, maxtime: int = 0, fade_ms: int = 0) -> None:
    get_engine().play_sound(name, loops, maxtime, fade_ms)

def play_music(name: str, loops: int = -1, start: float = 0, fade_ms: int = 0) -> None:
    get_engine().play_music(name, loops, start, fade_ms)

def stop_music() -> None:
    get_engine().stop_music()

def on_key_press(key: int, callback: Callable) -> None:
    get_engine().input.on_key_press(key, callback)

def on_key_release(key: int, callback: Callable) -> None:
    get_engine().input.on_key_release(key, callback)

def on_mouse_press(button: int, callback: Callable) -> None:
    get_engine().input.on_mouse_press(button, callback)

def on_mouse_release(button: int, callback: Callable) -> None:
    get_engine().input.on_mouse_release(button, callback)

def on_mouse_move(callback: Callable) -> None:
    get_engine().input.on_mouse_move(callback)

def on_mouse_wheel(callback: Callable) -> None:
    get_engine().input.on_mouse_wheel(callback)

def is_key_down(key: int) -> bool:
    return get_engine().input.is_key_down(key)

def is_mouse_down(button: int) -> bool:
    return get_engine().input.is_mouse_down(button)

def get_mouse_position() -> Tuple[int, int]:
    return get_engine().input.get_mouse_position()

def check_collision(shape_a: Shape, shape_b: Shape) -> bool:
    return get_engine().check_collision(shape_a, shape_b)

def get_collision_direction(shape_a: Shape, shape_b: Shape) -> Optional[str]:
    return get_engine().get_collision_direction(shape_a, shape_b)

def get_collision_info(shape_a: Shape, shape_b: Shape) -> Optional[CollisionInfo]:
    return get_engine().get_collision_info(shape_a, shape_b)

def resolve_collision(shape_a: Shape, shape_b: Shape, mass_a: float = 1, mass_b: float = 1) -> bool:
    return get_engine().resolve_collision(shape_a, shape_b, mass_a, mass_b)

def sweep_test(shape: Shape, velocity_x: float, velocity_y: float, other_shapes: List[Shape]) -> Optional[CollisionInfo]:
    return get_engine().sweep_test(shape, velocity_x, velocity_y, other_shapes)

def raycast(start_x: float, start_y: float, end_x: float, end_y: float, 
            shapes: List[Shape], ignore_shape: Optional[Shape] = None) -> Optional[CollisionInfo]:
    return get_engine().raycast(start_x, start_y, end_x, end_y, shapes, ignore_shape)

def check_all_collisions(shapes: Dict[int, Shape]) -> List[Tuple[Shape, Shape, CollisionInfo]]:
    return get_engine().check_all_collisions(shapes)

def update_spatial_grid(shape: Shape) -> None:
    get_engine().spatial_grid.update(shape)

def get_nearby_shapes(shape: Shape, radius: int = 2) -> List[Shape]:
    return get_engine().get_nearby_shapes(shape, radius)

def wait(ms: int) -> None:
    get_engine().wait(ms)

def clear_all() -> None:
    get_engine().clear_all()

def quit() -> None:
    get_engine().quit()

def get_delta_time() -> float:
    return get_engine().get_delta_time()

def set_fps(fps: float) -> None:
    get_engine().set_fps(fps)

def set_draw_callback(callback: Callable) -> None:
    get_engine().set_draw_callback(callback)

def get_shape_position(shape: Shape) -> Tuple[float, float]:
    return get_engine().get_shape_position(shape)

def is_touching(shape: Shape, other) -> bool:
    return shape.is_touching(other)

def touching_borders(shape: Shape) -> bool:
    return shape.touching_borders()

def touching_any(shape: Shape, shapes: List[Shape]) -> Optional[Shape]:
    return shape.touching_any(shapes)

def touching_all(shape: Shape, shapes: List[Shape]) -> List[Shape]:
    return shape.touching_all(shapes)

def create_group(name: str) -> Group:
    return get_engine().create_group(name)

def get_group(name: str) -> Optional[Group]:
    return get_engine().get_group(name)

def delete_group(name: str) -> None:
    get_engine().delete_group(name)