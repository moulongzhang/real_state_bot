---
name: real-estate-search
description: 不動産投資サイトで物件・市場データを検索するスキル。検索結果には必ずURLを添付する。楽待・健美家・SUUMO・HOMES等の主要ポータル、REINS・ハザードマップ等のデータサイトを横断的に検索し、物件情報や相場データを収集する。
---

# 🔍 不動産検索スキル

## 基本ルール

### ✅ 必須: 全ての検索結果にURLを添付すること

検索結果を提示する際は、**必ず該当ページのURLを添付**してください。URLが不明な場合は、最も近い検索結果ページのURLを添付してください。

```
✅ 正しい例:
品川区の区分マンション（楽待）
https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?area=13

❌ 間違った例:
品川区の区分マンションが楽待に掲載されています。（URLなし）
```

---

## 検索サイトURL一覧

### 物件検索サイト

| サイト名 | 検索ページURL | 用途 |
|----------|-------------|------|
| **楽待** | https://www.rakumachi.jp/syuuekibukken/city | 投資物件検索（地域別） |
| **楽待**（沿線） | https://www.rakumachi.jp/syuuekibukken/line | 投資物件検索（沿線別） |
| **楽待**（新着） | https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?newly=1 | 新着物件（24時間以内） |
| **楽待**（値下げ） | https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?price_down=1 | 値下げ物件 |
| **健美家**（首都圏） | https://www.kenbiya.com/pp0/s/ | 首都圏の収益物件 |
| **健美家**（関西） | https://www.kenbiya.com/pp0/k/ | 関西の収益物件 |
| **健美家**（九州） | https://www.kenbiya.com/pp0/f/ | 九州・沖縄の収益物件 |
| **健美家**（東海） | https://www.kenbiya.com/pp0/t/ | 東海の収益物件 |
| **健美家**（利回り15%↑） | https://www.kenbiya.com/pp0/r1=15/ | 高利回り物件 |
| **健美家**（値下げ） | https://www.kenbiya.com/pp0/prd=y/ | 値下げ物件 |
| **健美家**（新着24h） | https://www.kenbiya.com/pp0/cd2=1/ | 新着物件（24時間以内） |
| **SUUMO**（売買） | https://suumo.jp/ms/chuko/tokyo/sc_shinjuku/ | 中古マンション（エリア変更可） |
| **HOMES 投資** | https://toushi.homes.co.jp/ | 投資用物件検索 |
| **at home** | https://www.athome.co.jp/mansion/chuko/ | 中古マンション |
| **ノムコム・プロ** | https://www.nomu.com/pro/ | 高額投資物件 |

### RC一棟マンション特化 検索URL

| サイト名 | URL | 条件 |
|----------|-----|------|
| **楽待**（東京・RC・一棟） | https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?dim%5B%5D=1001&kouzou%5B%5D=3&area=13 | 東京都・1棟マンション・RC造 |
| **楽待**（神奈川・RC・一棟） | https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?dim%5B%5D=1001&kouzou%5B%5D=3&area=14 | 神奈川県・1棟マンション・RC造 |
| **楽待**（埼玉・RC・一棟） | https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?dim%5B%5D=1001&kouzou%5B%5D=3&area=11 | 埼玉県・1棟マンション・RC造 |
| **楽待**（千葉・RC・一棟） | https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?dim%5B%5D=1001&kouzou%5B%5D=3&area=12 | 千葉県・1棟マンション・RC造 |
| **東急リバブル**（東京・RC・2億以下） | https://www.livable.co.jp/fudosan-toushi/tatemono-tokyo-select-area/a13000/conditions-use=mansion-itto&price-to=20000&construction=rc-framed-house/ | 東京都全域・RC・1.8億以下 |
| **フットワーク**（RC一覧） | https://footwork-i.jp/db/rc.html | RC造の収益物件一覧（東京・神奈川・千葉・埼玉） |
| **一棟投資.com**（23区） | https://ittou-toushi.com/search/m_ichiran_01.html | 東京23区の一棟物件（会員登録で非公開物件閲覧可） |
| **住友不動産ステップ**（23区・RC） | https://www.stepon.co.jp/pro/area_13/list_13_100/cs_32_04/ | 東京23区・RC造の収益物件 |
| **健美家**（千葉・一棟マンション） | https://www.kenbiya.com/pp0/s/chiba/mansion/ | 千葉県・一棟マンション |
| **健美家**（埼玉・一棟マンション） | https://www.kenbiya.com/pp0/s/saitama/mansion/ | 埼玉県・一棟マンション |

### エリア別検索URL（楽待）

| エリア | URL |
|--------|-----|
| 北海道 | https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?area=1 |
| 宮城県 | https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?area=4 |
| 埼玉県 | https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?area=11 |
| 千葉県 | https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?area=12 |
| 東京都 | https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?area=13 |
| 神奈川県 | https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?area=14 |
| 愛知県 | https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?area=23 |
| 京都府 | https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?area=26 |
| 大阪府 | https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?area=27 |
| 兵庫県 | https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?area=28 |
| 広島県 | https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?area=34 |
| 福岡県 | https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?area=40 |

### エリア別検索URL（健美家）

| エリア | URL |
|--------|-----|
| 東京都 | https://www.kenbiya.com/pp0/s/tokyo/ |
| 神奈川県 | https://www.kenbiya.com/pp0/s/kanagawa/ |
| 埼玉県 | https://www.kenbiya.com/pp0/s/saitama/ |
| 千葉県 | https://www.kenbiya.com/pp0/s/chiba/ |
| 大阪府 | https://www.kenbiya.com/pp0/k/osaka/ |
| 京都府 | https://www.kenbiya.com/pp0/k/kyoto/ |
| 兵庫県 | https://www.kenbiya.com/pp0/k/hyogo/ |
| 愛知県 | https://www.kenbiya.com/pp0/t/aichi/ |
| 福岡県 | https://www.kenbiya.com/pp0/f/fukuoka/ |
| 北海道 | https://www.kenbiya.com/pp0/h/hokkaido/ |
| 広島県 | https://www.kenbiya.com/pp0/o/hiroshima/ |
| 宮城県 | https://www.kenbiya.com/pp0/m/miyagi/ |

### 市場データ・相場検索サイト

| サイト名 | URL | 用途 |
|----------|-----|------|
| **REINS** | http://www.contract.reins.or.jp/ | 成約価格データ |
| **土地総合情報システム** | https://www.land.mlit.go.jp/webland/ | 実取引価格・地価公示 |
| **土地総合情報（取引価格検索）** | https://www.land.mlit.go.jp/webland/servlet/MainServlet | 取引価格情報検索 |
| **マンションレビュー** | https://www.mansion-review.jp/ | AI適正価格・坪単価推移 |
| **東京カンテイ** | https://www.kantei.ne.jp/ | 市区町村別相場 |
| **HOMES 見える賃貸経営** | https://toushi.homes.co.jp/owner/ | 空室率・賃料相場 |
| **全国地価マップ** | https://www.chikamap.jp/ | 路線価・固定資産税評価額 |
| **ハザードマップポータル** | https://disaportal.gsi.go.jp/ | 災害リスク情報 |
| **ハザードマップ（重ねる）** | https://disaportal.gsi.go.jp/maps/ | 地図上でリスク確認 |
| **楽待 賃貸経営マップ** | https://www.rakumachi.jp/property/land_price/map | 路線価・空室率・利回り地図 |

### 競売・公売検索サイト

| サイト名 | URL | 用途 |
|----------|-----|------|
| **BIT** | https://www.bit.courts.go.jp/ | 裁判所競売物件 |
| **981.jp** | https://981.jp/ | 競売物件・落札結果 |
| **KSI官公庁オークション** | https://kankocho.jp/ | 公売物件 |

### ニュース・コラム検索

| サイト名 | URL | 用途 |
|----------|-----|------|
| **楽待新聞** | https://www.rakumachi.jp/news/ | 不動産投資ニュース |
| **健美家ニュース** | https://www.kenbiya.com/ar/ns/ | 市場動向・地域情報 |
| **健美家コラム** | https://www.kenbiya.com/ar/cl/ | 投資家コラム |

---

## 投資家プロフィール別 推奨検索条件

物件検索の前に、投資家の属性に応じた推奨条件を確認してください。

### 現在の投資家プロフィール

| 項目 | 値 |
|------|-----|
| 年齢 | 27歳 |
| 年収 | 1,600万円 |
| 保有資産 | 3,000万円 |
| 借入金 | 0円 |
| 投資経験 | 一件目 |
| 融資枠目安 | 1.6〜2.0億円 |

### 推奨検索条件（一件目）

| 条件 | 推奨値 | 理由 |
|------|--------|------|
| 構造 | **RC造**（鉄筋コンクリート） | 耐用年数47年で融資期間を長く取れる |
| 築年数 | **3〜25年** | 新築プレミアム回避〜融資期間確保のバランス |
| 価格帯 | **5,000万〜1.8億円** | 下限: 一棟RCの最低ライン / 上限: 予備資金確保 |
| 利回り（表面） | **5.5%以上** | 金利2%+経費控除後に実質CF黒字を確保 |
| エリア（候補1） | **23区城東城北（足立・葛飾・荒川・北・板橋）or 横浜・川崎** | 賃貸需要安定、利回りと資産性のバランス |
| エリア（候補2） | **首都圏通勤圏（千葉・埼玉）** — 下記エリア表を参照 | 都心より利回り高め、通勤需要あり |
| 戸数 | **6〜12戸** | 空室リスク分散と管理負担のバランス |
| 駅距離 | **徒歩10分以内** | 賃貸需要と出口戦略の両面で有利 |

> ⚠️ **重要**: 上記の推奨条件は自動検索スクリプト（`scripts/config.yaml`）と同期する必要があります。条件を変更する場合は、スキルとconfig.yamlの両方を更新してください。

### エリア候補 詳細

#### 候補1: 23区城東城北・横浜川崎（利回り×資産性バランス型）

| エリア | 特徴 | 目安利回り | 賃貸需要 |
|--------|------|-----------|---------|
| 足立区 | 価格控えめ、日暮里舎人ライナー・TX沿線で再開発進行 | 5〜7% | ◎ 単身需要強い |
| 葛飾区 | 下町エリア、家賃手頃で入居付けしやすい | 5〜7% | ○ |
| 荒川区 | 日暮里・町屋など交通利便性高い | 5〜6% | ◎ |
| 北区 | 赤羽・王子は人気上昇中、再開発エリア | 4.5〜6% | ◎ |
| 板橋区 | 池袋至近で家賃対比の利便性高い | 5〜6% | ◎ |
| 横浜市（神奈川区・鶴見区・南区） | 都心通勤可、利回りやや高め | 5〜7% | ◎ |
| 川崎市（川崎区・幸区・中原区） | 東京隣接、人口流入続く | 5〜6.5% | ◎ |

#### 候補2: 首都圏通勤圏・千葉埼玉（利回り重視型）

| エリア | 主要駅・路線 | 都心通勤時間 | 特徴 | 目安利回り |
|--------|-------------|-------------|------|-----------|
| 千葉市中央区・稲毛区 | JR総武線・京成線（千葉・稲毛） | 40〜50分 | 千葉大学・官公庁集積、単身需要安定 | 6〜8% |
| 船橋市 | JR総武線・東武野田線（船橋） | 25〜35分 | 人口60万超、商業施設充実、賃貸需要◎ | 5.5〜7% |
| 市川市 | JR総武線・都営新宿線（本八幡） | 20〜30分 | 東京隣接、都心アクセス抜群 | 5〜6.5% |
| 松戸市・柏市 | JR常磐線・TX（松戸・柏） | 25〜40分 | 大学多数・若年層需要、TX沿線は再開発進行 | 6〜8% |
| さいたま市（浦和・大宮） | JR京浜東北・宇都宮線 | 25〜35分 | 県庁所在地、教育水準高く家族需要も | 5.5〜7% |
| 川口市・蕨市 | JR京浜東北線 | 15〜25分 | 東京隣接、外国人需要も旺盛 | 5.5〜7% |
| 所沢市・川越市 | 西武線・東武東上線 | 30〜45分 | ベッドタウン、安定した賃貸需要 | 6〜8% |
| 越谷市・草加市 | 東武伊勢崎線・TX | 30〜40分 | レイクタウン等大型商業施設、ファミリー需要 | 6〜8% |

### ⚠️ 要注意条件（前回調査の教訓）

- **表面利回り4.5%以下** → 頭金10%・金利2%ではCFが確実にマイナス。5.5%以上を目標に
- **3戸以下の一棟物件** → 空室1戸で収入30%以上減。6戸以上を推奨
- **築年不明の物件** → 購入検討前に登記簿で築年確認必須
- **土地面積50㎡以下** → 積算評価が低く、融資・売却で不利
- **予算上限ギリギリの物件** → 諸費用（物件価格の7-8%）+予備資金300万を確保できるか確認

---

## 検索フロー

### A. 物件検索フロー

```
1. 投資条件を確認
   - エリア / 物件タイプ / 価格帯 / 目標利回り

2. 楽待で検索（URL添付必須）
   → https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?area={エリアコード}

3. 健美家で検索（URL添付必須）
   → https://www.kenbiya.com/pp0/{地域}/{都道府県}/

4. 結果を整理して提示
   - 各物件にソースURLを必ず添付
   - 利回り・価格・築年数・駅距離を表形式で整理
```

### B. 相場調査フロー

```
1. REINSで成約価格を確認（URL添付必須）
   → http://www.contract.reins.or.jp/

2. 土地総合情報で実取引価格を照合（URL添付必須）
   → https://www.land.mlit.go.jp/webland/

3. マンションレビューで適正価格を確認（URL添付必須）
   → https://www.mansion-review.jp/

4. HOMES見える賃貸経営で空室率を確認（URL添付必須）
   → https://toushi.homes.co.jp/owner/
```

### C. リスク調査フロー

```
1. ハザードマップで災害リスク確認（URL添付必須）
   → https://disaportal.gsi.go.jp/maps/

2. 全国地価マップで路線価確認（URL添付必須）
   → https://www.chikamap.jp/

3. 楽待賃貸経営マップで周辺データ確認（URL添付必須）
   → https://www.rakumachi.jp/property/land_price/map
```

### D. 条件合致物件スクリーニングフロー（推奨）

投資家プロフィールに基づく条件で効率的に物件を絞り込むフローです。

```
1. 【楽待】curlで物件URL一括抽出（4エリア合計5,126件、50件/ページ）
   bash: curl → grep 'href="/syuuekibukken/.*show.*"' → sort -u
   → 東京(area=13, 57p) / 神奈川(area=14, 21p) / 千葉(area=12, 13p) / 埼玉(area=11, 13p)
   → RC一棟: dim[]=1001&kouzou[]=3  (+SRC: &kouzou[]=1)
   → ページ送り: &page=2, &page=3 ...（重複なし確認済み）

2. 【健美家】pp3専用ページからcurlで一棟MSリンク抽出（4エリア合計5,025件、50件/ページ）
   bash: curl /pp3/s/{都道府県}/ → grep 'href="/pp3/s/.*re_.*"'
   → 東京(/pp3/s/tokyo/, 55p) / 神奈川(21p) / 埼玉(14p) / 千葉(12p)
   → ページ送り: /n-2/, /n-3/ ...
   ⚠️ 旧URL pp0/s/tokyo/ は全種別混在でpp3が8件のみ → 必ずpp3/s/tokyo/を使うこと

3. 【フットワーク】RC一覧（全116件 = rc.html + rc2.html + rc3.html）
   web_fetch: https://footwork-i.jp/db/rc.html（52件）
   web_fetch: https://footwork-i.jp/db/rc2.html（40件）
   web_fetch: https://footwork-i.jp/db/rc3.html（24件）

4. 【東急リバブル】RC一棟・2億以下（16件、1ページ完結）
   web_fetch: https://www.livable.co.jp/fudosan-toushi/tatemono-tokyo-select-area/a13000/conditions-use=mansion-itto&price-to=20000&construction=rc-framed-house/

5. Step 1-2で取得した物件URLから10〜20件をweb_fetchで個別取得し一次スクリーニング
   ✅ RC造
   ✅ 価格 5,000万〜1.8億円
   ✅ 表面利回り 5.5%以上
   ✅ 築3〜25年（2001年〜2023年築）
   ✅ 戸数 6戸以上
   ✅ 駅徒歩 10分以内

6. 二次スクリーニング（物件詳細確認）
   ✅ 築年月が明記されている
   ✅ 満室稼働中 or 高稼働率
   ✅ 所有権（借地権でない）
   ✅ 新耐震基準（1981年6月以降の建築確認）

7. 三次スクリーニング（投資分析）
   → CFシミュレーション（頭金10%、金利2%、35年）
   → 1年目CFがプラスになるか確認
   → 純資産プラス転換が15年以内か確認
   → ハザードマップで災害リスク確認
```

### 🚨 前回調査の教訓（2026年3月31日〜4月1日）

1. **表面利回り4.5%以下のRC一棟は頭金10%ではCFマイナス**になる（金利2%想定）。5.5%以上を目標に
2. **RC一棟・築25年以内・2億以下は市場で最も競争が激しい条件帯**。流通数は極めて少なく、条件緩和の検討も必要
3. **東急リバブル・フットワーク**は楽待・健美家に掲載されていない物件が見つかることがある。複数ポータル横断検索が重要
4. **3戸以下の一棟物件**は空室リスクが集中し、投資初心者には不向き
5. **築年不明の物件**は登記簿確認が最優先。購入検討前に必ず確認すること
6. **config.yamlとスキルの条件不一致が物件見落としの原因に（2026年4月1日）**: 八王子市明神町のRC一棟マンション（築19年・1.4億・利回り5.82%）が3/31の自動スキャンで見落とされた。原因は `config.yaml` の `max_building_age_years: 15` がスキルの推奨条件（築3〜25年）と不一致だったため。**config.yamlとスキルの検索条件は常に同期させること**
7. **`newly_listed: true`は物件見落としリスクあり**: 新着24時間以内のみの検索では、掲載済みの物件を見逃す。`newly_listed: false`に変更し、全掲載物件を対象とするべき
8. **自動スクリプト（daily_search.py）の検索条件はconfig.yamlで管理**: スキルの推奨条件を変更した場合は、必ず `scripts/config.yaml` も同時に更新すること

---

## 🔧 JS動的サイトの攻略方法（楽待・健美家）

### ⚠️ 重要: `web_fetch`ではなく`curl`→リンク抽出→`web_fetch`の2段階方式を使うこと

楽待・健美家の**検索一覧ページ**は物件リストをJavaScriptで動的レンダリングしている。`web_fetch`（Markdown変換）では物件データが消失するが、**HTMLソースには物件URLが埋め込まれている**。`curl`（bashツール）で生HTMLを取得し、物件URLを抽出した後、個別ページを`web_fetch`で取得する。

### 楽待（rakumachi.jp）の網羅的検索手順

**Step 1: curlで検索ページのHTMLから物件URLを一括抽出**

```bash
# 東京RC一棟（1ページ50件、ページネーション &page=N）
curl -s -L -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  "https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?dim%5B%5D=1001&kouzou%5B%5D=3&area=13&page=1" | \
  grep -o 'href="/syuuekibukken/[^"]*show[^"]*"' | sort -u

# 神奈川: area=14 / 埼玉: area=11 / 千葉: area=12
# SRC造も含める場合: &kouzou%5B%5D=1 を追加
```

- 1ページ50件、ページ間の重複なし（確認済み）
- 最終ページ超過（例: 東京はpage=58以降）で全件ダンプされるので注意
- **各エリアの掲載件数・ページ数（2026年4月1日時点）:**

| エリア | area= | 全掲載件数 | ページ数 | 最終ページ件数 |
|--------|-------|----------|---------|-------------|
| 東京都 | 13 | **2,830件** | 57 | 30件 |
| 神奈川県 | 14 | **1,015件** | 21 | 15件 |
| 埼玉県 | 11 | **642件** | 13 | 42件 |
| 千葉県 | 12 | **639件** | 13 | 39件 |
| **4エリア合計** | | **5,126件** | | |

**Step 2: 個別物件ページをweb_fetchで取得**

```
web_fetch: https://www.rakumachi.jp/syuuekibukken/kanto/tokyo/dim1001/{物件ID}/show.html
```

- 個別ページには価格・利回り・築年月・構造・戸数・間取り・所在地・駅距離が全て含まれる
- 「条件が近い物件」「この不動産会社の他の物件」セクションから追加候補も発見可能

**Step 3: 効率的なスクリーニング（全件web_fetchは非効率なので）**

1. Step 1で全URL（例: 東京50件 + 神奈川50件 = 100件）を取得
2. 10〜15件をランダムまたは最新順にweb_fetchし、条件適合をチェック
3. 「条件が近い物件」リンクから芋づる式に候補を広げる
4. 全件の価格・利回り一覧が必要な場合はHTMLソースからも抽出可能（prop_blockデータ）

### 健美家（kenbiya.com）の網羅的検索手順

**Step 1: curlで `pp3/s/{都道府県}/` ページから一棟マンションリンクを抽出**

> ⚠️ 重要: 以前使っていた `pp0/s/tokyo/` は全種別混在で一棟MSが8件しか含まれない。**必ず `pp3/s/tokyo/` を使うこと**（一棟マンション専用、全件網羅）。

```bash
# 東京の一棟マンション（50件/ページ）
curl -s -L -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  "https://www.kenbiya.com/pp3/s/tokyo/" | \
  grep -o 'href="/pp3/s/tokyo/[^"]*re_[^"]*"' | sort -u

# ページ2以降: /pp3/s/tokyo/n-2/, /pp3/s/tokyo/n-3/ ...
curl -s -L -A "..." "https://www.kenbiya.com/pp3/s/tokyo/n-2/" | grep -o 'href="/pp3/s/tokyo/[^"]*re_[^"]*"'
```

- `pp3` = 一棟マンション（`pp1`=区分, `pp2`=一棟アパート, `pp5`=一棟ビル）
- ページネーション: `/n-2/`, `/n-3/` ... `/n-{最終ページ}/`
- 一部物件は会員限定（リンク先が会社情報ページに転送）
- **各エリアの掲載件数（2026年4月1日時点）:**

| エリア | 検索URL | 全掲載件数 | ページ数（50件/ページ） |
|--------|---------|----------|----------------------|
| 東京都 | `/pp3/s/tokyo/` | **2,736件** | 55 |
| 神奈川県 | `/pp3/s/kanagawa/` | **1,037件** | 21 |
| 埼玉県 | `/pp3/s/saitama/` | **684件** | 14 |
| 千葉県 | `/pp3/s/chiba/` | **568件** | 12 |
| **4エリア合計** | | **5,025件** | |

**Step 2: 個別物件ページをweb_fetchで取得**

```
web_fetch: https://www.kenbiya.com/pp3/s/{都道府県}/{市区町村}/re_{物件ID}/
```

- 物件詳細（価格・利回り・築年月・構造・戸数・間取り・所在地・接道・用途地域）が取得可能
- 一部は `pp1` URLだが物件詳細が表示される場合もある

**Step 3: prop_blockからの簡易データ抽出（オプション）**

```bash
# HTMLソースからprop_block内の概要データ（エリア・価格・利回り・種別）を抽出
curl -s -L -A "..." "https://www.kenbiya.com/pp0/s/tokyo/" | \
  python3 -c "
import sys, re
html = sys.stdin.read()
blocks = html.split('prop_block')
for i, block in enumerate(blocks[1:], 1):
    text = re.sub(r'<[^>]+>', '|', block[:500])
    text = re.sub(r'\|+', '|', text).strip()
    print(f'Block {i}: {text[:200]}')
"
```

### GHA環境（日次ワークフロー）での注意

- **楽待はGHAデータセンターIPから403ブロック**される（2026年4月確認済み）。GHA環境ではフットワーク・リバブル・ノムコム・ステップの4サイトを使用し、楽待はローカルCLI実行時のみ対象とする。
- 健美家は上記curl手順で取得可能（GHA環境でも動作するがAWF設定でドメイン許可が必要）

---

## 出力フォーマット

検索結果を提示する際は、以下のフォーマットを使用してください：

### 物件情報の場合

```markdown
### 🏠 [物件名/エリア名]

| 項目 | 内容 |
|------|------|
| 所在地 | ○○県○○市○○ |
| 最寄駅 | ○○駅 徒歩○分 |
| 価格 | ○,○○○万円 |
| 利回り | 表面○.○% / 実質○.○% |
| 築年数 | ○年（○○年築） |
| 構造 | RC造 |

🔗 **ソースURL**: https://example.com/property/12345
```

### 市場データの場合

```markdown
### 📊 [エリア名] 市場データ

| 指標 | 数値 | 出典 |
|------|------|------|
| 平均坪単価 | ○○万円/坪 | [マンションレビュー](URL) |
| 空室率 | ○.○% | [HOMES見える賃貸経営](URL) |
| 成約価格中央値 | ○,○○○万円 | [REINS](URL) |
| 路線価 | ○○万円/㎡ | [全国地価マップ](URL) |
| 地価変動率 | +○.○% | [土地総合情報](URL) |
```

---

## ⚠️ 注意事項

1. **URL必須**: 全ての検索結果・データ引用には必ずURLを添付する。URLがない情報は提示しない
2. **日付記載**: データの取得日を明記する（「2026年3月30日時点」など）
3. **複数ソース**: 可能な限り2つ以上のサイトから情報を取得し、クロスチェックする
4. **JS動的サイト対策**: 楽待・健美家の検索一覧は`web_fetch`ではなく`curl`（bashツール）でHTML取得→物件URL抽出→`web_fetch`で個別ページ取得の2段階方式を使う。上記「JS動的サイトの攻略方法」セクションを参照
5. **鮮度**: 物件情報は掲載から数時間〜数日で売れることがある。「○月○日時点の情報」と明記する

---

## 更新履歴

| 日付 | 内容 |
|------|------|
| 2026-04-01 | v1.4 — 楽待・健美家のJS動的サイト攻略方法を追加。curl→リンク抽出→web_fetch個別取得の2段階方式。楽待は4エリア合計5,126件（50件/ページ、ページネーション確認済み、重複なし）、健美家はpp3専用URL(pp0ではなくpp3/s/tokyo/)で4エリア合計5,025件。フットワークはrc.html+rc2.html+rc3.htmlの3ページで全116件。スクリーニングフローを全面改訂 |
| 2026-04-01 | v1.3 — 教訓追加: config.yamlとスキルの条件不一致により八王子市明神町物件を見落とし。newly_listed設定のリスクを文書化。config.yaml同期の重要性を明記 |
