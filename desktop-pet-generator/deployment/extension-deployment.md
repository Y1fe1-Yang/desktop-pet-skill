# 浏览器插件部署指南

本指南详细说明如何将桌面宠物打包为浏览器插件，支持 Chrome、Firefox、Edge 等浏览器。

## 目录

1. [插件类型选择](#插件类型选择)
2. [Chrome 插件开发](#chrome-插件开发)
3. [Firefox 插件开发](#firefox-插件开发)
4. [Edge 插件开发](#edge-插件开发)
5. [发布到商店](#发布到商店)
6. [自动更新配置](#自动更新配置)
7. [故障排查](#故障排查)

---

## 插件类型选择

桌面宠物插件有三种实现方式：

### 1. Content Script 模式（推荐）

**优点**：
- 在所有网页上显示
- 可以与页面交互
- 用户体验最佳

**缺点**：
- 可能与某些网站冲突
- 需要注入权限

**适用场景**：大多数桌面宠物

---

### 2. Popup 模式

**优点**：
- 简单轻量
- 不干扰网页
- 权限要求最少

**缺点**：
- 需要点击图标才显示
- 关闭 popup 窗口后消失

**适用场景**：工具型宠物（如番茄钟助手）

---

### 3. Side Panel 模式（Chrome 114+）

**优点**：
- 独立侧边栏
- 持久显示
- 不遮挡页面内容

**缺点**：
- 仅 Chrome 支持
- 占用屏幕空间

**适用场景**：任务管理型宠物

---

## Chrome 插件开发

### 步骤 1：创建项目结构

```
my-pet-extension/
├── manifest.json       # 插件配置文件
├── background.js       # 后台脚本（可选）
├── content.js          # 内容脚本
├── popup.html          # 弹出页面（可选）
├── popup.js            # 弹出页面脚本（可选）
├── styles.css          # 样式
├── icons/
│   ├── icon16.png      # 16x16
│   ├── icon48.png      # 48x48
│   └── icon128.png     # 128x128
└── assets/
    ├── pet.png
    └── sounds/
```

---

### 步骤 2：创建 Manifest V3 配置

创建 `manifest.json`：

```json
{
  "manifest_version": 3,
  "name": "My Desktop Pet",
  "version": "1.0.0",
  "description": "A cute desktop pet that lives in your browser",
  "author": "Your Name",

  "icons": {
    "16": "icons/icon16.png",
    "48": "icons/icon48.png",
    "128": "icons/icon128.png"
  },

  "action": {
    "default_popup": "popup.html",
    "default_icon": {
      "16": "icons/icon16.png",
      "48": "icons/icon48.png",
      "128": "icons/icon128.png"
    },
    "default_title": "My Desktop Pet"
  },

  "background": {
    "service_worker": "background.js"
  },

  "content_scripts": [
    {
      "matches": ["<all_urls>"],
      "js": ["content.js"],
      "css": ["styles.css"],
      "run_at": "document_end"
    }
  ],

  "web_accessible_resources": [
    {
      "resources": ["assets/*", "sounds/*"],
      "matches": ["<all_urls>"]
    }
  ],

  "permissions": [
    "storage",
    "activeTab"
  ],

  "host_permissions": [
    "<all_urls>"
  ]
}
```

---

### 步骤 3：创建 Content Script

创建 `content.js`：

```javascript
// 检查是否已注入（避免重复）
if (!window.desktopPetInjected) {
  window.desktopPetInjected = true;

  // 创建宠物容器
  const petContainer = document.createElement('div');
  petContainer.id = 'desktop-pet-extension';
  petContainer.innerHTML = `
    <div class="pet" id="pet-element">
      <img src="${chrome.runtime.getURL('assets/pet.png')}" alt="Pet">
    </div>
  `;

  // 添加到页面
  document.body.appendChild(petContainer);

  // 初始化交互系统
  class PetInteractionSystem {
    constructor(petElement) {
      this.pet = petElement;
      this.isDragging = false;
      this.offset = { x: 0, y: 0 };
      this.init();
    }

    init() {
      this.loadPosition();
      this.setupDragging();
      this.setupAnimations();
      this.setupClickResponse();
    }

    loadPosition() {
      chrome.storage.sync.get(['petX', 'petY'], (result) => {
        const x = result.petX || window.innerWidth - 200;
        const y = result.petY || window.innerHeight - 200;
        this.pet.style.left = x + 'px';
        this.pet.style.top = y + 'px';
      });
    }

    savePosition() {
      const x = parseInt(this.pet.style.left);
      const y = parseInt(this.pet.style.top);
      chrome.storage.sync.set({ petX: x, petY: y });
    }

    setupDragging() {
      this.pet.addEventListener('mousedown', (e) => {
        this.isDragging = true;
        this.offset.x = e.clientX - this.pet.offsetLeft;
        this.offset.y = e.clientY - this.pet.offsetTop;
        this.pet.style.cursor = 'grabbing';
      });

      document.addEventListener('mousemove', (e) => {
        if (this.isDragging) {
          this.pet.style.left = (e.clientX - this.offset.x) + 'px';
          this.pet.style.top = (e.clientY - this.offset.y) + 'px';
        }
      });

      document.addEventListener('mouseup', () => {
        if (this.isDragging) {
          this.isDragging = false;
          this.pet.style.cursor = 'grab';
          this.savePosition();
        }
      });
    }

    setupAnimations() {
      // 待机动画
      setInterval(() => {
        if (!this.isDragging) {
          this.pet.classList.add('bounce');
          setTimeout(() => this.pet.classList.remove('bounce'), 500);
        }
      }, 10000);
    }

    setupClickResponse() {
      this.pet.addEventListener('click', () => {
        this.pet.classList.add('clicked');
        this.playSound('meow');
        setTimeout(() => this.pet.classList.remove('clicked'), 500);
      });
    }

    playSound(name) {
      const audio = new Audio(chrome.runtime.getURL(`sounds/${name}.mp3`));
      audio.volume = 0.5;
      audio.play().catch(e => console.warn('Audio play failed:', e));
    }
  }

  // 初始化
  const pet = document.getElementById('pet-element');
  new PetInteractionSystem(pet);
}
```

---

### 步骤 4：创建样式

创建 `styles.css`：

```css
#desktop-pet-extension {
  position: fixed;
  z-index: 2147483647; /* 最大 z-index */
  pointer-events: none; /* 不阻止页面点击 */
}

#desktop-pet-extension .pet {
  position: fixed;
  width: 150px;
  height: 150px;
  cursor: grab;
  pointer-events: auto; /* 宠物本身可点击 */
  transition: transform 0.3s ease;
  user-select: none;
}

#desktop-pet-extension .pet img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  pointer-events: none;
}

/* 动画 */
#desktop-pet-extension .pet.bounce {
  animation: bounce 0.5s ease;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}

#desktop-pet-extension .pet.clicked {
  animation: click-response 0.5s ease;
}

@keyframes click-response {
  0% { transform: scale(1) rotate(0deg); }
  50% { transform: scale(1.2) rotate(10deg); }
  100% { transform: scale(1) rotate(0deg); }
}

/* 拖拽时 */
#desktop-pet-extension .pet:active {
  cursor: grabbing;
}
```

---

### 步骤 5：创建 Background Script（可选）

创建 `background.js`：

```javascript
// 监听插件安装
chrome.runtime.onInstalled.addListener((details) => {
  if (details.reason === 'install') {
    console.log('Desktop Pet installed!');

    // 设置默认配置
    chrome.storage.sync.set({
      enabled: true,
      volume: 0.5,
      petX: null,
      petY: null
    });

    // 打开欢迎页面
    chrome.tabs.create({
      url: 'popup.html'
    });
  }
});

// 监听消息
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'getConfig') {
    chrome.storage.sync.get(['enabled', 'volume'], (result) => {
      sendResponse(result);
    });
    return true; // 异步响应
  }
});
```

---

### 步骤 6：创建 Popup 页面

创建 `popup.html`：

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body {
      width: 300px;
      padding: 20px;
      font-family: Arial, sans-serif;
    }
    h2 {
      margin-top: 0;
      font-size: 18px;
    }
    .control {
      margin: 15px 0;
    }
    label {
      display: block;
      margin-bottom: 5px;
      font-weight: bold;
    }
    input[type="range"] {
      width: 100%;
    }
    button {
      width: 100%;
      padding: 10px;
      margin: 5px 0;
      background: #4CAF50;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      font-size: 14px;
    }
    button:hover {
      background: #45a049;
    }
    button.secondary {
      background: #2196F3;
    }
    button.secondary:hover {
      background: #0b7dda;
    }
    .status {
      padding: 10px;
      background: #e7f3ff;
      border-radius: 4px;
      margin-top: 10px;
      font-size: 12px;
    }
  </style>
</head>
<body>
  <h2>🐾 Desktop Pet Settings</h2>

  <div class="control">
    <label>
      <input type="checkbox" id="enabled" checked>
      Enable Pet
    </label>
  </div>

  <div class="control">
    <label for="volume">Sound Volume: <span id="volume-value">50%</span></label>
    <input type="range" id="volume" min="0" max="100" value="50">
  </div>

  <button id="reset-position">Reset Position</button>
  <button id="change-pet" class="secondary">Change Pet (Coming Soon)</button>

  <div class="status">
    <strong>Version:</strong> 1.0.0<br>
    <strong>Status:</strong> Active
  </div>

  <script src="popup.js"></script>
</body>
</html>
```

创建 `popup.js`：

```javascript
// 加载设置
chrome.storage.sync.get(['enabled', 'volume'], (result) => {
  document.getElementById('enabled').checked = result.enabled !== false;
  document.getElementById('volume').value = (result.volume || 0.5) * 100;
  updateVolumeLabel();
});

// 保存启用状态
document.getElementById('enabled').addEventListener('change', (e) => {
  chrome.storage.sync.set({ enabled: e.target.checked });

  // 重新加载所有标签页（应用更改）
  chrome.tabs.query({}, (tabs) => {
    tabs.forEach(tab => {
      chrome.tabs.reload(tab.id);
    });
  });
});

// 保存音量
document.getElementById('volume').addEventListener('input', (e) => {
  const volume = e.target.value / 100;
  chrome.storage.sync.set({ volume });
  updateVolumeLabel();
});

function updateVolumeLabel() {
  const value = document.getElementById('volume').value;
  document.getElementById('volume-value').textContent = value + '%';
}

// 重置位置
document.getElementById('reset-position').addEventListener('click', () => {
  chrome.storage.sync.remove(['petX', 'petY'], () => {
    // 重新加载当前标签页
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      chrome.tabs.reload(tabs[0].id);
    });
    alert('Position reset! Refresh the page to see changes.');
  });
});
```

---

### 步骤 7：本地测试

#### 加载未打包的扩展

1. 打开 Chrome 浏览器
2. 访问 `chrome://extensions/`
3. 启用 "开发者模式"（右上角开关）
4. 点击 "加载已解压的扩展程序"
5. 选择项目文件夹 `my-pet-extension`

#### 测试功能

- [ ] 访问任意网页，宠物是否显示
- [ ] 拖拽宠物，位置是否保存
- [ ] 点击宠物，是否有响应
- [ ] 打开插件 popup，设置是否生效
- [ ] 禁用插件，宠物是否消失

---

### 步骤 8：打包插件

#### 方法 1：通过 Chrome

1. `chrome://extensions/`
2. 点击 "打包扩展程序"
3. 选择根目录
4. 生成 `.crx` 文件和 `.pem` 密钥文件

**重要**：保管好 `.pem` 文件，更新插件时需要。

---

#### 方法 2：使用命令行

```bash
# 安装 crx3 工具
npm install -g crx3

# 打包
crx3 my-pet-extension -o my-pet.crx
```

---

## Firefox 插件开发

Firefox 使用 Manifest V2（逐步迁移到 V3）。

### 修改 Manifest

创建 `manifest-firefox.json`：

```json
{
  "manifest_version": 2,
  "name": "My Desktop Pet",
  "version": "1.0.0",
  "description": "A cute desktop pet for Firefox",

  "icons": {
    "48": "icons/icon48.png",
    "96": "icons/icon128.png"
  },

  "browser_action": {
    "default_popup": "popup.html",
    "default_icon": {
      "48": "icons/icon48.png"
    }
  },

  "background": {
    "scripts": ["background.js"]
  },

  "content_scripts": [
    {
      "matches": ["<all_urls>"],
      "js": ["content.js"],
      "css": ["styles.css"]
    }
  ],

  "web_accessible_resources": [
    "assets/*",
    "sounds/*"
  ],

  "permissions": [
    "storage",
    "activeTab",
    "<all_urls>"
  ],

  "browser_specific_settings": {
    "gecko": {
      "id": "desktop-pet@example.com",
      "strict_min_version": "109.0"
    }
  }
}
```

### API 差异处理

```javascript
// 兼容 Chrome 和 Firefox
const browserAPI = typeof browser !== 'undefined' ? browser : chrome;

// 使用
browserAPI.storage.sync.get(['enabled'], (result) => {
  // ...
});
```

### 本地测试

1. 访问 `about:debugging#/runtime/this-firefox`
2. 点击 "临时载入附加组件"
3. 选择 `manifest.json`

### 打包

```bash
# 安装 web-ext
npm install -g web-ext

# 构建
cd my-pet-extension
web-ext build
```

生成的 `.zip` 文件即为 Firefox 插件包。

---

## Edge 插件开发

Edge 基于 Chromium，与 Chrome 插件兼容。

### 测试

1. 访问 `edge://extensions/`
2. 启用 "开发人员模式"
3. 加载未打包的扩展

### 打包

与 Chrome 相同，生成 `.crx` 文件。

---

## 发布到商店

### Chrome Web Store

#### 步骤 1：注册开发者账户

1. 访问 [Chrome Web Store Developer Dashboard](https://chrome.google.com/webstore/devconsole/)
2. 支付一次性注册费（$5 USD）
3. 同意开发者协议

#### 步骤 2：准备发布资源

**必需**：
- 插件 `.zip` 包
- 图标（128x128px）
- 至少 1 张截图（1280x800 或 640x400）
- 详细描述（英文，至少 132 字符）
- 简短描述（英文，最多 132 字符）

**可选**：
- 宣传图片（440x280, 920x680, 1400x560）
- 宣传视频（YouTube）

#### 步骤 3：上传插件

1. Dashboard → "新建项目"
2. 上传 `.zip` 文件
3. 填写商店信息：
   - 名称
   - 描述
   - 分类（娱乐 / Entertainment）
   - 隐私政策 URL（如需要）
   - 支持语言
4. 上传截图和图片
5. 设置定价（免费或付费）
6. 选择可见性（公开、不公开或私有）

#### 步骤 4：提交审核

1. 点击 "提交审核"
2. 审核通常需要 1-3 个工作日
3. 通过后自动发布（或等待手动发布）

#### 更新插件

1. 修改 `manifest.json` 中的 `version`（如 1.0.0 → 1.0.1）
2. 打包新版本
3. 在 Dashboard 上传新版本
4. 提交审核

---

### Firefox Add-ons

#### 步骤 1：注册账户

访问 [Firefox Add-on Developer Hub](https://addons.mozilla.org/developers/)

#### 步骤 2：提交插件

1. 点击 "Submit a New Add-on"
2. 上传 `.zip` 或 `.xpi` 文件
3. 选择分发渠道：
   - On this site（公开发布）
   - On your own（自行分发）
4. 填写插件信息
5. 上传截图（至少 1 张）
6. 提交审核

审核通常需要几小时到几天。

---

### Edge Add-ons

#### 步骤 1：注册

访问 [Partner Center](https://partner.microsoft.com/dashboard/microsoftedge/public/login)

#### 步骤 2：提交

1. 创建新扩展
2. 上传 `.zip` 包
3. 填写详细信息
4. 提交审核（通常 1-2 天）

---

## 自动更新配置

### Chrome 自动更新

Chrome Web Store 托管的插件会自动更新。

自托管插件需要 `update_url`：

```json
{
  "update_url": "https://example.com/updates.xml"
}
```

`updates.xml` 示例：

```xml
<?xml version='1.0' encoding='UTF-8'?>
<gupdate xmlns='http://www.google.com/update2/response' protocol='2.0'>
  <app appid='YOUR_EXTENSION_ID'>
    <updatecheck codebase='https://example.com/my-pet-extension.crx' version='1.0.1' />
  </app>
</gupdate>
```

---

### Firefox 自动更新

AMO 托管的插件自动更新。

自托管插件在 `manifest.json` 中添加：

```json
{
  "browser_specific_settings": {
    "gecko": {
      "update_url": "https://example.com/updates.json"
    }
  }
}
```

`updates.json` 示例：

```json
{
  "addons": {
    "desktop-pet@example.com": {
      "updates": [
        {
          "version": "1.0.1",
          "update_link": "https://example.com/desktop-pet-1.0.1.xpi"
        }
      ]
    }
  }
}
```

---

## 故障排查

### 问题 1：插件未显示

**检查**：
- 是否有控制台错误？（F12）
- `manifest.json` 格式是否正确？
- `content_scripts` 的 `matches` 是否包含当前网址？

---

### 问题 2：资源加载失败

**检查**：
- 是否在 `web_accessible_resources` 中声明？
- 是否使用了 `chrome.runtime.getURL()`？

**正确**：
```javascript
const img = chrome.runtime.getURL('assets/pet.png');
```

**错误**：
```javascript
const img = 'assets/pet.png'; // 相对路径无效
```

---

### 问题 3：存储数据丢失

**原因**：使用了 `localStorage` 而非 `chrome.storage`

**解决**：
```javascript
// 使用 chrome.storage.sync（跨设备同步）
chrome.storage.sync.set({ key: 'value' });

// 或使用 chrome.storage.local（本地存储）
chrome.storage.local.set({ key: 'value' });
```

---

### 问题 4：Content Security Policy 错误

**原因**：内联脚本被阻止

**解决**：避免内联脚本，使用外部文件

**错误**：
```html
<button onclick="doSomething()">Click</button>
```

**正确**：
```html
<button id="myButton">Click</button>
<script src="script.js"></script>
```

```javascript
// script.js
document.getElementById('myButton').addEventListener('click', doSomething);
```

---

### 问题 5：审核被拒

**常见原因**：
- 权限请求过多
- 缺少隐私政策
- 截图不清晰
- 描述不完整

**解决**：
- 仅请求必需权限
- 添加隐私政策链接
- 提供高质量截图
- 详细描述功能

---

## 最佳实践

### 1. 性能优化

```javascript
// 使用事件委托
document.addEventListener('click', (e) => {
  if (e.target.matches('.pet')) {
    handlePetClick(e);
  }
});

// 防抖
const debouncedSave = debounce(savePosition, 500);
```

### 2. 用户体验

- 提供禁用选项
- 允许自定义位置
- 音量可调
- 低资源占用

### 3. 兼容性

```javascript
// 检测浏览器
const isChrome = !!window.chrome;
const isFirefox = typeof InstallTrigger !== 'undefined';
const isEdge = navigator.userAgent.includes('Edg');
```

---

## 总结

浏览器插件适合：
- 需要跨网站显示
- 希望用户随时可见
- 集成浏览器功能

推荐发布平台：
- **Chrome Web Store**: 用户最多
- **Firefox Add-ons**: 开源友好
- **Edge Add-ons**: 快速增长

下一步：
- [部署为桌面应用](desktop-deployment.md)
- [优化插件性能](../TUTORIAL.md#性能优化)
