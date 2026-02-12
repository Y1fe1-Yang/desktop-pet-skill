#!/usr/bin/env python3
"""
Smart Desktop Pet Creator - One-command pet generation
Analyzes image, infers parameters, generates complete pet system, and starts preview
"""
import sys
import os
import argparse
import subprocess
import json
from pathlib import Path
import tempfile

def analyze_image_with_ai(image_path: str) -> dict:
    """
    Use AI to analyze the image and extract pet characteristics
    Returns: {animal_type, suggested_name, style, recommended_preset}
    """
    # For now, return sensible defaults
    # In a real implementation, this would use vision AI
    return {
        'animal_type': 'Pet',
        'suggested_name': Path(image_path).stem.replace('_', ' ').replace('-', ' ').title(),
        'style': 'pixel-art',
        'recommended_preset': 'standard'
    }

def generate_pet(image_path: str, name: str = None, animations: str = None, output_dir: str = None):
    """Generate desktop pet with smart defaults"""

    # Analyze image if no name provided
    if not name:
        analysis = analyze_image_with_ai(image_path)
        name = analysis['suggested_name']
        print(f"🔍 Detected: {analysis['animal_type']}")
        print(f"✨ Generated name: {name}")

        if not animations:
            animations = analysis['recommended_preset']
            print(f"🎬 Using {animations} animation preset")

    # Set default animations if not specified
    if not animations:
        animations = 'standard'

    # Set default output directory if not specified
    if not output_dir:
        output_dir = Path.cwd() / "outputs" / name.lower().replace(' ', '-')

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Get the pet_generator.py path
    pet_gen_path = Path(__file__).parent.parent.parent / "desktop-pet-generator" / "scripts" / "pet_generator.py"

    if not pet_gen_path.exists():
        print(f"❌ Error: pet_generator.py not found at {pet_gen_path}")
        sys.exit(1)

    # Run pet generator
    print(f"\n🎨 Generating desktop pet...")
    print(f"   Name: {name}")
    print(f"   Animations: {animations}")
    print(f"   Output: {output_dir}")

    cmd = [
        'python3',
        str(pet_gen_path),
        '--image', image_path,
        '--name', name,
        '--animations', animations,
        '--output', str(output_dir)
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"❌ Generation failed:")
        print(result.stderr)
        sys.exit(1)

    print(result.stdout)

    # Start preview server
    print(f"\n🌐 Starting preview server...")

    # Check if server is already running on port 8080
    check_port = subprocess.run(['lsof', '-i', ':8080'], capture_output=True)

    if check_port.returncode == 0:
        print("⚠️  Server already running on port 8080")
        port = 8080
    else:
        # Start HTTP server in background
        os.chdir(output_dir)
        server_process = subprocess.Popen(
            ['python3', '-m', 'http.server', '8080'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        port = 8080
        print(f"✅ Server started on port {port}")

    # Export port
    export_script = Path('/app/export-port.sh')
    if export_script.exists():
        result = subprocess.run([str(export_script), str(port)], capture_output=True, text=True)
        if result.returncode == 0:
            preview_url = result.stdout.strip()
            print(f"\n✨ Desktop pet generated successfully!")
            print(f"📁 Location: {output_dir}")
            print(f"🔗 Preview: {preview_url}")
            print(f"\n🎮 Interactions:")
            print(f"   • Drag to move (triggers walk animation)")
            print(f"   • Click to jump")
            print(f"   • Double-click for happy animation")
            print(f"   • Long-press for pet animation with hearts")
            print(f"   • Right-click for menu")

            return {
                'success': True,
                'output_dir': str(output_dir),
                'preview_url': preview_url,
                'name': name,
                'animations': animations
            }

    print(f"\n✨ Desktop pet generated successfully!")
    print(f"📁 Location: {output_dir}")
    print(f"💡 Open {output_dir}/index.html in your browser")

    return {
        'success': True,
        'output_dir': str(output_dir),
        'name': name,
        'animations': animations
    }

def main():
    parser = argparse.ArgumentParser(
        description='Smart Desktop Pet Creator - One-command generation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Minimal - just provide image
  python create_pet.py /path/to/cat.png

  # With custom name
  python create_pet.py /path/to/dog.png --name "小狗"

  # With custom animations
  python create_pet.py /path/to/bear.png --name "Bear" --animations complete

  # Full customization
  python create_pet.py /path/to/image.png --name "My Pet" --animations core --output ./my-pet
        """
    )

    parser.add_argument('image', help='Path to pet image')
    parser.add_argument('--name', help='Pet name (auto-generated if not provided)')
    parser.add_argument('--animations', help='Animation preset: core/standard/complete (default: standard)')
    parser.add_argument('--output', help='Output directory (default: ./outputs/<pet-name>)')

    args = parser.parse_args()

    # Validate image exists
    if not Path(args.image).exists():
        print(f"❌ Error: Image not found: {args.image}")
        sys.exit(1)

    # Generate pet
    result = generate_pet(
        image_path=args.image,
        name=args.name,
        animations=args.animations,
        output_dir=args.output
    )

    # Output result as JSON for programmatic use
    if result:
        with open(Path(result['output_dir']) / 'generation_info.json', 'w') as f:
            json.dump(result, f, indent=2)

if __name__ == '__main__':
    main()
