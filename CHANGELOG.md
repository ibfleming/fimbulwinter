# Changelog

All notable changes to Fimbulwinter will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
