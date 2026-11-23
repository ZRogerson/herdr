# Herdr zro setup

This repo contains my personal Herdr desktop setup, based on Herdr 0.1.16. On
this Mac, `~/.config/herdr-app` is a symlink to `~/dev/herdr-setup/config`.
Edits under `config/` affect the live app.

| Path | Contents |
| --- | --- |
| `config/layouts/zro.json` and `zro.svg` | zro layout and preview |
| `config/themes/tron-grid.json` | Tron Grid theme |
| `config/mods/` | Supporting mods and their assets |
| `config/keys.json` and `config/settings.json` | Shortcuts and app preferences |

Herdr writes local state, bundled defaults, and program icons into this
directory. Git ignores those paths. `zro` uses some bundled mods and assets
that Herdr supplies on first launch. New custom layouts, themes, mods, and
assets can be added with ordinary `git add`.

## Included mods and credits

I include modified copies of other authors’ mods alongside the mods I use
to tie the `zro` layout together. These credits identify the upstream
projects and contributors.

| Included mod | Credit |
| --- | --- |
| `better-changes` | [Munza · Better Changes](https://github.com/munza/herdr-mods/tree/main/better-changes) |
| `drover-files` | [Drover Files contributors](config/mods/drover-files/NOTICE), based on Herdr’s Files mod |
| `drover-open` | [Drover Open contributors](config/mods/drover-open/NOTICE) |
| `drover-viewer` | [Drover Viewer contributors](config/mods/drover-viewer/NOTICE) |
| `agent-name-prompt` | Adapted from the [Herdr](https://github.com/herdrdev/herdr-app) Prompt mod |
| `master-menu` | Adapted from Herdr’s Menu mod |
| `master-new-menu` | Adapted from Herdr’s New Menu mod |
| `master-tabs` | Adapted from Herdr’s Tabs mod |
| `master-worktree` | Adapted from Herdr’s Worktree mod |
| `tron-spaces` | Adapted from Herdr’s Spaces mod |
| `agent-name-menu` | Setup-specific menu for agent names |

The Drover notices also credit the icon projects whose assets they use.

## Install on another Mac

1. Install Herdr, launch it once, then quit its window.
2. From a fresh clone of this repo, run `python3 install.py`. The installer
   backs up the settings and assets it replaces in a timestamped folder
   beside the destination config. It uses `~/.config/herdr-app` by default, or
   the directory set in `HERDR_APP_HOME`.
3. Reopen Herdr and select `zro`.

   ```sh
   herdr-app do layout.switch '{"name":"zro"}'
   ```

Workspace history, sessions, and per-workspace preferences stay local.
See [AGENTS.md](AGENTS.md) for repo maintenance instructions.
