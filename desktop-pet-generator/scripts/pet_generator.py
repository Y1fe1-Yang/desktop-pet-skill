#!/usr/bin/env python3
"""
Desktop Pet Generator - Main Orchestration Script
Converts a single user image into an animated desktop pet with multi-animation support
"""
import json
import os
import shutil
import sys
import argparse
import zipfile
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageChops
from typing import Dict, List, Tuple

# Animation presets and metadata
ANIMATION_PRESETS = {
    'core': ['idle', 'walk', 'jump'],
    'standard': ['idle', 'walk', 'jump', 'happy', 'pet', 'sleep', 'eat'],
    'complete': ['idle', 'walk', 'jump', 'happy', 'pet', 'sleep', 'eat', 'attack', 'hurt', 'death']
}

ANIMATION_CONFIGS = {
    'idle': {
        'frames': 8,
        'duration': 0.8,
        'trigger': 'auto',
        'description': 'Default idle breathing animation',
        'transform': 'breathe'
    },
    'walk': {
        'frames': 8,
        'duration': 0.6,
        'trigger': 'drag',
        'description': 'Walking cycle animation',
        'transform': 'walk_cycle'
    },
    'jump': {
        'frames': 6,
        'duration': 0.5,
        'trigger': 'click',
        'description': 'Jump/bounce animation',
        'transform': 'jump_arc'
    },
    'happy': {
        'frames': 8,
        'duration': 0.6,
        'trigger': 'pet',
        'description': 'Happy excited bounce',
        'transform': 'bounce_rotate'
    },
    'pet': {
        'frames': 6,
        'duration': 0.5,
        'trigger': 'hover',
        'description': 'Being petted reaction',
        'transform': 'gentle_sway'
    },
    'sleep': {
        'frames': 4,
        'duration': 1.2,
        'trigger': 'idle_timeout',
        'description': 'Sleeping/resting animation',
        'transform': 'sleep_fade'
    },
    'eat': {
        'frames': 8,
        'duration': 0.7,
        'trigger': 'food',
        'description': 'Eating animation',
        'transform': 'chew'
    },
    'attack': {
        'frames': 10,
        'duration': 0.8,
        'trigger': 'double_click',
        'description': 'Attack/pounce animation',
        'transform': 'pounce'
    },
    'hurt': {
        'frames': 4,
        'duration': 0.4,
        'trigger': 'shake',
        'description': 'Taking damage animation',
        'transform': 'shake'
    },
    'death': {
        'frames': 6,
        'duration': 1.0,
        'trigger': 'special',
        'description': 'Defeat/death animation',
        'transform': 'collapse'
    }
}

def create_sprite_sheet_for_animation(img: Image.Image, animation_type: str, size: Tuple[int, int]) -> Image.Image:
    """
    Generate a sprite sheet for a specific animation type
    Uses different transformations based on animation type
    """
    config = ANIMATION_CONFIGS.get(animation_type, ANIMATION_CONFIGS['idle'])
    frames = config['frames']
    transform = config['transform']

    # Create sprite sheet
    sprite_width = size[0] * frames
    sprite_height = size[1]
    sprite_sheet = Image.new('RGBA', (sprite_width, sprite_height), (0, 0, 0, 0))

    for i in range(frames):
        frame = img.copy()

        # Apply animation-specific transformations
        if transform == 'breathe':
            # Idle breathing: gentle scale pulsing
            progress = i / frames
            scale_factor = 1.0 + 0.1 * abs((progress - 0.5) * 2)
            new_size = (int(frame.width * scale_factor), int(frame.height * scale_factor))
            frame = frame.resize(new_size, Image.Resampling.LANCZOS)

        elif transform == 'walk_cycle':
            # Walking: alternating leg movement simulation
            progress = i / frames
            offset_y = int(5 * abs((progress - 0.5) * 2))
            rotation = -3 + (progress * 6)  # -3 to +3 degrees
            frame = frame.rotate(rotation, expand=False, fillcolor=(0, 0, 0, 0))

        elif transform == 'jump_arc':
            # Jumping: parabolic arc
            progress = i / frames
            height = -50 * (4 * progress * (1 - progress))  # Parabola
            offset_y = int(height)
            squash = 1.0 - 0.2 * abs(progress - 0.5)
            new_w = int(frame.width * squash)
            new_h = int(frame.height * (1.0 / squash))
            frame = frame.resize((new_w, new_h), Image.Resampling.LANCZOS)

        elif transform == 'bounce_rotate':
            # Happy bouncing with rotation
            progress = i / frames
            offset_y = -int(15 * abs((progress - 0.5) * 2))
            rotation = -10 + (progress * 20)  # -10 to +10 degrees
            frame = frame.rotate(rotation, expand=False, fillcolor=(0, 0, 0, 0))

        elif transform == 'gentle_sway':
            # Being petted: gentle side sway
            progress = i / frames
            rotation = 5 * ((progress - 0.5) * 2)  # -5 to +5 degrees
            frame = frame.rotate(rotation, expand=False, fillcolor=(0, 0, 0, 0))

        elif transform == 'sleep_fade':
            # Sleeping: rotate and fade
            progress = i / frames
            rotation = -30 * progress
            alpha = int(255 * (1.0 - 0.5 * progress))
            frame = frame.rotate(rotation, expand=False, fillcolor=(0, 0, 0, 0))
            # Apply alpha
            alpha_layer = Image.new('RGBA', frame.size, (255, 255, 255, alpha))
            frame = Image.composite(frame, Image.new('RGBA', frame.size, (0, 0, 0, 0)), alpha_layer)

        elif transform == 'chew':
            # Eating: up-down chewing motion
            progress = i / frames
            offset_y = int(8 * abs((progress - 0.5) * 2))
            scale = 1.0 + 0.15 * abs((progress - 0.5) * 2)
            new_w = int(frame.width * scale)
            new_h = int(frame.height / scale)
            frame = frame.resize((new_w, new_h), Image.Resampling.LANCZOS)

        elif transform == 'pounce':
            # Attack: fast forward motion with stretch
            progress = i / frames
            if progress < 0.3:
                # Wind up
                offset_x = -int(10 * progress / 0.3)
                rotation = -15 * progress / 0.3
            elif progress < 0.7:
                # Strike
                offset_x = int(30 * (progress - 0.3) / 0.4)
                rotation = 15 * (progress - 0.3) / 0.4
                scale_x = 1.3
                new_w = int(frame.width * scale_x)
                frame = frame.resize((new_w, frame.height), Image.Resampling.LANCZOS)
            else:
                # Recovery
                offset_x = 30 - int(30 * (progress - 0.7) / 0.3)
                rotation = 15 - 15 * (progress - 0.7) / 0.3
            frame = frame.rotate(rotation, expand=False, fillcolor=(0, 0, 0, 0))

        elif transform == 'shake':
            # Hurt: rapid shake
            progress = i / frames
            offset_x = int(10 * ((-1) ** i))
            rotation = 5 * ((-1) ** i)
            frame = frame.rotate(rotation, expand=False, fillcolor=(0, 0, 0, 0))

        elif transform == 'collapse':
            # Death: fall and fade
            progress = i / frames
            rotation = -90 * progress
            offset_y = int(30 * progress)
            alpha = int(255 * (1.0 - progress))
            frame = frame.rotate(rotation, expand=False, fillcolor=(0, 0, 0, 0))
            alpha_layer = Image.new('RGBA', frame.size, (255, 255, 255, alpha))
            frame = Image.composite(frame, Image.new('RGBA', frame.size, (0, 0, 0, 0)), alpha_layer)

        else:
            # Default: simple bounce
            progress = i / frames
            offset_y = -int(10 * abs((progress - 0.5) * 2))

        # Create canvas and paste frame
        canvas = Image.new('RGBA', size, (0, 0, 0, 0))
        x_offset = (size[0] - frame.width) // 2 + locals().get('offset_x', 0)
        y_offset = (size[1] - frame.height) // 2 + locals().get('offset_y', 0)

        # Ensure offsets are within bounds
        x_offset = max(0, min(x_offset, size[0] - frame.width))
        y_offset = max(0, min(y_offset, size[1] - frame.height))

        canvas.paste(frame, (x_offset, y_offset), frame)
        sprite_sheet.paste(canvas, (i * size[0], 0), canvas)

    return sprite_sheet

def create_sprite_sheet(image_path, output_path, frames=8, size=(64, 64)):
    """
    Legacy function for backward compatibility
    Generate a single sprite sheet with default idle animation
    """
    print(f"📸 Loading image: {image_path}")
    img = Image.open(image_path).convert("RGBA")
    img.thumbnail(size, Image.Resampling.LANCZOS)

    sprite_sheet = create_sprite_sheet_for_animation(img, 'idle', size)
    sprite_sheet.save(output_path)
    print(f"✅ Sprite sheet saved: {output_path}")

    return sprite_sheet.width, sprite_sheet.height

def create_multi_animation_sprites(image_path: str, output_dir: Path, animations: List[str], size: Tuple[int, int]) -> Dict:
    """
    Generate multiple sprite sheets for different animation types
    Returns metadata for all generated animations
    """
    print(f"📸 Loading image: {image_path}")
    img = Image.open(image_path).convert("RGBA")
    img.thumbnail(size, Image.Resampling.LANCZOS)

    animations_metadata = {}

    for animation_type in animations:
        if animation_type not in ANIMATION_CONFIGS:
            print(f"⚠️  Unknown animation type: {animation_type}, skipping...")
            continue

        config = ANIMATION_CONFIGS[animation_type]
        print(f"🎞️  Generating {animation_type} animation ({config['frames']} frames)...")

        sprite_sheet = create_sprite_sheet_for_animation(img, animation_type, size)
        sprite_filename = f"sprite_{animation_type}.png"
        sprite_path = output_dir / sprite_filename
        sprite_sheet.save(sprite_path)

        animations_metadata[animation_type] = {
            'sprite': sprite_filename,
            'frames': config['frames'],
            'duration': config['duration'],
            'trigger': config['trigger'],
            'description': config['description'],
            'width': sprite_sheet.width,
            'height': sprite_sheet.height,
            'frame_width': size[0],
            'frame_height': size[1]
        }

        print(f"✅ {animation_type}: {sprite_filename}")

    return animations_metadata

def generate_web_version(config, sprite_info, output_dir):
    """Generate standalone HTML version"""
    print("🌐 Generating web version...")

    template_path = Path(__file__).parent.parent / "templates" / "web" / "index.html"
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    # Replace placeholders
    html = template.replace('{{PET_NAME}}', config['name'])

    # Handle multi-animation or legacy mode
    if isinstance(sprite_info, dict) and 'animations' in sprite_info:
        # Multi-animation mode
        animations_json = json.dumps(sprite_info['animations'], ensure_ascii=False, indent=2)
        html = html.replace('{{ANIMATIONS_CONFIG}}', animations_json)

        # Use first animation's info for basic placeholders
        first_anim = list(sprite_info['animations'].values())[0]
        html = html.replace('{{SPRITE_WIDTH}}', str(first_anim['width']))
        html = html.replace('{{FRAME_WIDTH}}', str(first_anim['frame_width']))
        html = html.replace('{{FRAME_COUNT}}', str(first_anim['frames']))
    else:
        # Legacy single sprite mode
        html = html.replace('{{ANIMATIONS_CONFIG}}', 'null')
        html = html.replace('{{SPRITE_WIDTH}}', str(sprite_info['width']))
        html = html.replace('{{FRAME_WIDTH}}', str(sprite_info['frame_width']))
        html = html.replace('{{FRAME_COUNT}}', str(sprite_info['frames']))

    # Replace event listeners placeholder
    html = html.replace('{{EVENT_LISTENERS}}', '// Custom event listeners can be added here')

    output_file = output_dir / "index.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ Web version: {output_file}")

def create_extension_zip(ext_dir: Path, zip_path: Path):
    """
    Create a zip file of the browser extension directory
    """
    print(f"📦 Creating extension package...")

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Walk through the extension directory
        for root, dirs, files in os.walk(ext_dir):
            for file in files:
                file_path = Path(root) / file
                # Calculate the archive name (relative path from ext_dir)
                arcname = file_path.relative_to(ext_dir.parent)
                zipf.write(file_path, arcname)

    print(f"✅ Extension packaged: {zip_path}")

def generate_extension_version(config, sprite_info, output_dir):
    """Generate browser extension version"""
    print("🧩 Generating browser extension...")

    ext_dir = output_dir / "extension"
    ext_dir.mkdir(exist_ok=True)

    template_dir = Path(__file__).parent.parent / "templates" / "extension"

    # Copy and process manifest
    with open(template_dir / "manifest.json", 'r') as f:
        manifest = json.load(f)

    manifest['name'] = f"{config['name']} Desktop Pet"
    manifest['description'] = f"Your personal {config['name']} companion"

    with open(ext_dir / "manifest.json", 'w') as f:
        json.dump(manifest, f, indent=2)

    # Process and copy content script with placeholder replacement
    with open(template_dir / "content.js", 'r', encoding='utf-8') as f:
        content_js = f.read()

    content_js = content_js.replace('{{PET_NAME}}', config['name'])

    # Handle animations config
    if isinstance(sprite_info, dict) and 'animations' in sprite_info:
        animations_json = json.dumps(sprite_info['animations'], ensure_ascii=False, indent=2)
        content_js = content_js.replace('{{ANIMATIONS_CONFIG}}', animations_json)

        # Use first animation's info for basic placeholders
        first_anim = list(sprite_info['animations'].values())[0]
        content_js = content_js.replace('{{SPRITE_WIDTH}}', str(first_anim['width']))
        content_js = content_js.replace('{{FRAME_WIDTH}}', str(first_anim['frame_width']))
        content_js = content_js.replace('{{FRAME_COUNT}}', str(first_anim['frames']))
    else:
        content_js = content_js.replace('{{ANIMATIONS_CONFIG}}', 'null')
        content_js = content_js.replace('{{SPRITE_WIDTH}}', str(sprite_info['width']))
        content_js = content_js.replace('{{FRAME_WIDTH}}', str(sprite_info['frame_width']))
        content_js = content_js.replace('{{FRAME_COUNT}}', str(sprite_info['frames']))

    # Replace event listeners placeholder
    content_js = content_js.replace('{{EVENT_LISTENERS}}', '// Custom event listeners can be added here')

    with open(ext_dir / "content.js", 'w', encoding='utf-8') as f:
        f.write(content_js)

    shutil.copy(template_dir / "popup.html", ext_dir / "popup.html")
    shutil.copy(template_dir / "popup.js", ext_dir / "popup.js")

    # Copy sprite(s)
    if isinstance(sprite_info, dict) and 'animations' in sprite_info:
        # Multi-animation mode
        for anim_name, anim_data in sprite_info['animations'].items():
            sprite_file = output_dir / anim_data['sprite']
            if sprite_file.exists():
                shutil.copy(sprite_file, ext_dir / anim_data['sprite'])
        # Copy animations config
        if (output_dir / "animations.json").exists():
            shutil.copy(output_dir / "animations.json", ext_dir / "animations.json")
    else:
        # Legacy single sprite mode
        shutil.copy(output_dir / "sprite.png", ext_dir / "sprite.png")

    # Create zip file automatically
    zip_path = output_dir / "extension.zip"
    create_extension_zip(ext_dir, zip_path)

    print(f"✅ Extension: {ext_dir}")
    print(f"✅ Package: {zip_path}")

def package_desktop_app(desktop_dir: Path, config: dict) -> bool:
    """
    Automatically package the desktop app using electron-builder
    Returns True if packaging succeeded, False otherwise
    """
    print(f"\n📦 Packaging desktop app...")
    print(f"{'='*50}")

    try:
        # Check if npm is available
        npm_check = subprocess.run(['npm', '--version'],
                                   capture_output=True,
                                   text=True,
                                   timeout=10)
        if npm_check.returncode != 0:
            print("⚠️  npm not found. Skipping automatic packaging.")
            print("   Install Node.js to enable automatic packaging.")
            return False

        print(f"📥 Installing dependencies...")
        install_result = subprocess.run(
            ['npm', 'install'],
            cwd=desktop_dir,
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes timeout
        )

        if install_result.returncode != 0:
            print(f"⚠️  npm install failed:")
            print(install_result.stderr)
            return False

        print(f"✅ Dependencies installed")

        # Build portable version (cross-platform)
        print(f"🔨 Building portable executable...")
        build_result = subprocess.run(
            ['npm', 'run', 'build'],
            cwd=desktop_dir,
            capture_output=True,
            text=True,
            timeout=600  # 10 minutes timeout
        )

        if build_result.returncode != 0:
            print(f"⚠️  Build failed:")
            print(build_result.stderr)
            return False

        # Check for generated files
        dist_dir = desktop_dir / "dist"
        if not dist_dir.exists():
            print(f"⚠️  dist directory not found after build")
            return False

        # List generated files
        built_files = list(dist_dir.glob("*"))
        if built_files:
            print(f"✅ Desktop app packaged successfully!")
            print(f"\n📂 Packaged files in {dist_dir}:")
            for file in built_files:
                size = file.stat().st_size if file.is_file() else "dir"
                size_str = f"{size:,} bytes" if isinstance(size, int) else size
                print(f"   • {file.name} ({size_str})")
            return True
        else:
            print(f"⚠️  No files generated in dist directory")
            return False

    except subprocess.TimeoutExpired:
        print(f"⚠️  Packaging timed out")
        return False
    except FileNotFoundError:
        print(f"⚠️  npm not found. Skipping automatic packaging.")
        print(f"   Install Node.js to enable automatic packaging.")
        return False
    except Exception as e:
        print(f"⚠️  Packaging error: {e}")
        return False

def generate_desktop_version(config, sprite_info, output_dir, auto_package=True):
    """Generate Electron desktop app version"""
    print("🖥️  Generating desktop app...")

    desktop_dir = output_dir / "desktop-app"
    desktop_dir.mkdir(exist_ok=True)

    template_dir = Path(__file__).parent.parent / "templates" / "desktop"

    # Copy Electron files (except renderer.js and index.html which need processing)
    for file in ['main.js', 'package.json']:
        src = template_dir / file
        if src.exists():
            shutil.copy(src, desktop_dir / file)

    # Process renderer.js with placeholder replacement
    with open(template_dir / 'renderer.js', 'r', encoding='utf-8') as f:
        renderer_js = f.read()

    renderer_js = renderer_js.replace('{{PET_NAME}}', config['name'])

    if isinstance(sprite_info, dict) and 'animations' in sprite_info:
        animations_json = json.dumps(sprite_info['animations'], ensure_ascii=False, indent=2)
        renderer_js = renderer_js.replace('{{ANIMATIONS_CONFIG}}', animations_json)

        first_anim = list(sprite_info['animations'].values())[0]
        renderer_js = renderer_js.replace('{{SPRITE_WIDTH}}', str(first_anim['width']))
        renderer_js = renderer_js.replace('{{FRAME_WIDTH}}', str(first_anim['frame_width']))
        renderer_js = renderer_js.replace('{{FRAME_COUNT}}', str(first_anim['frames']))
    else:
        renderer_js = renderer_js.replace('{{ANIMATIONS_CONFIG}}', 'null')
        renderer_js = renderer_js.replace('{{SPRITE_WIDTH}}', str(sprite_info['width']))
        renderer_js = renderer_js.replace('{{FRAME_WIDTH}}', str(sprite_info['frame_width']))
        renderer_js = renderer_js.replace('{{FRAME_COUNT}}', str(sprite_info['frames']))

    renderer_js = renderer_js.replace('{{EVENT_LISTENERS}}', '// Custom event listeners can be added here')

    with open(desktop_dir / 'renderer.js', 'w', encoding='utf-8') as f:
        f.write(renderer_js)

    # Process index.html if needed
    if (template_dir / 'index.html').exists():
        shutil.copy(template_dir / 'index.html', desktop_dir / 'index.html')

    # Update package.json with pet name
    pkg_path = desktop_dir / "package.json"
    with open(pkg_path, 'r') as f:
        pkg = json.load(f)

    pkg['name'] = config['name'].lower().replace(' ', '-')
    pkg['productName'] = f"{config['name']} Pet"

    with open(pkg_path, 'w') as f:
        json.dump(pkg, f, indent=2)

    # Copy sprite(s)
    if isinstance(sprite_info, dict) and 'animations' in sprite_info:
        # Multi-animation mode
        for anim_name, anim_data in sprite_info['animations'].items():
            sprite_file = output_dir / anim_data['sprite']
            if sprite_file.exists():
                shutil.copy(sprite_file, desktop_dir / anim_data['sprite'])
        # Copy animations config
        if (output_dir / "animations.json").exists():
            shutil.copy(output_dir / "animations.json", desktop_dir / "animations.json")
    else:
        # Legacy single sprite mode
        shutil.copy(output_dir / "sprite.png", desktop_dir / "sprite.png")

    print(f"✅ Desktop app: {desktop_dir}")

    # Automatically package if enabled
    if auto_package:
        package_success = package_desktop_app(desktop_dir, config)
        if not package_success:
            print("   📦 Manual build: cd desktop-app && npm install && npm run build")
    else:
        print("   📦 Build: cd desktop-app && npm install && npm run build")

def generate_readme(config, output_dir, has_multi_animations=False):
    """Generate README with instructions"""
    animations_section = ""
    if has_multi_animations:
        animations_section = f"""
## 🎬 Animations Included

This pet includes multiple animations:
- Check `animations.json` for complete animation metadata
- Each animation has its own sprite sheet (sprite_*.png)
- Animations are automatically triggered based on user interactions

"""

    readme_content = f"""# {config['name']} Desktop Pet

Your personal {config['name']} companion, generated by Desktop Pet Generator!

## 🎨 What's Included

- **Web Version** (`index.html`) - Open directly in browser
- **Browser Extension** (`extension/`) - Install in Chrome/Firefox
- **Desktop App** (`desktop-app/`) - Native Electron application
{animations_section}
## 🚀 Quick Start

### Web Version (Easiest)
```bash
# Just open the file
open index.html
```

### Browser Extension
```bash
# Package the extension
cd extension
zip -r ../extension.zip .

# Install:
# Chrome: chrome://extensions → Load unpacked → Select extension/
# Firefox: about:debugging → Load Temporary Add-on
```

### Desktop App
```bash
# The desktop app is automatically packaged during generation!
# Look for pre-built executables in desktop-app/dist/

# Or run from source:
cd desktop-app
npm install
npm start

# Manual rebuild (if needed):
npm run build
```

## 🎮 Features

- ✅ Sprite-based animations
- ✅ Draggable pet
- ✅ Click interactions
- ✅ Hover effects
- ✅ Always on top (desktop app)
- ✅ Cross-platform support
{"- ✅ Multiple animation states" if has_multi_animations else ""}

## 📝 Customization

Edit the sprite sheet(s) to change your pet's appearance.
Adjust animation speed and triggers in the HTML/JS files.
{"Modify animations.json to customize animation behavior." if has_multi_animations else ""}

## 🔧 Built With

- Desktop Pet Generator Skill
- Sprite Sheet Animation
- Pure HTML/CSS/JavaScript
- Electron (for desktop version)

---

Made with ❤️ by Desktop Pet Generator
"""

    with open(output_dir / "README.md", 'w', encoding='utf-8') as f:
        f.write(readme_content)

    print(f"✅ README.md created")

def main():
    parser = argparse.ArgumentParser(
        description='Desktop Pet Generator - Create animated desktop pets with multiple animations',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage with default animations
  python pet_generator.py --image bear.png --name "小熊"

  # Use preset animation sets
  python pet_generator.py --image cat.png --name "猫咪" --animations core
  python pet_generator.py --image dog.png --name "小狗" --animations standard
  python pet_generator.py --image bird.png --name "小鸟" --animations complete

  # Custom animation combination
  python pet_generator.py --image bear.png --name "小熊" \\
    --animations idle,walk,jump,happy,pet --output ./my-pet

Animation presets:
  core     : idle, walk, jump (3 animations)
  standard : idle, walk, jump, happy, pet, sleep, eat (7 animations)
  complete : All 10 animations

Available animations:
  idle, walk, jump, happy, pet, sleep, eat, attack, hurt, death
        """
    )
    parser.add_argument('--image', required=True, help='Path to input image')
    parser.add_argument('--name', default='My Pet', help='Pet name')
    parser.add_argument('--output', default='./output', help='Output directory')
    parser.add_argument('--animations', default=None,
                        help='Animation types: comma-separated list or preset (core/standard/complete)')
    parser.add_argument('--frames', type=int, default=8, help='Number of animation frames (legacy mode only)')
    parser.add_argument('--size', type=int, default=64, help='Frame size (pixels)')
    parser.add_argument('--modes', default='web,extension,desktop', help='Generation modes (comma-separated)')
    parser.add_argument('--no-package', action='store_true',
                        help='Skip automatic packaging of desktop app (default: auto-package enabled)')

    args = parser.parse_args()

    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n🎨 Desktop Pet Generator v2.0")
    print(f"{'='*50}")
    print(f"Image: {args.image}")
    print(f"Name: {args.name}")
    print(f"Output: {output_dir}")

    # Configuration
    config = {
        'name': args.name,
        'image': args.image,
        'size': (args.size, args.size)
    }

    # Determine animation mode
    use_multi_animations = args.animations is not None

    if use_multi_animations:
        # Parse animations argument
        if args.animations.lower() in ANIMATION_PRESETS:
            animations = ANIMATION_PRESETS[args.animations.lower()]
            print(f"Animations: {args.animations} preset ({len(animations)} animations)")
        else:
            animations = [a.strip() for a in args.animations.split(',')]
            print(f"Animations: Custom ({len(animations)} animations)")

        print(f"  → {', '.join(animations)}")
        print(f"{'='*50}\n")

        # Generate multi-animation sprites
        animations_metadata = create_multi_animation_sprites(
            args.image,
            output_dir,
            animations,
            config['size']
        )

        # Save animations.json
        animations_config = {
            'pet_name': config['name'],
            'version': '2.0',
            'animations': animations_metadata,
            'default_animation': animations[0] if animations else 'idle'
        }

        with open(output_dir / "animations.json", 'w', encoding='utf-8') as f:
            json.dump(animations_config, f, indent=2, ensure_ascii=False)

        print(f"\n✅ animations.json created with {len(animations_metadata)} animations")

        sprite_info = animations_config

    else:
        # Legacy single sprite mode
        print(f"Mode: Legacy (single sprite)")
        print(f"Frames: {args.frames}")
        print(f"{'='*50}\n")

        config['frames'] = args.frames

        sprite_path = output_dir / "sprite.png"
        width, height = create_sprite_sheet(
            args.image,
            sprite_path,
            frames=args.frames,
            size=config['size']
        )

        sprite_info = {
            'width': width,
            'height': height,
            'frames': args.frames,
            'frame_width': args.size
        }

    # Generate versions based on modes
    modes = [m.strip() for m in args.modes.split(',')]
    auto_package = not args.no_package

    if 'web' in modes:
        generate_web_version(config, sprite_info, output_dir)

    if 'extension' in modes:
        generate_extension_version(config, sprite_info, output_dir)

    if 'desktop' in modes:
        generate_desktop_version(config, sprite_info, output_dir, auto_package=auto_package)

    # Generate README
    generate_readme(config, output_dir, has_multi_animations=use_multi_animations)

    print(f"\n{'='*50}")
    print(f"✨ Generation complete!")
    print(f"{'='*50}")
    print(f"📁 Output directory: {output_dir}")
    if use_multi_animations:
        print(f"🎬 Generated {len(animations_metadata)} animations")
        print(f"📋 Check animations.json for animation metadata")
    print(f"\n🎉 Your {config['name']} pet is ready to use!")

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Desktop Pet Generator v2.0")
        print("=" * 60)
        print("\nUsage:")
        print("  python pet_generator.py --image <path> [options]")
        print("\nRequired:")
        print("  --image PATH        Input image file")
        print("\nOptions:")
        print("  --name NAME         Pet name (default: My Pet)")
        print("  --output DIR        Output directory (default: ./output)")
        print("  --animations SET    Animation preset or custom list")
        print("                      Presets: core, standard, complete")
        print("                      Custom: idle,walk,jump,happy,pet")
        print("  --size N            Frame size in pixels (default: 64)")
        print("  --modes MODES       Output modes (default: web,extension,desktop)")
        print("  --no-package        Skip automatic packaging (default: auto-package enabled)")
        print("  --frames N          [Legacy] Animation frames (default: 8)")
        print("\nAnimation Presets:")
        print("  core       → idle, walk, jump (3 animations)")
        print("  standard   → idle, walk, jump, happy, pet, sleep, eat (7)")
        print("  complete   → All 10 animations")
        print("\nAvailable Animations:")
        print("  idle      - Default breathing animation")
        print("  walk      - Walking cycle")
        print("  jump      - Jump/bounce")
        print("  happy     - Excited bounce")
        print("  pet       - Being petted")
        print("  sleep     - Sleeping/resting")
        print("  eat       - Eating animation")
        print("  attack    - Attack/pounce")
        print("  hurt      - Taking damage")
        print("  death     - Defeat animation")
        print("\nExamples:")
        print("  # Default single animation (legacy mode)")
        print("  python pet_generator.py --image bear.png --name '小熊'")
        print("\n  # Core animations preset")
        print("  python pet_generator.py --image cat.png --name '猫咪' --animations core")
        print("\n  # Custom animation selection")
        print("  python pet_generator.py --image dog.png --name '小狗' \\")
        print("    --animations idle,walk,jump,happy,pet --output ./my-pet")
        print("\n  # Complete animation set")
        print("  python pet_generator.py --image bird.png --name '小鸟' --animations complete")
        print("\n" + "=" * 60)
        sys.exit(0)

    main()
