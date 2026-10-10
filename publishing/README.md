# GitHub publishing

Repository: https://github.com/DooDesch-Mods/TheCabinGame-Vortex

`ci.yml`: every main push and PR checks the actual installer on Windows,
builds the ZIP and verifies the gameplay package builder. Packages and receipts
are workflow artifacts. `NEXUS_GAME_DOMAIN` selects a final-domain build;
without it, CI deliberately produces a local candidate.

`release.yml`: a published stable GitHub release (or explicit retry of an
existing tag) checks tag/version equality and tests the tagged source. It
attaches the ZIP/receipt to that release. Nexus updates run only after domain,
file-group ID and live acceptance are configured. Missing initial IDs are a
visible deliberate skip; incomplete live acceptance or missing credentials
on a configured target fail the job.

Variables: `NEXUS_GAME_DOMAIN`, `NEXUS_FILE_GROUP_ID`, `NEXUS_LIVE_TESTED=true`.
Secret: existing org `NEXUSMODS_API_KEY`, visibility `all` checked on 10 October 2026.
IDs are public configuration; keys never belong in source files or chat.

The official Nexus upload action is pinned to commit
`c96019556046053aa26044b44396cd38929daf23` (tag v1.0.0-beta.10, direct commit).
It returns a version ID; the workflow requires that acknowledgement and records
it in the job summary. A timeout is not automatic permission to duplicate an
upload: verify Nexus state before using workflow_dispatch to retry.

`gameplay-publish.example.yml` is a template for the gameplay owner's separate
repo, not an active workflow in this extension repo. Its asset naming and
build acceptance must be adapted to the final mod. No gameplay source has
been published by this integration session.

See [the complete setup guide](../NEXUS-SETUP.md). Initial Nexus pages/files
and the Nexus extension review still require the website/maintainers.
