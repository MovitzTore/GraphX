# graphX

A lightweight 2D framework

## Installation
```python
pip install pygame
```
Place `GraphX` folder in your project dir

## Quick Start

```python
from GraphX.framework import *

create_window("My Game", 800, 600)

player = create_shape("rectangle", 400, 300, width=50, height=50, color=(0, 255, 0))

def on_space():
    print("Space pressed")

on_key_press(KeyCode.SPACE, on_space)

while is_running():
    update()
```

## Shapes

### rectangle (rect)
```python
box = create_shape("rectangle", x, y, width=50, height=50, color=(255,0,0), filled=True)
```

### circle (circ, sphere)
```python
circle = create_shape("circle", x, y, radius=25, color=(0,0,255))
circle = create_shape("circle", x, y, width=50, height=50)
```

### oval
```python
oval = create_shape("oval", x, y, radius_x=30, radius_y=20, color=(255,255,0))
oval = create_shape("oval", x, y, width=60, height=40)
```

### pixel
```python
pixel = create_shape("pixel", x, y, color=(255,255,255))
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

## Collision

### simple collision
```python
if player.is_touching(enemy):
    print("ouch!")

if player.is_touching("borders"):
    print("hit the edge!")

# check specific edges
if player.at_left_edge:
    player.x = 10
if player.at_right_edge:
    player.x = 790
if player.at_top_edge:
    player.y = 10
if player.at_bottom_edge:
    player.y = 590

# check against multiple shapes
touched = player.touching_any([coin1, coin2, coin3])
if touched:
    delete_shape(touched)

all_touching = player.touching_all([enemy, spike, lava])
```

### advanced collision
```python
if check_collision(player, enemy):
    # handle

direction = get_collision_direction(player, wall)

info = get_collision_info(player, enemy)
# info.direction, info.penetration, info.normal_x, info.normal_y

resolve_collision(player, enemy, mass_a=1, mass_b=2)

result = sweep_test(bullet, vx, vy, [enemy1, enemy2])

hit = raycast(start_x, start_y, end_x, end_y, shapes, ignore_shape=None)

nearby = get_nearby_shapes(shape, radius=2)

all_shapes = get_all_shapes()
```

## Mouse

```python
# simple mouse object
box.x = mouse.x - 25
box.y = mouse.y - 25

if mouse.is_down(1):  # left click
    box.color = (255,0,0)

# mouse callbacks
def on_left_click(x, y):
    print(f"clicked at {x}, {y}")

def on_move(x, y):
    print(f"mouse at {x}, {y}")

def on_wheel(x, y):
    print(f"scrolled {x}, {y}")

on_mouse_press(1, on_left_click)   # 1=left, 2=middle, 3=right
on_mouse_release(1, callback)
on_mouse_move(on_move)
on_mouse_wheel(on_wheel)

if is_mouse_down(1):
    pos = get_mouse_position()
```

## Keyboard

```python
def on_space():
    print("Space pressed")

def on_escape():
    quit()

on_key_press(KeyCode.SPACE, on_space)
on_key_release(KeyCode.ESCAPE, on_escape)

if is_key_down(KeyCode.W):
    player.y -= 5
```

Key codes: `SPACE`, `RETURN`, `ESCAPE`, `BACKSPACE`, `TAB`, `DELETE`, `INSERT`, `HOME`, `END`, `PAGE_UP`, `PAGE_DOWN`, `UP`, `DOWN`, `LEFT`, `RIGHT`, `A`-`Z`, `0`-`9`, `F1`-`F12`, `LSHIFT`, `RSHIFT`, `LCTRL`, `RCTRL`, `LALT`, `RALT`

## Tweens

```python
from GraphX.framework import *

create_window("Tween Demo", 800, 600)

box = create_shape("rectangle", 100, 300, width=50, height=50, color=(0,255,0))

# create a tween
move = tween(box, 2, {"x": 700}, EasingStyle.BOUNCE, EasingDirection.OUT)

# control it
move.play()
move.pause()
move.stop()
move.speed = 0.5  # half speed

# check properties
print(move.goals)  # prints {"x": 700}
print(move.EasingStyle)  # prints EasingStyle.BOUNCE
print(move.EasingDirection)  # prints EasingDirection.OUT

# run code when done
def on_finished():
    print("tween done!")

move.on_complete = on_finished

# color tweens
color_tween = tween(box, 2, {"color": (0, 0, 255)}, EasingStyle.ELASTIC, EasingDirection.IN_OUT)

# multiple properties at once
tween(box, 1, {"x": 500, "y": 300, "scale_x": 2}, EasingStyle.QUAD, EasingDirection.OUT)

# update tweens in your main loop
while is_running():
    update_tweens()
    update()

# stop all tweens
stop_all_tweens()

# cancel tweens on a specific object
cancel_tweens(box)
```

### Easing Styles
`LINEAR`, `QUAD`, `CUBIC`, `QUART`, `QUINT`, `SINE`, `EXPO`, `CIRC`, `BACK`, `BOUNCE`, `ELASTIC`

### Easing Directions
`IN`, `OUT`, `IN_OUT`

## Assets

```python
load("texture", "sprites/player.png", "player")
load("sound", "sounds/jump.wav", "jump")
load("music", "music/theme.ogg", "theme")
load("font", "fonts/arial.ttf", "main", size=32)

texture = get_texture("player")
sound = get_sound("jump")
font = get_font("main")

play_sound("jump")
play_music("theme", loops=-1)
stop_music()
```

## Drawing

```python
draw_text("Hello", None, 100, 100, color=(255,255,255), size=24)
draw_text("Hello", "main", 100, 150, color=(0,255,0), size=48)

def custom_draw():
    # called every frame after shapes
    draw_text("Score: " + str(score), None, 10, 10, size=24)

set_draw_callback(custom_draw)

fill_screen(r, g, b)
```

## Camera

```python
set_camera(x, y)
move_camera(dx, dy)
```

## Utils

```python
set_fps(60)
delta = get_delta_time()
wait(ms)
clear_all()
quit()

update_spatial_grid(shape)
get_shape_position(shape)
```

## API References

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
| `get_all_shapes()` | Returns list of all shapes |
| `get_shape_position(shape)` | Returns (x, y) tuple of shape position |
| `clear_all()` | Removes all shapes |

Shape parameters by type:
- **rectangle**: `width`, `height`, `filled`, `color`
- **circle**: `radius` or `width`/`height` (must be equal), `filled`, `color`
- **oval**: `radius_x`/`radius_y` or `width`/`height`, `filled`, `color`
- **pixel**: `color`

Common parameters for all shapes: `z_index`, `rotation`, `scale_x`, `scale_y`, `visible`

### Collision Functions (SIMPLE)

| Function | Description |
|----------|-------------|
| `shape.is_touching(other)` | Checks if shape touches another shape or "borders" |
| `shape.touching_borders()` | Checks if shape touches window edges |
| `shape.touching_any(list)` | Returns first shape touched from a list |
| `shape.touching_all(list)` | Returns all shapes touched from a list |
| `shape.at_left_edge` | True if shape touches left edge |
| `shape.at_right_edge` | True if shape touches right edge |
| `shape.at_top_edge` | True if shape touches top edge |
| `shape.at_bottom_edge` | True if shape touches bottom edge |
| `shape.touching_border` | True if shape touches any edge |

### Collision Functions (ADVANCED)

| Function | Description |
|----------|-------------|
| `check_collision(a, b)` | Returns boolean |
| `get_collision_direction(a, b)` | Returns string or None |
| `get_collision_info(a, b)` | Returns CollisionInfo or None |
| `resolve_collision(a, b, mass_a=1, mass_b=1)` | Separates colliding shapes |
| `sweep_test(shape, vx, vy, others)` | Returns CollisionInfo or None |
| `raycast(x1, y1, x2, y2, shapes, ignore=None)` | Returns CollisionInfo or None |
| `check_all_collisions(shapes)` | Returns list of collision tuples |
| `get_nearby_shapes(shape, radius=2)` | Returns list of nearby shapes |

### Mouse Functions

| Function | Description |
|----------|-------------|
| `mouse.x` | Mouse X position |
| `mouse.y` | Mouse Y position |
| `mouse.pos` | Mouse position as (x, y) tuple |
| `mouse.is_down(button)` | Returns True if button is pressed |
| `on_mouse_press(button, callback)` | Registers callback for mouse press (callback gets x, y) |
| `on_mouse_release(button, callback)` | Registers callback for mouse release (callback gets x, y) |
| `on_mouse_move(callback)` | Registers callback for mouse movement (callback gets x, y) |
| `on_mouse_wheel(callback)` | Registers callback for scroll wheel (callback gets scroll_x, scroll_y) |
| `is_mouse_down(button)` | Returns boolean |
| `get_mouse_position()` | Returns (x, y) tuple |

### Keyboard Functions

| Function | Description |
|----------|-------------|
| `on_key_press(key, callback)` | Registers callback for key press (callback gets no arguments) |
| `on_key_release(key, callback)` | Registers callback for key release (callback gets no arguments) |
| `is_key_down(key)` | Returns boolean |

### Tween Functions

| Function | Description |
|----------|-------------|
| `tween(obj, duration, goal, style, direction)` | Creates and returns a Tween object |
| `update_tweens()` | Updates all active tweens (call in main loop) |
| `stop_all_tweens()` | Stops all tweens |
| `cancel_tweens(obj)` | Cancels all tweens on a specific object |

Tween Methods:
| Method | Description |
|--------|-------------|
| `tween.play()` | Plays or resumes the tween |
| `tween.pause()` | Pauses the tween |
| `tween.stop()` | Stops and cancels the tween |
| `tween.speed` | Gets or sets the tween speed (1 = normal) |
| `tween.goals` | Returns the goal dictionary |
| `tween.EasingStyle` | Returns the easing style |
| `tween.EasingDirection` | Returns the easing direction |
| `tween.on_complete` | Set a callback for when tween finishes |
| `tween.on_update` | Set a callback called every frame during tween |

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

All pygame key constants are exposed through `KeyCode`. Common values: `SPACE`, `RETURN`, `ESCAPE`, `BACKSPACE`, `TAB`, `DELETE`, `INSERT`, `HOME`, `END`, `PAGE_UP`, `PAGE_DOWN`, `UP`, `DOWN`, `LEFT`, `RIGHT`, `A`-`Z`, `0`-`9`, `F1`-`F12`, `LSHIFT`, `RSHIFT`, `LCTRL`, `RCTRL`, `LALT`, `RALT`
