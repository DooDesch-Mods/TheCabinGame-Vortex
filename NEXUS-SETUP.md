# Step by Step: Nexus und GitHub

Stand 10. Oktober 2026. Erweiterung vorbereitet; Gameplay-Mod und reale
Vortex-/Spielprüfung stehen noch aus. Das erste Anlegen der Nexus-Seiten und
die Freigabe durch Nexus sind einmalig; spätere Dateiversionen können über
GitHub Actions veröffentlicht werden.

## 1. Gameplay-Mod abschließen

Die andere Session liefert das akzeptierte Release-ZIP, Version, Requirements,
Beschreibung und eigene Screenshots. Ein technisch noch ungeprüfter Prototyp
erfüllt Nexus' Voraussetzung eines nutzbaren Mods nicht. Der
[Paketvertrag](MOD-HANDOFF.md) hilft bei der Vortex-kompatiblen Struktur.

Lizenz für Gameplay-Mod und Erweiterung: wie **Valheim ServerPasswordOnce**.
Eigener DooDesch-Lizenztext, Quellcode einsehbar/private Änderungen erlaubt,
öffentliche Weiterverteilung grundsätzlich nur mit schriftlicher Erlaubnis,
mit der im Text definierten Ausnahme bei Aufgabe. Siehe [LICENSE.md](LICENSE.md).

## 2. Spieleintrag anlegen und ersten Mod hochladen

1. Bei [Nexus Mods](https://www.nexusmods.com/) als DooDesch anmelden.
2. Allgemeinen **Upload a mod**-Dialog öffnen.
3. In der Spielauswahl `the cabin game` und `The Cabin Game` suchen.
4. Falls nicht vorhanden: **ADD NEW GAME**, offiziellen Steam-Titel
   `the cabin game` eintragen, danach **ADD GAME**.
5. Den fertigen Gameplay-Mod hochladen: Name/Version aus seiner Session,
   Kategorie gemäß Funktion, Summary/Beschreibung, Requirements, Bilder und
   Lizenz-Permissions. ZIP als **Main File** und Mod-Manager-Download auswählen.
6. Upload abschließen. Nexus prüft und entscheidet über den neuen Spielebereich.

[Vorbereitete Spieldaten](submission/game-request.md). Laut
[Nexus-Hilfe](https://help.nexusmods.com/article/104-how-can-i-add-a-new-game-to-nexus-mods)
muss ein nutzbarer Mod vorhanden sein. Nach mehr als sieben Werktagen ohne
Freigabe nennt Nexus Support als Kontakt; hier wird keine Nachricht versendet.

## 3. Tatsächliche Nexus-Werte notieren

Nach Erstellung/Freigabe benötigt die Automation:

| Wert | Woher |
|---|---|
| Game-Domain | Tatsächlicher Pfad des neuen Spielebereichs: `nexusmods.com/<domain>` |
| Gameplay-Mod-URL | Seite des ersten Mods |
| Gameplay-Datei-Gruppen-ID | **Files → API Info**, in der aktuellen Oberfläche ggf. unter **Advanced**, oder Manage Files → Edit |

Die Nummer am Ende der Mod-URL ist **nicht** die Datei-Gruppen-ID. Domain
nicht raten. Die Vortex-Erweiterung hat anschließend eine eigene Datei-ID.
Offizielle Erklärung: [Nexus Upload Action](https://github.com/Nexus-Mods/upload-action).

## 4. Vortex-Paket mit echter Domain bauen

Im [GitHub-Repo](https://github.com/DooDesch-Mods/TheCabinGame-Vortex) unter
**Settings → Secrets and variables → Actions → Variables → New repository variable**
`NEXUS_GAME_DOMAIN` auf die echte Game-Domain setzen.

Danach **Actions → Check and build → Run workflow** starten. Sobald grün,
das Artefakt **vortex-package** herunterladen und entpacken. Darin liegt das
Extension-ZIP `TheCabinGame-Vortex-0.1.0.zip` samt Prüfnachweis. Das äußere
GitHub-Artefakt-ZIP wird nicht in Vortex/Nexus installiert.

Alternativ lokal im Repo bauen:

```powershell
python -m pip install -r requirements.txt
python tools/build-extension.py --nexus-domain <actual-domain>
```

## 5. In Vortex und im Spiel prüfen

1. Vortex öffnen, **Extensions** wählen, Extension-ZIP auf den Installationsbereich
   ziehen und Vortex neu starten.
2. Unter **Games** nach `the cabin game` suchen und **Manage** wählen. Bei
   manueller Erkennung den Ordner mit `the_cabin_game.exe` auswählen.
3. Fertigen Gameplay-Mod installieren und **Deploy** ausführen.
4. Spiel starten und die tatsächliche Modwirkung prüfen; bei UE4SS muss der
   Mod im aktuellen Loader-Log geladen sein, PAK-Inhalte müssen im Spiel wirken.
5. Spiel schließen, Mod deaktivieren und Deploy: Dateien und Wirkung weg.
   Erneut aktivieren/Deploy: Wirkung wieder da. **Purge**: nur verwaltete
   Moddateien weg, Originaldateien erhalten. Spielstände gemäß Mod-Anleitung prüfen.

Die vorhandenen 21 technischen Tests ersetzen diese Prüfung nicht.

## 6. Vortex-Erweiterung einmalig bei Nexus hochladen

1. [Modding Tools](https://www.nexusmods.com/site) öffnen → Upload.
2. Kategorie **Vortex > Extensions**.
3. Name `the cabin game - Vortex Support`, Version `0.1.0`.
4. [Summary](submission/vortex-summary.txt), [BBCode-Beschreibung](submission/vortex-description.bbcode)
   und [Uploadfelder](submission/vortex-upload.md) verwenden. Den Draft-
   Status durch tatsächlich geprüfte Vortex-Version/Spielbuild/Testgrenzen ersetzen.
5. `extension/gameart.png` als Bild; dasselbe Bild wie in der Erweiterung.
6. Finale Extension-ZIP als **eine** Main File hochladen; Version exakt wie
   `extension/info.json`. License/Permissions wie ServerPasswordOnce.
7. Erweiterungs-URL und eigene **API Info Datei-Gruppen-ID** notieren.

[Offizielle Paketregeln](https://github.com/Nexus-Mods/Vortex-Backend/wiki/How-to-package-a-game-extension).

## 7. Nexus-Dateiupdates aktivieren

Im Extension-Repo unter **Settings → Secrets and variables → Actions → Variables**:

| Variable | Inhalt |
|---|---|
| `NEXUS_GAME_DOMAIN` | Domain des Spiels, obwohl die Extension selbst unter `/site` liegt |
| `NEXUS_FILE_GROUP_ID` | API-Info-Gruppen-ID der **Extension**-Main-File |
| `NEXUS_LIVE_TESTED` | `true`, nachdem Schritt 5 erfolgreich geprüft ist |

Der vorhandene Org-Secret **NEXUSMODS_API_KEY** hat Sichtbarkeit `all` und ist
damit für das neue Repo verfügbar. Den Schlüssel weder ins Repo noch in den
Chat kopieren. Falls er später fehlt: unter GitHub Actions Secrets im Repo/Org
setzen; Quelle [Nexus API Keys](https://www.nexusmods.com/settings/api-keys).

Die Gameplay-Mod erhält in ihrem eigenen Repo ihre eigene Datei-Gruppen-ID.
Eine [Workflow-Vorlage](publishing/gameplay-publish.example.yml) liegt hier bereit;
ihre Build-/Release-Dateinamen müssen vom Gameplay-Owner angepasst werden.

## 8. Vortex-Review anfordern

Das [Review-Formular](https://github.com/Nexus-Mods/Vortex-Backend/issues/new?template=verify-extension.yaml)
öffnen. [Vorbereitete Antworten](submission/review-issue.md) verwenden und
echte Extension-/Game-URLs einsetzen. Verpackung und Live-Test nur bestätigen,
wenn tatsächlich erledigt. Danach entscheidet Nexus über die Manifestaufnahme.

## 9. Künftige Updates über GitHub veröffentlichen

1. Code ändern, `extension/info.json` auf z.B. `0.1.1` erhöhen, Commit pushen.
2. Grüne **Check and build**-Prüfung abwarten.
3. **Releases → Draft a new release**, Tag `v0.1.1`, Änderungen beschreiben.
4. **Publish release**. Der Workflow testet den Code vom Tag, baut die ZIP,
   hängt sie samt Prüfnachweis an den GitHub-Release und lädt die neue
   Dateiversion bei Nexus hoch. Alte Nexus-Version wird archiviert, die neue
   als primärer Mod-Manager-Download gesetzt.
5. Grünen Workflow und bestätigte Nexus-Version-ID prüfen; Download einmal testen.

Der erste manuelle Nexus-Upload ist bereits `0.1.0`; nicht denselben Release
nochmals automatisiert als neue Nexus-Version veröffentlichen. Mit `0.1.1`
oder dem nächsten tatsächlichen Update beginnen. Bei Uploadfehlern vor Retry
die Nexus-Dateiversion prüfen: Ein Timeout beweist nicht, dass nichts ankam.

## Was bleibt einmalig/manuell?

Spieleantrag, Erstupload beider Seiten, Live-Test, tatsächliche IDs/Domain,
Vortex-Review, Bilder/Seitenbeschreibung und gewählte Permissions. CI/Build,
GitHub-Release-Dateien und spätere Nexus-Dateiupdates sind automatisierbar.
