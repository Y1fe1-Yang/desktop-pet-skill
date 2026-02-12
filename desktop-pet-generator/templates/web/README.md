# 网页版桌面宠物 - 使用说明

## 简介

这是一个单文件网页版的桌面宠物，可以在浏览器中直接运行。

## 使用方法

### 方式一：直接打开

1. 双击 `index.html` 文件
2. 浏览器会自动打开并显示宠物
3. 宠物可以通过鼠标拖拽移动位置
4. 使用右侧控制面板触发不同动画

### 方式二：本地服务器

```bash
# 使用 Python
python -m http.server 8000

# 或使用 Node.js
npx http-server

# 或使用 Live Server (VS Code 插件)
```

然后在浏览器访问 `http://localhost:8000`

## 功能说明

### 基础功能

- **拖拽移动**: 按住宠物并移动鼠标即可拖拽
- **点击交互**: 点击宠物触发特殊交互效果
- **自动动画**: 宠物会每 5 秒自动切换随机动画
- **控制面板**: 手动触发各种动画状态

### 控制面板功能

- **待机**: 宠物进入待机状态
- **走路**: 宠物开始走路动画
- **跳跃**: 宠物跳跃
- **睡觉**: 宠物进入睡眠状态
- **重置位置**: 将宠物移回初始位置（左上角 100, 100）

## 自定义修改

### 修改样式

在 `<style>` 标签中修改 CSS 样式：

```css
.pet-container {
    /* 修改宠物大小、位置等 */
}
```

### 添加新动画

在 JavaScript 部分添加新的动画类型：

```javascript
function triggerAnimation(animationType) {
    pet.className = 'pet-container ' + animationType;
}
```

### 修改自动行为

调整自动动画的间隔时间：

```javascript
setInterval(() => {
    // 修改动画逻辑
}, 5000); // 修改这个数值（毫秒）
```

## 浏览器兼容性

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 注意事项

1. 宠物位置不会保存，刷新页面后会重置
2. 拖拽时不会触发自动动画
3. 控制面板固定在右上角，可以通过修改 CSS 调整位置
4. 建议在全屏模式下使用以获得最佳体验

## 部署到网站

### GitHub Pages

1. 将 `index.html` 上传到 GitHub 仓库
2. 在仓库设置中启用 GitHub Pages
3. 访问 `https://your-username.github.io/repo-name/`

### Netlify

1. 将文件拖拽到 Netlify Drop
2. 获得即时部署的 URL

### Vercel

```bash
npm i -g vercel
vercel
```

## 问题排查

### 宠物不显示

- 检查浏览器控制台是否有错误
- 确认 HTML 结构是否完整
- 检查 CSS 样式是否正确加载

### 拖拽不工作

- 确认鼠标事件监听器已正确绑定
- 检查是否有其他元素遮挡宠物

### 动画不播放

- 检查 CSS 动画定义是否正确
- 确认 JavaScript 中的动画触发逻辑

## 技术栈

- HTML5
- CSS3 (Animations)
- Vanilla JavaScript (ES6+)

## 许可证

MIT License
