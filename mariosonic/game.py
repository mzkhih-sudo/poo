"""Interactive Mario and Sonic crossover adventure."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Iterable, List, Optional, Sequence


@dataclass
class Character:
    """A playable hero with a unique ability."""

    name: str
    title: str
    franchise: str
    description: str
    ability_name: str
    ability_description: str
    ability_story: str

    def ability_text(self, context: Optional[str] = None) -> str:
        """Return a narrated description of the character using their ability."""

        base = (
            f"{self.name} unleashes {self.ability_name}! "
            f"{self.ability_story} {self.ability_description}"
        ).strip()
        if context:
            return f"{base} {context}".strip()
        return base


@dataclass
class StorySegment:
    """Metadata describing a major chapter in the adventure."""

    name: str
    location: str
    objective: str
    boss: str
    introduction: str
    completion: str


class GameEngine:
    """Text-based crossover adventure starring Mario and Sonic."""

    def __init__(
        self,
        *,
        characters: Sequence[Character],
        storyline: Sequence[StorySegment],
    ) -> None:
        self.characters: List[Character] = list(characters)
        self.storyline: List[StorySegment] = list(storyline)
        self.inventory: List[str] = []
        self.mushrooms: int = 0
        self.hero: Optional[Character] = None
        self.story_log: List[str] = []
        self.quit_game: bool = False
        self.level_handlers: Dict[str, Callable[[StorySegment], bool]] = {}
        self.current_level: Optional[StorySegment] = None

    # ------------------------------------------------------------------
    # Setup helpers
    # ------------------------------------------------------------------
    def log_event(self, message: str) -> None:
        """Record a moment in the adventure's running log."""

        self.story_log.append(message)

    def show_characters(self) -> None:
        """Print the roster of available characters."""

        print("\nChoose your hero for the crossover quest:\n")
        for index, character in enumerate(self.characters, start=1):
            print(f"{index}. {character.name} — {character.title} ({character.franchise})")
            print(f"   {character.description}")
            print(
                f"   Ability: {character.ability_name} — {character.ability_description}\n"
            )

    def choose_character(self) -> Optional[Character]:
        """Prompt the player to select a hero."""

        if not self.characters:
            print("No characters are available for selection.")
            return None

        while True:
            try:
                choice = input("Select a hero by number (or type 'quit'): ").strip()
            except EOFError:
                self.quit_game = True
                print("\nInput stream closed. Ending the adventure.")
                return None

            if not choice:
                continue

            lowered = choice.lower()
            if lowered in {"quit", "q", "exit"}:
                self.quit_game = True
                print("You decide to postpone the crossover. See you next time!")
                return None

            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(self.characters):
                    hero = self.characters[index]
                    self.hero = hero
                    print(
                        f"\n{hero.name} steps forward! {hero.title}.\n"
                        f"Special Ability: {hero.ability_name} — {hero.ability_description}\n"
                    )
                    self.log_event(f"Hero chosen: {hero.name}.")
                    return hero

            print("That option isn't available. Try again or type 'quit'.")

    def use_hero_ability(self, context: Optional[str] = None) -> bool:
        """Trigger the currently selected hero's unique ability."""

        if not self.hero:
            print("No hero has been selected yet!")
            return False

        narration = self.hero.ability_text(context)
        print(narration)
        self.log_event(narration)
        return True

    def add_mushroom(self, label: str, found_at: str) -> None:
        """Add a mushroom to the inventory and narrate the find."""

        self.mushrooms += 1
        item = f"{label} ({found_at})"
        self.inventory.append(item)
        message = (
            f"Collected {label} near {found_at}. Total mushrooms: {self.mushrooms}."
        )
        print(message)
        self.log_event(message)

    def show_inventory(self) -> None:
        """Display the player's current inventory."""

        print("\n--- Inventory ---")
        if not self.inventory:
            print("(Empty)")
        else:
            for item in self.inventory:
                print(f"- {item}")
        print("-----------------\n")

    def show_status(self) -> None:
        """Print current adventure status."""

        hero_name = self.hero.name if self.hero else "None"
        current_level = self.current_level.name if self.current_level else "None"
        objective = self.current_level.objective if self.current_level else "Begin the journey."
        print("\n=== Adventure Status ===")
        print(f"Hero: {hero_name}")
        print(f"Location: {current_level}")
        print(f"Objective: {objective}")
        print(f"Mushrooms collected: {self.mushrooms}")
        print(f"Inventory items: {len(self.inventory)}")
        print("========================\n")

    def _print_help(self) -> None:
        """Show a list of general purpose commands."""

        print(
            "\nCommon commands: status, inventory, ability, help, quit. "
            "Most stages also list unique actions that advance the story.\n"
        )

    def _handle_common_command(self, choice: str, *, allow_ability: bool = True) -> bool:
        """Handle commands that are available in every stage."""

        normalized = choice.lower().strip()
        if normalized in {"status", "s"}:
            self.show_status()
            return True
        if normalized in {"inventory", "bag", "i"}:
            self.show_inventory()
            return True
        if allow_ability and normalized in {"ability", "power", "a"}:
            self.use_hero_ability()
            return True
        if normalized in {"help", "h"}:
            self._print_help()
            return True
        if normalized in {"quit", "exit", "q"}:
            self.quit_game = True
            print("You retreat for now. The Mushroom Kingdom and Mobius await your return!\n")
            return True
        return False

    # ------------------------------------------------------------------
    # Gameplay
    # ------------------------------------------------------------------
    def play(self) -> None:
        """Run the interactive adventure."""

        print(
            "\nMario & Sonic: Warpstar Rush\n"
            "A crossover quest to save the Mushroom Kingdom and Mobius!\n"
        )
        self.show_characters()
        hero = self.choose_character()
        if not hero or self.quit_game:
            return

        print(
            "With alliances formed, a shimmering Warp Star beckons.\n"
            "Four major stages stand between peace and chaos!\n"
        )

        for segment in self.storyline:
            if self.quit_game:
                break
            self.current_level = segment
            print(f"\n=== {segment.name} ({segment.location}) ===")
            print(segment.introduction)
            handler = self.level_handlers.get(segment.name)
            success = True
            if handler:
                success = handler(segment)
            if not success or self.quit_game:
                break
            print(segment.completion)

        if (
            not self.quit_game
            and self.storyline
            and self.current_level == self.storyline[-1]
        ):
            self._print_epilogue()

    # ------------------------------------------------------------------
    # Level handlers
    # ------------------------------------------------------------------
    def _level_mushroom_meadows(self, segment: StorySegment) -> bool:
        """Opening chapter: gather mushrooms to power the Warp Star."""

        required = 3
        search_points = [
            (
                "the sunlit hill",
                "You crest a grassy hill where Mario's classic bricks float beside Green Hill palmtrees.",
            ),
            (
                "the sparkling river",
                "Rippling water reflects Sonic's rings as you scoop up a glowing mushroom from the bank.",
            ),
            (
                "the Goomba burrow",
                "A squad of helmeted Goombas tumble away when you stomp the ground, revealing another mushroom.",
            ),
        ]
        search_index = 0

        print(
            "The Mushroom Kingdom stretches into Green Hill's loops. "
            "Collect M-Boost Mushrooms to wake the Warp Star."
        )
        while self.mushrooms < required and not self.quit_game:
            print(
                "\nActions:"
                "\n 1) Explore the hybrid meadow"
                "\n 2) Sprint with Sonic along the ring trail"
                "\n 3) Consult Luigi's crossover field guide"
                "\n (You can also type status, inventory, ability, help, or quit.)"
            )
            try:
                choice = input("What will you do? ").strip().lower()
            except EOFError:
                self.quit_game = True
                print("Input stream closed. Ending the adventure.")
                return False

            if not choice:
                continue

            if self._handle_common_command(choice):
                continue

            if choice in {"1", "explore", "search"}:
                location, narration = search_points[search_index % len(search_points)]
                search_index += 1
                print(narration)
                self.add_mushroom("M-Boost Mushroom", location)
            elif choice in {"2", "sprint", "dash", "run"}:
                print(
                    "Sonic matches your pace, leaving a trail of sparkling rings that blend with Mario's coins."
                    " The burst of speed inspires the team to search faster!"
                )
                self.log_event("Sonic's speed boosts morale in the meadow.")
            elif choice in {"3", "consult", "guide", "talk"}:
                print(
                    "Luigi hands you a notebook filled with doodles of pipes merging with loop-de-loops."
                    " He points out likely hiding spots for mushrooms."
                )
                self.log_event("Luigi's notes reveal secret hideaways.")
            else:
                print("That action doesn't help with collecting mushrooms right now.")

        if self.quit_game:
            return False

        print(
            "The gathered mushrooms pulse with combined Mushroom Kingdom and Chaos energy,"
            " lighting the Warp Star for inter-world travel!"
        )
        self.log_event("Warp Star empowered by M-Boost Mushrooms.")
        return True

    def _level_green_hill_crossover(self, segment: StorySegment) -> bool:
        """Second chapter: gather emerald fragments in Green Hill."""

        fragments: Dict[str, str] = {}
        fragment_messages = {
            "trail": (
                "Turbo Emerald Shard",
                "Sonic races ahead, tracing rings that align into a shining emerald fragment.",
            ),
            "totem": (
                "Harmony Emerald Shard",
                "Mario uncovers a hidden totem where a fragment hums with Mushroom Kingdom magic.",
            ),
        }

        print(
            "A Green Hill sunrise paints the sky. Metal Goomba Mk-II patrols nearby."
            " Recover Chaos Emerald fragments that fused with power mushrooms!"
        )

        while len(fragments) < len(fragment_messages) and not self.quit_game:
            print(
                "\nActions:"
                "\n 1) Dash along the ring trail"
                "\n 2) Investigate the ancient totem"
                "\n 3) Ask Tails for a tactical scan"
                "\n (Commands: status, inventory, ability, help, quit)"
            )
            try:
                choice = input("Your move? ").strip().lower()
            except EOFError:
                self.quit_game = True
                print("Input stream closed. Ending the adventure.")
                return False

            if not choice:
                continue

            if self._handle_common_command(choice):
                continue

            if choice in {"1", "dash", "run", "trail"}:
                if "trail" not in fragments:
                    name, narration = fragment_messages["trail"]
                    print(narration)
                    fragments["trail"] = name
                    self.inventory.append(name)
                    self.log_event(f"Recovered {name} from the ring trail.")
                else:
                    print("The ring trail already yielded its fragment, but the energy keeps spirits high.")
            elif choice in {"2", "totem", "investigate", "ancient"}:
                if "totem" not in fragments:
                    name, narration = fragment_messages["totem"]
                    print(narration)
                    fragments["totem"] = name
                    self.inventory.append(name)
                    self.log_event(f"Recovered {name} from the ancient totem.")
                else:
                    print("Only faint echoes remain at the totem. The fragment is secure in your pack.")
            elif choice in {"3", "scan", "tails", "ask"}:
                if len(fragments) == len(fragment_messages):
                    print(
                        "Tails grins and fuses the shards with your mushrooms, creating a Warp Emerald Engine."
                        " The Metal Goomba reels as the path to the next zone opens!"
                    )
                    self.log_event("Tails assembled the Warp Emerald Engine.")
                else:
                    print(
                        "Tails deploys a Miles Electric drone, highlighting nearby flickies in need of rescue."
                        " They cheer you on as you continue gathering fragments."
                    )
                    self.log_event("Tails provides reconnaissance data in Green Hill.")
            else:
                print("That tactic doesn't connect with the hybrid landscape right now.")

        if self.quit_game:
            return False

        print(
            "The forged Warp Emerald Engine hums aboard the Warp Star,"
            " ready to pierce the sky toward the aerial fortress!"
        )
        self.log_event("Warp Emerald Engine stabilized the crossover portal.")
        return True

    def _level_sky_race_express(self, segment: StorySegment) -> bool:
        """Third chapter: prepare the Sky Tornado transport."""

        engine_ready = False
        team_synced = False
        royal_gift_received = False

        print(
            "Sky Sanctuary ruins serve as a launchpad. The Sky Tornado must be tuned,"
            " and the team needs morale before tackling the twin villains."
        )

        while not (engine_ready and team_synced) and not self.quit_game:
            print(
                "\nActions:"
                "\n 1) Collaborate with Tails on engine tuning"
                "\n 2) Spar with Sonic along floating platforms"
                "\n 3) Call Princess Peach for strategic supplies"
                "\n (Commands: status, inventory, ability, help, quit)"
            )
            try:
                choice = input("How will you prepare? ").strip().lower()
            except EOFError:
                self.quit_game = True
                print("Input stream closed. Ending the adventure.")
                return False

            if not choice:
                continue

            if self._handle_common_command(choice):
                continue

            if choice in {"1", "collaborate", "tails", "engine"}:
                if not engine_ready:
                    print(
                        "Tails hands you a wrench while explaining Mobian aerodynamics."
                        " Together you calibrate the Warp Emerald Engine to the Sky Tornado."
                    )
                    engine_ready = True
                    self.log_event("Sky Tornado calibrated with Tails' help.")
                else:
                    print("The engine hums steadily. Tails gives a thumbs-up from the cockpit.")
            elif choice in {"2", "spar", "train", "sonic"}:
                if not team_synced:
                    print(
                        "You and Sonic dash across floating tiles, timing jumps with rhythmic precision."
                        " The synchronized moves ready the team for aerial combat."
                    )
                    team_synced = True
                    self.log_event("Team synchronization achieved with Sonic's training.")
                else:
                    print("Another round of practice keeps reflexes sharp while the Sky Tornado idles overhead.")
            elif choice in {"3", "call", "peach", "supplies"}:
                if not royal_gift_received:
                    print(
                        "Princess Peach deploys a Starlight Supply Drop: shimmering power-ups and a morale-boosting message."
                        " Among the gifts is a Royal Starlight Mushroom infused with protective magic."
                    )
                    royal_gift_received = True
                    self.add_mushroom("Royal Starlight Mushroom", "Peach's supply drop")
                    self.log_event("Received support package from Princess Peach.")
                else:
                    print("Peach radios in encouragement as the crew finalizes preparations.")
            else:
                print("The preparations stay focused on engines, training, and support.")

        if self.quit_game:
            return False

        print(
            "With engines primed and teamwork synchronized, the Sky Tornado rockets toward the dual fortress!"
        )
        self.log_event("Sky Tornado launched toward the fortress.")
        return True

    def _level_fortress_finale(self, segment: StorySegment) -> bool:
        """Final chapter: battle Bowser and Dr. Eggman."""

        boss_health = 3
        barrier_broken = False
        ability_charged = False

        print(
            "Bowser's airship chains clank against Dr. Eggman's metallic fortress."
            " The villains combine fire breath and mechs to shield the Chaos Boiler Core."
        )

        while boss_health > 0 and not self.quit_game:
            status = "barrier intact" if not barrier_broken else "barrier shattered"
            print(
                f"\nBoss health: {boss_health} | Fortress barrier: {status}"
                "\nActions:"
                "\n 1) Use your special ability"
                "\n 2) Coordinate a team-up strike"
                "\n 3) Deploy a power mushroom boost"
                "\n 4) Rally allies for support"
                "\n (Commands: status, inventory, help, quit)"
            )
            try:
                choice = input("Choose your tactic: ").strip().lower()
            except EOFError:
                self.quit_game = True
                print("Input stream closed. Ending the adventure.")
                return False

            if not choice:
                continue

            if self._handle_common_command(choice, allow_ability=False):
                continue

            if choice in {"1", "ability", "power"}:
                context = (
                    "An energy wave spirals from the Warp Emerald Engine, cascading over Bowser's mech armor."
                )
                if self.use_hero_ability(context=context):
                    if not barrier_broken:
                        ability_charged = True
                        print(
                            "The barrier flickers but holds. You sense a team strike will finish the job."
                        )
                        self.log_event("Hero ability charged the barrier during the final battle.")
                    else:
                        boss_health -= 1
                        print(
                            "The empowered strike pierces the exposed mech joints, sending sparks across the arena!"
                        )
                        self.log_event("Hero ability damages the fortress core.")
            elif choice in {"2", "team", "strike", "combo"}:
                if not barrier_broken:
                    if ability_charged:
                        barrier_broken = True
                        boss_health -= 1
                        print(
                            "With a combined leap, Sonic's spin dash and your heroics smash the barrier, exposing the core!"
                        )
                        self.log_event("Barrier shattered by a coordinated strike.")
                    else:
                        print(
                            "The barrier deflects the attack. You need to charge it with a special ability first!"
                        )
                else:
                    boss_health -= 1
                    print(
                        "Mario's allies unleash a combo: Luigi super-jumps, Tails fires an energy cannon, and Sonic spins."
                        " The villains stagger!"
                    )
                    self.log_event("Team combo damages Bowser and Eggman.")
            elif choice in {"3", "mushroom", "boost"}:
                if self.mushrooms > 0:
                    self.mushrooms -= 1
                    print(
                        "You share a power mushroom with the team, renewing stamina and amplifying the Warp Emerald glow."
                    )
                    self.log_event("Mushroom boost renews the team's strength.")
                else:
                    print("All mushrooms are spent! You'll need to rely on teamwork and abilities.")
            elif choice in {"4", "rally", "support", "allies"}:
                print(
                    "Princess Peach shields the arena with heart energy while Knuckles cracks Eggman's reinforcements."
                    " Your allies chant in unison, boosting morale!"
                )
                self.log_event("Allies rallied for the final assault.")
            else:
                print("Focus on the battle! Choose an action that impacts the fight.")

        if self.quit_game:
            return False

        print(
            "Bowser and Dr. Eggman tumble into the disabled Chaos Boiler as the fortress powers down."
            " The worlds begin to separate safely."
        )
        self.log_event("Villains defeated and worlds stabilized.")
        return True

    # ------------------------------------------------------------------
    # Post game and utilities
    # ------------------------------------------------------------------
    def _print_epilogue(self) -> None:
        """Narrate the adventure epilogue."""

        hero_name = self.hero.name if self.hero else "The heroes"
        print(
            "\nEpilogue:"  # newline ensures separation
            f"\n{hero_name} leads the celebration as Toads and Chao share a grand festival."
            " Peach and Tails unveil a memorial Warp Star linking the worlds for friendly races."
            " The Mushroom Kingdom and Mobius now share a legend of unity!\n"
        )
        self.log_event("Epilogue celebrated across both worlds.")

    def story_summary(self) -> List[Dict[str, str]]:
        """Return a concise description of the storyline for reference and testing."""

        return [
            {
                "name": segment.name,
                "location": segment.location,
                "objective": segment.objective,
                "boss": segment.boss,
            }
            for segment in self.storyline
        ]

    # ------------------------------------------------------------------
    # Factory
    # ------------------------------------------------------------------
    @classmethod
    def create_default_game(cls) -> "GameEngine":
        """Create a GameEngine instance with the crossover storyline preloaded."""

        characters: Iterable[Character] = [
            Character(
                name="Mario",
                title="Hero of the Mushroom Kingdom",
                franchise="Super Mario",
                description="A brave plumber ready to stomp, jump, and team up for justice.",
                ability_name="Heroic Jump",
                ability_description="A multi-bounce jump that cracks armor and activates switches.",
                ability_story="Mario rockets upward with classic determination, cape fluttering in the breeze.",
            ),
            Character(
                name="Luigi",
                title="Green Guardian of the Warp Star",
                franchise="Super Mario",
                description="An agile hero whose clever tactics keep everyone safe.",
                ability_name="Green Thunder",
                ability_description="A gravity-defying leap that generates protective lightning.",
                ability_story="Luigi twirls midair, releasing a thunderous burst that electrifies foes.",
            ),
            Character(
                name="Princess Peach",
                title="Royal Diplomat and Defender",
                franchise="Super Mario",
                description="Her heart magic shields allies and turns even villains into friends.",
                ability_name="Heartburst Parasol",
                ability_description="A floating strike that charms enemies and heals teammates.",
                ability_story="Peach soars gracefully, scattering heart-shaped light across the battlefield.",
            ),
            Character(
                name="Sonic",
                title="Fastest Thing Alive",
                franchise="Sonic the Hedgehog",
                description="A speedy hero who loves adventures and chili dogs alike.",
                ability_name="Supersonic Dash",
                ability_description="A spin dash so fast it warps reality for a heartbeat.",
                ability_story="Sonic becomes a streak of blue energy, rings chiming as he blazes forward.",
            ),
            Character(
                name="Tails",
                title="Genius Fox Pilot",
                franchise="Sonic the Hedgehog",
                description="Inventor extraordinaire who keeps everyone flying high.",
                ability_name="Cyclone Tailspin",
                ability_description="Twin tails create whirlwinds that reposition allies and gear.",
                ability_story="Tails spins into a miniature tornado, scattering gadget parts into useful tools.",
            ),
            Character(
                name="Knuckles",
                title="Guardian of the Master Emerald",
                franchise="Sonic the Hedgehog",
                description="A powerhouse ready to punch through any obstacle protecting his friends.",
                ability_name="Knuckle Quake",
                ability_description="Ground-shaking punches expose secrets and topple machines.",
                ability_story="Knuckles slams the ground, fissures racing outward with crimson energy.",
            ),
        ]

        storyline: Iterable[StorySegment] = [
            StorySegment(
                name="Mushroom Meadows",
                location="Mushroom Kingdom",
                objective="Collect M-Boost Mushrooms to power the Warp Star.",
                boss="Goomba Troop",
                introduction=(
                    "Mario's world bleeds into Green Hill Zone. Pipes sprout from checkerboard hills,"
                    " and Goombas ride loop-de-loops. Gather mushrooms to fuel interdimensional travel!"
                ),
                completion="The Warp Star glows brighter than ever, eager to blaze into the next world!",
            ),
            StorySegment(
                name="Green Hill Crossover",
                location="Green Hill Zone",
                objective="Gather Chaos Emerald fragments fused with mushrooms.",
                boss="Metal Goomba Mk-II",
                introduction=(
                    "Rolling hills echo with chimes of rings and coins. Metal Goomba Mk-II patrols the skies"
                    " while Tails detects emerald energy interwoven with mushroom spores."
                ),
                completion="With the Warp Emerald Engine built, the path toward the fortress unfurls in the clouds!",
            ),
            StorySegment(
                name="Sky Race Express",
                location="Sky Sanctuary",
                objective="Tune the Sky Tornado and raise team morale for the assault.",
                boss="Preparation Gauntlet",
                introduction=(
                    "An alliance of Toad engineers and Chaotix mechanics rig the Sky Tornado for a dimensional jump."
                    " Everyone must be ready before storming the combined fortress."
                ),
                completion="The Sky Tornado rockets ahead, contrails spelling out unity across the sky!",
            ),
            StorySegment(
                name="Fortress of Dual Kings",
                location="Egg Bowser Fortress",
                objective="Defeat Bowser and Dr. Eggman before the worlds collide for good.",
                boss="Bowser & Dr. Eggman",
                introduction=(
                    "A fused castle and giant Eggman mech loom above a swirling portal."
                    " Bowser hurls fire while Eggman pilots a Chaos-powered suit."
                ),
                completion="The villains fall, and the Chaos Boiler core deactivates with a triumphant chime!",
            ),
        ]

        engine = cls(characters=characters, storyline=storyline)
        engine.level_handlers = {
            "Mushroom Meadows": engine._level_mushroom_meadows,
            "Green Hill Crossover": engine._level_green_hill_crossover,
            "Sky Race Express": engine._level_sky_race_express,
            "Fortress of Dual Kings": engine._level_fortress_finale,
        }
        return engine
