[app]

# 应用名称
title = 古诗文背诵检测

# 包名
package.name = poetryrecite

# 包域名
package.domain = org.example

# 源代码目录
source.dir = .

# 源文件包含
source.include_exts = py,png,jpg,kv,atlas,json

# 版本
version = 1.0.0

# 需求
requirements = python3,kivy

# 支持的Android版本
android.api = 31

# 最小SDK版本
android.minapi = 21

# NDK版本
android.ndk = 25b

# 接受Android SDK许可
android.accept_sdk_license = True

# 方向：portrait竖屏，landscape横屏
orientation = portrait

# 全屏
fullscreen = 0

# 图标
# icon.filename = icon.png

# 权限
android.permissions = INTERNET,RECORD_AUDIO

# ABI
android.archs = arm64-v8a,armeabi-v7a

# 允许备份
android.allow_backup = True
