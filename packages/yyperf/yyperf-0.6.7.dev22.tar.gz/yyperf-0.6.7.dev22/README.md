# yyperf
编辑器能够提供辅助编写脚本，查看组件信息，调试代码，采集性能数据等功能。

## 安装
依赖项目

- Python3.6+
  - [uiautomator2](https://github.com/openatx/uiautomator2)
  - [facebook-wda](https://github.com/openatx/facebook-wda)
  - [weditor](https://github.com/openatx/weditor)
  - [tidevice](https://github.com/alibaba/taobao-iphone-device)
  - [py-ios-device](https://github.com/YueChen-C/py-ios-device)

> Only tested in `Google Chrome`, _IE_ seems not working well.

```bash
git clone https://github.com/mrx1203
pip3 install -r requirements.txt
python3 setup.py install #如果提示没有权限，则加--user
```

## 使用方法
```bash
yyperf # 启动server并打开浏览器
```
创建桌面快捷方式（仅限Windows）

```bash
yyperf --shortcut
```

更多选项通过 `yyperf --help` 查看

如果浏览器没有自动打开，可以手动访问 <http://localhost:17310>

## Windows下使用
windows下，如果是安装到用户目录下的site-packages，则需要将用户目录下的python3.x\Scripts目录添加到环境变量。
windows采集ios，需要安装iTunes。

## 执行Android用例
1. 在控件查看中，选择Android，输入设备id(通过adb devices查看)，点击Connect.
2. 录制用例，
3. 点击右边工具栏的三角形按钮，执行用例


## 执行iOS用例

1. 首先安装WDA，不知道怎么安装的可以联系周云鹏。
2. 获取WDA的bundleid:`tidevice applist` 在输出结果中找到WebDriverAgentRunner-Runner 对应的bundleid
3. 启动WDA：`tidevice wdaproxy -B com.yy.perftest.WebDriverAgentRunner.xctrunner -p 6103` 。其中com.yy.perftest.WebDriverAgentRunner.xctrunner为bundleid
4. 在控件查看中，选择ios，输入http://localhost:6103 .点击Connect.
5. 录制用例
6. 点击右边工具栏的三角形按钮，执行用例


## 性能采集
1. 选择测试设备（可以点击 更新设备列表 刷新后面接入的设备）
2. 选择测试app(如果没有获取到app列表，试试切换测试设备)
3. 点击开始采集数据，等待一段时间后（10s左右），数据实时显示，也可以通过yyperf启动窗口的日志找到数据保存路径。

## 常用快捷键

**Mac**

- Command+Enter: 运行编辑器中所有代码
- Command+SHIFT+Enter: 运行选中代码或光标所在行代码

**Windows**

- CTRL+Enter: 运行编辑器中所有代码
- CTRL+SHIFT+Enter: 运行选中代码或光标所在行代码

## LICENSE
[MIT](LICENSE)
