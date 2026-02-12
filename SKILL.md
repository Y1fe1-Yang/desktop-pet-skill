---
name: desktop-pet
description: One-command animated desktop pet generator. Converts any image into an interactive desktop pet with multiple animations (idle, walk, jump, happy, pet, sleep, etc.) and automatic preview. Use when user wants to create a desktop pet, animated character, screen companion, or mentions "desktop pet", "桌宠", "screen pet", "create pet from image", or uploads an image asking for a pet/companion. Generates web, extension, and desktop versions with drag interactions, click animations, and visual effects.
---

# Desktop Pet Generator

Convert any image into an animated desktop pet with one command. Automatically generates sprite animations, interactive behaviors, and preview.

## Quick Start

Minimal usage - just provide an image:

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

## Usage Patterns

### Pattern 1: Minimal (Image Only)
User provides image, everything else auto-generated:

```bash
python3 scripts/create_pet.py cat.png
```

### Pattern 2: Custom Name
```bash
python3 scripts/create_pet.py dog.png --name "小狗"
```

### Pattern 3: Custom Animations
```bash
python3 scripts/create_pet.py bear.png --name "Bear" --animations complete
```

### Pattern 4: Full Control
```bash
python3 scripts/create_pet.py image.png --name "My Pet" --animations core --output ./my-pet
```

## Animation Presets

- **core**: 3 animations (idle, walk, jump) - Fast generation
- **standard**: 7 animations (adds happy, pet, sleep, eat) - **RECOMMENDED**
- **complete**: 10 animations (adds attack, hurt, death) - Maximum variety

For detailed animation information, see [references/animations.md](references/animations.md).

## Script Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `image` | *required* | Path to pet image |
| `--name` | Auto-generated | Pet display name |
| `--animations` | `standard` | Preset or custom list |
| `--output` | `./outputs/<name>` | Output directory |

## Output Structure

```
outputs/<pet-name>/
├── index.html              # Web version (open directly)
├── sprite_*.png            # Animation sprite sheets
├── animations.json         # Animation metadata
├── README.md              # Usage instructions
├── extension/             # Browser extension (source)
│   ├── manifest.json
│   ├── content.js
│   └── sprite_*.png
├── extension.zip          # Browser extension (packaged - ready to install)
└── desktop-app/           # Electron app
    ├── main.js
    ├── renderer.js
    ├── package.json
    ├── sprite_*.png
    └── dist/              # Packaged executables (if npm available)
        ├── *.exe          # Windows installer
        ├── *.dmg          # macOS installer
        └── *.AppImage     # Linux executable
```

## Interaction Features

Generated pets support:
- **Drag**: Triggers walk animation
- **Click**: Jump animation
- **Double-click**: Happy animation
- **Long-press** (2s): Pet animation with floating hearts
- **Right-click**: Context menu with all animations
- **Idle** (5s): Returns to idle breathing
- **Idle** (60s): Sleep animation with Z symbols
- **Keyboard** (1-9, Space): Desktop version only

## Workflow

When user requests a desktop pet:

1. Identify the image path from user message or attachments
2. Extract any custom name from user request
3. Determine animation preset (default: standard)
4. Run `scripts/create_pet.py` with appropriate parameters
5. Report the preview URL to user
6. Explain key interactions (drag, click, long-press, right-click)

## Automatic Packaging

The script automatically packages ready-to-install versions:

### Browser Extension
- Automatically creates `extension.zip` file
- Ready to install: Load unpacked in Chrome/Firefox
- Contains all required files (manifest.json, content.js, sprites)
- No manual zipping required

### Desktop App (Electron)
- Automatically runs `npm install` and `electron-builder` if npm is available
- Generates platform-specific executables in `desktop-app/dist/`:
  - Windows: `.exe` installer
  - macOS: `.dmg` installer
  - Linux: `.AppImage` executable
- Falls back to source files if npm is not available
- Build time: ~2-3 minutes (one-time per pet)

## Implementation Notes

- The script automatically starts an HTTP server on port 8080
- Port export is handled automatically if `/app/export-port.sh` exists
- Preview URL is returned in the script output
- All three versions (web, extension, desktop) are generated simultaneously
- Generation time: ~5 seconds for standard preset (plus packaging time for desktop if npm available)

## Dependencies

Requires the `desktop-pet-generator` skill to be installed alongside this skill. The underlying `pet_generator.py` is located at:

```
~/.claude/skills/desktop-pet-generator/scripts/pet_generator.py
```

## Example Interactions

**User**: "Help me make a desktop pet from this cat image"
**Claude**:
1. Saves/identifies the image path
2. Runs: `python3 scripts/create_pet.py cat.png`
3. Reports: "Created 'Cat' desktop pet with 7 animations. Preview: https://..."
4. Explains: "Drag to move, click to jump, long-press for hearts!"

**User**: "Create a bear pet called 小熊 with all animations"
**Claude**:
1. Runs: `python3 scripts/create_pet.py bear.png --name "小熊" --animations complete`
2. Reports: "Created '小熊' with 10 animations. Preview: https://..."
