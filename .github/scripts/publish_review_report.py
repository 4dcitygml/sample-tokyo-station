# Copyright (c) 2026 4dcitygml
# SPDX-License-Identifier: Apache-2.0
"""Publish a deterministic explanation from CI evidence, never a human transcription."""
import json
import os
from pathlib import Path
from check_review_report import api, checked
from operator_explanation import context, pages, latest_run, encode_report, report_comment, REPORT_MARKER, bot

TEXT = {
 'ja': {'heading': 'CI が生成した確認用報告', 'labels': dict(zip(('change','evidence','checks','impact','recommendation'), ('変更','根拠','検査','影響','推奨'))),
        'source': '投稿者が示した根拠・説明（内容の裏付けを機械が保証するものではありません）：\n',
        'impact': '変更ファイル数：{n}。マージ後の変更は次回の配布対象です。現在の安定版は自動で差し替わりません。\n',
        'pass': '機械検査は完了しました。承認者はこの共通報告と比較表示を確認し、採用してよければ GitHub の Approve で承認してください。必要人数はリポジトリの現在の設定に従います。',
        'fix': '投稿者による修正が必要です。下記の不合格項目と詳細コメントを確認し、修正を送信してください。再検査と報告の再生成は自動で行います。職員への承認依頼は保留します。',
        'system': '検査または報告の生成・配信が完了していません。データ不備とは区別し、失敗した処理を再実行してください。人手で結果を補って承認へ進めません。',
        'missing': '変更説明を生成できませんでした。', 'plain': 'データ変更以外の提案です。変更ファイル：\n',
        'bulk': '一括処理・対象範囲の再現検査を伴う提案です。来歴と再現結果：\n',
        'limited': '\n（表示を省略しています。完全な結果はこの CI 実行の artifact を確認してください。）',
        'human': '\n人による確認事項：根拠と変更の整合、比較表示、例外ラベルの意図。不明点だけ補足・照会してください。',
        'statuses': {'pass':'合格','fail':'不合格','na':'対象外','pending':'未完了'}},
 'en': {'heading':'CI-generated review report','labels':dict(zip(('change','evidence','checks','impact','recommendation'),('Change','Evidence','Checks','Impact','Recommendation'))),
        'source':'Proposer-supplied evidence and explanation (not independently verified by CI):\n',
        'impact':'Changed files: {n}. Merged changes enter a future release; the current stable release is not replaced automatically.\n',
        'pass':'Mechanical checks completed. Reviewers read this shared report and comparisons, then use GitHub Approve if the proposal should be adopted. The required count follows current repository settings.',
        'fix':'The proposer must address the failed items and detailed comments, then submit the fix. Re-inspection and report generation run automatically. City approval is not requested yet.',
        'system':'Inspection or report generation/delivery is incomplete. Retry the failed process; do not substitute a human-written result to proceed.',
        'missing':'Change explanation could not be generated.', 'plain':'Non-data proposal. Changed files:\n',
        'bulk':'Reproducible bulk/scope proposal. Provenance and reproduction results:\n',
        'limited':'\n(Display shortened. Read the complete artifact from this CI run.)',
        'human':'\nHuman attention: consistency of evidence and change, comparison views, and the intent of exception labels. Add notes or questions only where needed.',
        'statuses':{'pass':'Pass','fail':'Fail','na':'Not applicable','pending':'Incomplete'}},
 'de': {'heading':'Automatisch erstellter Prüfbericht','labels':dict(zip(('change','evidence','checks','impact','recommendation'),('Änderung','Belege','Prüfungen','Auswirkungen','Empfehlung'))),
        'source':'Belege und Erläuterung des Einreichers (nicht unabhängig durch CI bestätigt):\n',
        'impact':'Geänderte Dateien: {n}. Übernommene Änderungen werden mit einer künftigen Version verteilt; die bestehende stabile Version bleibt bestehen.\n',
        'pass':'Die automatischen Prüfungen sind abgeschlossen. Prüfende lesen denselben Bericht und die Vergleiche und stimmen mit GitHub Approve zu. Die erforderliche Anzahl richtet sich nach den aktuellen Repository-Regeln.',
        'fix':'Der Einreicher muss die fehlgeschlagenen Prüfungen bearbeiten und die Korrektur senden. Prüfung und Bericht werden automatisch erneuert. Eine Freigabe der Stadt wird noch nicht angefordert.',
        'system':'Prüfung oder Berichtserstellung/-veröffentlichung ist unvollständig. Den fehlgeschlagenen Prozess erneut ausführen; kein manuelles Ergebnis als Ersatz verwenden.',
        'missing':'Die Änderungsbeschreibung konnte nicht erstellt werden.', 'plain':'Vorschlag ohne Datenänderung. Geänderte Dateien:\n',
        'bulk':'Reproduzierbarer Sammelvorschlag. Herkunft und Reproduktionsprüfung:\n',
        'limited':'\n(Anzeige gekürzt. Vollständige Ergebnisse im Artefakt dieses CI-Laufs.)',
        'human':'\nMenschliche Prüfung: Übereinstimmung von Belegen und Änderung, Vergleichsansichten und Ausnahmelabel. Nur offene Punkte ergänzen oder erfragen.',
        'statuses':{'pass':'Bestanden','fail':'Fehlgeschlagen','na':'Nicht anwendbar','pending':'Unvollständig'}}}


def build_report(repo, pr, run, inspection, artifacts, files):
    if inspection.get('context') != context(pr) or inspection.get('pr') != pr['number']:
        raise ValueError('Inspection context is stale')
    rows = inspection.get('checks')
    expected = {'reason','classification','commit-scope','scope-reproducibility','reproduction','freshness','file-scope','schema','minimal-diff','texture','structure','plausibility','topology','model'}
    # Every gate this publisher knows must be present; a newer analyzer may add gates
    # (this trusted side runs from main and is updated first, so it must accept both).
    if not isinstance(rows, list) or not expected <= {r.get('key') for r in rows if isinstance(r, dict)}:
        raise ValueError('Incomplete inspection result')
    if any(r.get('status') not in ('pass','fail','na','pending') for r in rows):
        raise ValueError('Unknown inspection state')
    text = TEXT.get(str(inspection.get('lang','en')).split('-')[0], TEXT['en'])
    state = 'fix' if any(r['status'] == 'fail' for r in rows) else 'pass'
    if any(r['status'] == 'pending' for r in rows) or (run['conclusion'] != 'success' and state == 'pass'):
        state = 'system'
    outcome_keys = {'reason':'REASON_OUTCOME','classification':'CLASSIFICATION_OUTCOME','commit-scope':'COMMIT_SCOPE_OUTCOME','freshness':'FRESHNESS_OUTCOME',
                    'schema':'FORMAT_OUTCOME','minimal-diff':'REVIEWABILITY_OUTCOME','file-scope':'QUALITY_OUTCOME',
                    'texture':'TEXTURE_OUTCOME','structure':'STRUCTURE_OUTCOME','plausibility':'PLATEAU_OUTCOME',
                    'topology':'TOPOLOGY_OUTCOME','model':'PREVIEW_OUTCOME','reproduction':'REPRODUCTION_OUTCOME',
                    'scope-reproducibility':'SCOPE_REPRODUCIBILITY_OUTCOME'}
    outcomes = inspection.get('outcomes')
    if outcomes is not None and any(r['status'] == 'fail' and outcomes.get(outcome_keys.get(r['key'], '')) not in ('success','failure') for r in rows if r['key'] in outcome_keys):
        state = 'system'
    def shorten(value):
        return value if len(value) <= 1800 else value[:1800] + text['limited']
    names = '\n'.join('- '+f['filename'] for f in files)
    if inspection.get('bulk') or inspection.get('scopeExtract'):
        change = text['bulk'] + artifacts.get('reproduction.md', artifacts.get('commit-scope.md', ''))
        if state == 'pass' and not (artifacts.get('reproduction.md') or artifacts.get('commit-scope.md')):
            state = 'system'
    elif inspection.get('hasGml'):
        change = artifacts.get('summary.md') or text['missing']
        if state == 'pass' and not artifacts.get('summary.md'):
            state = 'system'
    else:
        change = text['plain'] + names
    lifecycle = inspection.get('lifecycle') or []
    if lifecycle:
        event_lines = []
        for event in lifecycle:
            event_lines.append(f"{event['kind']} / {event['eventId']}: " + ', '.join(event['oldIds']) + ' → ' + ', '.join(event['newIds']))
            event_lines.append(event['reason'])
            event_lines.append('confirmedOn: ' + event['confirmedOn'])
            if event.get('occurredOn'):
                event_lines.append('occurredOn: ' + event['occurredOn'])
            event_lines.extend(e['title'] + ': ' + e['url'] for e in event['evidence'])
        change = '\n'.join(event_lines) + '\n\n' + change
        attention = {
            'ja': '旧・新建物の対応は申告された関係です。CI は ID と記録の整合を検査します。実際に一つの建て替え・分割・統合であることは、自治体が根拠と比較表示で判断してください。',
            'en': 'The old/new relationship is declared evidence. CI checks ID and record consistency. The city must judge whether this is one real-world rebuild, split or merge using evidence and comparison views.',
            'de': 'Die Beziehung zwischen alten und neuen Gebäuden ist eine Angabe des Einreichers. CI prüft IDs und Aufzeichnungen. Die Stadt beurteilt anhand von Belegen und Vergleichen, ob ein tatsächlicher Neubau-, Teilungs- oder Zusammenlegungsvorgang vorliegt.'}
        lifecycle_note = attention.get(str(inspection.get('lang', 'en')).split('-')[0], attention['en'])
    else:
        lifecycle_note = ''
    result = '\n'.join(f"- {r['label']}: {text['statuses'][r['status']]}" for r in rows)
    fields = {'change':shorten(change), 'evidence':shorten(text['source'] + (pr.get('body') or '—')),
              'checks':result, 'impact':shorten(text['impact'].format(n=len(files)) + names),
              'recommendation':text[state] + text['human'] + ('\n' + lifecycle_note if lifecycle_note else '')}
    return encode_report({'version':1,'repo':repo,'pr':pr['number'],'context':context(pr),
                          'runId':run['id'],'runAttempt':run.get('run_attempt',1),
                          'runUrl':f"https://github.com/{repo}/actions/runs/{run['id']}/attempts/{run.get('run_attempt',1)}",
                          'toolsRef':inspection.get('toolsRef',''),'state':state,'checks':rows,'lifecycle':lifecycle,
                          'heading':text['heading'],'labels':text['labels'],'fields':fields})


def run():
    repo = os.environ['GITHUB_REPOSITORY']
    event = json.loads(Path(os.environ.get('REPORT_EVENT_PATH') or os.environ['GITHUB_EVENT_PATH']).read_text())
    analysis = event['workflow_run']
    number = int(Path('out/pr.txt').read_text())
    pr = checked(f'/repos/{repo}/pulls/{number}')
    if pr['state'] != 'open' or pr['head']['sha'] != analysis['head_sha']:
        raise ValueError('Stale run')
    if sum(p['head']['sha'] == pr['head']['sha'] for p in pages(api, f'/repos/{repo}/pulls?state=open')) != 1:
        raise ValueError('Multiple open PRs share this head; checks cannot distinguish them')
    latest = latest_run(api,repo,pr)
    if (latest['id'],latest.get('run_attempt',1)) != (analysis['id'],analysis.get('run_attempt',1)):
        raise ValueError('Superseded run')
    check = checked(f'/repos/{repo}/check-runs','POST',{'name':'ci-report','head_sha':pr['head']['sha'],'status':'in_progress'})
    try:
        inspection = json.loads(Path('out/inspection.json').read_text())
        artifacts = {p.name:p.read_text(errors='replace') for p in Path('out').glob('*.md') if p.is_file() and not p.is_symlink()}
        files = pages(api,f'/repos/{repo}/pulls/{number}/files')
        report = build_report(repo,pr,analysis,inspection,artifacts,files)
        current = checked(f'/repos/{repo}/pulls/{number}')
        if context(current) != context(pr):
            raise ValueError('PR changed during publication')
        # One immutable comment per CI run/attempt. A retry repairs that comment;
        # it never replaces a different report to which a human already attested.
        comments = pages(api,f'/repos/{repo}/issues/{number}/comments')
        key = f"<!-- citygml-report-run:{analysis['id']}:{analysis.get('run_attempt',1)} -->"
        body = report_comment(report) + '\n' + key
        existing = next((c for c in comments if bot(c) and c.get('body','').startswith(REPORT_MARKER) and key in c['body']),None)
        if existing:
            checked(f"/repos/{repo}/issues/comments/{existing['id']}",'PATCH',{'body':body})
        else:
            checked(f'/repos/{repo}/issues/{number}/comments','POST',{'body':body})
        checked(f"/repos/{repo}/check-runs/{check['id']}",'PATCH',{'status':'completed',
                'conclusion':'success' if report['state']=='pass' else 'failure',
                'external_id':report['reportId'], 'output':{'title':report['heading'],'summary':report['fields']['recommendation']}})
    except Exception:
        checked(f"/repos/{repo}/check-runs/{check['id']}",'PATCH',{'status':'completed','conclusion':'failure',
                'output':{'title':'Report publication failed','summary':'Retry PR Comment (CityGML); no operator transcription is required.'}})
        raise


if __name__ == '__main__':
    run()
