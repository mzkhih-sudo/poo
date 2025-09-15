"""Tests for the Mario & Sonic crossover adventure."""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from mariosonic import GameEngine


def test_characters_include_mario_and_sonic() -> None:
    """Ensure that both franchises are represented among the playable heroes."""

    engine = GameEngine.create_default_game()
    names = {character.name for character in engine.characters}
    assert {"Mario", "Sonic"}.issubset(names)
    assert len(names) >= 6


def test_storyline_has_four_segments() -> None:
    """The story should span four major chapters with clear objectives."""

    engine = GameEngine.create_default_game()
    summary = engine.story_summary()
    assert len(summary) == 4
    assert summary[0]["name"] == "Mushroom Meadows"
    assert summary[-1]["boss"] == "Bowser & Dr. Eggman"
    for stage in summary:
        assert stage["objective"]
        assert stage["location"]


def test_ability_text_mentions_hero_and_power() -> None:
    """Ability narration should mention both the hero and their signature move."""

    engine = GameEngine.create_default_game()
    mario = next(character for character in engine.characters if character.name == "Mario")
    text = mario.ability_text("to rally the team against Bowser.")
    assert "Mario" in text
    assert mario.ability_name in text
