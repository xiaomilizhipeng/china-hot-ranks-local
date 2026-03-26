---
name: china-hot-ranks-local
description: 获取中国平台热榜与技术榜单的本地技能。当前稳定支持 GitHub Trending、CSDN 全站综合热榜、B站热门、百度热搜。优先使用稳定公开页面或公开接口，不依赖额外本地后端。用户提到“热榜、热搜、GitHub Trending、CSDN 热榜、B站热门、百度热搜、热点聚合、榜单抓取”时使用。
---

# China Hot Ranks Local

使用本技能时，优先运行脚本而不是手写抓取逻辑。

## 脚本

主脚本：`/home/xp/openclaw/skills/china-hot-ranks-local/scripts/hot_ranks_local.py`

## 支持的平台

- `github`：GitHub Trending
- `csdn`：CSDN 全站综合热榜
- `bilibili`：B站热门
- `baidu`：百度热搜（realtime）
- `all`：同时获取上述来源

## 用法

### 获取单个平台

```bash
python3 /home/xp/openclaw/skills/china-hot-ranks-local/scripts/hot_ranks_local.py github
python3 /home/xp/openclaw/skills/china-hot-ranks-local/scripts/hot_ranks_local.py csdn
python3 /home/xp/openclaw/skills/china-hot-ranks-local/scripts/hot_ranks_local.py bilibili
python3 /home/xp/openclaw/skills/china-hot-ranks-local/scripts/hot_ranks_local.py baidu
```

### 同时获取全部支持的平台

```bash
python3 /home/xp/openclaw/skills/china-hot-ranks-local/scripts/hot_ranks_local.py all
```

### 需要结构化结果时输出 JSON

```bash
python3 /home/xp/openclaw/skills/china-hot-ranks-local/scripts/hot_ranks_local.py all --json
```

## 说明

- GitHub 无官方 Trending API；本技能抓取 Trending 页面并解析。
- CSDN 私有接口容易风控；本技能优先抓取榜单页面而不是私有接口。
- B站优先使用公开热门接口 `x/web-interface/popular`。
- 百度优先抓取 `top.baidu.com/board?tab=realtime` 的页面文本。
- 知乎、微博、掘金在当前网络环境中不稳定：知乎 403、微博访客墙、掘金 451，因此暂不默认接入。
- 如果页面结构变化导致解析失败，先检查对应来源的文本结构，再更新脚本。
