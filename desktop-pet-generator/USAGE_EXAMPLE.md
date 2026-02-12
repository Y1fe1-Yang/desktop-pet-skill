# Desktop Pet Generator - 使用示例

## 完整对话示例

### 示例 1：从猫咪照片创建桌面宠物

```
用户: 我想创建一个桌面宠物
      [上传 cat.jpg]

Claude: 欢迎使用桌面宠物生成器！🎨

我已经分析了你的图片：
- 类型：猫咪
- 主色调：橙色 (#F4A460)
- 尺寸：800x600px
- 透明背景：否

让我们开始创建你的专属桌宠！

**步骤 1/5：选择生成模式**

你想用哪种方式生成桌宠？

1️⃣ **CSS 模式** (推荐)
   ✅ 简单轻量
   ✅ 纯代码实现
   ✅ 易于定制
   适合：简化风格、卡通形象

2️⃣ **Sprite 模式** (高级)
   ✅ 精确还原
   ✅ 复杂动画
   ✅ 帧控制
   适合：详细图片、多帧动画

请选择：1 或 2

用户: 1

Claude: 太好了！CSS 模式非常适合你的猫咪。

**步骤 2/5：选择动画效果**

我为你准备了这些动画：

**基础动画** (推荐全选)
✓ 1. idle - 空闲摇晃
✓ 2. working - 工作跳动
✓ 3. completed - 完成庆祝

**情感动画**
□ 4. happy - 开心跳跃
□ 5. sleep - 睡觉打盹
□ 6. excited - 兴奋转圈

**互动动画**
□ 7. click - 点击反应
□ 8. hover - 悬停发光
□ 9. drag - 拖拽跟随

输入数字选择（用逗号分隔），或输入 "all" 全选：

用户: 1,2,3,7,8

Claude: 完美的选择！✨

**步骤 3/5：配置互动行为**

你想让桌宠支持哪些互动？

□ 1. 点击响应 - 点击时播放动画和声音
□ 2. 拖拽移动 - 可以拖动宠物到任意位置
□ 3. 悬停效果 - 鼠标悬停时发光
□ 4. 右键菜单 - 显示选项菜单
□ 5. 双击特效 - 双击触发特殊动画
□ 6. 状态感知 - 监听工作状态（需要 Claude Code）

选择互动类型（数字，逗号分隔）：

用户: 1,2,3,6

Claude: 很好！你的桌宠会很智能！🤖

**步骤 4/5：个性化设置**

让我们设置一些细节：

🎯 宠物名称: _______
📏 大小: 小(100px) / 中(200px) / 大(300px)
📍 默认位置: 右下角 / 左下角 / 右上角 / 左上角
⚡ 动画速度: 慢 / 中 / 快

输入设置（或输入 "default" 使用默认值）：

用户: 名称：橘猫, 大小：200px, 位置：右下角, 速度：中

Claude: 完美！🎨

**步骤 5/5：选择部署方式**

最后一步！你想怎么使用你的桌宠？

1️⃣ **网页版** (最简单)
   - 单个 HTML 文件
   - 直接在浏览器打开
   - 可部署到 GitHub Pages
   推荐：快速预览、网站装饰

2️⃣ **浏览器插件** (Chrome/Firefox)
   - 安装到浏览器
   - 随时显示/隐藏
   - 跨网页使用
   推荐：日常陪伴

3️⃣ **桌面应用** (Electron)
   - 独立应用程序
   - 悬浮在桌面
   - 完整功能支持
   推荐：专业开发者

选择部署方式 (1-3):

用户: 1

Claude: 🎉 正在生成你的桌面宠物...

📸 分析图片... ✓
✨ 生成动画 (5个)... ✓
🎮 配置互动 (4个)... ✓
📦 打包网页版... ✓
📝 生成文档... ✓

✅ **桌宠生成完成！**

输出目录：`/output/web/`

📁 生成的文件：
- index.html (完整的桌宠页面)
- pet-image.png (你的猫咪图片)
- README.md (使用说明)

🚀 **快速预览**：
1. 打开 output/web/index.html
2. 你的橘猫就会出现在屏幕右下角！

💡 **部署到 GitHub Pages**：
```bash
cd output/web
git init
git add .
git commit -m "Add my desktop pet"
git remote add origin https://github.com/your-username/my-pet.git
git push -u origin main
```

然后在 GitHub 仓库设置中启用 Pages！

🎨 **自定义提示**：
- 修改颜色：编辑 index.html 中的 CSS 变量
- 调整大小：修改 `--pet-size` 变量
- 添加动画：参考 README.md 中的动画库

需要其他部署方式吗？我可以再生成插件或桌面应用版本！
```

---

## 示例 2：创建工作助手桌宠

```
用户: 创建一个监听 Claude Code 状态的桌宠

Claude: 太棒了！我帮你创建一个智能工作助手桌宠！

请上传桌宠的图片，或者我可以用默认的机器人形象。

用户: 用默认机器人

Claude: 好的！使用默认机器人形象。🤖

**快速配置（工作助手预设）**

我为工作助手准备了专门配置：

✓ 动画：
  - idle (待机)
  - working (工作中 - 打字动画)
  - completed (完成 - 庆祝动画)
  - error (错误 - 抖动提示)
  - thinking (思考 - 问号动画)

✓ 互动：
  - 状态感知（监听 Claude Code）
  - 点击响应
  - 拖拽定位

✓ 设置：
  - 名称：CodeBot
  - 大小：150px
  - 位置：右下角
  - 速度：快速

这个配置适合你吗？(y/n 或自定义)

用户: y

Claude: 🚀 正在生成工作助手桌宠...

由于你选择了"状态感知"，我推荐使用 **桌面应用** 部署方式，
这样才能监听 Claude Code 的工作状态。

是否生成桌面应用？(y/n)

用户: y

Claude: ✅ 生成完成！

你的 CodeBot 已准备就绪！

📁 输出目录：`/output/desktop/`

🎯 **功能说明**：

当你使用 Claude Code 时，CodeBot 会：
- 🟢 Claude 空闲 → CodeBot 平静待机
- 🔵 Claude 工作中 → CodeBot 打字动画
- ✅ 任务完成 → CodeBot 庆祝跳跃
- ❌ 出现错误 → CodeBot 抖动提示

🚀 **运行方式**：

1. 进入目录：
   ```bash
   cd /output/desktop
   ```

2. 安装依赖：
   ```bash
   npm install
   ```

3. 启动应用：
   ```bash
   npm start
   ```

4. 构建安装包：
   ```bash
   npm run build
   # 生成的应用在 dist/ 目录
   ```

💡 **提示**：
- CodeBot 会自动监听 `~/.claude/sessions/` 目录
- 确保 Claude Code 正在运行
- CodeBot 完全本地运行，保护你的隐私

享受你的智能工作伙伴吧！🎉
```

---

## 示例 3：创建浏览器插件

```
用户: 我想要一个浏览器插件版的桌宠

Claude: 好主意！浏览器插件桌宠可以在你浏览网页时随时陪伴你！

上传你的宠物图片吧！

用户: [上传 dog.png]

Claude: 收到！分析中...

检测到：
- 可爱的柴犬 🐕
- 主色调：棕色、白色
- 图片清晰，适合制作插件

使用快速模式？预设包括：
- 基础动画（待机、行走、坐下）
- 点击互动
- 浏览器插件优化

(y/n)

用户: y

Claude: ⚡ 快速生成中...

✅ 插件生成完成！

📦 输出：`/output/extension/`

📋 **安装步骤**：

**Chrome / Edge**：
1. 打开 `chrome://extensions/`
2. 开启"开发者模式"
3. 点击"加载已解压的扩展程序"
4. 选择 `/output/extension/` 文件夹
5. 完成！柴犬会出现在右下角

**Firefox**：
1. 打开 `about:debugging#/runtime/this-firefox`
2. 点击"临时载入附加组件"
3. 选择 `/output/extension/manifest.json`
4. 完成！

🎮 **使用方式**：
- 点击浏览器工具栏的图标显示/隐藏
- 右键菜单设置位置和大小
- 在任何网页都能看到你的柴犬

📢 **发布到商店**：
参考 `/output/extension/PUBLISH.md` 了解如何发布到：
- Chrome Web Store
- Firefox Add-ons
- Edge Add-ons

你的柴犬插件已经可以用了！🐕
```

---

## 命令行使用

如果你更喜欢命令行：

```bash
# 使用配置文件生成
python scripts/pet_generator.py --config my-config.json

# 使用命令行参数
python scripts/pet_generator.py \
  --image cat.png \
  --name "橘猫" \
  --mode css \
  --deployment html \
  --output ./my-pet

# 查看帮助
python scripts/pet_generator.py --help
```

配置文件示例 (config.json)：

```json
{
  "name": "MyPet",
  "mode": "css",
  "image_path": "./cat.png",
  "size": "200px",
  "animations": ["idle", "working", "completed", "click"],
  "interactions": ["clickable", "draggable", "status_aware"],
  "deployment": "html",
  "output_dir": "./output",
  "position": "bottom-right",
  "speed": "medium"
}
```

---

## 预设模板

快速开始使用预设：

```
用户: 用"可爱助手"预设创建桌宠

Claude: 使用"可爱助手"预设 ✨

配置：
- 风格：可爱卡通
- 动画：idle, happy, excited, sleep
- 互动：点击、拖拽、双击
- 部署：网页版

[直接生成，跳过配置步骤]
```

可用预设：
- `可爱助手` - 卡通风格，适合装饰
- `工作伙伴` - 监听工作状态，专业风格
- `极简宠物` - 最小配置，快速生成
- `全功能` - 包含所有动画和互动

---

## 常见问题

**Q: 可以用 GIF 动图吗？**
A: 可以！使用 Sprite 模式，GIF 会被拆分成帧。

**Q: 桌宠会占用很多资源吗？**
A: 不会。CSS 动画非常轻量，CPU 占用 < 1%。

**Q: 能否添加声音效果？**
A: 可以！在高级设置中启用音效。

**Q: 支持哪些图片格式？**
A: PNG, JPG, GIF, SVG, WebP 都支持。

**Q: 可以商用吗？**
A: 生成的代码完全属于你，可以自由使用！

---

## 高级技巧

### 1. 组合多个动画

```javascript
// 在生成的 pet.js 中
const animations = ['idle', 'walk', 'jump'];
let current = 0;

setInterval(() => {
  pet.className = animations[current];
  current = (current + 1) % animations.length;
}, 3000);
```

### 2. 添加对话气泡

```javascript
function showMessage(text) {
  const bubble = document.createElement('div');
  bubble.className = 'speech-bubble';
  bubble.textContent = text;
  pet.appendChild(bubble);

  setTimeout(() => bubble.remove(), 3000);
}
```

### 3. 响应键盘事件

```javascript
document.addEventListener('keydown', (e) => {
  if (e.key === 'p') {
    pet.classList.toggle('paused');
  }
});
```

---

享受创建桌宠的乐趣！🎨✨
