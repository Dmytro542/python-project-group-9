import pickle
from pathlib import Path

from notebook.notebook import Notebook


def save_data(notebook: Notebook, filename: str | Path = "notebook.pkl") -> None:
    with open(filename, "wb") as f:
        pickle.dump(notebook, f)


def load_data(filename: str | Path = "notebook.pkl") -> Notebook:
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return Notebook()
