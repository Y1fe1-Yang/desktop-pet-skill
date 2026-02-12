# AI Animation Generator

AI-powered animation frame generator for Desktop Pet. Generates unique, AI-generated animation frames for different interaction types.

## Overview

The `animation_generator.py` script uses the `generate-image` skill to create custom animation frames for various pet interactions. Unlike the basic `pet_generator.py` which uses PIL transformations, this generator creates truly unique animations where each frame is AI-generated.

## Features

- 20 pre-defined animation types (idle, walk, jump, happy, pet, sleep, etc.)
- AI-generated frames with detailed prompts for each animation phase
- Automatic sprite sheet generation (8 frames → 512x64 sprite sheet)
- JSON configuration output for each animation
- Retry mechanism for robust generation
- Batch generation support (multiple animations at once)

## Animation Types

| Type | Description |
|------|-------------|
| `idle` | 静止待机状态，轻微呼吸动作 |
| `walk` | 行走动作，腿部交替移动 |
| `jump` | 跳跃动作序列，从蹲下到跃起 |
| `happy` | 开心表情，可能有爱心特效 |
| `pet` | 被抚摸的享受表情，闭眼微笑 |
| `sleep` | 睡觉姿态，Z字符号 |
| `eat` | 吃东西动作，咀嚼表情 |
| `celebrate` | 庆祝动作，举手欢呼 |
| `shake` | 摇晃或抖动身体 |
| `bounce` | 弹跳动作，有弹性的运动 |
| `sad` | 伤心表情，可能有眼泪 |
| `angry` | 生气表情，可能有火焰符号 |
| `wave` | 挥手问候 |
| `dance` | 跳舞动作，节奏感的摆动 |
| `stretch` | 伸展动作，伸懒腰 |
| `spin` | 旋转动作，360度转身 |
| `surprise` | 惊讶表情，张大嘴巴 |
| `think` | 思考姿态，手托腮 |
| `run` | 奔跑动作，快速移动 |
| `fly` | 飞行动作，张开翅膀 |

## Usage

### List Available Animation Types

```bash
python3 animation_generator.py --list
```

### Generate Single Animation

```bash
python3 animation_generator.py \
  --description "可爱的橙色小猫" \
  --type happy \
  --output ./animations
```

### Generate Multiple Animations

```bash
python3 animation_generator.py \
  --description "小熊" \
  --type "idle,walk,jump,happy,sleep" \
  --output ./my-pet-animations
```

### Custom Frame Count and Size

```bash
python3 animation_generator.py \
  --description "蓝色小鸟" \
  --type fly \
  --frames 12 \
  --size 128 \
  --output ./bird-animations
```

## Command Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--description` | `-d` | Character description (required) | - |
| `--type` | `-t` | Animation type(s), comma-separated (required) | - |
| `--output` | `-o` | Output directory | `./animations` |
| `--frames` | `-f` | Number of frames per animation | 8 |
| `--size` | `-s` | Frame size in pixels | 64 |
| `--list` | `-l` | List all available animation types | - |

## Output Structure

For each animation type, the generator creates:

```
animations/
├── idle/
│   ├── idle_frame_00.png       # Individual frames
│   ├── idle_frame_01.png
│   ├── ...
│   ├── idle_frame_07.png
│   ├── idle_sprite.png         # Combined sprite sheet
│   └── idle_config.json        # Animation configuration
├── walk/
│   └── ...
└── generation_summary.json     # Overall generation summary
```

### Animation Config Format

```json
{
  "animation_type": "happy",
  "description": "开心表情，欢快的姿态，可能有爱心或星星特效...",
  "sprite_width": 512,
  "sprite_height": 64,
  "frame_width": 64,
  "frame_height": 64,
  "frame_count": 8,
  "fps": 8,
  "loop": true
}
```

## Implementation Details

### Frame Generation Process

1. For each frame, generates a detailed prompt including:
   - Base character description
   - Animation type and phase
   - Frame number and progress (0-100%)
   - Pixel art style requirements
   - Transparent background specification

2. Calls `generate-image` skill with retry mechanism (3 attempts)

3. Validates generated image exists

### Prompt Engineering

Each frame prompt is dynamically generated based on:
- **Animation Phase**: Starting (0-25%), Developing (25-50%), Peak (50-75%), Ending (75-100%)
- **Progress**: Ensures smooth transitions between frames
- **Style Consistency**: All prompts include pixel art and transparency requirements

### Error Handling

- Retry mechanism with exponential backoff
- Graceful handling of failed frames
- Continues generation even if some frames fail
- Summary report of successes and failures

## Integration with Desktop Pet

The generated sprite sheets can be used directly in the desktop pet application:

```javascript
// Example usage in pet application
const animations = {
  idle: {
    sprite: 'animations/idle/idle_sprite.png',
    frames: 8,
    fps: 8
  },
  walk: {
    sprite: 'animations/walk/walk_sprite.png',
    frames: 8,
    fps: 8
  }
};
```

## Examples

### Example 1: Cute Cat Pet

```bash
python3 animation_generator.py \
  -d "可爱的橙色小猫，大眼睛，圆圆的脸" \
  -t "idle,walk,jump,happy,pet,sleep,eat" \
  -o ./cat-animations
```

### Example 2: Bear Character

```bash
python3 animation_generator.py \
  -d "棕色的小熊，友好的笑容，穿着蓝色围巾" \
  -t "wave,celebrate,dance,happy,think" \
  -o ./bear-animations
```

### Example 3: Dragon Pet

```bash
python3 animation_generator.py \
  -d "小龙，绿色鳞片，可爱的翅膀" \
  -t "fly,breathe,roar,sleep,celebrate" \
  -f 10 \
  -s 64 \
  -o ./dragon-animations
```

## Tips for Best Results

1. **Character Description**: Be specific about colors, features, and style
2. **Batch Generation**: Generate multiple animations at once to maintain style consistency
3. **Frame Count**: 8 frames is optimal for smooth animation and reasonable generation time
4. **Animation Selection**: Choose animations that match your character's capabilities
5. **Review Output**: Check `generation_summary.json` for any failed frames

## Troubleshooting

### All frames fail to generate

- Check `generate-image` skill is installed and working
- Verify network connectivity
- Try with simpler character descriptions

### Inconsistent style across frames

- Use more detailed character descriptions
- Specify consistent style keywords (e.g., "像素艺术", "卡通风格")
- Generate all animations in one batch

### Long generation time

- Reduce number of frames (`--frames 6`)
- Generate fewer animation types at once
- Check API rate limits

## Technical Requirements

- Python 3.7+
- PIL/Pillow library
- `generate-image` skill installed
- Claude Code CLI access

## Future Enhancements

- [ ] Custom animation type definitions
- [ ] Style transfer from reference image
- [ ] Automatic animation blending/transitions
- [ ] Preview animation in terminal
- [ ] GIF export option
- [ ] Video format export (MP4)

## License

Part of the Desktop Pet Generator skill.
