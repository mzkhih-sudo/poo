# Mario & Sonic: Warpstar Rush

Welcome to **Mario & Sonic: Warpstar Rush**, a text-based crossover adventure that lets you
lead iconic heroes from the Mushroom Kingdom and Mobius on a quest to stop Bowser and
Dr. Eggman from fusing their worlds together. Choose your hero, collect mushrooms,
assemble Chaos Emerald tech, and guide the team through a complete four-chapter storyline.

## Features

- **Playable roster:** Mario, Luigi, Princess Peach, Sonic, Tails, and Knuckles—each with
a unique ability narration and role in the story.
- **Complete narrative arc:** Travel from Mushroom Meadows to the combined Egg Bowser
  Fortress, collecting items, prepping your crew, and facing a climactic boss battle.
- **Interactive choices:** Explore, train, rally allies, or trigger special abilities to move the
  story forward. Common commands like `status`, `inventory`, `ability`, and `quit` are always
  available.
- **Collectible mushrooms:** Gather M-Boost and Starlight mushrooms that fuel the Warp Star
  and empower your final assault.
- **Replay-friendly:** Different heroes bring their own flavor text, letting you experience the
  crossover from multiple perspectives.

## Getting Started

1. Ensure you have Python 3.9+ installed.
2. Install dependencies (none beyond the standard library are required).
3. Launch the adventure:

   ```bash
   python main.py
   ```

Follow the on-screen prompts to make choices. At any time you can view your status,
check inventory, use your hero's ability, or quit the session.

## Gameplay Overview

The storyline unfolds across four major chapters:

1. **Mushroom Meadows** – Collect M-Boost Mushrooms to power the Warp Star while Mario and
   Sonic's worlds blend together in strange ways.
2. **Green Hill Crossover** – Recover Chaos Emerald fragments that have fused with mushrooms
   and let Tails build the Warp Emerald Engine.
3. **Sky Race Express** – Tune the Sky Tornado with Tails, spar with Sonic, and call on Princess
   Peach for supplies before the final assault.
4. **Fortress of Dual Kings** – Break through Bowser and Dr. Eggman's combined defenses,
   using mushrooms and teamwork to shut down the Chaos Boiler core.

Every chapter offers custom interactions plus the universal commands.

## Tests

Lightweight tests verify that the roster and storyline are properly configured. Run them with:

```bash
pytest
```

## Project Structure

```
├── main.py                 # Entry point for the interactive adventure
├── mariosonic
│   ├── __init__.py         # Package export definitions
│   └── game.py             # Game engine, characters, and storyline logic
├── tests
│   └── test_storyline.py   # Unit tests for data and narration helpers
└── README.md               # Project documentation (this file)
```

Enjoy saving two worlds in one legendary team-up!
