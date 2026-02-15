# Changelog

All notable changes to Fimbulwinter will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
