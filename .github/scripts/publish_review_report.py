# Copyright (c) 2026 4dcitygml
# SPDX-License-Identifier: Apache-2.0
"""Publish a deterministic explanation from CI evidence, never a human transcription."""
import json
from pathlib import Path

import github_api as gh
import texts
from texts import STATUSES
from operator_explanation import REPORT_MARKER, context, encode_report, report_comment

# Every gate this publisher knows. Each inspection row says itself whether the gates
# behind it reached a result (`ran`, written by the analyzer since tools v1.5.0; the
# trusted scripts and the tools pin move together, so there is no older analyzer to
# serve). A newer analyzer may add gates: this trusted side runs from main and is
# updated first, so it must accept both.
GATES = ('reason', 'classification', 'commit-scope', 'scope-reproducibility', 'reproduction', 'freshness',
         'file-scope', 'schema', 'minimal-diff', 'texture', 'structure', 'plausibility', 'topology', 'model')
SHOWN = 1800   # characters of a field shown in the comment; the artifact keeps the rest


def validated_rows(pr, inspection):
    """The inspection rows, once the inspection is current and complete."""
    if inspection.get('context') != context(pr) or inspection.get('pr') != pr['number']:
        raise ValueError('Inspection context is stale')
    rows = inspection.get('checks')
    if not isinstance(rows, list) or not set(GATES) <= {r.get('key') for r in rows if isinstance(r, dict)}:
        raise ValueError('Incomplete inspection result')
    if any(r.get('status') not in STATUSES for r in rows):
        raise ValueError('Unknown inspection state')
    return rows


def decide_state(rows, run):
    """pass / fix / system from the gate rows and the run that produced them."""
    # `warn` (advisory) never blocks; `error` is a system failure, not the proposer's data.
    state = 'fix' if any(r['status'] == 'fail' for r in rows) else 'pass'
    if any(r['status'] in ('pending', 'error') for r in rows) or (run['conclusion'] != 'success' and state == 'pass'):
        return 'system'
    # A failed gate that did not run to completion is an incomplete run, not a finding.
    if any(r['status'] == 'fail' and r.get('ran') is not True for r in rows):
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
    text = texts.language(inspection.get('lang'))
    state = decide_state(rows, run)
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
              'recommendation': text[state] + text['human'] + ('\n' + text['lifecycle'] if lifecycle else '')
                                + (text['advisory'] if state == 'pass' and any(r['status'] == 'warn' for r in rows) else '')}
    return encode_report({'version': 1, 'repo': repo, 'pr': pr['number'], 'context': context(pr),
                          'runId': run['id'], 'runAttempt': gh.attempt(run),
                          'runUrl': f"https://github.com/{repo}/actions/runs/{run['id']}/attempts/{gh.attempt(run)}",
                          'toolsRef': inspection.get('toolsRef', ''), 'state': state, 'checks': rows, 'lifecycle': lifecycle,
                          'heading': text['heading'], 'labels': text['labels'], 'fields': fields})


def publish(repo, pr, analysis, comments):
    """Post the report of `analysis` for `pr`. The poster already checked that the run is the
    latest completed analysis of the PR's open head and that no other open PR shares the head;
    `comments` are the bot's comments it read."""
    number = pr['number']
    inspection = json.loads(Path('out/inspection.json').read_text())
    artifacts = {p.name: p.read_text(errors='replace') for p in Path('out').glob('*.md') if p.is_file() and not p.is_symlink()}
    files = gh.pages(f'/repos/{repo}/pulls/{number}/files')
    report = build_report(repo, pr, analysis, inspection, artifacts, files)
    if not gh.same_pr(repo, pr)[1]:
        raise ValueError('PR changed during publication')
    # One immutable comment per CI run/attempt. A retry repairs that comment;
    # it never replaces a different report to which a human already attested.
    # The ci-report check is review-report.yml's alone: it runs after this job
    # and judges the report this job posted.
    key = f"<!-- citygml-report-run:{analysis['id']}:{gh.attempt(analysis)} -->"
    existing = gh.find_comment(comments, REPORT_MARKER, key)
    gh.upsert_comment(repo, number, report_comment(report) + '\n' + key, existing)
