# Gameplay mod packaging guide

Package a tested gameplay release in a layout supported by the Vortex extension.
Gameplay implementation, validation, and licensing remain the mod author's
responsibility; this repository supplies installer support and packaging tools.

## Archive layout

```text
Mods/CabinRejoin/Scripts/main.lua
Mods/CabinRejoin/enabled.txt
Mods/CabinRejoin/dlls/main.dll
the_cabin_game/Content/Paks/~mods/CabinRejoin_P.pak
the_cabin_game/Content/Paks/~mods/CabinRejoin_P.utoc
the_cabin_game/Content/Paks/~mods/CabinRejoin_P.ucas
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
python tools/package-game-mod.py <release-payload-folder> --name CabinRejoin --version 0.1.0
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

## First Nexus upload

Provide the accepted package, final name/version, accurate description,
requirements, license, and original screenshots. Once Nexus approves the game
section, use its actual domain to rebuild the extension:

```powershell
python tools/build-extension.py --nexus-domain <approved-domain>
```

The local ID `thecabingame` is provisional and is not a confirmed Nexus domain.

## Gameplay license

The gameplay mod retains the DooDesch license terms used for Valheim
ServerPasswordOnce. Adapt that project's license title, release channels, and
contact details while preserving its permissions and restrictions, subject to
the gameplay mod's own dependency licenses.

The Vortex extension is separately licensed under GPL-3.0-only. Its `LICENSE.md`
is not the gameplay license template. Installing a separate gameplay mod through
Vortex does not by itself apply the extension's license to that mod.
