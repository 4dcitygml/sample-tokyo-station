<!--
Copyright (c) 2026 4dcitygml
PR-Vorlage für Gebäudedaten in diesem Stadt-Repository.
Von den gemeinsamen Bearbeitungswerkzeugen erstellte PRs füllen die Begründung
automatisch aus; bei manuellen PRs sind "Zielgebäude / Umfang" und
"Zusammenfassung der Änderungen" das Minimum. Spezialabschnitte, die auf
alltägliche Korrekturen nicht zutreffen, können leer bleiben. Administrative
PRs (source-update usw.) müssen alle Pflichtabschnitte ausfüllen.
Sie reichen mit einem eigenen Werkzeug oder Skript ein? Der vollständige
Maschinenvertrag: https://github.com/4dcitygml/tools/blob/main/docs/exchange-contract.md
-->

## PR-Typ
<!-- Genau einen auswählen. Typen, deren eigene CI noch nicht umgesetzt ist, dürfen nicht als "Ready for review" markiert werden. -->
- [ ] `correction` (alltägliche Korrekturen an Attributen / Geometrie / Position / Texturen)
- [ ] `lifecycle` (Neubau, Teilung, Zusammenlegung)
- [ ] `identity-correction` (Korrektur einer falsch verknüpften ID in der veröffentlichten Historie)
- [ ] `source-update` (Übernahme einer amtlichen Quelle / Jahresedition)
- [ ] `semantic-correction` (nur unterstützte Pilotverfahren; erfordert die dafür freigegebene Tools-Version und Belege)
- [ ] `schema-update` (Ergänzung editionsspezifischer Artefakte und Validierungsprofile)
- [ ] `carry-forward` (Neubasierung der Repository-Änderungen auf eine neue offizielle Edition)
- [ ] `schema-migration` (registry-gesteuerte Neuserialisierung in eine neue Edition, wenn das Repository die Masterkopie ist)
- [ ] `layout` (semantikerhaltende Mesh-Unterteilung)
- [ ] `texture-gc`
- [ ] `revert`
- [ ] nur Dokumentation / Konfiguration (Code wird hier nicht angenommen — Werkzeuge bitte in `4dcitygml/tools` vorschlagen)

## Zielgebäude / Umfang
<!-- Die stabile Gebäude-ID (wie `building_id` in 4dcitygml.json sie festlegt) jedes betroffenen Gebäudes. Sammeleinreichungen (mit Herkunftsmanifest): eine ID pro Commit. Administrative PRs: Mesh oder Manifest angeben. -->
-

## Zusammenfassung der Änderungen <!--sec:reason-->
<!-- Pflichtfeld — die CI stuft den PR als "Begründung fehlt" ein, wenn dieser Abschnitt leer bleibt. Was wurde geändert und warum (Positionskorrektur / Höhenkorrektur / Texturersatz usw.), plus Beleg (amtliche Quelle, eigenes Foto vor Ort, ...), in 1-2 Zeilen. -->


## Art der Änderung
<!-- Alles Zutreffende ankreuzen. Im Zweifel die Situation unter "Sonstiges" beschreiben. -->
- [ ] Attributkorrektur (Geschosszahl, Nutzung, Fläche usw.)
- [ ] Geometriekorrektur (Form, Höhe, Dachform usw.)
- [ ] Positionskorrektur (Behebung eines Versatzes)
- [ ] Texturkorrektur (Ersatz, Schließen von Lücken usw.)
- [ ] Lebenszyklus (Zusammenlegung / Teilung / Neubau; umfasst Hinzufügen/Löschen)
- [ ] Sonstiges:

## Bildrechte
<!-- Pflicht, sobald der PR Fotos / Texturbilder hinzufügt oder ersetzt; andernfalls leer lassen. Siehe ../docs/de/data-contribution-policy.md (§1-§2). -->
- [ ] Jedes hinzugefügte Bild wurde **von mir selbst aufgenommen** (keine Fotos Dritter, keine Bilder aus dem Web oder aus sozialen Medien)
- [ ] Jedes Foto wurde von einem rechtlich zulässigen Standort aus aufgenommen (z. B. öffentliche Straße)
- [ ] Es sind keine erkennbaren Gesichter, Kfz-Kennzeichen, Namensschilder, Raum-Innenansichten oder ähnliche privatsphärerelevante Details verblieben (bei Bedarf maskiert / unkenntlich gemacht)
- [ ] Kein fremdes Werk (Schild, Plakat, Anzeige) ist Hauptmotiv eines Bildes
- [ ] Ich stelle die hinzugefügten Daten und Bilder gemäß der [Daten-Beitragsrichtlinie](../docs/de/data-contribution-policy.md) unter **CC0 1.0** bereit und verzichte bei Fotos zudem auf die Ausübung von Urheberpersönlichkeitsrechten (Zuschnitt, Perspektivkorrektur, Montage und Rekompression gehören zum Texturieren)

## Quelle / Manifest (source-update / schema / layout usw.)
<!-- Für alltägliche Korrekturen genügt der Beleg in der Zusammenfassung. Für die administrativen PR-Typen unten Pflicht. -->
- Source-From:
- Source-To:
- Scope-Mesh:
- Attribute-Family:
- Allowed-Paths:
- History-Manifest:
- Provenance-Manifest:
- Manifest-SHA256:
- Plan-Issue:
- Building-Count:
- First-Building-ID:
- Last-Building-ID:

## Checkliste
- [ ] Vom aktuellen main erstellt, ohne Konflikt mit früheren PRs auf demselben Mesh
- [ ] Bei normalen Updates gilt: **1 Commit = 1 Gebäude-ID**
- [ ] Bei normalen Updates sind Korrekturen an derselben buildingID nicht auf mehrere Commits des PRs verteilt
- [ ] Der `Building:`-Trailer (usw.) jedes Gebäude-Commits entspricht der tatsächlich geänderten buildingID
- [ ] Bei Sammeleinreichungen (mehrere Gebäude-Commits mit Herkunftsmanifest) wird der gesamte PR korrigiert, sobald ein einzelnes Gebäude eine blockierende CI-Prüfung nicht besteht
- [ ] Falls eine Geometrie-Vorschau angezeigt wurde, wurde das Erscheinungsbild mit 🔴 vorher / 🔵 nachher geprüft
- [ ] Bei Lebenszyklus-Änderungen steht der **Grund für Zusammenlegung / Teilung / Neubau** unter "Zusammenfassung der Änderungen"
- [ ] Bei Texturänderungen wird kein vorhandenes Bild **unter gleichem Namen überschrieben** (Ausnahme: `texture-override`)
- [ ] Ein zugehöriges Issue ist mit `Fixes #<Nummer>` oder `Refs #<Nummer>` verknüpft
- [ ] Bei einem PR ohne die Bearbeitungswerkzeuge wurde die zutreffende Checkliste im [Betriebshandbuch](../docs/operator-handbook.md) durchgesehen (der Vertrag selbst: [PR-Betriebsleitfaden](../docs/pr-operations.md))

## Verwandte Issues
<!-- Fixes, wenn der PR das Issue schließt; Refs, wenn nur verwandt. "None", falls keines. -->


## Ergänzende Hinweise (optional)
<!-- Belegdokumente, Quellen der korrekten Werte, Punkte, auf die Reviewer achten sollen. -->
