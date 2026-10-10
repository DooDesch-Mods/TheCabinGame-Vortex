# the cabin game — Vortex support 0.1.0

Community extension by DooDesch. Steam Windows version, app 4406280.

Install this archive through Vortex's Extensions page (drop the ZIP onto the
installation area), then restart Vortex. Find **the cabin game** in Games and
select Manage. If discovery does not find it, select the folder containing
`the_cabin_game.exe`, usually `steamapps/common/the cabin game`.

Supported archives:

- Loose or wrapped `.pak` files go into `the_cabin_game/Content/Paks/~mods`.
- `.utoc` and `.ucas` files must ship together with matching names. Their names
  are preserved. Include the `.pak` companion when the mod's build produces one.
- Game-root archives preserve `the_cabin_game/Content/Paks/...` paths, including
  `LogicMods`, and `the_cabin_game/Binaries/Win64/ue4ss/...` paths.
- `Mods/<ModName>/...` archives go into
  `the_cabin_game/Binaries/Win64/ue4ss/Mods/<ModName>/...`.
- A separately supplied modern UE4SS runtime archive containing `dwmapi.dll`
  and `ue4ss/UE4SS.dll` can be installed through the same route. The runtime is
  not included or downloaded automatically by this extension.

Independent Lua/native mods must include `enabled.txt` in their mod folder.
The supplied packaging tool can add this marker. The extension rejects a
standalone mod that replaces shared `mods.txt`/`mods.json`. Mods requiring a
specific loader order need an explicit authored solution before distribution.

Disable a mod and Deploy to remove its deployed files. Purge removes managed
files from the game; Remove deletes the staged mod. User saves are not an
installation target. Files created by the game/loader while running, such as
logs and mod state, remain outside Vortex's deployment manifest.

This preparation build uses a local game ID. Nexus download links require the
real Nexus game domain to be configured after the game entry is created. The
code and isolated filesystem deployment have been checked; testing in Vortex
and in the running game remains pending. No reconnect functionality is supplied
by this extension. The gameplay mod is developed separately.

Code/art license: the DooDesch custom source-available license, matching ServerPasswordOnce. `gameart.png` is original illustrative artwork,
not an official game screenshot or logo. See LICENSE.md and CREDITS.md.
