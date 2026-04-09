import math
import pygame
from typing import List, Dict, Tuple, Callable, Optional, Set
from dataclasses import dataclass
from .shape import Shape
from ..globals import get_engine

@dataclass
class CollisionInfo:
    collided: bool = False
    other: Optional['Shape'] = None
    direction: Optional[str] = None
    overlap_x: float = 0
    overlap_y: float = 0
    penetration: float = 0
    normal_x: float = 0
    normal_y: float = 0

class CollisionSystem:
    def __init__(self) -> None:
        self.collision_callbacks: List[Callable] = []
        self.collision_pairs: Set[Tuple[int, int]] = set()
    
    def on_collision(self, callback: Callable) -> None:
        self.collision_callbacks.append(callback)
    
    def rect_rect(self, a: Shape, b: Shape) -> Optional[CollisionInfo]:
        a_width = a.width * a.scale_x
        a_height = a.height * a.scale_y
        b_width = b.width * b.scale_x
        b_height = b.height * b.scale_y
        
        if not (a.x < b.x + b_width and
                a.x + a_width > b.x and
                a.y < b.y + b_height and
                a.y + a_height > b.y):
            return None
        
        info = CollisionInfo()
        info.collided = True
        info.other = b
        
        overlap_left = (a.x + a_width) - b.x
        overlap_right = (b.x + b_width) - a.x
        overlap_top = (a.y + a_height) - b.y
        overlap_bottom = (b.y + b_height) - a.y
        
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
    
    def rect_circle(self, rect: Shape, circle: Shape) -> Optional[CollisionInfo]:
        radius_x = (circle.radius_x if hasattr(circle, 'radius_x') else circle.radius) * circle.scale_x
        radius_y = (circle.radius_y if hasattr(circle, 'radius_y') else circle.radius) * circle.scale_y
        rect_width = rect.width * rect.scale_x
        rect_height = rect.height * rect.scale_y
        
        closest_x = max(rect.x, min(circle.x, rect.x + rect_width))
        closest_y = max(rect.y, min(circle.y, rect.y + rect_height))
        dx = closest_x - circle.x
        dy = closest_y - circle.y
        
        ellipse_dist = (dx * dx) / (radius_x * radius_x) + (dy * dy) / (radius_y * radius_y)
        if ellipse_dist > 1:
            return None
        
        info = CollisionInfo()
        info.collided = True
        info.other = rect
        
        dist = math.sqrt(dx * dx + dy * dy)
        if dist > 0:
            info.normal_x = dx / dist
            info.normal_y = dy / dist
            angle = math.atan2(dy, dx)
            radius_at_angle = (radius_x * radius_y) / math.sqrt(
                (radius_y * math.cos(angle)) ** 2 + (radius_x * math.sin(angle)) ** 2
            )
            info.penetration = radius_at_angle - dist
        else:
            info.normal_x = 1
            info.normal_y = 0
            info.penetration = min(radius_x, radius_y)
        
        if abs(info.normal_x) > abs(info.normal_y):
            info.direction = "left" if info.normal_x < 0 else "right"
        else:
            info.direction = "top" if info.normal_y < 0 else "bottom"
        
        info.overlap_x = abs(dx)
        info.overlap_y = abs(dy)
        
        return info
    
    def circle_circle(self, a: Shape, b: Shape) -> Optional[CollisionInfo]:
        dx = a.x - b.x
        dy = a.y - b.y
        
        radius_x_a = (a.radius_x if hasattr(a, 'radius_x') else a.radius) * a.scale_x
        radius_y_a = (a.radius_y if hasattr(a, 'radius_y') else a.radius) * a.scale_y
        radius_x_b = (b.radius_x if hasattr(b, 'radius_x') else b.radius) * b.scale_x
        radius_y_b = (b.radius_y if hasattr(b, 'radius_y') else b.radius) * b.scale_y
        
        angle = math.atan2(dy, dx)
        radius_a = (radius_x_a * radius_y_a) / math.sqrt(
            (radius_y_a * math.cos(angle)) ** 2 + (radius_x_a * math.sin(angle)) ** 2
        )
        radius_b = (radius_x_b * radius_y_b) / math.sqrt(
            (radius_y_b * math.cos(angle + math.pi)) ** 2 + (radius_x_b * math.sin(angle + math.pi)) ** 2
        )
        
        dist = math.sqrt(dx * dx + dy * dy)
        if dist > radius_a + radius_b:
            return None
        
        info = CollisionInfo()
        info.collided = True
        info.other = b
        
        if dist > 0:
            info.normal_x = dx / dist
            info.normal_y = dy / dist
            info.penetration = (radius_a + radius_b) - dist
        else:
            info.normal_x = 1
            info.normal_y = 0
            info.penetration = radius_a + radius_b
        
        if abs(info.normal_x) > abs(info.normal_y):
            info.direction = "left" if info.normal_x > 0 else "right"
        else:
            info.direction = "top" if info.normal_y > 0 else "bottom"
        
        info.overlap_x = abs(dx)
        info.overlap_y = abs(dy)
        
        return info
    
    def check(self, shape_a: Shape, shape_b: Shape) -> bool:
        global _engine
        _engine = get_engine()
        
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
    
    def get_collision_info(self, shape_a: Shape, shape_b: Shape) -> Optional[CollisionInfo]:
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
    
    def get_direction(self, shape_a: Shape, shape_b: Shape) -> Optional[str]:
        info = self.get_collision_info(shape_a, shape_b)
        return info.direction if info else None
    
    def resolve(self, shape_a: Shape, shape_b: Shape, mass_a: float = 1, mass_b: float = 1) -> bool:
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
    
    def sweep_test(self, shape: Shape, velocity_x: float, velocity_y: float, 
                   other_shapes: List[Shape]) -> Optional[CollisionInfo]:
        if not other_shapes:
            return None
        
        speed = math.sqrt(velocity_x * velocity_x + velocity_y * velocity_y)
        steps = max(1, int(speed / 5))
        step_x = velocity_x / steps
        step_y = velocity_y / steps
        
        original_x = shape.x
        original_y = shape.y
        
        for _ in range(steps):
            shape.x += step_x
            shape.y += step_y
            
            for other in other_shapes:
                if shape != other and shape.visible and other.visible:
                    info = self.get_collision_info(shape, other)
                    if info:
                        shape.x = original_x
                        shape.y = original_y
                        info.collided = True
                        info.other = other
                        return info
        
        shape.x = original_x
        shape.y = original_y
        return None
    
    def raycast(self, start_x: float, start_y: float, end_x: float, end_y: float, 
                shapes: List[Shape], ignore_shape: Optional[Shape] = None) -> Optional[CollisionInfo]:
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
            
            for shape in shapes:
                if shape == ignore_shape or not shape.visible:
                    continue
                
                temp_shape = Shape(-1, "pixel", current_x, current_y)
                temp_shape.visible = True
                
                if self.check(temp_shape, shape):
                    info = CollisionInfo()
                    info.collided = True
                    info.other = shape
                    info.normal_x = -step_x
                    info.normal_y = -step_y
                    info.penetration = dist - math.sqrt((current_x - start_x) ** 2 + (current_y - start_y) ** 2)
                    return info
        
        return None
    
    def check_all(self, shapes: Dict[int, Shape]) -> List[Tuple[Shape, Shape, CollisionInfo]]:
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