"""
桌面宠物互动系统 - 对话式交互选择器
通过问答的方式帮助用户选择和配置互动
"""

import json
import os
from typing import List, Dict, Optional
from interactions import (
    Interaction, InteractionManager, TriggerType, ActionType,
    EffectType, SoundEffect, VisualEffect, FeedbackConfig,
    create_default_interactions
)


class InteractionUI:
    """对话式交互配置界面"""

    def __init__(self, presets_file: Optional[str] = None):
        self.manager = InteractionManager()
        self.presets = {}

        # 加载预设
        if presets_file and os.path.exists(presets_file):
            self.load_presets(presets_file)
        else:
            # 使用默认路径
            default_path = os.path.join(
                os.path.dirname(__file__),
                'interaction_presets.json'
            )
            if os.path.exists(default_path):
                self.load_presets(default_path)

    def load_presets(self, file_path: str) -> None:
        """加载预设配置"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.presets = data.get('presets', {})
                self.templates = data.get('interaction_templates', {})
                self.sound_library = data.get('sound_library', {})
            print(f"✓ 成功加载预设配置: {len(self.presets)} 个方案")
        except Exception as e:
            print(f"✗ 加载预设配置失败: {e}")

    def show_welcome(self) -> None:
        """显示欢迎信息"""
        print("\n" + "="*60)
        print("   桌面宠物互动系统配置向导")
        print("="*60)
        print("\n欢迎使用桌面宠物互动配置工具!")
        print("我将帮助你创建一个个性化的互动系统。\n")

    def ask_preset_or_custom(self) -> str:
        """询问使用预设还是自定义"""
        print("\n你想如何配置互动系统?")
        print("1. 使用预设方案 (快速)")
        print("2. 自定义配置 (灵活)")
        print("3. 混合模式 (从预设开始,再自定义)")

        while True:
            choice = input("\n请选择 (1/2/3): ").strip()
            if choice in ['1', '2', '3']:
                return choice
            print("无效选择,请输入 1、2 或 3")

    def show_presets(self) -> None:
        """显示所有预设方案"""
        print("\n可用的预设方案:")
        print("-" * 60)

        for i, (key, preset) in enumerate(self.presets.items(), 1):
            name = preset.get('name', key)
            desc = preset.get('description', '无描述')
            count = len(preset.get('interactions', []))
            print(f"{i}. {name}")
            print(f"   描述: {desc}")
            print(f"   互动数量: {count}")
            print()

    def select_preset(self) -> Optional[str]:
        """选择预设方案"""
        self.show_presets()

        preset_keys = list(self.presets.keys())
        while True:
            choice = input(f"请选择方案 (1-{len(preset_keys)}): ").strip()
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(preset_keys):
                    return preset_keys[idx]
            print("无效选择,请重试")

    def load_preset_interactions(self, preset_key: str) -> None:
        """加载预设互动"""
        preset = self.presets.get(preset_key)
        if not preset:
            print(f"未找到预设: {preset_key}")
            return

        interactions_data = preset.get('interactions', [])
        for data in interactions_data:
            try:
                interaction = Interaction.from_dict(data)
                self.manager.add_interaction(interaction)
            except Exception as e:
                print(f"加载互动失败: {e}")

        print(f"\n✓ 已加载 {len(interactions_data)} 个互动")

    def ask_interactions(self) -> None:
        """询问用户想要的互动"""
        print("\n让我们配置互动系统!")
        print("我会问你一些问题,请根据你的喜好回答。\n")

        # 点击互动
        if self.ask_yes_no("1. 点击宠物时要有反应吗?"):
            self.configure_click_interaction()

        # 双击互动
        if self.ask_yes_no("2. 双击时要有特殊效果吗?"):
            self.configure_doubleclick_interaction()

        # 拖拽
        if self.ask_yes_no("3. 允许拖拽移动宠物吗?"):
            self.configure_drag_interaction()

        # 悬停
        if self.ask_yes_no("4. 鼠标悬停时显示效果吗?"):
            self.configure_hover_interaction()

        # 右键菜单
        if self.ask_yes_no("5. 右键显示菜单吗?"):
            self.configure_rightclick_interaction()

        # 长按
        if self.ask_yes_no("6. 长按时进入睡眠模式吗?"):
            self.configure_longpress_interaction()

    def ask_yes_no(self, question: str) -> bool:
        """询问是/否问题"""
        while True:
            answer = input(f"{question} (y/n): ").strip().lower()
            if answer in ['y', 'yes', '是', 'Y']:
                return True
            elif answer in ['n', 'no', '否', 'N']:
                return False
            print("请输入 y 或 n")

    def ask_choice(self, question: str, options: List[str]) -> int:
        """询问多选一问题"""
        print(f"\n{question}")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")

        while True:
            choice = input(f"\n请选择 (1-{len(options)}): ").strip()
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(options):
                    return idx
            print("无效选择,请重试")

    def configure_click_interaction(self) -> None:
        """配置点击互动"""
        print("\n配置点击互动:")

        actions = ["弹跳", "显示文字", "播放声音", "切换动画"]
        action_idx = self.ask_choice("点击时要做什么?", actions)

        action_map = {
            0: ActionType.BOUNCE.value,
            1: ActionType.SHOW_TEXT.value,
            2: ActionType.PLAY_SOUND.value,
            3: ActionType.CHANGE_ANIMATION.value
        }

        effect_map = {
            0: EffectType.BOUNCE.value,
            1: EffectType.PULSE.value,
            2: EffectType.PULSE.value,
            3: EffectType.FADE.value
        }

        action = action_map[action_idx]
        effect_type = effect_map[action_idx]

        # 创建互动
        params = {}
        if action == ActionType.SHOW_TEXT.value:
            text = input("要显示什么文字? ").strip() or "你好!"
            params = {"text": text, "duration": 2000}

        enable_sound = self.ask_yes_no("要播放声音吗?")
        sound = SoundEffect(
            enabled=enable_sound,
            file="sounds/click.mp3" if enable_sound else None,
            volume=0.5
        )

        interaction = Interaction(
            name="click_interaction",
            trigger=TriggerType.CLICK.value,
            action=action,
            effect=VisualEffect(type=effect_type, duration=400),
            sound=sound,
            feedback=FeedbackConfig(visual=True, message="点击!"),
            params=params
        )

        self.manager.add_interaction(interaction)
        print("✓ 点击互动已配置")

    def configure_doubleclick_interaction(self) -> None:
        """配置双击互动"""
        print("\n配置双击互动:")

        actions = ["旋转", "放大/缩小", "更换皮肤"]
        action_idx = self.ask_choice("双击时要做什么?", actions)

        action_map = {
            0: ActionType.SPIN.value,
            1: ActionType.TOGGLE_FULLSCREEN.value,
            2: ActionType.CHANGE_SKIN.value
        }

        effect_map = {
            0: EffectType.ROTATE.value,
            1: EffectType.SCALE.value,
            2: EffectType.FADE.value
        }

        action = action_map[action_idx]
        effect_type = effect_map[action_idx]

        enable_sound = self.ask_yes_no("要播放声音吗?")
        sound = SoundEffect(
            enabled=enable_sound,
            file="sounds/spin.mp3" if enable_sound else None,
            volume=0.6
        )

        interaction = Interaction(
            name="doubleclick_interaction",
            trigger=TriggerType.DOUBLE_CLICK.value,
            action=action,
            effect=VisualEffect(type=effect_type, duration=500),
            sound=sound,
            feedback=FeedbackConfig(visual=True, message="双击!")
        )

        self.manager.add_interaction(interaction)
        print("✓ 双击互动已配置")

    def configure_drag_interaction(self) -> None:
        """配置拖拽互动"""
        interaction = Interaction(
            name="drag_move",
            trigger=TriggerType.DRAG.value,
            action=ActionType.MOVE_POSITION.value,
            effect=VisualEffect(type=EffectType.NONE.value),
            sound=SoundEffect(enabled=False),
            feedback=FeedbackConfig(visual=False)
        )

        self.manager.add_interaction(interaction)
        print("✓ 拖拽互动已配置")

    def configure_hover_interaction(self) -> None:
        """配置悬停互动"""
        print("\n配置悬停互动:")

        actions = ["发光", "显示提示", "显示文字"]
        action_idx = self.ask_choice("悬停时要做什么?", actions)

        action_map = {
            0: ActionType.GLOW_EFFECT.value,
            1: ActionType.SHOW_TOOLTIP.value,
            2: ActionType.SHOW_TEXT.value
        }

        action = action_map[action_idx]

        params = {}
        if action == ActionType.SHOW_TEXT.value:
            text = input("要显示什么文字? ").strip() or "看什么看?"
            params = {"text": text, "duration": 1500}
        elif action == ActionType.SHOW_TOOLTIP.value:
            text = input("提示内容: ").strip() or "这是提示"
            params = {"text": text}

        interaction = Interaction(
            name="hover_glow",
            trigger=TriggerType.HOVER.value,
            action=action,
            effect=VisualEffect(type=EffectType.GLOW.value, duration=300),
            sound=SoundEffect(enabled=False),
            feedback=FeedbackConfig(visual=True, message="悬停"),
            params=params
        )

        self.manager.add_interaction(interaction)
        print("✓ 悬停互动已配置")

    def configure_rightclick_interaction(self) -> None:
        """配置右键互动"""
        print("\n配置右键菜单:")
        print("默认菜单项: 隐藏、设置、退出")

        custom = self.ask_yes_no("要自定义菜单项吗?")
        menu_items = ["隐藏", "设置", "退出"]

        if custom:
            print("请输入菜单项 (用逗号分隔):")
            items_str = input("> ").strip()
            if items_str:
                menu_items = [item.strip() for item in items_str.split(',')]

        interaction = Interaction(
            name="rightclick_menu",
            trigger=TriggerType.RIGHT_CLICK.value,
            action=ActionType.SHOW_MENU.value,
            effect=VisualEffect(type=EffectType.NONE.value),
            sound=SoundEffect(enabled=True, file="sounds/menu.mp3", volume=0.4),
            feedback=FeedbackConfig(visual=True, message="菜单"),
            params={"menu": menu_items}
        )

        self.manager.add_interaction(interaction)
        print("✓ 右键菜单已配置")

    def configure_longpress_interaction(self) -> None:
        """配置长按互动"""
        interaction = Interaction(
            name="longpress_sleep",
            trigger=TriggerType.LONG_PRESS.value,
            action=ActionType.SLEEP_MODE.value,
            effect=VisualEffect(type=EffectType.FADE.value, duration=800),
            sound=SoundEffect(enabled=True, file="sounds/sleep.mp3", volume=0.3),
            feedback=FeedbackConfig(visual=True, message="晚安...")
        )

        self.manager.add_interaction(interaction)
        print("✓ 长按互动已配置")

    def show_summary(self) -> None:
        """显示配置摘要"""
        print("\n" + "="*60)
        print("   配置摘要")
        print("="*60)

        interactions = self.manager.interactions
        if not interactions:
            print("没有配置任何互动")
            return

        print(f"\n总共配置了 {len(interactions)} 个互动:\n")

        for i, interaction in enumerate(interactions, 1):
            print(f"{i}. {interaction.name}")
            print(f"   触发: {interaction.trigger}")
            print(f"   动作: {interaction.action}")
            print(f"   效果: {interaction.effect.type} ({interaction.effect.duration}ms)")

            if interaction.sound.enabled:
                print(f"   声音: {interaction.sound.file} (音量: {interaction.sound.volume})")

            if interaction.feedback.message:
                print(f"   反馈: {interaction.feedback.message}")

            print()

    def ask_export(self) -> Optional[str]:
        """询问是否导出配置"""
        print("\n你想导出配置吗?")
        print("1. 导出为 JSON 配置文件")
        print("2. 导出为 JavaScript 代码")
        print("3. 两者都导出")
        print("4. 不导出")

        while True:
            choice = input("\n请选择 (1/2/3/4): ").strip()
            if choice in ['1', '2', '3', '4']:
                return choice
            print("无效选择,请输入 1、2、3 或 4")

    def export_config(self, output_dir: str = ".") -> None:
        """导出配置"""
        # 导出 JSON
        config_path = os.path.join(output_dir, "pet_interactions.json")
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(self.manager.export_config(), f, indent=2, ensure_ascii=False)
        print(f"✓ JSON 配置已导出: {config_path}")

    def export_javascript(self, output_dir: str = ".") -> None:
        """导出 JavaScript"""
        js_code = self.manager.generate_javascript()
        js_path = os.path.join(output_dir, "pet_interactions.js")

        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(js_code)

        print(f"✓ JavaScript 代码已导出: {js_path}")

    def run(self) -> None:
        """运行配置向导"""
        self.show_welcome()

        # 选择配置模式
        mode = self.ask_preset_or_custom()

        if mode == '1':  # 使用预设
            preset_key = self.select_preset()
            self.load_preset_interactions(preset_key)

        elif mode == '2':  # 自定义配置
            self.ask_interactions()

        elif mode == '3':  # 混合模式
            preset_key = self.select_preset()
            self.load_preset_interactions(preset_key)
            print("\n现在你可以继续自定义配置...")
            if self.ask_yes_no("要添加更多互动吗?"):
                self.ask_interactions()

        # 显示摘要
        self.show_summary()

        # 询问导出
        export_choice = self.ask_export()

        if export_choice in ['1', '3']:
            output_dir = input("\n输出目录 (留空使用当前目录): ").strip() or "."
            self.export_config(output_dir)

        if export_choice in ['2', '3']:
            output_dir = input("\n输出目录 (留空使用当前目录): ").strip() or "."
            self.export_javascript(output_dir)

        print("\n" + "="*60)
        print("   配置完成!")
        print("="*60)
        print("\n感谢使用桌面宠物互动配置工具!")
        print("祝你的宠物给你带来快乐! 🎉\n")


def main():
    """主函数"""
    ui = InteractionUI()
    ui.run()


if __name__ == "__main__":
    main()
