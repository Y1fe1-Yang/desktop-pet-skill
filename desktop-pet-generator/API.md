# Desktop Pet Generator - API 文档

本文档提供桌面宠物生成器所有 Python 脚本、模板变量和扩展 API 的详细说明。

## 目录

1. [Python 脚本 API](#python-脚本-api)
   - [image_analyzer.py](#image_analyzerpy)
   - [animation_builder.py](#animation_builderpy)
   - [interactions.py](#interactionspy)
2. [模板系统](#模板系统)
3. [JavaScript API](#javascript-api)
4. [配置文件格式](#配置文件格式)
5. [扩展开发指南](#扩展开发指南)

---

## Python 脚本 API

### image_analyzer.py

**位置**: `~/.claude/skills/desktop-pet-generator/scripts/image_analyzer.py`

图片分析工具，用于提取图片特征、颜色和元数据。

#### 类: `ImageAnalyzer`

##### 初始化

```python
analyzer = ImageAnalyzer(image_path: str)
```

**参数**:
- `image_path` (str): 图片文件的路径

**示例**:
```python
from image_analyzer import ImageAnalyzer

analyzer = ImageAnalyzer("path/to/pet.png")
results = analyzer.analyze()
```

##### 方法

###### `load_image()`

加载并验证图片文件。

```python
analyzer.load_image()
```

**返回**: None

**异常**:
- `FileNotFoundError`: 图片文件不存在
- `ValueError`: 图片格式无法识别

---

###### `get_dimensions() -> Dict[str, int]`

获取图片尺寸信息。

```python
dims = analyzer.get_dimensions()
```

**返回**:
```python
{
    "width": 500,
    "height": 500,
    "aspect_ratio": 1.0
}
```

---

###### `has_transparency() -> bool`

检查图片是否包含透明像素。

```python
has_alpha = analyzer.has_transparency()
```

**返回**: `bool` - True 表示有透明度，False 表示无

---

###### `get_dominant_colors(num_colors: int = 5) -> List[Dict]`

提取主色调。

```python
colors = analyzer.get_dominant_colors(num_colors=5)
```

**参数**:
- `num_colors` (int): 要提取的颜色数量，默认 5

**返回**:
```python
[
    {
        "hex": "#FF5733",
        "rgb": [255, 87, 51],
        "percentage": 35.2,
        "name": "red"
    },
    ...
]
```

---

###### `detect_complexity() -> str`

检测图片复杂度。

```python
complexity = analyzer.detect_complexity()
```

**返回**: `str` - "simple", "moderate", 或 "complex"

---

###### `suggest_mode() -> str`

根据图片特征推荐动画模式。

```python
mode = analyzer.suggest_mode()
```

**返回**: `str` - "css" 或 "sprite"

---

###### `get_suggested_size() -> str`

推荐显示尺寸。

```python
size = analyzer.get_suggested_size()
```

**返回**: `str` - 如 "200px"

---

###### `detect_features() -> List[str]`

检测图片特征（形状、对比度等）。

```python
features = analyzer.detect_features()
```

**返回**:
```python
["transparent_background", "square_shape", "high_contrast"]
```

---

###### `analyze() -> Dict`

运行完整分析。

```python
results = analyzer.analyze()
```

**返回**:
```python
{
    "file": {
        "path": "/path/to/image.png",
        "name": "image.png",
        "format": "PNG",
        "size_kb": 120.5
    },
    "dimensions": {
        "width": 500,
        "height": 500,
        "aspect_ratio": 1.0
    },
    "transparency": true,
    "dominant_colors": [...],
    "complexity": "moderate",
    "features": ["transparent_background", "square_shape"],
    "suggestions": {
        "mode": "css",
        "display_size": "200px",
        "mode_reason": "Image is moderate with good transparency support..."
    }
}
```

#### 命令行用法

```bash
python image_analyzer.py <image_path>
```

**输出**: JSON 格式的分析结果

**示例**:
```bash
python image_analyzer.py my_pet.png
```

---

### animation_builder.py

**位置**: `~/.claude/skills/desktop-pet-generator/scripts/animation_builder.py`

动画构建工具，提供预设动画库和组合系统。

#### 类: `AnimationLibrary`

动画预设库。

##### 类属性

- `CSS_ANIMATIONS` (Dict): CSS 关键帧动画字典
- `SPRITE_ANIMATIONS` (Dict): 精灵图动画配置字典

##### 类方法

###### `get_animation(name: str, mode: str = "css") -> Optional[Dict]`

获取指定动画。

```python
anim = AnimationLibrary.get_animation("float", mode="css")
```

**参数**:
- `name` (str): 动画名称
- `mode` (str): "css" 或 "sprite"

**返回**: 动画配置字典，如果不存在则返回 None

---

###### `get_by_category(category: str, mode: str = "css") -> Dict[str, Dict]`

获取某类别的所有动画。

```python
idle_anims = AnimationLibrary.get_by_category("idle", mode="css")
```

**参数**:
- `category` (str): 类别名称（如 "idle", "movement", "interactive"）
- `mode` (str): "css" 或 "sprite"

**返回**: 该类别的所有动画

---

###### `get_default_set(mode: str = "css") -> List[str]`

获取默认推荐的动画集合。

```python
defaults = AnimationLibrary.get_default_set(mode="css")
# 返回: ["float", "walk", "onClick"]
```

---

###### `list_all(mode: str = "css") -> Dict[str, List[str]]`

列出所有动画，按类别分组。

```python
all_anims = AnimationLibrary.list_all(mode="css")
# 返回:
# {
#     "idle": ["float", "breathe", "sway"],
#     "movement": ["walk", "jump", "fly"],
#     ...
# }
```

---

#### 类: `AnimationBuilder`

动画构建器。

##### 初始化

```python
builder = AnimationBuilder(mode: str = "css")
```

**参数**:
- `mode` (str): "css" 或 "sprite"

##### 方法

###### `add_animation(name: str)`

添加动画到构建队列。

```python
builder.add_animation("float")
builder.add_animation("walk")
```

**异常**: `ValueError` - 动画不存在

---

###### `add_multiple(names: List[str])`

批量添加动画。

```python
builder.add_multiple(["float", "walk", "onClick"])
```

---

###### `generate_css() -> str`

生成合并后的 CSS 代码（仅 CSS 模式）。

```python
css_code = builder.generate_css()
```

**返回**: 完整的 CSS 字符串

---

###### `generate_sprite_config() -> Dict`

生成精灵图动画配置（仅 Sprite 模式）。

```python
config = builder.generate_sprite_config()
```

**返回**:
```python
{
    "animations": {
        "walk_sprite": {
            "frames": 8,
            "fps": 12,
            "loop": true
        },
        ...
    },
    "default": "idle_sprite"
}
```

---

###### `generate_javascript(interactions: List[str]) -> str`

生成交互 JavaScript 代码。

```python
js_code = builder.generate_javascript(["clickable", "draggable", "status_aware"])
```

**参数**:
- `interactions` (List[str]): 交互类型列表
  - `"clickable"`: 点击交互
  - `"draggable"`: 拖拽交互
  - `"status_aware"`: 状态感知（检测打字、空闲等）

**返回**: JavaScript 代码字符串

---

###### `get_summary() -> Dict`

获取已添加动画的摘要。

```python
summary = builder.get_summary()
```

**返回**:
```python
{
    "mode": "css",
    "count": 3,
    "animations": [
        {
            "name": "float",
            "display_name": "Float",
            "category": "idle",
            "description": "Gentle up/down hover"
        },
        ...
    ]
}
```

#### 可用动画列表

##### CSS 动画

**待机类 (idle)**:
- `float`: 上下浮动
- `breathe`: 缩放呼吸效果
- `sway`: 左右摇摆

**移动类 (movement)**:
- `walk`: 水平行走
- `jump`: 跳跃
- `fly`: 飞行路径

**交互类 (interactive)**:
- `onClick`: 点击响应
- `onHover`: 悬停效果

**情感类 (emotional)**:
- `happy`: 开心跳跃
- `sad`: 悲伤下沉
- `excited`: 激动摇晃
- `sleep`: 睡眠状态

**工作状态类 (work)**:
- `coding`: 打字效果
- `thinking`: 思考摇摆
- `complete`: 完成庆祝
- `error`: 错误抖动

#### 命令行用法

```bash
python animation_builder.py <mode> <animation1,animation2,...>
```

**示例**:
```bash
python animation_builder.py css float,walk,onClick
```

**输出**: 动画摘要和生成的代码

---

### interactions.py

**位置**: `~/.claude/skills/desktop-pet-generator/scripts/interactions.py`

交互系统核心模块，定义交互类型和生成事件监听器。

#### 枚举类

##### `TriggerType`

触发方式枚举。

```python
class TriggerType(Enum):
    CLICK = "click"
    DOUBLE_CLICK = "dblclick"
    DRAG = "drag"
    HOVER = "hover"
    RIGHT_CLICK = "contextmenu"
    LONG_PRESS = "longpress"
    MOUSE_ENTER = "mouseenter"
    MOUSE_LEAVE = "mouseleave"
```

##### `ActionType`

动作类型枚举。

```python
class ActionType(Enum):
    PLAY_SOUND = "playSound"
    CHANGE_ANIMATION = "changeAnimation"
    SHOW_TEXT = "showText"
    TOGGLE_FULLSCREEN = "toggleFullscreen"
    CHANGE_SKIN = "changeSkin"
    MOVE_POSITION = "movePosition"
    SHOW_TOOLTIP = "showTooltip"
    GLOW_EFFECT = "glowEffect"
    SHOW_MENU = "showMenu"
    HIDE = "hide"
    OPEN_SETTINGS = "openSettings"
    EXIT = "exit"
    SLEEP_MODE = "sleepMode"
    BOUNCE = "bounce"
    SPIN = "spin"
    SHAKE = "shake"
```

##### `EffectType`

视觉效果枚举。

```python
class EffectType(Enum):
    NONE = "none"
    FADE = "fade"
    SCALE = "scale"
    ROTATE = "rotate"
    GLOW = "glow"
    SHAKE = "shake"
    BOUNCE = "bounce"
    PULSE = "pulse"
    RIPPLE = "ripple"
```

#### 数据类

##### `SoundEffect`

声音效果配置。

```python
@dataclass
class SoundEffect:
    enabled: bool = False
    file: Optional[str] = None
    volume: float = 1.0
```

**示例**:
```python
sound = SoundEffect(enabled=True, file="sounds/meow.mp3", volume=0.8)
```

---

##### `VisualEffect`

视觉效果配置。

```python
@dataclass
class VisualEffect:
    type: str
    duration: int = 300  # 毫秒
    easing: str = "ease-in-out"
    params: Dict[str, Any] = None
```

**示例**:
```python
effect = VisualEffect(
    type="glow",
    duration=500,
    easing="ease-out",
    params={"intensity": 0.8}
)
```

---

##### `FeedbackConfig`

反馈机制配置。

```python
@dataclass
class FeedbackConfig:
    visual: bool = True
    audio: bool = False
    haptic: bool = False
    message: Optional[str] = None
```

---

##### `Interaction`

完整的交互配置。

```python
@dataclass
class Interaction:
    name: str
    trigger: str  # TriggerType
    action: str  # ActionType
    effect: VisualEffect
    sound: Optional[SoundEffect] = None
    feedback: Optional[FeedbackConfig] = None
    params: Dict[str, Any] = None
    enabled: bool = True
```

**方法**:
- `to_dict() -> Dict`: 导出为字典
- `from_dict(data: Dict) -> Interaction`: 从字典创建

**示例**:
```python
interaction = Interaction(
    name="click_bounce",
    trigger=TriggerType.CLICK.value,
    action=ActionType.BOUNCE.value,
    effect=VisualEffect(type=EffectType.BOUNCE.value, duration=400),
    sound=SoundEffect(enabled=True, file="sounds/click.mp3", volume=0.5),
    feedback=FeedbackConfig(visual=True, message="宠物很开心!")
)
```

---

#### 类: `InteractionManager`

交互管理器。

##### 初始化

```python
manager = InteractionManager()
```

##### 方法

###### `add_interaction(interaction: Interaction) -> None`

添加交互。

```python
manager.add_interaction(interaction)
```

---

###### `remove_interaction(name: str) -> bool`

移除交互。

```python
success = manager.remove_interaction("click_bounce")
```

**返回**: 是否成功

---

###### `get_interaction(name: str) -> Optional[Interaction]`

获取交互。

```python
interaction = manager.get_interaction("click_bounce")
```

---

###### `enable_interaction(name: str) -> bool`

启用交互。

```python
manager.enable_interaction("click_bounce")
```

---

###### `disable_interaction(name: str) -> bool`

禁用交互。

```python
manager.disable_interaction("click_bounce")
```

---

###### `export_config() -> Dict`

导出配置为 JSON。

```python
config = manager.export_config()
```

**返回**:
```python
{
    "interactions": [
        {...},
        {...}
    ]
}
```

---

###### `import_config(config: Dict) -> None`

从 JSON 导入配置。

```python
manager.import_config(config)
```

---

###### `generate_javascript(template_path: Optional[str] = None) -> str`

生成完整的 JavaScript 交互系统代码。

```python
js_code = manager.generate_javascript()
```

**返回**: JavaScript 类 `PetInteractionSystem` 的完整代码

---

#### 辅助函数

##### `create_default_interactions() -> List[Interaction]`

创建默认交互配置集合。

```python
from interactions import create_default_interactions

defaults = create_default_interactions()
# 返回包含以下默认交互的列表:
# - click_bounce (点击弹跳)
# - doubleclick_spin (双击旋转)
# - hover_glow (悬停发光)
# - rightclick_menu (右键菜单)
# - longpress_sleep (长按睡眠)
# - drag_move (拖拽移动)
```

---

## 模板系统

### 模板变量

生成项目时，以下变量可在模板中使用：

#### HTML 模板变量

| 变量名 | 类型 | 描述 |
|--------|------|------|
| `{{PET_NAME}}` | string | 宠物名称 |
| `{{PET_IMAGE}}` | string | 宠物图片路径 |
| `{{PET_SIZE}}` | string | 宠物尺寸（如 "200px"） |
| `{{ANIMATION_CSS}}` | string | 生成的动画 CSS 代码 |
| `{{INTERACTION_JS}}` | string | 生成的交互 JavaScript 代码 |
| `{{PRIMARY_COLOR}}` | string | 主色调（十六进制） |
| `{{DESCRIPTION}}` | string | 宠物描述 |

**示例模板**:
```html
<!DOCTYPE html>
<html>
<head>
    <title>{{PET_NAME}}</title>
    <style>
        {{ANIMATION_CSS}}
    </style>
</head>
<body>
    <div id="desktop-pet" class="pet" style="width: {{PET_SIZE}};">
        <img src="{{PET_IMAGE}}" alt="{{PET_NAME}}">
    </div>
    <script>
        {{INTERACTION_JS}}
    </script>
</body>
</html>
```

---

## JavaScript API

生成的项目包含以下 JavaScript API。

### 类: `PetInteractionSystem`

交互系统类（由 `interactions.py` 生成）。

#### 构造函数

```javascript
const pet = document.getElementById('desktop-pet');
const interactionSystem = new PetInteractionSystem(pet);
```

**参数**:
- `petElement` (HTMLElement): 宠物 DOM 元素

#### 属性

- `pet` (HTMLElement): 宠物元素
- `interactions` (Map): 交互配置映射
- `longPressTimer` (number|null): 长按计时器
- `longPressDelay` (number): 长按延迟（默认 800ms）
- `isDragging` (boolean): 是否正在拖拽
- `dragOffset` (Object): 拖拽偏移 `{x, y}`

#### 方法

##### 事件处理方法

- `handleClick(event)`: 处理点击事件
- `handleDoubleClick(event)`: 处理双击事件
- `handleRightClick(event)`: 处理右键点击
- `handleMouseEnter(event)`: 处理鼠标进入
- `handleMouseLeave(event)`: 处理鼠标离开
- `handleMouseDown(event)`: 处理鼠标按下
- `handleMouseMove(event)`: 处理鼠标移动
- `handleMouseUp(event)`: 处理鼠标释放

##### 交互执行方法

- `executeInteractions(trigger, event)`: 执行触发器对应的所有交互
- `executeAction(interaction, event)`: 执行具体动作

##### 效果方法

- `applyVisualEffect(effect)`: 应用视觉效果
- `playSound(file, volume)`: 播放声音
- `changeAnimation(animation)`: 切换动画
- `showText(text, duration)`: 显示文字气泡

##### 动作方法

- `bounce()`: 弹跳动画
- `spin()`: 旋转动画
- `shake()`: 抖动动画
- `hidePet()`: 隐藏宠物
- `enterSleepMode()`: 进入睡眠模式

---

## 配置文件格式

### animations.json

动画配置文件。

```json
{
  "mode": "css",
  "default": "float",
  "animations": {
    "float": {
      "name": "Float",
      "category": "idle",
      "description": "Gentle up/down hover",
      "duration": "3s",
      "timing": "ease-in-out",
      "loop": true
    }
  }
}
```

### interactions.json

交互配置文件。

```json
{
  "interactions": [
    {
      "name": "click_bounce",
      "trigger": "click",
      "action": "bounce",
      "effect": {
        "type": "bounce",
        "duration": 400,
        "easing": "ease-in-out",
        "params": {}
      },
      "sound": {
        "enabled": true,
        "file": "sounds/click.mp3",
        "volume": 0.5
      },
      "feedback": {
        "visual": true,
        "audio": false,
        "haptic": false,
        "message": "宠物很开心!"
      },
      "params": {},
      "enabled": true
    }
  ]
}
```

### pet-config.json

宠物配置文件。

```json
{
  "name": "我的猫咪",
  "image": "assets/cat.png",
  "size": "200px",
  "position": "bottom-right",
  "draggable": true,
  "alwaysOnTop": true,
  "transparency": 0.95,
  "theme": {
    "primaryColor": "#FF5733",
    "shadow": true,
    "border": "none"
  },
  "behavior": {
    "randomMovement": true,
    "randomInterval": 30000,
    "sleepAfterIdle": 600000,
    "followCursor": false
  }
}
```

---

## 扩展开发指南

### 添加自定义动画

#### 步骤 1：定义动画

在 `animation_builder.py` 的 `CSS_ANIMATIONS` 字典中添加：

```python
"my_custom_animation": {
    "name": "My Custom Animation",
    "category": "custom",
    "description": "My custom animation description",
    "css": """
@keyframes myCustomAnimation {
    0% { /* start state */ }
    100% { /* end state */ }
}
.pet.my-custom { animation: myCustomAnimation 2s ease infinite; }
""",
    "duration": "2s",
    "timing": "ease"
}
```

#### 步骤 2：使用动画

```python
builder = AnimationBuilder(mode="css")
builder.add_animation("my_custom_animation")
css_code = builder.generate_css()
```

---

### 添加自定义交互

#### 步骤 1：创建交互

```python
from interactions import Interaction, VisualEffect, SoundEffect, FeedbackConfig
from interactions import TriggerType, ActionType, EffectType

custom_interaction = Interaction(
    name="custom_action",
    trigger=TriggerType.CLICK.value,
    action=ActionType.SHOW_TEXT.value,
    effect=VisualEffect(type=EffectType.PULSE.value, duration=300),
    sound=SoundEffect(enabled=True, file="sounds/custom.mp3"),
    feedback=FeedbackConfig(message="自定义消息"),
    params={"text": "Hello!", "duration": 2000}
)
```

#### 步骤 2：添加到管理器

```python
manager = InteractionManager()
manager.add_interaction(custom_interaction)
js_code = manager.generate_javascript()
```

---

### 创建自定义模板

#### 目录结构

```
templates/
└── my-custom-template/
    ├── index.html
    ├── styles.css
    ├── pet.js
    └── config.json
```

#### config.json

```json
{
  "template_name": "my-custom-template",
  "description": "My custom template",
  "variables": [
    "PET_NAME",
    "PET_IMAGE",
    "PET_SIZE"
  ],
  "platforms": ["web", "extension", "desktop"]
}
```

---

### 集成外部 API

#### 天气 API 示例

```javascript
// 在 pet.js 中添加
class WeatherAwarePet extends PetInteractionSystem {
  constructor(petElement) {
    super(petElement);
    this.initWeatherCheck();
  }

  async initWeatherCheck() {
    const weather = await this.fetchWeather();
    this.updatePetBasedOnWeather(weather);
  }

  async fetchWeather() {
    const response = await fetch('https://api.weather.com/...');
    return response.json();
  }

  updatePetBasedOnWeather(weather) {
    if (weather.condition === 'rainy') {
      this.changeAnimation('hide');
    } else if (weather.condition === 'sunny') {
      this.changeAnimation('happy');
    }
  }
}
```

---

### 添加插件系统

#### 插件接口

```javascript
class PetPlugin {
  constructor(pet) {
    this.pet = pet;
  }

  onLoad() {
    // 插件加载时调用
  }

  onUpdate(deltaTime) {
    // 每帧更新时调用
  }

  onUnload() {
    // 插件卸载时调用
  }
}
```

#### 使用插件

```javascript
class CustomPlugin extends PetPlugin {
  onLoad() {
    console.log('Custom plugin loaded!');
    this.pet.addEventListener('click', () => {
      console.log('Pet clicked!');
    });
  }
}

// 注册插件
const plugin = new CustomPlugin(petElement);
plugin.onLoad();
```

---

## 最佳实践

### 性能优化

1. **限制动画复杂度**：避免同时运行过多动画
2. **使用 `transform` 和 `opacity`**：这些属性有硬件加速
3. **防抖和节流**：对频繁触发的事件（如 `mousemove`）使用防抖/节流
4. **懒加载资源**：音效和图片按需加载

### 代码示例：防抖

```javascript
function debounce(func, wait) {
  let timeout;
  return function(...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(this, args), wait);
  };
}

// 使用
const debouncedMove = debounce((e) => {
  console.log('Mouse moved:', e.clientX, e.clientY);
}, 100);

document.addEventListener('mousemove', debouncedMove);
```

---

## 故障排查

### 常见错误

**错误**: `ModuleNotFoundError: No module named 'PIL'`

**解决**:
```bash
pip install Pillow
```

---

**错误**: `Animation 'xyz' not found`

**解决**: 检查动画名称拼写，使用 `AnimationLibrary.list_all()` 查看可用动画

---

**错误**: JavaScript 交互无响应

**解决**:
1. 检查浏览器控制台是否有错误
2. 确认 `PetInteractionSystem` 已正确初始化
3. 验证 DOM 元素 ID 是否正确

---

## 参考资料

- [CSS Animation MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Animations)
- [JavaScript Event Reference](https://developer.mozilla.org/en-US/docs/Web/Events)
- [Pillow Documentation](https://pillow.readthedocs.io/)

---

**需要更多帮助？** 查阅其他文档：
- [README.md](README.md) - 快速入门
- [TUTORIAL.md](TUTORIAL.md) - 完整教程
- [EXAMPLES.md](EXAMPLES.md) - 实际案例
