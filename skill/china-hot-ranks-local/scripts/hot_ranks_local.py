#!/usr/bin/env python3
import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from typing import List

import requests

JINA_PREFIX = "https://r.jina.ai/http://"
UA = {"User-Agent": "Mozilla/5.0"}
BILI_HEADERS = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.bilibili.com"}


@dataclass
class RankItem:
    rank: int
    title: str
    url: str
    meta: str = ""


def http_get(url: str, headers: dict, timeout: int = 30) -> requests.Response:
    last_error = None
    for trust_env in (True, False):
        session = requests.Session()
        session.trust_env = trust_env
        try:
            resp = session.get(url, headers=headers, timeout=timeout)
            resp.raise_for_status()
            return resp
        except Exception as e:
            last_error = e
        finally:
            session.close()
    raise last_error


def fetch_markdown(url: str, timeout: int = 30) -> str:
    resp = http_get(
        JINA_PREFIX + url.replace('https://', '').replace('http://', ''),
        headers=UA,
        timeout=timeout,
    )
    return resp.text


def parse_github_trending(md: str, limit: int = 10) -> List[RankItem]:
    lines = md.splitlines()
    items: List[RankItem] = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        m = re.match(r'^##?\s*\[(.+?)\]\((https?://github\.com/[^)]+)\)$', line)
        if m and '/trending' not in m.group(2):
            title = re.sub(r'\s+', ' ', m.group(1)).replace(' / ', '/').strip()
            url = m.group(2)
            meta_parts = []
            for j in range(i + 1, min(i + 8, len(lines))):
                s = lines[j].strip()
                if not s:
                    continue
                if 'Built by' in s:
                    break
                if s.startswith('[') and 'github.com/' in s:
                    continue
                if s in {'Star', 'Fork'}:
                    continue
                if len(s) < 180:
                    meta_parts.append(s)
            meta = ' | '.join(dict.fromkeys(meta_parts))
            items.append(RankItem(len(items) + 1, title, url, meta))
            if len(items) >= limit:
                break
        i += 1
    return items


def parse_csdn_rank(md: str, limit: int = 10) -> List[RankItem]:
    lines = md.splitlines()
    start = 0
    for idx, line in enumerate(lines):
        if '全站综合热榜' in line:
            start = idx
            break

    items: List[RankItem] = []
    i = start
    while i < len(lines):
        line = lines[i].strip()
        if re.fullmatch(r'\d+', line):
            rank = int(line)
            title = ''
            url = ''
            meta_parts = []
            for j in range(i + 1, min(i + 12, len(lines))):
                s = lines[j].strip()
                m = re.match(r'^\[(.+?)\]\((https?://blog\.csdn\.net/[^)]+)\)$', s)
                if m and not title:
                    title = re.sub(r'\s+', ' ', m.group(1)).strip()
                    url = m.group(2)
                    continue
                if any(k in s for k in ['浏览', '评论', '收藏', '热度']):
                    meta_parts.append(s)
                if title and url and meta_parts:
                    break
            if title and url:
                items.append(RankItem(rank, title, url, ' | '.join(meta_parts)))
                if len(items) >= limit:
                    break
        i += 1
    return items


def parse_baidu_realtime(md: str, limit: int = 10) -> List[RankItem]:
    lines = md.splitlines()
    items: List[RankItem] = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        m = re.match(r'^\[(\d+) .*\]\((https?://www\.baidu\.com/s\?wd=[^)]+)\)$', line)
        if m:
            rank = int(m.group(1))
            url = m.group(2)
            title = ''
            meta = ''
            for j in range(i + 1, min(i + 14, len(lines))):
                s = lines[j].strip()
                if not meta and re.fullmatch(r'\d{3,}', s):
                    meta = f'热搜指数 {s}'
                m2 = re.match(r'^\[(.+?)\]\((https?://www\.baidu\.com/s\?wd=[^)]+)\)$', s)
                if m2:
                    candidate = re.sub(r'\s+', ' ', m2.group(1)).strip()
                    if not re.match(r'^\d+$', candidate) and 'Image' not in candidate and candidate != '查看更多>':
                        title = candidate
                        break
            if title:
                items.append(RankItem(rank, title, url, meta))
                if len(items) >= limit:
                    break
        i += 1
    return items


def get_bilibili_popular(limit: int = 10) -> List[RankItem]:
    r = http_get(
        f'https://api.bilibili.com/x/web-interface/popular?ps={limit}&pn=1',
        headers=BILI_HEADERS,
        timeout=20,
    )
    data = r.json()
    if data.get('code') != 0:
        raise RuntimeError(f"Bilibili API error: {data.get('code')} {data.get('message')}")
    items: List[RankItem] = []
    for idx, item in enumerate(data['data']['list'][:limit], 1):
        stat = item.get('stat', {}) or {}
        view = stat.get('view')
        meta = f'播放 {view}' if view is not None else ''
        url = item.get('short_link_v2') or f"https://www.bilibili.com/video/{item.get('bvid', '')}"
        items.append(RankItem(idx, item.get('title', '').strip(), url, meta))
    return items


def get_platform(platform: str, limit: int = 10) -> List[RankItem]:
    platform = platform.lower()
    if platform == 'github':
        return parse_github_trending(fetch_markdown('https://github.com/trending'), limit=limit)
    if platform == 'csdn':
        return parse_csdn_rank(fetch_markdown('https://blog.csdn.net/rank/list'), limit=limit)
    if platform == 'bilibili':
        return get_bilibili_popular(limit=limit)
    if platform == 'baidu':
        return parse_baidu_realtime(fetch_markdown('https://top.baidu.com/board?tab=realtime'), limit=limit)
    raise SystemExit(f'Unsupported platform: {platform}')


def print_items(platform: str, items: List[RankItem]) -> None:
    title = {
        'github': 'GitHub Trending',
        'csdn': 'CSDN 全站综合热榜',
        'bilibili': 'B站热门',
        'baidu': '百度热搜',
    }.get(platform, platform)
    print(f'# {title}\n')
    if not items:
        print('无结果')
        return
    for item in items:
        print(f"{item.rank}. {item.title}")
        print(f"   {item.url}")
        if item.meta:
            print(f"   {item.meta}")
        print()


def main() -> int:
    parser = argparse.ArgumentParser(description='Local hot-ranks skill for GitHub/CSDN/Bilibili/Baidu')
    parser.add_argument('platform', nargs='?', default='all', choices=['all', 'github', 'csdn', 'bilibili', 'baidu'])
    parser.add_argument('--limit', type=int, default=10)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    platforms = ['github', 'csdn', 'bilibili', 'baidu'] if args.platform == 'all' else [args.platform]
    result = {}
    for platform in platforms:
        items = get_platform(platform, limit=args.limit)
        result[platform] = [asdict(x) for x in items]

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    for idx, platform in enumerate(platforms):
        if idx:
            print('\n' + '=' * 60 + '\n')
        print_items(platform, [RankItem(**x) for x in result[platform]])
    return 0


if __name__ == '__main__':
    sys.exit(main())
