# Fimbulwinter - server-side-first Valheim modpack

Quality of life, building tools and biome backpacks for Valheim, built on one rule: **if the server
can do it, the server does it.** Most of the pack runs on the dedicated server, so players install as
little as possible and stay close to vanilla.

One exception: Jotunn and Vapok-AdventureBackpacks run on both sides -- see "AdventureBackpacks" below.

## Installation

**Via Thunderstore / r2modman or the Thunderstore Mod Manager (recommended):** search "Fimbulwinter"
and install/update like any other modpack. Dependencies resolve automatically.

**Manual `.r2z` import:** if you were handed a `.r2z` profile file directly, open r2modman -> Profiles
-> Import/Update -> From file -> select the file -> Import as new profile (or Update existing, if
you're updating a profile that already has this pack).

**Hosting the dedicated server:** see "For server admins" below.

## The split

Only 18 packages reach players. The other 7 live on the dedicated server and are excluded from the
client profile automatically.

### Client (18)

| Package | Version | Role |
|---|---|---|
| denikson-BepInExPack_Valheim | 5.4.2350 | loader |
| ValheimModding-YamlDotNet | 16.3.1 | library |
| shudnal-ConditionalConfigSync | 1.0.8 | server-enforced config |
| ValheimModding-Jotunn | 2.30.1 | library -- both sides, see "AdventureBackpacks" |
| **Vapok-AdventureBackpacks** | 2.1.4 | tiered biome backpacks -- **required for every player**, see below |
| **shudnal-MyLittleUI** | 1.2.22 | tooltips, production timers, chest preview, multicraft, weather |
| **shudnal-ExtraSlots** | 1.2.12 | equipment + quick slots |
| **Toxo-CraftFromChests** | 0.4.0 | craft/build/fuel from nearby chests |
| **Neobotics-HUDCompass** | 1.2.0 | compass bar |
| **JoelOliMclean-NoRainDamage** | 1.3.0 | no weather decay on builds |
| **korCaptain-NullReferenceFix** | 1.0.20 | stability |
| **JereKuusela-Server_devcommands** | 1.113.0 | admin console on a dedicated server (see below) |
| **Crystal-DeathPenalty** | 1.3.1 | tunes skill loss on death |
| **cjayride-RecycleItemsIntoParts** | 1.7.3 | recycle items into parts (drag + `Delete`) |
| **ComfyMods-Gizmo** | 1.16.0 | free build-piece rotation on all three axes |
| **Searica-Extra_Snap_Points_Made_Easy** | 2.1.0 | extra snap points, manual/grid snapping |
| **Ostrix-AdvancedTerrainModifiersCompatible** | 1.4.8 | square hoe/cultivator tools, radius + hardness scroll, precision raise, terrain reset |
| **Zenox-ServerConnect** | 1.0.7 | one-click main-menu connect button |

### Server only (7) - players install none of these

| Module | Version | Role |
|---|---|---|
| ArgusMagnus-ServersideQoL | 2.0.13 | (suite core) |
| `_AutoStore` | 2.0.11 | auto-pickup, auto-sort, stack-to-chest |
| `_ContainerSizes` | 2.0.11 | bigger chest grids |
| `_AutoProcess` | 2.0.11 | auto-feed smelters/kilns from nearby chests |
| `_LetItFloat` | 2.0.11 | items float instead of sinking |
| `_JustSleep` | 2.0.11 | majority-vote sleep skip |
| `_MultiplayerTweaks` | 2.0.11 | desync fixes (ownership assignment) |

Server-authoritative and works with **unmodded and console clients**, so none of it costs a player
anything to install.

## AdventureBackpacks, and why it's required

Six biome-tiered backpacks, each an equipped item (not an inventory slot -- see the caveat below) that
adds carry capacity at a movement-speed cost:

| Tier | Biome | Station | Perk |
|---|---|---|---|
| Satchel | Meadows | Workbench | -- |
| Rugged Backpack | Black Forest | Forge | -- |
| Bloodbag Wetpack | Swamp | Forge | Waterproof (no "Wet" debuff) |
| Arctic Sherpa Pack | Mountain | Forge | Frost/Cold Resistance |
| Lox Hide Knappsack | Plains | Forge | -- |
| Explorers Wisppack | Mistlands | Black Forge | Built-in Demister + Slow Fall |

Each tier has 4 upgrade levels at its crafting station (bigger grid each time) -- upgrade what you
have before jumping to the next biome's tier. Every tier costs -15% movement speed while worn, and
halves the weight of its own contents (0.5x weight multiplier) -- that trade-off is the balance, not a
bug.

**Keys:** `I` opens/closes the equipped backpack; the backpack also opens automatically alongside your
main inventory. `Y` quick-drops it (detach and drop behind you). `L` toggles the Wisppack's Demister
in Mistlands.

**Craft and store straight from the backpack:** crafting and building pull materials
from your inventory first, then the equipped backpack; newly crafted items land in the backpack when
your inventory is full; picked-up items auto-store into the backpack if it already holds that item, and
overflow into it when your inventory fills up. All four are on by default and server-synced.

**Telemetry is off in this pack.** AdventureBackpacks ships an opt-out crash/error reporter
(`Send Error Reports`) that defaults to **on** upstream and makes outbound HTTP calls; this pack ships
it set to `false`, along with `Enable Anonymous Telemetry = false` (already the upstream default) and
the startup splash screen disabled.

**Caveat: it occupies the Cape/Shoulder slot**, not a separate dedicated slot -- you cannot wear a
backpack and a cape at the same time. The mod's own item data confirms this (backpacks are typed as
capes internally). There's no config option to change this; the Arctic Sherpa Pack's own
Frost/Cold Resistance perk exists specifically to compensate for the cape-based cold resistance you'd
otherwise lose.

**Why this one requires every player to match exactly:** unlike the rest of this pack,
AdventureBackpacks enforces itself on both client and server with built-in version checking -- a
mismatched or missing install is rejected on connect, not silently degraded. If you're setting up a
server yourself, this is the one mod you cannot make optional.

## One-click server connect (Zenox-ServerConnect)

Adds a button above "Start Game" on the main menu that connects straight to a configured server
address and password, skipping the server browser.

**Its config holds a real address and password in plain text and is never part of this repository or
the shared `.r2z`.** `BepInEx/config/zenox.serverconnect.cfg` generates its own placeholder defaults
(`127.0.0.1:2456` / `changeme`) the first time it runs -- fill in the real values yourself, in your own
profile, after installing.

## For server admins

```bash
make profile                 # build the client .r2z from thunderstore.toml
bash scripts/deploy.sh full  # push mods + config to a Pelican-panel dedicated server
```

`scripts/deploy.sh` talks to the Pelican panel Client API (`.env`: `PANEL_URL`, `PELICAN_CLIENT_KEY`,
`SERVER_ID`) and needs `.env` filled in from `.env.example`. `server/fimbulwinter-egg.yaml` is a
self-contained Pelican egg (Valheim + BepInEx only; mods/config reach the server exclusively through
`deploy.sh`).

### Why Server_devcommands is required

Vanilla gates every cheat command behind `Terminal.IsCheatsEnabled()`, which requires the caller to
*be* the server -- a connected player on a dedicated server never is, so `god`/`fly`/`debugmode` are
rejected regardless of adminlist.txt (being an admin grants kick/ban, not client cheats).
Server_devcommands patches that gate and must be installed on **both** sides: the console it patches is
client-side, permissions are enforced server-side.

### ServersideQoL tuning

The suite ships mostly inert by default -- values below are what this pack turns on.

| Module | Setting | Value | Why |
|---|---|---|---|
| AutoStore | `AutoPickup` | true | off by default -- the headline feature |
| AutoStore | `AutoPickupRange` | 20 | |
| AutoStore | `StackInventoryIntoContainersEmote` | -2 (any emote) | most reliable across crossplay |
| AutoStore | `AutoSort` | true | |
| AutoProcess | `FeedFromContainersRange` | 15 | default of 4 is uselessly tight |
| AutoProcess | `CapacityMultiplier` / `TimePerProductMultiplier` | 1 / 1 | no smelting speed/capacity cheats |
| JustSleep | `RequiredPlayerPercentage` | 51 | majority rather than unanimous |
| MultiplayerTweaks | `AssignInteractablesToClosestPlayer`, `AssignMobsToClosestPlayer`, `AssignShipsToCaptain` | true | desync fixes |
| MultiplayerTweaks | `ForcePlayerMapPin` | false | left vanilla -- a visibility change, not a fix |
| ContainerSizes | wood `5x3`, reinforced `6x5`, blackmetal `8x6`, karve `4x2`, longship `6x4` | | |

Untouched, still vanilla: personal chest, barrel, cart, wardrobe, grausten chest, Ashlands ship, pots
and gifts. The infinite-expanding `+` container variant is not used anywhere in this pack.

### Crystal-DeathPenalty tuning

`config/dev.crystal.deathpenalty.cfg`, all four keys server-enforced (change via `deploy.sh configs`).

| Key | Value | Vanilla |
|---|---|---|
| `SkillLossPercent` | **2** | 5 |
| `MercyEffectDuration` | 600 | 600 |
| `SafetyEffectDuration` | 50 | 50 |
| `ResetLevelProgress` | true | true |

Vanilla's 5% compounds harshly on this pack's combat-hard preset; 2% keeps death meaningful without
being crushing (a level-30 skill loses roughly half a level per death).

## cjayride-RecycleItemsIntoParts

Drag an item onto the cursor and press `Delete` to recycle it into its crafting materials. Config at
`config/cjayride.RecycleItemsIntoParts.cfg`, shipped at mod defaults (100% resource return, coins
excluded, consumables/trophies/shards included).

It needs *some* resolvable recipe to act -- raw materials and recipe-less drops just print "Cannot be
recycled or unknown recipe" and are left alone. There's no "delete anything, return nothing" option.

## Keyboard Shortcuts

| Key | Mod | Action | Context |
|-----|-----|--------|---------|
| `Alt + Z / X / C / V` | ExtraSlots | Quick slots 1-4 | Anywhere |
| `Alt + U` | ExtraSlots | Quick slot 5 | Anywhere |
| `Alt + Y` | ExtraSlots | Quick slot 6 | Anywhere |
| `Alt + 1 / 2 / 3` | ExtraSlots | Ammo slots 1-3 | Anywhere |
| `Alt + Q / E / R` | ExtraSlots | Food slots 1-3 | Anywhere |
| `Alt` (hold) | ExtraSlots | Drag item between equipment slots | Inventory open |
| `J` | HUDCompass | Toggle the compass bar | Anywhere |
| `Delete` | RecycleItemsIntoParts | Recycle the item on the cursor | Inventory open |
| `LeftShift` (hold) + scroll | Gizmo | Rotate piece on X axis | Build mode, hammer |
| `LeftAlt` (hold) + scroll | Gizmo | Rotate piece on Z axis | Build mode, hammer (terrain tools use this key for ATM instead) |
| `G` / `T` | Gizmo | Reset selected axis / reset all axes | Build mode |
| `` ` `` (BackQuote) | Gizmo | Cycle rotation mode (default / roof / local-frame) | Build mode |
| `P` | Gizmo | Copy targeted piece's rotation | Build mode |
| `PageUp` / `PageDown` | Gizmo | Snap divisions +/- | Build mode |
| `B` | ExtraSnapPointsMadeEasy | Toggle Manual+ snap mode | Build mode |
| `CapsLock` | ExtraSnapPointsMadeEasy | Toggle Manual snap mode | Build mode |
| `F11` / `F4` | ExtraSnapPointsMadeEasy | Toggle grid snap / cycle grid precision | Build mode |
| `Q` / `E` | ExtraSnapPointsMadeEasy | Iterate placing / targeted snap points | Manual snap modes |
| `LeftAlt` (hold) + scroll | AdvancedTerrainModifiers | Change tool radius | Hoe / cultivator / shovel |
| `LeftControl` (hold) + scroll | AdvancedTerrainModifiers | Change tool hardness | Hoe / cultivator / shovel |
| `I` | AdventureBackpacks | Toggle equipped backpack | Anywhere |
| `Y` (bare) | AdventureBackpacks | Outward quick-drop the backpack | Anywhere |
| `L` | AdventureBackpacks | Toggle Demister (Explorers Wisppack only) | Mistlands |
| `O` | Server devcommands | Admin bundle: `debugmode` + `nocost` + `god` | Admins only |
| `K` | Server devcommands | Admin `fly` toggle | Admins only |

Free keys for future additions: `U` (bare), `F3`, `F6`, `F7`, `F8`, `F10`. Rationale for every moved
bind (and why some near-misses aren't actually conflicts) is in `docs/DECISIONS.md`.

## Optional additions

Not part of the pack, but known to work alongside it if you want to add them to your own profile:

- `Advize-PlantEverything` -- plant every resource
- `Advize-PlantEasily` -- grid planting
- `Crystal-DigDeeper` -- deeper digging
- `shudnal-ConfigurationManager` -- in-game config editor (needs JsonDotNET)
- `MSchmoecker-VNEI` -- item browser
- `ArgusMagnus-ServersideQoL_ContainerSigns` -- chest labels (server)
- `ArgusMagnus-ServersideQoL_PortalProgression` -- ores through portals by boss progress (server;
  mutually exclusive with `-modifier portals casual`)

## Credits

Fimbulwinter bundles the work of a lot of mod authors. Thank you, in package order:

denikson & the BepInEx team, ValheimModding (Jotunn, YamlDotNet), shudnal (ConditionalConfigSync,
MyLittleUI, ExtraSlots), Toxo (CraftFromChests), Neobotics (HUDCompass), JoelOliMclean
(NoRainDamage), korCaptain (NullReferenceFix), JereKuusela (Server_devcommands), Crystal
(DeathPenalty), cjayride (RecycleItemsIntoParts), ComfyMods (Gizmo), Searica
(Extra_Snap_Points_Made_Easy), Ostrix (AdvancedTerrainModifiersCompatible), Zenox (ServerConnect),
ArgusMagnus (ServersideQoL and its modules), Vapok (AdventureBackpacks).

Every mod here is redistributed unmodified, resolved from Thunderstore at build time -- this repo
ships only the configuration tuned for this pack. See each mod's own Thunderstore page for its
license and full credits.
