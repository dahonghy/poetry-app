# -*- coding: utf-8 -*-
"""
高中古诗文背诵检测系统 - Kivy手机版（美化版）
"""

import os
import json
import random
from datetime import datetime

# ========== 字体设置必须在导入Kivy其他模块之前 ==========
from kivy.config import Config
from kivy.resources import resource_find

# 设置中文字体
def setup_chinese_font():
    font_files = ['DroidSansFallback.ttf', 'NotoSansSC-Regular.otf']
    for font_file in font_files:
        font_path = resource_find(font_file)
        if font_path:
            Config.set('kivy', 'default_font', [font_path])
            return font_path
    for font_path in ['/system/fonts/DroidSansFallback.ttf', '/system/fonts/NotoSansCJK-Regular.ttc']:
        if os.path.exists(font_path):
            Config.set('kivy', 'default_font', [font_path])
            return font_path
    return None

setup_chinese_font()
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
from kivy.uix.floatlayout import FloatLayout
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle

# 设置白色背景
Window.clearcolor = (1, 1, 1, 1)

# Android平台导入
try:
    from jnius import autoclass
    PYTHON_ACTIVITY = autoclass('org.kivy.android.PythonActivity')
    Intent = autoclass('android.content.Intent')
    Uri = autoclass('android.net.Uri')
    File = autoclass('java.io.File')
    ANDROID_AVAILABLE = True
except:
    ANDROID_AVAILABLE = False

# ========== 颜色主题 ==========
COLORS = {
    'primary': (0.2, 0.4, 0.8, 1),      # 蓝色 #3366CC
    'secondary': (0.95, 0.95, 0.98, 1),  # 浅灰蓝背景
    'accent': (0.98, 0.73, 0.24, 1),     # 金色 #F7BB3D
    'text_dark': (0.13, 0.13, 0.13, 1),  # 深灰文字
    'text_light': (0.4, 0.4, 0.4, 1),    # 浅灰文字
    'white': (1, 1, 1, 1),
    'success': (0.3, 0.69, 0.31, 1),     # 绿色
    'danger': (0.87, 0.32, 0.32, 1),     # 红色
    'background': (0.96, 0.96, 0.98, 1), # 页面背景
}

# 数据文件路径
PROGRAM_DIR = os.path.dirname(os.path.abspath(__file__)) if os.path.dirname(__file__) else os.getcwd()
POETRY_FILE = os.path.join(PROGRAM_DIR, "poetry_data.json")
RECORDS_FILE = os.path.join(PROGRAM_DIR, "recite_records.json")

# 预置古诗文数据
BUILTIN_POETRY = {
    "论语十二章": {"type": "文言文", "category": "必修", "author": "孔子及其弟子",
        "content": "子曰：学而时习之，不亦说乎？有朋自远方来，不亦乐乎？人不知而不愠，不亦君子乎？\n\n曾子曰：吾日三省吾身：为人谋而不忠乎？与朋友交而不信乎？传不习乎？\n\n子曰：吾十有五而志于学，三十而立，四十而不惑，五十而知天命，六十而耳顺，七十而从心所欲，不逾矩。"},
    "劝学": {"type": "文言文", "category": "必修", "author": "荀子",
        "content": "君子曰：学不可以已。\n\n青，取之于蓝，而青于蓝；冰，水为之，而寒于水。\n\n故木受绳则直，金就砺则利，君子博学而日参省乎己，则知明而行无过矣。"},
    "师说": {"type": "文言文", "category": "必修", "author": "韩愈",
        "content": "古之学者必有师。师者，所以传道受业解惑也。\n\n人非生而知之者，孰能无惑？惑而不从师，其为惑也，终不解矣。"},
    "赤壁赋": {"type": "文言文", "category": "必修", "author": "苏轼",
        "content": "壬戌之秋，七月既望，苏子与客泛舟游于赤壁之下。\n\n清风徐来，水波不兴。举酒属客，诵明月之诗，歌窈窕之章。"},
    "念奴娇赤壁怀古": {"type": "诗词曲", "category": "必修", "author": "苏轼",
        "content": "大江东去，浪淘尽，千古风流人物。\n\n故垒西边，人道是，三国周郎赤壁。"},
    "登高": {"type": "诗词曲", "category": "必修", "author": "杜甫",
        "content": "风急天高猿啸哀，渚清沙白鸟飞回。\n\n无边落木萧萧下，不尽长江滚滚来。"},
    "虞美人": {"type": "诗词曲", "category": "必修", "author": "李煜",
        "content": "春花秋月何时了？往事知多少。\n\n小楼昨夜又东风，故国不堪回首月明中。"},
    "短歌行": {"type": "诗词曲", "category": "必修", "author": "曹操",
        "content": "对酒当歌，人生几何！譬如朝露，去日苦多。\n\n青青子衿，悠悠我心。"},
}


class RoundedButton(Button):
    """圆角按钮"""
    def __init__(self, bg_color=COLORS['primary'], **kwargs):
        self.bg_color = bg_color
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = bg_color
        self.color = COLORS['white']
        self.font_size = '16sp'
        self.bold = True


class CardBox(BoxLayout):
    """卡片容器"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.padding = dp(15)
        self.spacing = dp(10)
        with self.canvas.before:
            Color(*COLORS['white'])
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[dp(10)])
        self.bind(size=self.update_rect, pos=self.update_rect)
    
    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class MainScreen(Screen):
    """主界面"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.poetry_data = {}
        self.records = {}
        self.current_poetry = None
        self.load_data()
        self.build_ui()
    
    def load_data(self):
        self.poetry_data = BUILTIN_POETRY.copy()
        if os.path.exists(POETRY_FILE):
            try:
                with open(POETRY_FILE, 'r', encoding='utf-8') as f:
                    self.poetry_data.update(json.load(f))
            except:
                pass
        if os.path.exists(RECORDS_FILE):
            try:
                with open(RECORDS_FILE, 'r', encoding='utf-8') as f:
                    self.records = json.load(f)
            except:
                pass
    
    def save_data(self):
        try:
            with open(RECORDS_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.records, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def build_ui(self):
        # 主布局
        main_layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(15))
        
        # 顶部标题卡片
        title_card = CardBox(orientation='vertical', size_hint_y=0.18)
        title = Label(
            text='[size=22][b]古诗文背诵检测[/b][/size]\n[size=12]统编版高中语文72篇[/size]',
            markup=True,
            color=COLORS['text_dark'],
            halign='center'
        )
        title_card.add_widget(title)
        main_layout.add_widget(title_card)
        
        # 分类按钮区
        cat_layout = BoxLayout(size_hint_y=0.1, spacing=dp(8))
        categories = [('必修', COLORS['primary']), ('选修', (0.3, 0.6, 0.4, 1)), 
                      ('个人新增', (0.6, 0.4, 0.6, 1)), ('PDF', (0.8, 0.5, 0.2, 1))]
        for cat, color in categories:
            btn = RoundedButton(text=cat, bg_color=color, font_size='14sp')
            btn.bind(on_press=lambda x, c=cat: self.show_category(c))
            cat_layout.add_widget(btn)
        main_layout.add_widget(cat_layout)
        
        # 内容区
        content_card = CardBox(size_hint_y=0.52)
        self.content_label = Label(
            text='[size=16]请选择分类查看古诗文[/size]\n\n[size=14]点击下方按钮开始检测[/size]',
            markup=True,
            color=COLORS['text_dark'],
            halign='center',
            valign='middle'
        )
        self.content_label.bind(texture_size=self.content_label.setter('size'))
        content_card.add_widget(self.content_label)
        main_layout.add_widget(content_card)
        
        # 底部按钮
        btn_layout = BoxLayout(size_hint_y=0.12, spacing=dp(15))
        btn1 = RoundedButton(text='填空检测', bg_color=COLORS['primary'])
        btn1.bind(on_press=self.start_fill_test)
        btn2 = RoundedButton(text='背诵记录', bg_color=(0.4, 0.4, 0.45, 1))
        btn2.bind(on_press=self.show_records)
        btn_layout.add_widget(btn1)
        btn_layout.add_widget(btn2)
        main_layout.add_widget(btn_layout)
        
        self.add_widget(main_layout)
    
    def show_category(self, category):
        if category == 'PDF':
            if self.open_pdf():
                return
            self.content_label.text = '[size=14][color=F44336]无法打开PDF[/color][/size]\n\n请安装PDF阅读器'
            return
        
        items = [(n, d) for n, d in self.poetry_data.items() if d.get('category') == category]
        if not items:
            self.content_label.text = f'[size=16]{category}分类暂无内容[/size]'
            return
        
        text = f'[size=18][b]{category}[/b][/size]\n\n'
        for name, data in items:
            t = data.get('type', '文言文')
            text += f'[color=3366CC]•[/color] {name} [size=12]({t})[/size]\n'
        self.content_label.text = text
    
    def open_pdf(self):
        if not ANDROID_AVAILABLE:
            return False
        try:
            pdf_path = os.path.join(PROGRAM_DIR, '高中文言文基础知识点全解读.pdf')
            if not os.path.exists(pdf_path):
                return False
            pdf_file = File(pdf_path)
            context = PYTHON_ACTIVITY.mActivity
            intent = Intent(Intent.ACTION_VIEW)
            intent.setDataAndType(Uri.fromFile(pdf_file), 'application/pdf')
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            context.startActivity(intent)
            return True
        except:
            return False
    
    def start_fill_test(self, instance):
        content = BoxLayout(orientation='vertical', spacing=dp(10))
        scroll = ScrollView()
        list_layout = BoxLayout(orientation='vertical', spacing=dp(8), size_hint_y=None)
        list_layout.bind(minimum_height=list_layout.setter('height'))
        
        for name in sorted(self.poetry_data.keys()):
            btn = RoundedButton(text=name, bg_color=COLORS['secondary'])
            btn.color = COLORS['text_dark']
            btn.bind(on_press=lambda x, n=name: self.do_fill_test(n))
            list_layout.add_widget(btn)
        
        scroll.add_widget(list_layout)
        content.add_widget(scroll)
        
        popup = Popup(title='选择诗文', content=content, size_hint=(0.9, 0.8),
                      background=COLORS['white'], separator_color=COLORS['primary'])
        
        for child in list_layout.children:
            child.bind(on_press=lambda x: popup.dismiss())
        
        popup.open()
    
    def do_fill_test(self, poetry_name):
        self.current_poetry = poetry_name
        self.manager.current = 'fill_test'
        self.manager.get_screen('fill_test').setup_test(poetry_name)
    
    def show_records(self, instance):
        if not self.records:
            popup = Popup(title='背诵记录', content=Label(text='暂无记录', color=COLORS['text_dark']),
                          size_hint=(0.8, 0.4), background=COLORS['white'])
            popup.open()
            return
        
        text = ''
        for name, recs in self.records.items():
            text += f'[b]{name}[/b]\n'
            for r in recs[-3:]:
                text += f"  {r['time']} | {r['score']:.0f}%\n"
            text += '\n'
        
        popup = Popup(title='背诵记录', content=Label(text=text, markup=True, color=COLORS['text_dark']),
                      size_hint=(0.9, 0.7), background=COLORS['white'])
        popup.open()


class FillTestScreen(Screen):
    """填空检测界面"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.answer_entries = []
        self.correct_answers = []
    
    def setup_test(self, poetry_name):
        self.clear_widgets()
        self.answer_entries = []
        self.correct_answers = []
        
        main_screen = self.manager.get_screen('main')
        content = main_screen.poetry_data.get(poetry_name, {}).get('content', '')
        sentences = [s.strip() for s in content.split('\n') if s.strip() and len(s.strip()) > 2]
        
        layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        
        # 标题
        layout.add_widget(Label(
            text=f'[size=20][b]{poetry_name}[/b][/size]',
            markup=True, color=COLORS['text_dark'], size_hint_y=0.08
        ))
        
        # 题目区
        scroll = ScrollView(size_hint_y=0.72)
        q_layout = BoxLayout(orientation='vertical', spacing=dp(12), size_hint_y=None)
        q_layout.bind(minimum_height=q_layout.setter('height'))
        
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
            q_box.add_widget(Label(
                text=f'第{i+1}句：{hint}',
                color=COLORS['text_dark'], font_size='16sp', size_hint_y=0.4
            ))
            
            entry = TextInput(hint_text='填写答案', font_size='16sp', size_hint_y=0.6,
                             multiline=False, background_color=COLORS['secondary'])
            q_box.add_widget(entry)
            
            self.answer_entries.append(entry)
            self.correct_answers.append(blank)
            q_layout.add_widget(q_box)
        
        scroll.add_widget(q_layout)
        layout.add_widget(scroll)
        
        # 按钮
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
        main_screen.records[name].append({
            'type': '填空检测',
            'score': score,
            'time': datetime.now().strftime('%m-%d %H:%M')
        })
        main_screen.save_data()
        
        Popup(title='检测结果', content=Label(text=f'得分：{score:.0f}%\n正确：{correct}/{total}',
              color=COLORS['text_dark'], font_size='20sp'), size_hint=(0.7, 0.4),
              background=COLORS['white']).open()
    
    def show_answers(self, instance):
        for entry, answer in zip(self.answer_entries, self.correct_answers):
            entry.text = answer
            entry.background_color = COLORS['secondary']
    
    def go_back(self, instance):
        self.manager.current = 'main'


class PoetryApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(FillTestScreen(name='fill_test'))
        return sm
    
    def on_stop(self):
        self.root.get_screen('main').save_data()


if __name__ == '__main__':
    PoetryApp().run()
