# Copyright (c) 2026 4dcitygml
# SPDX-License-Identifier: Apache-2.0
"""Every text the trusted side posts to a pull request, in the city's language.

The city's language is `lang` in 4dcitygml.json (the report reads it from the inspection).
Residents read the city's language only; English is the text for `en` and for a language
this table does not carry. Comment markers stay outside this table: they are fixed.
"""
from operator_explanation import FIELDS

STATUSES = ('pass', 'warn', 'fail', 'error', 'na', 'pending')


def labels(*names):
    return dict(zip(FIELDS, names))


def statuses(*names):
    return dict(zip(STATUSES, names))


TEXT = {
 'ja': {
        'check_current': '最新の CI 報告があります', 'check_fix': '修正が必要です', 'check_system': 'システムの失敗',
        'check_workflow_change': 'workflow の変更：メンテナーの確認待ち', 'check_waiting': '最新の CI 報告を待っています',
        'freshness_active': '## 🔄 最新版を取り込んでください\n\nこの提案の作成後に、ほかの変更が {behind} 件先に反映されました。\n作業が失われないよう、最新版を取り込んでから再度送信してください。\n\n<sub>レビュー担当者の対応は不要です。更新後、自動検査が再び実行されます。</sub>\n',
        'freshness_resolved': '## ✅ 最新版を取り込みました\n\nこの変更は、公開中の最新データに基づいています。\n',
        'recheck_not_allowed': '再検査を依頼できるのは、提案者とメンテナーだけです。',
        'recheck_no_record': '再実行できる自動検査の記録が見つかりませんでした。メンテナーに連絡してください。',
        'recheck_running': '🔄 自動検査はまだ実行中です。結果が出るまで数分お待ちください。',
        'recheck_started': '🔄 自動検査を再び開始しました。結果が出るまで数分お待ちください。',
        'heading': 'CI が生成した確認用報告', 'labels': labels('変更', '根拠', '検査', '影響', '推奨'),
        'source': '投稿者が示した根拠・説明（内容の裏付けを機械が保証するものではありません）：\n',
        'impact': '変更ファイル数：{n}。マージ後の変更は次回の配布対象です。現在の安定版は自動で差し替わりません。\n',
        'pass': '機械検査は完了しました。承認者はこの共通報告と比較表示を確認し、採用してよければ GitHub の Approve で承認してください。必要人数はリポジトリの現在の設定に従います。',
        'fix': '投稿者による修正が必要です。下記の不合格項目と詳細コメントを確認し、修正を送信してください。再検査と報告の再生成は自動で行います。職員への承認依頼は保留します。',
        'system': '検査または報告の生成・配信が完了していません。データ不備とは区別し、失敗した処理を再実行してください。人手で結果を補って承認へ進めません。',
        'missing': '変更説明を生成できませんでした。', 'plain': 'データ変更以外の提案です。変更ファイル：\n',
        'bulk': '一括処理・対象範囲の再現検査を伴う提案です。来歴と再現結果：\n',
        'limited': '\n（表示を省略しています。完全な結果はこの CI 実行の artifact を確認してください。）',
        'human': '\n人による確認事項：根拠と変更の整合、比較表示、例外ラベルの意図。不明点だけ補足・照会してください。',
        'lifecycle': '旧・新建物の対応は申告された関係です。CI は ID と記録の整合を検査します。実際に一つの建て替え・分割・統合であることは、自治体が根拠と比較表示で判断してください。',
        'advisory': '\n助言（⚠️）の項目があります。比較表示とあわせて確認してください。これらはマージを止めません。',
        'statuses': statuses('合格', '警告', '不合格', 'システムエラー', '対象外', '未完了')},
 'en': {
        'check_current': 'Current CI report available', 'check_fix': 'Fix needed', 'check_system': 'System failure',
        'check_workflow_change': 'Workflow change: maintainer review', 'check_waiting': 'Waiting for current CI report',
        'freshness_active': '## 🔄 Please merge in the latest version\n\nAfter this proposal was created, {behind} other change(s) were applied first.\nTo avoid losing your work, merge in the latest version and submit again.\n\n<sub>No reviewer action is needed. After the update, the automated checks run again.</sub>\n',
        'freshness_resolved': '## ✅ Latest version merged\n\nThe changes are based on the latest published data.\n',
        'recheck_not_allowed': 'Only the proposer or a maintainer can request a re-inspection.',
        'recheck_no_record': 'No re-runnable automated inspection record was found. Please contact a maintainer.',
        'recheck_running': '🔄 The automated inspection is still running. Please wait a few minutes for the results.',
        'recheck_started': '🔄 The automated inspection was started again. Please wait a few minutes for the results.',
        'heading': 'CI-generated review report', 'labels': labels('Change', 'Evidence', 'Checks', 'Impact', 'Recommendation'),
        'source': 'Proposer-supplied evidence and explanation (not independently verified by CI):\n',
        'impact': 'Changed files: {n}. Merged changes enter a future release; the current stable release is not replaced automatically.\n',
        'pass': 'Mechanical checks completed. Reviewers read this shared report and comparisons, then use GitHub Approve if the proposal should be adopted. The required count follows current repository settings.',
        'fix': 'The proposer must address the failed items and detailed comments, then submit the fix. Re-inspection and report generation run automatically. City approval is not requested yet.',
        'system': 'Inspection or report generation/delivery is incomplete. Retry the failed process; do not substitute a human-written result to proceed.',
        'missing': 'Change explanation could not be generated.', 'plain': 'Non-data proposal. Changed files:\n',
        'bulk': 'Reproducible bulk/scope proposal. Provenance and reproduction results:\n',
        'limited': '\n(Display shortened. Read the complete artifact from this CI run.)',
        'human': '\nHuman attention: consistency of evidence and change, comparison views, and the intent of exception labels. Add notes or questions only where needed.',
        'lifecycle': 'The old/new relationship is declared evidence. CI checks ID and record consistency. The city must judge whether this is one real-world rebuild, split or merge using evidence and comparison views.',
        'advisory': '\nThere are advisory findings (⚠️). Review them with the comparison views; they do not block the merge.',
        'statuses': statuses('Pass', 'Warning', 'Fail', 'System error', 'Not applicable', 'Incomplete')},
 'de': {
        'check_current': 'Aktueller CI-Bericht vorhanden', 'check_fix': 'Korrektur nötig', 'check_system': 'Systemfehler',
        'check_workflow_change': 'Workflow-Änderung: Prüfung durch den Maintainer', 'check_waiting': 'Warten auf aktuellen CI-Bericht',
        'freshness_active': '## 🔄 Bitte die neueste Version übernehmen\n\nNach dem Erstellen dieses Vorschlags wurden zuerst {behind} andere Änderung(en) übernommen.\nDamit Ihre Arbeit nicht verloren geht, übernehmen Sie die neueste Version und reichen Sie erneut ein.\n\n<sub>Für die Prüfenden ist nichts zu tun. Nach der Aktualisierung laufen die automatischen Prüfungen erneut.</sub>\n',
        'freshness_resolved': '## ✅ Neueste Version übernommen\n\nDie Änderungen beruhen auf den neuesten veröffentlichten Daten.\n',
        'recheck_not_allowed': 'Eine erneute Prüfung können nur der Einreicher und Maintainer anfordern.',
        'recheck_no_record': 'Es wurde kein erneut ausführbarer Lauf der automatischen Prüfung gefunden. Bitte wenden Sie sich an einen Maintainer.',
        'recheck_running': '🔄 Die automatische Prüfung läuft noch. Bitte warten Sie einige Minuten auf die Ergebnisse.',
        'recheck_started': '🔄 Die automatische Prüfung wurde erneut gestartet. Bitte warten Sie einige Minuten auf die Ergebnisse.',
        'heading': 'Automatisch erstellter Prüfbericht', 'labels': labels('Änderung', 'Belege', 'Prüfungen', 'Auswirkungen', 'Empfehlung'),
        'source': 'Belege und Erläuterung des Einreichers (nicht unabhängig durch CI bestätigt):\n',
        'impact': 'Geänderte Dateien: {n}. Übernommene Änderungen werden mit einer künftigen Version verteilt; die bestehende stabile Version bleibt bestehen.\n',
        'pass': 'Die automatischen Prüfungen sind abgeschlossen. Prüfende lesen denselben Bericht und die Vergleiche und stimmen mit GitHub Approve zu. Die erforderliche Anzahl richtet sich nach den aktuellen Repository-Regeln.',
        'fix': 'Der Einreicher muss die fehlgeschlagenen Prüfungen bearbeiten und die Korrektur senden. Prüfung und Bericht werden automatisch erneuert. Eine Freigabe der Stadt wird noch nicht angefordert.',
        'system': 'Prüfung oder Berichtserstellung/-veröffentlichung ist unvollständig. Den fehlgeschlagenen Prozess erneut ausführen; kein manuelles Ergebnis als Ersatz verwenden.',
        'missing': 'Die Änderungsbeschreibung konnte nicht erstellt werden.', 'plain': 'Vorschlag ohne Datenänderung. Geänderte Dateien:\n',
        'bulk': 'Reproduzierbarer Sammelvorschlag. Herkunft und Reproduktionsprüfung:\n',
        'limited': '\n(Anzeige gekürzt. Vollständige Ergebnisse im Artefakt dieses CI-Laufs.)',
        'human': '\nMenschliche Prüfung: Übereinstimmung von Belegen und Änderung, Vergleichsansichten und Ausnahmelabel. Nur offene Punkte ergänzen oder erfragen.',
        'lifecycle': 'Die Beziehung zwischen alten und neuen Gebäuden ist eine Angabe des Einreichers. CI prüft IDs und Aufzeichnungen. Die Stadt beurteilt anhand von Belegen und Vergleichen, ob ein tatsächlicher Neubau-, Teilungs- oder Zusammenlegungsvorgang vorliegt.',
        'advisory': '\nEs gibt Hinweise (⚠️). Bitte zusammen mit den Vergleichsansichten prüfen; sie blockieren den Merge nicht.',
        'statuses': statuses('Bestanden', 'Warnung', 'Fehlgeschlagen', 'Systemfehler', 'Nicht anwendbar', 'Unvollständig')}}


def language(code):
    """The text table of a language code such as `ja`, `de-DE` or `en`."""
    return TEXT.get(str(code or 'en').split('-')[0], TEXT['en'])
