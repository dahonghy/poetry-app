# -*- coding: utf-8 -*-
"""
高中古诗文背诵检测系统 - Kivy手机版
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.treeview import TreeView, TreeViewLabel
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.core.text import LabelBase
import json
import os
import random
from datetime import datetime

# Android平台导入pyjnius用于打开PDF
try:
    from jnius import autoclass
    from android import activity
    PYTHON_ACTIVITY = autoclass('org.kivy.android.PythonActivity')
    Intent = autoclass('android.content.Intent')
    Uri = autoclass('android.net.Uri')
    File = autoclass('java.io.File')
    ANDROID_AVAILABLE = True
except:
    ANDROID_AVAILABLE = False

# 注册中文字体
def setup_chinese_font():
    """设置中文字体，优先使用应用内置的中文字体"""
    # 首先尝试应用内置的字体文件
    app_font_paths = [
        ('NotoSansSC-Regular.otf', 'NotoSansSC'),
        ('SourceHanSansSC-Regular.otf', 'SourceHanSansSC'),
        ('DroidSansFallback.ttf', 'DroidSansFallback'),
    ]
    
    font_registered = False
    registered_font_name = None
    
    for font_file, font_name in app_font_paths:
        app_font = os.path.join(os.path.dirname(__file__), font_file)
        if os.path.exists(app_font):
            try:
                LabelBase.register(font_name, app_font)
                registered_font_name = font_name
                font_registered = True
                print(f"[字体] 成功注册内置字体: {font_name}")
                break
            except Exception as e:
                print(f"[字体] 注册 {font_file} 失败: {e}")
                continue
    
    # 如果内置字体未注册成功，尝试Android系统字体
    if not font_registered:
        android_fonts = [
            ('/system/fonts/DroidSansFallback.ttf', 'DroidSansFallback'),
            ('/system/fonts/NotoSansCJK-Regular.ttc', 'NotoSansCJK'),
            ('/system/fonts/NotoSansSC-Regular.otf', 'NotoSansSC'),
        ]
        
        for font_path, font_name in android_fonts:
            if os.path.exists(font_path):
                try:
                    LabelBase.register(font_name, font_path)
                    registered_font_name = font_name
                    font_registered = True
                    print(f"[字体] 成功注册系统字体: {font_name}")
                    break
                except:
                    continue
    
    # 设置默认字体
    if font_registered and registered_font_name:
        from kivy.config import Config
        Config.set('kivy', 'default_font', [registered_font_name])
    
    return font_registered, registered_font_name

# 执行字体设置
setup_chinese_font()

# 数据文件
POETRY_FILE = "poetry_data.json"
RECORDS_FILE = "recite_records.json"

# 预置古诗文数据（精简版）
BUILTIN_POETRY = {
    # 必修文言文
    "论语十二章": {"type": "文言文", "category": "必修", "author": "孔子及其弟子",
        "content": "子曰：学而时习之，不亦说乎？有朋自远方来，不亦乐乎？人不知而不愠，不亦君子乎？\n\n曾子曰：吾日三省吾身：为人谋而不忠乎？与朋友交而不信乎？传不习乎？\n\n子曰：吾十有五而志于学，三十而立，四十而不惑，五十而知天命，六十而耳顺，七十而从心所欲，不逾矩。\n\n子曰：温故而知新，可以为师矣。\n\n子曰：学而不思则罔，思而不学则殆。\n\n子曰：贤哉，回也！一箪食，一瓢饮，在陋巷，人不堪其忧，回也不改其乐。贤哉，回也！\n\n子曰：知之者不如好之者，好之者不如乐之者。\n\n子曰：饭疏食，饮水，曲肱而枕之，乐亦在其中矣。不义而富且贵，于我如浮云。\n\n子曰：三人行，必有我师焉。择其善者而从之，其不善者而改之。\n\n子在川上曰：逝者如斯夫，不舍昼夜。\n\n子曰：三军可夺帅也，匹夫不可夺志也。\n\n子夏曰：博学而笃志，切问而近思，仁在其中矣。"},
    "劝学": {"type": "文言文", "category": "必修", "author": "荀子",
        "content": "君子曰：学不可以已。\n\n青，取之于蓝，而青于蓝；冰，水为之，而寒于水。木直中绳，輮以为轮，其曲中规。虽有槁暴，不复挺者，輮使之然也。故木受绳则直，金就砺则利，君子博学而日参省乎己，则知明而行无过矣。\n\n吾尝终日而思矣，不如须臾之所学也；吾尝跂而望矣，不如登高之博见也。登高而招，臂非加长也，而见者远；顺风而呼，声非加疾也，而闻者彰。假舆马者，非利足也，而致千里；假舟楫者，非能水也，而绝江河。君子生非异也，善假于物也。\n\n积土成山，风雨兴焉；积水成渊，蛟龙生焉；积善成德，而神明自得，圣心备焉。故不积跬步，无以至千里；不积小流，无以成江海。骐骥一跃，不能十步；驽马十驾，功在不舍。锲而舍之，朽木不折；锲而不舍，金石可镂。蚓无爪牙之利，筋骨之强，上食埃土，下饮黄泉，用心一也。蟹六跪而二螯，非蛇鳝之穴无可寄托者，用心躁也。"},
    "师说": {"type": "文言文", "category": "必修", "author": "韩愈",
        "content": "古之学者必有师。师者，所以传道受业解惑也。人非生而知之者，孰能无惑？惑而不从师，其为惑也，终不解矣。\n\n生乎吾前，其闻道也固先乎吾，吾从而师之；生乎吾后，其闻道也亦先乎吾，吾从而师之。吾师道也，夫庸知其年之先后生于吾乎？是故无贵无贱，无长无少，道之所存，师之所存也。\n\n嗟乎！师道之不传也久矣！欲人之无惑也难矣！古之圣人，其出人也远矣，犹且从师而问焉；今之众人，其下圣人也亦远矣，而耻学于师。\n\n爱其子，择师而教之；于其身也，则耻师焉，惑矣。巫医乐师百工之人，不耻相师。士大夫之族，曰师曰弟子云者，则群聚而笑之。位卑则足羞，官盛则近谀。\n\n圣人无常师。孔子师郯子、苌弘、师襄、老聃。闻道有先后，术业有专攻，如是而已。"},
    "赤壁赋": {"type": "文言文", "category": "必修", "author": "苏轼",
        "content": "壬戌之秋，七月既望，苏子与客泛舟游于赤壁之下。清风徐来，水波不兴。举酒属客，诵明月之诗，歌窈窕之章。\n\n少焉，月出于东山之上，徘徊于斗牛之间。白露横江，水光接天。纵一苇之所如，凌万顷之茫然。遗世独立，羽化而登仙。\n\n客有吹洞箫者，倚歌而和之。舞幽壑之潜蛟，泣孤舟之嫠妇。\n\n山川相缪，郁乎苍苍。\n\n寄蜉蝣于天地，渺沧海之一粟。\n\n逝者如斯，而未尝往也；盈虚者如彼，而卒莫消长也。\n\n惟江上之清风，与山间之明月，耳得之而为声，目遇之而成色。取之无禁，用之不竭，是造物者之无尽藏也。"},
    # 必修诗词曲
    "念奴娇赤壁怀古": {"type": "诗词曲", "category": "必修", "author": "苏轼",
        "content": "大江东去，浪淘尽，千古风流人物。\n\n故垒西边，人道是，三国周郎赤壁。\n\n羽扇纶巾，谈笑间，樯橹灰飞烟灭。\n\n人生如梦，一尊还酹江月。"},
    "登高": {"type": "诗词曲", "category": "必修", "author": "杜甫",
        "content": "风急天高猿啸哀，渚清沙白鸟飞回。\n\n无边落木萧萧下，不尽长江滚滚来。\n\n万里悲秋常作客，百年多病独登台。\n\n艰难苦恨繁霜霜鬓，潦倒新停浊酒杯。"},
    "虞美人": {"type": "诗词曲", "category": "必修", "author": "李煜",
        "content": "春花秋月何时了？往事知多少。\n\n小楼昨夜又东风，故国不堪回首月明中。\n\n雕栏玉砌应犹在，只是朱颜改。\n\n问君能有几多愁？恰似一江春水向东流。"},
    "琵琶行": {"type": "诗词曲", "category": "必修", "author": "白居易",
        "content": "浔阳江头夜送客，枫叶荻花秋瑟瑟。\n\n大弦嘈嘈如急雨，小弦切切如私语。\n\n别有幽咽泉流冷，凝绝不通声暂歇。\n\n银瓶乍破水浆迸，铁骑突出刀枪鸣。\n\n同是天涯沦落人，相逢何必曾相识。\n\n岂无山歌与村笛，呕哑嘲哳难为听。"},
    "沁园春长沙": {"type": "诗词曲", "category": "必修", "author": "毛泽东",
        "content": "独立寒秋，湘江北去，橘子洲头。\n\n看万山红遍，层林尽染；漫江碧透，百舸争流。\n\n鹰击长空，鱼翔浅底，万类霜天竞自由。\n\n怅寥廓，问苍茫大地，谁主沉浮？\n\n携来百侣曾游，忆往昔峥嵘岁月稠。\n\n恰同学少年，风华正茂；书生意气，挥斥方遒。\n\n曾记否，到中流击水，浪遏飞舟？"},
    "短歌行": {"type": "诗词曲", "category": "必修", "author": "曹操",
        "content": "对酒当歌，人生几何！譬如朝露，去日苦多。\n\n青青子衿，悠悠我心。\n\n呦呦鹿鸣，食野之苹。\n\n契阔谈讌，心念旧恩。\n\n月明星稀，乌鹊南飞。绕树三匝，何枝可依？\n\n山不厌高，海不厌深。周公吐哺，天下归心。"},
}


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
        """加载数据"""
        self.poetry_data = BUILTIN_POETRY.copy()
        if os.path.exists(POETRY_FILE):
            try:
                with open(POETRY_FILE, 'r', encoding='utf-8') as f:
                    user_data = json.load(f)
                    self.poetry_data.update(user_data)
            except:
                pass
        if os.path.exists(RECORDS_FILE):
            try:
                with open(RECORDS_FILE, 'r', encoding='utf-8') as f:
                    self.records = json.load(f)
            except:
                pass
    
    def save_data(self):
        """保存数据"""
        try:
            with open(RECORDS_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.records, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def build_ui(self):
        """构建界面"""
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # 标题
        title = Label(
            text='[size=24][b]古诗文背诵检测系统[/b][/size]\n[size=14]统编版高中语文72篇[/size]',
            markup=True,
            size_hint_y=0.12
        )
        layout.add_widget(title)
        
        # 分类按钮
        btn_layout = BoxLayout(size_hint_y=0.08, spacing=dp(5))
        categories = ['必修', '选择性必修', '选修', '个人新增', '文言文PDF']
        for cat in categories:
            btn = Button(
                text=cat,
                font_size='14sp',
                on_press=lambda x, c=cat: self.show_category(c)
            )
            btn_layout.add_widget(btn)
        layout.add_widget(btn_layout)
        
        # 内容区域
        self.content_label = Label(
            text='请选择分类查看古诗文\n\n点击下方按钮开始检测',
            markup=True,
            font_size='18sp',
            size_hint_y=0.65,
            halign='center',
            valign='middle'
        )
        self.content_label.bind(texture_size=self.content_label.setter('size'))
        layout.add_widget(self.content_label)
        
        # 底部按钮
        bottom_layout = BoxLayout(size_hint_y=0.15, spacing=dp(10))
        
        btn1 = Button(text='填空检测', font_size='18sp', 
                      on_press=self.start_fill_test)
        btn2 = Button(text='背诵记录', font_size='18sp',
                      on_press=self.show_records)
        
        bottom_layout.add_widget(btn1)
        bottom_layout.add_widget(btn2)
        layout.add_widget(bottom_layout)
        
        self.add_widget(layout)
    
    def show_category(self, category):
        """显示分类内容"""
        # 特殊处理：PDF分类
        if category == '文言文PDF':
            # 尝试用Android系统打开PDF
            if self.open_pdf():
                return
            # 如果打开失败，显示提示
            self.content_label.text = '[b]📄 高中文言文基础知识点全解读[/b]\n\n[color=F44336]无法打开PDF文件[/color]\n\n请安装PDF阅读器应用，或在电脑端查看。'
            return
        
        items = [(name, data) for name, data in self.poetry_data.items()
                 if data.get('category') == category]
        
        if not items:
            self.content_label.text = f'{category}分类暂无内容'
            return
        
        # 显示诗文列表
        text = f'[b]{category}[/b]\n\n'
        types = {'文言文': [], '诗词曲': []}
        for name, data in items:
            t = data.get('type', '文言文')
            if t in types:
                types[t].append(name)
        
        for t, names in types.items():
            if names:
                text += f'[color=2196F3]【{t}】[/color]\n'
                for name in names:
                    text += f'  • {name}\n'
                text += '\n'
        
        self.content_label.text = text
    
    def open_pdf(self):
        """用Android系统打开PDF文件"""
        if not ANDROID_AVAILABLE:
            print("[PDF] Android API不可用")
            return False
        
        try:
            # PDF文件路径
            pdf_path = os.path.join(os.path.dirname(__file__), '高中文言文基础知识点全解读.pdf')
            
            if not os.path.exists(pdf_path):
                print(f"[PDF] 文件不存在: {pdf_path}")
                return False
            
            print(f"[PDF] 尝试打开: {pdf_path}")
            
            # 创建File对象
            pdf_file = File(pdf_path)
            
            # 使用FileProvider获取URI (Android 7.0+)
            context = PYTHON_ACTIVITY.mActivity
            package_name = context.getPackageName()
            
            try:
                # 尝试使用FileProvider
                FileProvider = autoclass('androidx.core.content.FileProvider')
                uri = FileProvider.getUriForFile(
                    context,
                    f"{package_name}.fileprovider",
                    pdf_file
                )
            except:
                # 如果FileProvider失败，尝试直接使用file:// URI
                uri = Uri.fromFile(pdf_file)
            
            # 创建Intent打开PDF
            intent = Intent(Intent.ACTION_VIEW)
            intent.setDataAndType(uri, 'application/pdf')
            intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            
            # 启动Activity
            context.startActivity(intent)
            print("[PDF] 成功启动PDF阅读器")
            return True
            
        except Exception as e:
            print(f"[PDF] 打开失败: {e}")
            return False
    
    def start_fill_test(self, instance):
        """开始填空检测"""
        # 弹出选择窗口
        content = BoxLayout(orientation='vertical', spacing=dp(10))
        
        # 诗文列表
        scroll = ScrollView()
        list_layout = BoxLayout(orientation='vertical', spacing=dp(5), size_hint_y=None)
        list_layout.bind(minimum_height=list_layout.setter('height'))
        
        for name in sorted(self.poetry_data.keys()):
            btn = Button(
                text=name,
                size_hint_y=None,
                height=dp(50),
                font_size='16sp'
            )
            btn.bind(on_press=lambda x, n=name: self.do_fill_test(n))
            list_layout.add_widget(btn)
        
        scroll.add_widget(list_layout)
        content.add_widget(scroll)
        
        popup = Popup(
            title='选择要检测的古诗文',
            content=content,
            size_hint=(0.9, 0.8)
        )
        
        # 更新按钮绑定
        for child in list_layout.children:
            child.bind(on_press=lambda x: popup.dismiss())
        
        popup.open()
    
    def do_fill_test(self, poetry_name):
        """执行填空检测"""
        self.current_poetry = poetry_name
        self.manager.current = 'fill_test'
        self.manager.get_screen('fill_test').setup_test(poetry_name)
    
    def show_records(self, instance):
        """显示背诵记录"""
        if not self.records:
            popup = Popup(
                title='背诵记录',
                content=Label(text='暂无背诵记录', font_size='18sp'),
                size_hint=(0.8, 0.4)
            )
            popup.open()
            return
        
        text = ''
        for name, recs in self.records.items():
            text += f'[b]{name}[/b]\n'
            for r in recs[-5:]:  # 最近5条
                text += f"  {r['time']} | {r['score']:.0f}%\n"
            text += '\n'
        
        popup = Popup(
            title='背诵记录',
            content=Label(text=text, markup=True, font_size='14sp'),
            size_hint=(0.9, 0.7)
        )
        popup.open()


class FillTestScreen(Screen):
    """填空检测界面"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.answer_entries = []
        self.correct_answers = []
        self.layout = None
    
    def setup_test(self, poetry_name):
        """设置测试"""
        self.clear_widgets()
        self.answer_entries = []
        self.correct_answers = []
        
        # 获取诗文内容
        main_screen = self.manager.get_screen('main')
        content = main_screen.poetry_data.get(poetry_name, {}).get('content', '')
        
        # 按句分割
        sentences = [s.strip() for s in content.split('\n') if s.strip() and len(s.strip()) > 2]
        
        # 构建界面
        self.layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(5))
        
        # 标题
        self.layout.add_widget(Label(
            text=f'[b]{poetry_name}[/b]\n请填写空缺内容',
            markup=True,
            font_size='20sp',
            size_hint_y=0.08
        ))
        
        # 题目区域
        scroll = ScrollView(size_hint_y=0.75)
        questions_layout = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None)
        questions_layout.bind(minimum_height=questions_layout.setter('height'))
        
        for i, sentence in enumerate(sentences):
            # 半句挖空
            mid = len(sentence) // 2
            if mid < 2:
                mid = 2
            
            is_front = random.choice([True, False])
            
            if is_front:
                blank = sentence[:mid]
                show = sentence[mid:]
                hint = f'___ {show}'
            else:
                show = sentence[:mid]
                blank = sentence[mid:]
                hint = f'{show} ___'
            
            # 题目框
            q_box = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(70))
            q_box.add_widget(Label(
                text=f'第{i+1}句：{hint}',
                font_size='16sp',
                size_hint_y=0.4,
                halign='left',
                text_size=(Window.width - dp(40), None)
            ))
            
            entry = TextInput(
                hint_text='填写答案',
                font_size='18sp',
                size_hint_y=0.6,
                multiline=False
            )
            q_box.add_widget(entry)
            
            self.answer_entries.append(entry)
            self.correct_answers.append(blank)
            
            questions_layout.add_widget(q_box)
        
        scroll.add_widget(questions_layout)
        self.layout.add_widget(scroll)
        
        # 底部按钮
        btn_layout = BoxLayout(size_hint_y=0.12, spacing=dp(10))
        btn_layout.add_widget(Button(
            text='提交答案',
            font_size='18sp',
            on_press=self.submit_answers
        ))
        btn_layout.add_widget(Button(
            text='显示答案',
            font_size='18sp',
            on_press=self.show_answers
        ))
        btn_layout.add_widget(Button(
            text='返回',
            font_size='18sp',
            on_press=self.go_back
        ))
        self.layout.add_widget(btn_layout)
        
        self.add_widget(self.layout)
    
    def submit_answers(self, instance):
        """提交答案"""
        correct = 0
        total = len(self.answer_entries)
        
        for entry, answer in zip(self.answer_entries, self.correct_answers):
            user = entry.text.strip()
            # 简单比较（去标点）
            clean_user = user.replace('，', '').replace('。', '').replace(' ', '')
            clean_answer = answer.replace('，', '').replace('。', '').replace(' ', '')
            
            if clean_user == clean_answer:
                correct += 1
                entry.background_color = (0.5, 0.9, 0.5, 1)  # 绿色
            else:
                entry.background_color = (0.9, 0.5, 0.5, 1)  # 红色
        
        score = (correct / total * 100) if total > 0 else 0
        
        # 保存记录
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
        
        # 显示结果
        Popup(
            title='检测结果',
            content=Label(
                text=f'得分：{score:.0f}%\n正确：{correct}/{total}',
                font_size='20sp'
            ),
            size_hint=(0.7, 0.4)
        ).open()
    
    def show_answers(self, instance):
        """显示答案"""
        for entry, answer in zip(self.answer_entries, self.correct_answers):
            entry.text = answer
            entry.background_color = (1, 1, 1, 1)
    
    def go_back(self, instance):
        """返回主界面"""
        self.manager.current = 'main'


class PoetryApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(FillTestScreen(name='fill_test'))
        return sm
    
    def on_stop(self):
        """保存数据"""
        main_screen = self.root.get_screen('main')
        main_screen.save_data()


if __name__ == '__main__':
    PoetryApp().run()
