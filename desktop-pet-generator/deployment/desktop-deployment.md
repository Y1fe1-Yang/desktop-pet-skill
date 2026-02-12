# 桌面应用部署指南

本指南详细说明如何使用 Electron 将桌面宠物打包为独立的桌面应用程序，支持 Windows、macOS 和 Linux。

## 目录

1. [Electron 简介](#electron-简介)
2. [项目初始化](#项目初始化)
3. [开发环境配置](#开发环境配置)
4. [打包配置](#打包配置)
5. [多平台构建](#多平台构建)
6. [应用签名和公证](#应用签名和公证)
7. [自动更新](#自动更新)
8. [分发和安装](#分发和安装)
9. [故障排查](#故障排查)

---

## Electron 简介

### 什么是 Electron

Electron 是一个使用 Web 技术（HTML、CSS、JavaScript）构建跨平台桌面应用的框架。

**优点**：
- 跨平台（Windows、macOS、Linux）
- 使用熟悉的 Web 技术
- 丰富的生态系统
- 原生系统集成

**缺点**：
- 应用体积较大（~50-100MB）
- 内存占用较高
- 启动速度相对较慢

---

## 项目初始化

### 步骤 1：创建 Electron 项目

```bash
mkdir desktop-pet-app
cd desktop-pet-app
npm init -y
```

### 步骤 2：安装 Electron

```bash
npm install --save-dev electron
npm install --save-dev electron-builder
```

### 步骤 3：项目结构

```
desktop-pet-app/
├── main.js              # Electron 主进程
├── preload.js           # 预加载脚本
├── renderer/
│   ├── index.html       # 渲染进程 HTML
│   ├── styles.css       # 样式
│   └── renderer.js      # 渲染进程 JS
├── assets/
│   ├── pet.png
│   ├── icon.png         # 应用图标
│   └── sounds/
├── package.json
└── electron-builder.yml # 打包配置
```

---

## 开发环境配置

### 步骤 1：创建主进程

创建 `main.js`：

```javascript
const { app, BrowserWindow, Tray, Menu, ipcMain, screen } = require('electron');
const path = require('path');

let mainWindow;
let tray;

function createWindow() {
  const { width, height } = screen.getPrimaryDisplay().workAreaSize;

  mainWindow = new BrowserWindow({
    width: 200,
    height: 200,
    x: width - 220,
    y: height - 220,
    frame: false,              // 无边框窗口
    transparent: true,         // 透明背景
    alwaysOnTop: true,         // 始终置顶
    resizable: false,
    skipTaskbar: false,        // 显示在任务栏
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    }
  });

  mainWindow.loadFile('renderer/index.html');

  // 开发时打开 DevTools
  if (process.env.NODE_ENV === 'development') {
    mainWindow.webContents.openDevTools({ mode: 'detach' });
  }

  // 窗口失去焦点时不最小化
  mainWindow.on('blur', () => {
    // 可选：降低透明度
    mainWindow.setOpacity(0.7);
  });

  mainWindow.on('focus', () => {
    mainWindow.setOpacity(1.0);
  });
}

function createTray() {
  tray = new Tray(path.join(__dirname, 'assets/icon.png'));

  const contextMenu = Menu.buildFromTemplate([
    {
      label: 'Show Pet',
      click: () => {
        mainWindow.show();
        mainWindow.focus();
      }
    },
    {
      label: 'Hide Pet',
      click: () => {
        mainWindow.hide();
      }
    },
    { type: 'separator' },
    {
      label: 'Settings',
      click: () => {
        // 打开设置窗口
        createSettingsWindow();
      }
    },
    { type: 'separator' },
    {
      label: 'Quit',
      click: () => {
        app.quit();
      }
    }
  ]);

  tray.setToolTip('Desktop Pet');
  tray.setContextMenu(contextMenu);

  // 双击托盘图标显示/隐藏
  tray.on('double-click', () => {
    if (mainWindow.isVisible()) {
      mainWindow.hide();
    } else {
      mainWindow.show();
      mainWindow.focus();
    }
  });
}

function createSettingsWindow() {
  const settingsWindow = new BrowserWindow({
    width: 400,
    height: 500,
    parent: mainWindow,
    modal: true,
    show: false,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    }
  });

  settingsWindow.loadFile('renderer/settings.html');
  settingsWindow.once('ready-to-show', () => {
    settingsWindow.show();
  });
}

// 应用准备完成
app.whenReady().then(() => {
  createWindow();
  createTray();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

// 所有窗口关闭时退出（macOS 除外）
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// IPC 通信
ipcMain.handle('get-window-position', () => {
  const position = mainWindow.getPosition();
  return { x: position[0], y: position[1] };
});

ipcMain.handle('set-window-position', (event, { x, y }) => {
  mainWindow.setPosition(x, y);
});

ipcMain.on('play-sound', (event, soundName) => {
  // 播放声音（如果需要在主进程处理）
  console.log('Playing sound:', soundName);
});
```

---

### 步骤 2：创建预加载脚本

创建 `preload.js`：

```javascript
const { contextBridge, ipcRenderer } = require('electron');

// 暴露安全的 API 给渲染进程
contextBridge.exposeInMainWorld('electronAPI', {
  getWindowPosition: () => ipcRenderer.invoke('get-window-position'),
  setWindowPosition: (x, y) => ipcRenderer.invoke('set-window-position', { x, y }),
  playSound: (soundName) => ipcRenderer.send('play-sound', soundName),
  platform: process.platform
});
```

---

### 步骤 3：创建渲染进程

创建 `renderer/index.html`：

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta http-equiv="Content-Security-Policy" content="default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self'">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <div id="pet-container">
    <img id="pet-image" src="../assets/pet.png" alt="Desktop Pet" draggable="false">
  </div>

  <script src="renderer.js"></script>
</body>
</html>
```

创建 `renderer/styles.css`：

```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  width: 100%;
  height: 100%;
  overflow: hidden;
  background: transparent;
}

#pet-container {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: grab;
}

#pet-container:active {
  cursor: grabbing;
}

#pet-image {
  width: 150px;
  height: 150px;
  object-fit: contain;
  user-select: none;
  -webkit-user-drag: none;
  transition: transform 0.3s ease;
}

/* 动画 */
#pet-image.bounce {
  animation: bounce 0.5s ease;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}

#pet-image.clicked {
  animation: click-effect 0.5s ease;
}

@keyframes click-effect {
  0% { transform: scale(1) rotate(0deg); }
  50% { transform: scale(1.2) rotate(10deg); }
  100% { transform: scale(1) rotate(0deg); }
}
```

创建 `renderer/renderer.js`：

```javascript
const petImage = document.getElementById('pet-image');
let isDragging = false;

// 拖拽功能
petImage.addEventListener('mousedown', (e) => {
  isDragging = true;
  const startX = e.screenX;
  const startY = e.screenY;

  const onMouseMove = async (e) => {
    if (isDragging) {
      const deltaX = e.screenX - startX;
      const deltaY = e.screenY - startY;

      const currentPos = await window.electronAPI.getWindowPosition();
      window.electronAPI.setWindowPosition(
        currentPos.x + deltaX,
        currentPos.y + deltaY
      );
    }
  };

  const onMouseUp = () => {
    isDragging = false;
    document.removeEventListener('mousemove', onMouseMove);
    document.removeEventListener('mouseup', onMouseUp);
  };

  document.addEventListener('mousemove', onMouseMove);
  document.addEventListener('mouseup', onMouseUp);
});

// 点击响应
petImage.addEventListener('click', () => {
  petImage.classList.add('clicked');
  playSound('meow');
  setTimeout(() => petImage.classList.remove('clicked'), 500);
});

// 待机动画
setInterval(() => {
  if (!isDragging) {
    petImage.classList.add('bounce');
    setTimeout(() => petImage.classList.remove('bounce'), 500);
  }
}, 10000);

// 播放声音
function playSound(name) {
  const audio = new Audio(`../assets/sounds/${name}.mp3`);
  audio.volume = 0.5;
  audio.play().catch(e => console.warn('Audio play failed:', e));
}

// 右键菜单
petImage.addEventListener('contextmenu', (e) => {
  e.preventDefault();
  // Electron 会显示托盘菜单
});
```

---

### 步骤 4：配置 package.json

修改 `package.json`：

```json
{
  "name": "desktop-pet-app",
  "version": "1.0.0",
  "description": "A cute desktop pet application",
  "main": "main.js",
  "author": "Your Name",
  "license": "MIT",
  "scripts": {
    "start": "electron .",
    "dev": "NODE_ENV=development electron .",
    "build": "electron-builder",
    "build:win": "electron-builder --win",
    "build:mac": "electron-builder --mac",
    "build:linux": "electron-builder --linux"
  },
  "devDependencies": {
    "electron": "^28.0.0",
    "electron-builder": "^24.9.1"
  }
}
```

---

### 步骤 5：测试运行

```bash
npm start
```

你应该看到一个无边框的透明窗口，显示你的宠物。

---

## 打包配置

### 创建 electron-builder.yml

```yaml
appId: com.example.desktoppet
productName: DesktopPet
copyright: Copyright © 2024 Your Name

directories:
  output: dist
  buildResources: assets

files:
  - "**/*"
  - "!**/{.git,.gitignore,.vscode,docs,test}/*"

compression: normal

# Windows 配置
win:
  target:
    - nsis
    - portable
  icon: assets/icon.ico
  artifactName: ${productName}-${version}-${os}-${arch}.${ext}

nsis:
  oneClick: false
  allowToChangeInstallationDirectory: true
  createDesktopShortcut: true
  createStartMenuShortcut: true
  shortcutName: Desktop Pet
  uninstallDisplayName: Desktop Pet

# macOS 配置
mac:
  category: public.app-category.entertainment
  target:
    - dmg
    - zip
  icon: assets/icon.icns
  artifactName: ${productName}-${version}-${os}-${arch}.${ext}

dmg:
  title: ${productName} ${version}
  icon: assets/icon.icns
  contents:
    - x: 130
      y: 220
    - x: 410
      y: 220
      type: link
      path: /Applications

# Linux 配置
linux:
  target:
    - AppImage
    - deb
    - rpm
  icon: assets/icon.png
  category: Utility
  artifactName: ${productName}-${version}-${os}-${arch}.${ext}

# 发布配置（自动更新）
publish:
  provider: github
  owner: yourusername
  repo: desktop-pet-app
```

---

## 多平台构建

### Windows 打包

#### 准备图标

需要 `.ico` 格式图标：

```bash
# 使用 ImageMagick 转换
convert assets/icon.png -define icon:auto-resize=256,128,64,48,32,16 assets/icon.ico
```

#### 构建

```bash
npm run build:win
```

生成文件：
- `DesktopPet-1.0.0-win-x64.exe` - 安装程序
- `DesktopPet-1.0.0-win-x64-portable.exe` - 便携版

---

### macOS 打包

#### 准备图标

需要 `.icns` 格式图标：

```bash
# 创建 iconset
mkdir icon.iconset
sips -z 16 16     icon.png --out icon.iconset/icon_16x16.png
sips -z 32 32     icon.png --out icon.iconset/icon_16x16@2x.png
sips -z 32 32     icon.png --out icon.iconset/icon_32x32.png
sips -z 64 64     icon.png --out icon.iconset/icon_32x32@2x.png
sips -z 128 128   icon.png --out icon.iconset/icon_128x128.png
sips -z 256 256   icon.png --out icon.iconset/icon_128x128@2x.png
sips -z 256 256   icon.png --out icon.iconset/icon_256x256.png
sips -z 512 512   icon.png --out icon.iconset/icon_256x256@2x.png
sips -z 512 512   icon.png --out icon.iconset/icon_512x512.png
sips -z 1024 1024 icon.png --out icon.iconset/icon_512x512@2x.png

# 生成 icns
iconutil -c icns icon.iconset -o assets/icon.icns
```

#### 构建

```bash
npm run build:mac
```

生成文件：
- `DesktopPet-1.0.0-mac-x64.dmg` - 磁盘映像
- `DesktopPet-1.0.0-mac-x64.zip` - 压缩包

---

### Linux 打包

#### 构建

```bash
npm run build:linux
```

生成文件：
- `DesktopPet-1.0.0-linux-x86_64.AppImage` - AppImage
- `DesktopPet-1.0.0-linux-amd64.deb` - Debian 包
- `DesktopPet-1.0.0-linux-x86_64.rpm` - RPM 包

---

## 应用签名和公证

### Windows 代码签名

#### 购买代码签名证书

从 DigiCert、Sectigo 等 CA 购买。

#### 配置签名

在 `electron-builder.yml` 中：

```yaml
win:
  certificateFile: path/to/certificate.pfx
  certificatePassword: YOUR_PASSWORD
  signAndEditExecutable: true
  signingHashAlgorithms:
    - sha256
```

或使用环境变量：

```bash
export CSC_LINK=/path/to/certificate.pfx
export CSC_KEY_PASSWORD=your_password
npm run build:win
```

---

### macOS 签名和公证

#### 准备

1. 加入 Apple Developer Program（$99/年）
2. 获取 Developer ID Application 证书

#### 配置签名

在 `electron-builder.yml` 中：

```yaml
mac:
  hardenedRuntime: true
  gatekeeperAssess: false
  entitlements: build/entitlements.mac.plist
  entitlementsInherit: build/entitlements.mac.plist
```

创建 `build/entitlements.mac.plist`：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>com.apple.security.cs.allow-jit</key>
  <true/>
  <key>com.apple.security.cs.allow-unsigned-executable-memory</key>
  <true/>
  <key>com.apple.security.cs.disable-library-validation</key>
  <true/>
</dict>
</plist>
```

#### 公证

```bash
# 构建并公证
export APPLE_ID=your@email.com
export APPLE_ID_PASSWORD=app-specific-password
export APPLE_TEAM_ID=TEAM_ID

npm run build:mac
```

electron-builder 会自动处理公证。

---

## 自动更新

### 步骤 1：安装 electron-updater

```bash
npm install electron-updater
```

### 步骤 2：配置更新

在 `main.js` 中添加：

```javascript
const { autoUpdater } = require('electron-updater');

// 检查更新
autoUpdater.checkForUpdatesAndNotify();

autoUpdater.on('update-available', () => {
  dialog.showMessageBox({
    type: 'info',
    title: 'Update Available',
    message: 'A new version is available. Downloading now...'
  });
});

autoUpdater.on('update-downloaded', () => {
  dialog.showMessageBox({
    type: 'info',
    title: 'Update Ready',
    message: 'Update downloaded. It will be installed on restart.',
    buttons: ['Restart Now', 'Later']
  }).then((result) => {
    if (result.response === 0) {
      autoUpdater.quitAndInstall();
    }
  });
});
```

### 步骤 3：配置发布

在 `electron-builder.yml` 中：

```yaml
publish:
  provider: github
  owner: yourusername
  repo: desktop-pet-app
  releaseType: release
```

### 步骤 4：发布新版本

```bash
# 更新版本号
npm version patch  # 或 minor, major

# 构建并发布到 GitHub Releases
export GH_TOKEN=your_github_token
npm run build -- --publish always
```

---

## 分发和安装

### GitHub Releases

1. 构建应用
2. 创建 GitHub Release
3. 上传安装包
4. 用户下载并安装

### 自托管

创建下载页面：

```html
<!DOCTYPE html>
<html>
<head>
  <title>Download Desktop Pet</title>
</head>
<body>
  <h1>Download Desktop Pet</h1>
  <ul>
    <li><a href="DesktopPet-1.0.0-win-x64.exe">Windows Installer</a></li>
    <li><a href="DesktopPet-1.0.0-mac-x64.dmg">macOS DMG</a></li>
    <li><a href="DesktopPet-1.0.0-linux-x86_64.AppImage">Linux AppImage</a></li>
  </ul>
</body>
</html>
```

---

## 故障排查

### 问题 1：窗口无法拖拽

**原因**：`-webkit-app-region` 样式问题

**解决**：

```css
#pet-container {
  -webkit-app-region: drag;
}

#pet-image {
  -webkit-app-region: no-drag;
}
```

---

### 问题 2：透明背景不工作

**检查**：
- `BrowserWindow` 是否设置了 `transparent: true`？
- CSS 是否设置了 `background: transparent`？
- macOS 可能需要额外配置

---

### 问题 3：打包后资源找不到

**原因**：路径错误

**解决**：使用 `__dirname` 或 `app.getAppPath()`

```javascript
const iconPath = path.join(__dirname, 'assets/icon.png');
```

---

### 问题 4：Windows Defender 误报

**原因**：未签名的应用被标记为可疑

**解决**：购买代码签名证书并签名

---

### 问题 5：macOS 提示"已损坏"

**原因**：应用未签名或公证

**临时解决**（开发时）：

```bash
xattr -cr /Applications/DesktopPet.app
```

**正式解决**：签名并公证应用

---

## 高级功能

### 1. 系统托盘

已在 `main.js` 中实现。

### 2. 全局快捷键

```javascript
const { globalShortcut } = require('electron');

app.whenReady().then(() => {
  // 注册快捷键
  globalShortcut.register('CommandOrControl+Shift+P', () => {
    if (mainWindow.isVisible()) {
      mainWindow.hide();
    } else {
      mainWindow.show();
    }
  });
});
```

### 3. 开机自启

```javascript
app.setLoginItemSettings({
  openAtLogin: true,
  openAsHidden: true
});
```

### 4. 通知

```javascript
const { Notification } = require('electron');

new Notification({
  title: 'Desktop Pet',
  body: 'Hello! I\'m your desktop pet!'
}).show();
```

---

## 性能优化

### 1. 减小应用体积

```yaml
# electron-builder.yml
asar: true
asarUnpack:
  - "**/*.node"

files:
  - "**/*"
  - "!docs"
  - "!test"
  - "!*.md"
```

### 2. 延迟加载

```javascript
// 懒加载模块
let heavyModule;
ipcMain.handle('use-heavy-feature', async () => {
  if (!heavyModule) {
    heavyModule = require('./heavy-module');
  }
  return heavyModule.doSomething();
});
```

### 3. 使用 Web Workers

```javascript
// 在渲染进程中
const worker = new Worker('worker.js');
worker.postMessage({ task: 'heavy-computation' });
worker.onmessage = (e) => {
  console.log('Result:', e.data);
};
```

---

## 总结

桌面应用适合：
- 需要系统级集成
- 希望提供最佳用户体验
- 愿意投入更多开发资源

推荐工具链：
- **Electron Builder**: 全功能打包工具
- **electron-updater**: 自动更新
- **electron-store**: 数据持久化

下一步：
- 优化应用性能
- 添加更多功能
- 发布到应用商店（可选）

相关文档：
- [网页部署指南](web-deployment.md)
- [浏览器插件指南](extension-deployment.md)
