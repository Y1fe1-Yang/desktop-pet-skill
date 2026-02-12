// 后台服务脚本

// 安装时初始化
chrome.runtime.onInstalled.addListener((details) => {
    if (details.reason === 'install') {
        console.log('{{PET_NAME}} 扩展已安装!');

        // 设置默认配置
        chrome.storage.local.set({
            petEnabled: false,
            size: 100,
            speed: 5,
            interval: 10
        });

        // 打开欢迎页面
        chrome.tabs.create({
            url: 'welcome.html'
        });
    } else if (details.reason === 'update') {
        console.log('{{PET_NAME}} 扩展已更新!');
    }
});

// 监听扩展图标点击
chrome.action.onClicked.addListener(async (tab) => {
    // 获取当前状态
    const { petEnabled } = await chrome.storage.local.get({ petEnabled: false });

    // 切换状态
    const newState = !petEnabled;
    await chrome.storage.local.set({ petEnabled: newState });

    // 发送消息到当前标签页
    try {
        await chrome.tabs.sendMessage(tab.id, {
            action: newState ? 'enablePet' : 'disablePet'
        });

        // 更新图标
        updateIcon(newState);
    } catch (error) {
        console.error('无法向标签页发送消息:', error);
    }
});

// 监听来自 content script 的消息
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'getPetStatus') {
        chrome.storage.local.get({ petEnabled: false }, (result) => {
            sendResponse({ enabled: result.petEnabled });
        });
        return true; // 保持消息通道打开
    }

    if (request.action === 'logEvent') {
        console.log(`[${request.event}]`, request.data);
        sendResponse({ success: true });
    }
});

// 监听标签页更新
chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
    // 页面加载完成时，检查是否需要启用宠物
    if (changeInfo.status === 'complete') {
        const { petEnabled } = await chrome.storage.local.get({ petEnabled: false });

        if (petEnabled) {
            try {
                await chrome.tabs.sendMessage(tabId, {
                    action: 'enablePet'
                });
            } catch (error) {
                // 某些页面可能无法注入脚本（如 chrome:// 页面）
                console.log('无法在此页面启用宠物:', tab.url);
            }
        }
    }
});

// 更新扩展图标
function updateIcon(enabled) {
    const iconPath = enabled ? 'icons/icon-active.png' : 'icons/icon.png';

    chrome.action.setIcon({
        path: {
            16: iconPath,
            48: iconPath,
            128: iconPath
        }
    });
}

// 定期任务（可选）
chrome.alarms.create('dailyReset', {
    delayInMinutes: 1440, // 24 小时
    periodInMinutes: 1440
});

chrome.alarms.onAlarm.addListener((alarm) => {
    if (alarm.name === 'dailyReset') {
        console.log('执行每日重置任务');
        // 可以在这里添加每日重置逻辑
    }
});

// 监听存储变化
chrome.storage.onChanged.addListener((changes, namespace) => {
    if (namespace === 'local') {
        for (let [key, { oldValue, newValue }] of Object.entries(changes)) {
            console.log(`设置已更改: ${key}`, { oldValue, newValue });
        }
    }
});

console.log('{{PET_NAME}} 后台服务已启动');
