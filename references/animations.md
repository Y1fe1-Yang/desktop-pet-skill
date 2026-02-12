# Desktop Pet Animation System

## Animation Presets

### core (3 animations)
**Best for**: Quick generation, minimal complexity
- `idle` - Default breathing animation (auto-trigger)
- `walk` - Walking cycle (drag-trigger)
- `jump` - Jump/bounce (click-trigger)

### standard (7 animations) - **RECOMMENDED**
**Best for**: Rich interactions without overwhelming complexity
- All core animations +
- `happy` - Excited bounce (double-click)
- `pet` - Being petted reaction (long-press, shows hearts)
- `sleep` - Sleeping/resting (60s idle timeout, shows Z symbols)
- `eat` - Eating animation (right-click menu)

### complete (10 animations)
**Best for**: Maximum variety, game-like experience
- All standard animations +
- `attack` - Attack/pounce (special trigger)
- `hurt` - Taking damage (shake trigger)
- `death` - Defeat animation (special trigger)

## Interaction Triggers

| Interaction | Animation | Visual Effect |
|------------|-----------|---------------|
| Drag | walk | Pet follows cursor |
| Single Click | jump | Bounces up |
| Double Click | happy | Happy bounce |
| Long Press (2s) | pet | Hearts float up ❤️💕💖 |
| Hover | curious/happy | Gentle reaction |
| Right-Click | menu | Context menu appears |
| Idle 5s | idle | Breathing animation |
| Idle 60s | sleep | Z symbols float 💤 |
| Keyboard 1-9 | Switch animations | Desktop only |
| Space | Random animation | Desktop only |

## Platform Features

### Web Version
- ✅ All interactions except keyboard shortcuts
- ✅ Drag anywhere on screen
- ✅ Click interactions
- ✅ Control panel with animation buttons

### Browser Extension
- ✅ All interactions except keyboard shortcuts
- ✅ Works on any webpage
- ✅ Pet stays on top of page content
- ✅ Settings popup for size/speed

### Desktop App (Electron)
- ✅ All interactions including keyboard shortcuts
- ✅ Always on top
- ✅ Cross-platform (Windows, macOS, Linux)
- ✅ Transparent window
- ✅ System tray integration

## Customization

All versions support:
- Multiple sprite sheets (one per animation)
- animations.json metadata with timing and triggers
- Custom event listeners via {{EVENT_LISTENERS}} placeholder
- Visual effects (hearts, Z symbols)
- Context menus with all available animations
