---
name: real-estate-site-directory
description: 日本の投資用不動産を探すためのサイト一覧を参照するスキル。物件探し・相場確認・競売情報・市場データなど、不動産投資に必要なWebサイトを網羅的にリストアップしている。
---

# 🏠 不動産投資 物件探しサイト一覧

> **目的**: 投資用不動産を効率的に探すためのサイトリファレンス
> **最終更新**: 2026年3月 ｜ **ステータス**: ドラフト v1.0

---

## 📋 サイト分類マップ

```
投資物件を探す
├── ① 投資専門ポータル（まずここから）
├── ② 総合不動産ポータル（実需向けだが掘り出し物あり）
├── ③ 競売・公売サイト（上級者向け・高利回り狙い）
├── ④ 市場データ・相場分析（価格妥当性の検証）
├── ⑤ 地域・ニッチ特化サイト
└── ⑥ 情報収集・コミュニティ
```

---

## ① 投資専門ポータル ⭐ 最重要

投資用物件に特化。利回り・CF計算が充実。**毎日チェック推奨**。

| サイト名 | URL | 特徴 | 対象エリア |
|----------|-----|------|-----------|
| **楽待（らくまち）** | https://www.rakumachi.jp/ | 国内最大の投資用不動産ポータル。会員限定の非公開物件あり。収益シミュレーション機能が充実。メルマガで新着通知 | 全国 |
| **健美家（けんびや）** | https://www.kenbiya.com/ | 楽待と双璧。コラム・ブログが充実し投資家コミュニティが活発。利回り検索が使いやすい | 全国 |
| **不動産投資連合隊** | https://www.rals.co.jp/ | 北海道発だが全国対応。高利回り物件が多く掲載。地方RC一棟物件に強い | 全国（北海道に強い） |
| **LIFULL HOME'S 不動産投資** | https://toushi.homes.co.jp/ | HOME'Sの投資版。データ分析ツール「見える！賃貸経営」で周辺相場・空室率を無料で確認可能 | 全国 |
| **ノムコム・プロ（野村不動産）** | https://www.nomu.com/pro/ | 野村不動産ソリューションズ運営。都心高額物件・一棟物件が充実。質の高い物件が多い | 首都圏中心 |
| **不動産投資★連合隊** | https://www.inv.co.jp/ | 一棟アパート・マンションに特化。地方高利回り物件が豊富 | 全国 |
| **東急リバブル 投資物件** | https://www.livable.co.jp/fudosan-toushi/ | 大手仲介の投資物件専門ページ。構造・築年・価格で詳細な絞り込みが可能。**RC一棟マンションの検索に特に強い**。物件写真・間取り・利回り情報が充実 | 首都圏中心 |
| **フットワーク** | https://footwork-i.jp/ | 東京・神奈川・千葉・埼玉の投資物件専門。**RC造の物件一覧ページ（https://footwork-i.jp/db/rc.html）**があり、RC特化検索に便利。538件以上のRC物件を掲載。会員登録で追加物件閲覧可 | 首都圏（東京・神奈川・千葉・埼玉） |
| **一棟投資.com** | https://ittou-toushi.com/ | 東京23区の一棟物件（アパート・マンション・ビル）に完全特化。会員登録（無料）で非公開物件も閲覧可能。運営はクラフコ | 東京23区 |
| **住友不動産ステップ 投資** | https://www.stepon.co.jp/pro/ | 住友不動産販売の投資物件。構造・価格帯で絞り込み可能。RC造の東京23区物件一覧あり | 首都圏中心 |
| **三菱UFJ不動産販売** | https://www.sumai1.com/buyers/investor/ | 銀行系仲介の投資物件。RC造・一棟マンション専用フィルタあり（`bukshu_2/?kozo[]=4`）。楽待・健美家未掲載の独自物件あり。東京26件・神奈川5件・埼玉5件・千葉3件（2026年4月時点） | 首都圏中心 |

### 🔍 投資専門ポータルの使い方Tips
- **楽待 + 健美家** を基本セットとして毎日チェック
- 会員登録して「新着メール通知」を必ず設定（良い物件は数時間で消える）
- 表面利回りだけでなく、実質利回り・CF・返済比率で絞り込む
- 同一物件が複数サイトに掲載 → 掲載期間が長い物件は値引き交渉の余地あり
- **RC一棟マンション専門検索**: 楽待・健美家だけでなく、**東急リバブル・フットワーク・三菱UFJ不動産販売**も必ずチェック。大手ポータルに掲載されていないRC一棟物件が見つかることがある
- **条件絞り込みの優先順位**: ① 構造（RC造）→ ② 価格帯 → ③ 利回り → ④ 築年数 → ⑤ エリア の順で絞り込むと効率的
- **楽待のJS動的ページ**: 楽待の検索結果ページはJavaScriptで動的レンダリングされるため、web_fetchでは物件一覧を取得できない。個別物件ページ（`/show.html`）は取得可能

### 📍 楽待 エリア別・フィルタ別URL

| 用途 | URL |
|------|-----|
| 地域別検索 | `https://www.rakumachi.jp/syuuekibukken/city` |
| 沿線別検索 | `https://www.rakumachi.jp/syuuekibukken/line` |
| 新着物件（24h以内） | `https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?newly=1` |
| 値下げ物件 | `https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?price_down=1` |
| 賃貸経営マップ | `https://www.rakumachi.jp/property/land_price/map` |
| 楽待新聞 | `https://www.rakumachi.jp/news/` |
| 北海道 | `https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?area=1` |
| 宮城県 | `https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?area=4` |
| 埼玉県 | `https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?area=11` |
| 千葉県 | `https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?area=12` |
| 東京都 | `https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?area=13` |
| 神奈川県 | `https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?area=14` |
| 愛知県 | `https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?area=23` |
| 京都府 | `https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?area=26` |
| 大阪府 | `https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?area=27` |
| 兵庫県 | `https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?area=28` |
| 広島県 | `https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?area=34` |
| 福岡県 | `https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?area=40` |

### 📍 健美家 エリア別・フィルタ別URL

| 用途 | URL |
|------|-----|
| 首都圏 | `https://www.kenbiya.com/pp0/s/` |
| 関西 | `https://www.kenbiya.com/pp0/k/` |
| 東海 | `https://www.kenbiya.com/pp0/t/` |
| 九州 | `https://www.kenbiya.com/pp0/f/` |
| 利回り15%↑ | `https://www.kenbiya.com/pp0/r1=15/` |
| 値下げ物件 | `https://www.kenbiya.com/pp0/prd=y/` |
| 新着24h | `https://www.kenbiya.com/pp0/cd2=1/` |
| 東京都 | `https://www.kenbiya.com/pp0/s/tokyo/` |
| 神奈川県 | `https://www.kenbiya.com/pp0/s/kanagawa/` |
| 埼玉県 | `https://www.kenbiya.com/pp0/s/saitama/` |
| 千葉県 | `https://www.kenbiya.com/pp0/s/chiba/` |
| 大阪府 | `https://www.kenbiya.com/pp0/k/osaka/` |
| 京都府 | `https://www.kenbiya.com/pp0/k/kyoto/` |
| 兵庫県 | `https://www.kenbiya.com/pp0/k/hyogo/` |
| 愛知県 | `https://www.kenbiya.com/pp0/t/aichi/` |
| 福岡県 | `https://www.kenbiya.com/pp0/f/fukuoka/` |
| 北海道 | `https://www.kenbiya.com/pp0/h/hokkaido/` |
| 広島県 | `https://www.kenbiya.com/pp0/o/hiroshima/` |
| 宮城県 | `https://www.kenbiya.com/pp0/m/miyagi/` |
| 健美家ニュース | `https://www.kenbiya.com/ar/ns/` |
| 健美家コラム | `https://www.kenbiya.com/ar/cl/` |

---

### 🏢 RC一棟マンション 特化検索URL

RC造一棟マンションを効率的に探すための直リンク集です。

| サイト | 条件 | URL |
|--------|------|-----|
| 楽待（東京・RC一棟） | 東京都・1棟マンション・RC造 | https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?dim%5B%5D=1001&kouzou%5B%5D=3&area=13 |
| 楽待（神奈川・RC一棟） | 神奈川県・1棟マンション・RC造 | https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?dim%5B%5D=1001&kouzou%5B%5D=3&area=14 |
| 楽待（埼玉・RC一棟） | 埼玉県・1棟マンション・RC造 | https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?dim%5B%5D=1001&kouzou%5B%5D=3&area=11 |
| 楽待（千葉・RC一棟） | 千葉県・1棟マンション・RC造 | https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?dim%5B%5D=1001&kouzou%5B%5D=3&area=12 |
| 東急リバブル（東京RC・2億以下） | 東京都全域・RC一棟・2億以下 | https://www.livable.co.jp/fudosan-toushi/tatemono-tokyo-select-area/a13000/conditions-use=mansion-itto&price-to=20000&construction=rc-framed-house/ |
| フットワーク（RC一覧） | RC造の収益物件全件 | https://footwork-i.jp/db/rc.html |
| 一棟投資.com（23区） | 東京23区の一棟物件 | https://ittou-toushi.com/search/m_ichiran_01.html |
| 住友不動産ステップ（23区RC） | 東京23区・RC造 | https://www.stepon.co.jp/pro/area_13/list_13_100/cs_32_04/ |

---

## ② 総合不動産ポータル

実需向けが中心だが、投資家目線で見ると**割安物件の発掘**に使える。

| サイト名 | URL | 特徴 | 投資家的使い方 |
|----------|-----|------|---------------|
| **SUUMO（スーモ）** | https://suumo.jp/ | リクルート運営。国内最大級の物件数。写真・間取り情報が充実 | 賃貸相場の確認、周辺環境リサーチ |
| **SUUMO**（中古マンション例） | https://suumo.jp/ms/chuko/tokyo/sc_shinjuku/ | 新宿区の中古マンション（エリア変更可） | エリア別の売買物件チェック |
| **HOME'S（ホームズ）** | https://www.homes.co.jp/ | LIFULL運営。「価格相場」機能で周辺取引価格を確認可能 | 売買相場 vs 賃料から利回り逆算 |
| **at home（アットホーム）** | https://www.athome.co.jp/ | 地場の中小不動産会社の掲載が多く、大手ポータルにない物件が見つかることも | 地場業者の独自物件を発掘 |
| **at home**（中古マンション） | https://www.athome.co.jp/mansion/chuko/ | 中古マンション売買 | 割安物件の発掘 |
| **Yahoo!不動産** | https://realestate.yahoo.co.jp/ | ヤフーの不動産。複数サイトの横断検索が可能 | 横断比較で相場感を掴む |
| **オウチーノ** | https://o-uccino.com/ | 中古マンション・リノベに強い | リノベ投資の物件探し |
| **マンションナビ** | https://t23m-navi.jp/ | マンション一括査定。AI価格推定あり | 保有物件の時価評価、売り時判断 |

### 🔍 総合ポータルの投資家的活用法
- SUUMOの賃貸で**想定賃料**を調査 → 売買価格と比較して利回り計算
- HOME'Sの「見える！賃貸経営」で空室率・賃料相場をエリア単位で把握
- at homeで**大手に載っていない地場物件**を探す（特に地方都市で有効）

---

## ③ 競売・公売サイト 🔥 上級者向け

市場価格より**30〜50%安**で取得できる可能性あり。ただし内覧不可・瑕疵担保なし等のリスクあり。

| サイト名 | URL | 特徴 |
|----------|-----|------|
| **BIT（不動産競売物件情報サイト）** | https://www.bit.courts.go.jp/ | 裁判所公式。全国の競売物件を検索可能。3点セット（物件明細書・評価書・現況調査報告書）を閲覧 |
| **981.jp** | https://981.jp/ | 競売物件の情報をわかりやすく整理。落札結果データベースが充実 |
| **KSI官公庁オークション** | https://kankocho.jp/ | 国税局・自治体の公売物件。滞納処分による差押物件が出品 |
| **Yahoo!官公庁オークション** | https://koubai.auctions.yahoo.co.jp/ | 自治体の公売物件をオンライン入札。不動産以外も出品 |

### ⚠️ 競売・公売の注意点
- **内覧不可**のケースが多い（3点セットで判断）
- 占有者の立退き交渉が必要な場合がある
- 入札保証金（売却基準価額の20%）が必要
- 初心者は競売専門の不動産会社にサポートを依頼すべき

---

## ④ 市場データ・相場分析 📊

物件の価格妥当性を検証するために**必ず参照**すべきデータソース。

| サイト名 | URL | 用途 |
|----------|-----|------|
| **REINS Market Information** | http://www.contract.reins.or.jp/ | 実際の成約価格データを公開。売出価格と成約価格の乖離を確認 |
| **土地総合情報システム（国交省）** | https://www.land.mlit.go.jp/webland/ | 国交省が公開する実取引価格データ。地価公示・都道府県地価調査も |
| **マンションレビュー** | https://www.mansion-review.jp/ | 中古マンションの適正価格をAI算出。坪単価の推移グラフが便利 |
| **東京カンテイ** | https://www.kantei.ne.jp/ | マンションデータの老舗。70㎡換算価格で市区町村別の相場把握 |
| **LIFULL HOME'S 見える！賃貸経営** | https://toushi.homes.co.jp/owner/ | 空室率・賃料相場・利回り相場をエリア別に無料で閲覧。投資判断に必須 |
| **TAS-MAP（タスマップ）** | https://www.tas-japan.com/ | 不動産鑑定のプロ向け。収益還元法のパラメータ確認に |
| **全国地価マップ** | https://www.chikamap.jp/ | 路線価・固定資産税評価額を地図上で確認。相続税評価の参考 |
| **ハザードマップポータル** | https://disaportal.gsi.go.jp/ | 国交省の災害リスク情報。洪水・土砂・津波リスクを確認 |
| **ハザードマップ（重ねる）** | https://disaportal.gsi.go.jp/maps/ | 地図上で複数の災害リスクを重ねて確認 |
| **土地総合情報（取引価格検索）** | https://www.land.mlit.go.jp/webland/servlet/MainServlet | 実取引価格を条件検索 |

### 🔍 データサイトの活用フロー
```
物件発見 → REINSで成約相場確認 → 土地総合情報で実取引価格照合
        → マンションレビューで適正価格AI算出
        → HOME'S見える賃貸経営で空室率・賃料確認
        → ハザードマップで災害リスクチェック
        → 全国地価マップで路線価確認（融資評価の目安）
```

---

## ⑤ 地域・ニッチ特化サイト

特定の投資戦略やエリアに強いサイト。

| サイト名 | URL | 特化領域 |
|----------|-----|---------|
| **タウンライフ不動産投資** | https://www.town-life.jp/shinchiku/invest/ | 非公開物件の一括資料請求。複数業者を比較 |
| **RENOSY（リノシー）** | https://www.renosy.com/ | AI活用の都心ワンルーム投資。管理代行まで一気通貫 |
| **Oh!Ya（オーヤ）** | https://oh-ya.jp/ | 投資用不動産の一括比較。セミナー情報も充実 |
| **Owners.com** | https://owners-style.com/ | 大家さん向けポータル。管理・経営ノウハウが豊富 |
| **HOME4U 土地活用** | https://land.home4u.jp/ | NTTデータ運営。土地活用プランの一括比較 |
| **CREAL** | https://creal.jp/ | 不動産クラウドファンディング。少額（1万円〜）から不動産投資可能 |
| **Rimawari（利回り不動産）** | https://rimawari.co.jp/ | 不動産クラウドファンディング。高利回り案件多め |

---

## ⑥ 情報収集・コミュニティ 📚

投資判断の質を上げるための情報源。

| サイト名 | URL | 内容 |
|----------|-----|------|
| **楽待コラム** | https://www.rakumachi.jp/news/column/ | プロ投資家・専門家のコラム。市場分析・戦略論が充実 |
| **健美家コラム** | https://www.kenbiya.com/ar/ | 実践的な大家業ノウハウ。確定申告・管理術・リフォーム情報 |
| **不動産投資の楽待チャンネル（YouTube）** | YouTube検索 | 動画で投資ノウハウを学習。物件分析ライブ配信も |
| **X（旧Twitter）不動産クラスタ** | X検索 | #不動産投資 で最新情報・投資家の生の声。相場の空気感を掴む |
| **BiggerPockets（海外参考）** | https://www.biggerpockets.com/ | 米国の不動産投資コミュニティ。分析フレームワークの参考に |

---

## 🎯 投資タイプ別 おすすめ巡回ルート

### タイプA：キャッシュフロー重視（利回り5%以上狙い）
```
毎日: 楽待 → 健美家 → 不動産投資連合隊
週次: HOME'S見える賃貸経営で空室率チェック
月次: REINS + 土地総合情報で相場更新確認
```

### タイプB：キャピタルゲイン狙い（再開発エリア）
```
毎日: 楽待 → SUUMO（売買）→ ノムコム・プロ
週次: マンションレビューで価格推移確認
月次: 東京カンテイ + 全国地価マップで地価動向
```

### タイプC：バランス型（CF + 値上がり両取り）
```
毎日: 楽待 → 健美家 → HOME'S投資
週次: HOME'S見える賃貸経営 + マンションレビュー
月次: REINS成約データ + ハザードマップ再確認
```

### タイプD：RC一棟マンション特化（当投資家の推奨ルート）
```
【候補1: 23区城東城北・横浜川崎】
毎日: 楽待（東京RC一棟）→ 東急リバブル → フットワーク
週次: 健美家 → 一棟投資.com → 住友不動産ステップ

【候補2: 千葉・埼玉 通勤圏】
毎日: 楽待（千葉RC一棟）→ 楽待（埼玉RC一棟）
週次: 健美家（千葉）→ 健美家（埼玉）→ フットワーク

【共通】
月次: REINS成約データ + 東京カンテイ坪単価推移
随時: ハザードマップで新着物件のリスク確認
```

**検索条件メモ（現在の投資家プロフィール）:**
- RC造・一棟マンション
- 価格: **5,000万〜1.8億円**
- 表面利回り: 5.5%以上
- 築年数: **3〜25年**
- エリア候補1: 23区城東城北（足立・葛飾・荒川・北・板橋）/ 横浜・川崎
- エリア候補2: 千葉（千葉市・船橋・市川・松戸・柏）/ 埼玉（さいたま・川口・所沢・川越・越谷・草加）
- 戸数: 6〜12戸
- 駅徒歩: 10分以内

---

## 🔄 更新履歴

| 日付 | 内容 |
|------|------|
| 2026-03-30 | ドラフト v1.0 作成 |
| 2026-03-31 | v1.1 — 東急リバブル・フットワーク・一棟投資.com・住友不動産ステップを追加。RC一棟特化検索URL集を新設。投資家プロフィール別巡回ルート（タイプD）を追加 |
| 2026-03-31 | v1.2 — 条件改定: 築3〜25年・価格5000万〜1.8億。候補2エリア（千葉・埼玉通勤圏）追加。巡回ルート候補1/候補2に分割 |

---

> ⚠️ **免責**: 本リストは情報提供目的であり、特定サイトの推奨ではありません。各サイトの利用規約に従い、自己責任でご利用ください。URLは変更される可能性があります。
