---
name: 🏠 日次不動産物件検索
description: 首都圏のRC一棟マンションを毎日自動検索し、投資条件に合致する物件をGitHub Issueで報告するワークフロー

on:
  schedule: daily
  workflow_dispatch:

timeout-minutes: 30

permissions:
  contents: read
  issues: read
  pull-requests: read

tools:
  web-fetch:
  cache-memory:
  github:
    toolsets: [default]

mcp-scripts:
  batch-fetch:
    description: "複数URLを並列fetchし結果をまとめて返す。一覧ページの一括取得に使用。"
    inputs:
      urls:
        type: string
        required: true
        description: "カンマ区切りのURL一覧"
      max_chars:
        type: number
        default: 5000
        description: "各URLから取得する最大文字数"
    timeout: 120
    script: |
      const urlList = urls.split(',').map(u => u.trim()).filter(u => u.length > 0);
      const limit = max_chars || 5000;
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
            return { url, status: res.status, chars: text.length, content: text.slice(0, limit), time_ms: Date.now() - t0 };
          } catch (e) {
            return { url, error: e.message, time_ms: Date.now() - t0 };
          }
        })
      );
      return { total_urls: urlList.length, total_time_ms: Date.now() - start, results };

network:
  allowed:
    - defaults
    - "*.nomu.com"
    - "*.livable.co.jp"
    - "footwork-i.jp"
    - "*.stepon.co.jp"
    # 以下はエージェントが個別物件詳細を取得する際に必要になる可能性があるため残す
    - "ittou-toushi.com"
    - "*.athome.co.jp"
    - "*.reins.or.jp"
    - "*.land.mlit.go.jp"
    - "*.mansion-review.jp"
    - "*.chikamap.jp"
    - "disaportal.gsi.go.jp"
    - "*.kantei.ne.jp"
    - "*.bit.courts.go.jp"
    - "981.jp"
    # 除外サイト:
    # *.rakumachi.jp — GHA IP が一律403ブロック（検証済み）
    # *.kenbiya.com — JS動的レンダリングでfetchからデータ取得不可
    # *.homes.co.jp / toushi.homes.co.jp — 同上
    # TODO: Self-Hosted Runner を導入すれば楽待・健美家も取得可能。
    #   案A: SHRジョブで取得→artifact経由で本体エージェントに渡す
    #   案B: エージェント全体をSHRで実行（AWF/Docker要件あり）
    #   実装案: Azure CLI でエフェメラルVM を都度起動する構成も可能
    #     Job1(GH-hosted): az vm create + ランナー登録(--ephemeral)
    #     Job2(self-hosted): 楽待・健美家取得→artifact保存
    #     Job3(GH-hosted): az vm delete
    #   注意: Azure VM もデータセンターIPのため同様に403の可能性あり。自宅マシンが最も確実。

safe-outputs:
  create-issue:
    max: 1
    labels: [daily-report, auto-generated]
    close-older-issues: true
    title-prefix: "🏠 "
---

# 日次不動産物件検索エージェント

あなたは不動産投資の物件検索を行うAIエージェントです。毎日、首都圏のRC一棟マンションを主要ポータルサイトで横断検索し、投資条件に合致する物件をGitHub Issueとしてレポートしてください。

## 検索条件

以下のフィルタ条件に**すべて**合致する物件を探してください:

| 条件 | 値 |
|------|-----|
| 構造 | **RC造**（鉄筋コンクリート）またはSRC造 |
| 築年数 | **3〜25年** |
| 価格帯 | **5,000万〜1.8億円** |
| 表面利回り | **5.5%以上** |
| 戸数 | **6戸以上** |
| 駅距離 | **徒歩10分以内** |
| エリア | 東京都・神奈川県・埼玉県・千葉県 |

## 検索対象サイト

以下のサイトを**すべて**検索してください。各サイトでRC一棟マンションの掲載物件を確認し、条件に合うものをリストアップします。

### SSR確認済み（確実にデータ取得可能）

1. **フットワーク（RC一覧）**: `https://footwork-i.jp/db/rc.html` ← **最も確実。最優先で検索**
2. **東急リバブル（東京RC一棟〜2億）**: `https://www.livable.co.jp/fudosan-toushi/tatemono-tokyo-select-area/a13000/conditions-use=mansion-itto&price-to=20000&construction=rc-framed-house/`
3. **東急リバブル（神奈川RC一棟〜2億）**: `https://www.livable.co.jp/fudosan-toushi/tatemono-kanagawa-select-area/a14000/conditions-use=mansion-itto&price-to=20000&construction=rc-framed-house/`
4. **ノムコム・プロ（検索結果）**: `https://www.nomu.com/pro/search/` — SSRで物件データ（価格・利回り・所在地・構造・築年月）が取得可能。URLパラメータでのフィルタは効かないため、取得した40件からエージェント側でRC一棟マンションを抽出すること。
5. **住友不動産ステップ（23区RC）**: `https://www.stepon.co.jp/pro/area_13/list_13_100/cs_32_04/` — ⚠️ **Shift-JIS**: batch-fetchが自動でエンコーディング変換するが、文字化けが残る場合は数値データ（価格・利回り・築年・面積）を優先的に抽出すること。

### 対象外

- **健美家** — JS動的レンダリングのため、fetchでは検索フィルタUIのみ返り物件データが取得不可。
- **HOMES投資** — JS動的レンダリングのため、fetchではサイト説明のみ返り物件データが取得不可。
- **楽待** — GHAデータセンターIPがボット対策で一律403ブロック（検証済み）。楽待の検索はローカル環境のCopilot CLIで別途実行するか、Self-Hosted Runner導入で対応予定。

## 検索手順

1. **前回の検索結果を確認**: `cache-memory` から前回レポートした物件URLリストを読み込む（ファイル名: `seen-properties.json`）。キャッシュファイルのタイムスタンプはハイフン区切り（例: `2026-04-01-08-00-00`）を使用し、コロンは使用しないこと。

2. **全サイト一覧ページを `batch-fetch` で一括並列取得**: 以下のURLをカンマ区切りで `batch-fetch` ツールに渡し、**1回のtool callで全サイトを同時取得**してください。`web-fetch` で1件ずつ取得しないこと。

   ```
   https://footwork-i.jp/db/rc.html,https://www.livable.co.jp/fudosan-toushi/tatemono-tokyo-select-area/a13000/conditions-use=mansion-itto&price-to=20000&construction=rc-framed-house/,https://www.livable.co.jp/fudosan-toushi/tatemono-kanagawa-select-area/a14000/conditions-use=mansion-itto&price-to=20000&construction=rc-framed-house/,https://www.nomu.com/pro/search/,https://www.stepon.co.jp/pro/area_13/list_13_100/cs_32_04/
   ```

3. **条件フィルタリング**: batch-fetchの結果から物件情報を抽出し、検索条件でフィルタリング。403/404のサイトはスキップ。**データが不明な場合は除外せず、条件合致の可能性ありとして残す**。

4. **新着判定**: 前回のseen-properties.jsonに含まれていないURLの物件を「新着」として特定する。

5. **物件詳細の取得（上位5件まで）**: 条件に合致しそうな物件のうち、**上位5件のみ** `web-fetch` で個別ページを取得して詳細確認する。全件fetchしない。

6. **cache-memoryを更新**: 今回確認した全物件のURLリストを `seen-properties.json` に保存する。

## Issue出力フォーマット

GitHub Issueを以下のフォーマットで作成してください:

**タイトル**: `[YYYY-MM-DD] 首都圏RC一棟 日次物件レポート (N件合致 / M件新着)`

**本文**:

```markdown
## 📊 検索サマリー

| 項目 | 値 |
|------|-----|
| 検索日 | YYYY年MM月DD日 |
| 検索サイト数 | X サイト |
| 確認物件数 | Y 件 |
| 条件合致 | **N 件** |
| うち新着 | **M 件** |

---

## 🔥 条件合致物件

### 物件1: [物件名/エリア名]

| 項目 | 内容 |
|------|------|
| 所在地 | ○○県○○市○○ |
| 最寄駅 | ○○駅 徒歩○分 |
| 価格 | ○,○○○万円 |
| 表面利回り | ○.○% |
| 築年数 | ○年 |
| 構造 | RC造 |
| 戸数 | ○戸 |
| 新着 | ✅ / — |

🔗 [物件詳細ページ](URL)

（物件2以降も同じフォーマットで繰り返し）

---

## 📋 条件に近い注目物件（1〜2条件未達）

条件を1〜2個満たさないが注目すべき物件があれば記載。

---

## ⚠️ 注意事項
- 物件情報は掲載時点のものです。最新情報は各サイトで確認してください。
- 表面利回りは想定賃料ベースの場合があります。現況利回りは物件詳細で確認してください。
```

## 重要な注意事項

- **楽待は対象外**: 楽待はGHAデータセンターIPを一律403ブロックしている（検証済み: curl/Python/Node.js全て403）。楽待の検索はローカルCopilot CLIで別途実行すること。
- **403/404エラーはスキップ**: 健美家など一部サイトもボット対策で403を返す場合がある。エラーが出たサイトはスキップし、アクセスできたサイトの結果だけでレポートを作成する。**エラーで止まらない**こと。
- **batch-fetch優先**: 一覧ページは必ず `batch-fetch` で一括並列取得すること。`web-fetch` は個別物件の詳細取得（上位5件）にのみ使用する。
- **時間管理**: 全体で15分以内に完了すること。一括取得で大半の時間を節約できる。
- **データ不明時は除外しない**: 築年数・価格・利回りなどが取得できない物件は、条件外とは断定せず「要確認」として残す
- **URLは必ず添付**: すべての物件情報にソースURLを添付する
- **重複チェック**: cache-memoryで前回のURLリストと照合し、新着/既知を判定する
- **条件合致0件でもレポート作成**: 合致物件がなくても検索サマリーと「条件に近い物件」をレポートする
