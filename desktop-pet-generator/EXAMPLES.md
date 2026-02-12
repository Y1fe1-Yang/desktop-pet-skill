# Desktop Pet Generator - 完整示例

本文档提供 5 个从零到部署的完整示例，涵盖不同风格和使用场景。

## 目录

1. [示例 1：经典猫咪桌宠](#示例-1经典猫咪桌宠)
2. [示例 2：互动型柴犬助手](#示例-2互动型柴犬助手)
3. [示例 3：幻想风格龙宠物](#示例-3幻想风格龙宠物)
4. [示例 4：科技风机器人伙伴](#示例-4科技风机器人伙伴)
5. [示例 5：可爱企鹅管家](#示例-5可爱企鹅管家)
6. [常见问题解决方案](#常见问题解决方案)

---

## 示例 1：经典猫咪桌宠

**适合场景**：个人博客、网站装饰、入门学习

### 概述

创建一只橙色虎斑猫桌宠，具有基础待机和行走动画，点击时会喵叫。

### 第 1 步：准备图片

**图片要求**:
- 格式：PNG
- 尺寸：300x300px
- 背景：透明
- 姿势：坐姿，面向前方

```
[占位图：cat-sitting.png]
```

如果背景不透明，可以使用在线工具 [remove.bg](https://remove.bg) 自动去除。

### 第 2 步：启动生成器

```bash
/desktop-pet-generator
```

对话流程：

```
助手: 欢迎使用桌面宠物生成器！请上传你的宠物图片。

用户: [上传 cat-sitting.png]

助手: 已分析图片：
- 主体：橙色虎斑猫
- 尺寸：300x300px
- 背景：透明 ✓
- 复杂度：中等
- 建议模式：CSS 动画

推荐动画：
1. 待机 - 轻微摇晃
2. 行走 - 左右移动
3. 睡觉 - 打瞌睡
4. 互动 - 点击响应

请选择动画（输入编号）：
```

### 第 3 步：选择动画

```
用户: 1,2,4

助手: 已选择 3 种动画。配置互动行为：
- 点击猫咪时做什么？
  a) 喵叫 + 弹跳
  b) 旋转
  c) 显示对话
  d) 自定义

用户: a
```

### 第 4 步：选择部署平台

```
助手: 选择部署平台：
1. 网页版（GitHub Pages）
2. Chrome 插件
3. Electron 桌面应用

用户: 1

助手: 正在生成网页版桌宠...
✓ 图片处理完成
✓ 动画配置生成
✓ 互动系统创建
✓ 项目文件生成

项目位置：~/desktop-pets/orange-cat/
```

### 第 5 步：本地预览

```bash
cd ~/desktop-pets/orange-cat
npm install
npm start
```

浏览器打开 `http://localhost:3000`，你会看到：

```
[占位图：cat-pet-preview.png]
```

测试要点：
- [ ] 猫咪轻微上下浮动（待机动画）
- [ ] 每隔一段时间左右移动（行走动画）
- [ ] 点击时弹跳并播放喵叫声
- [ ] 可以拖拽移动位置

### 第 6 步：部署到 GitHub Pages

```bash
# 构建
npm run build

# 部署
npm run deploy
```

完成后访问：`https://<your-username>.github.io/orange-cat/`

### 完整配置文件

**animations.json**:
```json
{
  "mode": "css",
  "default": "float",
  "animations": {
    "float": {
      "duration": "3s",
      "timing": "ease-in-out",
      "loop": true
    },
    "walk": {
      "duration": "10s",
      "timing": "linear",
      "loop": true,
      "alternate": true
    },
    "onClick": {
      "duration": "0.5s",
      "timing": "ease"
    }
  }
}
```

**interactions.json**:
```json
{
  "interactions": [
    {
      "name": "click_meow",
      "trigger": "click",
      "action": "bounce",
      "effect": {
        "type": "bounce",
        "duration": 400
      },
      "sound": {
        "enabled": true,
        "file": "sounds/meow.mp3",
        "volume": 0.7
      },
      "feedback": {
        "message": "喵~"
      }
    }
  ]
}
```

### 自定义建议

**添加更多音效**:
```javascript
// 在 pet.js 中添加随机喵叫
const meowSounds = ['meow1.mp3', 'meow2.mp3', 'meow3.mp3'];
const randomSound = meowSounds[Math.floor(Math.random() * meowSounds.length)];
```

**调整行走速度**:
```css
/* 在 styles.css 中 */
@keyframes walk {
    0% { left: 0%; }
    100% { left: 80%; }
}
/* 修改 duration 来调整速度 */
.pet { animation: walk 15s linear infinite alternate; }
```

---

## 示例 2：互动型柴犬助手

**适合场景**：生产力工具、编程伴侣、状态提醒

### 概述

创建一只柴犬桌宠，能够感知你的工作状态（打字、空闲、完成任务），并给予反馈。

### 特殊功能

- 检测打字活动 → 显示"努力工作中"动画
- 检测空闲 10 分钟 → 提醒休息
- 任务完成时 → 庆祝动画
- 右键菜单 → 快速设置

### 第 1 步：准备图片

使用柴犬坐姿图片（推荐像素风格）。

```
[占位图：shiba-pixel.png]
```

### 第 2 步：生成项目

```
用户: /desktop-pet-generator

助手: 请上传图片。

用户: [上传 shiba-pixel.png] 我想要一个能感知工作状态的桌宠

助手: 检测到"工作状态感知"需求。推荐以下功能：
- 打字检测
- 空闲提醒
- 完成庆祝
- 专注模式

是否启用？(Y/n)

用户: Y

助手: 选择动画：
1. 待机
2. 打字（工作中）
3. 睡觉（空闲）
4. 庆祝（完成）
5. 思考

全选推荐？(Y/n)

用户: Y
```

### 第 3 步：配置工作状态检测

生成的 `pet.js` 包含以下逻辑：

```javascript
class WorkAwarePet extends PetInteractionSystem {
  constructor(petElement) {
    super(petElement);
    this.workState = 'idle';
    this.lastActivity = Date.now();
    this.setupWorkTracking();
  }

  setupWorkTracking() {
    // 检测打字
    document.addEventListener('keydown', () => {
      this.workState = 'coding';
      this.lastActivity = Date.now();
      this.pet.classList.add('coding');
      this.pet.classList.remove('idle', 'sleeping');
    });

    // 检测空闲
    setInterval(() => {
      const idleTime = Date.now() - this.lastActivity;

      if (idleTime > 10 * 60 * 1000) { // 10 分钟
        this.workState = 'sleeping';
        this.pet.classList.add('sleeping');
        this.showText('该休息啦~ 🌙', 5000);
      } else if (idleTime > 1000) {
        this.workState = 'idle';
        this.pet.classList.remove('coding');
        this.pet.classList.add('idle');
      }
    }, 5000);

    // 检测鼠标活动
    document.addEventListener('mousemove', () => {
      this.lastActivity = Date.now();
    });
  }

  // 外部调用：标记任务完成
  markTaskComplete() {
    this.pet.classList.add('complete');
    this.showText('干得好！🎉', 3000);
    setTimeout(() => {
      this.pet.classList.remove('complete');
    }, 2000);
  }
}
```

### 第 4 步：集成到工作流

**VS Code 集成示例**:

创建 VS Code 插件钩子：

```javascript
// vscode-extension.js
const vscode = require('vscode');

function activate(context) {
  // 监听任务完成
  vscode.tasks.onDidEndTask((e) => {
    if (e.execution.task.name === 'build' && !e.execution.task.isBackground) {
      // 通知桌宠
      fetch('http://localhost:3000/api/task-complete', {
        method: 'POST',
        body: JSON.stringify({ task: 'build' })
      });
    }
  });
}
```

**添加 API 接收端点**:

```javascript
// 在 pet.js 中添加
class WorkAwarePet extends PetInteractionSystem {
  constructor(petElement) {
    super(petElement);
    this.setupAPI();
  }

  setupAPI() {
    // 简易 API（仅用于 localhost）
    if (window.location.hostname === 'localhost') {
      window.addEventListener('message', (event) => {
        if (event.data.action === 'task-complete') {
          this.markTaskComplete();
        }
      });
    }
  }
}
```

### 第 5 步：自定义提醒

编辑 `pet-config.json`：

```json
{
  "reminders": {
    "idle_10min": {
      "enabled": true,
      "message": "休息一下吧~ ☕",
      "animation": "sleeping"
    },
    "idle_30min": {
      "enabled": true,
      "message": "该站起来活动了！🚶",
      "animation": "excited"
    },
    "hourly": {
      "enabled": true,
      "message": "已经过去一小时了 ⏰",
      "animation": "alert"
    }
  },
  "work_sessions": {
    "pomodoro": {
      "enabled": true,
      "work_duration": 25,
      "break_duration": 5
    }
  }
}
```

### 部署建议

推荐部署为 **Chrome 插件**，这样可以：
- 始终显示在浏览器中
- 与 Web 应用集成
- 跨标签页工作

```bash
npm run build:extension
```

---

## 示例 3：幻想风格龙宠物

**适合场景**：游戏风格界面、创意项目、娱乐

### 概述

创建一只会飞的小龙，具有精灵图动画和粒子效果。

### 特色功能

- 精灵图动画（8 帧飞行循环）
- 点击时喷火粒子效果
- 随机飞行路径
- 夜间模式自动变色

### 第 1 步：准备精灵图

需要准备一个精灵表（sprite sheet）：

```
[占位图：dragon-spritesheet.png]
布局：8 帧横向排列，每帧 128x128px
总尺寸：1024x128px
```

### 第 2 步：配置精灵动画

```
用户: /desktop-pet-generator

助手: 上传图片。

用户: [上传 dragon-spritesheet.png] 这是一个精灵表，8 帧

助手: 检测到精灵表格式。分析结果：
- 帧数：8
- 每帧尺寸：128x128px
- 建议模式：Sprite 动画

是否使用精灵动画模式？(Y/n)

用户: Y

助手: 配置精灵动画：
- 飞行动画：8 帧，12 FPS
- 建议添加飞行路径动画

选择飞行模式：
1. 水平飞行
2. 随机路径
3. 圆周飞行
4. 自由飞行

用户: 2
```

### 第 3 步：添加粒子效果

生成后，编辑 `effects.js`：

```javascript
class ParticleEffect {
  constructor(pet) {
    this.pet = pet;
    this.particles = [];
  }

  createFireBreath(x, y) {
    for (let i = 0; i < 20; i++) {
      const particle = {
        x: x,
        y: y,
        vx: Math.random() * 4 - 2,
        vy: Math.random() * 4 - 2,
        life: 1.0,
        size: Math.random() * 10 + 5,
        color: `hsl(${Math.random() * 60}, 100%, 50%)`
      };
      this.particles.push(particle);
    }
    this.animate();
  }

  animate() {
    const canvas = document.getElementById('particle-canvas');
    const ctx = canvas.getContext('2d');

    const update = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      this.particles = this.particles.filter(p => {
        p.x += p.vx;
        p.y += p.vy;
        p.life -= 0.02;
        p.size *= 0.98;

        if (p.life > 0) {
          ctx.globalAlpha = p.life;
          ctx.fillStyle = p.color;
          ctx.beginPath();
          ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
          ctx.fill();
          return true;
        }
        return false;
      });

      if (this.particles.length > 0) {
        requestAnimationFrame(update);
      }
    };

    update();
  }
}

// 使用
const particleEffect = new ParticleEffect(pet);
pet.addEventListener('click', (e) => {
  particleEffect.createFireBreath(e.clientX, e.clientY);
});
```

### 第 4 步：添加 Canvas 层

在 `index.html` 中添加：

```html
<canvas id="particle-canvas"
        style="position: fixed; top: 0; left: 0;
               width: 100%; height: 100%;
               pointer-events: none; z-index: 9998;">
</canvas>
```

### 第 5 步：配置飞行路径

编辑 `pet.js`：

```javascript
class FlyingDragon {
  constructor(pet) {
    this.pet = pet;
    this.waypoints = [];
    this.currentWaypoint = 0;
    this.generateRandomPath();
    this.startFlying();
  }

  generateRandomPath() {
    this.waypoints = [];
    for (let i = 0; i < 5; i++) {
      this.waypoints.push({
        x: Math.random() * (window.innerWidth - 128),
        y: Math.random() * (window.innerHeight - 128)
      });
    }
  }

  startFlying() {
    setInterval(() => {
      const target = this.waypoints[this.currentWaypoint];
      this.flyTo(target.x, target.y);

      this.currentWaypoint = (this.currentWaypoint + 1) % this.waypoints.length;
    }, 5000);
  }

  flyTo(x, y) {
    this.pet.style.transition = 'all 5s ease-in-out';
    this.pet.style.left = x + 'px';
    this.pet.style.top = y + 'px';

    // 翻转方向
    const currentX = parseInt(this.pet.style.left || 0);
    if (x < currentX) {
      this.pet.style.transform = 'scaleX(-1)';
    } else {
      this.pet.style.transform = 'scaleX(1)';
    }
  }
}
```

### 第 6 步：夜间模式

```javascript
function updateThemeBasedOnTime() {
  const hour = new Date().getHours();
  const isNight = hour < 6 || hour > 20;

  if (isNight) {
    document.body.classList.add('night-mode');
    pet.style.filter = 'hue-rotate(30deg) brightness(0.8)';
  } else {
    document.body.classList.remove('night-mode');
    pet.style.filter = 'none';
  }
}

// 每分钟检查一次
setInterval(updateThemeBasedOnTime, 60000);
updateThemeBasedOnTime();
```

### 完整效果

```
[占位 GIF：dragon-pet-demo.gif]
展示：龙飞行路径 + 点击喷火效果
```

---

## 示例 4：科技风机器人伙伴

**适合场景**：技术博客、开发者工具、科技展示

### 概述

像素风格机器人，具有终端输出效果和系统监控功能。

### 特色功能

- LED 指示灯状态显示
- 实时系统监控（CPU、内存）
- 终端风格对话
- Glitch 效果

### 第 1 步：设计机器人

```
[占位图：robot-pixel.png]
特征：
- 像素艺术风格
- LED 眼睛（可变色）
- 天线（带信号动画）
```

### 第 2 步：添加 LED 状态

```css
/* styles.css */
.robot-led {
  position: absolute;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  top: 20px;
  left: 30px;
  background: #00ff00;
  box-shadow: 0 0 10px #00ff00;
  animation: led-pulse 1s infinite;
}

@keyframes led-pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

.robot-led.idle { background: #00ff00; box-shadow: 0 0 10px #00ff00; }
.robot-led.busy { background: #ffff00; box-shadow: 0 0 10px #ffff00; }
.robot-led.error { background: #ff0000; box-shadow: 0 0 10px #ff0000; }
```

```html
<!-- index.html -->
<div class="pet robot">
  <img src="robot-pixel.png" alt="Robot">
  <div class="robot-led idle"></div>
</div>
```

### 第 3 步：系统监控

```javascript
class SystemMonitorRobot {
  constructor(pet) {
    this.pet = pet;
    this.led = pet.querySelector('.robot-led');
    this.startMonitoring();
  }

  async getSystemStats() {
    // 使用 Performance API（浏览器环境）
    const memory = performance.memory;
    const cpuUsage = await this.estimateCPU();

    return {
      memory: {
        used: memory.usedJSHeapSize,
        total: memory.jsHeapSizeLimit,
        percentage: (memory.usedJSHeapSize / memory.jsHeapSizeLimit) * 100
      },
      cpu: cpuUsage
    };
  }

  async estimateCPU() {
    // 简易 CPU 估算
    const start = performance.now();
    for (let i = 0; i < 1000000; i++) {} // 空循环
    const duration = performance.now() - start;

    return Math.min((duration / 10) * 100, 100);
  }

  startMonitoring() {
    setInterval(async () => {
      const stats = await this.getSystemStats();
      this.updateLED(stats);
      this.updateDisplay(stats);
    }, 2000);
  }

  updateLED(stats) {
    this.led.className = 'robot-led';

    if (stats.memory.percentage > 80 || stats.cpu > 80) {
      this.led.classList.add('error');
    } else if (stats.memory.percentage > 50 || stats.cpu > 50) {
      this.led.classList.add('busy');
    } else {
      this.led.classList.add('idle');
    }
  }

  updateDisplay(stats) {
    const display = document.getElementById('system-stats');
    display.innerHTML = `
      <div class="terminal">
        <div>CPU: ${stats.cpu.toFixed(1)}%</div>
        <div>MEM: ${stats.memory.percentage.toFixed(1)}%</div>
        <div>STATUS: ${this.getStatus(stats)}</div>
      </div>
    `;
  }

  getStatus(stats) {
    if (stats.memory.percentage > 80) return 'HIGH_MEM';
    if (stats.cpu > 80) return 'HIGH_CPU';
    return 'OK';
  }
}
```

### 第 4 步：终端风格对话

```javascript
class TerminalSpeech {
  constructor() {
    this.commands = [
      'SYSTEM_CHECK: OK',
      'ANALYZING_CODE...',
      'OPTIMIZING_PERFORMANCE',
      'DETECTING_BUGS...',
      'ALL_TESTS_PASSED'
    ];
  }

  show(text, duration = 3000) {
    const terminal = document.createElement('div');
    terminal.className = 'terminal-speech';
    terminal.innerHTML = `<span class="prompt">$</span> ${text}`;

    document.body.appendChild(terminal);

    // 打字机效果
    this.typewriter(terminal.querySelector('span:last-child'), text);

    setTimeout(() => terminal.remove(), duration);
  }

  typewriter(element, text) {
    let i = 0;
    element.textContent = '';

    const type = () => {
      if (i < text.length) {
        element.textContent += text.charAt(i);
        i++;
        setTimeout(type, 50);
      }
    };

    type();
  }

  randomCommand() {
    const cmd = this.commands[Math.floor(Math.random() * this.commands.length)];
    this.show(cmd);
  }
}
```

### 第 5 步：Glitch 效果

```css
@keyframes glitch {
  0% {
    transform: translate(0);
  }
  20% {
    transform: translate(-2px, 2px);
  }
  40% {
    transform: translate(-2px, -2px);
  }
  60% {
    transform: translate(2px, 2px);
  }
  80% {
    transform: translate(2px, -2px);
  }
  100% {
    transform: translate(0);
  }
}

.robot.error {
  animation: glitch 0.3s infinite;
}
```

---

## 示例 5：可爱企鹅管家

**适合场景**：任务管理、日程提醒、家庭助手

### 概述

企鹅形象的任务管理助手，可以显示待办事项和日程提醒。

### 特色功能

- 待办清单显示
- 番茄钟计时器
- 日历事件提醒
- 可爱的鼓励话语

### 完整实现

由于篇幅限制，完整代码见项目文件，主要特性：

**任务管理**:
```javascript
class PenguinTaskManager {
  constructor(pet) {
    this.pet = pet;
    this.tasks = this.loadTasks();
    this.renderTasks();
  }

  addTask(task) {
    this.tasks.push({
      id: Date.now(),
      text: task,
      completed: false,
      createdAt: new Date()
    });
    this.saveTasks();
    this.renderTasks();
    this.pet.showEncouragement();
  }

  completeTask(id) {
    const task = this.tasks.find(t => t.id === id);
    if (task) {
      task.completed = true;
      this.saveTasks();
      this.pet.celebrate();
    }
  }
}
```

---

## 常见问题解决方案

### 问题 1：动画卡顿

**症状**: 动画不流畅，掉帧明显

**原因**:
- 图片过大
- 同时运行过多动画
- 使用了非硬件加速的 CSS 属性

**解决方案**:

```bash
# 1. 优化图片
python scripts/optimize_images.py --input assets/ --max-size 300
```

```css
/* 2. 使用硬件加速属性 */
.pet {
  /* 避免使用 */
  /* margin, padding, width, height */

  /* 使用这些 */
  transform: translate(0, 0);
  opacity: 1;
  will-change: transform, opacity;
}
```

```javascript
// 3. 限制动画数量
const MAX_CONCURRENT_ANIMATIONS = 2;
let activeAnimations = 0;

function playAnimation(name) {
  if (activeAnimations >= MAX_CONCURRENT_ANIMATIONS) {
    return;
  }
  activeAnimations++;
  // ... 播放动画
  setTimeout(() => activeAnimations--, duration);
}
```

---

### 问题 2：声音无法播放

**症状**: 点击没有声音，控制台显示播放被阻止

**原因**: 浏览器自动播放策略限制

**解决方案**:

```javascript
// 方案 1：用户首次交互后启用音频
let audioEnabled = false;

document.addEventListener('click', function enableAudio() {
  if (!audioEnabled) {
    const audio = new Audio();
    audio.play().then(() => {
      audioEnabled = true;
      document.removeEventListener('click', enableAudio);
    }).catch(() => {});
  }
}, { once: true });

// 方案 2：提示用户启用音频
function checkAudioPermission() {
  const testAudio = new Audio('sounds/test.mp3');
  testAudio.volume = 0.01;

  testAudio.play().then(() => {
    console.log('Audio enabled');
  }).catch(() => {
    showNotification('点击任意位置启用音效');
  });
}
```

---

### 问题 3：宠物超出屏幕边界

**症状**: 行走时宠物移动到屏幕外

**解决方案**:

```javascript
function constrainToViewport(pet) {
  const rect = pet.getBoundingClientRect();
  const maxX = window.innerWidth - rect.width;
  const maxY = window.innerHeight - rect.height;

  let x = parseInt(pet.style.left) || 0;
  let y = parseInt(pet.style.top) || 0;

  // 限制边界
  x = Math.max(0, Math.min(x, maxX));
  y = Math.max(0, Math.min(y, maxY));

  pet.style.left = x + 'px';
  pet.style.top = y + 'px';
}

// 在移动时调用
setInterval(() => constrainToViewport(pet), 100);

// 窗口调整时调用
window.addEventListener('resize', () => constrainToViewport(pet));
```

---

### 问题 4：Chrome 插件安装失败

**症状**: 加载扩展时显示"Manifest 错误"

**解决方案**:

检查 `manifest.json` 格式：

```json
{
  "manifest_version": 3,
  "name": "My Desktop Pet",
  "version": "1.0.0",
  "description": "A cute desktop pet",
  "action": {
    "default_popup": "popup.html"
  },
  "permissions": [
    "storage"
  ],
  "content_scripts": [
    {
      "matches": ["<all_urls>"],
      "js": ["content.js"],
      "css": ["styles.css"]
    }
  ]
}
```

常见错误：
- `manifest_version` 必须是 3（Chrome）或 2（Firefox）
- `permissions` 数组必须包含所有需要的权限
- 文件路径必须正确

---

### 问题 5：部署后路径 404

**症状**: GitHub Pages 部署后图片和资源加载失败

**解决方案**:

```javascript
// 使用相对路径或动态基础路径
const BASE_PATH = window.location.origin + window.location.pathname.replace(/\/$/, '');

// 加载资源
const imgSrc = `${BASE_PATH}/assets/pet.png`;
const soundSrc = `${BASE_PATH}/sounds/meow.mp3`;
```

或在 `package.json` 中配置：

```json
{
  "homepage": "https://yourusername.github.io/pet-name",
  "scripts": {
    "build": "react-scripts build",
    "predeploy": "npm run build",
    "deploy": "gh-pages -d build"
  }
}
```

---

### 问题 6：内存泄漏

**症状**: 长时间运行后浏览器变慢

**原因**: 未清理的定时器或事件监听器

**解决方案**:

```javascript
class PetSystem {
  constructor(pet) {
    this.pet = pet;
    this.timers = [];
    this.listeners = [];
  }

  addTimer(callback, interval) {
    const timer = setInterval(callback, interval);
    this.timers.push(timer);
    return timer;
  }

  addEventListener(element, event, handler) {
    element.addEventListener(event, handler);
    this.listeners.push({ element, event, handler });
  }

  destroy() {
    // 清理定时器
    this.timers.forEach(timer => clearInterval(timer));
    this.timers = [];

    // 清理事件监听器
    this.listeners.forEach(({ element, event, handler }) => {
      element.removeEventListener(event, handler);
    });
    this.listeners = [];
  }
}

// 使用
const petSystem = new PetSystem(pet);

// 页面卸载时清理
window.addEventListener('beforeunload', () => {
  petSystem.destroy();
});
```

---

## 性能优化技巧

### 1. 图片优化

```bash
# 使用 ImageMagick 压缩
convert input.png -strip -quality 85 output.png

# 或使用 Python 脚本
python scripts/optimize_images.py --quality 85 --max-size 300
```

### 2. CSS 优化

```css
/* 启用 GPU 加速 */
.pet {
  transform: translateZ(0);
  backface-visibility: hidden;
  perspective: 1000px;
}

/* 避免重排 */
.pet {
  position: fixed; /* 而不是 absolute */
}
```

### 3. JavaScript 优化

```javascript
// 使用 requestAnimationFrame
function animate() {
  updatePetPosition();
  requestAnimationFrame(animate);
}
animate();

// 防抖高频事件
const debouncedResize = debounce(() => {
  adjustPetSize();
}, 200);
window.addEventListener('resize', debouncedResize);
```

---

## 更多资源

- **社区示例库**: [查看更多用户创建的桌宠](https://github.com/desktop-pets/gallery)
- **模板市场**: [下载现成的模板](https://desktop-pets.com/templates)
- **视频教程**: [YouTube 教程播放列表](https://youtube.com/...)

---

**现在开始创建你自己的桌面宠物吧！** 如有问题，参考：
- [README.md](README.md) - 快速参考
- [TUTORIAL.md](TUTORIAL.md) - 详细教程
- [API.md](API.md) - 技术文档
