# Changelog

All notable changes to Fimbulwinter are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] - 2026-11-14

A fresh start for Fimbulwinter: a server-side-first modpack for Valheim 1.0
"Deep North". Not compatible with earlier versions -- start a new world.

### Heads-up
- **Every player needs this exact version to join.** Adventure Backpacks
  checks for a matching install on both the client and the server, so a
  mismatched or missing install is turned away at connect.

### Added
- **Server-side quality of life** that works for every player, including
  unmodded and console clients: auto-pickup and auto-sort into nearby chests,
  bigger chests and ship storage, smelters and kilns fed from nearby chests,
  floating items, majority-vote sleep skip, and multiplayer desync fixes.
- **Biome-tiered backpacks** (Adventure Backpacks): six backpacks with
  their own perks, and crafting and storing straight from the backpack.
- **Building tools:** free piece rotation (Gizmo), manual and grid snapping
  (Extra Snap Points Made Easy), and square hoe and cultivator brushes
  (Advanced Terrain Modifiers).
- **Inventory and UI:** extra equipment, quick, ammo and food slots;
  crafting and building from nearby chests; a compass bar; richer tooltips,
  production timers and chest previews; recycling items back into parts.
- **A one-click connect button** on the main menu (Zenox ServerConnect) --
  fill in your server's address and password in your own profile.
- **A working admin console** on a dedicated server (Server devcommands).

### Changed
- Skill loss on death is 2% instead of vanilla's 5%.
- Telemetry and error reporting in Adventure Backpacks are switched off.
