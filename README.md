# Nexus und Vortex für the cabin game

Vorbereitet am 10. Oktober 2026. Der Gameplay-Mod entsteht separat; diese
Integration ergänzt den Nexus-Spieleintrag und den Mod-Manager-Support.
Öffentliches Repo: https://github.com/DooDesch-Mods/TheCabinGame-Vortex

## Ergebnis

- Version 0.1.0: ZIP und Prüfnachweise werden als GitHub-Actions-Artefakte gebaut.
- [Spieleantrag](submission/game-request.md), [Vortex-Uploadfelder](submission/vortex-upload.md),
  [Summary](submission/vortex-summary.txt), [BBCode-Beschreibung](submission/vortex-description.bbcode),
  [Review-Vorlage](submission/review-issue.md).
- [Paketvertrag für die Mod-Session](MOD-HANDOFF.md) und überprüfbarer
  [Gameplay-Paketierer](tools/package-game-mod.py).
- [Step-by-Step-Guide](NEXUS-SETUP.md), [GitHub-Automation](publishing/README.md).
- Lokale Prüfnachweise bleiben unter `evidence`; sie sind kein öffentlicher Quellcode.

## Reihenfolge bis zur Veröffentlichung

1. Andere Session schließt den Gameplay-Mod samt In-game-Acceptance ab.
2. Mit diesem Mod bei Nexus `the cabin game` über **ADD NEW GAME** beantragen und
   den Erstupload fertigstellen. Nexus entscheidet über Freigabe und Domain.
3. Mit der echten Domain das finale Extension-Paket bauen:

   ```powershell
   python tools/build-extension.py --nexus-domain <actual-nexus-domain>
   ```

   Der Builder setzt im ZIP sowohl Game-ID als auch `nexusPageId`. Die Domain
   nicht raten. Eine bereits genutzte lokale Test-Game-ID bleibt in alten
   Vortex-Profilen gespeichert; für die endgültige ID ein neues Testprofil
   anlegen und den lokalen Kandidaten vorher entfernen.
4. Finales ZIP in Vortex importieren, Steam-Discovery/manuelle Erkennung und
   Start testen. Den akzeptierten Mod installieren, seine Wirkung im Spiel
   beobachten, deaktivieren, erneut aktivieren und purgen. Originaldateien
   und den von Vortex erfassten Dateibestand danach kontrollieren.
5. Extension unter Nexus Modding Tools, Kategorie **Vortex > Extensions** mit
   genau einer Main File hochladen. Die beiden echten URLs in die Review-Vorlage
   einsetzen und erst dann die Verifikation bei Nexus-Mods/Vortex-Backend einreichen.
6. Einen Nexus-Download über **Mod Manager Download** mit der realen Domain testen.

Der Upload erzeugt keinen automatischen Manifest-Eintrag. Das Nexus-Team prüft
die Erweiterung, bevor sie regulär in Vortex gelistet wird.

## Checks erneut ausführen

```powershell
node --test tests/extension.test.js
python -m pip install -r requirements.txt
python tools/build-extension.py
```

Auf diesem Rechner existieren alte Vortex-Daten, aber an den geprüften Standard-
und Registry-Pfaden wurde keine ausführbare Installation gefunden. Die
technischen Tests sind bestätigt; Vortex-UI, Steam-Start, Modwirkung im Spiel
und Nexus-Download sind offen. Nexus-Spiel-/Mod-/Extension-Uploads bleiben ausstehend.
Der öffentliche Integrationscode wird auf Wunsch über GitHub verwaltet.
Der Gameplay-Checkpoint wurde nicht verändert.

Die Lizenz entspricht ServerPasswordOnce: eigener DooDesch-Lizenztext,
Quellcode einsehbar und private Änderungen erlaubt; öffentliche Weiterverteilung
grundsätzlich nur mit schriftlicher Erlaubnis, mit der definierten Aufgabe-
Ausnahme. Siehe [LICENSE.md](LICENSE.md). GitHub-Forks für Beiträge sind erlaubt.

## Quellen

- [Nexus: neues Spiel hinzufügen](https://help.nexusmods.com/article/104-how-can-i-add-a-new-game-to-nexus-mods)
- [Nexus: Extension-Paket](https://github.com/Nexus-Mods/Vortex-Backend/wiki/How-to-package-a-game-extension)
- [Nexus: Review-Prozess](https://forums.nexusmods.com/topic/13480550-changes-to-how-we-review-community-game-extensions/)
- [Aktuelles Review-Formular](https://github.com/Nexus-Mods/Vortex-Backend/blob/main/.github/ISSUE_TEMPLATE/verify-extension.yaml)
- [Vortex API](https://github.com/Nexus-Mods/Vortex/blob/master/packages/vortex-api/README.md)
- [UE4SS-Aktivierungsmarker](https://docs.ue4ss.com/guides/installing-a-c%2B%2B-mod.html)
- [Offizielles Spiel](https://store.steampowered.com/app/4406280/the_cabin_game/)

Primärquellen-Abrufe und ihre Fehler liegen unter `evidence/sources`.
Die verlinkte Vortex-Backend-Test-Wiki-Seite lieferte 404, die Review-Wiki ist
ein Stub; das tatsächliche YAML-Formular ist vorhanden. Die Interpretation
stützt sich auf dieses Formular und die vollständigen Paket-/API-Quellen.
