# -*- coding: utf-8 -*-
"""
高中古诗文背诵检测系统 - Kivy手机版（完整版）
统编版高中语文72篇必背古诗文
"""

import os
import json
import random
from datetime import datetime

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
from kivy.resources import resource_find

Window.clearcolor = (1, 1, 1, 1)

# Android平台
try:
    from jnius import autoclass
    PYTHON_ACTIVITY = autoclass('org.kivy.android.PythonActivity')
    Intent = autoclass('android.content.Intent')
    Uri = autoclass('android.net.Uri')
    ANDROID = True
except:
    ANDROID = False

# ========== 颜色 ==========
COLORS = {
    'primary': (0.2, 0.4, 0.8, 1),
    'secondary': (0.95, 0.95, 0.98, 1),
    'accent': (0.98, 0.73, 0.24, 1),
    'text_dark': (0.13, 0.13, 0.13, 1),
    'text_light': (0.4, 0.4, 0.4, 1),
    'success': (0.3, 0.69, 0.31, 1),
    'danger': (0.87, 0.32, 0.32, 1),
    'white': (1, 1, 1, 1),
}

# ========== 获取字体 ==========
def get_font():
    font = resource_find('DroidSansFallback.ttf')
    if font:
        return font
    paths = ['DroidSansFallback.ttf']
    for p in paths:
        if os.path.exists(p):
            return p
    return None

FONT = get_font()

BUILTIN_POETRY = {
    # ========== 文言文 32篇 ==========
    # 必修 10篇
    "论语十二章": {
        "type": "文言文",
        "category": "必修",
        "author": "孔子及其弟子",
        "content": """子曰：学而时习之，不亦说乎？有朋自远方来，不亦乐乎？人不知而不愠，不亦君子乎？

曾子曰：吾日三省吾身：为人谋而不忠乎？与朋友交而不信乎？传不习乎？

子曰：吾十有五而志于学，三十而立，四十而不惑，五十而知天命，六十而耳顺，七十而从心所欲，不逾矩。

子曰：温故而知新，可以为师矣。

子曰：学而不思则罔，思而不学则殆。

子曰：贤哉，回也！一箪食，一瓢饮，在陋巷，人不堪其忧，回也不改其乐。贤哉，回也！

子曰：知之者不如好之者，好之者不如乐之者。

子曰：饭疏食，饮水，曲肱而枕之，乐亦在其中矣。不义而富且贵，于我如浮云。

子曰：三人行，必有我师焉。择其善者而从之，其不善者而改之。

子在川上曰：逝者如斯夫，不舍昼夜。

子曰：三军可夺帅也，匹夫不可夺志也。

子夏曰：博学而笃志，切问而近思，仁在其中矣。"""
    },
    "劝学": {
        "type": "文言文",
        "category": "必修",
        "author": "荀子",
        "content": """君子曰：学不可以已。

青，取之于蓝，而青于蓝；冰，水为之，而寒于水。木直中绳，輮以为轮，其曲中规。虽有槁暴，不复挺者，輮使之然也。故木受绳则直，金就砺则利，君子博学而日参省乎己，则知明而行无过矣。

吾尝终日而思矣，不如须臾之所学也；吾尝跂而望矣，不如登高之博见也。登高而招，臂非加长也，而见者远；顺风而呼，声非加疾也，而闻者彰。假舆马者，非利足也，而致千里；假舟楫者，非能水也，而绝江河。君子生非异也，善假于物也。

积土成山，风雨兴焉；积水成渊，蛟龙生焉；积善成德，而神明自得，圣心备焉。故不积跬步，无以至千里；不积小流，无以成江海。骐骥一跃，不能十步；驽马十驾，功在不舍。锲而舍之，朽木不折；锲而不舍，金石可镂。蚓无爪牙之利，筋骨之强，上食埃土，下饮黄泉，用心一也。蟹六跪而二螯，非蛇鳝之穴无可寄托者，用心躁也。"""
    },
    "屈原列传": {
        "type": "文言文",
        "category": "必修",
        "author": "司马迁",
        "content": """屈平疾王听之不聪也，谗谄之蔽明也，邪曲之害公也，方正之不容也，故忧愁幽思而作《离骚》。离骚者，犹离忧也。夫天者，人之始也；父母者，人之本也。人穷则反本，故劳苦倦极，未尝不呼天也；疾痛惨怛，未尝不呼父母也。屈平正道直行，竭忠尽智以事其君，谗人间之，可谓穷矣。信而见疑，忠而被谤，能无怨乎？屈平之作《离骚》，盖自怨生也。

其志洁，故其称物芳；其行廉，故死而不容。自疏濯淖污泥之中，蝉蜕于浊秽，以浮游尘埃之外，不获世之滋垢，皭然泥而不滓者也。推此志也，虽与日月争光可也。"""
    },
    "谏太宗十思疏": {
        "type": "文言文",
        "category": "必修",
        "author": "魏征",
        "content": """臣闻：求木之长者，必固其根本；欲流之远者，必浚其泉源；思国之安者，必积其德义。源不深而望流之远，根不固而求木之长，德不厚而思国之安，臣虽下愚，知其不可，而况于明哲乎？

人君当神器之重，居域中之大，将崇极天之峻，永保无疆之休。不念居安思危，戒奢以俭，德不处其厚，情不胜其欲，斯亦伐根以求木茂，塞源而欲流长也。

凡百元首，承天景命，莫不殷忧而道著，功成而德衰。有善始者实繁，能克终者盖寡。岂其取之易守之难乎？盖在殷忧必竭诚以待下，既得志则纵情以傲物；竭诚则吴越为一体，傲物则骨肉为行路。

怨不在大，可畏惟人；载舟覆舟，所宜深慎。

诚能见可欲则思知足以自戒，将有作则思知止以安人，念高危则思谦冲以自牧，惧满溢则思江海下百川，乐盘游则思三驱以为度，忧懈怠则思慎始而敬终，虑壅蔽则思虚心以纳下，想谗邪则思正身以黜恶，恩所加则思无因喜以谬赏，罚所及则思无因怒而滥刑。

总此十思，宏兹九德，简能而任之，择善而从之，则智者尽其谋，勇者竭其力，仁者播其惠，信者效其忠。文武争驰，君臣无事，可以尽豫游之乐，可以养松乔之寿，鸣琴垂拱，不言而化。"""
    },
    "师说": {
        "type": "文言文",
        "category": "必修",
        "author": "韩愈",
        "content": """古之学者必有师。师者，所以传道受业解惑也。人非生而知之者，孰能无惑？惑而不从师，其为惑也，终不解矣。

生乎吾前，其闻道也固先乎吾，吾从而师之；生乎吾后，其闻道也亦先乎吾，吾从而师之。吾师道也，夫庸知其年之先后生于吾乎？是故无贵无贱，无长无少，道之所存，师之所存也。

嗟乎！师道之不传也久矣！欲人之无惑也难矣！古之圣人，其出人也远矣，犹且从师而问焉；今之众人，其下圣人也亦远矣，而耻学于师。

爱其子，择师而教之；于其身也，则耻师焉，惑矣。巫医乐师百工之人，不耻相师。士大夫之族，曰师曰弟子云者，则群聚而笑之。位卑则足羞，官盛则近谀。

圣人无常师。孔子师郯子、苌弘、师襄、老聃。闻道有先后，术业有专攻，如是而已。"""
    },
    "阿房宫赋": {
        "type": "文言文",
        "category": "必修",
        "author": "杜牧",
        "content": """六王毕，四海一；蜀山兀，阿房出。覆压三百余里，隔离天日。骊山北构而西折，直走咸阳。二川溶溶，流入宫墙。

五步一楼，十步一阁；廊腰缦回，檐牙高啄；各抱地势，钩心斗角。盘盘焉，囷囷焉，蜂房水涡，矗不知其几千万落。长桥卧波，未云何龙？复道行空，不霁何虹？

妃嫔媵嫱，王子皇孙，辞楼下殿，辇来于秦。明星荧荧，开妆镜也；绿云扰扰，梳晓鬟也；渭流涨腻，弃脂水也。

燕赵之收藏，韩魏之经营，齐楚之精英，鼎铛玉石，金块珠砾，弃掷逦迤。

奈何取之尽锱铢，用之如泥沙？

戍卒叫，函谷举；楚人一炬，可怜焦土。

灭六国者，六国也，非秦也。族秦者，秦也，非天下也。秦人不暇自哀，而后人哀之；后人哀之而不鉴之，亦使后人而复哀后人也。"""
    },
    "六国论": {
        "type": "文言文",
        "category": "必修",
        "author": "苏洵",
        "content": """六国破灭，非兵不利，战不善，弊在赂秦。赂秦而力亏，破灭之道也。

思厥先祖父，暴霜露，斩荆棘，以有尺寸之地。子孙视之不甚惜，举以予人，如弃草芥。

古人云：以地事秦，犹抱薪救火，薪不尽，火不灭。此言得之。

齐人未尝赂秦，终继五国迁灭，何哉？与嬴而不助五国也。

洎牧以谗诛，邯郸为郡，惜其用武而不终也。

夫六国与秦皆诸侯，其势弱于秦，而犹有可以不赂而胜之之势。苟以天下之大，下而从六国破亡之故事，是又在六国下矣。"""
    },
    "答司马谏议书": {
        "type": "文言文",
        "category": "必修",
        "author": "王安石",
        "content": """某启：昨日蒙教，窃以为与君实游处相好之日久，而议事每不合，所操之术多异故也。

虽欲强聒，终必不蒙见察，故略上报，不复一一自辨；重念蒙君实视遇厚，于反复不宜卤莽，故今具道所以。

今君实所以见教者，以为侵官、生事、征利、拒谏。

某则以谓受命于人主，议法度而修之于朝廷，以授之于有司，不为侵官；举先王之政，以兴利除弊，不为生事；为天下理财，不为征利；辟邪说，难壬人，不为拒谏。

盘庚之迁，胥怨者民也，非特朝廷士大夫而已。盘庚不为怨者故改其度，度义而后动，是而不见可悔故也。"""
    },
    "赤壁赋": {
        "type": "文言文",
        "category": "必修",
        "author": "苏轼",
        "content": """壬戌之秋，七月既望，苏子与客泛舟游于赤壁之下。清风徐来，水波不兴。举酒属客，诵明月之诗，歌窈窕之章。

少焉，月出于东山之上，徘徊于斗牛之间。白露横江，水光接天。纵一苇之所如，凌万顷之茫然。遗世独立，羽化而登仙。

客有吹洞箫者，倚歌而和之。舞幽壑之潜蛟，泣孤舟之嫠妇。

山川相缪，郁乎苍苍。

寄蜉蝣于天地，渺沧海之一粟。

逝者如斯，而未尝往也；盈虚者如彼，而卒莫消长也。

惟江上之清风，与山间之明月，耳得之而为声，目遇之而成色。取之无禁，用之不竭，是造物者之无尽藏也。"""
    },
    "项脊轩志": {
        "type": "文言文",
        "category": "必修",
        "author": "归有光",
        "content": """项脊轩，旧南阁子也。室仅方丈，可容一人居。百年老屋，尘泥渗漉，雨泽下注。

余稍为修葺，使不上漏。前辟四窗，垣墙周庭。

迨诸父异爨，内外多置小门。

家有老妪，先妣抚之甚厚。

吾家读书久不效，儿之成，则可待乎。顷之，持一象笏至。

余扃牖而居，久之，能以足音辨人。

庭有枇杷树，吾妻死之年所手植也，今已亭亭如盖矣。"""
    },
    # 选择性必修 10篇
    "子路曾皙冉有公西华侍坐": {
        "type": "文言文",
        "category": "选择性必修",
        "author": "《论语》",
        "content": """子路率尔而对曰：千乘之国，摄乎大国之间，加之以师旅，因之以饥馑。

冉有曰：方六七十，如五六十。

公西华曰：端章甫，愿为小相焉。

曾皙：鼓瑟希，铿尔，舍瑟而作。

莫春者，春服既成，浴乎沂，风乎舞雩，咏而归。"""
    },
    "报任安书": {
        "type": "文言文",
        "category": "选择性必修",
        "author": "司马迁",
        "content": """古者富贵而名摩灭，不可胜记，唯倜傥非常之人称焉。

盖文王拘而演《周易》；仲尼厄而作《春秋》；屈原放逐，乃赋《离骚》；左丘失明，厥有《国语》；孙子膑脚，《兵法》修列。

《诗》三百篇，大底圣贤发愤之所为作也。"""
    },
    "过秦论": {
        "type": "文言文",
        "category": "选择性必修",
        "author": "贾谊",
        "content": """秦孝公据崤函之固，拥雍州之地。

外连衡而斗诸侯。

合从缔交，相与为一。

始皇奋六世之余烈，履至尊而制六合。

隳名城，杀豪杰。

瓮牖绳枢之子，氓隶之人。

蹑足行伍之间，揭竿为旗。

一夫作难而七庙隳，身死人手，为天下笑者，何也？仁义不施，而攻守之势异也。"""
    },
    "礼运大同": {
        "type": "文言文",
        "category": "选择性必修",
        "author": "《礼记》",
        "content": """大道之行也，天下为公。

选贤与能，讲信修睦。

故人不独亲其亲，不独子其子。

矜、寡、孤、独、废疾者皆有所养。

货恶其弃于地也，不必藏于己；力恶其不出于身也，不必为己。

是故谋闭而不兴，盗窃乱贼而不作，故外户而不闭。是谓大同。"""
    },
    "陈情表": {
        "type": "文言文",
        "category": "选择性必修",
        "author": "李密",
        "content": """臣以险衅，夙遭闵凶。生孩六月，慈父见背。

门衰祚薄，茕茕孑立，形影相吊。

而刘夙婴疾病，常在床蓐。

前太守臣逵察臣孝廉，后刺史臣荣举臣秀才。

诏书切峻，责臣逋慢。

日薄西山，气息奄奄，人命危浅。

乌鸟私情，愿乞终养。

臣生当陨首，死当结草。"""
    },
    "归去来兮辞": {
        "type": "文言文",
        "category": "选择性必修",
        "author": "陶渊明",
        "content": """归去来兮，田园将芜胡不归？既自以心为形役，奚惆怅而独悲？

悟已往之不谏，知来者之可追。

乃瞻衡宇，载欣载奔。

三径就荒，松菊犹存。

木欣欣以向荣，泉涓涓而始流。

委心任去留，遑遑欲何之。"""
    },
    "种树郭橐驼传": {
        "type": "文言文",
        "category": "选择性必修",
        "author": "柳宗元",
        "content": """郭橐驼，病偻。

能顺木之天，以致其性焉。

其本欲舒，其培欲平，其土欲故。

长人者好烦其令，促尔耕，勖尔植。"""
    },
    "五代史伶官传序": {
        "type": "文言文",
        "category": "选择性必修",
        "author": "欧阳修",
        "content": """原庄宗之所以得天下。

庄宗受而藏之于庙，一少牢告庙。

方其系燕父子以组，函梁君臣之首。

满招损，谦得益。

忧劳可以兴国，逸豫可以亡身。

祸患常积于忽微，智勇多困于所溺。"""
    },
    "石钟山记": {
        "type": "文言文",
        "category": "选择性必修",
        "author": "苏轼",
        "content": """郦元以为下临深潭，微风鼓浪，水石相搏，声如洪钟。

寺僧使小童持斧，于乱石间择其一二扣之，硿硿焉。

栖鹘，磔磔云霄。

噌吰如钟鼓不绝，窾坎镗鞳。"""
    },
    "登泰山记": {
        "type": "文言文",
        "category": "选择性必修",
        "author": "姚鼐",
        "content": """泰山之阳，汶水西流；其阴，济水东流。

道皆砌石为磴，七千有余。

苍山负雪，明烛天南。

望晚日照城郭，徂徕如画。

摴蒱数十立者，山也。"""
    },
    # 选修 12篇
    "老子八章": {
        "type": "文言文",
        "category": "选修",
        "author": "老子",
        "content": """①上善若水。水善利万物而不争，处众人之所恶，故几于道。

②知人者智，自知者明。胜人者有力，自胜者强。

③大方无隅，大器晚成，大音希声，大象无形。

④千里之行，始于足下。

⑤为无为，则无不治。

⑥柔弱胜刚强。

⑦祸兮，福之所倚；福兮，祸之所伏。

⑧合抱之木，生于毫末；九层之台，起于累土。"""
    },
    "季氏将伐颛臾": {
        "type": "文言文",
        "category": "选修",
        "author": "《论语》",
        "content": """季氏将伐颛臾。冉有、子路见于孔子曰：季氏将有事于颛臾。

孔子曰：无乃尔是过与？夫颛臾，昔者先王以为东蒙主，且在邦域之中矣，是社稷之臣也，何以伐为？

陈力就列，不能者止。危而不持，颠而不扶，则将焉用彼相矣？

君子疾夫舍曰欲之而必为之辞。

不患寡而患不均，不患贫而患不安。"""
    },
    "大学": {
        "type": "文言文",
        "category": "选修",
        "author": "《礼记》",
        "content": """大学之道，在明明德，在亲民，在止于至善。

知止而后有定，定而后能静，静而后能安，安而后能虑，虑而后能得。

物有本末，事有终始，知所先后，则近道矣。"""
    },
    "孟子公孙丑上": {
        "type": "文言文",
        "category": "选修",
        "author": "孟子",
        "content": """天时不如地利，地利不如人和。

得道者多助，失道者寡助。寡助之至，亲戚畔之；多助之至，天下顺之。"""
    },
    "逍遥游": {
        "type": "文言文",
        "category": "选修",
        "author": "庄子",
        "content": """鹏之徙于南冥也，水击三千里，抟扶摇而上者九万里。

野马也，尘埃也，生物之以息相吹也。

小知不及大知，小年不及大年。

至人无己，神人无功，圣人无名。"""
    },
    "谏逐客书": {
        "type": "文言文",
        "category": "选修",
        "author": "李斯",
        "content": """臣闻地广者粟多，国大者人众，兵强则士勇。

是以泰山不让土壤，故能成其大；河海不择细流，故能就其深。

王者不却众庶，故能明其德。"""
    },
    "兰亭集序": {
        "type": "文言文",
        "category": "选修",
        "author": "王羲之",
        "content": """群贤毕至，少长咸集。

天朗气清，惠风和畅。

仰观宇宙之大，俯察品类之盛。

固知一死生为虚诞，齐彭殇为妄作。"""
    },
    "滕王阁序": {
        "type": "文言文",
        "category": "选修",
        "author": "王勃",
        "content": """落霞与孤鹜齐飞，秋水共长天一色。

渔舟唱晚，响穷彭蠡之滨；雁阵惊寒，声断衡阳之浦。"""
    },
    "黄冈竹楼记": {
        "type": "文言文",
        "category": "选修",
        "author": "王禹偁",
        "content": """竹之为瓦，仅十稔；若重覆之，得二十稔。

江山之外，第见风帆沙鸟、烟云竹树而已。"""
    },
    "上枢密韩太尉书": {
        "type": "文言文",
        "category": "选修",
        "author": "苏辙",
        "content": """文者，气之所形。

太史公行天下，周览四海名山大川。"""
    },
    "毛诗序": {
        "type": "文言文",
        "category": "选修",
        "author": "佚名",
        "content": """情动于中而形于言，言之不足，故嗟叹之。"""
    },
    "典论论文": {
        "type": "文言文",
        "category": "选修",
        "author": "曹丕",
        "content": """盖文章，经国之大业，不朽之盛事。"""
    },
    
    # ========== 诗词曲 40篇 ==========
    # 必修 12篇
    "沁园春长沙": {
        "type": "诗词曲",
        "category": "必修",
        "author": "毛泽东",
        "content": """独立寒秋，湘江北去，橘子洲头。

看万山红遍，层林尽染；漫江碧透，百舸争流。

鹰击长空，鱼翔浅底，万类霜天竞自由。

怅寥廓，问苍茫大地，谁主沉浮？

携来百侣曾游，忆往昔峥嵘岁月稠。

恰同学少年，风华正茂；书生意气，挥斥方遒。

曾记否，到中流击水，浪遏飞舟？"""
    },
    "短歌行": {
        "type": "诗词曲",
        "category": "必修",
        "author": "曹操",
        "content": """对酒当歌，人生几何！譬如朝露，去日苦多。

青青子衿，悠悠我心。

呦呦鹿鸣，食野之苹。

契阔谈讌，心念旧恩。

月明星稀，乌鹊南飞。绕树三匝，何枝可依？

山不厌高，海不厌深。周公吐哺，天下归心。"""
    },
    "归园田居其一": {
        "type": "诗词曲",
        "category": "必修",
        "author": "陶渊明",
        "content": """少无适俗韵，性本爱丘山。

误落尘网中，一去三十年。

羁鸟恋旧林，池鱼思故渊。

暧暧远人村，依依墟里烟。

久在樊笼里，复得返自然。"""
    },
    "梦游天姥吟留别": {
        "type": "诗词曲",
        "category": "必修",
        "author": "李白",
        "content": """海客谈瀛洲，烟涛微茫信难求。

天姥连天向天横，势拔五岳掩赤城。

渌水荡漾清猿啼，脚著谢公屐。

訇然中开，青冥浩荡不见底。

安能摧眉折腰事权贵，使我不得开心颜！"""
    },
    "登高": {
        "type": "诗词曲",
        "category": "必修",
        "author": "杜甫",
        "content": """风急天高猿啸哀，渚清沙白鸟飞回。

无边落木萧萧下，不尽长江滚滚来。

万里悲秋常作客，百年多病独登台。

艰难苦恨繁霜鬓，潦倒新停浊酒杯。"""
    },
    "琵琶行": {
        "type": "诗词曲",
        "category": "必修",
        "author": "白居易",
        "content": """浔阳江头夜送客，枫叶荻花秋瑟瑟。

大弦嘈嘈如急雨，小弦切切如私语。

别有幽咽泉流冷，凝绝不通声暂歇。

银瓶乍破水浆迸，铁骑突出刀枪鸣。

同是天涯沦落人，相逢何必曾相识。

岂无山歌与村笛，呕哑嘲哳难为听。"""
    },
    "念奴娇赤壁怀古": {
        "type": "诗词曲",
        "category": "必修",
        "author": "苏轼",
        "content": """大江东去，浪淘尽，千古风流人物。

故垒西边，人道是，三国周郎赤壁。

羽扇纶巾，谈笑间，樯橹灰飞烟灭。

人生如梦，一尊还酹江月。"""
    },
    "永遇乐京口北固亭怀古": {
        "type": "诗词曲",
        "category": "必修",
        "author": "辛弃疾",
        "content": """千古江山，英雄无觅孙仲谋处。

舞榭歌台，风流总被雨打风吹去。

可堪回首，佛狸祠下，一片神鸦社鼓。"""
    },
    "静女": {
        "type": "诗词曲",
        "category": "必修",
        "author": "《诗经》",
        "content": """静女其姝，俟我于城隅。爱而不见，搔首踟蹰。

静女其娈，贻我彤管。

自牧归荑，洵美且异。"""
    },
    "涉江采芙蓉": {
        "type": "诗词曲",
        "category": "必修",
        "author": "古诗十九首",
        "content": """涉江采芙蓉，兰泽多芳草。

采之欲遗谁？所思在远道。

还望旧乡，长路浩浩。

同心而离居，忧伤以终老。"""
    },
    "虞美人": {
        "type": "诗词曲",
        "category": "必修",
        "author": "李煜",
        "content": """春花秋月何时了？往事知多少。

小楼昨夜又东风，故国不堪回首月明中。

雕栏玉砌应犹在，只是朱颜改。

问君能有几多愁？恰似一江春水向东流。"""
    },
    "鹊桥仙": {
        "type": "诗词曲",
        "category": "必修",
        "author": "秦观",
        "content": """纤云弄巧，飞星传恨，银汉迢迢暗度。

金风玉露一相逢，便胜却人间无数。

两情若是久长时，又岂在朝朝暮暮。"""
    },
    # 选择性必修 18篇
    "无衣": {
        "type": "诗词曲",
        "category": "选择性必修",
        "author": "《诗经》",
        "content": """岂曰无衣？与子同袍。王于兴师，修我戈矛，与子同仇。

岂曰无衣？与子同泽。王于兴师，修我矛戟，与子偕作。"""
    },
    "春江花月夜": {
        "type": "诗词曲",
        "category": "选择性必修",
        "author": "张若虚",
        "content": """春江潮水连海平，海上明月共潮生。

滟滟随波千万里，何处春江无月明。

人生代代无穷已，江月年年望相似。"""
    },
    "山居秋暝": {
        "type": "诗词曲",
        "category": "选择性必修",
        "author": "王维",
        "content": """空山新雨后，天气晚来秋。

明月松间照，清泉石上流。

随意春芳歇，王孙自可留。"""
    },
    "蜀道难": {
        "type": "诗词曲",
        "category": "选择性必修",
        "author": "李白",
        "content": """蜀道之难，难于上青天。

扪参历井仰胁息，以手抚膺坐长叹。

连峰去天不盈尺，枯松倒挂倚绝壁。"""
    },
    "蜀相": {
        "type": "诗词曲",
        "category": "选择性必修",
        "author": "杜甫",
        "content": """丞相祠堂何处寻？锦官城外柏森森。

三顾频烦天下计，两朝开济老臣心。

出师未捷身先死，长使英雄泪满襟。"""
    },
    "客至": {
        "type": "诗词曲",
        "category": "选择性必修",
        "author": "杜甫",
        "content": """舍南舍北皆春水，但见群鸥日日来。

花径不曾缘客扫，蓬门今始为君开。"""
    },
    "登快阁": {
        "type": "诗词曲",
        "category": "选择性必修",
        "author": "黄庭坚",
        "content": """落木千山天远大，澄江一道月分明。

万里归船弄长笛，此心吾与白鸥盟。"""
    },
    "临安春雨初霁": {
        "type": "诗词曲",
        "category": "选择性必修",
        "author": "陆游",
        "content": """小楼一夜听春雨，深巷明朝卖杏花。

素衣莫起风尘叹，犹及清明可到家。"""
    },
    "声声慢": {
        "type": "诗词曲",
        "category": "选择性必修",
        "author": "李清照",
        "content": """寻寻觅觅，冷冷清清，凄凄惨惨戚戚。

梧桐更兼细雨，到黄昏、点点滴滴。"""
    },
    "书愤": {
        "type": "诗词曲",
        "category": "选择性必修",
        "author": "陆游",
        "content": """楼船夜雪瓜洲渡，铁马秋风大散关。

塞上长城空自许，镜中衰鬓已先斑。"""
    },
    "李凭箜篌引": {
        "type": "诗词曲",
        "category": "选择性必修",
        "author": "李贺",
        "content": """昆山玉碎凤凰叫，芙蓉泣露香兰笑。

女娲炼石补天处，石破天惊逗秋雨。"""
    },
    "菩萨蛮": {
        "type": "诗词曲",
        "category": "选择性必修",
        "author": "温庭筠",
        "content": """小山重叠金明灭，鬓云欲度香腮雪。

新帖绣罗襦，双双金鹧鸪。"""
    },
    "锦瑟": {
        "type": "诗词曲",
        "category": "选择性必修",
        "author": "李商隐",
        "content": """锦瑟无端五十弦，一弦一柱思华年。

庄生晓梦迷蝴蝶，望帝春心托杜鹃。"""
    },
    "望海潮": {
        "type": "诗词曲",
        "category": "选择性必修",
        "author": "柳永",
        "content": """东南形胜，三吴都会，钱塘自古繁华。

烟柳画桥，风帘翠幕，参差十万人家。"""
    },
    "扬州慢": {
        "type": "诗词曲",
        "category": "选择性必修",
        "author": "姜夔",
        "content": """淮左名都，竹西佳处，解鞍少驻初程。

废池乔木，犹厌言兵。"""
    },
    "燕歌行": {
        "type": "诗词曲",
        "category": "选择性必修",
        "author": "高适",
        "content": """大漠穷秋塞草腓，孤城落日斗兵稀。

战士军前半死生，美人帐下犹歌舞。"""
    },
    "拟行路难其四": {
        "type": "诗词曲",
        "category": "选择性必修",
        "author": "鲍照",
        "content": """泻水置平地，各自东西南北流。

人生亦有命，安能行叹复坐愁。"""
    },
    "长亭送别": {
        "type": "诗词曲",
        "category": "选择性必修",
        "author": "王实甫",
        "content": """碧云天，黄花地，西风紧，北雁南飞。

晓来谁染霜林醉？总是离人泪。"""
    },
    # 选修 10篇
    "氓": {
        "type": "诗词曲",
        "category": "选修",
        "author": "《诗经》",
        "content": """氓之蚩蚩，抱布贸丝。匪来贸丝，来即我谋。

夙兴夜寐，靡有朝矣。

信誓旦旦，不思其反。反是不思，亦已焉哉。"""
    },
    "离骚": {
        "type": "诗词曲",
        "category": "选修",
        "author": "屈原",
        "content": """长太息以掩涕兮，哀民生之多艰。

亦余心之所善兮，虽九死其犹未悔。

路漫漫其修远兮，吾将上下而求索。"""
    },
    "孔雀东南飞": {
        "type": "诗词曲",
        "category": "选修",
        "author": "佚名",
        "content": """孔雀东南飞，五里一徘徊。

君当作磐石，妾当作蒲苇。

蒲苇纫如丝，磐石无转移。"""
    },
    "白马篇": {
        "type": "诗词曲",
        "category": "选修",
        "author": "曹植",
        "content": """白马饰金羁，连翩西北驰。

捐躯赴国难，视死忽如归。"""
    },
    "饮酒其五": {
        "type": "诗词曲",
        "category": "选修",
        "author": "陶渊明",
        "content": """采菊东篱下，悠然见南山。

山气日夕佳，飞鸟相与还。"""
    },
    "行路难其一": {
        "type": "诗词曲",
        "category": "选修",
        "author": "李白",
        "content": """长风破浪会有时，直挂云帆济沧海。"""
    },
    "茅屋为秋风所破歌": {
        "type": "诗词曲",
        "category": "选修",
        "author": "杜甫",
        "content": """安得广厦千万间，大庇天下寒士俱欢颜。"""
    },
    "白雪歌送武判官归京": {
        "type": "诗词曲",
        "category": "选修",
        "author": "岑参",
        "content": """忽如一夜春风来，千树万树梨花开。"""
    },
    "雁门太守行": {
        "type": "诗词曲",
        "category": "选修",
        "author": "李贺",
        "content": """黑云压城城欲摧，甲光向日金鳞开。"""
    },
    "水龙吟登建康赏心亭": {
        "type": "诗词曲",
        "category": "选修",
        "author": "辛弃疾",
        "content": """楚天千里清秋，水随天去秋无际。

把吴钩看了，栏杆拍遍，无人会，登临意。"""
    }
}


# ========== 数据目录 ==========
def get_data_dir():
    if ANDROID:
        try:
            return PYTHON_ACTIVITY.mActivity.getFilesDir().getPath()
        except:
            pass
    return os.path.dirname(os.path.abspath(__file__)) if os.path.dirname(__file__) else os.getcwd()

DATA_DIR = get_data_dir()
RECORDS_FILE = os.path.join(DATA_DIR, "recite_records.json")

def load_records():
    try:
        if os.path.exists(RECORDS_FILE):
            with open(RECORDS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    return {}

def save_records(records):
    try:
        with open(RECORDS_FILE, 'w', encoding='utf-8') as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
    except:
        pass

# ========== 主界面 ==========
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.records = load_records()
        self.current_poetry = None
        self._popup = None
        self._records_popup = None
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        
        # 标题
        layout.add_widget(Label(
            text='高中古诗文背诵检测',
            font_name=FONT,
            font_size='24sp',
            color=COLORS['primary'],
            size_hint_y=0.1,
            bold=True
        ))
        
        # 分类按钮 - 第一行
        self.category_btns1 = BoxLayout(size_hint_y=0.06, spacing=dp(5))
        for cat in ['全部', '必修', '选择性必修']:
            btn = Button(
                text=cat,
                font_name=FONT,
                font_size='14sp',
                background_color=COLORS['primary'] if cat == '全部' else (0.6, 0.6, 0.6, 1)
            )
            btn.bind(on_press=lambda x, c=cat: self.filter_category(c))
            self.category_btns1.add_widget(btn)
        layout.add_widget(self.category_btns1)
        
        # 分类按钮 - 第二行
        self.category_btns2 = BoxLayout(size_hint_y=0.06, spacing=dp(5))
        for cat in ['选修', '文言文', '诗词曲']:
            btn = Button(
                text=cat,
                font_name=FONT,
                font_size='14sp',
                background_color=(0.6, 0.6, 0.6, 1)
            )
            btn.bind(on_press=lambda x, c=cat: self.filter_category(c))
            self.category_btns2.add_widget(btn)
        layout.add_widget(self.category_btns2)
        
        # 列表区域
        scroll = ScrollView(size_hint_y=0.68)
        self.list_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(8))
        self.list_layout.bind(minimum_height=self.list_layout.setter('height'))
        scroll.add_widget(self.list_layout)
        layout.add_widget(scroll)
        
        # 底部按钮
        bottom = BoxLayout(size_hint_y=0.1, spacing=dp(10))
        
        btn_pdf = Button(
            text='文言文PDF',
            font_name=FONT,
            background_color=COLORS['accent']
        )
        btn_pdf.bind(on_press=self.open_pdf)
        bottom.add_widget(btn_pdf)
        
        btn_records = Button(
            text='查看记录',
            font_name=FONT,
            background_color=(0.5, 0.5, 0.5, 1)
        )
        btn_records.bind(on_press=self.show_records)
        bottom.add_widget(btn_records)
        layout.add_widget(bottom)
        
        self.add_widget(layout)
        self.filter_category('全部')
    
    def filter_category(self, category):
        # 更新按钮状态
        for btn in self.category_btns1.children:
            btn.background_color = COLORS['primary'] if btn.text == category else (0.6, 0.6, 0.6, 1)
        for btn in self.category_btns2.children:
            btn.background_color = COLORS['primary'] if btn.text == category else (0.6, 0.6, 0.6, 1)
        
        self.list_layout.clear_widgets()
        
        if category == '全部':
            items = list(BUILTIN_POETRY.items())
        elif category in ['文言文', '诗词曲']:
            items = [(n, d) for n, d in BUILTIN_POETRY.items() if d.get('type') == category]
        else:
            # 必修、选择性必修、选修
            items = [(n, d) for n, d in BUILTIN_POETRY.items() if d.get('category') == category]
        
        for name, data in items:
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=dp(5))
            
            info = BoxLayout(orientation='vertical')
            info.add_widget(Label(
                text=name,
                font_name=FONT,
                color=COLORS['text_dark'],
                font_size='16sp',
                size_hint_y=0.6
            ))
            info.add_widget(Label(
                text=f"{data.get('author', '')} · {data.get('category', '')}",
                font_name=FONT,
                color=COLORS['text_light'],
                font_size='12sp',
                size_hint_y=0.4
            ))
            box.add_widget(info)
            
            btn = Button(
                text='背诵',
                font_name=FONT,
                size_hint_x=0.3,
                background_color=COLORS['success']
            )
            btn.bind(on_press=lambda x, n=name: self.select_poetry(n))
            box.add_widget(btn)
            
            self.list_layout.add_widget(box)
    
    def select_poetry(self, name):
        self.current_poetry = name
        data = BUILTIN_POETRY.get(name, {})
        
        content = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        
        # 作者信息
        info_label = Label(
            text=f"作者：{data.get('author', '')}  |  {data.get('category', '')}",
            font_name=FONT,
            color=COLORS['text_light'],
            font_size='14sp',
            size_hint_y=0.08
        )
        content.add_widget(info_label)
        
        # 诗文内容
        scroll = ScrollView(size_hint_y=0.77)
        text_label = Label(
            text=data.get('content', ''),
            font_name=FONT,
            color=COLORS['text_dark'],
            font_size='18sp',
            size_hint_y=None,
            halign='left',
            valign='top'
        )
        text_label.bind(texture_size=text_label.setter('size'))
        scroll.add_widget(text_label)
        content.add_widget(scroll)
        
        # 按钮
        btns = BoxLayout(size_hint_y=0.15, spacing=dp(10))
        
        btn_test = Button(
            text='背诵检测',
            font_name=FONT,
            background_color=COLORS['primary']
        )
        btn_test.bind(on_press=lambda x: self.start_test(name))
        btns.add_widget(btn_test)
        
        btn_close = Button(
            text='关闭',
            font_name=FONT,
            background_color=(0.6, 0.6, 0.6, 1)
        )
        btn_close.bind(on_press=lambda x: self._popup.dismiss())
        btns.add_widget(btn_close)
        content.add_widget(btns)
        
        self._popup = Popup(
            title=name,
            title_font=FONT,
            title_color=COLORS['text_dark'],
            content=content,
            size_hint=(0.9, 0.85),
            background='',
            background_color=COLORS['white']
        )
        self._popup.open()
    
    def start_test(self, name):
        if self._popup:
            self._popup.dismiss()
        self.manager.current = 'fill_test'
        self.manager.get_screen('fill_test').setup_test(name)
    
    def open_pdf(self, instance):
        """打开PDF文件"""
        if ANDROID:
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
        
        # 无法打开PDF时的提示
        Popup(
            title='提示',
            title_font=FONT,
            content=Label(
                text='请在电脑端查看PDF文件\n或安装PDF阅读器',
                font_name=FONT,
                color=COLORS['text_dark']
            ),
            size_hint=(0.7, 0.3),
            background='',
            background_color=COLORS['white']
        ).open()
    
    def show_records(self, instance):
        content = BoxLayout(orientation='vertical', padding=dp(10))
        scroll = ScrollView()
        layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(5))
        layout.bind(minimum_height=layout.setter('height'))
        
        if not self.records:
            layout.add_widget(Label(
                text='暂无背诵记录',
                font_name=FONT,
                color=COLORS['text_light'],
                size_hint_y=None,
                height=dp(40)
            ))
        else:
            for name, recs in self.records.items():
                for r in recs[-5:]:
                    layout.add_widget(Label(
                        text=f"{name} - {r.get('score', 0):.0f}% - {r.get('time', '')}",
                        font_name=FONT,
                        color=COLORS['text_dark'],
                        size_hint_y=None,
                        height=dp(30),
                        font_size='14sp'
                    ))
        
        scroll.add_widget(layout)
        content.add_widget(scroll)
        
        close_btn = Button(
            text='关闭',
            font_name=FONT,
            size_hint_y=0.1,
            background_color=(0.6, 0.6, 0.6, 1)
        )
        close_btn.bind(on_press=lambda x: self._records_popup.dismiss())
        content.add_widget(close_btn)
        
        self._records_popup = Popup(
            title='背诵记录',
            title_font=FONT,
            content=content,
            size_hint=(0.9, 0.8),
            background='',
            background_color=COLORS['white']
        )
        self._records_popup.open()
    
    def save_data(self):
        save_records(self.records)

# ========== 填空检测界面 ==========
class FillTestScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.answer_entries = []
        self.correct_answers = []
    
    def setup_test(self, poetry_name):
        data = BUILTIN_POETRY.get(poetry_name, {})
        content = data.get('content', '')
        
        self.clear_widgets()
        self.answer_entries = []
        self.correct_answers = []
        
        layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        
        layout.add_widget(Label(
            text=f'填空检测：{poetry_name}',
            font_name=FONT,
            font_size='18sp',
            color=COLORS['primary'],
            size_hint_y=0.08
        ))
        
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
            q_box.add_widget(Label(
                text=f'第{i+1}句：{hint}',
                font_name=FONT,
                color=COLORS['text_dark'],
                font_size='16sp',
                size_hint_y=0.4
            ))
            
            entry = TextInput(
                hint_text='填写答案',
                font_name=FONT,
                font_size='16sp',
                size_hint_y=0.6,
                multiline=False,
                background_color=COLORS['secondary']
            )
            q_box.add_widget(entry)
            
            self.answer_entries.append(entry)
            self.correct_answers.append(blank)
            q_layout.add_widget(q_box)
        
        scroll.add_widget(q_layout)
        layout.add_widget(scroll)
        
        btn_layout = BoxLayout(size_hint_y=0.12, spacing=dp(10))
        
        btn_submit = Button(
            text='提交',
            font_name=FONT,
            background_color=COLORS['primary']
        )
        btn_submit.bind(on_press=self.submit_answers)
        btn_layout.add_widget(btn_submit)
        
        btn_answer = Button(
            text='答案',
            font_name=FONT,
            background_color=COLORS['accent']
        )
        btn_answer.bind(on_press=self.show_answers)
        btn_layout.add_widget(btn_answer)
        
        btn_back = Button(
            text='返回',
            font_name=FONT,
            background_color=(0.6, 0.6, 0.6, 1)
        )
        btn_back.bind(on_press=self.go_back)
        btn_layout.add_widget(btn_back)
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
        
        Popup(
            title='检测结果',
            title_font=FONT,
            content=Label(
                text=f'得分：{score:.0f}%\n正确：{correct}/{total}',
                font_name=FONT,
                color=COLORS['text_dark'],
                font_size='20sp'
            ),
            size_hint=(0.7, 0.4),
            background='',
            background_color=COLORS['white']
        ).open()
    
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
