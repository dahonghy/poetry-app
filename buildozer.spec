[app]

# (str) Title of your application
title = 高中古诗文背诵检测

# (str) Package name
package.name = poetryapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json,ttf,otf,pdf

# (str) Application versioning
version = 1.0.0

# (list) Application requirements
requirements = python3,kivy,pyjnius,android

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/icon.png

# (str) Supported orientation (landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) If True, then skip trying to update the Android sdk
android.skip_update = False

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True

# (str) The Android arch to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) Android entry point, default is ok for Kivy-based apps
android.entrypoint = org.kivy.android.PythonActivity

# (str) Full path to the file containing the FileProvider paths XML
# This is needed for Android 7.0+ to share files between apps
android.fileprovider = %(source.dir)s/file_paths.xml

# (str) The Android logcat filters to use
#android.logcat_filters = *:D python:D

# (bool) enables Android broadcast receivers
android.broadcast_receiver = False

# (bool) enables Android service
android.service = False

# (str) The Android additional libraries to copy
#android.add_libs_armeabi = libs/android/*.so

# (str) The Android meta data to add to the AndroidManifest.xml
#android.meta_data = com.android.vending.license=com.google.android.vending.licensing.ILicensingService

# (str) The Android additional tags to add to the AndroidManifest.xml
#android.manifest_placeholders = [android:largeHeap="true"]

# (str) Presplash background color (for new android toolchain)
#android.presplash_color = #FFFFFF

# (list) Android wakelock modes, can be 'partial', 'full' or 'none'
android.wakelock = partial

# (list) Android Java files to add to the project
#android.add_src =

# (list) Android aar files to add to the project
#android.add_aars =

# (list) Android gradle dependencies to add
android.gradle_dependencies = androidx.core:core:1.10.0

# (bool) Enable verbose logging for the compilation
verbose = False

# (bool) Copy library instead of making a libpython*.so
#android.copy_libs = 1

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
