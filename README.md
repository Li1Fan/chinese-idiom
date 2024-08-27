# chinese-idiom
中文成语数据库、汉语成语数据库，共计收录48766个成语。

本数据库收集自网络，初衷是在自己的机器人加入“成语接龙”游戏，因[已有数据库](https://github.com/pwxcoo/chinese-xinhua)不全，所以自己重新收集。本项目仅作为学习使用，特此声明，如有侵权，将及时删除。

#### 目录结构

```shell
├── data
│   ├── idiom.csv
│   ├── idiom.db
│   └── idiom.json
├── LICENSE
├── README.md
└── scripts
    ├── crawling.py
    ├── csv2db.py
    ├── db2csv.py
    └── db2json.py
```

#### 类别

成语归在`data/`目录底下，三种类型

idiom.db

```shell
sqlite> pragma table_info(idiom);
0|id|INTEGER|0||1
1|derivation|TEXT|0||0
2|example|TEXT|0||0
3|explanation|TEXT|0||0
4|pinyin|TEXT|0||0
5|word|TEXT|0||0
6|abbreviation|TEXT|0||0
7|pinyin_r|TEXT|0||0
8|first|TEXT|0||0
9|last|TEXT|0||0
sqlite> select * from idiom limit 3;
1|北宋・程颢《春日偶成诗》：“云淡风轻近午天，傍花随柳过前川。”|元·徐琰《青楼十咏·初见》：“一笑情通，傍柳随花，偎香倚玉，弄月搏风。”|春天依倚花草柳树而游乐的情调。比喻狎妓。|bàng liǔ suí huā|傍柳随花|blsh|bang liu sui hua|bang|hua
2|元・曾瑞《留鞋记》楔子：“自谓状元探手可得，岂知时运不济，榜上无名，屡次束装而回。”|这话令兄也说过，若榜上无名，大家莫想他回来。（清・李汝珍《镜花缘》第四十二回）|张贴的名单上没有名字。泛指落选。|bǎng shàng wú míng|榜上无名|bswm|bang shang wu ming|bang|ming
3|明・孙仁孺《东郭记・人之所以求富贵利达者》：“尽宇内秦楚燕韩，傍门依户者，共是俺一家友生。”||傍：依傍，靠着；门、户：家。依靠在别人门庭上。指依赖别人，不能自立。|bàng mén yī hù|傍门依户|bmyh|bang men yi hu|bang|hu
sqlite> 
```

idiom.csv

| derivation                                                   | example                                                      | explanation                              | pinyin           | word     | abbreviation |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ---------------------------------------- | ---------------- | -------- | ------------ |
| 北宋・程颢《春日偶成诗》：“云淡风轻近午天，傍花随柳过前川。” | 元·徐琰《青楼十咏·初见》：“一笑情通，傍柳随花，偎香倚玉，弄月搏风。” | 春天依倚花草柳树而游乐的情调。比喻狎妓。 | bàng liǔ suí huā | 傍柳随花 | blsh         |

idiom.json

```json
[
    {
        "derivation": "北宋・程颢《春日偶成诗》：“云淡风轻近午天，傍花随柳过前川
。”",
        "example": "元·徐琰《青楼十咏·初见》：“一笑情通，傍柳随花，偎香倚玉，弄>月搏风。”",
        "explanation": "春天依倚花草柳树而游乐的情调。比喻狎妓。",
        "pinyin": "bàng liǔ suí huā",
        "word": "傍柳随花",
        "abbreviation": "blsh",
        "pinyin_r": "bang liu sui hua",
        "first": "bang",
        "last": "hua"
    }]
```

