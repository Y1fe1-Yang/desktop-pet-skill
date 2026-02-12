// 弹窗控制脚本

let petEnabled = false;

// 初始化
document.addEventListener('DOMContentLoaded', async () => {
    // 从存储加载设置
    const settings = await chrome.storage.local.get({
        petEnabled: false,
        size: 100,
        speed: 5,
        interval: 10
    });

    petEnabled = settings.petEnabled;
    updateUI();

    // 设置滑块值
    document.getElementById('sizeSlider').value = settings.size;
    document.getElementById('speedSlider').value = settings.speed;
    document.getElementById('intervalSlider').value = settings.interval;

    updateValueDisplays();
});

// 启用/禁用宠物
document.getElementById('togglePet').addEventListener('click', async () => {
    petEnabled = !petEnabled;

    await chrome.storage.local.set({ petEnabled });

    // 向当前标签页发送消息
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    chrome.tabs.sendMessage(tab.id, {
        action: petEnabled ? 'enablePet' : 'disablePet'
    });

    updateUI();
});

// 重置位置
document.getElementById('resetPosition').addEventListener('click', async () => {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    chrome.tabs.sendMessage(tab.id, { action: 'resetPosition' });
});

// 动画控制
document.getElementById('idleAnim').addEventListener('click', () => {
    sendAnimation('idle');
});

document.getElementById('walkAnim').addEventListener('click', () => {
    sendAnimation('walk');
});

document.getElementById('jumpAnim').addEventListener('click', () => {
    sendAnimation('jump');
});

document.getElementById('sleepAnim').addEventListener('click', () => {
    sendAnimation('sleep');
});

async function sendAnimation(type) {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    chrome.tabs.sendMessage(tab.id, {
        action: 'triggerAnimation',
        animationType: type
    });
}

// 设置滑块
document.getElementById('sizeSlider').addEventListener('input', async (e) => {
    const value = e.target.value;
    document.getElementById('sizeValue').textContent = value + '%';

    await chrome.storage.local.set({ size: parseInt(value) });

    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    chrome.tabs.sendMessage(tab.id, {
        action: 'updateSize',
        value: parseInt(value)
    });
});

document.getElementById('speedSlider').addEventListener('input', async (e) => {
    const value = e.target.value;
    document.getElementById('speedValue').textContent = value;

    await chrome.storage.local.set({ speed: parseInt(value) });

    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    chrome.tabs.sendMessage(tab.id, {
        action: 'updateSpeed',
        value: parseInt(value)
    });
});

document.getElementById('intervalSlider').addEventListener('input', async (e) => {
    const value = e.target.value;
    document.getElementById('intervalValue').textContent = value + 's';

    await chrome.storage.local.set({ interval: parseInt(value) });

    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    chrome.tabs.sendMessage(tab.id, {
        action: 'updateInterval',
        value: parseInt(value) * 1000
    });
});

// 更新UI
function updateUI() {
    const toggleBtn = document.getElementById('togglePet');
    const status = document.getElementById('status');

    if (petEnabled) {
        toggleBtn.textContent = '禁用宠物';
        toggleBtn.classList.remove('off');
        status.textContent = '宠物状态: 已激活';
        status.classList.add('active');
    } else {
        toggleBtn.textContent = '启用宠物';
        toggleBtn.classList.add('off');
        status.textContent = '宠物状态: 未激活';
        status.classList.remove('active');
    }
}

// 更新值显示
function updateValueDisplays() {
    document.getElementById('sizeValue').textContent =
        document.getElementById('sizeSlider').value + '%';
    document.getElementById('speedValue').textContent =
        document.getElementById('speedSlider').value;
    document.getElementById('intervalValue').textContent =
        document.getElementById('intervalSlider').value + 's';
}
