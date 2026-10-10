# Nexus setup and release guide

This guide covers the first Nexus game entry, extension upload, live validation,
and subsequent GitHub-driven updates. The extension is currently a preparation
build; complete the live checks before publishing a stable release.

## 1. Prepare the first gameplay mod

Prepare a usable, tested gameplay mod with a release ZIP, version, requirements,
description, license, and your own gameplay screenshots. See the
[packaging guide](MOD-HANDOFF.md) for archive layouts.

The gameplay mod uses the separate DooDesch license based on Valheim
ServerPasswordOnce. Adapt that project's text for the gameplay mod.
The Vortex extension, tools, documentation and original illustration use
[GPL-3.0-only](LICENSE.md). The extension license is not the gameplay mod template.

## 2. Create the Nexus game entry

1. Sign in to [Nexus Mods](https://www.nexusmods.com/) as DooDesch.
2. Open **Upload a mod** and search for both `the cabin game` and `The Cabin Game`.
3. If the game is absent, select **ADD NEW GAME**, enter the official title
   `the cabin game`, and select **ADD GAME**.
4. Upload the tested gameplay mod with its correct category, description,
   requirements, screenshots, and license permissions. Upload its ZIP as a
   **Main File** with Mod Manager download enabled.
5. Complete the upload and wait for Nexus to approve the new game section.

Use the [prepared game details](submission/game-request.md).
[Nexus requires a usable initial mod](https://help.nexusmods.com/article/104-how-can-i-add-a-new-game-to-nexus-mods).
That page provides the support route if approval takes more than seven working days.

## 3. Record the actual Nexus identifiers

| Value | Where to find it |
|---|---|
| Game domain | The approved game section URL: `nexusmods.com/<domain>` |
| Gameplay mod URL | The published gameplay mod page |
| Gameplay file-group ID | **Files → API Info**, possibly under **Advanced**, or **Manage Files → Edit** |

The mod ID at the end of a mod page URL is not its file-group ID. The extension
will have its own file-group ID. See the
[official upload action documentation](https://github.com/Nexus-Mods/upload-action).

## 4. Build the final-domain extension

In the [extension repository](https://github.com/DooDesch-Mods/TheCabinGame-Vortex),
open **Settings → Secrets and variables → Actions → Variables** and set
`NEXUS_GAME_DOMAIN` to the approved game domain.

Run **Actions → Check and build → Run workflow**. Download the successful
`vortex-package` artifact and extract it. Install the inner
`TheCabinGame-Vortex-0.1.0.zip`, rather than the outer artifact ZIP.

Alternatively, build locally:

```powershell
python -m pip install -r requirements.txt
python tools/build-extension.py --nexus-domain <approved-domain>
```

Remove the earlier local-ID extension and use a new test profile when switching
game IDs. Both the packaged game ID and `nexusPageId` must match the real domain.

## 5. Validate in Vortex and the game

1. Install the ZIP through **Extensions**, restart Vortex, and manage the game.
2. Confirm Steam discovery and manual folder selection, then launch the game.
3. Install the tested gameplay ZIP and **Deploy**. Check its destination files.
4. Run the game and observe the advertised mod behavior. Confirm current UE4SS
   loader activation for Lua/native mods, and actual PAK mounting for PAK mods.
5. Close the game, disable the mod and Deploy. Confirm its managed files and
   effects are removed. Re-enable and Deploy; confirm they return.
6. **Purge** managed files and check that original game files remain intact.
   Handle generated saves/logs according to the gameplay mod's documentation.

Record the extension commit, package hash, Vortex version, game build, mod/runtime
versions and results. The automated installer tests do not replace these checks.

## 6. Upload the extension to Nexus

1. Open [Modding Tools](https://www.nexusmods.com/site) and start an upload.
2. Select **Vortex > Extensions**.
3. Use `the cabin game - Vortex Support` and version `0.1.0`.
4. Use the [summary](submission/vortex-summary.txt),
   [description](submission/vortex-description.bbcode), and
   [upload fields](submission/vortex-upload.md). Replace the preparation-status
   paragraph with the recorded live validation and its actual limitations.
5. Use `extension/gameart.png` as the extension image.
6. Upload the final-domain extension ZIP as exactly **one Main File**. Its version
   must match `extension/info.json`. Set permissions consistently with GPL-3.0-only.
7. Record the extension URL and its **API Info file-group ID**.

Follow the [official extension packaging rules](https://github.com/Nexus-Mods/Vortex-Backend/wiki/How-to-package-a-game-extension).
Link the source commit/tag matching the uploaded ZIP so recipients can obtain
the corresponding source.

## 7. Enable automated Nexus updates

Set the following extension-repository Actions variables:

| Variable | Value |
|---|---|
| `NEXUS_GAME_DOMAIN` | Approved game domain, although the extension page is under `/site` |
| `NEXUS_FILE_GROUP_ID` | The extension Main File's API Info file-group ID |
| `NEXUS_LIVE_TESTED` | `true` after the final-domain package passes step 5 |

Make the `NEXUSMODS_API_KEY` secret available to this repository through the
organization or repository Actions settings. An organization secret was already
available during setup; recheck its repository access if an upload reports it
missing. Obtain keys from [Nexus API settings](https://www.nexusmods.com/settings/api-keys).
Never commit a key or paste it into an issue or chat.

The gameplay mod uses its own repository and file-group ID. Adapt the separate
[workflow example](publishing/gameplay-publish.example.yml) to its actual release
asset and acceptance process.

## 8. Request the extension review

Recheck for existing support, then open the
[official review form](https://github.com/Nexus-Mods/Vortex-Backend/issues/new?template=verify-extension.yaml).
Use the [prepared checklist](submission/review-issue.md), replace pending URLs,
and confirm packaging/live tests only when complete. Nexus maintainers decide
whether to add the extension to the Vortex listing.

After upload, test **Mod Manager Download** from the real gameplay mod page and
confirm that the NXM link targets the configured game.

## 9. Publish subsequent updates

1. Update the extension and increment `extension/info.json`, for example to `0.1.1`.
2. Run relevant live regression checks, push the change, and wait for green CI.
   Reset `NEXUS_LIVE_TESTED` until acceptance is confirmed if behavior changes.
3. Create a GitHub release with the matching tag, for example `v0.1.1`, and describe
   changes, validation and compatibility limits.
4. Publish the release. The workflow checks the tagged source, builds the ZIP,
   attaches the ZIP/receipt, and uploads a new Nexus file version when configured.
5. Confirm the successful workflow and Nexus version ID, then test a download.

The first manual Nexus upload is already `0.1.0`; do not upload that version
again as a subsequent automated update. Start with the next actual version.
Before retrying a failed or timed-out upload, inspect the Nexus file state: an
observation timeout does not prove the upload failed.

Initial game/mod pages, the first extension upload, live tests, page permissions,
images, and maintainer review require one-time manual work. CI, release assets,
and subsequent Nexus file updates are automated.
