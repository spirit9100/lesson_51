[app]
title = AI Chat
package.name = aichat
package.domain = org.aichat
source.dir = src
source.include_exts = py,png,jpg,kv,atlas,json,env
version = 1.0
requirements = python3,\
    flet==0.24.1,\
    kivy,\
    asyncio,\
    aiohttp,\
    certifi,\
    python-dotenv,\
    requests,\
    datetime,\
    charset_normalizer,\
    multidict,\
    yarl,\
    attrs,\
    async_timeout,\
    frozenlist

android.permissions = INTERNET
android.arch = arm64-v8a
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.accept_sdk_license = True

orientation = portrait
fullscreen = 0
android.presplash_color = #1E1E1E
p4a.branch = master
p4a.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 1
