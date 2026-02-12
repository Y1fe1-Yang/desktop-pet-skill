# Desktop Pet Generator - 完整教程

本教程将手把手教你从零开始创建一个桌面宠物，并部署到不同平台。

## 目录

1. [前置准备](#前置准备)
2. [创建你的第一个桌宠](#创建你的第一个桌宠)
3. [图片准备与上传](#图片准备与上传)
4. [动画选择与配置](#动画选择与配置)
5. [互动功能设置](#互动功能设置)
6. [本地预览与测试](#本地预览与测试)
7. [部署到各平台](#部署到各平台)
8. [进阶定制](#进阶定制)

---

## 前置准备

### 所需工具

1. **Claude Code CLI**
   ```bash
   # 确保已安装并登录
   claude --version
   ```

2. **Python 环境**（用于图片处理）
   ```bash
   python --version  # 需要 3.8+
   pip install pillow opencv-python
   ```

3. **Node.js 环境**（用于项目构建）
   ```bash
   node --version  # 需要 16+
   npm --version
   ```

4. **图片编辑工具**（可选）
   - Photoshop / GIMP（处理透明背景）
   - 在线工具：remove.bg（自动去背景）

### 准备工作空间

```bash
# 创建工作目录
mkdir ~/desktop-pets
cd ~/desktop-pets
```

---

## 创建你的第一个桌宠

### 步骤 1：启动 Skill

在 Claude Code 中运行：

```bash
/desktop-pet-generator
```

你会看到欢迎信息：

```
欢迎使用桌面宠物生成器！

这个工具将帮助你创建一个可交互的桌面宠物。
支持的平台：网页、浏览器插件、桌面应用

首先，请上传你的宠物图片，或者描述你想要的宠物类型。
支持的格式：PNG, JPG, GIF, WebP
```

### 步骤 2：选择创建方式

有两种方式开始：

**方式 A：上传已有图片**
```
我有一张猫咪的照片，想做成桌面宠物
[拖放图片到对话框]
```

**方式 B：描述生成**
```
我想要一个像素风格的小龙桌面宠物，绿色的，有翅膀
```

---

## 图片准备与上传

### 图片要求

#### 最佳实践
- **格式**：PNG（支持透明背景）
- **尺寸**：200x200 到 500x500 像素
- **背景**：透明或纯色（方便自动抠图）
- **角色**：居中、完整、清晰

#### 示例图片

```
[截图占位：good-pet-image.png]
✓ 好的例子：猫咪居中，透明背景，完整身体

[截图占位：bad-pet-image.png]
✗ 不好的例子：角色被裁切，背景复杂，模糊不清
```

### 上传流程

1. **直接拖放**
   ```
   将图片拖入 Claude Code 对话框
   ```

2. **提供路径**
   ```
   我的图片在 ~/Pictures/my-cat.png
   ```

3. **使用 URL**
   ```
   使用这张图片：https://example.com/cat.png
   ```

### AI 图片分析

上传后，AI 会自动分析：

```
图片分析结果：
- 主体：橙色虎斑猫
- 姿势：坐姿，尾巴向右
- 风格：真实照片
- 背景：白色（建议移除）
- 建议尺寸：300x300px

是否需要我自动处理背景？(Y/n)
```

输入 `Y` 让 AI 自动去除背景并优化图片。

---

## 动画选择与配置

### 可用动画类型

AI 会根据你的图片推荐动画：

```
推荐动画方案：

基础动画（必选至少 1 个）：
1. [待机] 轻微摇晃 - 让宠物看起来"活着"
2. [行走] 左右移动 - 在屏幕上散步

进阶动画（可选）：
3. [跳跃] 向上跳起 - 互动反馈
4. [睡觉] 打瞌睡 - 长时间无操作时
5. [玩耍] 追逐光标 - 有趣的互动
6. [表情] 表情变化 - 增加生动感

自定义动画：
7. [自定义] 描述你想要的动画

请输入动画编号（逗号分隔，如：1,2,3）
```

### 动画配置详解

#### 1. 待机动画（Idle）

```yaml
idle:
  type: "sway"         # 摇晃类型：sway, bounce, breathe
  amplitude: 5         # 摆动幅度（像素）
  duration: 2000       # 周期（毫秒）
  loop: true
```

**效果预览**：
```
[GIF 占位：idle-animation.gif]
```

#### 2. 行走动画（Walk）

```yaml
walk:
  type: "horizontal"   # 方向：horizontal, random, patrol
  speed: 50            # 速度（像素/秒）
  flip: true           # 转向时翻转图片
  boundary: "screen"   # 边界：screen, custom
```

**效果预览**：
```
[GIF 占位：walk-animation.gif]
```

#### 3. 跳跃动画（Jump）

```yaml
jump:
  height: 100          # 跳跃高度（像素）
  duration: 500        # 持续时间（毫秒）
  easing: "ease-out"   # 缓动函数
  sound: true          # 播放音效
```

#### 4. 睡觉动画（Sleep）

```yaml
sleep:
  trigger: "idle_10min"  # 触发条件
  animation: "curl_up"   # 睡姿：curl_up, lie_down
  zzz_bubbles: true      # 显示 ZZZ
  wake_on_click: true    # 点击唤醒
```

#### 5. 玩耍动画（Play）

```yaml
play:
  trigger: "random"      # 触发：random, hover, click
  type: "chase_cursor"   # 玩耍类型
  duration: 5000
  probability: 0.1       # 随机触发概率
```

### 选择建议

**简单桌宠**（新手推荐）：
```
选择：1（待机）+ 2（行走）
时间：5 分钟
效果：基础但完整的桌宠
```

**标准桌宠**（推荐）：
```
选择：1, 2, 3, 4
时间：10 分钟
效果：丰富的动画和互动
```

**豪华桌宠**（进阶）：
```
选择：全选 + 自定义
时间：20+ 分钟
效果：高度定制的个性桌宠
```

---

## 互动功能设置

### 互动事件类型

```
配置互动行为：

鼠标事件：
1. [点击] 点击宠物时触发
2. [悬停] 鼠标悬停时触发
3. [拖拽] 拖动宠物位置

键盘事件：
4. [快捷键] 自定义快捷键（如 Ctrl+Shift+P）

自动事件：
5. [定时] 每隔一段时间随机行为
6. [空闲] 长时间无操作时
7. [系统] 响应系统事件（时间、天气等）

请选择要配置的事件（逗号分隔）：
```

### 点击事件配置

```yaml
onClick:
  actions:
    - animation: "jump"
      probability: 0.5
      sound: "meow"

    - animation: "rotate"
      probability: 0.3
      degrees: 360

    - speech: "喵~"
      probability: 0.2
      duration: 2000
```

**效果**：
- 50% 概率跳跃并喵叫
- 30% 概率原地旋转
- 20% 概率显示对话气泡

### 对话系统

```yaml
speech:
  enabled: true
  bubbles:
    - text: "你好呀！"
      trigger: "click"
    - text: "我饿了..."
      trigger: "idle_30min"
    - text: "该休息了~"
      trigger: "night"

  style:
    font: "Comic Sans MS"
    color: "#333"
    background: "#fff"
    border_radius: 10
```

**示例对话**：
```
[截图占位：speech-bubble.png]
```

### 随机行为

```yaml
randomBehavior:
  enabled: true
  interval: [30000, 60000]  # 30-60 秒随机
  actions:
    - action: "walk"
      weight: 0.5
    - action: "play"
      weight: 0.3
    - action: "sleep"
      weight: 0.2
```

### 高级互动：系统集成

```yaml
systemIntegration:
  time:
    morning: "stretch"      # 早上伸懒腰
    night: "sleep"          # 晚上睡觉

  weather:
    rainy: "hide"           # 下雨躲起来
    sunny: "play"           # 晴天玩耍

  notifications:
    on_message: "alert"     # 新消息提醒
```

---

## 本地预览与测试

### 生成项目

配置完成后，选择生成：

```
配置完成！正在生成项目...

✓ 图片处理完成
✓ 动画文件生成
✓ 配置文件创建
✓ 项目文件生成

项目位置：~/desktop-pets/my-cat-pet/

接下来：
1. 预览：npm start
2. 构建：npm run build
3. 部署：参考 deployment/ 目录
```

### 本地预览

```bash
cd ~/desktop-pets/my-cat-pet
npm install
npm start
```

浏览器会自动打开：`http://localhost:3000`

```
[截图占位：local-preview.png]
```

### 测试清单

- [ ] 待机动画是否流畅
- [ ] 行走是否正常（不超出屏幕）
- [ ] 点击响应是否灵敏
- [ ] 对话气泡是否显示正确
- [ ] 拖拽功能是否可用
- [ ] 动画切换是否自然
- [ ] 性能是否流畅（CPU 占用）

### 调试技巧

**1. 打开浏览器开发者工具**
```
按 F12 查看控制台
```

**2. 调整动画速度**（用于调试）
```javascript
// 在 pet.js 中添加
window.DEBUG_MODE = true;  // 动画速度 x2
```

**3. 查看碰撞检测**
```javascript
// 显示边界框
pet.showBoundingBox = true;
```

---

## 部署到各平台

### 平台选择

```
选择部署平台：

1. [网页版] 最简单，可嵌入任何网站
   - 优点：无需安装，跨平台
   - 缺点：需要浏览器打开

2. [Chrome 插件] 始终在浏览器中显示
   - 优点：开机自启，方便访问
   - 缺点：仅限 Chrome/Edge

3. [桌面应用] 独立窗口，系统级集成
   - 优点：功能最强，可系统托盘
   - 缺点：需要安装，体积较大

请输入编号（可多选，如：1,2）：
```

### 网页版部署（GitHub Pages）

**详细步骤见**：`deployment/web-deployment.md`

```bash
# 快速部署
npm run build
npm run deploy
```

**结果**：
```
部署成功！
网址：https://yourusername.github.io/my-cat-pet/

嵌入代码：
<iframe src="https://yourusername.github.io/my-cat-pet/"
        width="400" height="400" frameborder="0">
</iframe>
```

### 浏览器插件部署（Chrome）

**详细步骤见**：`deployment/extension-deployment.md`

```bash
# 构建插件
npm run build:extension

# 打包
npm run package:extension
```

**安装测试**：
1. 打开 `chrome://extensions/`
2. 启用"开发者模式"
3. 点击"加载已解压的扩展程序"
4. 选择 `dist/extension` 目录

```
[截图占位：chrome-extension-installed.png]
```

### 桌面应用部署（Electron）

**详细步骤见**：`deployment/desktop-deployment.md`

```bash
# 构建应用
npm run build:desktop

# 打包（Windows）
npm run package:win

# 打包（macOS）
npm run package:mac

# 打包（Linux）
npm run package:linux
```

**安装包位置**：
```
dist/
├── my-cat-pet-1.0.0.exe       # Windows
├── my-cat-pet-1.0.0.dmg       # macOS
└── my-cat-pet-1.0.0.AppImage  # Linux
```

---

## 进阶定制

### 添加自定义动画帧

**步骤 1**：准备动画帧

```
assets/
├── cat-walk-1.png
├── cat-walk-2.png
├── cat-walk-3.png
└── cat-walk-4.png
```

**步骤 2**：编辑 `animations.json`

```json
{
  "walk": {
    "frames": [
      {"sprite": "cat-walk-1.png", "duration": 100},
      {"sprite": "cat-walk-2.png", "duration": 100},
      {"sprite": "cat-walk-3.png", "duration": 100},
      {"sprite": "cat-walk-4.png", "duration": 100}
    ],
    "loop": true,
    "speed": 50
  }
}
```

**步骤 3**：测试

```bash
npm start
```

### 集成音效

**添加音效文件**：

```
assets/sounds/
├── meow.mp3
├── purr.mp3
└── jump.mp3
```

**配置音效**：

```javascript
// 在 pet.js 中
const sounds = {
  meow: new Audio('assets/sounds/meow.mp3'),
  purr: new Audio('assets/sounds/purr.mp3'),
  jump: new Audio('assets/sounds/jump.mp3')
};

// 播放音效
pet.on('click', () => {
  sounds.meow.play();
});
```

### 创建主题变体

**白天模式**：
```css
.pet.theme-light {
  filter: brightness(1.1);
}
```

**夜间模式**：
```css
.pet.theme-dark {
  filter: brightness(0.8) contrast(1.2);
}
```

**自动切换**：
```javascript
function updateTheme() {
  const hour = new Date().getHours();
  const theme = (hour >= 6 && hour < 18) ? 'light' : 'dark';
  pet.classList.add(`theme-${theme}`);
}
```

### 添加特殊效果

**粒子效果**（点击时）：

```javascript
function createParticles(x, y) {
  for (let i = 0; i < 10; i++) {
    const particle = document.createElement('div');
    particle.className = 'particle';
    particle.style.left = x + 'px';
    particle.style.top = y + 'px';
    document.body.appendChild(particle);

    setTimeout(() => particle.remove(), 1000);
  }
}
```

**轨迹效果**（移动时）：

```javascript
function drawTrail(x, y) {
  const trail = document.createElement('div');
  trail.className = 'trail';
  trail.style.left = x + 'px';
  trail.style.top = y + 'px';
  document.body.appendChild(trail);

  setTimeout(() => {
    trail.style.opacity = '0';
    setTimeout(() => trail.remove(), 500);
  }, 100);
}
```

---

## 常见问题解决

### 问题 1：动画不流畅

**原因**：图片太大或帧率太高

**解决**：
```bash
# 优化图片
python scripts/optimize_images.py --input assets/ --output assets-optimized/

# 降低帧率
# 在 animations.json 中增加 duration 值
```

### 问题 2：宠物超出屏幕

**原因**：边界检测未配置

**解决**：
```javascript
// 在 pet.js 中添加
function constrainToScreen() {
  const rect = pet.getBoundingClientRect();
  if (rect.left < 0) pet.x = 0;
  if (rect.right > window.innerWidth) {
    pet.x = window.innerWidth - rect.width;
  }
  // 类似地处理 top 和 bottom
}
```

### 问题 3：点击无响应

**原因**：z-index 层级问题

**解决**：
```css
.pet {
  z-index: 9999;
  pointer-events: auto;
}
```

### 问题 4：部署后路径错误

**原因**：相对路径配置不正确

**解决**：
```javascript
// 使用绝对路径
const basePath = window.location.origin + '/my-cat-pet/';
const spritePath = basePath + 'assets/cat.png';
```

---

## 下一步

完成教程后，你可以：

1. **查看示例**：阅读 `EXAMPLES.md` 获取更多创意
2. **学习 API**：阅读 `API.md` 深入了解技术细节
3. **分享作品**：在社区展示你的桌宠
4. **贡献代码**：改进模板和功能

---

**恭喜你完成教程！开始创建你的专属桌面宠物吧！**

需要帮助？参考：
- [README.md](README.md) - 快速参考
- [API.md](API.md) - 技术文档
- [EXAMPLES.md](EXAMPLES.md) - 灵感来源
