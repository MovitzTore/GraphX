import pygame
from typing import Dict, List, Tuple
from .shapes.shape import Shape
from .globals import get_engine
class SpatialGrid:
    def __init__(self, cell_size: float = 100) -> None:
        global _engine
        _engine = get_engine()
        
        if not isinstance(cell_size, (int, float)) or cell_size <= 0:
            error_msg = f"cell_size must be a positive number"
            if _engine and _engine.error_handler:
                _engine.error_handler.show_fatal_error(_engine.screen, error_msg)
            raise ValueError(error_msg)
        self.cell_size = float(cell_size)
        self.grid: Dict[Tuple[int, int], List[Shape]] = {}
    
    def _get_cell(self, x: float, y: float) -> Tuple[int, int]:
        return (int(x // self.cell_size), int(y // self.cell_size))
    
    def _get_cells_for_shape(self, shape: Shape) -> List[Tuple[int, int]]:
        global _engine
        _engine = get_engine()
        
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
    
    def add(self, shape: Shape) -> None:
        cells = self._get_cells_for_shape(shape)
        for cell in cells:
            if cell not in self.grid:
                self.grid[cell] = []
            if shape not in self.grid[cell]:
                self.grid[cell].append(shape)
    
    def remove(self, shape: Shape) -> None:
        cells = self._get_cells_for_shape(shape)
        for cell in cells:
            if cell in self.grid and shape in self.grid[cell]:
                self.grid[cell].remove(shape)
                if not self.grid[cell]:
                    del self.grid[cell]
    
    def update(self, shape: Shape) -> None:
        self.remove(shape)
        self.add(shape)
    
    def get_nearby(self, shape: Shape, radius: int = 2) -> List[Shape]:
        global _engine
        _engine = get_engine()
        
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
        return list(nearby)