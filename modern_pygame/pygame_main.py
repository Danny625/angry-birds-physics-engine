try:
    from angrybirds.pygame_client import run
except ModuleNotFoundError as error:
    if error.name == "pygame":
        raise SystemExit(
            "Pygame is not installed yet. Run `python -m pip install -r requirements.txt` "
            "and then start the game with `python pygame_main.py`."
        ) from error
    raise


if __name__ == "__main__":
    run()
