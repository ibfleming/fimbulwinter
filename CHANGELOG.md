# Changelog

All notable changes to Fimbulwinter will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed — 2026-07-21 full-pack audit
Systematic pass over every config for syntax errors, keybind conflicts,
documented-rule drift, cross-mod contradictions, out-of-range values, and
performance red flags.

- **JSON syntax error**: `EpicLoot/patches/TherzieMods_2.0/Lootables_Gear_Wizardry.json`
  had a trailing comma in the Tier6Circlets loot array — would have failed
  to parse at runtime, silently dropping that entire loot patch
- **Keybind: SkilledCarryWeight quick-cart** (`Y`) collided with
  AdventureBackpacks' own default `Quickdrop Backpack = Y` — pressing Y near
  a cart would also instantly dump your backpack's contents on the ground.
  Moved to `Period`
- **Keybind: CircletExtended beam/demister controls** (bare arrow keys)
  collided with PlantEasily's grid-resize (`RightControl` + arrows) — since
  BepInEx shortcuts fire on their own keys regardless of what else is held,
  every grid-resize keypress while wearing a circlet also adjusted beam
  width or toggled the demister. Added `+ LeftControl` (a distinct KeyCode
  from PlantEasily's `RightControl`)
- **Keybind: AzuExtendedPlayerInventory quick-slots 5 and 6** (`Alt+B`,
  `Alt+N`) collided with OdinHorse Saddlebags / ExtraSnapPointsMadeEasy
  Manual+ Snap (`B`) and CircletExtended Toggle light (`N`) — swapping gear
  mid-build or mid-ride would also fire those. Moved to `Alt+3`/`Alt+4`,
  extending the pack's existing Alt+1/Alt+2 numbering (slots 7-8) instead of
  claiming more letters
- **Keybind: TradersExtended's new 2.0.0 in-game editor** defaulted to
  `Ctrl+P`, colliding with Gizmo's bare `selectTargetPieceKey = P`. Moved to
  `Ctrl+Semicolon`
- **Keybind (highest severity): AzuCraftyBoxes' `Prevent Pulling Logic`**
  defaulted to `Alt+O`, colliding with the admin bind bundle (`O` =
  `debugmode`+`nocost`+`god`, binds.yaml). Any admin using this ordinary
  client convenience mod would accidentally toggle god mode / no-cost
  building / debug mode on themselves. Moved to `Alt+Slash`
- Also previously undocumented in README: AzuExtendedPlayerInventory quick
  slots 4-8 (only 1-3 were ever listed), AdventureBackpacks' Quickdrop key,
  and CircletExtended's beam-width controls — all added to the Keyboard
  Shortcuts table

### Verified (no changes needed)
- All 46 YAML/JSON configs parse cleanly (post JSON fix)
- 556 range-bounded settings checked against their own declared acceptable
  range: zero violations
- 2,701 enum-constrained settings checked against their own declared
  acceptable-values list: zero real violations (one KeyboardShortcut false
  positive from the checker's comma-splitting, not an actual bug)
- Documented pack rules match actual config values exactly: death penalty
  (0% skill loss across all 9 Smoothbrain/blacks7ar skill mods, SmartSkills
  75% recovery), TeleportEverything 10% tax, CLLC (+50% HP/+6% DMG per
  player, splitting 2%, boss stars 15/5/2%), Custom Raids (36min/30%),
  Sailing (125% base, 1.5x at skill 100, raft 2.0x), AdventureBackpacks
  (-0.15 speed on all 8 backpacks), Epic Loot economy (balanced, 20% set
  items, 80/70 unidentified/materials split, boss-gated items and bounties)
- ConditionalConfigSync's SyncPolicy/HiddenConfigs have no stale references
  to the mods removed this week (GammaOfNightLights/BreatheEasy/LazyVikings
  were never ConditionalConfigSync-managed)
- Spawn_That's tracked config stays vanilla-creatures-only per pack policy;
  the auto-generated per-creature sidecar scaffolds are untracked and empty
  by default, so no accidental modded-creature spawner duplication risk
- BetterArchery's `Bow Draw Cancel Hotkey = E` lives inside its already-disabled
  `[Bow Zoom]` section — its apparent overlap with ProjectileTweaks/ESPME's
  own E-key bindings is inert, not a live conflict
- OdinHorse's hover-context R/T/B keys are naturally exclusive with
  Gizmo/ESPME's build-mode-only bindings on the same letters (different
  equip states) — re-confirmed, not a live conflict
- Repair stacking (ComfyAutoRepair + AzuWorkbenchTweaks Auto Repair +
  MyLittleUI repair-on-hold) is redundant but harmless — repairing an
  already-full-durability item is a no-op, so three triggers on one
  interaction cost a negligible amount of overhead, not a bug
- BepInEx logging levels, ShutUp.cfg per-mod overrides, and NetworkTweaks/
  TimeoutLimit/LocalizationCache/container-scan-range settings are all sane;
  no debug-level log spam or excessive scan ranges/intervals found

### Changed
- QuickConnect UI tuned: `ButtonFontSize`/`LabelFontSize` 0→16, `WindowWidth`
  250→384, `WindowHeight` 50→72, `WindowPosX`/`WindowPosY` 20→50 (matches
  the same change applied to Fimbulwinter Lite)

### Tooling
- `scripts/deploy.sh full` now calls `disable_auto_update()` before staging,
  which sets the egg's `AUTO_UPDATE_MODS` startup variable to `0` via the
  Pelican Client API. Fixes a recurring edge case: a `full` deploy pushes
  unpublished local state for testing, but if `AUTO_UPDATE_MODS=1`, the
  post-deploy restart's boot-time `server-autoupdate.sh` could re-sync to
  the latest *published* Thunderstore pack and clobber the test deploy. The
  existing `local-*` manifest-marker skip was meant to prevent this but
  isn't relied on anymore — the variable is now switched off outright.
  **Deploy.sh does not re-enable it automatically** — flip `AUTO_UPDATE_MODS`
  back to `1` yourself once testing is done and you're ready to publish.

### Changed
- warpalicious-More_World_Locations_AIO updated from 5.0.6 to 5.0.7 — MWL
  port, trader, and trainer location pieces set to 9999 health so they can
  no longer be broken for progression skips. No config schema change; no
  action needed on `warpalicious.More_World_Locations_AIO.cfg`.

## [2.0.0] - UNRELEASED

Ground-up rebuild on the Fimbulwinter Lite foundation (103 mods). The entire Lite
QoL/UI/fix/server stack and its tuned configs replace the old equivalents, with
Fimbulwinter's overhaul content (CLLC, Epic Loot, Therzie suite, creatures,
locations, skills) layered back on top. All mods verified non-deprecated against
the Thunderstore API; all versions bumped to latest.

### Added (from Fimbulwinter Lite)
- shudnal-ConditionalConfigSync 1.0.3 (server-enforced config ownership; required by Seasons)
- shudnal-Seasons 1.8.1 (replaces RustyMods Seasonality; 7-day seasons, tuned sync policy)
- shudnal-MyLittleUI 1.2.15 (replaces BetterUI_ForeverMaintained)
- MSchmoecker-VNEI 0.17.5 (item/recipe browser)
- ComfyMods-Gizmo 1.15.0 (build rotation; reset key moved G→U for Epic Loot)
- Searica-Extra_Snap_Points_Made_Easy 2.0.5
- Azumatt-AzuAreaRepair 1.1.6
- Azumatt-AzuMiscPatches 1.2.8
- Azumatt-SleepSkip 1.3.0 (majority-rules night skip)
- ComfyMods-ComfyAutoRepair 1.0.0
- TastyChickenLegs-AutomaticFuel 1.4.8 (torches/ground-pull off, 5m range, F7 toggle)
- k942-MassFarming 1.11.0
- Smoothbrain-Groups 1.2.10 (party system)
- shudnal-LongshipUpgrades 1.0.17 (turrets and 2nd Forsaken power disabled per pack rules)
- Lite server tooling: shared installer (scripts/install-mods.sh), thin Pelican egg
  (server/valheim-fimbulwinter-egg.yaml), deploy.sh, server-autoupdate.sh,
  export-profile.sh, Makefile, permissions.yaml (deny-all default), upgrade_world.cfg

### Removed (deprecated on Thunderstore)
- MSchmoecker-StartupHotfix, KGvalheim-ItemDrawers
- Soloredis-RtDDungeons, RtDHorrors, RtDMonsters, RtDMonstrum (author mass-deprecated the suite; RtDOcean kept)
- Horem-Fee_Fi_Fo_Fum, Horem-MushroomMonsters

### Removed (superseded or unmaintained)
- BetterUI_ForeverMaintained → MyLittleUI
- RustyMods-Seasonality + Willybach-HD_Seasonality (texture pack) → shudnal Seasons
- CacoFFF-LeanNet → NetworkTweaks
- zamboni-Gungnir → Server_devcommands
- Huntardys-EpicValheimsAdditions (unmaintained since 2024-06; overlaps Therzie + official biome content)
- Korppis-ReliableBlock (unmaintained since 2022)
- Digitalroot-Eternal_Fire (redundant with AutomaticFuel; removed fuel gameplay entirely)
- Smoothbrain-TargetPortal (Lite-only convenience; conflicts with the pack's travel-cost design)

### Removed (Vanilla++ preservation — keep vanilla visuals and core gameplay loops)
- shudnal-GammaOfNightLights (night lighting overhaul — vanilla night atmosphere restored)
- RandomSteve-BreatheEasy (smoke/dust/heat-wave removal — vanilla visual effects restored)
- blacks7ar-LazyVikings (auto-feeding/auto-collecting stations removed a core gameplay loop for a veteran pack)

### Changed
- All shared mods now use Lite's newer versions and tuned configs (BepInEx.cfg,
  server_devcommands + binds.yaml/permissions.yaml, AzuEPI quick slots Alt+Z/X/C, etc.)
- Version bumps (previous → now): Jotunn 2.28.0→2.29.2, EpicLoot 0.12.11→0.12.15,
  RtDOcean 2.1.0→2.2.38, More_World_Locations_AIO 4.2.0→5.0.6, OdinShip 0.7.4→0.7.6,
  OdinHorse 1.6.1→1.6.2, SeaAnimals 0.3.4→0.3.6, TradersExtended 1.3.12→2.0.0
  (major: in-game trader editor, YAML/CSV item lists, per-trader currencies and buyback),
  Structure_Tweaks 1.35.0→1.36.0, Bestiary 1.1.5→1.1.6, ShieldBash 1.5.2→1.5.5,
  MissingPieces 2.2.2→2.2.3, PlantEasily 2.0.3→2.1.1, HUDCompass 1.1.7→1.1.9,
  AdventureBackpacks 1.9.12→1.9.13, ConfigurationManager 1.1.13→1.1.15,
  Server_devcommands 1.102.0→1.108.0, Upgrade_World 1.77.0→1.80.0
- Keybind conflict resolutions for the merged pack:
  - Gizmo reset-rotation G→U (G = Epic Loot ability 1)
  - SkilledCarryWeight quick-cart V→Y (V = vanilla voice chat)
  - CircletExtended toggle light K→N (K = admin fly), overload T→Comma (T = Gizmo reset-all)
  - ShieldBash F→Middle Mouse (F = vanilla Forsaken Power)
  - BetterArchery bow zoom disabled (ProjectileTweaks owns zoom); quiver stays disabled
- AdventureBackpacks keeps the original tuned drop lists (CLLC/Epic Loot economy)
- HUDCompass: dynamic map pins stay off (Better Cartography Table owns map pins)
- Epic Loot: bounties now gated by biome boss kills (`Gated Bounty Mode =
  BossKillUnlocksCurrentBiomeBounties`) to match item-drop gating — closes an
  early-game currency leak; economy otherwise verified (balanced template, 20% set
  items, 80% unidentified + 70% materials, global drop rate 1.0)
- CLLC scaling verified: Hard + BossesKilled, 50% HP / 30% DMG per star (bosses
  25/10), biome-progressive star ramps in CreatureConfig.yml, splitting 2%,
  Serpent/Deathsquito/Eikthyr guardrails intact
- AAA Crafting: `Paginator = Off` — mitigates crafting-menu search breaking
  (filtered list could land beyond the current page and render empty)
- ItemConfig.yml: stale "20% tax" comments corrected to the actual 10% TeleportEverything fee
- MyLittleUI: `Show slots space taken = true` — inventory grid now shows free/used slot count

### Fixed
- **ShieldBash keybind was never actually applied.** The repo shipped
  `alexbez.valheim.shieldbash.cfg` (GUID `alexbez.valheim.shieldbash`, a
  different/unrelated ShieldBash build, v2.2.0) — a stale leftover the
  installed `Mexanik-ShieldBash` mod (GUID `mexanik.shieldbash`) never reads.
  All BashKey tuning, including the F→Mouse2 fix, was silently inert; the
  live game still ran BashKey=F colliding with vanilla Forsaken Power.
  Replaced with the correct `mexanik.shieldbash.cfg` (real 1.5.5 schema,
  BashKey=Mouse2 applied). The orphan `alexbez.*` file is deleted.
- Synced 16 configs against a fresh game-launch regen (profile
  `Fimbulwinter-v2.0.0`), pulling forward version-bump schema changes with
  zero loss of tuned values (verified key-by-key before merging):
  Raelaziel.OdinHorse.cfg (1.6.1→1.6.2), Soloredis.RtDOcean.cfg
  (2.1.0→2.2.38), marlthon.SeaAnimals.cfg (+33 new HP/regen keys),
  radamanto.Bestiary.cfg (+216 new per-creature keys), shudnal.TradersExtended.cfg
  (1.3.12→2.0.0, +17 new in-game trader-editor keys), vapok.mods.adventurebackpacks.cfg
  (1.9.10→1.9.13), warpalicious.More_World_Locations_AIO.cfg (4.2.0→5.0.6,
  +1 new key), _shudnal.ConfigurationManager.cfg (1.1.14→1.1.15),
  Searica.Valheim.ExtraSnapPointsMadeEasy.cfg (+290 new per-piece snap
  entries for content added since the merge — Wizardry tables, Armory forge,
  OdinHorse rugs, LongshipUpgrades pulleys, CookingAdditions stations, RtD/TW
  saplings), blacks7ar.CookingAdditions.cfg, Azumatt.SleepSkip.cfg,
  Azumatt.ChangelogEditor.cfg, bruce.valheim.comfymods.gizmo.cfg (also
  picked up `isLocalFrameModeEnabled = true` from live playtesting),
  org.bepinex.plugins.{farming,mining,foraging,resurrection}.cfg
- `.gitignore`: corrected `config/EpicLoot/MWL_Ports/` → `config/MWL_Ports/`
  (More World Locations writes port data at config root, not inside
  EpicLoot/); added ignores for Neobotics/, TherzieTranslations/, and
  LongshipUpgrades' asset-dump images/folders — all runtime-extracted,
  non-customized data confirmed present in a live profile
- Left untouched (repo already correct, live profile was simply stale):
  randyknapp.mods.epicloot.cfg (repo has the 2026-07-20 bounty-gating fix;
  live pre-dates it), ItemConfig.yml (repo has the 10%-tax comment fix),
  org.bepinex.plugins.sailing.cfg and drop_that.cfg (repo's design-rationale
  comments are stripped by BepInEx's own regen but no values differ — kept
  the documented version), ShutUp.cfg (live picked up log-level entries for
  BreatheEasy/GammaOfNightLights/LazyVikings because that profile still has
  their orphaned DLLs installed — resolves on next full mod resync),
  org.bepinex.plugins.servercharacters.cfg (repo's empty `Server key` is
  intentional; never commit a live key)

## [1.6.1] - 2026-03-13

### Changed
- ValheimModding-Jotunn updated from 2.27.1 to 2.28.0
- shudnal-ConfigurationManager updated from 1.1.12 to 1.1.13
- JereKuusela-Upgrade_World updated from 1.76.0 to 1.77.0
- Soloredis-RtDOcean updated from 1.5.2 to 2.1.0 (major rewrite -- creature factions reassigned, RtDItems decoupled)
- Soloredis-RtDDungeons updated from 1.0.0 to 1.0.3
- Soloredis-RtDHorrors updated from 0.4.9 to 0.5.1
- Soloredis-RtDMonsters updated from 2.2.8 to 2.3.1 (~50% polygon reduction, remodeled enemies)
- Soloredis-RtDMonstrum updated from 0.8.1 to 0.8.4
- OdinPlus-OdinHorse updated from 1.5.8 to 1.6.1 (speed system reworked, new horse bite attack, saddlebag support)
- RustyMods-Seasonality updated from 3.7.9 to 3.8.0
- shudnal-GammaOfNightLights updated from 1.0.8 to 1.0.9
- Vapok-AdventureBackpacks updated from 1.9.10 to 1.9.12 (backpack nesting now blocked)
- Azumatt-AzuExtendedPlayerInventory updated from 2.3.7 to 2.4.1
- Azumatt-AzuCraftyBoxes updated from 1.8.13 to 1.8.14
- Azumatt-Recycle_N_Reclaim updated from 1.3.10 to 1.4.0 (new undo recycle feature, tooltip yield preview)
- Radamanto-Bestiary updated from 1.1.4 to 1.1.5

### Fixed
- OdinHorse: Reset Speed Modifier from 7 to 1 (field changed from absolute value to multiplier in v1.6.0)
- Fixed game crashing because of QuickConnect and its configuration file

## [1.6.0] - 2026-02-24

### Added
- KGvalheim-ItemDrawers 1.2.0 -- Single-item bulk storage drawers with visual display (works with AzuAutoStore)
- Azumatt-ChangelogEditor 1.0.9 -- Customize or hide the main menu changelog (client-only)
- bdew-QuickConnect 1.7.0 -- Quick connect window with configurable server list (client-only)

### Changed
- Seasonality: Disabled Sleep Override so seasons rotate automatically on a timer instead of requiring players to sleep
- Seasonality: Changed season duration from 3 in-game days to 4 real-time hours per season (16-hour full year cycle)
- HUDCompass: Set Player Pin Visibility to ForceOff and Show My Player Pin to false (fixes red player icon appearing on map/minimap)

## [1.5.1] - 2026-02-24

### Changed
- RandyKnapp-EpicLoot updated from 0.12.10 to 0.12.11
- warpalicious-More_World_Locations_AIO updated from 4.1.1 to 4.2.0
- Mexanik-ShieldBash updated from 1.5.1 to 1.5.2

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
