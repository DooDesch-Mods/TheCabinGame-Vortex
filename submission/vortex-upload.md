# Extension upload fields

| Field | Value |
|---|---|
| Destination | https://www.nexusmods.com/site |
| Category | Vortex > Extensions |
| Name | the cabin game - Vortex Support |
| Author | DooDesch |
| Language | English |
| Summary | [vortex-summary.txt](vortex-summary.txt) |
| Description | [vortex-description.bbcode](vortex-description.bbcode) |
| Version | 0.1.0; must match `extension/info.json` |
| Image | `extension/gameart.png`, original 640 × 360 PNG illustration |
| Main File | Final-domain `TheCabinGame-Vortex-0.1.0.zip` |
| File display name | the cabin game - Vortex Support |
| Mod Manager download | Enabled; upload the extension ZIP |
| License | GPL-3.0-only; extension code, documentation and original artwork |
| Donation Points | Apply the author's existing preference |

Before upload, replace the description's preparation-status paragraph with the
actual Vortex version, game build, tested mod/runtime versions, and validation
limits. Do not claim completed live tests or Nexus review before they occur.

## Permissions

Allow redistribution, modification, conversion and code/asset reuse under
GPL-3.0-only. Do not require separate approval or prohibit commercial
redistribution. Preserve required copyright/license notices and provide
corresponding source according to the GPL. Link the source commit/tag matching
the uploaded package. Donation Points are a separate platform setting.

Suggested permissions text:

```text
Copyright (c) 2026 DooDesch. The extension code, documentation and original
illustrative artwork are licensed under GPL-3.0-only; see LICENSE.md.
You may modify and redistribute them, including commercially, under the GPL
terms. Preserve the required notices and provide the corresponding source.
Source: https://github.com/DooDesch-Mods/TheCabinGame-Vortex
No game assets or UE4SS binaries are included.
```

After the initial upload, record the extension URL in the
[review checklist](review-issue.md), and set the actual extension file-group ID
for [automated updates](../publishing/README.md). The gameplay mod uses its own
page, license, file-group ID, and publication workflow.

Reference: [official extension packaging rules](https://github.com/Nexus-Mods/Vortex-Backend/wiki/How-to-package-a-game-extension).
