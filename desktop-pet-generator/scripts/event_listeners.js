/**
 * 桌面宠物互动系统 - JavaScript 事件监听器模板
 * 由 interactions.py 自动生成
 *
 * 使用方法:
 * 1. 在 HTML 中引入此文件
 * 2. 创建 PetInteractionSystem 实例
 * 3. 传入宠物元素
 *
 * 示例:
 * const pet = document.getElementById('desktop-pet');
 * const interactionSystem = new PetInteractionSystem(pet);
 */

class PetInteractionSystem {
  constructor(petElement, config = null) {
    this.pet = petElement;
    this.config = config;
    this.interactions = new Map();
    this.longPressTimer = null;
    this.longPressDelay = 800; // 长按延迟 (ms)
    this.isDragging = false;
    this.dragOffset = { x: 0, y: 0 };
    this.currentAnimation = null;
    this.isSleeping = false;

    this.init();
  }

  init() {
    console.log('初始化桌面宠物互动系统...');

    // 加载配置
    if (this.config) {
      this.loadConfig(this.config);
    } else {
      this.loadDefaultConfig();
    }

    // 设置事件监听器
    this.setupEventListeners();

    // 设置默认样式
    this.setupDefaultStyles();

    console.log(`已加载 ${this.interactions.size} 个互动`);
  }

  loadConfig(config) {
    if (config.interactions) {
      config.interactions.forEach(interaction => {
        if (interaction.enabled) {
          this.interactions.set(interaction.name, interaction);
        }
      });
    }
  }

  loadDefaultConfig() {
    // 默认配置将在此处注入
    // 由 Python 生成器填充
    const defaultConfig = {
      interactions: []
    };
    this.loadConfig(defaultConfig);
  }

  setupDefaultStyles() {
    // 确保宠物可拖拽
    this.pet.style.position = 'fixed';
    this.pet.style.cursor = 'grab';
    this.pet.style.userSelect = 'none';
    this.pet.style.transition = 'all 0.3s ease';
  }

  setupEventListeners() {
    // 点击事件
    this.pet.addEventListener('click', (e) => this.handleClick(e));

    // 双击事件
    this.pet.addEventListener('dblclick', (e) => this.handleDoubleClick(e));

    // 右键菜单
    this.pet.addEventListener('contextmenu', (e) => this.handleRightClick(e));

    // 鼠标悬停
    this.pet.addEventListener('mouseenter', (e) => this.handleMouseEnter(e));
    this.pet.addEventListener('mouseleave', (e) => this.handleMouseLeave(e));

    // 拖拽事件
    this.pet.addEventListener('mousedown', (e) => this.handleMouseDown(e));
    document.addEventListener('mousemove', (e) => this.handleMouseMove(e));
    document.addEventListener('mouseup', (e) => this.handleMouseUp(e));

    console.log('事件监听器设置完成');
  }

  // ==================== 事件处理器 ====================

  handleClick(event) {
    if (this.isDragging) return; // 拖拽时不触发点击

    console.log('点击事件触发');
    this.executeInteractions('click', event);
  }

  handleDoubleClick(event) {
    console.log('双击事件触发');
    this.executeInteractions('dblclick', event);
  }

  handleRightClick(event) {
    event.preventDefault();
    console.log('右键事件触发');
    this.executeInteractions('contextmenu', event);
  }

  handleMouseEnter(event) {
    console.log('鼠标进入');
    this.executeInteractions('mouseenter', event);
    this.executeInteractions('hover', event);
  }

  handleMouseLeave(event) {
    console.log('鼠标离开');
    this.executeInteractions('mouseleave', event);
  }

  handleMouseDown(event) {
    if (event.button === 0) { // 左键
      this.isDragging = true;
      const rect = this.pet.getBoundingClientRect();
      this.dragOffset.x = event.clientX - rect.left;
      this.dragOffset.y = event.clientY - rect.top;
      this.pet.style.cursor = 'grabbing';

      // 长按检测
      this.startLongPress(event);
    }
  }

  handleMouseMove(event) {
    if (this.isDragging) {
      this.executeInteractions('drag', event);

      const x = event.clientX - this.dragOffset.x;
      const y = event.clientY - this.dragOffset.y;

      // 边界检测
      const maxX = window.innerWidth - this.pet.offsetWidth;
      const maxY = window.innerHeight - this.pet.offsetHeight;

      this.pet.style.left = Math.max(0, Math.min(x, maxX)) + 'px';
      this.pet.style.top = Math.max(0, Math.min(y, maxY)) + 'px';
    }
  }

  handleMouseUp(event) {
    this.isDragging = false;
    this.pet.style.cursor = 'grab';
    this.cancelLongPress();
  }

  startLongPress(event) {
    this.longPressTimer = setTimeout(() => {
      console.log('长按事件触发');
      this.executeInteractions('longpress', event);
    }, this.longPressDelay);
  }

  cancelLongPress() {
    if (this.longPressTimer) {
      clearTimeout(this.longPressTimer);
      this.longPressTimer = null;
    }
  }

  // ==================== 互动执行 ====================

  executeInteractions(trigger, event) {
    let executed = 0;
    this.interactions.forEach((interaction, name) => {
      if (interaction.trigger === trigger && interaction.enabled) {
        this.executeAction(interaction, event);
        executed++;
      }
    });

    if (executed > 0) {
      console.log(`执行了 ${executed} 个 ${trigger} 互动`);
    }
  }

  executeAction(interaction, event) {
    const { action, effect, sound, feedback, params } = interaction;

    console.log(`执行动作: ${action}`);

    // 播放声音
    if (sound && sound.enabled && sound.file) {
      this.playSound(sound.file, sound.volume);
    }

    // 应用视觉效果
    this.applyVisualEffect(effect);

    // 执行具体动作
    switch (action) {
      case 'playSound':
        if (params.soundFile) {
          this.playSound(params.soundFile, params.volume || 1.0);
        }
        break;

      case 'changeAnimation':
        if (params.animation) {
          this.changeAnimation(params.animation);
        }
        break;

      case 'showText':
        if (params.text) {
          this.showText(params.text, params.duration || 2000);
        }
        break;

      case 'toggleFullscreen':
        this.toggleFullscreen();
        break;

      case 'changeSkin':
        if (params.skin) {
          this.changeSkin(params.skin);
        }
        break;

      case 'movePosition':
        // 拖拽在 handleMouseMove 中处理
        break;

      case 'showMenu':
        this.showContextMenu(event, params.menu || []);
        break;

      case 'hide':
        this.hidePet();
        break;

      case 'openSettings':
        this.openSettings();
        break;

      case 'exit':
        this.exitPet();
        break;

      case 'sleepMode':
        this.enterSleepMode();
        break;

      case 'bounce':
        this.bounce();
        break;

      case 'spin':
        this.spin();
        break;

      case 'shake':
        this.shake();
        break;

      case 'glowEffect':
        this.glowEffect(params);
        break;

      case 'showTooltip':
        this.showTooltip(params.text || '提示信息');
        break;

      default:
        console.warn(`未知动作类型: ${action}`);
    }

    // 显示反馈
    if (feedback && feedback.message) {
      this.showFeedback(feedback.message);
    }
  }

  // ==================== 视觉效果 ====================

  applyVisualEffect(effect) {
    if (!effect || effect.type === 'none') return;

    const { type, duration, easing, params } = effect;

    // 保存当前 transition
    const originalTransition = this.pet.style.transition;
    this.pet.style.transition = `all ${duration}ms ${easing}`;

    switch (type) {
      case 'glow':
        this.pet.style.filter = `drop-shadow(0 0 ${params.glowSize || 10}px ${params.color || 'rgba(255, 255, 255, 0.8)'})`;
        setTimeout(() => {
          this.pet.style.filter = 'none';
          this.pet.style.transition = originalTransition;
        }, duration);
        break;

      case 'pulse':
        const scale = params.scale || 1.1;
        this.pet.style.transform = `scale(${scale})`;
        setTimeout(() => {
          this.pet.style.transform = 'scale(1)';
          this.pet.style.transition = originalTransition;
        }, duration);
        break;

      case 'fade':
        const opacity = params.opacity || 0.3;
        this.pet.style.opacity = opacity;
        setTimeout(() => {
          this.pet.style.opacity = '1';
          this.pet.style.transition = originalTransition;
        }, duration);
        break;

      case 'scale':
        const targetScale = params.scale || 2;
        this.pet.style.transform = `scale(${targetScale})`;
        setTimeout(() => {
          this.pet.style.transform = 'scale(1)';
          this.pet.style.transition = originalTransition;
        }, duration);
        break;

      case 'rotate':
        const rotation = params.rotation || 360;
        this.pet.style.transform = `rotate(${rotation}deg)`;
        setTimeout(() => {
          this.pet.style.transform = 'rotate(0deg)';
          this.pet.style.transition = originalTransition;
        }, duration);
        break;

      case 'shake':
        this.pet.classList.add('shake-animation');
        setTimeout(() => {
          this.pet.classList.remove('shake-animation');
          this.pet.style.transition = originalTransition;
        }, duration);
        break;

      case 'bounce':
        this.pet.classList.add('bounce-animation');
        setTimeout(() => {
          this.pet.classList.remove('bounce-animation');
          this.pet.style.transition = originalTransition;
        }, duration);
        break;

      default:
        console.warn(`未知视觉效果: ${type}`);
    }
  }

  // ==================== 动作实现 ====================

  playSound(file, volume = 1.0) {
    try {
      const audio = new Audio(file);
      audio.volume = Math.max(0, Math.min(1, volume)); // 限制在 0-1 之间
      audio.play().catch(e => console.warn('无法播放声音:', e));
    } catch (error) {
      console.error('播放声音失败:', error);
    }
  }

  changeAnimation(animation) {
    this.currentAnimation = animation;
    this.pet.className = `pet-animation-${animation}`;
    console.log(`切换到动画: ${animation}`);
  }

  showText(text, duration = 2000) {
    // 移除现有的气泡
    const existingBubble = this.pet.querySelector('.speech-bubble');
    if (existingBubble) {
      existingBubble.remove();
    }

    // 创建新的气泡
    const bubble = document.createElement('div');
    bubble.className = 'speech-bubble';
    bubble.textContent = text;
    bubble.style.cssText = `
      position: absolute;
      top: -40px;
      left: 50%;
      transform: translateX(-50%);
      background: white;
      border: 2px solid #333;
      border-radius: 10px;
      padding: 8px 12px;
      font-size: 14px;
      white-space: nowrap;
      box-shadow: 0 2px 8px rgba(0,0,0,0.2);
      animation: fadeIn 0.3s ease;
      z-index: 1000;
    `;

    this.pet.appendChild(bubble);

    setTimeout(() => {
      bubble.style.animation = 'fadeOut 0.3s ease';
      setTimeout(() => bubble.remove(), 300);
    }, duration);
  }

  toggleFullscreen() {
    const currentScale = this.pet.style.transform.includes('scale')
      ? parseFloat(this.pet.style.transform.match(/scale\(([^)]+)\)/)?.[1] || 1)
      : 1;

    const newScale = currentScale === 1 ? 2 : 1;
    this.pet.style.transform = `scale(${newScale})`;
    console.log(`缩放到: ${newScale}x`);
  }

  changeSkin(skin) {
    // 切换皮肤 - 具体实现取决于皮肤系统
    this.pet.dataset.skin = skin;
    console.log(`切换皮肤: ${skin}`);
  }

  showContextMenu(event, menuItems) {
    event.preventDefault();

    // 移除现有菜单
    const existingMenu = document.querySelector('.pet-context-menu');
    if (existingMenu) {
      existingMenu.remove();
    }

    // 创建菜单
    const menu = document.createElement('div');
    menu.className = 'pet-context-menu';
    menu.style.cssText = `
      position: fixed;
      left: ${event.clientX}px;
      top: ${event.clientY}px;
      background: white;
      border: 1px solid #ccc;
      border-radius: 5px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.2);
      z-index: 10000;
      min-width: 120px;
    `;

    // 添加菜单项
    menuItems.forEach((item, index) => {
      const menuItem = document.createElement('div');
      menuItem.textContent = item;
      menuItem.style.cssText = `
        padding: 8px 16px;
        cursor: pointer;
        transition: background 0.2s;
      `;

      menuItem.addEventListener('mouseenter', () => {
        menuItem.style.background = '#f0f0f0';
      });

      menuItem.addEventListener('mouseleave', () => {
        menuItem.style.background = 'white';
      });

      menuItem.addEventListener('click', () => {
        this.handleMenuAction(item);
        menu.remove();
      });

      menu.appendChild(menuItem);
    });

    document.body.appendChild(menu);

    // 点击外部关闭菜单
    setTimeout(() => {
      document.addEventListener('click', () => menu.remove(), { once: true });
    }, 100);
  }

  handleMenuAction(action) {
    console.log(`菜单操作: ${action}`);

    switch (action) {
      case '隐藏':
        this.hidePet();
        break;
      case '设置':
        this.openSettings();
        break;
      case '更换皮肤':
        this.changeSkin('default');
        break;
      case '退出':
        this.exitPet();
        break;
      default:
        console.log(`未处理的菜单操作: ${action}`);
    }
  }

  hidePet() {
    this.pet.style.opacity = '0';
    setTimeout(() => {
      this.pet.style.display = 'none';
    }, 300);
    console.log('宠物已隐藏');
  }

  openSettings() {
    console.log('打开设置面板');
    alert('设置功能待实现');
  }

  exitPet() {
    if (confirm('确定要关闭桌面宠物吗?')) {
      this.pet.remove();
      console.log('宠物已退出');
    }
  }

  enterSleepMode() {
    this.isSleeping = true;
    this.pet.classList.add('sleeping');
    this.pet.style.opacity = '0.6';
    console.log('进入睡眠模式');
  }

  bounce() {
    this.pet.style.animation = 'bounce 0.6s ease';
    setTimeout(() => {
      this.pet.style.animation = '';
    }, 600);
  }

  spin() {
    const currentRotation = this.pet.style.transform.includes('rotate')
      ? parseFloat(this.pet.style.transform.match(/rotate\(([^d]+)deg\)/)?.[1] || 0)
      : 0;

    this.pet.style.transform = `rotate(${currentRotation + 360}deg)`;
    setTimeout(() => {
      this.pet.style.transform = `rotate(${currentRotation}deg)`;
    }, 500);
  }

  shake() {
    this.pet.style.animation = 'shake 0.5s ease';
    setTimeout(() => {
      this.pet.style.animation = '';
    }, 500);
  }

  glowEffect(params = {}) {
    const color = params.color || 'rgba(255, 255, 255, 0.8)';
    const size = params.glowSize || 15;

    this.pet.style.filter = `drop-shadow(0 0 ${size}px ${color})`;
    setTimeout(() => {
      this.pet.style.filter = 'none';
    }, params.duration || 500);
  }

  showTooltip(text) {
    // 创建提示框
    const tooltip = document.createElement('div');
    tooltip.className = 'pet-tooltip';
    tooltip.textContent = text;
    tooltip.style.cssText = `
      position: absolute;
      bottom: 100%;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(0, 0, 0, 0.8);
      color: white;
      padding: 6px 10px;
      border-radius: 5px;
      font-size: 12px;
      white-space: nowrap;
      margin-bottom: 10px;
      pointer-events: none;
    `;

    this.pet.appendChild(tooltip);

    setTimeout(() => tooltip.remove(), 2000);
  }

  showFeedback(message) {
    console.log(`反馈: ${message}`);
    // 可以在这里添加更多的反馈机制
  }

  // ==================== 工具方法 ====================

  enableInteraction(name) {
    const interaction = this.interactions.get(name);
    if (interaction) {
      interaction.enabled = true;
      console.log(`启用互动: ${name}`);
      return true;
    }
    return false;
  }

  disableInteraction(name) {
    const interaction = this.interactions.get(name);
    if (interaction) {
      interaction.enabled = false;
      console.log(`禁用互动: ${name}`);
      return true;
    }
    return false;
  }

  addInteraction(interaction) {
    this.interactions.set(interaction.name, interaction);
    console.log(`添加互动: ${interaction.name}`);
  }

  removeInteraction(name) {
    const result = this.interactions.delete(name);
    if (result) {
      console.log(`移除互动: ${name}`);
    }
    return result;
  }

  getInteraction(name) {
    return this.interactions.get(name);
  }

  getAllInteractions() {
    return Array.from(this.interactions.values());
  }
}

// ==================== CSS 动画 ====================

// 添加 CSS 动画样式
const styleSheet = document.createElement('style');
styleSheet.textContent = `
  @keyframes fadeIn {
    from { opacity: 0; transform: translateX(-50%) translateY(-10px); }
    to { opacity: 1; transform: translateX(-50%) translateY(0); }
  }

  @keyframes fadeOut {
    from { opacity: 1; }
    to { opacity: 0; }
  }

  @keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-20px); }
  }

  @keyframes shake {
    0%, 100% { transform: translateX(0); }
    25% { transform: translateX(-10px); }
    75% { transform: translateX(10px); }
  }

  .bounce-animation {
    animation: bounce 0.6s ease;
  }

  .shake-animation {
    animation: shake 0.5s ease;
  }

  .sleeping {
    filter: brightness(0.7);
  }
`;

document.head.appendChild(styleSheet);

// ==================== 导出 ====================

// 支持模块化导出
if (typeof module !== 'undefined' && module.exports) {
  module.exports = PetInteractionSystem;
}

// 支持全局使用
if (typeof window !== 'undefined') {
  window.PetInteractionSystem = PetInteractionSystem;
}

console.log('桌面宠物互动系统已加载');
