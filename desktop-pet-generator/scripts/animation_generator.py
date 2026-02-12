#!/usr/bin/env python3
"""
AI Animation Generator for Desktop Pet
Generates unique animation frames for different interaction types using AI image generation
"""
import json
import os
import sys
import subprocess
import time
from pathlib import Path
from PIL import Image

# Animation type definitions with descriptions for AI generation
ANIMATION_TYPES = {
    'idle': '静止待机状态，轻微呼吸动作，平静的表情，像素艺术风格',
    'walk': '行走动作，腿部交替移动，身体轻微上下摆动，像素艺术风格',
    'jump': '跳跃动作序列，从蹲下准备到跃起到落地，动态姿态，像素艺术风格',
    'happy': '开心表情，欢快的姿态，可能有爱心或星星特效，明亮的颜色，像素艺术风格',
    'pet': '被抚摸的享受表情，闭眼微笑，放松的身体姿态，舒适感，像素艺术风格',
    'sleep': '睡觉姿态，闭眼，平躺或蜷缩，Z字符号漂浮，平静，像素艺术风格',
    'eat': '吃东西动作，张嘴咀嚼，享受食物的表情，可能有食物道具，像素艺术风格',
    'celebrate': '庆祝动作，举手欢呼，跳跃，欢快的表情，可能有彩带或烟花，像素艺术风格',
    'shake': '摇晃或抖动身体，快速左右摆动，可能是抖落水珠或表达情绪，像素艺术风格',
    'bounce': '弹跳动作，有弹性的上下运动，轻快的节奏，像素艺术风格',
    'sad': '伤心表情，低头，可能有眼泪，失落的肢体语言，像素艺术风格',
    'angry': '生气表情，皱眉，可能有火焰或愤怒符号，紧张的姿态，像素艺术风格',
    'wave': '挥手问候，手臂上下或左右摆动，友好的表情，像素艺术风格',
    'dance': '跳舞动作，节奏感的身体摆动，欢快的氛围，音符符号，像素艺术风格',
    'stretch': '伸展动作，伸懒腰，拉伸身体，放松的表情，像素艺术风格',
    'spin': '旋转动作，360度转身，动感的姿态，像素艺术风格',
    'surprise': '惊讶表情，张大嘴巴，瞪大眼睛，可能有感叹号，像素艺术风格',
    'think': '思考姿态，手托腮，可能有问号或思考泡泡，专注的表情，像素艺术风格',
    'run': '奔跑动作，快速的腿部移动，身体前倾，速度线，像素艺术风格',
    'fly': '飞行动作，张开翅膀或手臂，漂浮感，云朵或天空背景，像素艺术风格'
}

def call_generate_image_skill(prompt, output_path, retries=3):
    """
    Call the generate-image skill to create an image

    Args:
        prompt: Text description for image generation
        output_path: Where to save the generated image
        retries: Number of retry attempts

    Returns:
        bool: Success status
    """
    for attempt in range(retries):
        try:
            print(f"  🎨 Generating image (attempt {attempt + 1}/{retries})...")

            # Call the generate-image skill via subprocess
            # The skill should be invoked as: generate-image <prompt> --output <path>
            result = subprocess.run(
                ['claude-code', 'skill', 'generate-image', prompt, '--output', str(output_path)],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0 and Path(output_path).exists():
                print(f"  ✅ Image generated successfully")
                return True
            else:
                print(f"  ⚠️  Generation failed: {result.stderr}")

        except subprocess.TimeoutExpired:
            print(f"  ⚠️  Timeout on attempt {attempt + 1}")
        except Exception as e:
            print(f"  ⚠️  Error on attempt {attempt + 1}: {str(e)}")

        if attempt < retries - 1:
            wait_time = (attempt + 1) * 2
            print(f"  ⏳ Waiting {wait_time}s before retry...")
            time.sleep(wait_time)

    return False

def generate_frame_prompt(base_description, animation_type, frame_number, total_frames):
    """
    Generate a detailed prompt for a specific animation frame

    Args:
        base_description: Description of the base character/pet
        animation_type: Type of animation (from ANIMATION_TYPES)
        frame_number: Current frame number (0-indexed)
        total_frames: Total number of frames in animation

    Returns:
        str: Detailed prompt for image generation
    """
    animation_desc = ANIMATION_TYPES.get(animation_type, '动作序列')

    # Calculate progress through animation (0.0 to 1.0)
    progress = frame_number / (total_frames - 1) if total_frames > 1 else 0.5

    # Frame-specific descriptors based on progress
    if progress < 0.25:
        phase = "起始阶段"
        phase_desc = "动作刚开始，准备姿态"
    elif progress < 0.5:
        phase = "发展阶段"
        phase_desc = "动作进行中，中间过渡"
    elif progress < 0.75:
        phase = "高潮阶段"
        phase_desc = "动作最明显的时刻"
    else:
        phase = "结束阶段"
        phase_desc = "动作收尾，回到待机"

    prompt = f"""像素艺术风格的角色动画帧 - 第{frame_number + 1}帧（共{total_frames}帧）

角色: {base_description}

动画类型: {animation_type} - {animation_desc}

当前阶段: {phase} - {phase_desc}
进度: {int(progress * 100)}%

要求:
- 64x64像素艺术风格
- 透明背景(PNG)
- 清晰的轮廓和鲜明的颜色
- 符合{animation_type}动作的姿态
- 帧与帧之间应该有连贯性
- 可爱的卡通风格
- 单个角色居中

这是第{frame_number + 1}帧，应该展现{animation_type}动作的{phase}。"""

    return prompt

def generate_animation_frames(base_description, animation_type, output_dir, frames=8):
    """
    Generate animation frames for a specific animation type

    Args:
        base_description: Description of the base character/pet
        animation_type: Type of animation to generate
        output_dir: Directory to save frames
        frames: Number of frames to generate (default: 8)

    Returns:
        list: Paths to generated frame images, or None if failed
    """
    if animation_type not in ANIMATION_TYPES:
        print(f"❌ Unknown animation type: {animation_type}")
        print(f"Available types: {', '.join(ANIMATION_TYPES.keys())}")
        return None

    print(f"\n🎬 Generating {frames} frames for '{animation_type}' animation")
    print(f"Description: {ANIMATION_TYPES[animation_type]}")
    print(f"Output directory: {output_dir}")

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    frame_paths = []
    failed_frames = []

    for i in range(frames):
        print(f"\n📸 Frame {i + 1}/{frames}")

        # Generate prompt for this frame
        prompt = generate_frame_prompt(base_description, animation_type, i, frames)

        # Output path for this frame
        frame_file = output_path / f"{animation_type}_frame_{i:02d}.png"

        # Generate the image
        success = call_generate_image_skill(prompt, frame_file)

        if success:
            frame_paths.append(str(frame_file))
        else:
            print(f"  ❌ Failed to generate frame {i + 1}")
            failed_frames.append(i)
            # Add placeholder
            frame_paths.append(None)

    if failed_frames:
        print(f"\n⚠️  Warning: {len(failed_frames)} frames failed to generate: {failed_frames}")
        if len(failed_frames) == frames:
            print("❌ All frames failed. Animation generation unsuccessful.")
            return None

    print(f"\n✅ Generated {frames - len(failed_frames)}/{frames} frames successfully")
    return frame_paths

def combine_frames_to_sprite_sheet(frame_paths, output_path, frame_size=(64, 64)):
    """
    Combine multiple frames into a single sprite sheet

    Args:
        frame_paths: List of paths to frame images
        output_path: Path to save the sprite sheet
        frame_size: Size of each frame (width, height)

    Returns:
        tuple: (width, height) of the sprite sheet, or None if failed
    """
    print(f"\n🎞️  Combining frames into sprite sheet...")

    # Filter out None values (failed frames)
    valid_frames = [p for p in frame_paths if p is not None and Path(p).exists()]

    if not valid_frames:
        print("❌ No valid frames to combine")
        return None

    num_frames = len(valid_frames)
    sprite_width = frame_size[0] * num_frames
    sprite_height = frame_size[1]

    # Create sprite sheet canvas
    sprite_sheet = Image.new('RGBA', (sprite_width, sprite_height), (0, 0, 0, 0))

    for i, frame_path in enumerate(valid_frames):
        try:
            # Open and resize frame
            frame = Image.open(frame_path).convert('RGBA')
            frame = frame.resize(frame_size, Image.Resampling.LANCZOS)

            # Paste frame into sprite sheet
            x_offset = i * frame_size[0]
            sprite_sheet.paste(frame, (x_offset, 0), frame)

            print(f"  ✓ Frame {i + 1}/{num_frames} added")

        except Exception as e:
            print(f"  ⚠️  Error processing frame {i + 1}: {str(e)}")

    # Save sprite sheet
    sprite_sheet.save(output_path)
    print(f"\n✅ Sprite sheet saved: {output_path}")
    print(f"   Size: {sprite_width}x{sprite_height} ({num_frames} frames)")

    return sprite_width, sprite_height

def generate_animation_config(animation_type, sprite_info, output_path):
    """
    Generate a JSON configuration file for the animation

    Args:
        animation_type: Type of animation
        sprite_info: Dictionary with sprite sheet information
        output_path: Path to save the config file
    """
    config = {
        'animation_type': animation_type,
        'description': ANIMATION_TYPES.get(animation_type, ''),
        'sprite_width': sprite_info['width'],
        'sprite_height': sprite_info['height'],
        'frame_width': sprite_info['frame_width'],
        'frame_height': sprite_info['frame_height'],
        'frame_count': sprite_info['frame_count'],
        'fps': 8,  # Frames per second for playback
        'loop': True
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print(f"✅ Animation config saved: {output_path}")

def main():
    """Main function for CLI usage"""
    import argparse

    parser = argparse.ArgumentParser(
        description='AI Animation Generator for Desktop Pet',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Available Animation Types:
{chr(10).join([f'  {k:12} - {v}' for k, v in ANIMATION_TYPES.items()])}

Example:
  python animation_generator.py --description "可爱的橙色小猫" --type jump --output ./animations
  python animation_generator.py --description "小熊" --type happy,walk,sleep --output ./animations
        """
    )

    parser.add_argument('--description', '-d',
                       help='Description of the base character/pet')
    parser.add_argument('--type', '-t',
                       help='Animation type(s) to generate (comma-separated for multiple)')
    parser.add_argument('--output', '-o', default='./animations',
                       help='Output directory (default: ./animations)')
    parser.add_argument('--frames', '-f', type=int, default=8,
                       help='Number of frames per animation (default: 8)')
    parser.add_argument('--size', '-s', type=int, default=64,
                       help='Frame size in pixels (default: 64)')
    parser.add_argument('--list', '-l', action='store_true',
                       help='List all available animation types')

    args = parser.parse_args()

    # List animation types
    if args.list:
        print("\n📋 Available Animation Types:\n")
        for anim_type, desc in ANIMATION_TYPES.items():
            print(f"  {anim_type:12} - {desc}")
        print()
        return

    # Validate required arguments if not listing
    if not args.description or not args.type:
        parser.error("--description and --type are required (unless using --list)")
        return

    # Parse animation types
    animation_types = [t.strip() for t in args.type.split(',')]

    print(f"\n🎨 AI Animation Generator")
    print(f"{'='*60}")
    print(f"Character: {args.description}")
    print(f"Animation types: {', '.join(animation_types)}")
    print(f"Frames per animation: {args.frames}")
    print(f"Frame size: {args.size}x{args.size}px")
    print(f"Output directory: {args.output}")
    print(f"{'='*60}\n")

    # Generate each animation type
    results = {}

    for anim_type in animation_types:
        if anim_type not in ANIMATION_TYPES:
            print(f"⚠️  Skipping unknown animation type: {anim_type}")
            continue

        # Create output directory for this animation
        anim_dir = Path(args.output) / anim_type

        # Generate frames
        frame_paths = generate_animation_frames(
            args.description,
            anim_type,
            anim_dir,
            frames=args.frames
        )

        if frame_paths:
            # Combine into sprite sheet
            sprite_path = anim_dir / f"{anim_type}_sprite.png"
            sprite_size = combine_frames_to_sprite_sheet(
                frame_paths,
                sprite_path,
                frame_size=(args.size, args.size)
            )

            if sprite_size:
                # Generate config
                sprite_info = {
                    'width': sprite_size[0],
                    'height': sprite_size[1],
                    'frame_width': args.size,
                    'frame_height': args.size,
                    'frame_count': len([p for p in frame_paths if p is not None])
                }

                config_path = anim_dir / f"{anim_type}_config.json"
                generate_animation_config(anim_type, sprite_info, config_path)

                results[anim_type] = {
                    'success': True,
                    'sprite_path': str(sprite_path),
                    'config_path': str(config_path),
                    'frames': sprite_info['frame_count']
                }
            else:
                results[anim_type] = {'success': False, 'error': 'Failed to create sprite sheet'}
        else:
            results[anim_type] = {'success': False, 'error': 'Failed to generate frames'}

    # Summary
    print(f"\n{'='*60}")
    print("📊 Generation Summary")
    print(f"{'='*60}\n")

    successful = sum(1 for r in results.values() if r.get('success'))
    total = len(results)

    for anim_type, result in results.items():
        if result.get('success'):
            print(f"✅ {anim_type:12} - {result['frames']} frames")
            print(f"   Sprite: {result['sprite_path']}")
            print(f"   Config: {result['config_path']}")
        else:
            print(f"❌ {anim_type:12} - {result.get('error', 'Unknown error')}")
        print()

    print(f"{'='*60}")
    print(f"✨ Complete: {successful}/{total} animations generated successfully")
    print(f"{'='*60}\n")

    # Save results summary
    summary_path = Path(args.output) / "generation_summary.json"
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump({
            'character_description': args.description,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'results': results
        }, f, indent=2, ensure_ascii=False)

    print(f"📄 Summary saved: {summary_path}\n")

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("\n🎨 AI Animation Generator for Desktop Pet\n")
        print("Usage:")
        print("  python animation_generator.py --description <character> --type <animations> [options]")
        print("\nExamples:")
        print("  python animation_generator.py -d '可爱的橙色小猫' -t happy")
        print("  python animation_generator.py -d '小熊' -t 'walk,jump,sleep' -o ./my-animations")
        print("  python animation_generator.py --list  # Show all animation types")
        print("\nOptions:")
        print("  --description, -d  Character description (required)")
        print("  --type, -t         Animation type(s), comma-separated (required)")
        print("  --output, -o       Output directory (default: ./animations)")
        print("  --frames, -f       Frames per animation (default: 8)")
        print("  --size, -s         Frame size in pixels (default: 64)")
        print("  --list, -l         List all available animation types")
        print()
        sys.exit(0)

    main()
