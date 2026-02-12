# 网页部署指南

本指南详细说明如何将桌面宠物部署为网页版本，支持 GitHub Pages、Netlify、Vercel 等平台。

## 目录

1. [前置准备](#前置准备)
2. [部署到 GitHub Pages](#部署到-github-pages)
3. [部署到 Netlify](#部署到-netlify)
4. [部署到 Vercel](#部署到-vercel)
5. [自定义域名配置](#自定义域名配置)
6. [嵌入到现有网站](#嵌入到现有网站)
7. [性能优化](#性能优化)
8. [故障排查](#故障排查)

---

## 前置准备

### 系统要求

- Node.js 16+ 和 npm
- Git
- 生成的桌面宠物项目

### 检查项目结构

确保你的项目包含以下文件：

```
my-desktop-pet/
├── index.html
├── styles.css
├── pet.js
├── assets/
│   ├── pet.png
│   └── sounds/
│       └── *.mp3
├── package.json
└── README.md
```

### 安装依赖

```bash
cd my-desktop-pet
npm install
```

---

## 部署到 GitHub Pages

### 方法 1：使用 gh-pages 包（推荐）

#### 步骤 1：安装 gh-pages

```bash
npm install --save-dev gh-pages
```

#### 步骤 2：配置 package.json

在 `package.json` 中添加：

```json
{
  "name": "my-desktop-pet",
  "version": "1.0.0",
  "homepage": "https://yourusername.github.io/my-desktop-pet",
  "scripts": {
    "start": "python -m http.server 3000",
    "build": "npm run optimize",
    "optimize": "node scripts/optimize-assets.js",
    "predeploy": "npm run build",
    "deploy": "gh-pages -d ."
  },
  "devDependencies": {
    "gh-pages": "^5.0.0"
  }
}
```

**重要**：将 `yourusername` 替换为你的 GitHub 用户名。

#### 步骤 3：创建 Git 仓库

```bash
git init
git add .
git commit -m "Initial commit"
```

#### 步骤 4：创建 GitHub 仓库

1. 访问 [GitHub](https://github.com/new)
2. 创建新仓库，命名为 `my-desktop-pet`
3. **不要**初始化 README、.gitignore 或 LICENSE

#### 步骤 5：关联远程仓库

```bash
git remote add origin https://github.com/yourusername/my-desktop-pet.git
git branch -M main
git push -u origin main
```

#### 步骤 6：部署

```bash
npm run deploy
```

部署完成后，访问：
```
https://yourusername.github.io/my-desktop-pet/
```

**提示**：首次部署可能需要 5-10 分钟才能生效。

---

### 方法 2：使用 GitHub Actions（自动化）

#### 步骤 1：创建工作流文件

创建 `.github/workflows/deploy.yml`：

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches:
      - main

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Setup Pages
        uses: actions/configure-pages@v4

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: '.'

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

#### 步骤 2：启用 GitHub Pages

1. 访问仓库 Settings → Pages
2. Source 选择 "GitHub Actions"
3. 保存设置

#### 步骤 3：推送代码

```bash
git add .
git commit -m "Add GitHub Actions workflow"
git push
```

GitHub Actions 会自动构建并部署。

---

## 部署到 Netlify

### 方法 1：通过 Netlify CLI

#### 步骤 1：安装 Netlify CLI

```bash
npm install -g netlify-cli
```

#### 步骤 2：登录

```bash
netlify login
```

#### 步骤 3：初始化

```bash
cd my-desktop-pet
netlify init
```

按提示选择：
- Create & configure a new site
- 选择 team
- 输入 site name（如 `my-cute-pet`）

#### 步骤 4：配置构建设置

创建 `netlify.toml`：

```toml
[build]
  publish = "."
  command = "npm run build"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[build.environment]
  NODE_VERSION = "18"
```

#### 步骤 5：部署

```bash
netlify deploy --prod
```

访问：
```
https://my-cute-pet.netlify.app
```

---

### 方法 2：通过 Netlify Web UI

#### 步骤 1：上传到 GitHub

确保项目已推送到 GitHub。

#### 步骤 2：连接仓库

1. 访问 [Netlify](https://app.netlify.com)
2. 点击 "Add new site" → "Import an existing project"
3. 选择 GitHub 并授权
4. 选择你的仓库

#### 步骤 3：配置构建

- Build command: `npm run build`
- Publish directory: `.`
- 点击 "Deploy site"

完成后自动生成 URL。

---

## 部署到 Vercel

### 方法 1：通过 Vercel CLI

#### 步骤 1：安装 Vercel CLI

```bash
npm install -g vercel
```

#### 步骤 2：部署

```bash
cd my-desktop-pet
vercel
```

按提示操作：
- 登录 Vercel 账户
- 设置项目名称
- 选择默认设置

#### 步骤 3：生产部署

```bash
vercel --prod
```

---

### 方法 2：通过 Vercel Web UI

#### 步骤 1：导入项目

1. 访问 [Vercel](https://vercel.com/new)
2. 导入 Git 仓库
3. 选择你的 GitHub 仓库

#### 步骤 2：配置

Vercel 会自动检测项目类型，通常无需额外配置。

可选：创建 `vercel.json`

```json
{
  "version": 2,
  "builds": [
    {
      "src": "index.html",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/$1"
    }
  ]
}
```

#### 步骤 3：部署

点击 "Deploy"，完成后获得：
```
https://my-desktop-pet.vercel.app
```

---

## 自定义域名配置

### GitHub Pages 自定义域名

#### 步骤 1：购买域名

从 Namecheap、GoDaddy 或 Cloudflare 购买域名（如 `mycutepet.com`）。

#### 步骤 2：配置 DNS

在域名提供商的 DNS 设置中添加：

**A 记录**（Apex 域名）：
```
Type: A
Name: @
Value: 185.199.108.153
Value: 185.199.109.153
Value: 185.199.110.153
Value: 185.199.111.153
TTL: 3600
```

**CNAME 记录**（子域名）：
```
Type: CNAME
Name: www
Value: yourusername.github.io
TTL: 3600
```

#### 步骤 3：配置 GitHub Pages

1. 仓库 Settings → Pages
2. Custom domain 输入 `mycutepet.com`
3. 等待 DNS 检查通过
4. 启用 "Enforce HTTPS"

#### 步骤 4：添加 CNAME 文件

在项目根目录创建 `CNAME` 文件：

```
mycutepet.com
```

提交并推送：

```bash
git add CNAME
git commit -m "Add custom domain"
git push
npm run deploy
```

---

### Netlify 自定义域名

1. Netlify Dashboard → Site settings → Domain management
2. 点击 "Add custom domain"
3. 输入域名并验证
4. 按提示配置 DNS（Netlify 提供 DNS 服务）
5. 启用 HTTPS（自动）

---

### Vercel 自定义域名

1. Vercel Dashboard → Project settings → Domains
2. 添加域名
3. 配置 DNS（A 记录指向 Vercel IP）
4. Vercel 自动配置 SSL

---

## 嵌入到现有网站

### 方法 1：使用 iframe

```html
<iframe
  src="https://yourusername.github.io/my-desktop-pet/"
  width="400"
  height="400"
  frameborder="0"
  style="position: fixed; bottom: 20px; right: 20px; z-index: 9999;">
</iframe>
```

**优点**：
- 简单易用
- 完全隔离

**缺点**：
- 无法与主页面交互
- 可能被 CSP 阻止

---

### 方法 2：直接嵌入代码

#### 步骤 1：复制核心文件

将以下文件复制到你的网站：
- `assets/pet.png`
- `sounds/*.mp3`

#### 步骤 2：添加 HTML

在目标页面的 `<body>` 底部添加：

```html
<!-- Desktop Pet -->
<div id="desktop-pet" class="pet">
  <img src="/assets/pet.png" alt="Desktop Pet">
</div>

<!-- 样式 -->
<link rel="stylesheet" href="/css/pet.css">

<!-- 脚本 -->
<script src="/js/pet.js"></script>
<script>
  // 初始化
  const pet = document.getElementById('desktop-pet');
  const interactionSystem = new PetInteractionSystem(pet);
</script>
```

#### 步骤 3：添加 CSS

创建 `css/pet.css`（复制生成的 `styles.css`）。

#### 步骤 4：添加 JavaScript

创建 `js/pet.js`（复制生成的 `pet.js`）。

---

### 方法 3：作为 Web Component

将桌宠封装为 Web Component：

```javascript
// pet-widget.js
class DesktopPet extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.shadowRoot.innerHTML = `
      <style>
        /* 复制 styles.css 内容 */
        .pet { /* ... */ }
      </style>
      <div class="pet">
        <img src="${this.getAttribute('image')}" alt="Pet">
      </div>
    `;

    // 初始化交互系统
    const pet = this.shadowRoot.querySelector('.pet');
    new PetInteractionSystem(pet);
  }
}

customElements.define('desktop-pet', DesktopPet);
```

**使用**：

```html
<script src="pet-widget.js"></script>
<desktop-pet image="/assets/pet.png"></desktop-pet>
```

---

## 性能优化

### 1. 图片优化

```bash
# 压缩 PNG
pngquant assets/pet.png --quality=65-80 --output assets/pet-optimized.png

# 或使用 WebP
cwebp -q 80 assets/pet.png -o assets/pet.webp
```

**在 HTML 中使用**：

```html
<picture>
  <source srcset="assets/pet.webp" type="image/webp">
  <source srcset="assets/pet.png" type="image/png">
  <img src="assets/pet.png" alt="Pet">
</picture>
```

---

### 2. 音频优化

```bash
# 压缩音频（降低比特率）
ffmpeg -i sounds/meow.mp3 -b:a 64k sounds/meow-compressed.mp3
```

---

### 3. 懒加载资源

```javascript
// 懒加载音效
const sounds = {};

function loadSound(name) {
  if (!sounds[name]) {
    sounds[name] = new Audio(`sounds/${name}.mp3`);
  }
  return sounds[name];
}

// 使用
pet.addEventListener('click', () => {
  loadSound('meow').play();
});
```

---

### 4. 使用 CDN

将静态资源上传到 CDN：

```html
<img src="https://cdn.example.com/assets/pet.png" alt="Pet">
```

推荐 CDN：
- [Cloudflare](https://www.cloudflare.com/)
- [jsDelivr](https://www.jsdelivr.com/)
- [Vercel Edge Network](https://vercel.com/docs/edge-network)

---

### 5. 启用缓存

添加 `.htaccess`（Apache）：

```apache
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType image/png "access plus 1 year"
  ExpiresByType audio/mpeg "access plus 1 year"
  ExpiresByType text/css "access plus 1 month"
  ExpiresByType application/javascript "access plus 1 month"
</IfModule>
```

或在 `netlify.toml` 中：

```toml
[[headers]]
  for = "/assets/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000"
```

---

## 故障排查

### 问题 1：404 错误

**症状**：页面无法访问，返回 404

**原因**：
- 仓库名与 homepage 不匹配
- 部署目录错误

**解决**：

检查 `package.json`：

```json
{
  "homepage": "https://yourusername.github.io/repository-name"
}
```

确保 `repository-name` 与 GitHub 仓库名完全一致。

---

### 问题 2：资源路径错误

**症状**：图片、音效加载失败

**原因**：使用了绝对路径

**解决**：

使用相对路径或动态路径：

```javascript
const BASE_PATH = window.location.origin + window.location.pathname.replace(/\/$/, '');
const petImage = `${BASE_PATH}/assets/pet.png`;
```

或在 `index.html` 中使用 `<base>`：

```html
<head>
  <base href="https://yourusername.github.io/my-desktop-pet/">
</head>
```

---

### 问题 3：CORS 错误

**症状**：控制台显示 CORS 错误，音频无法播放

**原因**：跨域资源限制

**解决**：

在服务器配置中添加 CORS 头：

```
Access-Control-Allow-Origin: *
```

对于 GitHub Pages，将资源与页面放在同一域名下。

---

### 问题 4：部署后样式丢失

**症状**：页面显示但无样式

**原因**：CSS 路径错误

**解决**：

确保 `index.html` 中的链接正确：

```html
<link rel="stylesheet" href="./styles.css">
<!-- 不是 -->
<link rel="stylesheet" href="/styles.css">
```

---

### 问题 5：GitHub Pages 未启用

**症状**：部署成功但无法访问

**解决**：

1. 访问仓库 Settings → Pages
2. 确认 Source 设置为 "gh-pages" 分支
3. 或使用 GitHub Actions 部署

---

## 部署清单

部署前检查：

- [ ] 所有图片已优化
- [ ] 音频文件已压缩
- [ ] 路径使用相对路径
- [ ] package.json 中 homepage 配置正确
- [ ] 测试本地构建：`npm run build && npm start`
- [ ] Git 仓库已推送到远程
- [ ] 选择了部署平台
- [ ] DNS 配置正确（如使用自定义域名）
- [ ] HTTPS 已启用

---

## 进阶配置

### 添加分析统计

**Google Analytics**:

```html
<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

**简易统计**:

```javascript
// 记录访问
fetch('https://api.countapi.xyz/hit/my-desktop-pet/visits')
  .then(res => res.json())
  .then(data => console.log('Visits:', data.value));
```

---

### 添加 PWA 支持

创建 `manifest.json`：

```json
{
  "name": "My Desktop Pet",
  "short_name": "Pet",
  "description": "A cute desktop pet",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#4CAF50",
  "icons": [
    {
      "src": "icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

在 `index.html` 中引用：

```html
<link rel="manifest" href="manifest.json">
```

---

## 总结

网页部署是最简单的部署方式，适合：
- 快速分享给他人
- 嵌入个人博客/网站
- 无需安装的体验

推荐平台：
- **GitHub Pages**: 免费，适合开源项目
- **Netlify**: 功能强大，自动化部署
- **Vercel**: 性能最佳，适合高流量

下一步：
- [部署为浏览器插件](extension-deployment.md)
- [部署为桌面应用](desktop-deployment.md)
