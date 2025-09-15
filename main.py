"""Entry point for the Mario & Sonic crossover adventure."""

from mariosonic import GameEngine


def main() -> None:
    """Launch the interactive adventure."""

    engine = GameEngine.create_default_game()
    engine.play()


if __name__ == "__main__":
    main()
