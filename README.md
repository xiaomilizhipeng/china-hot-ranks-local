# china-hot-ranks-local

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg) ![Version](https://img.shields.io/badge/version-v0.1.0-blue.svg)

一个本地可运行的中国热榜聚合仓库，当前稳定支持：

- GitHub Trending
- CSDN 全站综合热榜
- B站热门
- 百度热搜

这个仓库面向两类用途：

1. 作为 OpenClaw 本地 Skill 使用
2. 作为命令行脚本直接获取热榜、生成每日简报

---

## 仓库结构

```text
china-hot-ranks-local/
├── README.md
├── .gitignore
├── skill/
│   └── china-hot-ranks-local/
│       ├── SKILL.md
│       ├── scripts/
│       │   └── hot_ranks_local.py
│       └── references/
│           └── notes.md
└── scripts/
    └── morning_hot_ranks.sh
```

---

## 当前支持的平台

- `github`：GitHub Trending
- `csdn`：CSDN 全站综合热榜
- `bilibili`：B站热门
- `baidu`：百度热搜（realtime）

## 当前未默认启用的平台

- 知乎：在当前网络环境中常出现 403 占位页
- 微博：访客墙导致内容提取不稳定
- 掘金：Jina 侧可能返回 451 限制

---

## 依赖

- Python 3.10+
- `requests`

安装依赖：

```bash
python3 -m pip install requests
```

---

## 命令行用法

### 获取单个平台

```bash
python3 skill/china-hot-ranks-local/scripts/hot_ranks_local.py github
python3 skill/china-hot-ranks-local/scripts/hot_ranks_local.py csdn
python3 skill/china-hot-ranks-local/scripts/hot_ranks_local.py bilibili
python3 skill/china-hot-ranks-local/scripts/hot_ranks_local.py baidu
```

### 获取全部平台

```bash
python3 skill/china-hot-ranks-local/scripts/hot_ranks_local.py all
```

### 控制条数

```bash
python3 skill/china-hot-ranks-local/scripts/hot_ranks_local.py all --limit 5
```

### 输出 JSON

```bash
python3 skill/china-hot-ranks-local/scripts/hot_ranks_local.py all --json
```

---

## 每日简报脚本

```bash
./scripts/morning_hot_ranks.sh
```

脚本会：

1. 获取全部可用热榜
2. 生成一份 markdown 报告
3. 输出到终端
4. 同时保存到：

```text
./briefs/YYYY-MM-DD-hot-ranks.md
```

如果你把公众号选题助手也接进来，它还可以继续联动生成每日选题结果。

---

## OpenClaw 中使用

如果你要把它作为本地 Skill 使用，可将：

```text
skill/china-hot-ranks-local/
```

放入 OpenClaw 的技能目录，然后按 `SKILL.md` 中的说明调用。

---

## 设计思路

- GitHub：抓 Trending 页面并解析
- CSDN：抓排行榜页面并解析
- B站：优先使用公开热门接口
- 百度：抓 realtime 热搜页文本
- 网络层：代理失败时自动尝试直连，降低因代理异常导致的失败率

---

## License

MIT
