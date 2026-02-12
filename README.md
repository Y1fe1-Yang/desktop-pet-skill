# Desktop Pet Generator

> Convert any image into an interactive animated desktop pet with one command

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)
![Node](https://img.shields.io/badge/node-24.x-green.svg)

A Claude Code skill that transforms any image into an animated desktop pet with multiple animations, interactive behaviors, and automatic packaging for web, browser extension, and desktop platforms.

## Features

- **One-Command Generation**: Convert any image to a desktop pet instantly
- **10 Built-in Animations**: idle, walk, jump, happy, pet, sleep, eat, attack, hurt, death
- **Multi-Platform Output**: Web (HTML), Browser Extension (ZIP), Desktop App (Electron)
- **Auto-Packaging**: Automatic `.zip` for extensions, `.exe`/`.dmg`/`.AppImage` for desktop
- **Interactive Behaviors**: Drag, click, long-press, right-click interactions
- **Visual Effects**: Floating hearts, sleep bubbles, particle effects
- **Auto-Preview**: Built-in HTTP server with instant preview

## Quick Start

### Installation

1. Clone this repository to your Claude skills directory:

```bash
cd ~/.claude/skills
git clone https://github.com/Y1fe1-Yang/desktop-pet-skill.git desktop-pet
```

2. The skill requires Python 3.11+ and optionally Node.js 24.x for desktop app packaging.

### Usage

Create a desktop pet from any image:

```bash
python3 scripts/create_pet.py /path/to/image.png
```

This automatically:
- Analyzes the image
- Generates appropriate pet name
- Creates 7 animations (standard preset)
- Builds web, extension, and desktop versions
- Starts preview server
- Returns preview URL

## Examples

### Basic Usage
```bash
# Minimal - auto-generates everything
python3 scripts/create_pet.py cat.png

# Custom name
python3 scripts/create_pet.py dog.png --name "小狗"

# Custom animations
python3 scripts/create_pet.py bear.png --animations complete

# Full control
python3 scripts/create_pet.py image.png --name "My Pet" --animations core --output ./my-pet
```

### Animation Presets

- **core**: 3 animations (idle, walk, jump) - Fast generation
- **standard**: 7 animations (adds happy, pet, sleep, eat) - Recommended
- **complete**: 10 animations (adds attack, hurt, death) - Maximum variety

## Output Structure

```
outputs/<pet-name>/
├── index.html              # Web version (open directly)
├── sprite_*.png            # Animation sprite sheets
├── animations.json         # Animation metadata
├── README.md              # Usage instructions
├── extension.zip          # Browser extension (ready to install)
├── extension/             # Browser extension source
│   ├── manifest.json
│   ├── content.js
│   └── sprite_*.png
└── desktop-app/           # Electron desktop app
    ├── main.js
    ├── renderer.js
    ├── package.json
    ├── sprite_*.png
    └── dist/              # Packaged executables
        ├── *.exe          # Windows
        ├── *.dmg          # macOS
        └── *.AppImage     # Linux
```

## Interactive Features

Generated pets support:
- **Drag**: Move pet around screen (triggers walk animation)
- **Click**: Jump animation
- **Double-click**: Happy animation with bounce
- **Long-press** (2s): Pet animation with floating hearts
- **Right-click**: Context menu with all animations
- **Auto-idle** (5s): Returns to idle breathing
- **Auto-sleep** (60s): Sleep animation with Z symbols
- **Keyboard** (1-9, Space): Desktop version only

## Automatic Packaging

### Browser Extension
- Automatically creates `extension.zip` file
- Ready to install: Chrome > Extensions > Load unpacked
- Contains all required files (manifest.json, content.js, sprites)
- No manual zipping required

### Desktop App (Electron)
- Automatically runs `npm install` and `electron-builder` (if npm available)
- Generates platform-specific executables in `desktop-app/dist/`:
  - **Windows**: `.exe` installer
  - **macOS**: `.dmg` installer
  - **Linux**: `.AppImage` executable
- Falls back to source files if npm is not available
- Build time: ~2-3 minutes (one-time per pet)

## Documentation

- [SKILL.md](SKILL.md) - Claude Code skill specification
- [desktop-pet-generator/](desktop-pet-generator/) - Core generator implementation
- [references/animations.md](references/animations.md) - Detailed animation documentation

## Technical Details

### Architecture
- **Image Analysis**: PIL-based image processing and analysis
- **Animation Generation**: Procedural sprite sheet generation
- **Web Version**: Standalone HTML with embedded JavaScript
- **Browser Extension**: Chrome/Firefox compatible manifest v3
- **Desktop App**: Electron-based with keyboard shortcuts

### Dependencies
- Python 3.11+
- PIL/Pillow (image processing)
- Node.js 24.x (optional, for desktop app packaging)
- electron-builder (auto-installed if npm available)

### Performance
- Generation time: ~5 seconds for standard preset
- Desktop packaging: ~2-3 minutes (one-time per pet)
- Preview server: Port 8080 (auto-export if available)

## Use Cases

- Personal desktop companions
- Screen pets for streaming
- Interactive mascots
- Animated avatars
- Educational demonstrations
- Fun gifts and memes

## Examples Gallery

Create pets from:
- Photos (cat, dog, hamster, etc.)
- Cartoon characters
- Game sprites
- Profile pictures
- Logos and mascots
- Meme images

## Claude Code Integration

This skill is designed for Claude Code and provides:
- Automatic skill detection via SKILL.md
- Conversational pet generation
- Smart parameter inference
- Auto-preview and sharing
- Multi-language support (English, 中文)

When using with Claude Code, simply say:
- "Create a desktop pet from this image"
- "Make a cat pet called 小猫 with all animations"
- "Generate a screen companion from my avatar"

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details

## Author

Created by Y1fe1-Yang

## Acknowledgments

- Built for Claude Code
- Inspired by classic desktop pets
- Powered by Python, Electron, and AI

---

**Note**: This is a Claude Code skill. For standalone usage, see the desktop-pet-generator directory.
