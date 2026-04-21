# -*- coding: utf-8 -*-
"""
高中古诗文背诵检测系统 - Kivy手机版（修复版）
解决闪退问题
"""

import os
import json
import random
from datetime import datetime

# ========== 字体设置必须在导入Kivy其他模块之前 ==========
from kivy.config import Config

# 先设置一个默认字体，防止崩溃
Config.set('kivy', 'default_font', ['DroidSansFallback.ttf'])
Config.set('graphics', 'background', '1,1,1,1')

# ========== 导入其他模块 ==========
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

Window.clearcolor = (1, 1, 1, 1)

# Android平台导入
try:
    from jnius import autoclass
    PYTHON_ACTIVITY = autoclass('org.kivy.android.PythonActivity')
    Intent = autoclass('android.content.Intent')
    Uri = autoclass('android.net.Uri')
    ANDROID_AVAILABLE = True
except:
    ANDROID_AVAILABLE = False

# ========== 颜色主题 ==========
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

# ========== 预置古诗文数据 ==========
BUILTIN_POETRY = {
    "论语十二章": {
        "type": "文言文", "category": "必修", "author": "孔子及其弟子",
        "content": """子曰："学而时习之，不亦说乎？有朋自远方来，不亦乐乎？人不知而不愠，不亦君子乎？"
子曰："温故而知新，可以为师矣。"
子曰："学而不思则罔，思而不学则殆。"
子曰："知之者不如好之者，好之者不如乐之者。"
子曰："三人行，必有我师焉。择其善者而从之，其不善者而改之。"
子曰："逝者如斯夫，不舍昼夜。"
子曰："三军可夺帅也，匹夫不可夺志也。"
曾子曰："吾日三省吾身：为人谋而不忠乎？与朋友交而不信乎？传不习乎？"
""",
        "key_points": ["学习态度", "学习方法", "修身养性"]
    },
    "劝学": {
        "type": "文言文", "category": "必修", "author": "荀子",
        "content": """君子曰：学不可以已。
青，取之于蓝，而青于蓝；冰，水为之，而寒于水。
故木受绳则直，金就砺则利，君子博学而日参省乎己，则知明而行无过矣。
吾尝终日而思矣，不如须臾之所学也。
假舆马者，非利足也，而致千里；假舟楫者，非能水也，而绝江河。
君子生非异也，善假于物也。
""",
        "key_points": ["学习的重要性", "学习方法"]
    },
    "师说": {
        "type": "文言文", "category": "必修", "author": "韩愈",
        "content": """古之学者必有师。师者，所以传道受业解惑也。
人非生而知之者，孰能无惑？惑而不从师，其为惑也，终不解矣。
是故无贵无贱，无长无少，道之所存，师之所存也。
""",
        "key_points": ["从师学习的必要性", "择师标准"]
    },
    "静夜思": {
        "type": "古诗", "category": "必修", "author": "李白",
        "content": """床前明月光，疑是地上霜。
举头望明月，低头思故乡。
""",
        "key_points": ["思乡之情"]
    },
    "登鹳雀楼": {
        "type": "古诗", "category": "必修", "author": "王之涣",
        "content": """白日依山尽，黄河入海流。
欲穷千里目，更上一层楼。
""",
        "key_points": ["进取精神"]
    }
}

# ========== 数据管理 ==========
def get_data_dir():
    if ANDROID_AVAILABLE:
        try:
            context = PYTHON_ACTIVITY.mActivity or PYTHON_ACTIVITY
            return context.getFilesDir().getPath()
        except:
            pass
    return os.path.dirname(os.path.abspath(__file__)) if os.path.dirname(__file__) else os.getcwd()

DATA_DIR = get_data_dir()

def load_records():
    try:
        records_file = os.path.join(DATA_DIR, "recite_records.json")
        if os.path.exists(records_file):
            with open(records_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    return {}

def save_records(records):
    try:
        records_file = os.path.join(DATA_DIR, "recite_records.json")
        with open(records_file, 'w', encoding='utf-8') as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
    except:
        pass

# ========== 美化按钮 ==========
class RoundedButton(Button):
    def __init__(self, **kwargs):
        self.bg_color = kwargs.pop('bg_color', COLORS['primary'])
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = self.bg_color
        self.color = COLORS['white']
        self.font_size = '16sp'

# ========== 主界面 ==========
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.poetry_data = BUILTIN_POETRY
        self.records = load_records()
        self.current_poetry = None
        self._popup = None
        self._records_popup = None
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        
        layout.add_widget(Label(text='高中古诗文背诵检测', font_size='24sp', color=COLORS['primary'], size_hint_y=0.1, bold=True))
        
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
        btn1 = RoundedButton(text='文言文PDF', bg_color=COLORS['accent'])
        btn1.color = COLORS['text_dark']
        btn1.bind(on_press=self.open_pdf)
        bottom.add_widget(btn1)
        btn2 = RoundedButton(text='查看记录', bg_color=(0.5, 0.5, 0.5, 1))
        btn2.bind(on_press=self.show_records)
        bottom.add_widget(btn2)
        layout.add_widget(bottom)
        
        self.add_widget(layout)
        self.filter_category('全部')
    
    def filter_category(self, category):
        for i, btn in enumerate(self.category_btns.children):
            cats = ['古诗', '文言文', '全部']
            btn.bg_color = COLORS['primary'] if cats[i] == category else (0.6, 0.6, 0.6, 1)
            btn.background_color = btn.bg_color
        
        self.list_layout.clear_widgets()
        
        if category == '全部':
            items = list(self.poetry_data.items())
        else:
            items = [(n, d) for n, d in self.poetry_data.items() if d.get('type') == category]
        
        for name, data in items:
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=dp(5))
            info = BoxLayout(orientation='vertical')
            info.add_widget(Label(text=name, color=COLORS['text_dark'], font_size='16sp', size_hint_y=0.6))
            info.add_widget(Label(text=f"{data.get('author', '')} · {data.get('category', '')}", color=COLORS['text_light'], font_size='12sp', size_hint_y=0.4))
            box.add_widget(info)
            btn = RoundedButton(text='背诵', bg_color=COLORS['success'], size_hint_x=0.3)
            btn.bind(on_press=lambda x, n=name: self.select_poetry(n))
            box.add_widget(btn)
            self.list_layout.add_widget(box)
    
    def select_poetry(self, name):
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
    
    def close_popup(self):
        if self._popup:
            self._popup.dismiss()
    
    def start_test(self, name):
        self.close_popup()
        self.manager.current = 'fill_test'
        self.manager.get_screen('fill_test').setup_test(name)
    
    def open_pdf(self, instance):
        if ANDROID_AVAILABLE:
            try:
                pdf_path = os.path.join(DATA_DIR, "高中文言文基础知识点全解读.pdf")
                if os.path.exists(pdf_path):
                    uri = Uri.parse(f"file://{pdf_path}")
                    intent = Intent(Intent.ACTION_VIEW)
                    intent.setDataAndType(uri, "application/pdf")
                    intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                    PYTHON_ACTIVITY.mActivity.startActivity(intent)
                    return
            except:
                pass
        Popup(title='提示', content=Label(text='请在电脑端查看PDF文件', color=COLORS['text_dark']), size_hint=(0.7, 0.3)).open()
    
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
                    layout.add_widget(Label(text=f"{name} - {r.get('type', '')} - {r.get('score', 0):.0f}% - {r.get('time', '')}", color=COLORS['text_dark'], size_hint_y=None, height=dp(30), font_size='14sp'))
        
        scroll.add_widget(layout)
        content.add_widget(scroll)
        close_btn = RoundedButton(text='关闭', bg_color=(0.6, 0.6, 0.6, 1), size_hint_y=0.1)
        close_btn.bind(on_press=lambda x: self.close_records_popup())
        content.add_widget(close_btn)
        self._records_popup = Popup(title='背诵记录', content=content, size_hint=(0.9, 0.8))
        self._records_popup.open()
    
    def close_records_popup(self):
        if self._records_popup:
            self._records_popup.dismiss()
    
    def save_data(self):
        save_records(self.records)

# ========== 填空检测界面 ==========
class FillTestScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.answer_entries = []
        self.correct_answers = []
    
    def setup_test(self, poetry_name):
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
            is_front = random.choice([True, False])
            if is_front:
                blank = sentence[:mid]
                show = sentence[mid:]
                hint = f'___ {show}'
            else:
                show = sentence[:mid]
                blank = sentence[mid:]
                hint = f'{show} ___'
            
            q_box = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(80))
            q_box.add_widget(Label(text=f'第{i+1}句：{hint}', color=COLORS['text_dark'], font_size='16sp', size_hint_y=0.4))
            entry = TextInput(hint_text='填写答案', font_size='16sp', size_hint_y=0.6, multiline=False, background_color=COLORS['secondary'])
            q_box.add_widget(entry)
            self.answer_entries.append(entry)
            self.correct_answers.append(blank)
            q_layout.add_widget(q_box)
        
        scroll.add_widget(q_layout)
        layout.add_widget(scroll)
        
        btn_layout = BoxLayout(size_hint_y=0.12, spacing=dp(10))
        btn1 = RoundedButton(text='提交', bg_color=COLORS['primary'])
        btn1.bind(on_press=self.submit_answers)
        btn2 = RoundedButton(text='答案', bg_color=COLORS['accent'])
        btn2.color = COLORS['text_dark']
        btn2.bind(on_press=self.show_answers)
        btn3 = RoundedButton(text='返回', bg_color=(0.6, 0.6, 0.6, 1))
        btn3.bind(on_press=self.go_back)
        btn_layout.add_widget(btn1)
        btn_layout.add_widget(btn2)
        btn_layout.add_widget(btn3)
        layout.add_widget(btn_layout)
        
        self.add_widget(layout)
    
    def submit_answers(self, instance):
        correct = 0
        total = len(self.answer_entries)
        for entry, answer in zip(self.answer_entries, self.correct_answers):
            user = entry.text.strip().replace('，', '').replace('。', '').replace(' ', '')
            ans = answer.replace('，', '').replace('。', '').replace(' ', '')
            if user == ans:
                correct += 1
                entry.background_color = COLORS['success']
            else:
                entry.background_color = COLORS['danger']
        
        score = (correct / total * 100) if total > 0 else 0
        main_screen = self.manager.get_screen('main')
        name = main_screen.current_poetry
        if name not in main_screen.records:
            main_screen.records[name] = []
        main_screen.records[name].append({'type': '填空检测', 'score': score, 'time': datetime.now().strftime('%m-%d %H:%M')})
        main_screen.save_data()
        Popup(title='检测结果', content=Label(text=f'得分：{score:.0f}%\n正确：{correct}/{total}', color=COLORS['text_dark'], font_size='20sp'), size_hint=(0.7, 0.4)).open()
    
    def show_answers(self, instance):
        for entry, answer in zip(self.answer_entries, self.correct_answers):
            entry.text = answer
            entry.background_color = COLORS['secondary']
    
    def go_back(self, instance):
        self.manager.current = 'main'

# ========== 应用入口 ==========
class PoetryApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(FillTestScreen(name='fill_test'))
        return sm
    
    def on_stop(self):
        try:
            self.root.get_screen('main').save_data()
        except:
            pass

if __name__ == '__main__':
    PoetryApp().run()
