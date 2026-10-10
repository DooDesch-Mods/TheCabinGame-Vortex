# Vertrag für die Gameplay-Mod-Session

Ziel: Der Gameplay-Mod liefert den ersten nutzbaren Upload für den neuen
Nexus-Spieleintrag. Diese Session besitzt nur `integrations/nexus-vortex`;
`STATE.md`, `tools/runtime`, `tools/static` und der Gameplay-Mod bleiben beim
bisherigen Owner. Kein Gameplay-Paket wurde hier verändert oder veröffentlicht.

Bevorzugte Archivstruktur (wie bei Palvolve, aber Cabin-Pfade):

```text
Mods/CabinRejoin/Scripts/main.lua
Mods/CabinRejoin/enabled.txt
Mods/CabinRejoin/dlls/main.dll            # nur falls tatsächlich benötigt
the_cabin_game/Content/Paks/~mods/CabinRejoin_P.pak
the_cabin_game/Content/Paks/~mods/CabinRejoin_P.utoc
the_cabin_game/Content/Paks/~mods/CabinRejoin_P.ucas
README.md
LICENSE
```

Nur benötigte Dateien ausliefern. `.utoc`/`.ucas` nur gemeinsam, falls der Build
sie produziert. Canonical game-root UE4SS-Pfade und reine PAK-Archive funktionieren
ebenfalls. `LogicMods` wird bei explizitem game-root Pfad beibehalten. Loader
als eigene Requirement angeben; keinen Runtime-Build erfinden oder ungeprüft
mit ausliefern. Der aktuell diagnostizierte experimentelle Build ist kein
allgemeines Kompatibilitätsversprechen.

`enabled.txt` aktiviert unabhängige Mods, ohne die gemeinsame `mods.txt` zu
überschreiben. Falls der Mod eine feste Loader-Reihenfolge braucht, reicht der
Marker nicht: diese Anforderung separat lösen. Vortex verwaltet ausschließlich
die gelieferten Dateien, keine vom Mod erzeugten Speicherstände/Logs.

Release-only Payload mit folgendem Runner paketieren; dieser ergänzt fehlende
Marker und prüft die tatsächliche Vortex-Dateizuordnung vor dem ZIP-Bau:

```powershell
python tools/package-game-mod.py <release-payload-folder> --name CabinRejoin --version 0.1.0
```

Der Runner testet Paketstruktur, keine Rejoin-Spiellogik. Keine Diagnoseordner,
Testserver, `command.lua`, `diagnostic.lua`, `probes.lua` oder `devbridge.lua`
als Release-Payload verwenden.

Die vorhandene Rejoin-Acceptance (einschließlich Host-Fall) bleibt verbindlich.
Vor dem ersten Nexus-Upload werden gebraucht: akzeptiertes Paket, finaler Name
und Version, ehrliche Funktionsbeschreibung, Requirements, Lizenz und eigene
Gameplay-Screenshots. Danach tatsächlichen Nexus-Spiel-Domain zurückmelden;
die Erweiterung kann dann mit `build-extension.py --nexus-domain <domain>`
passend gebaut werden. Keine Kommunikation an die andere Session wurde versendet.

Lizenzvorgabe vom Nutzer: wie Valheim ServerPasswordOnce. Den eigenen
DooDesch-Lizenztext verwenden; keine GPL/MIT-Vorlage übernehmen. Der Lizenztext
dieser Erweiterung liegt unter `LICENSE.md`; für den Gameplay-Mod Titel,
offizielle Releasekanäle und Kontakt passend anpassen, dieselben Rechte und
Einschränkungen erhalten. Der Gameplay-Owner muss dies in seinem Repo umsetzen.
