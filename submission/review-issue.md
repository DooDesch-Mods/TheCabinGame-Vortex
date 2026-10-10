# [Verify]: the cabin game

Submit using:
https://github.com/Nexus-Mods/Vortex-Backend/issues/new?template=verify-extension.yaml

## Nexus Username
DooDesch

## Extension URL
PENDING — paste the real https://www.nexusmods.com/site/mods/... URL after upload.

## Game URL
PENDING — paste the actual approved game section URL. Do not guess its domain.

## Existing Extension URL
Recheck Nexus/Vortex immediately before submission. Enter any existing
extension URL, or state that none was found in that check.

## New features
Steam discovery for app 4406280; manual game-folder detection; installation of
PAK and matching IoStore containers; UE4SS Lua/native and runtime archive layouts;
mixed archives with independent enabled.txt markers; visible errors for invalid
layouts and duplicate destinations; Vortex-managed deployment and purge.

## Confirmations
- [ ] Above URLs are accurate, accessible, and a fresh duplicate-extension check is complete.

## Packaging
- [x] Local candidate contains index.js, info.json, config.json and 640x360 PNG gameart at the archive root.
- [ ] Uploaded package includes GPL-3.0-only and a link to its matching source commit/tag.
- [ ] Final archive has the real Nexus domain and exactly matches the uploaded version and main file.

## Testing
- [x] 21 technical checks pass, including routing and isolated filesystem hardlink deploy/disable/re-enable/purge.
- [ ] Extension installed and game managed in Vortex; discovery/manual detection/launch verified.
- [ ] Actual gameplay-mod archive installed, enabled, disabled and purged in Vortex.
- [ ] Actual mod observed in the running game; loader activation and PAK mounting confirmed.
- [ ] Nexus Mod Manager download routes to this game after domain configuration.

Do not tick the official "This game extension has been tested" confirmation on
the basis of the simulated tests alone. The Vortex UI/in-game checks are pending.
No review request has been submitted.
