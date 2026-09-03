<!-- Copyright (c) 2026 4dcitygml -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# 公開後のPull Request運用手順

- 状態: 公開後運用の採用手順（専用CI未実装のPR種別は解禁条件付き）
- 対象: 公開された都市データリポジトリ

English (canonical): [docs/pr-operations.md](../pr-operations.md)

この文書を、**公開後にPRをどう進めるか**の正本とする。他の文書は設計理由や
個別ツールの使い方を説明し、日々の着手、審査、マージ、releaseの順序は本手順に揃える。

## 1. 最初に固定する原則

1. **1 commit = 1 `uro:buildingID`** を通常更新の最小単位とする。
2. 同じ根拠、原典、変更規則で審査できる複数の建物commitは、1つのPRへ束ねてよい。
3. 同じbuildingIDを1つのPR内の複数commitに分けない。別のPRや年次属性系統で再度現れることは許容する。
4. 建物の統合・分割・建替えは、複数IDを扱う1つの `lifecycle` イベントとする。
5. 都市データPRは**squashせずmerge commit**で取り込み、個々の建物commitをmainへ残す。
6. コード・文書だけのPRは都市データと混ぜず、squash mergeしてよい。
7. PRの**承認**、mainへの**マージ**、安定版の**release**は別の完了条件とする。
8. 一棟または一commitでもblocking検査に失敗したPRは、合格分だけを部分マージしない。
9. mainは作業中の途中状態を許容する。通常利用者には最新の安定releaseを案内する。

PRテキストの言語: 編集ツールが生成するPRタイトル・本文は**リポの作業言語**
（`4dcitygml.json` の `lang`）に従う。commitの題・`Building:`トレーラ・
branch prefixは英語/固定リテラルのまま（履歴と機械契約は言語非依存）。
都市データPRはmerge commitで取り込む（規則5）ため、PRタイトルがmainの履歴の
題行になることはない。（練習リポは例外: auto-mergeがsquashするため、リポ言語の
PRタイトルが練習履歴に入るが、練習履歴は定期的にリセットされる。）

```text
Issue・公的原典
  → Draft PR
  → 自動検査
  → Ready for review
  → 都市の意味審査
  → メンテナーがmerge commitで確定
  → Pages・履歴索引に反映
  → release gate合格後に安定版化
```

## 2. 役割と完了責任

| 役割 | 主な作業 | 完了の印 |
|---|---|---|
| 提案者 | 変更、根拠、commit、PR本文を用意 | PRをReady for reviewにする |
| CI | commit範囲、XML、参照、形式、幾何、manifestの機械検査 | required checksが全て成功 |
| 都市の承認役 | 値、形状、出典、lifecycle理由等の意味判断 | Approve、またはRequest changes |
| メンテナー | 必須検査、承認、マージ方式、最新mainを最終確認 | merge commitがmainへ入る |
| release担当 | 公式原典一致、全検査、release notes、tag | 安定版tagと検査結果を公開 |

同一人が複数の役割を担ってもよいが、工程と記録は分ける。都市ごとのCODEOWNERSと最終承認権限を
他都市と共有しない。

## 3. すべてのPRに共通する手順

### 3.1 着手前

```text
[ ] Issue、公的原典、定期保守のどれを起点にするか決めた
[ ] 対象都市、uro:buildingID、メッシュ、変更種別を特定した
[ ] 根拠資料を公開でき、ライセンス・個人情報・肖像等に問題がない
[ ] 同じメッシュGMLを変更する先行PRがない
[ ] このPRと別PRに分ける意味の境界が決まっている
```

同じメッシュGMLを変更するPRは直列にする。先行PRがマージされた後のmainから次のPRを作り直す。
異なるメッシュは、共通schema migrationが完了し、共有テクスチャやXLinkへの変更がない場合だけ並行できる。

### 3.2 ブランチとcommit

```text
[ ] 着手時点の最新mainから作業ブランチを作った
[ ] PRの履歴は直線で、PRブランチ内にmerge commitを入れていない
[ ] 通常更新は1 commitで1 buildingIDだけを変更した
[ ] 同じbuildingIDをPR内の複数commitへ分けていない
[ ] 建物commitをuro:buildingIDの昇順に並べた
[ ] Building:、Building-Added:、Building-Deleted:等のtrailerが実変更と一致する
[ ] 変更対象外の整形差分を最小差分版で除いた
```

`Draft`は作業中の保存とCI確認に使う。承認役の確認待ち一覧に入れるのは、自動検査と提案者確認を終えて
`Ready for review`にした後とする。

### 3.3 PR本文

```text
[ ] PR種別を1つ選んだ
[ ] 何を、なぜ、どの根拠で変えるかを書いた
[ ] 対象となる全buildingID又はmanifestを指定した
[ ] 変更してよいpathと、変更してはいけない範囲を明示した
[ ] 関連Issueを Fixes #<番号> 又は Refs #<番号> で接続した
[ ] 根拠のURL、文書名、取得日、版、hash等を追記した
[ ] 形状、LOD、属性、ID、lifecycleを混ぜた場合、分離できない理由を書いた
```

年次 `source-update` では、さらに次を必須にする。

```text
Source-From, Source-To, Scope-Mesh, Attribute-Family, Allowed-Paths,
History-Manifest, Manifest-SHA256, Building-Count,
First-Building-ID, Last-Building-ID
```

### 3.4 自動検査と提案者確認

```text
[ ] base freshnessの「最新版を取り込んでください」が未解決ではなく、headが最新mainを含む
[ ] commit scopeで全commitが合格した
[ ] XML/XSD、CityGML構造、規約のblocking検査が成功した
[ ] XLink、Appearance、imageURI、テクスチャ参照が成立している
[ ] 自動変更サマリがPR本文と一致する
[ ] 幾何変更がある建物は3D比較で旧新を確認した
[ ] warning・noticeを無視せず、対応不要の理由を判断した
[ ] churn通知がある場合、最小差分版を適用後に再検査した
[ ] 最後のpush後のhead SHAで全required checksが緑である
```

現行のchurn処理は通知と最小差分版の生成までであり、PR headへの自動適用は未実装である。
公開時の自動適用が完了するまでは、提案者又はメンテナーが適用する。

### 3.5 承認役の審査

```text
[ ] PRがDraftではなく、確認依頼の状態である
[ ] 確認中のhead SHAと自動検査対象が同じである
[ ] required checksが全て成功し、最新mainを含んでいる
[ ] 変更サマリ、根拠、形状比較、manifestを同じ対象として確認した
[ ] 値・形状・出典・旧新ID関係の意味が妥当である
[ ] lifecycle、identity、texture-override等の追加承認条件を満たした
[ ] 承認後にpushがあった場合は再審査する
```

- 修正可能な不備は `Request changes` で対応箇所を示す。
- 質問又は判断材料の確認は `Comment` を使い、承認と混同しない。
- 根拠が成立し、意味判断と必須検査が全て済んだ場合だけ `Approve` する。
- 重複PR、対象外、公開不可の根拠、解消不能な権利問題は、理由を残してcloseする。

### 3.6 マージ

```text
[ ] 最終head SHAのrequired checksが全て成功している
[ ] Request changesが解消済みである
[ ] 必要なCODEOWNERS・追加承認が揃っている
[ ] base freshnessが最新mainを示している
[ ] 都市データPRで Create a merge commit を選んだ
[ ] マージ直前にPR種別、対象メッシュ、manifestを再確認した
```

自動mergeは行わない。承認はマージ許可の一条件であり、承認役の操作だけでmainは書き換わらない。

### 3.7 マージ後

```text
[ ] merge commitと個々の建物commitがmainに残っている
[ ] main上の検査とPages生成が成功した
[ ] Fixesで接続したIssueが正しくcloseされた
[ ] Building: trailerからPRとmerge commitへ逆引きできる
[ ] 年次更新のrelease-planをplanned / in-progress / completeの正しい状態に更新した
[ ] 利用者画面で「main作業中」と「最新安定release」が区別されている
[ ] 異常がある場合、履歴改変ではなくrevert PRを起票した
```

manifest自身にマージ後のPR番号やSHAを追記するための後追いcommitは作らない。
Git履歴とGitHubからPages索引を再生成して接続する。

## 4. PR種別の選び方

| PR種別 | 1 PRの単位 | 建物commit | 必須の追加記録 |
|---|---|---|---|
| `correction` | 1つの根拠・変更規則 | 1 buildingIDずつ | Issue、根拠、変更前後 |
| `lifecycle` | 1つの建替え・分割・統合 | 専用1commitで複数ID可 | 旧新ID関係、理由、manifest、追加承認 |
| `identity-correction` | 1つの誤接続・ID訂正イベント | 専用ゲートに従う | 訂正前後ID、誤りの根拠、追加承認 |
| `source-update` | 1原典遷移 × 1メッシュ × 1属性系統・規則 | 1 buildingIDずつ | source/change manifest、許可path、件数、標本確認 |
| `schema-update` | 1schema bundle | GML変更なし | XSD・コードリスト等のhash、profile |
| `carry-forward` | 1版更新 × 1メッシュ（前回公式・リポ・新公式） | 新版の `source-baseline` の後、再適用建物ごとに `Building:` 1commit | 来歴manifest: 再適用／吸収／衝突／未対応／旧codeSpace引き継ぎ |
| `schema-migration` | 公式の新版ファイルが無い（リポが正本）ときの1版更新 × 1メッシュ: レジストリ駆動でi-UR部分木を再直列化 | 生成した新版の `source-baseline` 1件 | 来歴manifest、レジストリ全キーの意味同一性（保持／写像／引き継ぎ／未対応）— ゲート未実装 |
| `layout` | 1親メッシュの1段階細分化 | 意味不変の専用1commit | 再集約検査、ID・参照・容量検査 |
| `texture-gc` | 未参照画像の1回の回収 | 建物変更なし | 全imageURI非参照、削除リスト |
| `revert` | 1建物commit又は1PRの取消し | 元の単位を保つ | 取消し対象、理由、影響するrelease |
| コード・文書 | 1つのツール又は説明変更 | 建物変更なし | テスト、文書導線、影響範囲 |

`source-baseline`、`scope-extract`、`identity-baseline`は公開履歴を作る初期構築専用であり、
公開後の日常PRとして繰り返さない。

### 4.1 日常の `correction`

```text
[ ] data-issue又は公開可能な根拠がある
[ ] 同じPRへ束ねた建物は、同じ根拠と判断規則で審査できる
[ ] 各commitはBuilding: <uro:buildingID>を1件持つ
[ ] テクスチャ差し替えは新規画像追加＋imageURI更新で行った
[ ] 幾何を変えた場合、高さ・面積等の派生属性との整合を確認した
```

既存テクスチャの同名上書きは原則禁止とする。共有アトラス等の正当な例外だけ、
影響する全建物の確認後にメンテナーが `texture-override` ラベルを付ける。

### 4.2 `lifecycle`

```text
[ ] 旧新建物の関係を確定し、未解決候補を混ぜていない
[ ] 1つの実世界イベントだけをPRに入れた
[ ] Change-Type: lifecycle を記録した
[ ] Building-Deleted:、Building-Added:を実変更ID全件と一致させた
[ ] 旧新関係、発生日又は確認日、根拠、判断者をmanifestに残した
[ ] lifecycleラベルとCODEOWNERSの追加承認がある
```

旧新関係が不明なら、消滅や建替えと即断せずIssue又は `lifecycle-review`へ保留する。

### 4.3 `identity-correction`

公開済み履歴で同一性の誤接続が判明しても、過去のcommitやtagを書き換えない。
訂正前後ID、誤りの根拠、影響する履歴を新しいPRで残す。

```text
[ ] 訂正前と訂正後のbuildingIDを特定した
[ ] lifecycleではなく誤接続の訂正である根拠がある
[ ] 過去履歴のどの期間へ影響するかを記録した
[ ] identity-correction専用CIと追加承認が成功した
```

現行のcommit scope gateは既存buildingIDの置換を通常更新として通さない。
専用ゲートを実装し、公開パイロットで検証するまでReady for reviewにしない。

### 4.4 年次 `source-update`

年次更新は、次の順に別PRとして進める。

1. `schema-update` — 新版の成果物（`codelists/<版>/` のコード表、schema profile）。GML 変更なし
2. 版が変わる場合: 新公式版があればそれを `source-baseline` にして `carry-forward`（建物×属性の三方向比較）。リポが正本で公式の新版ファイルが無ければ `schema-migration`（レジストリ駆動でi-UR部分木を再直列化し、レジストリ全キーの意味同一性で検証）
3. 属性系統ごとの単棟パイロット
4. 属性系統ごとの複数棟PR
5. 幾何、LOD、原典`gml:id`の専用PR
6. 確定済みイベントの `lifecycle`
7. 各メッシュと全都市の完了検査
8. 年度release tag

```text
[ ] 更新開始前のsource、schema、ID、意味規則、lifecycle、容量判定が完了した
[ ] PRを1原典遷移 × 1メッシュ × 1属性系統・変更規則に限定した
[ ] manifestに許可path、旧新値、対象buildingIDを全件固定した
[ ] 各Attribute-Familyの代表一棟が先に合格した
[ ] 同じメッシュの先行PRマージ後のmainから生成した
[ ] 自動確定群と曖昧・lifecycle要確認群を分けた
[ ] 事前の最終path signatureと完了後の結果が一致した
```

新年度原本を1PRで丸ごと上書きしない。各属性PRは作業領域の新年度版から、
未反映buildingID manifestに基づいて毎回生成する。

`source-update` と `identity-baseline` / `identity-correction` は**一括投稿**であり、コミットを1件ずつ読むのではなく
**再現によって受け入れる**。提出物（計画 Issue、建物ごとの根拠と年度境界ごとの ID 体制を含む来歴マニフェスト、
コミット trailer、専用アカウント、標本監査）とゲートは
[一括投稿の来歴・検証・マージ方針（英語が正）](https://github.com/4dcitygml/tools/blob/main/docs/bulk-submission-provenance.md) に定める。
東京 2020〜2025 年度版の実測では、製品系列が変わる境界（2022→2023）で `uro:buildingID` が全件振り直され、
境界をまたいで同じ ID を持つ建物は**別の建物**だった。したがって ID の一致だけを同一性の根拠にしてはならず、
すべてのリンクに幾何的根拠を要する。

### 4.5 `schema-update` と版更新（`carry-forward`）

```text
[ ] schema-updateはGMLを変更せず、版の成果物（codelists/<版>/、schemas/、provenance/schema-update/）だけを追加した
[ ] 成果物のdigestと公式の出典（ZIP member）を記録した
[ ] 現行データが新profileのoffline XSD検証に合格した
[ ] 版更新は「新公式版＝source-baseline → carry-forward」で行い、旧ファイルの構造変換はしていない
[ ] carry-forward manifestに建物ごとの再適用／吸収／衝突／未対応／旧codeSpace引き継ぎが記録されている
[ ] 衝突と未対応は審査者が判断し、引き継いだコードはrelease gate用に集計した
```

版更新には二つの経路がある。公式版が独立に作られている間は、新公式版を次のbaselineにし、蓄積した修正を建物×意味属性の三方向比較で載せ直す
（`carry-forward`、[一括投稿の来歴・検証・マージ方針（英語が正）](https://github.com/4dcitygml/tools/blob/main/docs/bulk-submission-provenance.md)）。リポが正本になり公式版をリポから出力する段階では外部の新版ファイルは無く、
`schema-migration` がリポ自身の内容から新版の形式を生成する。CityGML核は2.0内で不変（3.0移行の核変換は3DCityDB経由）、i-UR部分木は意味レジストリ・
コード表クロスウォーク（1:1に写せないコードは旧codeSpaceを保持）・新版XSDの順序から建物ごとに再直列化する。ゲートはレジストリ全キーの意味同一性
（保持／写像／引き継ぎ／未対応）と再現で、設計済み・未実装。どちらの経路もレジストリに基づく同じ比較で検証する。`schema-update` はコミット範囲検査
（成果物パスのみ・CityGML変更なし）、`carry-forward` は `source-update` と同じ規則＋`reproduction` ゲートで検査する。

### 4.6 `layout`

```text
[ ] source-update後の保存GMLが50 MiB以上になることを更新前に確認した
[ ] 更新前のmainの現行メッシュだけを1段階細分化した
[ ] Change-Type: layout を記録し、建物ID trailerを付けていない
[ ] 建物件数、ID集合、意味hash、Appearance、XLinkが不変である
[ ] Envelope、XSD、一時再集約の検査に合格した
[ ] 細分化後の全ファイルが50 MiB未満で、100 MiB以上の登録ファイルがない
```

一度細分化したメッシュは、後年度で小さくなっても粗いメッシュへ戻さない。
現行ツールは1段階の細分化までであり、より深い分割は拡張と検証後に解禁する。

### 4.7 `texture-gc`

```text
[ ] 削除候補の全画像がmainの全imageURIから非参照である
[ ] 新たなdangling参照が0件である
[ ] 削除画像の一覧、件数、バイト数をPR本文に記録した
[ ] 建物GML、属性、幾何を同じPRで変更していない
```

### 4.8 `revert`と緊急訂正

公開後の誤りはforce pushやtagの差し替えで隠さない。新しいPRとして取り消す。

```text
[ ] 1建物commitだけを戻すか、PR全体を戻すかを決めた
[ ] 取消し対象のcommit又はmerge commit SHAを記録した
[ ] 取り消す理由、発見経路、影響する建物とreleaseを書いた
[ ] 取消し後のCityGMLに通常と同じ全検査を行った
[ ] 公開済みreleaseへ影響する場合、パッチreleaseの要否を決めた
```

緊急性が高くてもrequired checksと人の承認は省略しない。影響範囲を小さくし、優先度を上げることで対応する。

## 5. releaseの手順

### 5.1 通常の日常修正

- マージ後、修正はmainと建物履歴へ反映される。
- 各PRのマージだけで既存の安定releaseを動かさない。
- 次の定期パッチ又は年度releaseで安定版へ含める。
- 重大な誤り、法的・個人情報問題、利用上の危険がある場合はパッチreleaseを行う。

パッチreleaseのtag命名と定期発行頻度は、公開前に別ADRで固定する。

### 5.2 年次release

```text
[ ] 対象全メッシュの全属性系統PRが完了した
[ ] 幾何、LOD、原典gml:id、lifecycleの確定群が完了した
[ ] schema profileとschema migrationの検査が完了した
[ ] 全buildingID集合、重複、参照、Appearance、XSDが合格した
[ ] 最終path signatureと公式新年度版との意味一致を確認した
[ ] 未解決群を勝手に更新せず、保留一覧と影響を明記した
[ ] release-planがrelease-readyである
[ ] release notesに原典、hash、加工、ID統一、保留、検査結果を記載した
[ ] tag、Pages、ダウンロード、検査結果が同じcommitを指している
[ ] 旧 codeSpace で引き継いだコード（codelists/<版>/）を carried_codespace_report.py で数え、解決済みか公式側が受け入れ済み
```

release-readyの条件が一つでも欠ける間は、mainを「新年度の安定版」と表示しない。

## 6. マージ停止条件

次のいずれかに当てはまる場合は、Approve又はmergeをしない。

- PRが最新mainより遅れている
- required checkが失敗、未実行、又は古いhead SHAを対象にしている
- 原典、根拠、ライセンス、公開可否が確認できない
- PR種別と変更内容が一致しない
- manifest外のbuildingID、path、旧新値が一件でもある
- 同じメッシュの先行PRが未マージである
- buildingIDの同一性、lifecycle関係、schema変換の意味が未解決である
- 更新後に50 MiB以上になるメッシュのlayout PRが未完了である
- churnが残り、対象外の建物や行まで変わって見える
- 必要なCODEOWNERS、lifecycle、identity、texture-overrideの承認がない
- 専用CIが未実装のPR種別を、通常更新として迂回しようとしている

## 7. 現行実装と公開前の残作業

### 7.1 現行リポジトリで検査できるもの

- 通常commitの1 buildingID制約とtrailer一致
- PR内の同一buildingID重複commitの禁止
- `lifecycle`、`layout`、`source-baseline`、`scope-extract` のcommit scope例外
- `scope-extract` の対象自治体集合と保持建物不変
- XML/XSD、構造、参照、テクスチャ、幾何の検査と比較表示
- PR base freshnessの案内
- Draft、自動検査中、最新版待ち、承認待ちを分けた管理者レビュー画面

### 7.2 対象PRを解禁する前に実装するもの

- 版別schema profileの検証オプション（現在は1つのmaster schemaがi-UR 2.0〜3.2を包含）
- `identity-baseline` / `identity-correction` の実差分と追加承認ゲート
- `source-update` のAllowed-Paths、旧新値、manifest対象IDの全件照合
- 最終path signatureと公式原典一致のrelease gate
- より深いメッシュ分割が必要な場合の分割・再集約ツール
- Git履歴からbuildingID → commit → PR → merge commit → releaseを生成するPages索引
- same-repoとforkの最小差分版自動適用
- パッチreleaseのtag命名、発行頻度、緊急性判定のADR

未実装の専用ゲートは、文書上の注意だけで代替しない。実機でrejectとrevertを確認してから公開運用へ入れる。

- 建物別履歴の導出（tools の `scripts/building_history.py`。コミット粒度に依らず、ID 変更・ファイル丸ごとの baseline・manifest 付きコミットをまたいで建物を追い、コミットごとのレジストリ鍵の変更を出す）は実装済み。`history-index.yml` workflow が静的な Pages サイト（リポジトリ内容と同じ Pages サイト配下の `history/index.html`＋`history/buildings/<id>.json`）として公開する
- 実装済みの `identity-baseline` / `identity-correction` ゲート（コミット範囲規則＋`identity` 再現）の実リポジトリでのパイロット検証
- `source-update` の値置換ゲート（1 PR = 1 属性系統、マニフェスト裏付けコミット、再現）の実リポジトリでのパイロット検証
- 版仕様の変更（新年度版で属性コンテナが追加・削除されるもの。2020→2025 の実測差分の大半）は公式版がある間は `carry-forward`（実装済み）で扱う。リポが正本の段階の `schema-migration`（再直列化器・意味同一性ゲート・i-UR 4.0 レジストリ）は設計済み・未実装

## 8. 公開後の定期点検

### 毎週

```text
[ ] 承認待ち、Request changes、最新main待ちのPRを分けて確認した
[ ] CI故障とデータ不合格を分けて対応した
[ ] 長期停滞PRへ次の行動又はclose理由を書いた
[ ] 同じメッシュの競合PRがない
```

### 毎月・定期release前

```text
[ ] 未参照テクスチャ候補を確認した
[ ] 新規の公的原典・年次版の有無と確認日を記録した
[ ] required workflowと共通ツールのtag pinを点検した
[ ] CODEOWNERS、承認権限、退職・異動による欠員を確認した
[ ] release対象commitの出典、権利、未解決事項を確認した
```
