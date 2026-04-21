# -*- coding: utf-8 -*-
"""
高中古诗文背诵检测系统 - Kivy手机版（调试版）
添加日志定位闪退原因
"""

import os
import sys
import traceback

# 日志文件
LOG_FILE = "/sdcard/poetry_app.log"

def log(msg):
    """写入日志"""
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f"{msg}\n")
    except:
        pass

log("========== 应用启动 ==========")
log(f"Python版本: {sys.version}")
log(f"当前目录: {os.getcwd()}")

try:
    log("导入json...")
    import json
    log("导入json成功")
except Exception as e:
    log(f"导入json失败: {e}")

try:
    log("导入random...")
    import random
    log("导入random成功")
except Exception as e:
    log(f"导入random失败: {e}")

try:
    log("导入datetime...")
    from datetime import datetime
    log("导入datetime成功")
except Exception as e:
    log(f"导入datetime失败: {e}")

# ========== 字体设置 ==========
try:
    log("设置字体...")
    from kivy.config import Config
    Config.set('kivy', 'default_font', ['DroidSansFallback.ttf'])
    Config.set('graphics', 'background', '1,1,1,1')
    log("字体设置成功")
except Exception as e:
    log(f"字体设置失败: {e}")
    traceback.print_exc()

# ========== 导入Kivy ==========
try:
    log("导入Kivy模块...")
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.scrollview import ScrollView
    from kivy.uix.label import Label
    from kivy.uix.button import Button
    from kivy.uix.textinput import TextInput
    from kivy.uix.popup import Popup
    from kivy.uix.screenmanager import ScreenManager, Screen
    from kivy.metrics import dp
    from kivy.core.window import Window
    log("导入Kivy成功")
except Exception as e:
    log(f"导入Kivy失败: {e}")
    traceback.print_exc()

try:
    Window.clearcolor = (1, 1, 1, 1)
    log("设置窗口背景成功")
except:
    pass

# ========== Android平台 ==========
ANDROID_AVAILABLE = False
try:
    log("检查Android环境...")
    from jnius import autoclass
    PYTHON_ACTIVITY = autoclass('org.kivy.android.PythonActivity')
    Intent = autoclass('android.content.Intent')
    Uri = autoclass('android.net.Uri')
    ANDROID_AVAILABLE = True
    log("Android环境可用")
except Exception as e:
    log(f"Android环境不可用: {e}")

# ========== 颜色 ==========
COLORS = {
    'primary': (0.2, 0.4, 0.8, 1),
    'secondary': (0.95, 0.95, 0.98, 1),
    'accent': (0.98, 0.73, 0.24, 1),
    'text_dark': (0.13, 0.13, 0.13, 1),
    'text_light': (0.4, 0.4, 0.4, 1),
    'white': (1, 1, 1, 1),
    'success': (0.3, 0.69, 0.31, 1),
    'danger': (0.87, 0.32, 0.32, 1),
}

# ========== 数据 ==========
BUILTIN_POETRY = {
    "论语十二章": {
        "type": "文言文", "category": "必修", "author": "孔子弟子",
        "content": "子曰：学而时习之，不亦说乎？\n子曰：温故而知新，可以为师矣。\n子曰：学而不思则罔，思而不学则殆。"
    },
    "劝学": {
        "type": "文言文", "category": "必修", "author": "荀子",
        "content": "君子曰：学不可以已。\n青，取之于蓝，而青于蓝。\n故木受绳则直，金就砺则利。"
    },
    "静夜思": {
        "type": "古诗", "category": "必修", "author": "李白",
        "content": "床前明月光，疑是地上霜。\n举头望明月，低头思故乡。"
    }
}

log("预置数据加载完成")

# ========== 按钮 ==========
class RoundedButton(Button):
    def __init__(self, **kwargs):
        self.bg_color = kwargs.pop('bg_color', COLORS['primary'])
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = self.bg_color
        self.color = COLORS['white']
        self.font_size = '16sp'

log("按钮类定义完成")

# ========== 主界面 ==========
class MainScreen(Screen):
    def __init__(self, **kwargs):
        log("MainScreen初始化开始...")
        super().__init__(**kwargs)
        self.poetry_data = BUILTIN_POETRY
        self.records = {}
        self.current_poetry = None
        self._popup = None
        log("MainScreen属性设置完成")
        self.build_ui()
        log("MainScreen UI构建完成")
    
    def build_ui(self):
        try:
            log("开始构建UI...")
            layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
            
            layout.add_widget(Label(text='古诗文背诵检测', font_size='24sp', color=COLORS['primary'], size_hint_y=0.1))
            
            self.category_btns = BoxLayout(size_hint_y=0.08, spacing=dp(5))
            for cat in ['全部', '文言文', '古诗']:
                btn = RoundedButton(text=cat, bg_color=COLORS['primary'] if cat == '全部' else (0.6, 0.6, 0.6, 1))
                btn.bind(on_press=lambda x, c=cat: self.filter_category(c))
                self.category_btns.add_widget(btn)
            layout.add_widget(self.category_btns)
            
            scroll = ScrollView(size_hint_y=0.72)
            self.list_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(8))
            self.list_layout.bind(minimum_height=self.list_layout.setter('height'))
            scroll.add_widget(self.list_layout)
            layout.add_widget(scroll)
            
            bottom = BoxLayout(size_hint_y=0.1, spacing=dp(10))
            btn1 = RoundedButton(text='查看记录', bg_color=(0.5, 0.5, 0.5, 1))
            btn1.bind(on_press=self.show_records)
            bottom.add_widget(btn1)
            layout.add_widget(bottom)
            
            self.add_widget(layout)
            self.filter_category('全部')
            log("UI构建成功")
        except Exception as e:
            log(f"UI构建失败: {e}")
            traceback.print_exc()
    
    def filter_category(self, category):
        try:
            self.list_layout.clear_widgets()
            
            if category == '全部':
                items = list(self.poetry_data.items())
            else:
                items = [(n, d) for n, d in self.poetry_data.items() if d.get('type') == category]
            
            for name, data in items:
                box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=dp(5))
                info = BoxLayout(orientation='vertical')
                info.add_widget(Label(text=name, color=COLORS['text_dark'], font_size='16sp', size_hint_y=0.6))
                info.add_widget(Label(text=data.get('author', ''), color=COLORS['text_light'], font_size='12sp', size_hint_y=0.4))
                box.add_widget(info)
                btn = RoundedButton(text='背诵', bg_color=COLORS['success'], size_hint_x=0.3)
                btn.bind(on_press=lambda x, n=name: self.select_poetry(n))
                box.add_widget(btn)
                self.list_layout.add_widget(box)
        except Exception as e:
            log(f"筛选分类失败: {e}")
    
    def select_poetry(self, name):
        try:
            self.current_poetry = name
            data = self.poetry_data.get(name, {})
            content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
            
            scroll = ScrollView()
            text_label = Label(text=data.get('content', ''), color=COLORS['text_dark'], font_size='16sp', size_hint_y=None)
            text_label.bind(texture_size=text_label.setter('size'))
            scroll.add_widget(text_label)
            content.add_widget(scroll)
            
            btns = BoxLayout(size_hint_y=0.15, spacing=dp(5))
            btn1 = RoundedButton(text='背诵检测', bg_color=COLORS['primary'])
            btn1.bind(on_press=lambda x: self.start_test(name))
            btns.add_widget(btn1)
            btn2 = RoundedButton(text='关闭', bg_color=(0.6, 0.6, 0.6, 1))
            btn2.bind(on_press=lambda x: self.close_popup())
            btns.add_widget(btn2)
            content.add_widget(btns)
            
            self._popup = Popup(title=name, content=content, size_hint=(0.9, 0.85))
            self._popup.open()
        except Exception as e:
            log(f"选择诗文失败: {e}")
    
    def close_popup(self):
        if self._popup:
            self._popup.dismiss()
    
    def start_test(self, name):
        self.close_popup()
        self.manager.current = 'fill_test'
        self.manager.get_screen('fill_test').setup_test(name)
    
    def show_records(self, instance):
        content = BoxLayout(orientation='vertical', padding=dp(10))
        scroll = ScrollView()
        layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(5))
        layout.bind(minimum_height=layout.setter('height'))
        
        if not self.records:
            layout.add_widget(Label(text='暂无背诵记录', color=COLORS['text_light'], size_hint_y=None, height=dp(40)))
        else:
            for name, recs in self.records.items():
                for r in recs[-5:]:
                    layout.add_widget(Label(text=f"{name} - {r.get('score', 0):.0f}%", color=COLORS['text_dark'], size_hint_y=None, height=dp(30)))
        
        scroll.add_widget(layout)
        content.add_widget(scroll)
        close_btn = RoundedButton(text='关闭', bg_color=(0.6, 0.6, 0.6, 1), size_hint_y=0.1)
        close_btn.bind(on_press=lambda x: self._records_popup.dismiss() if hasattr(self, '_records_popup') else None)
        content.add_widget(close_btn)
        self._records_popup = Popup(title='背诵记录', content=content, size_hint=(0.9, 0.8))
        self._records_popup.open()

log("MainScreen类定义完成")

# ========== 填空检测界面 ==========
class FillTestScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.answer_entries = []
        self.correct_answers = []
    
    def setup_test(self, poetry_name):
        try:
            main_screen = self.manager.get_screen('main')
            data = main_screen.poetry_data.get(poetry_name, {})
            content = data.get('content', '')
            
            self.clear_widgets()
            self.answer_entries = []
            self.correct_answers = []
            
            layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
            layout.add_widget(Label(text=f'填空检测：{poetry_name}', font_size='18sp', color=COLORS['primary'], size_hint_y=0.08))
            
            scroll = ScrollView(size_hint_y=0.8)
            q_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(10))
            q_layout.bind(minimum_height=q_layout.setter('height'))
            
            sentences = [s.strip() for s in content.split('\n') if s.strip() and len(s.strip()) > 4]
            random.shuffle(sentences)
            
            for i, sentence in enumerate(sentences[:5]):
                mid = len(sentence) // 2
                blank = sentence[:mid]
                show = sentence[mid:]
                hint = f'___ {show}'
                
                q_box = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(80))
                q_box.add_widget(Label(text=f'第{i+1}句：{hint}', color=COLORS['text_dark'], font_size='16sp', size_hint_y=0.4))
                entry = TextInput(hint_text='填写答案', font_size='16sp', size_hint_y=0.6, multiline=False)
                q_box.add_widget(entry)
                self.answer_entries.append(entry)
                self.correct_answers.append(blank)
                q_layout.add_widget(q_box)
            
            scroll.add_widget(q_layout)
            layout.add_widget(scroll)
            
            btn_layout = BoxLayout(size_hint_y=0.12, spacing=dp(10))
            btn1 = RoundedButton(text='提交', bg_color=COLORS['primary'])
            btn1.bind(on_press=self.submit_answers)
            btn2 = RoundedButton(text='返回', bg_color=(0.6, 0.6, 0.6, 1))
            btn2.bind(on_press=self.go_back)
            btn_layout.add_widget(btn1)
            btn_layout.add_widget(btn2)
            layout.add_widget(btn_layout)
            
            self.add_widget(layout)
        except Exception as e:
            log(f"setup_test失败: {e}")
    
    def submit_answers(self, instance):
        correct = 0
        total = len(self.answer_entries)
        for entry, answer in zip(self.answer_entries, self.correct_answers):
            if entry.text.strip() == answer:
                correct += 1
                entry.background_color = COLORS['success']
            else:
                entry.background_color = COLORS['danger']
        
        score = (correct / total * 100) if total > 0 else 0
        Popup(title='结果', content=Label(text=f'得分：{score:.0f}%', color=COLORS['text_dark']), size_hint=(0.7, 0.4)).open()
    
    def go_back(self, instance):
        self.manager.current = 'main'

log("FillTestScreen类定义完成")

# ========== 应用入口 ==========
class PoetryApp(App):
    def build(self):
        log("PoetryApp.build开始...")
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(FillTestScreen(name='fill_test'))
        log("PoetryApp.build完成")
        return sm

log("PoetryApp类定义完成")
log("准备运行应用...")

if __name__ == '__main__':
    try:
        log("PoetryApp().run()...")
        PoetryApp().run()
        log("应用正常退出")
    except Exception as e:
        log(f"应用崩溃: {e}")
        traceback.print_exc()
