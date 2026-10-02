<!-- Copyright (c) 2026 4dcitygml -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# Datenbeitragspolitik (Attribute, Geometrie, Texturen, Fotos)

> Deutsche Übersetzung des englischen Originals: [../data-contribution-policy.md](../data-contribution-policy.md).
> Bei Abweichungen gilt das englische Original.

Status: v2 (v1 "Foto-Beitragspolitik" auf alle Datenbeiträge erweitert)

Diese Richtlinie regelt die Rechte bei **Beiträgen zu den Datendateien dieses Repositorys (CityGML und Textur-Bilder in den Daten-Verzeichnissen)**. Durch die Einreichung eines Pull Requests, der Daten ändert, stimmt der Einreicher dieser Richtlinie zu (die Bearbeitungs-Werkzeuge zeichnen diese Zustimmung im Pull-Request-Body auf).

Diese deutsche Fassung ist eine Übersetzung zum Verständnis. Bei Abweichungen gilt die englische Fassung ([docs/data-contribution-policy.md](../data-contribution-policy.md)).

## 1. Alle Datenbeiträge sind CC0 1.0

- Einreicher stellen ihre Datenbeiträge (Attributwerte, Geometrie-Fixes, Texturen, Fotos) unter **[CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/)** (Gemeingut-Widmung) zur Verfügung, soweit irgendwelche Rechte darin entstehen überhaupt.
- Korrektionen zu Attributwerten (Geschosszähler, Nutzungscodes, Überschwemmungstiefen, …) und Geometrie (Koordinaten) sind **Fakten / Daten** und sind normalerweise nicht urheberrechtlich geschützt überhaupt. Diese Klausel ist eine Erklärung auf der Sicherheitsseite ("selbst wenn Rechte irgendwie entstehen, sind sie CC0") — der gleiche Ansatz, den Wikidata für strukturierte Daten verfolgt.
- Fotos sind unabhängig urheberrechtlich geschützte Werke. Einreicher stimmen daher auch zu, **moralische Rechte nicht auszuüben** (die in einigen Rechtsprechungen nicht aufgegeben oder übertragen werden können, z. B. unter japanischem Gesetz). Texturierung umfasst Zuschneidung, Perspektiv-Korrektur, Zusammenstellung und Neukomprimierung, daher ist diese Zustimmung zur Änderung wesentlich.
- **Beiträge zu Code und Dokumentation sind außerhalb dieser Richtlinie.** Sie folgen der Repository-Lizenz (Apache-2.0) über die GitHub-Nutzungsbedingungen (D.6 inbound = outbound), wie üblich.
- Die Daten-Verteilung des Repositorys als Ganzes behält die Lizenz seiner offiziellen Quelle (siehe das Repository-README und `4dcitygml.json`; z. B. CC BY 4.0 für PLATEAU-abgeleitete Daten). Die Integration von CC0-Material steht im Konflikt damit nicht.

## 2. Zusätzliche Bedingungen für die Einreichung von Fotos

1. Das Foto muss **von Ihnen selbst aufgenommen** worden sein (keine Fotos von anderen, keine Bilder aus dem Web oder sozialen Medien).
2. Es muss **von einem rechtmäßigen Ort wie einer öffentlichen Straße** aufgenommen werden.
3. **Datenschutz und persönliche Informationen**: Fotos, in denen folgende erkannt werden, sollten vermieden oder diese Teile maskiert / unschärfe werden, bevor Sie eingereicht werden:
   - Gesichter oder Erscheinung von Menschen (Passanten, Bewohner)
   - Fahrzeug-Kennzeichen
   - Namensschilder, Rauminterieurs, Wäsche und ähnliche Spuren des täglichen Lebens
4. **Fremdliche Werke im Frame**: Lokales Urheberrecht ermöglicht normalerweise die Fotografieren von Gebäude-Außenseiten und erlaubt *beiläufige* Einbeziehung von Zeichen, Plakaten und Displays (in Japan: Artikel 46 und 30-2 des Urheberrechts-Gesetzes). Vermeiden Sie Fotos, bei denen solche Werke das Hauptthema sind.

Der Textur-Editor fordert eine ausdrückliche Zustimmungs-Überprüfung beim Erstellen eines Pull Requests an (Fotos sind wesentliche urheberrechtlich geschützte Werke, daher ist Zustimmung ausdrücklich). Der Attribut-Editor zeichnet die Zustimmung im Pull-Request-Body ohne ein Kontrollkästchen auf — **Reibung ist proportional zum Rechts-Risiko** nach Design.

## 3. Aufzeichnung und Ehrung von Beiträgen (unabhängig vom Urheberrecht)

- Beiträge werden dauerhaft im Git-Verlauf aufgezeichnet (Commit-Autor und der `Building:` Trailer). `git log --grep "Building: <id>"` und Autoren-Aggregation können verfolgen, wer zu welchem Building beigetragen hat.
- Visualisierung und Ehrung von Beiträgen basierend auf dieser Aufzeichnung (Beitragendenlisten, Urkunden der Wertschätzung, …) kann unabhängig von Urheberrecht-Eigentum betrieben werden.

## 4. Anforderung zur Entfernung

- Falls ein Datenschutz- oder Persönlichkeitsrechts-Problem in einem Bild nach der Tatsache entdeckt wird, bitte teilen Sie es uns in einem Issue mit. Wir werden es schnell aus den aktuellen Daten entfernen.
- Aufgrund wie Git funktioniert, **Daten bleiben in der vergangenheit Geschichte selbst nach Entfernung**. Für ernste Fälle mit Persönlichkeitsrechten oder Datenschutz werden die Maintainer Gegenmaßnahmen einschließlich Entfernung aus der Geschichte (Geschichte Umschreiben) in Betracht ziehen.

---

## Anhang: Entscheidungs-Datensatz

Zusammenfassung der Überlegungen, als diese Richtlinie angenommen wurde (behalten Sie für Transparenz).

**Vergleichende Ansätze**:

| Ansatz | Beispiel | Bewertung |
|---|---|---|
| Platform-Lizenz (Beitragende behält Urheberrecht, erteilt dem Betreiber eine breite Lizenz) | Google Maps-Bewertungen | Passt zu einem einzelnen Betreiber's Display-Use, aber Zuschreibungs-Verwaltung bleibt für Open-Data-Umverteilung |
| Kollektive Zuschreibung (Bedingungen erteilen Rechte an eine Stiftung, kollektive "© Beitragende" Hinweis) | OpenStreetMap | Solide Track-Record, aber schwere Bedingungen Dokumente und Operationen |
| **CC0 (Faktendaten der Öffentlichkeit widmet)** | **Wikidata** | **Angenommen.** Downstream-Benutzer (Gemeinden, Forscher, Unternehmen) können die Daten ohne Pro-Foto-Zuschreibungs-Verwaltung nutzen |

**Entscheidende Faktoren**:

1. **Vermeidung von Zuschreibungs-Stapelung** — Pro-Foto CC BY würde bedeuten, dass dauerhaft Zuschreibung für jede Textur in NOTICE-Dateien verwaltet wird, was in Ordnern mit offiziellen Quell-Texturen zusammengebrochen.
2. **Moralische Rechte** — in einigen Rechtsprechungen (z. B. Japan, Urheberrechts-Gesetz Art. 59) können sie nicht aufgegeben oder übertragen werden, daher ist ausdrückliche Nicht-Ausübungs-Zustimmung auf CC0 hinzugefügt (Texturierung ändert das Werk, daher muss das Integritäts-Recht adressiert werden).
3. **Erweiterung auf Attribute und Geometrie (v2)** — Faktendaten sind nicht urheberrechtlich geschützt, daher ist die Erklärung größtenteils ein No-Op, aber es kostet nichts und entfernt Mehrdeutigkeit. Begrenzt auf **Datenbeiträge** (Erweiterung von CC0 auf Code würde mit dem Apache-2.0-Schema konfligieren).
4. **Reibungs-Design** — ausdrückliche Zustimmung (Kontrollkästchen) nur für wesentliche Werke (Fotos); Attribut-Änderungen erhalten nur automatische Hinweise im Pull-Request-Body.
5. **Ehre ist unabhängig vom Urheberrecht** — der Git-Verlauf (Autor, `Building:` Trailer) funktioniert als doppelter Beitragendenliste, daher bleibt "wessen Beitrag" rückverfolgbar selbst unter CC0.
