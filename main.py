# -*- coding: utf-8 -*-
"""
高中古诗文背诵检测系统 - Kivy手机版
修复中文乱码（正确加载字体）
"""

import os

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.resources import resource_find

Window.clearcolor = (1, 1, 1, 1)

# ========== 颜色 ==========
COLORS = {
    'primary': (0.2, 0.4, 0.8, 1),
    'text_dark': (0.13, 0.13, 0.13, 1),
    'text_light': (0.4, 0.4, 0.4, 1),
    'success': (0.3, 0.69, 0.31, 1),
}

# ========== 数据 ==========
POETRY_DATA = {
    "论语": {
        "type": "文言文", 
        "author": "孔子",
        "content": "学而时习之\n温故而知新\n学而不思则罔"
    },
    "静夜思": {
        "type": "古诗",
        "author": "李白", 
        "content": "床前明月光\n疑是地上霜\n举头望明月\n低头思故乡"
    },
    "登鹳雀楼": {
        "type": "古诗",
        "author": "王之涣",
        "content": "白日依山尽\n黄河入海流\n欲穷千里目\n更上一层楼"
    }
}

# ========== 获取字体 ==========
def get_font():
    """安全获取字体路径"""
    # 方法1: 使用resource_find
    font = resource_find('DroidSansFallback.ttf')
    if font:
        return font
    
    # 方法2: 直接路径
    paths = [
        'DroidSansFallback.ttf',
        '/data/data/org.example.poetryrecite/files/DroidSansFallback.ttf',
    ]
    for p in paths:
        if os.path.exists(p):
            return p
    
    return None  # 返回None使用默认字体

# ========== 主界面 ==========
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font = get_font()
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(5))
        
        # 标题
        layout.add_widget(Label(
            text='古诗文背诵检测',
            font_name=self.font,
            font_size='24sp',
            color=COLORS['primary'],
            size_hint_y=0.1
        ))
        
        # 列表
        scroll = ScrollView(size_hint_y=0.85)
        list_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(5))
        list_layout.bind(minimum_height=list_layout.setter('height'))
        
        for name, data in POETRY_DATA.items():
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
            box.add_widget(Label(
                text=f'{name} - {data["author"]}',
                font_name=self.font,
                color=COLORS['text_dark'],
                size_hint_x=0.7
            ))
            btn = Button(
                text='查看',
                font_name=self.font,
                size_hint_x=0.3,
                background_color=COLORS['primary']
            )
            btn.bind(on_press=lambda x, n=name: self.show_poetry(n))
            box.add_widget(btn)
            list_layout.add_widget(box)
        
        scroll.add_widget(list_layout)
        layout.add_widget(scroll)
        
        # 底部提示
        layout.add_widget(Label(
            text='点击查看背诵',
            font_name=self.font,
            color=COLORS['text_light'],
            size_hint_y=0.05,
            font_size='12sp'
        ))
        
        self.add_widget(layout)
    
    def show_poetry(self, name):
        data = POETRY_DATA.get(name, {})
        content = BoxLayout(orientation='vertical', padding=dp(10))
        content.add_widget(Label(
            text=data.get('content', ''),
            font_name=self.font,
            color=COLORS['text_dark'],
            font_size='18sp'
        ))
        
        close_btn = Button(
            text='关闭',
            font_name=self.font,
            size_hint_y=0.15,
            background_color=(0.6, 0.6, 0.6, 1)
        )
        close_btn.bind(on_press=lambda x: popup.dismiss())
        content.add_widget(close_btn)
        
        popup = Popup(title=name, content=content, size_hint=(0.9, 0.8))
        popup.open()

# ========== 应用 ==========
class PoetryApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        return sm

if __name__ == '__main__':
    PoetryApp().run()
