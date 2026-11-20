# Changelog

All notable changes to Fimbulwinter are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.1] - 2026-11-20

**Do I need to update?** Yes. The server and every player need this version; mismatched installs can be refused when joining.

### Added
- Hold Alt and click an item in your inventory to share it in chat as a link that other players can hover to inspect.
- Extra snap points for many more pieces, and holding Shift reverses the direction when cycling snap points or grid precision.
- Carts and ships can now be named on the map.
- The main-menu connect button now shows whether the server is online or offline.
- Two new backpacks for the late game, the Cinderward Pack (Ashlands, heat resistance) and the Frostbound Haversack (Deep North, frost resistance and a stamina boost when you are low on health).

### Changed
- Crafting lists now show recipes you can make first, and holding Ctrl on the multicraft buttons changes the amount by the batch size.
- Floating item crates now despawn after an hour.
- Recycling now asks you to confirm first (Enter to accept, Escape to cancel). You still get all the crafting materials back.
- Backpacks have new Modern models, and a backpack holding ore or metal can no longer go through a portal. Opening a crafting station now opens your backpack next to it.

### Fixed
- Configuration sync is more reliable on slow connections.
- Opening a crafting station with a backpack on no longer stutters in bases with many chests, and several backpack tooltip, chest tab and shift-click errors are gone.

### Mod updates
- BepInExPack Valheim 5.4.2350 -> 5.4.2360 (both)
- ConditionalConfigSync 1.0.8 -> 1.0.11 (both)
- Jotunn 2.30.1 -> 2.30.2 (both)
- AdventureBackpacks 2.1.4 -> 2.4.7 (both)
- MyLittleUI 1.2.22 -> 1.2.34 (client)
- ExtraSlots 1.2.12 -> 1.2.24 (both)
- HUDCompass 1.2.0 -> 1.2.1 (client)
- NoRainDamage 1.3.0 -> 1.3.2 (both)
- NullReferenceFix 1.0.20 -> 1.0.50 (both)
- Server devcommands 1.113.0 -> 1.116.0 (both)
- RecycleItemsIntoParts 1.7.3 -> 1.8.10 (client)
- Extra Snap Points Made Easy 2.1.0 -> 2.2.0 (client)
- ServerConnect 1.0.7 -> 1.0.14 (client)
- ServersideQoL 2.0.13 -> 2.6.0 (server)
- ServersideQoL AutoStore 2.0.11 -> 2.5.1 (server)
- ServersideQoL AutoProcess 2.0.11 -> 2.3.0 (server)
- ServersideQoL LetItFloat 2.0.11 -> 2.6.0 (server)
- ServersideQoL MultiplayerTweaks 2.0.11 -> 2.6.0 (server)

### Key changes
- New: Left Shift -- Extra Snap Points Made Easy: Reverse Cycling Direction
- New: Left Shift -- HUDCompass: Use Key Modifier
- New: Left Alt -- ExtraSlots: Modifier shortcut
- New: Page Down -- ExtraSlots: Next row shortcut
- New: Page Up -- ExtraSlots: Previous row shortcut
- New: Left Control + Left Alt -- MyLittleUI: Hold to inspect chat modifier
- New: Left Alt -- MyLittleUI: Link item modifier
- New: Left Alt -- MyLittleUI: Original tooltip shortcut

Technical details: [GitHub Releases](https://github.com/ibfleming/fimbulwinter/releases)

## [3.0.0] - 2026-11-14

A fresh start for Fimbulwinter: a server-side-first modpack for Valheim 1.0
"Deep North".

### Heads-up
- **3.0.0 is a different modpack, not an update to 2.x.** It's rebuilt from
  scratch and moves well away from earlier versions and their spirit: a much
  smaller, server-side-first pack with far fewer mods, and most of what 2.x
  had is gone. It's still being built and improved, so expect more changes
  in the updates that follow. Updating replaces your old setup and needs a
  new world.
- **Want the old pack? Stay on 2.0.3.** In r2modman, pick version 2.0.3 for
  Fimbulwinter and don't update it. 2.0.3 won't get further updates, so any
  mod updates there are yours to do by hand.
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
