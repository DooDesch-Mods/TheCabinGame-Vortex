# the cabin game - Vortex Support

> 🛟 **Need help or found a bug?** Get support at [support.doodesch.de/thecabingame-vortex](https://support.doodesch.de/thecabingame-vortex).

Community extension by DooDesch for Steam on Windows, app ID `4406280`.
Version 0.1.1 passed Steam discovery, UE4SS installation, Chair Marker gameplay,
disable, re-enable and purge checks in Vortex 2.8.0. Nexus game mapping is pending.

## Install

1. Open **Extensions** in Vortex and drop this extension ZIP into the installation area.
2. Restart Vortex.
3. Find **the cabin game** under **Games** and select **Add game** (**Manage** in older versions).
4. Install a compatible gameplay mod and select **Deploy**.

For manual discovery, select the folder containing both files:

```text
the_cabin_game.exe
the_cabin_game/Binaries/Win64/the_cabin_game-Win64-Shipping.exe
```

Lua/native mods require a game-compatible UE4SS runtime. Follow the gameplay
mod's version requirement. The extension does not include or download UE4SS.

## Supported archives

- Loose or wrapped `.pak` files install into `the_cabin_game/Content/Paks/~mods`.
- `.utoc` and `.ucas` files must have matching names and ship together. Include the `.pak` companion when the mod build produces one.
- Game-root archives preserve `the_cabin_game/Content/Paks/...`, including `LogicMods`, and `the_cabin_game/Binaries/Win64/ue4ss/...`.
- `Mods/<ModName>/...` installs into `the_cabin_game/Binaries/Win64/ue4ss/Mods/<ModName>`.
- Separately supplied UE4SS bundles containing `dwmapi.dll` and `ue4ss/UE4SS.dll` retain their runtime layout.

Independent Lua/native mods need `enabled.txt` inside their mod folder.
Standalone mods that replace shared `mods.txt` or `mods.json` are rejected.
Mods requiring a specific loader order need a separately validated solution.
Use explicit game-root paths for `LogicMods`; PAK mount points are not inspected.

## Removal

Close the game. Disable a mod and select **Deploy** to remove its deployed files.
**Purge** removes files managed by Vortex. **Remove** deletes the staged mod.
Saves, logs and mod state generated during play remain outside Vortex's manifest.
Use the gameplay mod's uninstall guide for those files.

## Test limitations

Local-ID candidates cannot route the game's Nexus downloads. Final packages need
the approved Nexus game domain. The live test used Steam build 25553694,
UE4SS v3.0.1-1164-g5e627997 and Chair Marker 0.1.2. Manual discovery,
launch through Vortex, PAK mounting and Nexus download routing remain untested.

## License and source

Copyright (c) 2026 DooDesch. Extension code, tools and documentation use
GPL-3.0-only. See LICENSE.md. The game tile uses the original Steam library cover;
the package also includes an official Steam screenshot. Both are credited to
Twisted Corridor and excluded from the GPL license; image rights
remain with the respective rights holders. See [credits and image source](CREDITS.md).

Complete extension source and build tools:
[DooDesch-Mods/TheCabinGame-Vortex](https://github.com/DooDesch-Mods/TheCabinGame-Vortex).
For a published release, use the source tag or commit linked on its download page.
