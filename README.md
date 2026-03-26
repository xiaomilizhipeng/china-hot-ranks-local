# china-hot-ranks-local

一个可直接运行的本地热榜聚合仓库，当前稳定支持：

- GitHub Trending
- CSDN 全站综合热榜
- B站热门
- 百度热搜

这个仓库包含两部分：

1. `skill/china-hot-ranks-local/`：可放入 OpenClaw 的本地 Skill
2. `scripts/morning_hot_ranks.sh`：每天生成热榜 markdown 的辅助脚本

---

## 目录结构

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

## 支持的平台

当前稳定支持以下 4 个来源：

- `github`：GitHub Trending
- `csdn`：CSDN 全站综合热榜
- `bilibili`：B站热门
- `baidu`：百度热搜（realtime）

暂未默认接入的平台：

- 知乎：当前网络环境下常见 403 占位页
- 微博：访客墙导致文本不可稳定提取
- 掘金：Jina 当前可能返回 451 限制

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

## 生成每日 markdown

```bash
./scripts/morning_hot_ranks.sh
```

脚本会：

1. 调用热榜聚合脚本抓取全部可用平台
2. 生成一份 markdown 报告
3. 输出到终端
4. 同时保存到：

```text
./briefs/YYYY-MM-DD-hot-ranks.md
```

---

## OpenClaw 中使用

如果你要把它作为本地 Skill 使用，可将：

```text
skill/china-hot-ranks-local/
```

放入 OpenClaw 的技能目录，然后按 `SKILL.md` 中的说明调用。

---

## 定时任务示例（工作日 9 点）

如果你想在 OpenClaw 里设置 **每个工作日早上 9 点自动抓取热榜并发送到 QQ**，可以参考下面的思路：

### 1）先准备输出脚本

```bash
/home/xp/openclaw/scripts/morning_hot_ranks.sh
```

### 2）创建 cron

```bash
openclaw cron add \
  --name "workday-9am-hot-ranks-to-qq" \
  --cron "0 9 * * 1-5" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --wake now \
  --announce \
  --channel qqbot \
  --to "qqbot:c2c:YOUR_TARGET" \
  --timeout-seconds 300 \
  --message "请你在 Linux 环境执行命令：/home/xp/openclaw/scripts/morning_hot_ranks.sh 。然后把命令输出原样作为一条消息发送给用户。不要解释执行过程。"
```

这样就能实现：

- 工作日 9 点自动运行
- 自动抓取热榜
- 自动保存到 `briefs/`
- 自动发送到目标 QQ 会话

---

## 设计思路

- GitHub：抓 Trending 页面并解析
- CSDN：抓排行榜页面并解析
- B站：优先走公开热门接口
- 百度：抓 realtime 热搜页文本
- 网络层：代理失败时自动尝试直连，减少因本地代理异常导致的失败

---

## License

本仓库当前未单独附加 license 文件；如需开源分发，建议补一个 MIT License 喵~
