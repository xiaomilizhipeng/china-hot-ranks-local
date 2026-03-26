# china-hot-ranks-local

一个可直接运行的本地热榜聚合仓库，当前稳定支持：
- GitHub Trending
- CSDN 全站综合热榜
- B站热门
- 百度热搜

## 目录

- `skill/china-hot-ranks-local/`：OpenClaw Skill
- `scripts/morning_hot_ranks.sh`：生成每日热榜 markdown 并输出到终端

## 依赖

- Python 3.10+
- `requests`

安装依赖：

```bash
python3 -m pip install requests
```

## 用法

### 单个平台

```bash
python3 skill/china-hot-ranks-local/scripts/hot_ranks_local.py github
python3 skill/china-hot-ranks-local/scripts/hot_ranks_local.py csdn
python3 skill/china-hot-ranks-local/scripts/hot_ranks_local.py bilibili
python3 skill/china-hot-ranks-local/scripts/hot_ranks_local.py baidu
```

### 全部平台

```bash
python3 skill/china-hot-ranks-local/scripts/hot_ranks_local.py all
```

### 生成每日 markdown

```bash
./scripts/morning_hot_ranks.sh
```

输出文件会落到：

```text
./briefs/YYYY-MM-DD-hot-ranks.md
```
