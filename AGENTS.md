# Working on this repo

- Treat `config/` as live on this Mac. Herdr reaches it through
  `~/.config/herdr-app`. Check the symlink before any migration or
  bulk filesystem change. Leave the window open unless the task requires a
  restart. The user may be working in a Herdr terminal.
- Keep changes scoped to `zro` and its dependencies. Check layout references,
  mod code, and shortcuts before moving or removing a mod or asset.
- Use `config/AGENTS.md`, when present, as Herdr's generated reference for
  layout, mod, and CLI behavior. Herdr regenerates its bundled defaults on
  startup. Keep bundled files out of Git. Make customizations in `zro` or in
  a custom mod.
- Keep session data, workspace state, logs, telemetry, sockets, generated
  files, and credentials out of Git. Use ordinary `git add` for custom setup
  files and review staged paths before committing. Update `.gitignore` if a
  new Herdr version introduces generated paths.
- Verify changes with the narrowest available check. Parse JSON after edits,
  check referenced assets, and use `herdr-app status` to inspect the live
  layout when needed. Test installer changes against a disposable destination
  using `HERDR_APP_HOME`.
