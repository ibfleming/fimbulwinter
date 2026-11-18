# Decisions

Why Fimbulwinter is the way it is. This is the rationale record, kept out of
README.md and CHANGELOG.md so those stay readable for players, while the
evidence behind each call stays available to whoever maintains the pack.
Add to this file rather than letting README/CHANGELOG grow a diary.

## Server-side first

If the dedicated server can do something, the server does it. Players install
as little as possible, and unmodded or console clients are never locked out of
the server-side features. The ArgusMagnus ServersideQoL suite carries most of
the quality of life for exactly this reason: storage, smelting, floating
items, sleep voting and desync fixes are all server-authoritative.

## Jotunn

Jotunn is only in the pack because two mods need it:

- **Ostrix-AdvancedTerrainModifiersCompatible** (client-only). It works
  without Jotunn on the server: terrain syncs through vanilla RPCs, and
  Jotunn's compatibility handshake is skipped when the server doesn't run it.
- **Vapok-AdventureBackpacks** (both sides). Its own README requires it on
  client and server with built-in version checking, which puts Jotunn on the
  server too. This is a deliberate tradeoff: AdventureBackpacks is the one mod
  in the pack that can turn a mismatched or missing client away on connect.

## Terrain tools: why the ATM fork

Square hoe/cultivator brushes are a hard requirement. The original
Searica-AdvancedTerrainModifiers is unmaintained (last release 2024-12, pinned
to Jotunn 2.22). Alternatives evaluated:

- `Heimlife-Flattenheim` -- no Jotunn, but its `Shape: Square/Circle` option
  only applies to its pickaxe-flatten tool (the DLL's hoe/cultivator radius
  hook never sets `m_square`).
- VentureValheim `Pathside_Assistance` + `Venture_Terrain_Reset` -- trusted
  author, no dependencies, but circular brushes only.
- `disregardthatisuck-PreciseRotation`, `PONEIS-TerrainShaperPlus`,
  `MathiasDecrock-PlanBuild` -- all pull in Jotunn or HookGenPatcher for less
  than the fork provides.

`Ostrix-AdvancedTerrainModifiersCompatible` is a fork of ATM 1.4.1 (commit
`e773c62`) with the same plugin GUID, and the only Valheim 1.0 option with
square tools. It carries Thunderstore's "AI Generated" tag, but on a
compatibility shim over Searica's original gameplay code rather than an
AI-written rewrite.

## ATM config must stay plain ASCII

`Searica.Valheim.TerrainTools.cfg` once carried zero-width-space characters
on several section headers (a ConfigurationManager artifact). Three keys --
`RadiusModifier`, `HardnessModifier`, `Shovel` -- were orphaned by it, and
their values were silently never read. The file is clean now (0/28 keys
missing against the DLL via `strings -e l`). Any edit to this file should be
confirmed in-game, not trusted from the file alone.

A headless harvest of the pinned ATM version (the mod writing its own config
from scratch) puts zero-width characters in five of its six section names and
in the `RadiusModifier`, `HardnessModifier` and `Shovel` key names. The plain
file still works: checked in game on 2026-11-15, `MaxRadius = 20` takes effect
(Alt+scroll goes past radius 10). So the file stays plain ASCII, and the
config migration (`scripts/pipeline/config_diff.py`) keeps any plain-ASCII
file plain instead of copying the mod's spelling, flagging the difference for
an in-game check.

ESPME ships per-piece extra-snap-point toggles for every ATM terrain-tool
variant, gated by one master switch, `Extra Snap Points: Terrain`, which this
pack turns on. The six plain-circle ATM tool variants (`raise_v2`,
`mud_road_v2`, `path_v2`, `paved_road_v2`, `cultivate_v2`, `replant_v2`) are
listed explicitly at their defaults rather than left to auto-populate.

## Recycling: why RecycleItemsIntoParts

`TastyChickenLegs-RecyclePlus` was rejected: it recycled a plain club (6 wood)
into a Wooden Battle Idol, 100% reproducibly. Valheim 1.0's refinement forge
has recipes that consume idols, and RecyclePlus resolves materials through
`GetRecipe`, picking up the refinement recipe instead of the crafting one.
Nothing in its config could prevent it.

`cjayride-RecycleItemsIntoParts` fixes the same case on its own (its 1.7.2
changelog) and passes the club test: craft a plain club, recycle it, get wood
back and nothing else. Re-run that test after any update to it. It has no
"discard anything" option -- the DLL exposes 8 config keys and needs a
resolvable recipe to act at all.

## Mods evaluated and rejected

- **Swmarly-SwmarlyValheimQOL** -- boots clean alongside ServersideQoL, but
  duplicates four behaviours already covered (floating items, sleep-skip
  voting, no rain damage, eternal fires) and carries the "AI Generated" tag
  with little history. Worth revisiting if it matures.
- **VitByr-VBNetTweaks** -- its own README lists Searica NetworkTweaks' GUID
  as a hard incompatibility, and it carries the "AI Generated" tag with little
  history.
- **BentoG-MissingPieces** -- writes custom prefabs into the world; removing
  it later leaves holes in existing builds.

## Keybinds

The current bind table is in README.md "Keyboard Shortcuts". Why the
non-default binds are where they are:

- **ExtraSlots quick slots 5/6 on `Alt+U`/`Alt+Y`.** The mod's defaults
  collide with its own food slots (`Alt+Q`, `Alt+R`); the food row keeps
  `Alt+Q/E/R`.
- **HUDCompass toggle on bare `J`.** Its default `Alt+C` collides with
  ExtraSlots quick slot 3.
- **ExtraSlots `Rebind Connect Panel = F2`.** This is vanilla's own F2
  performance HUD (FPS/ping/ZDOs) exposed through ExtraSlots' config, not a
  conflict. Leave it on F2.
- **Gizmo reset on `G`.** `V` is vanilla voice chat.
- **ESPME Manual+ toggle on `B`.** Its default `LeftAlt` is Gizmo's z-rotate
  hold and ATM's radius-scroll modifier.
- **Gizmo and ATM both use `LeftAlt`+scroll in build mode.** Resolved by
  Gizmo's `ignoreTerrainOpPrefab = true`: Gizmo doesn't activate on
  terrain-modifying tools, so the scroll goes to ATM whenever a terrain tool
  (not the hammer) is equipped.
- **Admin binds on plain letters** (`O` = `debugmode`+`nocost`+`god`, `K` =
  `fly`). F9-F12 are common Steam Input, overlay and macro-software hotkeys
  that can swallow the keypress before Valheim sees it.

## Maintenance pipeline and release notes

- **Scripts first, AI last.** Everything checkable is a script: update and
  deprecation detection, changelog slices, the DLL key check, headless boot
  tests, the 3-way config migration and the keybind audit. The Claude step
  only resolves what the scripts flag and writes notes, which keeps it cheap
  enough for a Pro plan and keeps every run reproducible locally.
- **One rolling PR, not one per mod.** A single branch, `bot/maintenance`,
  with one commit per mod so any one can be reverted. Releases younger than
  48 hours are skipped (authors here often ship same-day hotfixes), and the
  batch runs weekly unless a new Valheim build or a deprecation makes it
  urgent.
- **Headless harvest for config defaults.** A dedicated server with every
  mod, client-only ones included, and an empty config writes fresh defaults
  for nearly every mod, so config migration doesn't need a game client.
  Settings a mod only creates in a client (ESPME's per-piece toggles, some
  ATM tool entries) are kept as shipped rather than treated as removed.
- **changie for players, git-cliff for developers.** Player notes are small
  files written and reviewed in the PR, because commit subjects for a
  modpack are mostly "bump X" and make poor player notes. semantic-release
  and release-please were rejected: both build notes from commits only, and
  semantic-release would tag and publish on every merge. git-cliff supplies
  only the commit list in the GitHub Release.

## Maintenance batch 2026-11-18 (review notes)

- **RecycleItemsIntoParts 1.8.10 return rate.** 1.8.x changed the default `ReturnResources` from `1`
  to `0.4`, and because the shipped `1` matched the old default, the 3-way merge took `0.4`. The
  owner chose to keep full return: `ReturnResources = 1` is now a deliberate override, not a
  default, so later migrations keep it. `ServerEnforced` is irrelevant: the mod is client-only, no server copy
  exists. `RequireConfirm = true` adds a Yes/No popup (Enter/Escape). The EpicLoot settings do
  nothing, EpicLoot is not in the pack.
- **ExtraSlots 1.2.24.** The three dropped `[Mods compatibility - Valheim Radial]` keys are
  intentional: upstream removed ValheimRadial support in 1.2.19. No rename target exists. The new
  hotbar row switching is off (`Switch inventory rows = false`), so its default binds (`LeftAlt`
  hold, `PageUp`/`PageDown`) are inert and the keybind audit overlap with Gizmo/ATM/MyLittleUI is
  harmless. If a player enables it, move `Previous/Next row shortcut` off `PageUp`/`PageDown` (Gizmo
  snap divisions).
- **MyLittleUI 1.2.34 `LeftAlt` binds.** `Link item modifier` (`LeftAlt` + click an inventory item)
  shares Alt with ExtraSlots' equipment drag key. Different gestures (click vs drag) but the same
  hold key in the same window, so it is a playtest item rather than rebound. `Original tooltip
  shortcut` is disabled by default and `Hold to inspect chat modifier` needs `LeftControl` too.
- **HUDCompass 1.2.1 `LeftShift`.** Map-naming modifier, map context only. Gizmo and ESPME use Shift
  in build mode. Harmless.
- **ExtraSnapPointsMadeEasy 2.2.0.** Our binds (`B`, `CapsLock`, `F11`, `F4`) are kept, the mod's new
  defaults (`F3`, `F4`, `Q`) collide with the existing `Q` iterate bind and are not adopted. New
  `Reverse Cycling Direction = LeftShift` only acts together with the cycle keys. The mod writes plain
  ASCII section names, so the stray zero-width character that was in the `[3 - Extra Snap Points]`
  header of our old file is gone and the section now matches the mod's own fresh config;
  `Extra Snap Points: Terrain = true` is preserved. Verify in game that the terrain snap points work.
- **Server_devcommands 1.116.** `Automatic item pick up` changed type from a boolean to
  `Default/On/Off`. Our old value was the old default (`true`), so it moves to `Default` (do nothing),
  which is what upstream now intends. `Automatic devcommands = false` is untouched.
- **AutoStore 2.5.1.** `PickedUpMessageType = TopLeftNear` kept (ours, still a valid value).
- **Zenox-ServerConnect 1.0.14.** The new server-status check on the button sends a query to the
  configured server and, with `PlayFabFallback` (default on), asks PlayFab for the server, the same
  lookup the game does when joining by IP. Defaults stay; there is no shipped config for this mod.
- **NullReferenceFix 1.0.50.** Adds and removes patches often (tooltip handling added, removed, added
  again; ItemDrawers patch reverted for server lag). Boots clean, 108 h old at review. Treated as
  needs-playtest rather than held.
- **Valheim build.** Boot test passed on build 26266951; `ci/valheim-build` is left to the workflow.
