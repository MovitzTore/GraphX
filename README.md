```markdown
# graphX

A lightweight 2D framework

## Installation

pip install pygame
```

Place `graphX.py` in your project dir

## Quick Start

```python
import graphX as gx

gx.create_window("My Game", 800, 600)

player = gx.create_shape("rectangle", 400, 300, width=50, height=50, color=(0, 255, 0))

def on_key():
    print("Space pressed")

gx.on_key_press(gx.KeyCode.SPACE, on_key)

while gx.is_running():
    gx.update()
```

## Shapes

### rectangle (rect)
```python
box = gx.create_shape("rectangle", x, y, width=50, height=50, color=(255,0,0), filled=True)
```

### circle (circ)
```python
circle = gx.create_shape("circle", x, y, radius=25, color=(0,0,255))
circle = gx.create_shape("circle", x, y, width=50, height=50)
```

### oval
```python
oval = gx.create_shape("oval", x, y, radius_x=30, radius_y=20, color=(255,255,0))
oval = gx.create_shape("oval", x, y, width=60, height=40)
```

### pixel
```python
pixel = gx.create_shape("pixel", x, y, color=(255,255,255))
```

## Shape Properties

```python
shape.x = 100
shape.y = 200
shape.z_index = 5
shape.rotation = 45
shape.scale_x = 2.0
shape.scale_y = 1.5
shape.visible = False
shape.color = (255,0,0)
shape.apply_texture("sprite_name")
```

## input

### keyboard
```python
gx.on_key_press(gx.KeyCode.SPACE, callback)
gx.on_key_release(gx.KeyCode.ESCAPE, callback)

if gx.is_key_down(gx.KeyCode.W):
    player.y -= 5
```

Key codes: `SPACE`, `RETURN`, `ESCAPE`, `UP`, `DOWN`, `LEFT`, `RIGHT`, `A`-`Z`, `0`-`9`, `F1`-`F12`, `LSHIFT`, `RSHIFT`, `LCTRL`, `RCTRL`, `LALT`, `RALT`

### mouse
```python
gx.on_mouse_press(1, callback)   # 1=left, 2=middle, 3=right
gx.on_mouse_release(1, callback)
gx.on_mouse_move(callback)
gx.on_mouse_wheel(callback)

if gx.is_mouse_down(1):
    pos = gx.get_mouse_position()
```

## collision

```python
if gx.check_collision(player, enemy):
    # handle

direction = gx.get_collision_direction(player, wall)

info = gx.get_collision_info(player, enemy)
# info.direction, info.penetration, info.normal_x, info.normal_y

gx.resolve_collision(player, enemy, mass_a=1, mass_b=2)

result = gx.sweep_test(bullet, vx, vy, [enemy1, enemy2])

hit = gx.raycast(start_x, start_y, end_x, end_y, shapes, ignore_shape=None)
```

## assets

```python
gx.load("texture", "sprites/player.png", "player")
gx.load("sound", "sounds/jump.wav", "jump")
gx.load("music", "music/theme.ogg", "theme")
gx.load("font", "fonts/arial.ttf", "main", size=32)

texture = gx.get_texture("player")
sound = gx.get_sound("jump")
font = gx.get_font("main")

gx.play_sound("jump")
gx.play_music("theme", loops=-1)
gx.stop_music()
```

## drawing

```python
gx.draw_text("Hello", None, 100, 100, color=(255,255,255), size=24)
gx.draw_text("Hello", "main", 100, 150, color=(0,255,0), size=48)

def custom_draw():
    # called every frame after shapes

gx.set_draw_callback(custom_draw)

gx.fill_screen(r, g, b)
```

## camera

```python
gx.set_camera(x, y)
gx.move_camera(dx, dy)
```

## utils

```python
gx.set_fps(60)
delta = gx.get_delta_time()
gx.wait(ms)
gx.clear_all()
gx.quit()

# Spatial grid for optimization
nearby = gx.get_nearby_shapes(shape, radius=2)
gx.update_spatial_grid(shape)
```

## API refrences

### Engine Functions

| Function | Description |
|----------|-------------|
| `create_window(title, width, height)` | Creates game window |
| `update()` | Processes events and renders frame |
| `is_running()` | Returns True if engine is active |
| `set_fps(fps)` | Sets target frame rate |
| `get_delta_time()` | Returns time since last frame (seconds) |
| `quit()` | Exits the engine |

### Shape Functions

| Function | Description |
|----------|-------------|
| `create_shape(type, x, y, **kwargs)` | Creates and returns a Shape object |
| `delete_shape(shape)` | Removes shape from engine |
| `get_shape(id)` | Returns shape by ID or None |
| `clear_all()` | Removes all shapes |

Shape parameters by type:
- **rectangle**: `width`, `height`, `filled`, `color`
- **circle**: `radius` or `width`/`height`, `filled`, `color`
- **oval**: `radius_x`/`radius_y` or `width`/`height`, `filled`, `color`
- **pixel**: `color`

Common parameters for all shapes: `z_index`, `rotation`, `scale_x`, `scale_y`, `visible`

### Input Functions

| Function | Description |
|----------|-------------|
| `on_key_press(key, callback)` | Registers callback for key press |
| `on_key_release(key, callback)` | Registers callback for key release |
| `on_mouse_press(button, callback)` | Registers callback for mouse button press |
| `on_mouse_release(button, callback)` | Registers callback for mouse button release |
| `on_mouse_move(callback)` | Registers callback for mouse movement |
| `on_mouse_wheel(callback)` | Registers callback for scroll wheel |
| `is_key_down(key)` | Returns boolean |
| `is_mouse_down(button)` | Returns boolean |
| `get_mouse_position()` | Returns (x, y) tuple |

### Asset Functions

| Function | Description |
|----------|-------------|
| `load(type, path, name=None, **kwargs)` | Loads asset, returns asset object |
| `get_texture(name)` | Returns pygame Surface |
| `get_sound(name)` | Returns pygame Sound |
| `get_font(name)` | Returns pygame Font |
| `play_sound(name, loops=0, maxtime=0, fade_ms=0)` | Plays sound |
| `play_music(name, loops=-1, start=0, fade_ms=0)` | Plays music |
| `stop_music()` | Stops current music |

### Collision Functions

| Function | Description |
|----------|-------------|
| `check_collision(a, b)` | Returns boolean |
| `get_collision_direction(a, b)` | Returns string or None |
| `get_collision_info(a, b)` | Returns CollisionInfo or None |
| `resolve_collision(a, b, mass_a=1, mass_b=1)` | Separates colliding shapes |
| `sweep_test(shape, vx, vy, others)` | Returns CollisionInfo or None |
| `raycast(x1, y1, x2, y2, shapes, ignore=None)` | Returns CollisionInfo or None |
| `check_all_collisions(shapes)` | Returns list of collision tuples |
| `get_nearby_shapes(shape, radius=2)` | Returns set of nearby shapes |

### Drawing Functions

| Function | Description |
|----------|-------------|
| `fill_screen(r, g, b)` | Sets background color |
| `draw_text(text, font_name, x, y, color, size)` | Returns text width |
| `set_draw_callback(callback)` | Sets function called each frame after shapes |
| `set_camera(x, y)` | Sets camera position |
| `move_camera(dx, dy)` | Moves camera relative |

### CollisionInfo Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `collided` | bool | True if collision occurred |
| `other` | Shape | The other shape involved |
| `direction` | str | "left", "right", "top", or "bottom" |
| `overlap_x` | float | Overlap amount on X axis |
| `overlap_y` | float | Overlap amount on Y axis |
| `penetration` | float | Minimum penetration depth |
| `normal_x` | float | Collision normal X component |
| `normal_y` | float | Collision normal Y component |

### KeyCode Constants

All pygame key constants are exposed through `gx.KeyCode`. Common values: `SPACE`, `RETURN`, `ESCAPE`, `UP`, `DOWN`, `LEFT`, `RIGHT`, `A`-`Z`, `0`-`9`, `F1`-`F12`, `LSHIFT`, `RSHIFT`, `LCTRL`, `RCTRL`, `LALT`, `RALT`.
```
