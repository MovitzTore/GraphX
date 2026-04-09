import math
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Union
from time import time as get_time

class EasingStyle(Enum):
    LINEAR = "linear"
    QUAD = "quad"
    CUBIC = "cubic"
    QUART = "quart"
    QUINT = "quint"
    SINE = "sine"
    EXPO = "expo"
    CIRC = "circ"
    BACK = "back"
    BOUNCE = "bounce"
    ELASTIC = "elastic"

class EasingDirection(Enum):
    IN = "in"
    OUT = "out"
    IN_OUT = "in_out"

class TweenStatus(Enum):
    PLAYING = "playing"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class TweenError(Exception):
    pass

def ease_linear(t: float) -> float:
    return t

def ease_quad_in(t: float) -> float:
    return t * t

def ease_quad_out(t: float) -> float:
    return t * (2 - t)

def ease_quad_in_out(t: float) -> float:
    if t < 0.5:
        return 2 * t * t
    return -1 + (4 - 2 * t) * t

def ease_cubic_in(t: float) -> float:
    return t * t * t

def ease_cubic_out(t: float) -> float:
    t -= 1
    return t * t * t + 1

def ease_cubic_in_out(t: float) -> float:
    if t < 0.5:
        return 4 * t * t * t
    t = t * 2 - 2
    return (t * t * t + 2) / 2

def ease_quart_in(t: float) -> float:
    return t * t * t * t

def ease_quart_out(t: float) -> float:
    t -= 1
    return 1 - t * t * t * t

def ease_quart_in_out(t: float) -> float:
    if t < 0.5:
        return 8 * t * t * t * t
    t = t * 2 - 2
    return (1 - t * t * t * t) / 2 + 0.5

def ease_quint_in(t: float) -> float:
    return t * t * t * t * t

def ease_quint_out(t: float) -> float:
    t -= 1
    return 1 + t * t * t * t * t

def ease_quint_in_out(t: float) -> float:
    if t < 0.5:
        return 16 * t * t * t * t * t
    t = t * 2 - 2
    return (1 + t * t * t * t * t) / 2

def ease_sine_in(t: float) -> float:
    return 1 - math.cos(t * math.pi / 2)

def ease_sine_out(t: float) -> float:
    return math.sin(t * math.pi / 2)

def ease_sine_in_out(t: float) -> float:
    return (1 - math.cos(math.pi * t)) / 2

def ease_expo_in(t: float) -> float:
    return 0 if t == 0 else math.pow(2, 10 * (t - 1))

def ease_expo_out(t: float) -> float:
    return 1 if t == 1 else 1 - math.pow(2, -10 * t)

def ease_expo_in_out(t: float) -> float:
    if t == 0 or t == 1:
        return t
    if t < 0.5:
        return math.pow(2, 20 * t - 10) / 2
    return (2 - math.pow(2, -20 * t + 10)) / 2

def ease_circ_in(t: float) -> float:
    return 1 - math.sqrt(1 - t * t)

def ease_circ_out(t: float) -> float:
    return math.sqrt(1 - (t - 1) * (t - 1))

def ease_circ_in_out(t: float) -> float:
    if t < 0.5:
        return (1 - math.sqrt(1 - 4 * t * t)) / 2
    return (math.sqrt(1 - (2 * t - 2) * (2 * t - 2)) + 1) / 2

def ease_back_in(t: float) -> float:
    return t * t * ((1.70158 + 1) * t - 1.70158)

def ease_back_out(t: float) -> float:
    t -= 1
    return t * t * ((1.70158 + 1) * t + 1.70158) + 1

def ease_back_in_out(t: float) -> float:
    if t < 0.5:
        return ease_back_in(t * 2) / 2
    return ease_back_out(t * 2 - 1) / 2 + 0.5

def ease_bounce_out(t: float) -> float:
    if t < 1 / 2.75:
        return 7.5625 * t * t
    elif t < 2 / 2.75:
        t -= 1.5 / 2.75
        return 7.5625 * t * t + 0.75
    elif t < 2.5 / 2.75:
        t -= 2.25 / 2.75
        return 7.5625 * t * t + 0.9375
    else:
        t -= 2.625 / 2.75
        return 7.5625 * t * t + 0.984375

def ease_bounce_in(t: float) -> float:
    return 1 - ease_bounce_out(1 - t)

def ease_bounce_in_out(t: float) -> float:
    if t < 0.5:
        return ease_bounce_in(t * 2) / 2
    return ease_bounce_out(t * 2 - 1) / 2 + 0.5

def ease_elastic_in(t: float) -> float:
    if t == 0 or t == 1:
        return t
    return -math.pow(2, 10 * (t - 1)) * math.sin((t - 1.075) * (2 * math.pi) / 0.3)

def ease_elastic_out(t: float) -> float:
    if t == 0 or t == 1:
        return t
    return math.pow(2, -10 * t) * math.sin((t - 0.075) * (2 * math.pi) / 0.3) + 1

def ease_elastic_in_out(t: float) -> float:
    if t == 0 or t == 1:
        return t
    if t < 0.5:
        return -(math.pow(2, 20 * t - 10) * math.sin((20 * t - 11.125) * (2 * math.pi) / 4.6)) / 2
    return math.pow(2, -20 * t + 10) * math.sin((20 * t - 11.125) * (2 * math.pi) / 4.6) / 2 + 1

def get_easing_function(style: EasingStyle, direction: EasingDirection) -> Callable:
    if not isinstance(style, EasingStyle):
        raise TweenError(f"style must be EasingStyle, got {type(style).__name__}")
    if not isinstance(direction, EasingDirection):
        raise TweenError(f"direction must be EasingDirection, got {type(direction).__name__}")
    
    if style == EasingStyle.LINEAR:
        return ease_linear
    
    if direction == EasingDirection.IN:
        if style == EasingStyle.QUAD:
            return ease_quad_in
        elif style == EasingStyle.CUBIC:
            return ease_cubic_in
        elif style == EasingStyle.QUART:
            return ease_quart_in
        elif style == EasingStyle.QUINT:
            return ease_quint_in
        elif style == EasingStyle.SINE:
            return ease_sine_in
        elif style == EasingStyle.EXPO:
            return ease_expo_in
        elif style == EasingStyle.CIRC:
            return ease_circ_in
        elif style == EasingStyle.BACK:
            return ease_back_in
        elif style == EasingStyle.BOUNCE:
            return ease_bounce_in
        elif style == EasingStyle.ELASTIC:
            return ease_elastic_in
    
    elif direction == EasingDirection.OUT:
        if style == EasingStyle.QUAD:
            return ease_quad_out
        elif style == EasingStyle.CUBIC:
            return ease_cubic_out
        elif style == EasingStyle.QUART:
            return ease_quart_out
        elif style == EasingStyle.QUINT:
            return ease_quint_out
        elif style == EasingStyle.SINE:
            return ease_sine_out
        elif style == EasingStyle.EXPO:
            return ease_expo_out
        elif style == EasingStyle.CIRC:
            return ease_circ_out
        elif style == EasingStyle.BACK:
            return ease_back_out
        elif style == EasingStyle.BOUNCE:
            return ease_bounce_out
        elif style == EasingStyle.ELASTIC:
            return ease_elastic_out
    
    elif direction == EasingDirection.IN_OUT:
        if style == EasingStyle.QUAD:
            return ease_quad_in_out
        elif style == EasingStyle.CUBIC:
            return ease_cubic_in_out
        elif style == EasingStyle.QUART:
            return ease_quart_in_out
        elif style == EasingStyle.QUINT:
            return ease_quint_in_out
        elif style == EasingStyle.SINE:
            return ease_sine_in_out
        elif style == EasingStyle.EXPO:
            return ease_expo_in_out
        elif style == EasingStyle.CIRC:
            return ease_circ_in_out
        elif style == EasingStyle.BACK:
            return ease_back_in_out
        elif style == EasingStyle.BOUNCE:
            return ease_bounce_in_out
        elif style == EasingStyle.ELASTIC:
            return ease_elastic_in_out
    
    return ease_linear

class Tween:
    def __init__(self, obj: Any, duration: float, goal: Dict[str, Any], 
                 style: EasingStyle = EasingStyle.LINEAR, 
                 direction: EasingDirection = EasingDirection.OUT):
        # validation
        if obj is None:
            raise TweenError("Object cannot be None")
        
        if not isinstance(duration, (int, float)):
            raise TweenError(f"Duration must be a number, got {type(duration).__name__}")
        
        if duration <= 0:
            raise TweenError(f"Duration must be positive, got {duration}")
        
        if not isinstance(goal, dict):
            raise TweenError(f"Goal must be a dictionary, got {type(goal).__name__}")
        
        if not goal:
            raise TweenError("Goal dictionary cannot be empty")
        
        if not isinstance(style, EasingStyle):
            raise TweenError(f"style must be EasingStyle, got {type(style).__name__}")
        
        if not isinstance(direction, EasingDirection):
            raise TweenError(f"direction must be EasingDirection, got {type(direction).__name__}")
        
        # check if properties exist (warning only)
        for prop in goal.keys():
            if not hasattr(obj, prop):
                print(f"Warning: '{prop}' might not be a valid property of {type(obj).__name__}")
        
        self.obj = obj
        self.duration = float(duration)
        self.goal = goal
        self.style = style
        self.direction = direction
        
        self._start_time: Optional[float] = None
        self._status = TweenStatus.PLAYING
        self._start_values: Dict[str, Any] = {}
        self._easing_func = get_easing_function(style, direction)
        self._speed = 1.0
        self._elapsed_before_pause: float = 0
        
        self.on_complete: Optional[Callable] = None
        self.on_update: Optional[Callable] = None
        
        self._start()
    
    def _start(self) -> 'Tween':
        self._start_time = get_time()
        for prop, goal_val in self.goal.items():
            if hasattr(self.obj, prop):
                self._start_values[prop] = getattr(self.obj, prop)
            else:
                print(f"Warning: Property '{prop}' not found on object, skipping")
        return self
    
    def play(self) -> 'Tween':
        try:
            if self._status == TweenStatus.PAUSED:
                self._status = TweenStatus.PLAYING
                self._start_time = get_time() - (self._elapsed_before_pause / self._speed)
            elif self._status == TweenStatus.COMPLETED:
                self._status = TweenStatus.PLAYING
                self._elapsed_before_pause = 0
                self._start_time = get_time()
                for prop, start_val in self._start_values.items():
                    if hasattr(self.obj, prop):
                        setattr(self.obj, prop, start_val)
            elif self._status == TweenStatus.CANCELLED:
                self._status = TweenStatus.PLAYING
                self._elapsed_before_pause = 0
                self._start_time = get_time()
        except Exception as e:
            raise TweenError(f"Failed to play tween: {str(e)}")
        return self
    
    def stop(self) -> None:
        self._status = TweenStatus.CANCELLED
    
    def pause(self) -> None:
        if self._status == TweenStatus.PLAYING:
            self._status = TweenStatus.PAUSED
            if self._start_time:
                self._elapsed_before_pause = (get_time() - self._start_time) * self._speed
    
    @property
    def speed(self) -> float:
        return self._speed
    
    @speed.setter
    def speed(self, value: float) -> None:
        if not isinstance(value, (int, float)):
            raise TweenError(f"Speed must be a number, got {type(value).__name__}")
        if value <= 0:
            value = 0.1
        try:
            if self._status == TweenStatus.PLAYING and self._start_time:
                now = get_time()
                elapsed = (now - self._start_time) * self._speed
                self._start_time = now - (elapsed / value)
            self._speed = value
        except Exception as e:
            raise TweenError(f"Failed to set speed: {str(e)}")
    
    @property
    def goals(self) -> Dict[str, Any]:
        return self.goal.copy()
    
    @property
    def EasingStyle(self) -> EasingStyle:
        return self.style
    
    @property
    def EasingDirection(self) -> EasingDirection:
        return self.direction
    
    @property
    def status(self) -> TweenStatus:
        return self._status
    
    def _clamp_color(self, value: float) -> int:
        return max(0, min(255, int(round(value))))
    
    def update(self) -> bool:
        try:
            if self._status != TweenStatus.PLAYING:
                return False
            
            if self._start_time is None:
                return True
            
            now = get_time()
            elapsed = (now - self._start_time) * self._speed
            elapsed = min(elapsed, self.duration)
            t = elapsed / self.duration if self.duration > 0 else 1
            eased_t = self._easing_func(t)
            
            for prop, goal_val in self.goal.items():
                if not hasattr(self.obj, prop):
                    continue
                
                start_val = self._start_values.get(prop, 0)
                
                if isinstance(goal_val, (int, float)):
                    new_val = start_val + (goal_val - start_val) * eased_t
                    try:
                        setattr(self.obj, prop, new_val)
                    except Exception as e:
                        print(f"Warning: Failed to set {prop}: {str(e)}")
                
                elif isinstance(goal_val, (tuple, list)) and len(goal_val) == 3:
                    if isinstance(start_val, (tuple, list)) and len(start_val) == 3:
                        new_r = start_val[0] + (goal_val[0] - start_val[0]) * eased_t
                        new_g = start_val[1] + (goal_val[1] - start_val[1]) * eased_t
                        new_b = start_val[2] + (goal_val[2] - start_val[2]) * eased_t
                        
                        new_r = self._clamp_color(new_r)
                        new_g = self._clamp_color(new_g)
                        new_b = self._clamp_color(new_b)
                        
                        try:
                            setattr(self.obj, prop, (new_r, new_g, new_b))
                        except Exception as e:
                            print(f"Warning: Failed to set color {prop}: {str(e)}")
            
            if self.on_update:
                try:
                    self.on_update()
                except Exception as e:
                    print(f"Warning: on_update callback failed: {str(e)}")
            
            if elapsed >= self.duration:
                for prop, goal_val in self.goal.items():
                    if hasattr(self.obj, prop):
                        try:
                            setattr(self.obj, prop, goal_val)
                        except Exception as e:
                            print(f"Warning: Failed to set final {prop}: {str(e)}")
                self._status = TweenStatus.COMPLETED
                if self.on_complete:
                    try:
                        self.on_complete()
                    except Exception as e:
                        print(f"Warning: on_complete callback failed: {str(e)}")
                return False
            
            return True
        
        except Exception as e:
            print(f"Error in tween update: {str(e)}")
            self._status = TweenStatus.CANCELLED
            return False

class TweenService:
    def __init__(self):
        self._active_tweens: List[Tween] = []
    
    def new(self, obj: Any, duration: float, goal: Dict[str, Any],
            style: EasingStyle = EasingStyle.LINEAR,
            direction: EasingDirection = EasingDirection.OUT) -> Tween:
        try:
            tween = Tween(obj, duration, goal, style, direction)
            self._active_tweens.append(tween)
            return tween
        except TweenError as e:
            print(f"Tween creation failed: {str(e)}")
            raise
    
    def update(self) -> None:
        for tween in self._active_tweens[:]:
            try:
                still_active = tween.update()
                if not still_active:
                    self._active_tweens.remove(tween)
            except Exception as e:
                print(f"Error updating tween: {str(e)}")
                self._active_tweens.remove(tween)
    
    def stop_all(self) -> None:
        for tween in self._active_tweens:
            try:
                tween.stop()
            except Exception as e:
                print(f"Error stopping tween: {str(e)}")
        self._active_tweens.clear()
    
    def get_tweens(self, obj: Any) -> List[Tween]:
        return [t for t in self._active_tweens if t.obj == obj]
    
    def cancel_tweens(self, obj: Any) -> None:
        for tween in self._active_tweens[:]:
            if tween.obj == obj:
                tween.stop()
                self._active_tweens.remove(tween)

_tween_service = TweenService()

def tween(obj: Any, duration: float, goal: Dict[str, Any],
          style: EasingStyle = EasingStyle.LINEAR,
          direction: EasingDirection = EasingDirection.OUT) -> Tween:
    return _tween_service.new(obj, duration, goal, style, direction)

def update_tweens() -> None:
    _tween_service.update()

def stop_all_tweens() -> None:
    _tween_service.stop_all()

def cancel_tweens(obj: Any) -> None:
    _tween_service.cancel_tweens(obj)