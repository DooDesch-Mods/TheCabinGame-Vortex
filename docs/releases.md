# GitHub publishing

> 🛟 **Need help or found a bug?** Get support at [support.doodesch.de/thecabingame-vortex](https://support.doodesch.de/thecabingame-vortex).

Repository: https://github.com/DooDesch-Mods/TheCabinGame-Vortex

## Continuous integration

The **Check and build** workflow runs on main-branch pushes, pull requests,
and manual dispatch. It checks the installer on Windows, builds the extension
ZIP, verifies the gameplay packaging tool and document links, and exercises
publication guards. Packages and receipts are available as workflow artifacts.
New pushes cancel an older check for the same branch. Publication runs stay
serialized and are never cancelled by a later release.

`NEXUS_GAME_DOMAIN` selects a final-domain build. Without it, CI deliberately
builds a `-local-candidate.zip` for testing. CI success covers automated checks;
it does not certify live Vortex/game behavior.

## Stable releases

The manual **Read Nexus game metadata** workflow reads game ID `10562` from the
legacy game list and checks the selected UE4SS file's existence through the current
API. The file response has no game mapping. The artifact contains selected public
metadata only. It does not upload files or set release variables. A missing legacy
game record does not establish approval status.

The **Release and update Nexus** workflow runs when a stable GitHub release is
published, or when an existing release tag is explicitly selected for a retry.
Stable release publication requests a Nexus upload automatically. A manual run
leaves **publish_nexus** unchecked by default. Select it only when a new Nexus
file version is intended. An unchecked manual run rebuilds and attaches the
checked GitHub assets without contacting the Nexus upload API.
It checks tag/version equality and the tagged source, requires
`NEXUS_LIVE_TESTED=true`, and attaches the ZIP and SHA-256 receipt. With no game
domain configured, the release preserves the tested local game ID and leaves
game-specific Nexus downloads unmapped. An invalid configured domain or an
untested package is rejected before release assets are built.

For a prepared GitHub draft, select **publish_github** to publish it after the
selected Nexus upload succeeds. This defaults to false. The workflow uses its
GitHub token for this operation; GitHub does not start other release-event
workflows from that token. Existing published releases can still use manual runs
to attach assets or update Nexus without another GitHub publication.

If the extension file-group ID is still absent, the workflow explicitly skips
Nexus upload so the first upload can be done manually. Once configured, the
ID must be numeric and the Nexus secret must be available, or the job fails.
Subsequent uploads archive the existing file version and enable the new version
as the primary Mod Manager download.

## Release notes

Maintain exactly one nonempty `## [X.Y.Z]` section in [CHANGELOG.md](../CHANGELOG.md)
for each release version. The workflow keeps the Markdown notes as evidence,
converts them to BBCode for the Nexus file description, and uses plain text for
the mod page's Changelogs tab. Supported markup includes headings, bold text,
links, inline code and lists with one nested level. Wrapped lines are joined.
A missing, duplicate or empty version section fails before any upload.

The Changelogs tab needs the global **API > Unique Mod ID**, not the short
game-scoped page number. If it is absent, a visible warning reports that the tab
is skipped; the file description still receives the notes.

## Configuration

| Setting | Purpose |
|---|---|
| Variable `NEXUS_GAME_DOMAIN` | Optional approved game domain used in both packaged mappings |
| Variable `NEXUS_FILE_GROUP_ID` | Extension Main File's API Info file-group ID |
| Variable `NEXUS_MOD_ID` | API Unique Mod ID for the extension page's Changelogs tab |
| Variable `NEXUS_LIVE_TESTED` | `true` after validation of the intended release |
| Secret `NEXUSMODS_API_KEY` | Nexus upload authentication; repository or permitted organization secret |

IDs are public configuration. Keys must stay in Actions secrets. If a change
affects behavior, reset the live-test flag until the relevant checks pass.
The public repository uses the organization's `NEXUSMODS_API_KEY`, following
the same convention as Palvolve. A repository secret with the same name takes
precedence; do not create a duplicate key just for this extension.

The official Nexus upload action is pinned to commit
`c96019556046053aa26044b44396cd38929daf23` (`v1.0.0-beta.10`). The workflow
requires its returned version ID and records that acknowledgement in the job
summary. After a failed or timed-out upload, inspect Nexus before retrying:
an observation timeout does not prove no upload occurred.

Initial Nexus pages, live checks and maintainer review must be completed before
the extension can appear in Vortex's public listing.
