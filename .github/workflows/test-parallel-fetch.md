---
name: 🧪 並列fetch検証
description: batch-fetch MCP Scriptの並列実行を検証するテストワークフロー

on:
  workflow_dispatch:

permissions:
  contents: read

tools:
  bash: true

mcp-scripts:
  batch-fetch:
    description: "複数URLを並列fetchし結果を返す。urlsにカンマ区切りのURL一覧を渡す。"
    inputs:
      urls:
        type: string
        required: true
        description: "カンマ区切りのURL一覧"
      max_chars:
        type: number
        default: 3000
        description: "各URLから取得する最大文字数"
    timeout: 120
    script: |
      const urlList = urls.split(',').map(u => u.trim()).filter(u => u.length > 0);
      const limit = max_chars || 3000;
      const start = Date.now();
      const results = await Promise.all(
        urlList.map(async (url) => {
          const t0 = Date.now();
          try {
            const res = await fetch(url, {
              headers: { 'User-Agent': 'Mozilla/5.0 (compatible; PropertyBot/1.0)' },
              signal: AbortSignal.timeout(15000)
            });
            const text = await res.text();
            return {
              url,
              status: res.status,
              chars: text.length,
              preview: text.slice(0, limit),
              time_ms: Date.now() - t0
            };
          } catch (e) {
            return { url, error: e.message, time_ms: Date.now() - t0 };
          }
        })
      );
      return {
        total_urls: urlList.length,
        total_time_ms: Date.now() - start,
        results
      };

network:
  allowed:
    - defaults
    - "*.kenbiya.com"
    - "footwork-i.jp"
    - "*.homes.co.jp"
    - "toushi.homes.co.jp"
    - "*.stepon.co.jp"
    - "*.rakumachi.jp"
---

# 並列fetch検証テスト

あなたはbatch-fetchツールの性能を検証するテストエージェントです。

## 手順

1. `batch-fetch` ツールを使って、以下の5つのURLを**一括で並列取得**してください:

```
https://www.kenbiya.com/pp0/s/tokyo/,https://www.kenbiya.com/pp0/s/kanagawa/,https://footwork-i.jp/db/rc.html,https://toushi.homes.co.jp/,https://www.stepon.co.jp/pro/area_13/list_13_100/cs_32_04/
```

2. 結果を以下のフォーマットで表示してください:

```
## 検証結果

| URL | ステータス | 取得文字数 | 所要時間 |
|-----|-----------|-----------|---------|
| ... | ... | ... | ...ms |

**合計所要時間**: Xms（Y件並列）
```

3. これで完了です。他のことはしないでください。
