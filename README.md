# the cabin game — Vortex Support

Community Vortex extension for the Steam Windows version of **the cabin game**
(app ID `4406280`), maintained by DooDesch.

Discover the game, install PAK/IoStore and UE4SS mod archives, and manage their
files through Vortex deployment, disable and purge.

## Release status

Version `0.1.0` is a preparation build. Installer checks and isolated filesystem
deployment have passed. Live Vortex/game validation, the approved Nexus game
domain, the first Nexus upload and extension review are still required.
CI produces a local test candidate until the real domain is configured.
Stable releases require the real domain and confirmed live acceptance.

This extension supplies game support. Gameplay mods and the UE4SS runtime
are separate downloads; follow each mod's compatibility requirements.

## Install

1. Obtain the extension ZIP from an official release, or build a test candidate
   using the instructions below. Extract the outer GitHub Actions artifact ZIP
   first; install the inner extension ZIP.
2. In Vortex, open **Extensions**, drop the extension ZIP onto the installation
   area, and restart Vortex.
3. Open **Games**, find **the cabin game**, and select **Manage**. If discovery
   fails, select the game folder containing `the_cabin_game.exe`.
4. Install a compatible gameplay mod and select **Deploy**.

See the [packaged user guide](extension/README.md) for supported layouts,
UE4SS activation markers, and removal behavior.

## Supported archives

| Layout | Destination |
|---|---|
| Loose or wrapped `.pak` files | `the_cabin_game/Content/Paks/~mods` |
| Matching `.utoc` / `.ucas` pairs | Same destination; names are preserved |
| Game-root `the_cabin_game/Content/Paks/...` | Original path, including `LogicMods` |
| Game-root `the_cabin_game/Binaries/Win64/ue4ss/...` | Original path |
| `Mods/<ModName>/...` | `the_cabin_game/Binaries/Win64/ue4ss/Mods/<ModName>` |

Independent UE4SS Lua/native mods must include `enabled.txt` in their mod folder.
The installer rejects unsafe paths, destination collisions, incomplete IoStore
pairs, base-game container replacements, and unsupported archive layouts.
It also rejects standalone mods that replace shared `mods.txt`/`mods.json`.

## Build and check

Prerequisites: Windows, Node.js 24, and Python 3.13.

```powershell
python -m pip install -r requirements.txt
node --test tests/extension.test.js
python tools/build-extension.py
python tools/verify-preparation.py
python tests/test_release.py
```

The default build creates `dist/TheCabinGame-Vortex-0.1.0-local-candidate.zip`
and a JSON receipt containing its SHA-256 and configuration. To build with the
approved Nexus domain:

```powershell
python tools/build-extension.py --nexus-domain <approved-domain>
```

The builder sets both the game ID and Nexus mapping in the ZIP. Do not guess the
domain. Switching from the local ID requires a new Vortex test profile.

The tests cover installer contracts and hardlink deployment in isolated fixtures.
They do not establish live game discovery, game launch, PAK mounting, UE4SS
activation, or Nexus download routing.

## Publishing and contributing

- [Nexus setup and release guide](NEXUS-SETUP.md)
- [GitHub publishing workflow](publishing/README.md)
- [Gameplay mod packaging guide](MOD-HANDOFF.md)
- [New-game submission](submission/game-request.md)
- [Extension upload fields](submission/vortex-upload.md)
- [Nexus review checklist](submission/review-issue.md)

Report bugs or submit pull requests in the
[GitHub repository](https://github.com/DooDesch-Mods/TheCabinGame-Vortex).
Include the extension and Vortex versions, archive layout, observed behavior,
and reproduction steps. Include live-game evidence for compatibility claims.

## License and credits

Copyright (c) 2026 DooDesch. This repository's extension, tools, documentation,
and original cabin illustration are licensed under **GPL-3.0-only**.
Modification and redistribution, including commercial redistribution, are
allowed under the GPL terms. Preserve required notices and provide corresponding
source. See [LICENSE.md](LICENSE.md) and [credits](extension/CREDITS.md).

The separate gameplay mod retains its own license. No game code, game assets,
screenshots, or UE4SS binaries are included. This is an unofficial community
extension for the game developed and published by Twisted Corridor.
