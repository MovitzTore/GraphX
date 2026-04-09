import pygame
import os
from typing import Dict, Optional, Union
from ..globals import get_engine
class AssetManager:
    def __init__(self) -> None:
        self.textures: Dict[str, pygame.Surface] = {}
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.music: Dict[str, str] = {}
        self.fonts: Dict[str, pygame.font.Font] = {}
        self.error_handler = None
        
        try:
            pygame.mixer.init()
        except Exception:
            pass
    
    def set_error_handler(self, error_handler) -> None:
        self.error_handler = error_handler
    
    def _validate_name(self, name: str) -> None:
        if name is not None and not isinstance(name, str):
            raise ValueError(f"Asset name must be a string, got {type(name).__name__}")
        if name == "":
            raise ValueError("Asset name cannot be empty")
    
    def load(self, asset_type: str, path: Optional[str], name: Optional[str] = None, 
             **kwargs) -> Union[pygame.Surface, pygame.mixer.Sound, str, pygame.font.Font]:
        global _engine
        _engine = get_engine()
        
        if asset_type not in ["texture", "sound", "music", "font"]:
            error_msg = f"Unknown asset type: '{asset_type}'. Valid types: texture, sound, music, font"
            if self.error_handler:
                self.error_handler.show_fatal_error(_engine.screen if _engine else None, error_msg)
            raise ValueError(error_msg)
        
        if name is None:
            if path is not None:
                name = os.path.basename(path).split('.')[0]
            else:
                name = "default"
        
        self._validate_name(name)
        
        if asset_type == "texture":
            return self._load_texture(path, name)
        elif asset_type == "sound":
            return self._load_sound(path, name)
        elif asset_type == "music":
            return self._load_music(path, name)
        else:
            return self._load_font(path, name, kwargs.get("size", 16))
    
    def _load_texture(self, path: str, name: str) -> pygame.Surface:
        global _engine
        _engine = get_engine()
        
        if not os.path.exists(path):
            error_msg = f"Texture file not found: {path}"
            if self.error_handler:
                self.error_handler.show_fatal_error(_engine.screen if _engine else None, error_msg)
            raise FileNotFoundError(error_msg)
        
        try:
            surface = pygame.image.load(path).convert_alpha()
            self.textures[name] = surface
            return surface
        except Exception as e:
            error_msg = f"Failed to load texture: {path}\n{str(e)}"
            if self.error_handler:
                self.error_handler.show_fatal_error(_engine.screen if _engine else None, error_msg)
            raise
    
    def _load_sound(self, path: str, name: str) -> pygame.mixer.Sound:
        global _engine
        _engine = get_engine()
        
        if not os.path.exists(path):
            error_msg = f"Sound file not found: {path}"
            if self.error_handler:
                self.error_handler.show_fatal_error(_engine.screen if _engine else None, error_msg)
            raise FileNotFoundError(error_msg)
        
        try:
            sound = pygame.mixer.Sound(path)
            self.sounds[name] = sound
            return sound
        except Exception as e:
            error_msg = f"Failed to load sound: {path}\n{str(e)}"
            if self.error_handler:
                self.error_handler.show_fatal_error(_engine.screen if _engine else None, error_msg)
            raise
    
    def _load_music(self, path: str, name: str) -> str:
        global _engine
        _engine = get_engine()
        
        if not os.path.exists(path):
            error_msg = f"Music file not found: {path}"
            if self.error_handler:
                self.error_handler.show_fatal_error(_engine.screen if _engine else None, error_msg)
            raise FileNotFoundError(error_msg)
        
        self.music[name] = path
        return path
    
    def _load_font(self, path: Optional[str], name: str, size: int) -> pygame.font.Font:
        global _engine
        _engine = get_engine()
        
        if not isinstance(size, (int, float)) or size <= 0:
            error_msg = f"Font size must be a positive number, got {size}"
            if self.error_handler:
                self.error_handler.show_fatal_error(_engine.screen if _engine else None, error_msg)
            raise ValueError(error_msg)
        
        if not pygame.font.get_init():
            pygame.font.init()
        
        try:
            if path is None or not os.path.exists(path):
                font = pygame.font.Font(None, int(size))
            else:
                font = pygame.font.Font(path, int(size))
            self.fonts[name] = font
            return font
        except Exception:
            font = pygame.font.Font(None, int(size))
            self.fonts[name] = font
            return font
    
    def get_texture(self, name: str) -> pygame.Surface:
        global _engine
        _engine = get_engine()
        
        if name not in self.textures:
            error_msg = f"Texture '{name}' not found"
            if self.error_handler:
                self.error_handler.show_fatal_error(_engine.screen if _engine else None, error_msg)
            raise KeyError(error_msg)
        return self.textures[name]
    
    def get_sound(self, name: str) -> pygame.mixer.Sound:
        global _engine
        _engine = get_engine()
        
        if name not in self.sounds:
            error_msg = f"Sound '{name}' not found"
            if self.error_handler:
                self.error_handler.show_fatal_error(_engine.screen if _engine else None, error_msg)
            raise KeyError(error_msg)
        return self.sounds[name]
    
    def get_music(self, name: str) -> str:
        global _engine
        _engine = get_engine()
        
        if name not in self.music:
            error_msg = f"Music '{name}' not found"
            if self.error_handler:
                self.error_handler.show_fatal_error(_engine.screen if _engine else None, error_msg)
            raise KeyError(error_msg)
        return self.music[name]
    
    def get_font(self, name: str) -> pygame.font.Font:
        global _engine
        _engine = get_engine()
        
        if name not in self.fonts:
            error_msg = f"Font '{name}' not found"
            if self.error_handler:
                self.error_handler.show_fatal_error(_engine.screen if _engine else None, error_msg)
            raise KeyError(error_msg)
        return self.fonts[name]