# Notes

## Current stable sources

- GitHub Trending: parse `https://r.jina.ai/http://github.com/trending`
- CSDN rank list: parse `https://r.jina.ai/http://blog.csdn.net/rank/list`
- Bilibili popular: use public API `https://api.bilibili.com/x/web-interface/popular`
- Baidu hot search: parse `https://r.jina.ai/http://top.baidu.com/board?tab=realtime`

## Currently unstable sources

- Zhihu: Jina returns 403-backed placeholder page
- Weibo: visitor wall / no meaningful ranking text
- Juejin: 451 blocked by Jina due to domain abuse protection

## Extension ideas

- Add fallback parsing for Bilibili ranking page if popular API rate-limits
- Add optional `gh search repos` fallback for GitHub recent-popular repos
- Add markdown export and timestamp metadata
