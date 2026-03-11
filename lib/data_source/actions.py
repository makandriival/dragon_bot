import pickle


def write_to_file(data, data_type: str):
    with open(f"{data_type}.pkl", "wb") as file:
        pickle.dump(data, file)


def read_from_file(data_type: str) -> list:
    try:
        with open(f"{data_type}.pkl", "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return []
