#!/usr/bin/env python3
"""
Animation Builder for Desktop Pet Generator
Provides preset animation library and combination system
"""

import json
from typing import Dict, List, Optional


class AnimationLibrary:
    """Comprehensive animation preset library"""

    # CSS Keyframe animations
    CSS_ANIMATIONS = {
        # Core Idle Animations
        "float": {
            "name": "Float",
            "category": "idle",
            "description": "Gentle up/down hover",
            "css": """
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
}
.pet { animation: float 3s ease-in-out infinite; }
""",
            "duration": "3s",
            "timing": "ease-in-out"
        },

        "breathe": {
            "name": "Breathe",
            "category": "idle",
            "description": "Scale pulsing effect",
            "css": """
@keyframes breathe {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
}
.pet { animation: breathe 2s ease-in-out infinite; }
""",
            "duration": "2s",
            "timing": "ease-in-out"
        },

        "sway": {
            "name": "Sway",
            "category": "idle",
            "description": "Side-to-side movement",
            "css": """
@keyframes sway {
    0%, 100% { transform: rotate(-5deg); }
    50% { transform: rotate(5deg); }
}
.pet { animation: sway 2s ease-in-out infinite; }
""",
            "duration": "2s",
            "timing": "ease-in-out"
        },

        # Movement Animations
        "walk": {
            "name": "Walk",
            "category": "movement",
            "description": "Horizontal walking",
            "css": """
@keyframes walk {
    0% { left: 0%; }
    100% { left: 80%; }
}
.pet { animation: walk 10s linear infinite alternate; }
""",
            "duration": "10s",
            "timing": "linear"
        },

        "jump": {
            "name": "Jump",
            "category": "movement",
            "description": "Vertical bounce",
            "css": """
@keyframes jump {
    0%, 100% { transform: translateY(0); }
    30% { transform: translateY(-50px); }
    60% { transform: translateY(-30px); }
}
.pet { animation: jump 1s ease infinite; }
""",
            "duration": "1s",
            "timing": "ease"
        },

        "fly": {
            "name": "Fly",
            "category": "movement",
            "description": "Floating movement",
            "css": """
@keyframes fly {
    0% { transform: translate(0, 0); }
    25% { transform: translate(50px, -50px); }
    50% { transform: translate(100px, 0); }
    75% { transform: translate(50px, 50px); }
    100% { transform: translate(0, 0); }
}
.pet { animation: fly 8s ease-in-out infinite; }
""",
            "duration": "8s",
            "timing": "ease-in-out"
        },

        # Interactive Animations
        "onClick": {
            "name": "Click Response",
            "category": "interactive",
            "description": "Excited bounce on click",
            "css": """
@keyframes clickBounce {
    0% { transform: scale(1); }
    50% { transform: scale(1.2) rotate(10deg); }
    100% { transform: scale(1) rotate(0deg); }
}
.pet.clicked { animation: clickBounce 0.5s ease; }
""",
            "duration": "0.5s",
            "timing": "ease",
            "trigger": "click"
        },

        "onHover": {
            "name": "Hover Effect",
            "category": "interactive",
            "description": "Scale and glow on hover",
            "css": """
.pet:hover {
    transform: scale(1.15);
    filter: drop-shadow(0 0 20px rgba(255, 255, 100, 0.8));
    transition: all 0.3s ease;
}
""",
            "duration": "0.3s",
            "timing": "ease",
            "trigger": "hover"
        },

        # Emotional Animations
        "happy": {
            "name": "Happy",
            "category": "emotional",
            "description": "Rapid bounce with rotation",
            "css": """
@keyframes happy {
    0%, 100% { transform: translateY(0) rotate(0deg); }
    25% { transform: translateY(-15px) rotate(-5deg); }
    75% { transform: translateY(-15px) rotate(5deg); }
}
.pet.happy { animation: happy 0.5s ease infinite; }
""",
            "duration": "0.5s",
            "timing": "ease"
        },

        "sad": {
            "name": "Sad",
            "category": "emotional",
            "description": "Droop down slowly",
            "css": """
@keyframes sad {
    0% { transform: translateY(0) scale(1); }
    100% { transform: translateY(20px) scale(0.9); opacity: 0.7; }
}
.pet.sad { animation: sad 2s ease forwards; }
""",
            "duration": "2s",
            "timing": "ease"
        },

        "excited": {
            "name": "Excited",
            "category": "emotional",
            "description": "Shake and wiggle",
            "css": """
@keyframes excited {
    0%, 100% { transform: rotate(0deg); }
    25% { transform: rotate(-10deg) translateX(-5px); }
    75% { transform: rotate(10deg) translateX(5px); }
}
.pet.excited { animation: excited 0.3s ease infinite; }
""",
            "duration": "0.3s",
            "timing": "ease"
        },

        "sleep": {
            "name": "Sleep",
            "category": "emotional",
            "description": "Slow fade and droop",
            "css": """
@keyframes sleep {
    0% { opacity: 1; transform: rotate(0deg); }
    100% { opacity: 0.5; transform: rotate(-30deg) translateY(10px); }
}
.pet.sleep { animation: sleep 3s ease forwards; }
""",
            "duration": "3s",
            "timing": "ease"
        },

        # Work Status Animations
        "coding": {
            "name": "Coding",
            "category": "work",
            "description": "Typing animation effect",
            "css": """
@keyframes coding {
    0%, 100% { transform: translateX(0); }
    10% { transform: translateX(-2px); }
    20% { transform: translateX(2px); }
    30% { transform: translateX(-2px); }
    40% { transform: translateX(2px); }
    50% { transform: translateX(0); }
}
.pet.coding { animation: coding 0.8s ease infinite; }
""",
            "duration": "0.8s",
            "timing": "ease"
        },

        "thinking": {
            "name": "Thinking",
            "category": "work",
            "description": "Contemplative movement",
            "css": """
@keyframes thinking {
    0%, 100% { transform: rotate(-3deg); }
    50% { transform: rotate(3deg); }
}
.pet.thinking { animation: thinking 1.5s ease-in-out infinite; }
""",
            "duration": "1.5s",
            "timing": "ease-in-out"
        },

        "complete": {
            "name": "Complete",
            "category": "work",
            "description": "Success celebration",
            "css": """
@keyframes complete {
    0% { transform: scale(1) rotate(0deg); }
    25% { transform: scale(1.3) rotate(10deg); }
    50% { transform: scale(1.2) rotate(-10deg); }
    75% { transform: scale(1.3) rotate(10deg); }
    100% { transform: scale(1) rotate(0deg); }
}
.pet.complete { animation: complete 0.8s ease; }
""",
            "duration": "0.8s",
            "timing": "ease"
        },

        "error": {
            "name": "Error",
            "category": "work",
            "description": "Alert shake",
            "css": """
@keyframes error {
    0%, 100% { transform: translateX(0); }
    10%, 30%, 50%, 70%, 90% { transform: translateX(-10px); }
    20%, 40%, 60%, 80% { transform: translateX(10px); }
}
.pet.error { animation: error 0.6s ease; }
""",
            "duration": "0.6s",
            "timing": "ease"
        }
    }

    # Sprite-based animation configurations
    SPRITE_ANIMATIONS = {
        "walk_sprite": {
            "name": "Walk (Sprite)",
            "category": "movement",
            "frames": 8,
            "fps": 12,
            "loop": True,
            "description": "8-frame walking cycle"
        },
        "jump_sprite": {
            "name": "Jump (Sprite)",
            "category": "movement",
            "frames": 6,
            "fps": 15,
            "loop": False,
            "description": "6-frame jump sequence"
        },
        "idle_sprite": {
            "name": "Idle (Sprite)",
            "category": "idle",
            "frames": 4,
            "fps": 8,
            "loop": True,
            "description": "4-frame breathing/idle"
        },
        "attack_sprite": {
            "name": "Attack (Sprite)",
            "category": "interactive",
            "frames": 10,
            "fps": 20,
            "loop": False,
            "description": "10-frame attack animation"
        }
    }

    @classmethod
    def get_animation(cls, name: str, mode: str = "css") -> Optional[Dict]:
        """Get specific animation by name"""
        if mode == "css":
            return cls.CSS_ANIMATIONS.get(name)
        else:
            return cls.SPRITE_ANIMATIONS.get(name)

    @classmethod
    def get_by_category(cls, category: str, mode: str = "css") -> Dict[str, Dict]:
        """Get all animations in a category"""
        animations = cls.CSS_ANIMATIONS if mode == "css" else cls.SPRITE_ANIMATIONS
        return {
            name: anim for name, anim in animations.items()
            if anim.get("category") == category
        }

    @classmethod
    def get_default_set(cls, mode: str = "css") -> List[str]:
        """Get default recommended animation set"""
        if mode == "css":
            return ["float", "walk", "onClick"]
        else:
            return ["idle_sprite", "walk_sprite", "jump_sprite"]

    @classmethod
    def list_all(cls, mode: str = "css") -> Dict[str, List[str]]:
        """List all animations grouped by category"""
        animations = cls.CSS_ANIMATIONS if mode == "css" else cls.SPRITE_ANIMATIONS

        categories = {}
        for name, anim in animations.items():
            cat = anim.get("category", "other")
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(name)

        return categories


class AnimationBuilder:
    """Builds animation code for pets"""

    def __init__(self, mode: str = "css"):
        self.mode = mode
        self.animations = []
        self.library = AnimationLibrary()

    def add_animation(self, name: str):
        """Add animation to the build"""
        anim = self.library.get_animation(name, self.mode)
        if anim:
            self.animations.append((name, anim))
        else:
            raise ValueError(f"Animation '{name}' not found in {self.mode} mode")

    def add_multiple(self, names: List[str]):
        """Add multiple animations"""
        for name in names:
            self.add_animation(name)

    def generate_css(self) -> str:
        """Generate combined CSS for all added animations"""
        if self.mode != "css":
            raise ValueError("CSS generation only available in CSS mode")

        css_parts = []

        # Add all keyframes
        for name, anim in self.animations:
            if "css" in anim:
                css_parts.append(f"/* {anim['name']} - {anim['description']} */")
                css_parts.append(anim["css"])
                css_parts.append("")

        return "\n".join(css_parts)

    def generate_sprite_config(self) -> Dict:
        """Generate sprite animation configuration"""
        if self.mode != "sprite":
            raise ValueError("Sprite config only available in sprite mode")

        config = {
            "animations": {},
            "default": self.animations[0][0] if self.animations else "idle_sprite"
        }

        for name, anim in self.animations:
            config["animations"][name] = {
                "frames": anim["frames"],
                "fps": anim["fps"],
                "loop": anim["loop"]
            }

        return config

    def generate_javascript(self, interactions: List[str]) -> str:
        """Generate JavaScript for interactions"""
        js_parts = [
            "// Pet animation controller",
            "const pet = document.querySelector('.pet');",
            ""
        ]

        # Add click interaction
        if "clickable" in interactions:
            js_parts.extend([
                "// Click interaction",
                "pet.addEventListener('click', () => {",
                "    pet.classList.add('clicked');",
                "    setTimeout(() => pet.classList.remove('clicked'), 500);",
                "});",
                ""
            ])

        # Add draggable interaction
        if "draggable" in interactions:
            js_parts.extend([
                "// Draggable interaction",
                "let isDragging = false;",
                "let offsetX, offsetY;",
                "",
                "pet.addEventListener('mousedown', (e) => {",
                "    isDragging = true;",
                "    offsetX = e.clientX - pet.offsetLeft;",
                "    offsetY = e.clientY - pet.offsetTop;",
                "    pet.style.cursor = 'grabbing';",
                "});",
                "",
                "document.addEventListener('mousemove', (e) => {",
                "    if (isDragging) {",
                "        pet.style.left = (e.clientX - offsetX) + 'px';",
                "        pet.style.top = (e.clientY - offsetY) + 'px';",
                "    }",
                "});",
                "",
                "document.addEventListener('mouseup', () => {",
                "    isDragging = false;",
                "    pet.style.cursor = 'grab';",
                "});",
                ""
            ])

        # Add status-aware behavior
        if "status_aware" in interactions:
            js_parts.extend([
                "// Status-aware animations",
                "let idleTimeout;",
                "",
                "// Detect typing",
                "document.addEventListener('keydown', () => {",
                "    pet.classList.add('coding');",
                "    clearTimeout(idleTimeout);",
                "    idleTimeout = setTimeout(() => {",
                "        pet.classList.remove('coding');",
                "    }, 3000);",
                "});",
                "",
                "// Detect idle",
                "let lastActivity = Date.now();",
                "setInterval(() => {",
                "    if (Date.now() - lastActivity > 60000) {",
                "        pet.classList.add('sleep');",
                "    } else {",
                "        pet.classList.remove('sleep');",
                "    }",
                "}, 5000);",
                "",
                "document.addEventListener('mousemove', () => {",
                "    lastActivity = Date.now();",
                "});",
                ""
            ])

        return "\n".join(js_parts)

    def get_summary(self) -> Dict:
        """Get summary of all added animations"""
        return {
            "mode": self.mode,
            "count": len(self.animations),
            "animations": [
                {
                    "name": name,
                    "display_name": anim["name"],
                    "category": anim.get("category", "other"),
                    "description": anim["description"]
                }
                for name, anim in self.animations
            ]
        }


def main():
    """CLI entry point for testing"""
    import sys

    if len(sys.argv) < 3:
        print("Usage: python animation_builder.py <mode> <animation1,animation2,...>")
        print("\nAvailable CSS animations:")
        for cat, anims in AnimationLibrary.list_all("css").items():
            print(f"  {cat}: {', '.join(anims)}")
        print("\nAvailable Sprite animations:")
        for cat, anims in AnimationLibrary.list_all("sprite").items():
            print(f"  {cat}: {', '.join(anims)}")
        sys.exit(1)

    mode = sys.argv[1]
    animations = sys.argv[2].split(",")

    builder = AnimationBuilder(mode)
    builder.add_multiple(animations)

    print(json.dumps(builder.get_summary(), indent=2))

    if mode == "css":
        print("\n--- Generated CSS ---")
        print(builder.generate_css())
    else:
        print("\n--- Generated Sprite Config ---")
        print(json.dumps(builder.generate_sprite_config(), indent=2))


if __name__ == "__main__":
    main()
