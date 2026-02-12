# Desktop Pet Generator

## Description
An interactive skill that generates customizable desktop pets from user-provided images. Converts static images into animated, interactive desktop companions with personality and behaviors.

## Trigger Words
- "desktop pet"
- "pet generator"
- "create pet"
- "animated mascot"
- "desktop companion"

## Overview
This skill helps users create desktop pets from their images through an interactive, guided conversation. It supports two generation modes (CSS-based and Sprite-based), includes a rich animation library, and exports to multiple deployment formats.

## Interactive Flow

### Step 1: Image Upload and Analysis
**Prompt:** "Please provide the image you'd like to turn into a desktop pet. You can upload an image file or provide a path."

**Actions:**
- Accepts image file (PNG, JPG, GIF, SVG)
- Runs `image_analyzer.py` to extract:
  - Dominant colors
  - Image dimensions
  - Transparency detection
  - Suggested features (eyes, limbs, etc.)

**Output:** "I've analyzed your image! It's a [description] with [dominant colors]. The image is [dimensions] and [has/doesn't have] transparency."

### Step 2: Mode Selection
**Prompt:** "Which generation mode would you like to use?

1. **CSS Mode** (Recommended for beginners)
   - Simpler implementation
   - Pure CSS animations
   - Lightweight (~50 lines)
   - Best for: Simple shapes, geometric designs

2. **Sprite Mode** (For detailed animations)
   - Frame-by-frame control
   - Supports complex movements
   - More customization options
   - Best for: Character art, detailed pets

Which mode works best for your project? (1 or 2)"

**User Input:** Mode selection (1 or 2)

### Step 3: Animation Selection
**Prompt:** "Great! Now let's choose animations. I have these preset animation categories:

**Core Animations** (Recommended):
- ✓ Idle (subtle breathing/bobbing)
- ✓ Walking (left/right movement)
- ✓ Jumping (bouncing effect)

**Work-Related**:
- Coding (typing animation)
- Thinking (question marks)
- Celebrating (confetti/sparkles)
- Error (shake/alert)

**Interactive**:
- Click Response (excited bounce)
- Drag Movement (smooth follow)
- Hover (scale/glow effect)

**Emotional**:
- Happy (bounce/smile)
- Sleepy (drooping/yawn)
- Excited (rapid movement)

Select animations by number or say 'default' for core animations:"

**User Input:** Animation selection

### Step 4: Interactivity Options
**Prompt:** "Do you want your pet to be interactive?

Available interactions:
1. **Clickable** - Pet responds to clicks (bounce, sound, animation)
2. **Draggable** - User can move pet around screen
3. **Hoverable** - Pet reacts to mouse hover
4. **Auto-roam** - Pet moves around screen automatically
5. **Status-aware** - Pet reacts to system events (work/break/complete)

Select options (comma-separated) or 'none' for static pet:"

**User Input:** Interaction types

### Step 5: Customization
**Prompt:** "Let's customize your pet's behavior:

1. **Size:** How large should your pet be? (e.g., 100px, 200px, 300px)
2. **Speed:** Animation speed? (slow/medium/fast or 1-10)
3. **Starting Position:** Where should it appear? (bottom-right/bottom-left/top-right/top-left/center)
4. **Personality:** (optional) Give your pet a name and personality trait!

You can skip this by saying 'default' or customize individual options:"

**User Input:** Customization preferences

### Step 6: Deployment Format
**Prompt:** "Almost done! How would you like to deploy your desktop pet?

1. **Standalone HTML** - Single file, open in browser
2. **Browser Extension** - Chrome/Firefox extension package
3. **Electron App** - Native desktop application
4. **Widget Code** - Embeddable code for existing websites

Select deployment format (1-4):"

**User Input:** Deployment choice

### Step 7: Generation and Output
**Actions:**
1. Run `pet_generator.py` with all collected parameters
2. Generate files based on selected format:
   - HTML/CSS/JS files
   - Asset files (images, sprites)
   - Configuration files
   - README with setup instructions

**Output:**
```
🎉 Your desktop pet is ready!

Generated files:
- [output_path]/index.html
- [output_path]/pet.css
- [output_path]/pet.js
- [output_path]/assets/
- [output_path]/README.md

Preview your pet:
1. Open index.html in a browser, or
2. Run: npm start (for Electron app)

Customization tips:
- Edit pet.css to adjust colors/size
- Modify pet.js for behavior changes
- See README.md for advanced options
```

## Configuration Options

### User-Configurable Parameters
```json
{
  "mode": "css|sprite",
  "image_path": "path/to/image.png",
  "size": "100px|200px|300px",
  "animations": ["idle", "walk", "jump", "click"],
  "interactions": ["clickable", "draggable", "hoverable"],
  "speed": "slow|medium|fast",
  "position": "bottom-right|bottom-left|top-right|top-left|center",
  "personality": {
    "name": "MyPet",
    "trait": "playful|calm|energetic|shy"
  },
  "deployment": "html|extension|electron|widget",
  "advanced": {
    "auto_roam": true,
    "status_aware": true,
    "sound_effects": false,
    "particle_effects": true
  }
}
```

### Preset Animation Library
Located in `scripts/animation_builder.py`:

**Idle Animations:**
- `float`: Gentle up/down hover
- `breathe`: Scale pulsing effect
- `sway`: Side-to-side movement

**Movement Animations:**
- `walk`: Horizontal walking
- `jump`: Vertical bounce
- `fly`: Floating movement
- `teleport`: Position snap

**Interactive Animations:**
- `onClick`: Excited bounce/spin
- `onHover`: Scale + glow
- `onDrag`: Smooth follow

**Emotional Animations:**
- `happy`: Rapid bounce
- `sad`: Droop down
- `excited`: Shake/wiggle
- `sleep`: Slow fade/droop

**Work Status Animations:**
- `coding`: Typing effect
- `thinking`: Question mark particles
- `complete`: Success celebration
- `error`: Alert shake

## Technical Architecture

### File Structure
```
desktop-pet-generator/
├── skill.md                 # This file
├── package.json            # Dependencies
├── scripts/
│   ├── image_analyzer.py   # Image feature extraction
│   ├── animation_builder.py # Animation presets & combination
│   ├── pet_generator.py    # Main generator orchestration
│   └── utils.py           # Helper functions
├── templates/
│   ├── css_mode/
│   │   ├── base.html
│   │   ├── styles.css
│   │   └── animations.js
│   ├── sprite_mode/
│   │   ├── base.html
│   │   ├── sprite.css
│   │   └── sprite_controller.js
│   ├── extension/
│   │   ├── manifest.json
│   │   └── content_script.js
│   └── electron/
│       ├── main.js
│       ├── preload.js
│       └── package.json
└── examples/
    ├── simple_pet/
    ├── interactive_pet/
    └── status_aware_pet/
```

### Python Dependencies
```
Pillow>=10.0.0          # Image processing
numpy>=1.24.0           # Color analysis
colorthief>=0.2.1      # Dominant color extraction
opencv-python>=4.8.0    # Advanced image analysis (optional)
```

### JavaScript Dependencies
```json
{
  "dependencies": {
    "electron": "^28.0.0",
    "express": "^4.18.2"
  },
  "devDependencies": {
    "webpack": "^5.89.0",
    "eslint": "^8.54.0"
  }
}
```

## Usage Examples

### Example 1: Simple CSS Pet
```
User: "Create a desktop pet from my logo"
Assistant: [Guides through flow]
User: [Uploads logo.png]
Assistant: "CSS mode recommended for your geometric logo"
User: "CSS mode, default animations, draggable"
Result: Simple draggable pet with idle animation
```

### Example 2: Advanced Sprite Pet
```
User: "I want an animated character that codes with me"
Assistant: [Guides through flow]
User: [Uploads character.png]
User: "Sprite mode, coding + thinking + complete animations"
User: "Make it status-aware and clickable"
Result: Character that animates based on work status
```

### Example 3: Browser Extension
```
User: "Create a pet browser extension"
Assistant: [Guides through flow]
User: [Uploads mascot.png]
User: "CSS mode, extension deployment"
Result: Packaged Chrome extension with pet
```

## Advanced Features

### Status-Aware Integration
When `status_aware: true`, the pet monitors:
- File save events → "complete" animation
- Long idle time → "sleepy" animation
- Rapid typing → "coding" animation
- Build errors → "error" animation

### Auto-Roaming Behavior
```javascript
// Generated in pet.js
const roamBehavior = {
  mode: 'random', // random, patrol, follow-mouse
  bounds: 'screen', // screen, window, custom
  speed: 2, // pixels per frame
  pauseInterval: 5000 // ms between movements
};
```

### Sound Effects (Optional)
```javascript
const sounds = {
  click: 'assets/sounds/pop.mp3',
  complete: 'assets/sounds/success.wav',
  error: 'assets/sounds/alert.mp3'
};
```

## Error Handling

### Invalid Image
"I couldn't process that image. Please provide a PNG, JPG, GIF, or SVG file with clear subject matter."

### Too Complex for CSS Mode
"Your image has intricate details that would work better in Sprite Mode. Would you like to switch?"

### Missing Dependencies
"I need to install some Python packages first. Running: pip install -r requirements.txt"

## Output Format

### Generated Project Structure
```
output/my-desktop-pet/
├── index.html          # Main entry point
├── pet.css            # Styling and animations
├── pet.js             # Behavior and interactions
├── config.json        # User preferences
├── assets/
│   ├── pet.png        # Original image
│   ├── sprite.png     # Sprite sheet (if sprite mode)
│   └── sounds/        # Sound effects (if enabled)
├── README.md          # Setup and customization guide
└── package.json       # For Electron/Extension builds
```

## Skill Metadata
- **Version:** 1.0.0
- **Author:** Desktop Pet Generator Team
- **Category:** Creative Tools, Development
- **Requires:** Python 3.8+, Node.js 18+ (for Electron)
- **Estimated Time:** 2-5 minutes per pet

## Notes for Claude
- Always validate image before proceeding
- Suggest mode based on image complexity
- Provide preview of generated pet if possible
- Include customization tips in final output
- Generate clean, commented code
- Create comprehensive README for users
