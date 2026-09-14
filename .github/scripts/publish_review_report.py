# Copyright (c) 2026 4dcitygml
# SPDX-License-Identifier: Apache-2.0
"""Publish a deterministic explanation from CI evidence, never a human transcription."""
import json
import os
from pathlib import Path

from check_review_report import api, checked, open_heads, open_check, close_check
from operator_explanation import FIELDS, REPORT_MARKER, bot, context, encode_report, latest_run, pages, report_comment

STATUSES = ('pass', 'fail', 'na', 'pending')
# Every gate this publisher knows, and the analysis-side outcome variable that
# records whether the gate itself ran. A newer analyzer may add gates: this
# trusted side runs from main and is updated first, so it must accept both.
OUTCOME_KEYS = {'reason': 'REASON_OUTCOME', 'classification': 'CLASSIFICATION_OUTCOME',
                'commit-scope': 'COMMIT_SCOPE_OUTCOME', 'scope-reproducibility': 'SCOPE_REPRODUCIBILITY_OUTCOME',
                'reproduction': 'REPRODUCTION_OUTCOME', 'freshness': 'FRESHNESS_OUTCOME',
                'file-scope': 'QUALITY_OUTCOME', 'schema': 'FORMAT_OUTCOME', 'minimal-diff': 'REVIEWABILITY_OUTCOME',
                'texture': 'TEXTURE_OUTCOME', 'structure': 'STRUCTURE_OUTCOME', 'plausibility': 'PLATEAU_OUTCOME',
                'topology': 'TOPOLOGY_OUTCOME', 'model': 'PREVIEW_OUTCOME'}
SHOWN = 1800   # characters of a field shown in the comment; the artifact keeps the rest


def labels(*names):
    return dict(zip(FIELDS, names))


def statuses(*names):
    return dict(zip(STATUSES, names))


TEXT = {
 'ja': {'heading': 'CI が生成した確認用報告', 'labels': labels('変更', '根拠', '検査', '影響', '推奨'),
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
        'statuses': statuses('合格', '不合格', '対象外', '未完了')},
 'en': {'heading': 'CI-generated review report', 'labels': labels('Change', 'Evidence', 'Checks', 'Impact', 'Recommendation'),
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
        'statuses': statuses('Pass', 'Fail', 'Not applicable', 'Incomplete')},
 'de': {'heading': 'Automatisch erstellter Prüfbericht', 'labels': labels('Änderung', 'Belege', 'Prüfungen', 'Auswirkungen', 'Empfehlung'),
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
        'statuses': statuses('Bestanden', 'Fehlgeschlagen', 'Nicht anwendbar', 'Unvollständig')}}


def language(inspection):
    return TEXT.get(str(inspection.get('lang', 'en')).split('-')[0], TEXT['en'])


def attempt(run):
    return run.get('run_attempt', 1)


def validated_rows(pr, inspection):
    """The inspection rows, once the inspection is current and complete."""
    if inspection.get('context') != context(pr) or inspection.get('pr') != pr['number']:
        raise ValueError('Inspection context is stale')
    rows = inspection.get('checks')
    if not isinstance(rows, list) or not set(OUTCOME_KEYS) <= {r.get('key') for r in rows if isinstance(r, dict)}:
        raise ValueError('Incomplete inspection result')
    if any(r.get('status') not in STATUSES for r in rows):
        raise ValueError('Unknown inspection state')
    return rows


def decide_state(rows, run, outcomes):
    """pass / fix / system from the gate rows and the run that produced them."""
    state = 'fix' if any(r['status'] == 'fail' for r in rows) else 'pass'
    if any(r['status'] == 'pending' for r in rows) or (run['conclusion'] != 'success' and state == 'pass'):
        return 'system'
    # A failed gate whose own outcome is not recorded did not run to completion.
    if outcomes is not None and any(r['status'] == 'fail' and outcomes.get(OUTCOME_KEYS[r['key']]) not in ('success', 'failure')
                                    for r in rows if r['key'] in OUTCOME_KEYS):
        return 'system'
    return state


def describe_change(inspection, artifacts, names, text):
    """The change field and whether the artifact that backs it is present."""
    if inspection.get('bulk') or inspection.get('scopeExtract'):
        return (text['bulk'] + artifacts.get('reproduction.md', artifacts.get('commit-scope.md', '')),
                bool(artifacts.get('reproduction.md') or artifacts.get('commit-scope.md')))
    if inspection.get('hasGml'):
        return artifacts.get('summary.md') or text['missing'], bool(artifacts.get('summary.md'))
    return text['plain'] + names, True


def lifecycle_lines(events):
    for event in events:
        yield f"{event['kind']} / {event['eventId']}: " + ', '.join(event['oldIds']) + ' → ' + ', '.join(event['newIds'])
        yield event['reason']
        yield 'confirmedOn: ' + event['confirmedOn']
        if event.get('occurredOn'):
            yield 'occurredOn: ' + event['occurredOn']
        yield from (e['title'] + ': ' + e['url'] for e in event['evidence'])


def build_report(repo, pr, run, inspection, artifacts, files):
    rows = validated_rows(pr, inspection)
    text = language(inspection)
    state = decide_state(rows, run, inspection.get('outcomes'))
    names = '\n'.join('- ' + f['filename'] for f in files)
    change, backed = describe_change(inspection, artifacts, names, text)
    if state == 'pass' and not backed:
        state = 'system'
    lifecycle = inspection.get('lifecycle') or []
    if lifecycle:
        change = '\n'.join(lifecycle_lines(lifecycle)) + '\n\n' + change

    def shorten(value):
        return value if len(value) <= SHOWN else value[:SHOWN] + text['limited']
    fields = {'change': shorten(change), 'evidence': shorten(text['source'] + (pr.get('body') or '—')),
              'checks': '\n'.join(f"- {r['label']}: {text['statuses'][r['status']]}" for r in rows),
              'impact': shorten(text['impact'].format(n=len(files)) + names),
              'recommendation': text[state] + text['human'] + ('\n' + text['lifecycle'] if lifecycle else '')}
    return encode_report({'version': 1, 'repo': repo, 'pr': pr['number'], 'context': context(pr),
                          'runId': run['id'], 'runAttempt': attempt(run),
                          'runUrl': f"https://github.com/{repo}/actions/runs/{run['id']}/attempts/{attempt(run)}",
                          'toolsRef': inspection.get('toolsRef', ''), 'state': state, 'checks': rows, 'lifecycle': lifecycle,
                          'heading': text['heading'], 'labels': text['labels'], 'fields': fields})


def run():
    repo = os.environ['GITHUB_REPOSITORY']
    event = json.loads(Path(os.environ.get('REPORT_EVENT_PATH') or os.environ['GITHUB_EVENT_PATH']).read_text())
    analysis = event['workflow_run']
    number = int(Path('out/pr.txt').read_text())
    pr = checked(f'/repos/{repo}/pulls/{number}')
    if pr['state'] != 'open' or pr['head']['sha'] != analysis['head_sha']:
        raise ValueError('Stale run')
    if open_heads(repo)[1][pr['head']['sha']] != 1:
        raise ValueError('Multiple open PRs share this head; checks cannot distinguish them')
    latest = latest_run(api, repo, pr)
    if (latest['id'], attempt(latest)) != (analysis['id'], attempt(analysis)):
        raise ValueError('Superseded run')
    check = open_check(repo, pr['head']['sha'])
    try:
        inspection = json.loads(Path('out/inspection.json').read_text())
        artifacts = {p.name: p.read_text(errors='replace') for p in Path('out').glob('*.md') if p.is_file() and not p.is_symlink()}
        files = pages(api, f'/repos/{repo}/pulls/{number}/files')
        report = build_report(repo, pr, analysis, inspection, artifacts, files)
        current = checked(f'/repos/{repo}/pulls/{number}')
        if context(current) != context(pr):
            raise ValueError('PR changed during publication')
        # One immutable comment per CI run/attempt. A retry repairs that comment;
        # it never replaces a different report to which a human already attested.
        comments = pages(api, f'/repos/{repo}/issues/{number}/comments')
        key = f"<!-- citygml-report-run:{analysis['id']}:{attempt(analysis)} -->"
        body = report_comment(report) + '\n' + key
        existing = next((c for c in comments if bot(c) and c.get('body', '').startswith(REPORT_MARKER) and key in c['body']), None)
        if existing:
            checked(f"/repos/{repo}/issues/comments/{existing['id']}", 'PATCH', {'body': body})
        else:
            checked(f'/repos/{repo}/issues/{number}/comments', 'POST', {'body': body})
        close_check(repo, check, report['state'] == 'pass', report['heading'], report['fields']['recommendation'],
                    external_id=report['reportId'])
    except Exception:
        close_check(repo, check, False, 'Report publication failed', 'Retry PR Comment (CityGML); no operator transcription is required.')
        raise


if __name__ == '__main__':
    run()
