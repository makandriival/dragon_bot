import pickle
from pathlib import Path


def write_to_file(data, data_type: str):
    with open(path(data_type), "wb") as file:
        pickle.dump(data, file)


def read_from_file(data_type: str) -> list:
    try:
        with open(path(data_type), "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return []


def path(data_type: str) -> Path:
    directory = Path.home() / "dragon_bot_data"
    directory.mkdir(exist_ok=True)
    return directory / f"{data_type}.pkl"
