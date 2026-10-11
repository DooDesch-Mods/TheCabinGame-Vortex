# the cabin game - Vortex Support

> 🛟 **Need help or found a bug?** Get support at [support.doodesch.de/thecabingame-vortex](https://support.doodesch.de/thecabingame-vortex).

[![Check and build](https://github.com/DooDesch-Mods/TheCabinGame-Vortex/actions/workflows/ci.yml/badge.svg)](https://github.com/DooDesch-Mods/TheCabinGame-Vortex/actions/workflows/ci.yml)

Community game support for the Steam Windows version of **the cabin game**.
Discover the game and manage PAK, IoStore and UE4SS mod files through Vortex.

**Status:** `0.1.1` passed Steam discovery, original UE4SS installation,
Chair Marker gameplay, disable, re-enable and purge checks in Vortex 2.8.0.
Nexus game mapping and public extension review are pending. Use the test build below.

## Requirements

- [the cabin game on Steam](https://store.steampowered.com/app/4406280/the_cabin_game/) for Windows, app ID `4406280`.
- [Vortex for Windows](https://www.nexusmods.com/site/mods/1), tested with version `2.8.0`.
- A game-compatible [UE4SS runtime](https://github.com/UE4SS-RE/RE-UE4SS) for Lua/native mods. Use the version required by the gameplay mod.

Install gameplay mods and UE4SS separately. The extension does not download a
runtime or choose its version for you.

## Install a test build

1. Open a successful [Check and build run](https://github.com/DooDesch-Mods/TheCabinGame-Vortex/actions/workflows/ci.yml) and download **vortex-package**.
2. Extract the artifact ZIP. The inner extension ZIP is the installable file.
3. In Vortex, open **Extensions**, drop that ZIP into the installation area, and restart Vortex.
4. Open **Games**, find **the cabin game**, and select **Add game** (**Manage** in older versions).
5. Install a compatible gameplay mod and select **Deploy**.

Builds without the approved Nexus domain use a local game ID. They cannot route
the game's Nexus downloads. A changed final game ID needs a new Vortex test profile.

The live test used Steam build `25553694`, UE4SS `v3.0.1-1164-g5e627997` and
Chair Marker `0.1.2`. All 23 deployed files matched their archives. Purge removed
those files and preserved the 26 recorded original game files. Manual discovery,
launch through Vortex, PAK mounting and Nexus download routing still need live checks.

## Game detection

Vortex searches Steam for app `4406280`. If discovery fails, select the game
folder manually. That folder must contain both files:

```text
the_cabin_game.exe
the_cabin_game/Binaries/Win64/the_cabin_game-Win64-Shipping.exe
```

## Supported mods

Paths below are relative to the game folder.

| Archive layout | Installed location |
|---|---|
| Loose or wrapped `.pak` files | `the_cabin_game/Content/Paks/~mods` |
| Matching `.utoc` and `.ucas` files | Same folder; filenames are preserved |
| Game-root `the_cabin_game/Content/Paks/...` | Original path, including `LogicMods` |
| Game-root `the_cabin_game/Binaries/Win64/ue4ss/...` | Original path |
| `Mods/<ModName>/...` | `the_cabin_game/Binaries/Win64/ue4ss/Mods/<ModName>` |

Independent Lua/native mods need `enabled.txt` inside their mod folder. Standalone
mods must not replace the shared `mods.txt` or `mods.json`. Explicit game-root
paths are required for `LogicMods`; the extension does not inspect PAK mount points.
See the [mod author guide](docs/mod-author.md) for archive examples and the packaging tool.

## Disable or remove mods

Close the game before changing deployed files. Disable a mod and select **Deploy**
to remove its deployed files. **Purge** removes all files managed by Vortex.
**Remove** deletes the mod's staged copy. Generated saves, logs and mod state
remain outside the deployment manifest. Follow the gameplay mod's uninstall guide.

## Troubleshooting

| Problem | Check |
|---|---|
| Game is not detected | Select the folder containing both files listed under Game detection. |
| IoStore archive is rejected | Include matching `.utoc` and `.ucas` files from the same mod build. |
| UE4SS archive is rejected | Use `Mods/<Name>/...` or game-root paths and include `<Name>/enabled.txt`. |
| Mod installs but has no effect | Check the mod's game/runtime requirements and its current loader log. PAK mounting still needs live validation. |

For unresolved problems, use the support link above. Include your extension,
Vortex, game and UE4SS versions, the archive's file list, the error text, and
steps to reproduce the problem.

## Development

Use Windows, Node.js 24 and Python 3.13.

```powershell
python -m pip install -r requirements.txt
node --test tests/extension.test.js
python tools/build-extension.py
python tools/verify-tooling.py
python tests/test_release.py
python tests/test_release_notes.py
```

The builder writes an extension ZIP and SHA-256 receipt under `dist`. To configure
both packaged game mappings, pass `--nexus-domain <approved-domain>`. Do not guess
the domain. Changing the local game ID requires a new Vortex test profile.

Automated checks cover installer rules, isolated hardlink deployment, packaging,
document links and release guards. They do not establish live game compatibility.
See [GitHub publishing](docs/releases.md) for the release workflow.
Pull requests are welcome in this repository.

To prepare the images, run `python tools/prepare-artwork.py`. It checks the
official Steam source hashes, copies the 600x900 library cover without changes,
and resizes the screenshot for the required 640x360 package thumbnail.
The game registration uses `cover.jpg` for Vortex's portrait tiles.
Use `--source <screenshot.jpg> --cover-source <cover.jpg>` to supply both originals locally.

## License and credits

Copyright (c) 2026 DooDesch. Extension code, tools and documentation use
[GPL-3.0-only](LICENSE.md). Redistribution and modification are allowed under its
terms. The official Steam library cover and screenshot are credited to
Twisted Corridor and excluded from the GPL license. See
[credits and image source](extension/CREDITS.md).

This is an unofficial extension for the game developed and published by Twisted
Corridor. No game code or UE4SS binaries are included. Gameplay mods retain their
own licenses.
