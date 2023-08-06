# yyperf
[![image](https://img.shields.io/pypi/v/weditor.svg?style=flat-square)](https://pypi.python.org/pypi/weditor)
[![image](https://img.shields.io/github/stars/alibaba/web-editor.svg?style=social&label=Star&style=flat-square)](https://github.com/alibaba/web-editor)
[![image](https://travis-ci.org/alibaba/web-editor.svg?branch=master)](https://travis-ci.org/alibaba/web-editor)

[中文文档](README.md)

This project is subproject for smart phone test framework [openatx](https://github.com/openatx)
for easily use web browser to edit UI scripts.

Screenshot

![screenshot](./screenshot.jpg)

## Installation
Dependencies

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
python3 setup.py install --user
```

## Usage
Create Shortcut in Desktop (Only windows)

```
yyperf --shortcut
```

By click shortcut or run in command line

```
yyperf
```

This command will start a local server with port 17310,
and then open a browser tab for you to editor you code.

Port 17310 is to memorize the created day -- 2017/03/10

To see more usage run `yyperf -h`

## Hotkeys(Both Mac and Win)
- Right click screen: `Dump Hierarchy`

### Hotkeys(only Mac)
- Command+Enter: Run the whole code
- Command+Shift+Enter: Run selected code or current line if not selected

### Hotkeys(only Win)
- Ctrl+Enter: Run the whole code
- Ctrl+Shift+Enter: Run selected code or current line if not selected

## LICENSE
[MIT](LICENSE)
