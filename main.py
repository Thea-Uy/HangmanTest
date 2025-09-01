from argparse import ArgumentParser

from model import HangmanModel
from view import HangmanView
from controller import HangmanController


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("answer")
    parser.add_argument("lives", type=int)
    args = parser.parse_args()

    model = HangmanModel(args.answer, args.lives)
    view = HangmanView()
    controller = HangmanController(model, view)

    controller.start()