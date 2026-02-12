"""
桌面宠物互动系统核心模块
定义互动类型、生成事件监听器、支持自定义互动效果
"""

import json
from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass, asdict


class TriggerType(Enum):
    """触发方式枚举"""
    CLICK = "click"
    DOUBLE_CLICK = "dblclick"
    DRAG = "drag"
    HOVER = "hover"
    RIGHT_CLICK = "contextmenu"
    LONG_PRESS = "longpress"
    MOUSE_ENTER = "mouseenter"
    MOUSE_LEAVE = "mouseleave"


class ActionType(Enum):
    """动作类型枚举"""
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


class EffectType(Enum):
    """视觉效果枚举"""
    NONE = "none"
    FADE = "fade"
    SCALE = "scale"
    ROTATE = "rotate"
    GLOW = "glow"
    SHAKE = "shake"
    BOUNCE = "bounce"
    PULSE = "pulse"
    RIPPLE = "ripple"


@dataclass
class SoundEffect:
    """声音效果配置"""
    enabled: bool = False
    file: Optional[str] = None
    volume: float = 1.0

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class VisualEffect:
    """视觉效果配置"""
    type: str
    duration: int = 300  # 毫秒
    easing: str = "ease-in-out"
    params: Dict[str, Any] = None

    def __post_init__(self):
        if self.params is None:
            self.params = {}

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class FeedbackConfig:
    """反馈机制配置"""
    visual: bool = True
    audio: bool = False
    haptic: bool = False  # 未来支持触觉反馈
    message: Optional[str] = None

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class Interaction:
    """互动配置类"""
    name: str
    trigger: str  # TriggerType
    action: str  # ActionType
    effect: VisualEffect
    sound: Optional[SoundEffect] = None
    feedback: Optional[FeedbackConfig] = None
    params: Dict[str, Any] = None
    enabled: bool = True

    def __post_init__(self):
        if self.sound is None:
            self.sound = SoundEffect()
        if self.feedback is None:
            self.feedback = FeedbackConfig()
        if self.params is None:
            self.params = {}

    def to_dict(self) -> Dict:
        data = {
            'name': self.name,
            'trigger': self.trigger,
            'action': self.action,
            'effect': self.effect.to_dict(),
            'sound': self.sound.to_dict(),
            'feedback': self.feedback.to_dict(),
            'params': self.params,
            'enabled': self.enabled
        }
        return data

    @classmethod
    def from_dict(cls, data: Dict) -> 'Interaction':
        """从字典创建互动对象"""
        effect = VisualEffect(**data['effect'])
        sound = SoundEffect(**data['sound']) if 'sound' in data else SoundEffect()
        feedback = FeedbackConfig(**data['feedback']) if 'feedback' in data else FeedbackConfig()

        return cls(
            name=data['name'],
            trigger=data['trigger'],
            action=data['action'],
            effect=effect,
            sound=sound,
            feedback=feedback,
            params=data.get('params', {}),
            enabled=data.get('enabled', True)
        )


class InteractionManager:
    """互动管理器"""

    def __init__(self):
        self.interactions: List[Interaction] = []

    def add_interaction(self, interaction: Interaction) -> None:
        """添加互动"""
        self.interactions.append(interaction)

    def remove_interaction(self, name: str) -> bool:
        """移除互动"""
        for i, interaction in enumerate(self.interactions):
            if interaction.name == name:
                self.interactions.pop(i)
                return True
        return False

    def get_interaction(self, name: str) -> Optional[Interaction]:
        """获取互动"""
        for interaction in self.interactions:
            if interaction.name == name:
                return interaction
        return None

    def enable_interaction(self, name: str) -> bool:
        """启用互动"""
        interaction = self.get_interaction(name)
        if interaction:
            interaction.enabled = True
            return True
        return False

    def disable_interaction(self, name: str) -> bool:
        """禁用互动"""
        interaction = self.get_interaction(name)
        if interaction:
            interaction.enabled = False
            return True
        return False

    def export_config(self) -> Dict:
        """导出配置"""
        return {
            'interactions': [i.to_dict() for i in self.interactions]
        }

    def import_config(self, config: Dict) -> None:
        """导入配置"""
        self.interactions = []
        for interaction_data in config.get('interactions', []):
            self.interactions.append(Interaction.from_dict(interaction_data))

    def generate_javascript(self, template_path: Optional[str] = None) -> str:
        """生成 JavaScript 事件监听器代码"""
        js_code = []

        # 开始部分
        js_code.append("// 桌面宠物互动系统 - 自动生成")
        js_code.append("// Generated by interactions.py\n")
        js_code.append("class PetInteractionSystem {")
        js_code.append("  constructor(petElement) {")
        js_code.append("    this.pet = petElement;")
        js_code.append("    this.interactions = new Map();")
        js_code.append("    this.longPressTimer = null;")
        js_code.append("    this.longPressDelay = 800; // 长按延迟 (ms)")
        js_code.append("    this.isDragging = false;")
        js_code.append("    this.dragOffset = { x: 0, y: 0 };")
        js_code.append("    this.init();")
        js_code.append("  }\n")

        # 初始化方法
        js_code.append("  init() {")
        js_code.append("    this.setupEventListeners();")
        js_code.append("    this.loadInteractions();")
        js_code.append("  }\n")

        # 加载互动配置
        js_code.append("  loadInteractions() {")
        js_code.append("    const config = " + json.dumps(self.export_config(), indent=4) + ";")
        js_code.append("    config.interactions.forEach(interaction => {")
        js_code.append("      if (interaction.enabled) {")
        js_code.append("        this.interactions.set(interaction.name, interaction);")
        js_code.append("      }")
        js_code.append("    });")
        js_code.append("  }\n")

        # 设置事件监听器
        js_code.append("  setupEventListeners() {")

        # 为每个互动添加事件监听器
        triggers_used = set()
        for interaction in self.interactions:
            if interaction.enabled:
                triggers_used.add(interaction.trigger)

        for trigger in triggers_used:
            if trigger == TriggerType.CLICK.value:
                js_code.append("    this.pet.addEventListener('click', (e) => this.handleClick(e));")
            elif trigger == TriggerType.DOUBLE_CLICK.value:
                js_code.append("    this.pet.addEventListener('dblclick', (e) => this.handleDoubleClick(e));")
            elif trigger == TriggerType.RIGHT_CLICK.value:
                js_code.append("    this.pet.addEventListener('contextmenu', (e) => this.handleRightClick(e));")
            elif trigger == TriggerType.HOVER.value or trigger == TriggerType.MOUSE_ENTER.value:
                js_code.append("    this.pet.addEventListener('mouseenter', (e) => this.handleMouseEnter(e));")
            elif trigger == TriggerType.MOUSE_LEAVE.value:
                js_code.append("    this.pet.addEventListener('mouseleave', (e) => this.handleMouseLeave(e));")
            elif trigger == TriggerType.DRAG.value:
                js_code.append("    this.pet.addEventListener('mousedown', (e) => this.handleMouseDown(e));")
                js_code.append("    document.addEventListener('mousemove', (e) => this.handleMouseMove(e));")
                js_code.append("    document.addEventListener('mouseup', (e) => this.handleMouseUp(e));")
            elif trigger == TriggerType.LONG_PRESS.value:
                js_code.append("    this.pet.addEventListener('mousedown', (e) => this.startLongPress(e));")
                js_code.append("    this.pet.addEventListener('mouseup', (e) => this.cancelLongPress(e));")
                js_code.append("    this.pet.addEventListener('mouseleave', (e) => this.cancelLongPress(e));")

        js_code.append("  }\n")

        # 事件处理方法
        js_code.append("  handleClick(event) {")
        js_code.append("    this.executeInteractions('click', event);")
        js_code.append("  }\n")

        js_code.append("  handleDoubleClick(event) {")
        js_code.append("    this.executeInteractions('dblclick', event);")
        js_code.append("  }\n")

        js_code.append("  handleRightClick(event) {")
        js_code.append("    event.preventDefault();")
        js_code.append("    this.executeInteractions('contextmenu', event);")
        js_code.append("  }\n")

        js_code.append("  handleMouseEnter(event) {")
        js_code.append("    this.executeInteractions('mouseenter', event);")
        js_code.append("    this.executeInteractions('hover', event);")
        js_code.append("  }\n")

        js_code.append("  handleMouseLeave(event) {")
        js_code.append("    this.executeInteractions('mouseleave', event);")
        js_code.append("  }\n")

        # 拖拽处理
        js_code.append("  handleMouseDown(event) {")
        js_code.append("    if (event.button === 0) { // 左键")
        js_code.append("      this.isDragging = true;")
        js_code.append("      const rect = this.pet.getBoundingClientRect();")
        js_code.append("      this.dragOffset.x = event.clientX - rect.left;")
        js_code.append("      this.dragOffset.y = event.clientY - rect.top;")
        js_code.append("      this.pet.style.cursor = 'grabbing';")
        js_code.append("    }")
        js_code.append("  }\n")

        js_code.append("  handleMouseMove(event) {")
        js_code.append("    if (this.isDragging) {")
        js_code.append("      this.executeInteractions('drag', event);")
        js_code.append("      const x = event.clientX - this.dragOffset.x;")
        js_code.append("      const y = event.clientY - this.dragOffset.y;")
        js_code.append("      this.pet.style.left = x + 'px';")
        js_code.append("      this.pet.style.top = y + 'px';")
        js_code.append("    }")
        js_code.append("  }\n")

        js_code.append("  handleMouseUp(event) {")
        js_code.append("    this.isDragging = false;")
        js_code.append("    this.pet.style.cursor = 'grab';")
        js_code.append("  }\n")

        # 长按处理
        js_code.append("  startLongPress(event) {")
        js_code.append("    this.longPressTimer = setTimeout(() => {")
        js_code.append("      this.executeInteractions('longpress', event);")
        js_code.append("    }, this.longPressDelay);")
        js_code.append("  }\n")

        js_code.append("  cancelLongPress(event) {")
        js_code.append("    if (this.longPressTimer) {")
        js_code.append("      clearTimeout(this.longPressTimer);")
        js_code.append("      this.longPressTimer = null;")
        js_code.append("    }")
        js_code.append("  }\n")

        # 执行互动
        js_code.append("  executeInteractions(trigger, event) {")
        js_code.append("    this.interactions.forEach((interaction, name) => {")
        js_code.append("      if (interaction.trigger === trigger && interaction.enabled) {")
        js_code.append("        this.executeAction(interaction, event);")
        js_code.append("      }")
        js_code.append("    });")
        js_code.append("  }\n")

        # 执行动作
        js_code.append("  executeAction(interaction, event) {")
        js_code.append("    const { action, effect, sound, feedback, params } = interaction;")
        js_code.append("")
        js_code.append("    // 播放声音")
        js_code.append("    if (sound && sound.enabled && sound.file) {")
        js_code.append("      this.playSound(sound.file, sound.volume);")
        js_code.append("    }")
        js_code.append("")
        js_code.append("    // 应用视觉效果")
        js_code.append("    this.applyVisualEffect(effect);")
        js_code.append("")
        js_code.append("    // 执行具体动作")
        js_code.append("    switch (action) {")
        js_code.append("      case 'playSound':")
        js_code.append("        if (params.soundFile) this.playSound(params.soundFile, params.volume || 1.0);")
        js_code.append("        break;")
        js_code.append("      case 'changeAnimation':")
        js_code.append("        if (params.animation) this.changeAnimation(params.animation);")
        js_code.append("        break;")
        js_code.append("      case 'showText':")
        js_code.append("        if (params.text) this.showText(params.text, params.duration || 2000);")
        js_code.append("        break;")
        js_code.append("      case 'toggleFullscreen':")
        js_code.append("        this.toggleFullscreen();")
        js_code.append("        break;")
        js_code.append("      case 'changeSkin':")
        js_code.append("        if (params.skin) this.changeSkin(params.skin);")
        js_code.append("        break;")
        js_code.append("      case 'showMenu':")
        js_code.append("        this.showContextMenu(event);")
        js_code.append("        break;")
        js_code.append("      case 'hide':")
        js_code.append("        this.hidePet();")
        js_code.append("        break;")
        js_code.append("      case 'sleepMode':")
        js_code.append("        this.enterSleepMode();")
        js_code.append("        break;")
        js_code.append("      case 'bounce':")
        js_code.append("        this.bounce();")
        js_code.append("        break;")
        js_code.append("      case 'spin':")
        js_code.append("        this.spin();")
        js_code.append("        break;")
        js_code.append("      case 'shake':")
        js_code.append("        this.shake();")
        js_code.append("        break;")
        js_code.append("    }")
        js_code.append("")
        js_code.append("    // 显示反馈")
        js_code.append("    if (feedback && feedback.message) {")
        js_code.append("      this.showFeedback(feedback.message);")
        js_code.append("    }")
        js_code.append("  }\n")

        # 辅助方法
        js_code.append("  applyVisualEffect(effect) {")
        js_code.append("    if (!effect || effect.type === 'none') return;")
        js_code.append("")
        js_code.append("    const { type, duration, easing, params } = effect;")
        js_code.append("    this.pet.style.transition = `all ${duration}ms ${easing}`;")
        js_code.append("")
        js_code.append("    switch (type) {")
        js_code.append("      case 'glow':")
        js_code.append("        this.pet.style.filter = 'drop-shadow(0 0 10px rgba(255, 255, 255, 0.8))';")
        js_code.append("        setTimeout(() => { this.pet.style.filter = 'none'; }, duration);")
        js_code.append("        break;")
        js_code.append("      case 'pulse':")
        js_code.append("        this.pet.style.transform = 'scale(1.1)';")
        js_code.append("        setTimeout(() => { this.pet.style.transform = 'scale(1)'; }, duration);")
        js_code.append("        break;")
        js_code.append("      case 'shake':")
        js_code.append("        this.pet.classList.add('shake-animation');")
        js_code.append("        setTimeout(() => { this.pet.classList.remove('shake-animation'); }, duration);")
        js_code.append("        break;")
        js_code.append("      case 'bounce':")
        js_code.append("        this.pet.classList.add('bounce-animation');")
        js_code.append("        setTimeout(() => { this.pet.classList.remove('bounce-animation'); }, duration);")
        js_code.append("        break;")
        js_code.append("    }")
        js_code.append("  }\n")

        js_code.append("  playSound(file, volume = 1.0) {")
        js_code.append("    const audio = new Audio(file);")
        js_code.append("    audio.volume = volume;")
        js_code.append("    audio.play().catch(e => console.warn('无法播放声音:', e));")
        js_code.append("  }\n")

        js_code.append("  changeAnimation(animation) {")
        js_code.append("    this.pet.className = `pet-animation-${animation}`;")
        js_code.append("  }\n")

        js_code.append("  showText(text, duration) {")
        js_code.append("    const bubble = document.createElement('div');")
        js_code.append("    bubble.className = 'speech-bubble';")
        js_code.append("    bubble.textContent = text;")
        js_code.append("    this.pet.appendChild(bubble);")
        js_code.append("    setTimeout(() => bubble.remove(), duration);")
        js_code.append("  }\n")

        js_code.append("  showContextMenu(event) {")
        js_code.append("    // 实现右键菜单")
        js_code.append("    console.log('显示右键菜单');")
        js_code.append("  }\n")

        js_code.append("  hidePet() {")
        js_code.append("    this.pet.style.opacity = '0';")
        js_code.append("  }\n")

        js_code.append("  enterSleepMode() {")
        js_code.append("    this.pet.classList.add('sleeping');")
        js_code.append("  }\n")

        js_code.append("  bounce() {")
        js_code.append("    this.pet.classList.add('bounce-animation');")
        js_code.append("    setTimeout(() => this.pet.classList.remove('bounce-animation'), 600);")
        js_code.append("  }\n")

        js_code.append("  spin() {")
        js_code.append("    this.pet.style.transform = 'rotate(360deg)';")
        js_code.append("    setTimeout(() => { this.pet.style.transform = 'rotate(0deg)'; }, 500);")
        js_code.append("  }\n")

        js_code.append("  shake() {")
        js_code.append("    this.pet.classList.add('shake-animation');")
        js_code.append("    setTimeout(() => this.pet.classList.remove('shake-animation'), 500);")
        js_code.append("  }\n")

        js_code.append("  showFeedback(message) {")
        js_code.append("    console.log('反馈:', message);")
        js_code.append("  }")

        js_code.append("}\n")

        # 导出
        js_code.append("// 使用示例:")
        js_code.append("// const pet = document.getElementById('desktop-pet');")
        js_code.append("// const interactionSystem = new PetInteractionSystem(pet);")

        return "\n".join(js_code)


def create_default_interactions() -> List[Interaction]:
    """创建默认互动配置"""
    interactions = []

    # 点击 - 弹跳
    interactions.append(Interaction(
        name="click_bounce",
        trigger=TriggerType.CLICK.value,
        action=ActionType.BOUNCE.value,
        effect=VisualEffect(type=EffectType.BOUNCE.value, duration=400),
        sound=SoundEffect(enabled=True, file="sounds/click.mp3", volume=0.5),
        feedback=FeedbackConfig(visual=True, message="宠物很开心!")
    ))

    # 双击 - 旋转
    interactions.append(Interaction(
        name="doubleclick_spin",
        trigger=TriggerType.DOUBLE_CLICK.value,
        action=ActionType.SPIN.value,
        effect=VisualEffect(type=EffectType.ROTATE.value, duration=500),
        sound=SoundEffect(enabled=True, file="sounds/spin.mp3", volume=0.6),
        params={"rotation": 360}
    ))

    # 悬停 - 发光
    interactions.append(Interaction(
        name="hover_glow",
        trigger=TriggerType.HOVER.value,
        action=ActionType.GLOW_EFFECT.value,
        effect=VisualEffect(type=EffectType.GLOW.value, duration=300),
        feedback=FeedbackConfig(visual=True, message="你在看我吗?")
    ))

    # 右键 - 显示菜单
    interactions.append(Interaction(
        name="rightclick_menu",
        trigger=TriggerType.RIGHT_CLICK.value,
        action=ActionType.SHOW_MENU.value,
        effect=VisualEffect(type=EffectType.NONE.value),
        params={"menu": ["隐藏", "设置", "退出"]}
    ))

    # 长按 - 睡眠模式
    interactions.append(Interaction(
        name="longpress_sleep",
        trigger=TriggerType.LONG_PRESS.value,
        action=ActionType.SLEEP_MODE.value,
        effect=VisualEffect(type=EffectType.FADE.value, duration=800),
        sound=SoundEffect(enabled=True, file="sounds/sleep.mp3", volume=0.3),
        feedback=FeedbackConfig(visual=True, message="晚安...")
    ))

    # 拖拽 - 移动位置
    interactions.append(Interaction(
        name="drag_move",
        trigger=TriggerType.DRAG.value,
        action=ActionType.MOVE_POSITION.value,
        effect=VisualEffect(type=EffectType.NONE.value),
        feedback=FeedbackConfig(visual=False)
    ))

    return interactions


if __name__ == "__main__":
    # 测试代码
    manager = InteractionManager()

    # 添加默认互动
    for interaction in create_default_interactions():
        manager.add_interaction(interaction)

    # 导出配置
    config = manager.export_config()
    print("配置导出成功:")
    print(json.dumps(config, indent=2, ensure_ascii=False))

    # 生成 JavaScript
    js_code = manager.generate_javascript()
    print("\nJavaScript 代码生成成功!")
    print(f"代码行数: {len(js_code.splitlines())}")
