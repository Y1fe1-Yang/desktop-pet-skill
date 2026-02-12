const { app, BrowserWindow, ipcMain, Menu, Tray, screen } = require('electron');
const path = require('path');

let mainWindow = null;
let tray = null;
let petSettings = {
    x: 100,
    y: 100,
    size: 200,
    alwaysOnTop: true,
    clickThrough: false
};

// 创建主窗口
function createWindow() {
    const { width, height } = screen.getPrimaryDisplay().workAreaSize;

    mainWindow = new BrowserWindow({
        width: petSettings.size,
        height: petSettings.size,
        x: petSettings.x,
        y: petSettings.y,
        frame: false,
        transparent: true,
        alwaysOnTop: petSettings.alwaysOnTop,
        skipTaskbar: true,
        resizable: false,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });

    mainWindow.loadFile('index.html');

    // 设置点击穿透
    if (petSettings.clickThrough) {
        mainWindow.setIgnoreMouseEvents(true, { forward: true });
    }

    // 保持窗口在所有桌面可见（macOS）
    if (process.platform === 'darwin') {
        mainWindow.setVisibleOnAllWorkspaces(true, { visibleOnFullScreen: true });
    }

    // 窗口关闭时的处理
    mainWindow.on('closed', () => {
        mainWindow = null;
    });

    // 开发模式下打开开发者工具
    if (process.env.NODE_ENV === 'development') {
        mainWindow.webContents.openDevTools({ mode: 'detach' });
    }

    console.log('{{PET_NAME}} 窗口已创建');
}

// 创建系统托盘
function createTray() {
    const iconPath = path.join(__dirname, 'assets', 'tray-icon.png');
    tray = new Tray(iconPath);

    const contextMenu = Menu.buildFromTemplate([
        {
            label: '{{PET_NAME}}',
            enabled: false
        },
        { type: 'separator' },
        {
            label: '显示宠物',
            click: () => {
                if (mainWindow) {
                    mainWindow.show();
                } else {
                    createWindow();
                }
            }
        },
        {
            label: '隐藏宠物',
            click: () => {
                if (mainWindow) {
                    mainWindow.hide();
                }
            }
        },
        { type: 'separator' },
        {
            label: '置顶',
            type: 'checkbox',
            checked: petSettings.alwaysOnTop,
            click: (menuItem) => {
                petSettings.alwaysOnTop = menuItem.checked;
                if (mainWindow) {
                    mainWindow.setAlwaysOnTop(menuItem.checked);
                }
            }
        },
        {
            label: '点击穿透',
            type: 'checkbox',
            checked: petSettings.clickThrough,
            click: (menuItem) => {
                petSettings.clickThrough = menuItem.checked;
                if (mainWindow) {
                    mainWindow.setIgnoreMouseEvents(menuItem.checked, { forward: true });
                }
            }
        },
        { type: 'separator' },
        {
            label: '重置位置',
            click: () => {
                if (mainWindow) {
                    mainWindow.setPosition(100, 100);
                }
            }
        },
        { type: 'separator' },
        {
            label: '退出',
            click: () => {
                app.quit();
            }
        }
    ]);

    tray.setToolTip('{{PET_NAME}} 桌面宠物');
    tray.setContextMenu(contextMenu);

    // 双击托盘图标显示/隐藏窗口
    tray.on('double-click', () => {
        if (mainWindow) {
            if (mainWindow.isVisible()) {
                mainWindow.hide();
            } else {
                mainWindow.show();
            }
        }
    });
}

// 应用准备就绪
app.whenReady().then(() => {
    createWindow();
    createTray();

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
});

// 所有窗口关闭时
app.on('window-all-closed', () => {
    // macOS 上除非用户明确退出，否则保持应用运行
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

// IPC 通信处理

// 保存位置
ipcMain.on('save-position', (event, { x, y }) => {
    petSettings.x = x;
    petSettings.y = y;
    console.log('位置已保存:', x, y);
});

// 获取设置
ipcMain.handle('get-settings', async () => {
    return petSettings;
});

// 更新设置
ipcMain.on('update-settings', (event, settings) => {
    petSettings = { ...petSettings, ...settings };

    if (mainWindow) {
        if (settings.alwaysOnTop !== undefined) {
            mainWindow.setAlwaysOnTop(settings.alwaysOnTop);
        }
        if (settings.clickThrough !== undefined) {
            mainWindow.setIgnoreMouseEvents(settings.clickThrough, { forward: true });
        }
        if (settings.size !== undefined) {
            mainWindow.setSize(settings.size, settings.size);
        }
    }

    console.log('设置已更新:', petSettings);
});

// 触发动画
ipcMain.on('trigger-animation', (event, animationType) => {
    console.log('触发动画:', animationType);
    // 动画由渲染进程处理
});

// 退出应用
ipcMain.on('quit-app', () => {
    app.quit();
});

// 重启应用
ipcMain.on('restart-app', () => {
    app.relaunch();
    app.quit();
});

// 获取屏幕信息
ipcMain.handle('get-screen-bounds', () => {
    return screen.getPrimaryDisplay().bounds;
});

// 日志记录
ipcMain.on('log', (event, message) => {
    console.log('[Renderer]', message);
});

console.log('{{PET_NAME}} 主进程已启动');
