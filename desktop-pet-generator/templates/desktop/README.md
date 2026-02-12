# 桌面版宠物 - 构建说明

## 简介

这是一个基于 Electron 的桌面宠物应用，可以在 Windows、macOS 和 Linux 上运行。

## 系统要求

- Node.js 16+
- npm 或 yarn
- 至少 200MB 可用磁盘空间

## 安装依赖

```bash
npm install
```

## 开发运行

```bash
npm start
```

这将启动开发模式，宠物会显示在桌面上，并自动打开开发者工具。

## 构建应用

### 构建所有平台

```bash
npm run build
```

### 构建特定平台

```bash
# macOS
npm run build:mac

# Windows
npm run build:win

# Linux
npm run build:linux
```

构建产物会输出到 `dist/` 目录。

### 打包（不构建安装包）

```bash
npm run pack
```

这会创建一个未打包的应用目录，用于测试。

## 项目结构

```
desktop/
├── main.js              # Electron 主进程
├── renderer.js          # 渲染进程（宠物逻辑）
├── index.html           # 宠物界面
├── package.json         # 项目配置
├── assets/              # 资源文件
│   ├── icon.icns       # macOS 图标
│   ├── icon.ico        # Windows 图标
│   ├── icon.png        # Linux 图标
│   └── tray-icon.png   # 托盘图标
└── README.md           # 本文件
```

## 功能特性

### 基础功能

- **透明窗口**: 宠物背景透明，融入桌面
- **拖拽移动**: 按住宠物拖拽到任意位置
- **置顶显示**: 始终显示在其他窗口之上（可关闭）
- **点击穿透**: 可穿透窗口点击下方内容（可启用）
- **系统托盘**: 最小化到托盘，右键菜单控制

### 交互功能

- **点击交互**: 点击宠物触发特殊效果
- **双击**: 双击触发跳跃动画
- **右键菜单**: 快速访问常用功能
- **自动动画**: 定期自动切换随机动画

### 快捷键

- `Esc`: 退出应用
- `Ctrl/Cmd + R`: 重启应用
- `Space`: 触发随机动画

### 系统托盘菜单

- 显示/隐藏宠物
- 置顶开关
- 点击穿透开关
- 重置位置
- 退出应用

## 自定义开发

### 修改宠物外观

编辑 `renderer.js` 中的 HTML 模板：

```javascript
petContainer.innerHTML = `
    <div class="pet">
        <!-- 自定义 HTML -->
    </div>
`;
```

### 添加新动画

在 `renderer.js` 的 `animations` 对象中添加：

```javascript
const animations = {
    custom: {
        duration: '2s',
        timing: 'ease-in-out',
        keyframes: `
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        `
    }
};
```

### 修改窗口设置

编辑 `main.js` 中的 `BrowserWindow` 配置：

```javascript
const mainWindow = new BrowserWindow({
    width: 300,        // 窗口宽度
    height: 300,       // 窗口高度
    transparent: true, // 透明背景
    frame: false,      // 无边框
    // ... 其他配置
});
```

### 添加 IPC 通信

主进程 (`main.js`):

```javascript
ipcMain.handle('custom-action', async (event, data) => {
    // 处理逻辑
    return result;
});
```

渲染进程 (`renderer.js`):

```javascript
const result = await ipcRenderer.invoke('custom-action', data);
```

## 平台特定说明

### macOS

#### 图标制作

```bash
# 创建 .icns 文件
mkdir icon.iconset
# 添加不同尺寸的 PNG 图片
# icon_16x16.png, icon_32x32.png, ...
iconutil -c icns icon.iconset
```

#### 代码签名

需要 Apple Developer 账号：

```bash
# 签名应用
codesign --deep --force --verify --verbose --sign "Developer ID Application: Your Name" dist/mac/YourApp.app

# 公证
xcrun altool --notarize-app --primary-bundle-id "com.yourcompany.app" --username "your@email.com" --password "app-specific-password" --file dist/YourApp.dmg
```

### Windows

#### 图标制作

使用在线工具或 ImageMagick：

```bash
convert icon.png -define icon:auto-resize=256,128,64,48,32,16 icon.ico
```

#### 构建选项

在 `package.json` 中配置：

```json
"win": {
    "target": ["nsis", "portable"],
    "icon": "assets/icon.ico"
}
```

### Linux

#### 支持的格式

- AppImage: 单文件可执行（推荐）
- deb: Debian/Ubuntu 包
- rpm: Red Hat/Fedora 包
- snap: Snap 包

#### 桌面集成

创建 `.desktop` 文件：

```desktop
[Desktop Entry]
Name={{PET_NAME}}
Comment=Desktop Pet Application
Exec=/path/to/app
Icon=/path/to/icon.png
Type=Application
Categories=Utility;
```

## 性能优化

### 减少内存占用

```javascript
// 使用 requestIdleCallback 处理非关键任务
requestIdleCallback(() => {
    // 低优先级任务
});
```

### 优化渲染

```javascript
// 使用 will-change CSS 属性
.pet {
    will-change: transform;
}

// 使用 transform 代替 top/left
petElement.style.transform = `translate(${x}px, ${y}px)`;
```

### 减少包体积

```bash
# 使用 electron-builder 的压缩选项
npm run build -- --config.compression=maximum
```

## 发布流程

### 1. 准备发布

- 更新版本号 (`package.json`)
- 更新更新日志
- 测试所有平台
- 准备发布说明

### 2. 构建

```bash
npm run build
```

### 3. 签名（macOS/Windows）

按照平台特定说明进行签名

### 4. 分发

上传到：
- GitHub Releases
- 个人网站
- Microsoft Store (Windows)
- Mac App Store (macOS)
- Snap Store (Linux)

## 调试技巧

### 主进程调试

```bash
# 设置环境变量
NODE_ENV=development npm start

# 或在代码中打开开发者工具
mainWindow.webContents.openDevTools()
```

### 渲染进程调试

按 `F12` 或在菜单中选择"开发者工具"

### 日志记录

```javascript
// 主进程
console.log('主进程日志');

// 渲染进程
ipcRenderer.send('log', '渲染进程日志');
```

## 常见问题

### 应用无法启动

1. 检查 Node.js 版本是否符合要求
2. 删除 `node_modules` 重新安装
3. 检查是否有权限问题

### 宠物不显示

1. 检查窗口是否在屏幕范围内
2. 尝试重置位置（托盘菜单 → 重置位置）
3. 检查透明度设置

### 拖拽不流畅

1. 关闭硬件加速（如有问题）
2. 减小窗口大小
3. 优化动画性能

### 托盘图标不显示

1. 确认 `assets/tray-icon.png` 存在
2. 检查图标尺寸（建议 16x16 或 32x32）
3. 重启应用

## 更新机制

可以集成 `electron-updater` 实现自动更新：

```bash
npm install electron-updater
```

在 `main.js` 中：

```javascript
const { autoUpdater } = require('electron-updater');

app.whenReady().then(() => {
    autoUpdater.checkForUpdatesAndNotify();
});
```

## 安全建议

- 不要启用 `nodeIntegration`（除非必要）
- 使用 `contextIsolation: true`
- 验证所有 IPC 消息
- 不要加载远程内容
- 定期更新依赖

## 技术栈

- Electron 28+
- Node.js 16+
- Vanilla JavaScript (ES6+)
- CSS3 Animations

## 依赖项

### 生产依赖

- Electron: 跨平台桌面应用框架

### 开发依赖

- electron-builder: 打包和分发工具

## 许可证

MIT License

## 参考资源

- [Electron 官方文档](https://www.electronjs.org/docs)
- [electron-builder 文档](https://www.electron.build/)
- [Electron API 示例](https://github.com/electron/electron-api-demos)

## 更新日志

### v1.0.0 (2024-XX-XX)
- 初始版本发布
- 基础拖拽和动画功能
- 系统托盘集成
- 跨平台支持

## 贡献

欢迎提交 Issues 和 Pull Requests!

## 支持

如有问题，请通过以下方式联系：
- GitHub Issues
- Email: [your-email]
- Discord: [your-server]
