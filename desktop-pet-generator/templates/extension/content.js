// 内容脚本 - 注入到网页中

let petContainer = null;
let isDragging = false;
let currentX, currentY, initialX, initialY;
let xOffset = 100;
let yOffset = 100;
let autoAnimationInterval = null;
let petEnabled = false;
let settings = {
    size: 100,
    speed: 5,
    interval: 10000
};

// 初始化
(async function init() {
    // 加载设置
    const stored = await chrome.storage.local.get({
        petEnabled: false,
        size: 100,
        speed: 5,
        interval: 10
    });

    settings = {
        size: stored.size,
        speed: stored.speed,
        interval: stored.interval * 1000
    };

    petEnabled = stored.petEnabled;

    if (petEnabled) {
        createPet();
    }
})();

// 监听来自 popup 的消息
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    switch (request.action) {
        case 'enablePet':
            if (!petContainer) {
                createPet();
            }
            petEnabled = true;
            break;

        case 'disablePet':
            if (petContainer) {
                removePet();
            }
            petEnabled = false;
            break;

        case 'resetPosition':
            resetPosition();
            break;

        case 'triggerAnimation':
            triggerAnimation(request.animationType);
            break;

        case 'updateSize':
            settings.size = request.value;
            updatePetSize();
            break;

        case 'updateSpeed':
            settings.speed = request.value;
            break;

        case 'updateInterval':
            settings.interval = request.value;
            restartAutoAnimation();
            break;
    }

    sendResponse({ success: true });
});

// 创建宠物
function createPet() {
    if (petContainer) return;

    petContainer = document.createElement('div');
    petContainer.id = 'desktop-pet-container';

    // 创建sprite图像
    const spriteImg = document.createElement('div');
    spriteImg.id = 'pet-sprite';
    spriteImg.style.width = '{{FRAME_WIDTH}}px';
    spriteImg.style.height = '{{FRAME_WIDTH}}px';
    spriteImg.style.background = `url(${chrome.runtime.getURL('sprite.png')}) 0 0 no-repeat`;
    spriteImg.style.imageRendering = 'pixelated';

    petContainer.appendChild(spriteImg);

    // 应用样式
    const style = document.createElement('style');
    style.textContent = `
        #desktop-pet-container {
            position: fixed;
            cursor: move;
            user-select: none;
            z-index: 999999;
            pointer-events: auto;
            transform: scale(${settings.size / 100});
            transform-origin: center center;
        }

        #pet-sprite {
            width: {{FRAME_WIDTH}}px;
            height: {{FRAME_WIDTH}}px;
            background: url(${chrome.runtime.getURL('sprite.png')}) 0 0 no-repeat;
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

        #desktop-pet-container.bounce #pet-sprite {
            animation: sprite-animation 0.4s steps({{FRAME_COUNT}}) infinite,
                       bounce 0.6s ease-in-out infinite;
        }

        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-15px); }
        }

        /* 视觉特效 */
        .heart-effect {
            position: fixed;
            font-size: 20px;
            animation: float-up 1s ease-out forwards;
            pointer-events: none;
            z-index: 1000000;
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
            z-index: 1000000;
        }

        @keyframes float-up-z {
            0% { transform: translate(0, 0) scale(0.5); opacity: 0.8; }
            100% { transform: translate(20px, -40px) scale(1); opacity: 0; }
        }

        /* 右键菜单 */
        .pet-context-menu {
            position: fixed;
            background: white;
            border: 1px solid #ccc;
            border-radius: 8px;
            padding: 5px 0;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 1000001;
            display: none;
            min-width: 150px;
        }

        .pet-context-menu-item {
            padding: 10px 20px;
            cursor: pointer;
            font-size: 14px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            color: #333;
        }

        .pet-context-menu-item:hover {
            background: #f0f0f0;
        }

        .pet-context-menu-separator {
            height: 1px;
            background: #e0e0e0;
            margin: 5px 0;
        }
    `;
    document.head.appendChild(style);

    document.body.appendChild(petContainer);

    // 设置初始位置
    petContainer.style.left = xOffset + 'px';
    petContainer.style.top = yOffset + 'px';

    // 绑定事件
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
        e.stopPropagation();
        showContextMenu(e.clientX, e.clientY);
        resetIdleTimer();
    });

    // 自定义事件
    {{EVENT_LISTENERS}}

    // 启动自动动画和闲置检测
    startAutoAnimation();
    resetIdleTimer();

    console.log('{{PET_NAME}} 已在页面中激活!');
    console.log('可用动画:', animationsConfig ? Object.keys(animationsConfig) : '无');
}

// 移除宠物
function removePet() {
    if (petContainer) {
        petContainer.remove();
        petContainer = null;
    }

    if (autoAnimationInterval) {
        clearInterval(autoAnimationInterval);
        autoAnimationInterval = null;
    }
}

// 拖拽功能
function dragStart(e) {
    if (e.button !== 0) return;

    initialX = e.clientX - xOffset;
    initialY = e.clientY - yOffset;
    isDragging = true;

    // 拖拽时触发 walk 动画
    if (animationsConfig && animationsConfig.walk) {
        switchAnimation('walk');
    }

    resetIdleTimer();
}

function drag(e) {
    if (isDragging && petContainer) {
        e.preventDefault();
        currentX = e.clientX - initialX;
        currentY = e.clientY - initialY;
        xOffset = currentX;
        yOffset = currentY;

        petContainer.style.left = currentX + 'px';
        petContainer.style.top = currentY + 'px';
    }
}

function dragEnd(e) {
    initialX = currentX;
    initialY = currentY;

    if (isDragging) {
        // 停止拖拽后恢复 idle 动画
        if (animationsConfig && animationsConfig.idle) {
            switchAnimation('idle');
        }
    }

    // 延迟重置拖拽状态，防止误触点击事件
    setTimeout(() => {
        isDragging = false;
    }, 100);

    resetIdleTimer();
}

// 重置位置
function resetPosition() {
    if (!petContainer) return;

    xOffset = 100;
    yOffset = 100;
    petContainer.style.left = xOffset + 'px';
    petContainer.style.top = yOffset + 'px';
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

    spriteImg.style.backgroundImage = `url(${chrome.runtime.getURL(config.sprite)})`;

    const duration = config.duration || 0.8;
    const frames = config.frames || 1;
    spriteImg.style.animation = `sprite-animation ${duration}s steps(${frames}) infinite`;

    currentAnimation = type;
    console.log('切换动画:', type, config);
}

// 触发动画
function triggerAnimation(type) {
    if (!petContainer) return;

    switchAnimation(type);
    petContainer.className = type;
    console.log('触发动画:', type);
}

// 更新宠物大小
function updatePetSize() {
    if (!petContainer) return;

    petContainer.style.transform = `scale(${settings.size / 100})`;
}

// 自动动画
function startAutoAnimation() {
    if (autoAnimationInterval) return;

    autoAnimationInterval = setInterval(() => {
        if (!isDragging && petContainer) {
            const animations = ['idle', 'walk', 'jump'];
            const randomAnim = animations[Math.floor(Math.random() * animations.length)];
            triggerAnimation(randomAnim);
        }
    }, settings.interval);
}

function restartAutoAnimation() {
    if (autoAnimationInterval) {
        clearInterval(autoAnimationInterval);
        autoAnimationInterval = null;
    }
    startAutoAnimation();
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

// 右键菜单
function showContextMenu(x, y) {
    // 移除已存在的菜单
    const existingMenu = document.querySelector('.pet-context-menu');
    if (existingMenu) existingMenu.remove();

    const menu = document.createElement('div');
    menu.className = 'pet-context-menu';
    menu.style.left = x + 'px';
    menu.style.top = y + 'px';

    // 根据可用动画生成菜单项
    const menuItems = [];
    if (animationsConfig) {
        if (animationsConfig.eat) menuItems.push({ label: '吃东西', action: 'eat' });
        if (animationsConfig.sleep) menuItems.push({ label: '睡觉', action: 'sleep' });
        if (animationsConfig.celebrate) menuItems.push({ label: '庆祝', action: 'celebrate' });
        if (animationsConfig.play) menuItems.push({ label: '玩耍', action: 'play' });
    }

    if (menuItems.length === 0) {
        menuItems.push(
            { label: '待机', action: 'idle' },
            { label: '跳跃', action: 'jump' }
        );
    }

    let menuHTML = '';
    menuItems.forEach(item => {
        menuHTML += `<div class="pet-context-menu-item" data-action="${item.action}">${item.label}</div>`;
    });
    menuHTML += '<div class="pet-context-menu-separator"></div>';
    menuHTML += '<div class="pet-context-menu-item" data-action="reset">重置位置</div>';

    menu.innerHTML = menuHTML;
    document.body.appendChild(menu);
    menu.style.display = 'block';

    // 菜单项点击事件
    menu.querySelectorAll('.pet-context-menu-item').forEach(item => {
        item.addEventListener('click', () => {
            const action = item.dataset.action;
            if (action === 'reset') {
                resetPosition();
            } else {
                triggerAnimation(action);
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

// 动画配置 - 从生成器注入
const animationsConfig = {{ANIMATIONS_CONFIG}};

let currentAnimation = 'idle';
let pressTimer = null;
let clickCount = 0;
let clickTimer = null;
let idleTimer = null;
let sleepTimer = null;
let lastInteractionTime = Date.now();
