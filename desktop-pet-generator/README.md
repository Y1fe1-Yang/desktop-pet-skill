# Desktop Pet Generator Skill

Generate customizable desktop pets from images through an interactive, guided conversation.

## Quick Start

```bash
# Trigger in Claude Code
"Create a desktop pet from my image"
```

## Architecture

```
desktop-pet-generator/
├── skill.md                 # Complete skill description with interactive flow
├── scripts/
│   ├── image_analyzer.py    # Image analysis (colors, features, complexity)
│   ├── animation_builder.py # 15+ preset animations library
│   └── pet_generator.py     # Main orchestration script
├── templates/               # HTML templates for both modes
└── examples/                # Example configurations
```

## Features

- **Two Modes**: CSS (simple) or Sprite (frame-based)
- **15+ Animations**: Idle, movement, emotional, work-status, interactive
- **Interactions**: Click, drag, hover, auto-roam, status-aware
- **Deployments**: HTML, browser extension, Electron app, widget
- **Smart Analysis**: Auto-detects image features and suggests mode

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Via Skill (Recommended)
Claude guides you through:
1. Image upload
2. Mode selection
3. Animation choices
4. Interactions
5. Deployment format

### Command Line

```bash
# Analyze image
python scripts/image_analyzer.py image.png

# Generate pet
python scripts/pet_generator.py config.json
```

## Example Config

```json
{
  "mode": "css",
  "image_path": "pet.png",
  "size": "200px",
  "animations": ["float", "walk", "onClick"],
  "interactions": ["clickable", "draggable"],
  "deployment": "html",
  "output_dir": "./output"
}
```

## Output

Generated projects include:
- `index.html` - Main file
- `pet.css` - Styles + animations
- `pet.js` - Behaviors
- `config.json` - Settings
- `README.md` - Usage guide

## Documentation

See `/home/node/.claude/skills/desktop-pet-generator/skill.md` for:
- Complete interactive flow
- All animation options
- Customization guide
- Advanced features

## License

MIT
