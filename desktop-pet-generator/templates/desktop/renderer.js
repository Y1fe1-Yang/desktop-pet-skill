const { ipcRenderer } = require('electron');

// 动画配置 - 从生成器注入
const animationsConfig = {{ANIMATIONS_CONFIG}};

// 宠物状态
let isDragging = false;
let currentX, currentY;
let initialX, initialY;
let xOffset = 0;
let yOffset = 0;
let autoAnimationInterval = null;
let currentAnimation = 'idle';
let pressTimer = null;
let clickCount = 0;
let clickTimer = null;
let idleTimer = null;
let sleepTimer = null;
let lastInteractionTime = Date.now();
let settings = {
    size: 200,
    speed: 5,
    interval: 10000
};

// DOM 元素
let petContainer = null;

// 初始化
document.addEventListener('DOMContentLoaded', async () => {
    petContainer = document.getElementById('pet');

    if (!petContainer) {
        console.error('找不到宠物容器元素');
        return;
    }

    // 加载设置
    const savedSettings = await ipcRenderer.invoke('get-settings');
    settings = { ...settings, ...savedSettings };

    // 设置初始样式
    setupPetStyles();

    // 绑定事件
    setupEventListeners();

    // 启动自动动画
    startAutoAnimation();

    console.log('{{PET_NAME}} 渲染进程已初始化');
});

// 设置宠物样式
function setupPetStyles() {
    if (!petContainer) return;

    // 创建sprite图像
    const spriteImg = document.createElement('div');
    spriteImg.id = 'pet-sprite';
    petContainer.appendChild(spriteImg);

    // 应用自定义样式
    const style = document.createElement('style');
    style.textContent = `
        body {
            margin: 0;
            padding: 0;
            overflow: hidden;
            background: transparent;
            cursor: move;
        }

        #pet {
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            user-select: none;
        }

        #pet-sprite {
            width: {{FRAME_WIDTH}}px;
            height: {{FRAME_WIDTH}}px;
            background: url('sprite.png') 0 0 no-repeat;
            image-rendering: pixelated;
            animation: sprite-animation 0.8s steps({{FRAME_COUNT}}) infinite;
        }

        @keyframes sprite-animation {
            from { background-position: 0 0; }
            to { background-position: -{{SPRITE_WIDTH}}px 0; }
        }

        #pet-sprite:hover {
            transform: scale(1.1);
            transition: transform 0.2s;
        }

        #pet.bounce #pet-sprite {
            animation: sprite-animation 0.4s steps({{FRAME_COUNT}}) infinite,
                       bounce 0.6s ease-in-out infinite;
        }

        #pet.jump #pet-sprite {
            animation: sprite-animation 0.3s steps({{FRAME_COUNT}}) 1,
                       jump 0.5s ease-in-out 1;
        }

        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-20px); }
        }

        @keyframes jump {
            0% { transform: translateY(0) scale(1); }
            50% { transform: translateY(-40px) scale(1.1); }
            100% { transform: translateY(0) scale(1); }
        }

        /* 视觉特效 */
        .heart-effect {
            position: fixed;
            font-size: 20px;
            animation: float-up 1s ease-out forwards;
            pointer-events: none;
            z-index: 10000;
        }

        @keyframes float-up {
            from { transform: translateY(0); opacity: 1; }
            to { transform: translateY(-50px); opacity: 0; }
        }

        .sleep-z {
            position: fixed;
            font-size: 24px;
            animation: float-up-z 2s ease-out infinite;
            pointer-events: none;
            z-index: 10000;
        }

        @keyframes float-up-z {
            0% { transform: translate(0, 0) scale(0.5); opacity: 0.8; }
            100% { transform: translate(20px, -40px) scale(1); opacity: 0; }
        }

        /* 右键菜单 */
        .context-menu {
            position: fixed;
            background: white;
            border: 1px solid #ccc;
            border-radius: 5px;
            padding: 5px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            z-index: 10000;
            display: none;
        }

        .context-menu-item {
            padding: 8px 20px;
            cursor: pointer;
            font-size: 14px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }

        .context-menu-item:hover {
            background: #f0f0f0;
        }

        .context-menu-separator {
            height: 1px;
            background: #e0e0e0;
            margin: 5px 0;
        }
    `;
    document.head.appendChild(style);
}

// 设置事件监听器
function setupEventListeners() {
    if (!petContainer) return;

    // 拖拽事件
    petContainer.addEventListener('mousedown', dragStart);
    document.addEventListener('mousemove', drag);
    document.addEventListener('mouseup', dragEnd);

    // 点击和双击处理
    petContainer.addEventListener('click', (e) => {
        if (isDragging) return;

        clickCount++;

        if (clickCount === 1) {
            clickTimer = setTimeout(() => {
                // 单击 - 触发 jump 动画
                switchAnimation('jump');
                clickCount = 0;
            }, 300);
        } else if (clickCount === 2) {
            // 双击 - 触发 happy 动画
            clearTimeout(clickTimer);
            switchAnimation('happy');
            clickCount = 0;
        }

        resetIdleTimer();
    });

    // 长按检测
    petContainer.addEventListener('mousedown', (e) => {
        if (e.button === 0) {
            pressTimer = setTimeout(() => {
                switchAnimation('pet');
                showHearts();
            }, 2000);
        }
    });

    petContainer.addEventListener('mouseup', () => {
        if (pressTimer) {
            clearTimeout(pressTimer);
            pressTimer = null;
        }
    });

    // 悬停效果
    petContainer.addEventListener('mouseenter', () => {
        if (!isDragging && animationsConfig) {
            const hoverAnim = animationsConfig.curious ? 'curious' : (animationsConfig.happy ? 'happy' : null);
            if (hoverAnim) switchAnimation(hoverAnim);
        }
        resetIdleTimer();
    });

    // 右键菜单
    petContainer.addEventListener('contextmenu', (e) => {
        e.preventDefault();
        showContextMenu(e.clientX, e.clientY);
        resetIdleTimer();
    });

    // 自定义事件监听器
    {{EVENT_LISTENERS}}

    // 键盘快捷键
    document.addEventListener('keydown', (e) => {
        // 数字键 1-9 切换动画
        if (e.key >= '1' && e.key <= '9' && animationsConfig) {
            const animKeys = Object.keys(animationsConfig);
            const index = parseInt(e.key) - 1;
            if (index < animKeys.length) {
                switchAnimation(animKeys[index]);
                resetIdleTimer();
            }
            return;
        }

        switch (e.key) {
            case 'Escape':
                ipcRenderer.send('quit-app');
                break;
            case 'r':
            case 'R':
                if (e.ctrlKey || e.metaKey) {
                    e.preventDefault();
                    ipcRenderer.send('restart-app');
                }
                break;
            case ' ':
                triggerRandomAnimation();
                resetIdleTimer();
                break;
        }
    });
}

// 拖拽功能
function dragStart(e) {
    if (e.button !== 0) return;

    const bounds = petContainer.getBoundingClientRect();
    initialX = e.clientX - xOffset;
    initialY = e.clientY - yOffset;
    isDragging = true;

    // 拖拽时触发 walk 动画
    if (animationsConfig && animationsConfig.walk) {
        switchAnimation('walk');
    }

    petContainer.style.cursor = 'grabbing';
    resetIdleTimer();
}

function drag(e) {
    if (isDragging) {
        e.preventDefault();
        currentX = e.clientX - initialX;
        currentY = e.clientY - initialY;

        // 通知主进程保存位置
        const windowPos = {
            x: e.screenX - e.clientX,
            y: e.screenY - e.clientY
        };

        ipcRenderer.send('save-position', windowPos);
    }
}

function dragEnd(e) {
    if (isDragging) {
        initialX = currentX;
        initialY = currentY;
        isDragging = false;

        // 停止拖拽后恢复 idle 动画
        if (animationsConfig && animationsConfig.idle) {
            switchAnimation('idle');
        }

        petContainer.style.cursor = 'move';
        resetIdleTimer();
    }
}

// 动画切换功能
function switchAnimation(type) {
    if (!petContainer) return;
    if (!animationsConfig || !animationsConfig[type]) {
        console.warn('动画类型不存在:', type);
        return;
    }

    const config = animationsConfig[type];
    const spriteImg = petContainer.querySelector('#pet-sprite');
    if (!spriteImg) return;

    spriteImg.style.backgroundImage = `url('${config.sprite}')`;

    const duration = config.duration || 0.8;
    const frames = config.frames || 1;
    spriteImg.style.animation = `sprite-animation ${duration}s steps(${frames}) infinite`;

    currentAnimation = type;
    console.log('切换动画:', type, config);
}

// 动画控制
function triggerAnimation(type) {
    if (!petContainer) return;

    switchAnimation(type);
    petContainer.className = type;
    ipcRenderer.send('trigger-animation', type);

    console.log('触发动画:', type);
}

function triggerRandomAnimation() {
    if (animationsConfig) {
        const animKeys = Object.keys(animationsConfig).filter(
            key => !['walk'].includes(key)
        );
        if (animKeys.length > 0) {
            const randomAnim = animKeys[Math.floor(Math.random() * animKeys.length)];
            triggerAnimation(randomAnim);
        }
    } else {
        const animations = ['idle', 'walk', 'jump', 'sleep'];
        const randomAnim = animations[Math.floor(Math.random() * animations.length)];
        triggerAnimation(randomAnim);
    }
}

// 自动动画
function startAutoAnimation() {
    if (autoAnimationInterval) return;

    autoAnimationInterval = setInterval(() => {
        if (!isDragging) {
            triggerRandomAnimation();
        }
    }, settings.interval);
}

function stopAutoAnimation() {
    if (autoAnimationInterval) {
        clearInterval(autoAnimationInterval);
        autoAnimationInterval = null;
    }
}

function restartAutoAnimation() {
    stopAutoAnimation();
    startAutoAnimation();
}

// 右键菜单
function showContextMenu(x, y) {
    // 移除已存在的菜单
    const existingMenu = document.querySelector('.context-menu');
    if (existingMenu) {
        existingMenu.remove();
    }

    const menu = document.createElement('div');
    menu.className = 'context-menu';
    menu.style.left = x + 'px';
    menu.style.top = y + 'px';

    // 根据可用动画生成菜单项
    let menuHTML = '';
    if (animationsConfig) {
        Object.keys(animationsConfig).forEach(animKey => {
            const labels = {
                idle: '待机',
                walk: '走路',
                jump: '跳跃',
                sleep: '睡觉',
                eat: '吃东西',
                celebrate: '庆祝',
                play: '玩耍',
                happy: '开心',
                curious: '好奇',
                pet: '抚摸'
            };
            const label = labels[animKey] || animKey;
            menuHTML += `<div class="context-menu-item" data-action="${animKey}">${label}</div>`;
        });
    } else {
        menuHTML = `
            <div class="context-menu-item" data-action="idle">待机</div>
            <div class="context-menu-item" data-action="walk">走路</div>
            <div class="context-menu-item" data-action="jump">跳跃</div>
            <div class="context-menu-item" data-action="sleep">睡觉</div>
        `;
    }

    menuHTML += `
        <div class="context-menu-separator"></div>
        <div class="context-menu-item" data-action="reset">重置位置</div>
        <div class="context-menu-separator"></div>
        <div class="context-menu-item" data-action="quit">退出</div>
    `;

    menu.innerHTML = menuHTML;
    document.body.appendChild(menu);
    menu.style.display = 'block';

    // 菜单项点击事件
    menu.querySelectorAll('.context-menu-item').forEach(item => {
        item.addEventListener('click', () => {
            const action = item.dataset.action;

            switch (action) {
                case 'reset':
                    ipcRenderer.send('save-position', { x: 100, y: 100 });
                    break;
                case 'quit':
                    ipcRenderer.send('quit-app');
                    break;
                default:
                    triggerAnimation(action);
                    break;
            }

            menu.remove();
        });
    });

    // 点击其他地方关闭菜单
    setTimeout(() => {
        document.addEventListener('click', function closeMenu(e) {
            if (!menu.contains(e.target)) {
                menu.remove();
                document.removeEventListener('click', closeMenu);
            }
        });
    }, 0);
}

// 显示爱心特效
function showHearts() {
    if (!petContainer) return;

    const hearts = ['❤️', '💕', '💖', '💗'];
    const rect = petContainer.getBoundingClientRect();

    for (let i = 0; i < 3; i++) {
        setTimeout(() => {
            const heart = document.createElement('div');
            heart.className = 'heart-effect';
            heart.textContent = hearts[Math.floor(Math.random() * hearts.length)];
            heart.style.left = (rect.left + 20 + Math.random() * 40) + 'px';
            heart.style.top = (rect.top + 10) + 'px';
            document.body.appendChild(heart);

            setTimeout(() => heart.remove(), 1000);
        }, i * 200);
    }
}

// 显示睡眠 Z 符号
function showSleepZ() {
    if (!petContainer) return;

    const rect = petContainer.getBoundingClientRect();
    const z = document.createElement('div');
    z.className = 'sleep-z';
    z.textContent = 'Z';
    z.style.left = (rect.left + 50) + 'px';
    z.style.top = (rect.top - 10) + 'px';
    document.body.appendChild(z);

    setTimeout(() => z.remove(), 2000);
}

// 闲置检测
function resetIdleTimer() {
    lastInteractionTime = Date.now();

    if (idleTimer) clearTimeout(idleTimer);
    if (sleepTimer) clearTimeout(sleepTimer);

    // 5秒后进入 idle
    idleTimer = setTimeout(() => {
        if (!isDragging && animationsConfig && animationsConfig.idle) {
            switchAnimation('idle');
        }
    }, 5000);

    // 1分钟后进入 sleep
    sleepTimer = setTimeout(() => {
        if (!isDragging && animationsConfig && animationsConfig.sleep) {
            switchAnimation('sleep');
            // 定期显示 Z 符号
            const sleepInterval = setInterval(() => {
                if (Date.now() - lastInteractionTime >= 60000) {
                    showSleepZ();
                } else {
                    clearInterval(sleepInterval);
                }
            }, 2000);
        }
    }, 60000);
}

// 日志函数
function log(message) {
    console.log(message);
    ipcRenderer.send('log', message);
}

// 导出函数供外部调用
window.petAPI = {
    triggerAnimation,
    triggerRandomAnimation,
    switchAnimation,
    startAutoAnimation,
    stopAutoAnimation,
    restartAutoAnimation,
    showHearts,
    showSleepZ,
    resetIdleTimer,
    log
};

// 初始化
if (animationsConfig && animationsConfig.idle) {
    setTimeout(() => {
        switchAnimation('idle');
    }, 100);
}
resetIdleTimer();

console.log('{{PET_NAME}} 已加载完成');
console.log('可用动画:', animationsConfig ? Object.keys(animationsConfig) : '无');
console.log('快捷键提示: 1-9 数字键切换动画, 空格随机动画, ESC 退出');
