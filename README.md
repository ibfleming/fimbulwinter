[![Build Status](https://github.com/ibfleming/fimbulwinter/actions/workflows/publish.yml/badge.svg)](https://github.com/ibfleming/fimbulwinter/actions/workflows/publish.yml)

# Fimbulwinter - A Veteran's Valheim Modpack

**Tuned for veteran multiplayer. No shortcuts, no cheese -- just deeper Valheim.**

Fimbulwinter is a curated Valheim modpack designed for experienced players returning to Valheim in a multiplayer group. Every mod has been hand-picked, configured, and balance-tested to enhance combat, exploration, visuals, and quality of life -- without betraying the core spirit of Valheim.

## Design Principles

- **Preserve the Spirit of Valheim** -- No flying, no teleport-cheese, no game-breaking shortcuts. Progression still requires biome exploration and earned power.
- **Reward Skill & Mastery** -- New content rewards experienced players with meaningful choices, deeper combat, and harder-earned victories.
- **Depth Over Breadth** -- Each mod adds genuine depth, not just volume. Quality over quantity.
- **Multiplayer-First** -- Every mod works on dedicated servers. Role specialization and group play are enhanced.
- **Actively Maintained** -- All mods are confirmed working with the current Valheim version.

## What's Included

### Difficulty & Loot (3 mods)
- **CreatureLevelAndLootControl** -- Hard difficulty, 5-star creatures, biome-scaling sectors
- **EpicLoot** -- Diablo-style magic/rare/epic/legendary loot with enchanting
- **EpicLoot_Therzie** -- Bridge patch integrating EpicLoot with all Therzie content

### Content: Weapons, Armor & Magic (4 mods)
- **Warfare** -- 200+ new weapons across all biome tiers
- **WarfareFireAndIce** -- Deep North endgame weapons
- **Armory** -- New armor sets with set bonuses
- **Wizardry** -- Full magic system with staves, spells, and elemental damage

### Content: Creatures & World (16 mods)
- **Monstrum + Deep North + Ashlands** -- 100+ new creatures across every biome
- **RtD Suite** (Ocean, Dungeons, Horrors, Monsters, Monstrum) -- Massive world expansion
- **Fee Fi Fo Fum** -- Giants roaming across biomes
- **EpicValheimsAdditions** -- Mistlands, DeepNorth, and Ashlands content expansion
- **Custom Raids** -- Configurable raid events
- **Forbidden Catacombs** -- Handcrafted swamp dungeon
- **More World Locations AIO** -- 153 new points of interest

### Content: Ships, Mounts & Cooking (5 mods)
- **OdinShip** -- 14 new ships and boats
- **SeaAnimals** -- Ocean creatures and rideable marine beasts
- **OdinHorse** -- Tameable horses with saddles and armor
- **DragoonCapes** -- 20+ capes with unique combat effects
- **CookingAdditions** -- 23 new foods and cooking stations

### Combat & Progression (8 mods)
- **Headshots + BetterArchery + ReliableBlock** -- Deeper, more rewarding combat
- **Agility + Endurance + Tenacity + SmartSkills** -- 4 new progression skills
- **SkilledCarryWeight** -- Carry weight scales with skill levels

### Visual & Atmosphere (6 mods)
- **Seasonality + HD Seasonality** -- Dynamic 4-season system with HD textures
- **GammaOfNightLights** -- Darker, moodier nights
- **HUDCompass** -- Map-pin compass with dynamic markers
- **BetterUI** -- Enemy HP bars, XP tracking, skill display

### Quality of Life (21 mods)
- **Extended Inventory + CraftyBoxes + AutoStore + ContainerSizes** -- Inventory overhaul
- **Quick Stack + Recycle + AAA Crafting** -- Streamlined crafting
- **LazyVikings + Eternal Fire + PetPantry** -- Automation
- **PlantEverything + PlantEasily** -- Advanced farming
- **SpeedyPaths + TeleportEverything** -- Movement QoL (ore teleport with 20% tax)
- **MissingPieces + NoRainDamage** -- Building improvements
- **TrueInstantLootDrop** -- Loot drops instantly at creature death location
- **TradersExtended** -- Expanded trader UI with sell lists and economy

### Sailing (2 mods)
- **Sailing Skill + SailingSpeed** -- Ship speed, health, and exploration scale with skill

### Multiplayer (1 mod)
- **Groups** -- Party system with group chat, shared pings, friendly fire toggle

### Admin Tools (3 mods)
- **ConfigurationManager + Server Devcommands + Gungnir** -- Full server admin toolkit

## Key Configuration Highlights

All mods have been individually configured for balanced veteran multiplayer:

- **Difficulty:** Hard mode, 5-star creatures, HP +50%/player scaling, elemental infusions
- **Loot:** Balanced preset, 80% unidentified drops, boss trophies per nearby player
- **Ore Teleporting:** Enabled with 20% transport tax (vanilla spirit preserved)
- **Seasons:** 5-day cycles with gameplay modifiers (Winter is harsh, Fall boosts damage)
- **Night Danger:** Darker nights (0.65 luminance) + horror spawns
- **Death Penalty:** No skill loss on death for mod skills; 75% vanilla skill recovery via SmartSkills
- **Sailing:** Skill-based speed/health/exploration bonuses, raft gets 2x boost
- **Raids:** ~Every 2 hours of play (36min interval, 30% chance)

## Installation

### With r2modman / Thunderstore Mod Manager

1. Open **r2modman** and select **Valheim**
2. Search for **Fimbulwinter** in the online mods tab
3. Click **Install with dependencies**
4. Click **Start modded** to launch

## Server Setup

This modpack is designed for dedicated server multiplayer. The server needs all gameplay mods but NOT the client-only visual/UI mods.

**Client-only mods** (server does not need):
- HD Seasonality textures
- HUDCompass, CameraTweaks, BetterUI
- BreatheEasy, GammaOfNightLights

All other mods should be installed on both client and server.

> **Note:** A separate server-specific package is planned for easier dedicated server installation in the future.

## Version History

See [CHANGELOG.md](https://github.com/ibfleming/fimbulwinter/blob/main/CHANGELOG.md) for full version history.

## Links

- **Source:** [GitHub](https://github.com/ibfleming/fimbulwinter)
- **Thunderstore:** [Fimbulwinter](https://thunderstore.io/c/valheim/p/ibfleming/Fimbulwinter/)
