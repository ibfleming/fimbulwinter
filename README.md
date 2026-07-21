[![Build Status](https://github.com/ibfleming/fimbulwinter/actions/workflows/publish.yml/badge.svg)](https://github.com/ibfleming/fimbulwinter/actions/workflows/publish.yml)

# Fimbulwinter - A Veteran's Valheim Overhaul

**Valheim was never this dangerous. 103 mods of starred monsters, enchanted loot, and blood-earned mastery — built for players who think vanilla is too easy.**

Fimbulwinter is a curated overhaul modpack for veteran multiplayer crews. CLLC difficulty scaling turns every biome into a gauntlet of starred creatures, Epic Loot fills the world with enchantable gear worth chasing, and the full Therzie suite (Warfare, Armory, Monstrum, Wizardry) hands you the arsenal to survive it — backed by new creatures, world locations, seasons, ships, and mounts, all wrapped in a polished QoL and UI layer so none of it gets in your way. Every mod is verified non-deprecated against Thunderstore.

## Design Principles

- **Preserve the Spirit of Valheim** — No teleport-cheese (ore transport carries a 10% tax), no game-breaking shortcuts. Progression still requires biome exploration and earned power.
- **Reward Skill & Mastery** — Harder than vanilla from the Meadows onward: starred creatures, elemental infusions, tuned raids.
- **Depth Over Breadth** — Quality content that extends the game's systems, not kitchen-sink bloat.
- **Multiplayer-First** — Every mod works on dedicated servers, with server-enforced config sync.
- **Actively Maintained** — Every mod verified current against Thunderstore; no deprecated or abandoned mods.

## What's Included

### Core & Frameworks (6 mods)
- **BepInExPack_Valheim** — Mod loader
- **Jotunn** — Modding framework
- **JsonDotNET / YamlDotNet** — Shared libraries
- **ConfigurationManager** (shudnal) — In-game config editing (F3)
- **ConditionalConfigSync** — Server-enforced config ownership and sync policies

### Difficulty & Loot Core (7 mods)
- **Creature Level and Loot Control** — Starred creatures (up to 5), per-player difficulty scaling, world levels
- **Epic Loot** — Magic item drops, enchanting, bounties, and gambling
- **EpicLoot_Therzie** — Bridge patches so Therzie gear rolls Epic Loot magic
- **Custom Raids** — Tuned raid tables with custom events
- **Drop That / Spawn That / This Goes Here** — Loot-table and spawner control

### Weapons, Armor & Magic (7 mods)
- **Warfare + Warfare Fire and Ice** — Massive weapon/shield expansion through Deep North
- **Armory** — New armor variants that upgrade across tiers
- **Wizardry** — Full magic system: staves, spells, and casting progression
- **Monstrum + Monstrum Deep North** — New monsters, mini-bosses, and forsaken bosses
- **DragoonCapes** — Capes with unique effects, vanilla capes revamped

### Creatures & World (6 mods)
- **Bestiary** — New creatures with configurable spawns
- **SeaAnimals** — Ocean life: dangerous and rideable marine creatures
- **RtDOcean** — Ocean expansion: sea life, crops, agriculture
- **Forbidden Catacombs** — Randomized Swamp dungeon
- **More World Locations AIO** — 181 new POIs: dungeons, traders, ports
- **Seasons** — Four rotating seasons with visual and gameplay variety (7-day seasons)

### Ships, Mounts & Trade (5 mods)
- **OdinShip** — 7 new ships plus docks and fishing gear
- **LongshipUpgrades** — Modular longship upgrades: mast, storage, hull HP
- **OdinHorse** — Tameable, rideable horses with carts and armor
- **TradersExtended** — Extended trader inventories and UI
- **CookingAdditions** — 23 new cookable foods

### Combat Mechanics (5 mods)
- **BetterArchery** — Improved bow gameplay, retrievable arrows (zoom off — ProjectileTweaks owns zoom)
- **ProjectileTweaks** — Arrows launch from where you aim, bow/crossbow zoom, ammo counter
- **Headshots** — Head weakspots reward precise pierce shots
- **ShieldBash** — Active shield bash attack (Middle Mouse while blocking)
- **DualWield** — Fight with a weapon in each hand

### Skills & Progression (15 mods)
- **SmartSkills** — 75% skill recovery after death; death matters but isn't crushing
- **Smoothbrain skill roster** — Tenacity, Evasion, Mining, Foraging, Farming, Lumberjacking, Building, Blacksmithing, Sailing (+ SailingSpeed base tuning)
- **Agility / Endurance** — Movement and stamina skills
- **SkilledCarryWeight** — Carry weight grows with your skills
- **CircletExtended** — Upgradeable circlet light with new abilities

### Inventory & Crafting (10 mods)
- **AzuExtendedPlayerInventory** — Dedicated equipment and quick slots
- **AzuCraftyBoxes** — Craft using materials from nearby containers
- **AzuAutoStore** — Auto-deposit items into nearby containers
- **AzuContainerSizes** — Larger chest capacities
- **AAA Crafting** — Improved crafting UI with bulk crafting and upgrades
- **Recycle N Reclaim** — Recycle items back into materials
- **Quick Stack Store Sort Trash Restock** — One-key chest stacking, sorting, and trash
- **MultiUserChest** — Multiple players can use one chest simultaneously
- **AdventureBackpacks** — Progression-gated craftable backpacks
- **TrueInstantLootDrop** — Loot drops instantly on kill

### UI & HUD (6 mods)
- **MyLittleUI** — Lightweight UI upgrades: timers, stats, chest contents, weather
- **VNEI** — In-game item and recipe browser
- **HUDCompass** — Compass bar with map pins
- **AzuHoverStats** — Detailed hover tooltips
- **Better Cartography Table** — Precise control over pin sharing and map exploration
- **ChangelogEditor** — Clean main-menu changelog

### Visual & Atmosphere (1 mod)
- **CameraTweaks** — Configurable FoV and camera distance (vanilla atmosphere otherwise untouched — no lighting or weather-effect mods)

### Building (8 mods)
- **Gizmo** — Precise build-piece rotation on all axes
- **Extra Snap Points Made Easy** — More snap points on every piece
- **AzuAreaRepair** — Repair all nearby build pieces with one hammer hit
- **MissingPieces** — Vanilla-styled build pieces that should have existed
- **AdvancedTerrainModifiers** — Precision terraforming with square/circle modes and undo
- **AzuWorkbenchTweaks** — Workbench behavior improvements
- **Structure Tweaks** — Advanced structure behavior control
- **MyPitsDontLeak** — Fixes the vanilla tarpit memory leak

### Farming & Nature (3 mods)
- **PlantEverything** — Plant every gatherable resource and tree
- **PlantEasily** — Grid-aligned planting and mass harvesting
- **MassFarming** — Bulk plant and pick with a modifier key

### Gameplay QoL (11 mods)
- **ComfyAutoRepair** — Opening a crafting station repairs everything
- **AutomaticFuel** — Fireplaces and smelters feed from nearby chests (F7 toggle)
- **PetPantry** — Tamed animals feed from nearby containers
- **SaveCrossbowState** — Crossbows stay loaded when switching weapons
- **WieldEquipmentWhileSwimming** — Keep gear in hand while swimming
- **AzuMiscPatches** — Collection of small vanilla fixes
- **Venture Floating Items** — Dropped items float on water
- **StumpsAreOneHp** — Tree stumps fall in a single hit
- **NoRainDamage** — Buildings no longer take weather damage
- **SpeedyPaths** — Move faster on paths, roads, and cleared ground
- **TeleportEverything** — Portal everything, with a 10% ore transport tax

### Fixes & Performance (5 mods)
- **LocalizationCache** — Dramatically faster load times
- **TimeoutLimit** — Fixes join timeouts on modded servers
- **NetworkTweaks** — Improved network throughput
- **ShutUp** — Silences console log spam
- **Scenic** — Improved scene error handling

### Multiplayer & Server (8 mods)
- **ServerCharacters** — Server-side character saves (anti-dupe, anti-cheat)
- **Groups** — Party system with shared map pings and chat
- **Resurrection** — Ritual to bring dead friends back
- **SleepSkip** — Majority-rules night skipping
- **Server devcommands** — Better admin commands and permissions
- **Upgrade World** — Regenerate world locations after game updates
- **QuickConnect** — One-click server join
- **Venture Logout Tweaks** — Safe logout handling

## Keyboard Shortcuts

All mod keybinds have been audited against Valheim's default bindings — nothing shadows a vanilla control. Modifier-based binds only act in their context (build mode, planting, menus) and don't interfere with the base action.

| Key | Mod | Action | Context |
|-----|-----|--------|---------|
| `Alt + Z / X / C` | AzuExtendedPlayerInventory | Use quick slot 1 / 2 / 3 | Anywhere |
| `Alt + V` | AzuExtendedPlayerInventory | Use quick slot 4 | Anywhere (shares base key with vanilla voice chat — low-risk, playtest if mic behaves oddly) |
| `Alt + 3 / 4` | AzuExtendedPlayerInventory | Use quick slot 5 / 6 | Anywhere (moved off `B`/`N` — collided with ESPME/OdinHorse and CircletExtended) |
| `Alt + 1 / 2` | AzuExtendedPlayerInventory | Use quick slot 7 / 8 | Anywhere (Quiver slots on BetterArchery disabled to avoid this) |
| `G` / `H` / `J` | Epic Loot | Magic item ability 1 / 2 / 3 | Anywhere |
| `I` | AdventureBackpacks | Open equipped backpack | Anywhere |
| `L` | AdventureBackpacks | Toggle Wisplight effect | Anywhere |
| `Y` | AdventureBackpacks | Quickdrop backpack contents | Anywhere |
| `N` | CircletExtended | Toggle circlet light | Circlet equipped (moved off `K` = admin fly) |
| `,` (comma) | CircletExtended | Overload circlet flash | Circlet equipped (moved off `T` = Gizmo reset-all) |
| `Ctrl + Left/Right Arrow` | CircletExtended | Narrow / widen beam | Circlet equipped (moved off bare arrows — collided with VNEI recipe-history nav) |
| `Ctrl + Down Arrow` | CircletExtended | Toggle demister | Circlet equipped (moved off bare `DownArrow` — collided with PlantEasily grid resize) |
| `Shift + Left/Right/Up/Down Arrow` | CircletExtended | Toggle shadows / radiance / adjust intensity | Circlet equipped |
| `Middle Mouse` | ShieldBash | Shield bash | While blocking (moved off `F` = vanilla Forsaken Power) |
| `Period` | SkilledCarryWeight | Quick-attach cart | Near cart (moved off `Y` — collided with AdventureBackpacks Quickdrop) |
| `Alt + H` | VNEI | Open item/recipe browser | Anywhere |
| `R` | VNEI | View recipe of hovered item | Menus only (vanilla sheath unaffected) |
| `Left/Right Arrow` | VNEI | Recipe history back / forward | VNEI window |
| `Ctrl + Z` | Recycle N Reclaim | Undo last recycle | Inventory |
| `Delete` | Quick Stack Store | Trash hovered item | Inventory |
| `Shift` (hold) | AzuCraftyBoxes | Craft max / fill all | Crafting menu |
| `Shift` (hold) | Gizmo | Rotate build piece on X axis | Build mode (hammer only — terrain tools stay vanilla) |
| `Alt` (hold) | Gizmo | Rotate build piece on Z axis | Build mode (hammer only — terrain tools stay vanilla) |
| `U` | Gizmo | Reset selected-axis rotation | Build mode (moved off `G` = Epic Loot ability 1) |
| `T` | Gizmo | Reset ALL axis rotations | Build mode |
| `P` | Gizmo | Copy rotation from targeted piece | Build mode |
| `B` | Extra Snap Points | Toggle Manual+ snap mode | Build mode |
| `CapsLock` | Extra Snap Points | Toggle manual closest-snap mode | Build mode |
| `Q` / `E` | Extra Snap Points | Cycle snap point on placing / targeted piece | Manual snap modes only |
| `F11` | Extra Snap Points | Toggle grid snapping | Build mode |
| `F4` | Extra Snap Points | Cycle grid snap precision | Grid snap mode |
| `Shift` (hold) | MassFarming | Mass plant / mass pick | Cultivator / interact |
| `F8` | PlantEasily | Toggle grid planting | Cultivator |
| `F10` | PlantEasily | Toggle grid snapping | Cultivator |
| `F6` | PlantEasily | Toggle auto-replant | Anywhere |
| `RCtrl + Arrows` | PlantEasily | Resize planting grid | Cultivator |
| `Shift` (hold) | PlantEasily | Harvest whole grid | Interact |
| `R` / `T` / `B` | OdinHorse | Remove armor / wait here / saddlebags | Pointing at tamed horse |
| `Alt + 1/2/3` | BetterArchery | Quiver slots | **Disabled** (collides with AzuEPI quick slots) |
| `Alt + click` | Groups | Ping map for your group | Map |
| `Shift` (hold) | Better Cartography Table | Modifier for pin sharing actions | Cartography table |
| `Shift` (hold) | Sailing | Nudge ship | Sailing |
| `F3` | ConfigurationManager | Open in-game mod settings | Anywhere |
| `Ctrl + Semicolon` | TradersExtended | Open trader configuration editor | Anywhere (moved off default `Ctrl + P` — collided with Gizmo's target-piece select) |
| `F7` | AutomaticFuel | Toggle auto-fueling on/off | Anywhere |
| `Alt + scroll` | AdvancedTerrainModifiers | Adjust tool radius | Hoe/cultivator/shovel |
| `Ctrl + scroll` | AdvancedTerrainModifiers | Adjust tool hardness | Hoe/cultivator/shovel |
| `Right Mouse` (hold) | ProjectileTweaks | Zoom while drawing bow/crossbow | Bow drawn (BetterArchery zoom disabled — one zoom owner) |
| `E` | ProjectileTweaks | Cancel bow draw | While drawing only |
| `O` | Server devcommands | Toggle debug mode + no-cost building + god mode | Admin only |
| `K` | Server devcommands | Toggle fly mode | Admin only |
| `Ctrl + Right-click` | Server devcommands | Teleport to map location | Admin only, map open |

Rebind anything in-game: press `F3` → find the mod → change the key (stored in that mod's config file).

## Key Gameplay Rules

- **Death:** SmartSkills grants 75% skill recovery — all other mod skills have 0% death loss.
- **Ore transport:** TeleportEverything charges a 10% transport tax. No portal-bypass mods.
- **Creature stars:** CLLC Hard mode, up to 5 stars, +50% HP / +6% damage per extra player.
- **Seasons:** 7 in-game days per season, full year in ~14 hours of play.
- **Raids:** 36-minute interval at 30% chance (~every 2 hours).

## For Server Admins: World Modifier Recommendation

**Leave Valheim's built-in "Combat" world modifier at its default (Hard) when creating your world. Do not raise it further to try to make the pack harder.**

All of this pack's difficulty is already tuned through CLLC's star system — biome-progressive star chances, per-star HP/damage scaling, and boss star chances are hand-calibrated assuming vanilla's default combat baseline. Vanilla's Combat modifier is a blunt global damage multiplier that has no awareness of stars, biomes, or CLLC's curve — stacking a harsher setting on top compounds unpredictably (worst on high-star Deep North/Mistlands spawns, where CLLC already pushes HP/DMG near its tuned ceiling) and it also scales *player-dealt* damage, which can undercut progression rather than reward it.

If the pack ever feels too easy for your group, adjust difficulty through the config values you can already see and reason about — CLLC's per-star/per-biome percentages in `org.bepinex.plugins.creaturelevelcontrol.cfg` and `config/CreatureConfig.yml`, or Custom Raids frequency — rather than introducing a second, uncontrolled global multiplier from the world-creation screen.

## Installation

**Client:** Install via [r2modman](https://thunderstore.io/c/valheim/p/ebkr/r2modman/) or the Thunderstore App — search for `Fimbulwinter` by `ibfleming`.

**Alternative (profile import):** Each [GitHub release](https://github.com/ibfleming/fimbulwinter/releases) ships a ready-made `.r2z` profile with all mods at pinned versions plus the tuned configs. In r2modman: Profiles → Import / Update → From file.

**Server:** Install all mods except client-only UI/visual mods. A Pelican/Pterodactyl server egg is provided in the [GitHub repo](https://github.com/ibfleming/fimbulwinter) (`server/valheim-fimbulwinter-egg.yaml`) that automates the full dedicated server install: SteamCMD, BepInEx, all server-side mods, and modpack configs.

## Links

- **GitHub:** [github.com/ibfleming/fimbulwinter](https://github.com/ibfleming/fimbulwinter)
- **Issues & suggestions:** [GitHub Issues](https://github.com/ibfleming/fimbulwinter/issues)
- **Changelog:** [CHANGELOG.md](https://github.com/ibfleming/fimbulwinter/blob/main/CHANGELOG.md)
