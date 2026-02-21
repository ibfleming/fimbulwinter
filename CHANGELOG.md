# Changelog

All notable changes to Fimbulwinter will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.5.0] - 2026-02-20

### Added
- JereKuusela-Upgrade_World 1.76.0 -- Console commands for regenerating explored world zones (needed for RtDDungeons 1.0.0 migration)
- VentureValheim-Venture_Logout_Tweaks 0.6.0 -- Preserves status effects across logout (anti-combat-logging for multiplayer integrity)
- VentureValheim-Venture_Floating_Items 0.3.3 -- Items float on water instead of sinking (prevents losing drops near coastlines and ocean fights)
- Azumatt-AzuWorkbenchTweaks 1.0.5 -- Auto-repair items at workbenches (reduces tedious manual repair clicks)

### Changed
- **CLLC Difficulty Rebalance:** HP per star reduced from 100% to 50% (1-star = 1.5x HP, not 2x); damage per star reduced from 50% to 30%
- **CLLC Quick Effect:** Global chance reduced from 10% to 5%; Meadows Quick = 0% (blocked), Black Forest Quick = 2% (heavily gated)
- **CLLC Star Chances:** Meadows WL0-WL2 reduced ~30% (WL0: 8%→5%); Black Forest WL0-WL1 reduced ~20% (WL0: 12%→9%)
- **CLLC Dungeon Respawn:** Disabled (was 30 min) -- dungeons now stay cleared permanently (vanilla behavior)
- **CLLC Camp Respawn:** Disabled (was 30 min) -- camps stay cleared permanently
- **CLLC Item Respawn:** Disabled (was 150 min) -- dungeon loot stays collected permanently
- **Seasonality:** All seasons shortened from 5 days to 3 days per season (6-hour full year cycle)
- **OdinHorse:** Creature Faction changed from ForestMonsters to AnimalsVeg (horses no longer aggro with hostile mobs); Health reduced from 200 to 100
- **HUDCompass:** Added "Death" to pin ignore list (fixes duplicate death marker on minimap)
- **Quick Stack Store:** Simplified UI -- disabled Quick Stack, Restock, Trash Can, and Favorite Toggle buttons (Sort, Store All, Take All remain)
- **AzuExtendedPlayerInventory:** Enabled Legacy Layout for vanilla-style UI
- **CreatureConfig.yml:** Deathsquito movement speed reduced to 0.8x; tamed animal health boosted to 1.5x
- ASharpPen-Drop_That updated from 3.1.3 to 3.1.4
- Azumatt-AzuAutoStore updated from 3.0.13 to 3.0.14
- Azumatt-AzuExtendedPlayerInventory updated from 2.3.4 to 2.3.7
- Soloredis-RtDDungeons updated from 0.4.3 to 1.0.0 (major update -- requires world migration via Upgrade_World)
- Total mod count: 108 → 111 (4 added, 1 removed)

### Removed
- coemt-Birds 0.2.0 -- Removed for being useless and annoying; AirAnimals remains for ambient atmosphere

## [1.4.0] - 2026-02-18

### Removed
- OdinPlus-BeeQueen 1.1.0 -- Bugged items and broken boss AI; removed for quality
- Smoothbrain-Groups 1.2.10 -- Groups are not persistent across sessions (disbands on logout); not suitable for ongoing multiplayer groups

### Changed
- EpicLoot: Disabled hot reloading patches (removes unnecessary filesystem watcher overhead in production)
- Drop_That: Set DropLimit to 200 (safety net against CLLC multiplier edge cases producing excessive item drops)
- LeanNet: Increased NetRatePhysics from 8 to 12 (reduces door and collectible interaction latency)
- AzuAutoStore: Increased IntervalSeconds from 10 to 15 (reduces background container scanning for less pickup contention)
- HUDCompass: Disabled dynamic pins on map (fixes minimap duplicate player markers caused by parallel pin tracking conflicting with Better_Cartography_Table)
- CLLC: Reduced Splitting effect chance from 5% to 2% (prevents entity explosion cascades with 9 creature mods stacking spawn density)
- CLLC CreatureConfig.yml: Reduced Deep North WL4-5 star chances (WL4: 80%→74% starred, WL5: 100%→89% starred; ensures some base creatures remain for breathing room)
- Spawn_That: WriteSpawnTablesToFileAfterChanges disabled (diagnostic completed)
- AzuCraftyBoxes: Reduced Container Range from 30 to 20 (reduces container scanning overhead at crafting stations)
- LeanNet: Increased Vec3CullSize from 0.05 to 0.1 (reduces ZDO network traffic by culling tiny position updates)
- BepInEx: Disabled WriteUnityLog to disk (eliminates Unity font/rendering warning spam from log files)
- BepInEx: Removed Warning from console LogLevels (cleans up server console output)
- ServerCharacters: Reduced backup count from 25 to 10 (reduces disk I/O during auto-saves)
- ServerCharacters: Enabled AFK Kick Timer at 15 minutes (frees server resources from idle players)
- AzuAutoStore: Updated from 3.0.11 to 3.0.13
- Total mod count: 110 → 108

## [1.3.1] - 2026-02-16

### Fixed
- BreatheEasy reclassified from client-only to server-required -- mod uses ServerSync with `ModRequired = true`, causing server incompatibility errors when not installed on the server

### Changed
- Updated Server Setup documentation to clarify BreatheEasy must be on both client and server
- Azumatt-AzuCraftyBoxes updated from 1.8.12 to 1.8.13

## [1.3.0] - 2026-02-15

### Added
- Smoothbrain-DualWield 1.0.10 -- Dual-wield weapons for deeper combat
- Smoothbrain-Evasion 1.0.4 -- Evasion skill that rewards dodge timing
- Smoothbrain-Lumberjacking 1.0.6 -- Woodcutting skill with yield scaling
- Smoothbrain-Building 1.2.6 -- Building skill that improves structure HP
- Smoothbrain-Blacksmithing 1.3.3 -- Crafting skill that improves upgrade quality
- Searica-ProjectileTweaks 1.6.0 -- Improved arrow and projectile physics
- shudnal-CircletExtended 1.1.9 -- Dverger circlet upgrades and progression
- Mexanik-ShieldBash 1.5.1 -- Shield bash attack for melee combat depth
- nbusseneau-Better_Cartography_Table 0.8.1 -- Better map sharing for multiplayer

### Changed
- DualWield and Evasion skill death penalty set to 0% (SmartSkills handles vanilla recovery)
- CircletExtended toggle light keybind changed from G to K (G/H used by EpicLoot Ability Hotkeys 1/2)
- Total mod count: 101 → 110

## [1.2.0] - 2026-02-14

### Added
- JereKuusela-Structure_Tweaks 1.35.0 -- structure scaling, collision override, building tools
- Azumatt-MyPitsDontLeak 1.0.0 -- fixes rain damage through built structures
- blacks7ar-WieldEquipmentWhileSwimming 1.1.3 -- use equipment while swimming
- coemt-Birds 0.2.0 -- ambient birds (herons, ravens, seagulls) across biomes
- Horem-MushroomMonsters 1.0.2 -- mushroom-themed creatures across multiple biomes
- CacoFFF-LeanNet 1.0.1 -- network optimization for better multiplayer performance
- ComfyMods-Scenic 1.5.0 -- client-side scene management and visual tools
- MSchmoecker-MultiUserChest 0.6.1 -- multiple players access chests simultaneously
- MSchmoecker-TimeoutLimit 0.2.0 -- increased server timeout to prevent disconnects
- MSchmoecker-LocalizationCache 0.3.0 -- cached localization for faster startup
- OdinPlus-BeeQueen 1.1.0 -- BeeQueen boss creature with weapons and armor
- Searica-NetworkTweaks 0.1.5 -- network buffer optimization and compression
- Smoothbrain-ShutUp 1.0.2 -- suppresses repetitive in-game messages
- Smoothbrain-Mining 1.1.6 -- mining skill with yield and speed progression
- Smoothbrain-Resurrection 1.0.13 -- resurrect dead players with item cost
- Smoothbrain-ServerCharacters 1.4.16 -- server-side character storage with encryption
- Smoothbrain-Foraging 1.0.10 -- foraging skill with pickable yield progression
- Smoothbrain-Farming 2.2.2 -- farming skill with crop yield progression
- Radamanto-Bestiary 1.1.4 -- 30+ new creatures across all biomes

### Changed
- ishid4-BetterArchery updated from 1.9.81 to 1.9.82
- Soloredis-RtDDungeons updated from 0.4.2 to 0.4.3
- BeeQueen `Can have stars` enabled for CLLC starred variants
- Structure Tweaks `Override portal restrictions` disabled (preserves 20% transport tax)
- New skill mods (Mining, Farming, Foraging) confirmed at 0% death penalty
- Thunderstore categories expanded: `modpacks` → `modpacks, server-side, enemies, gear, tweaks`
- Total mod count: 82 → 101

## [1.1.0] - 2026-02-13

### Added
- Marlthon-SeaAnimals 0.3.4 -- ocean creatures and rideable marine beasts
- Horem-Fee_Fi_Fo_Fum 0.1.9 -- 6 types of giants across biomes
- Huntardys-EpicValheimsAdditions 2.1.2 -- Mistlands, DeepNorth, Ashlands content expansion
- Azumatt-TrueInstantLootDrop 1.0.3 -- loot drops instantly at creature death location
- shudnal-TradersExtended 1.3.12 -- expanded trader UI with sell lists and coin economy

### Changed
- OdinPlus-OdinHorse updated from 1.5.7 to 1.5.8
- Soloredis-RtDMonstrum updated from 0.8.0 to 0.8.1
- Soloredis-RtDMonsters updated from 2.2.7 to 2.2.8
- Soloredis-RtDDungeons updated from 0.3.9 to 0.4.2
- Removed all mod skill death penalties (Tenacity, Sailing set to 0%; Agility, Endurance already 0%)
- Death penalty updated: 75% vanilla skill recovery via SmartSkills, no mod skill loss
- Removed "Manual HD Visuals" section from README
- Updated Thunderstore link to live package URL

### Removed
- blacks7ar-FineWoodPieces -- removed mod and config

## [1.0.2] - 2026-02-13

### Fixed
- Ensure CHANGELOG.md is included on Thunderstore builds.

## [1.0.1] - 2026-02-13

### Fixed
- Truncated config filenames in the build process.
- Icon dimensions resized to 256x256.

## [1.0.0] - 2026-02-13

### Added
- Initial release with 78 mods (71 Thunderstore-managed + 4 standalone HD visuals + 3 config-only)
- Full configuration tuning pass for veteran multiplayer balance
- Custom EpicLoot + Therzie integration patches
- Seasonality tweaks (pickables, plants, spawn adjustments)
- Multi-language Therzie translations (12 languages)
- CLLC creature and item YAML configurations
- Custom raid supplemental configs (Deathsquito Season, Ragnarok)

### Configuration Highlights
- Hard difficulty with 5-star creatures and elemental infusions
- EpicLoot Balanced preset with 80% unidentified drops
- Ore teleporting with 20% transport tax
- 5-day season cycles with gameplay modifiers
- Darker nights (0.65 luminance) with horror spawns
- 75% skill recovery on death, 5% exp loss per skill
- All keybind conflicts resolved (see PROJECT.md)
