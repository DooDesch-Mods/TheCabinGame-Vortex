# Mod archive authoring

Package a gameplay release in a layout supported by the Vortex extension.
The extension supplies installer support and packaging tools. Mod authors
choose their runtime requirements and license and validate their mod in the game.

## Archive layout

```text
Mods/ExampleMod/Scripts/main.lua
Mods/ExampleMod/enabled.txt
Mods/ExampleMod/dlls/main.dll
the_cabin_game/Content/Paks/~mods/ExampleMod_P.pak
the_cabin_game/Content/Paks/~mods/ExampleMod_P.utoc
the_cabin_game/Content/Paks/~mods/ExampleMod_P.ucas
README.md
LICENSE
```

This is a layout example, not a list of required payload files. Include only the
files produced and needed by the actual mod. Ship `.utoc`/`.ucas` as a matching
pair, with a `.pak` companion when the build produces one. Canonical game-root
UE4SS paths and pure PAK archives are also supported. Explicit game-root
`LogicMods` paths are preserved.

Declare the compatible UE4SS runtime as a separate requirement. Do not bundle
an unverified runtime. Include `enabled.txt` in each independent Lua/native mod
folder so it can activate without replacing shared `mods.txt`/`mods.json`.
Mods needing a particular loader order require a separately validated solution.

Vortex manages the supplied files. Saves, logs, and state generated while the
mod runs require their own documented lifecycle and uninstall behavior.

## Package and verify

From this repository:

```powershell
python tools/package-game-mod.py <release-payload-folder> --name ExampleMod --version 0.1.0
```

The tool adds missing independent activation markers, checks the actual
installer's routing, and writes a ZIP and SHA-256 receipt under `dist`.
It rejects known diagnostic scripts. Review the whole input folder before
packaging; the filename checks do not establish that every file is a release file.
Exclude test servers, probes, `command.lua`, `diagnostic.lua`, and `devbridge.lua`.

This validates packaging, not gameplay. Verify the mod's advertised behavior,
supported multiplayer/host cases, persistence, and uninstall behavior in the game.
Then test the exact ZIP through Vortex installation, deployment, disable,
re-enable and purge before its first Nexus upload.

