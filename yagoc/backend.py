"""Yet another game of chess backend
"""
from typing import Union

from yagoc.models import Colour, Player, Piece, Pawn, GridPosition

# TODO move to constants.py
# RGB colour defs
WHITE = Colour(red=255, green=255, blue=255)
BLACK = Colour(red=0, green=0, blue=0)
HORIZONTAL_CHARS = "abcdefgh"


class Game:
    def __init__(self) -> None:
        # colour is arbitrary/mutable, but referred to as white and black regardless by convention

        # construct white starting pieces
        whitePieces = [
            Pawn(spawnPosition=GridPosition(horizontal="a", vertical=2)),
            Pawn(spawnPosition=GridPosition(horizontal="b", vertical=2)),
            Pawn(spawnPosition=GridPosition(horizontal="c", vertical=2)),
            Pawn(spawnPosition=GridPosition(horizontal="d", vertical=2)),
            Pawn(spawnPosition=GridPosition(horizontal="e", vertical=2)),
            Pawn(spawnPosition=GridPosition(horizontal="f", vertical=2)),
            Pawn(spawnPosition=GridPosition(horizontal="g", vertical=2)),
            Pawn(spawnPosition=GridPosition(horizontal="h", vertical=2)),
            # TODO: other pieces
        ]

        self.white = Player(
            colour=WHITE, direction=Player.UP, pieces=whitePieces, game=self
        )

        # construct black starting pieces
        blackPieces = [
            Pawn(spawnPosition=GridPosition(horizontal="a", vertical=7)),
            Pawn(spawnPosition=GridPosition(horizontal="b", vertical=7)),
            Pawn(spawnPosition=GridPosition(horizontal="c", vertical=7)),
            Pawn(spawnPosition=GridPosition(horizontal="d", vertical=7)),
            Pawn(spawnPosition=GridPosition(horizontal="e", vertical=7)),
            Pawn(spawnPosition=GridPosition(horizontal="f", vertical=7)),
            Pawn(spawnPosition=GridPosition(horizontal="g", vertical=7)),
            Pawn(spawnPosition=GridPosition(horizontal="h", vertical=7)),
            # TODO: other pieces
        ]
        self.black = Player(
            colour=BLACK, direction=Player.DOWN, pieces=blackPieces, game=self
        )

        # initial state: white starts
        self.activePlayer = self.white

    @property
    def allPieces(self) -> list[Piece]:
        return self.white.pieces + self.black.pieces

    @property
    def state(self) -> str:
        """ASCII art style repr of game state"""
        cell = "|"
        grid = ""
        for rowIndex in range(8, 0, -1):
            row = ""
            entity = " "
            for colIndex in range(8):
                thisPosition = GridPosition(
                    horizontal=HORIZONTAL_CHARS[colIndex], vertical=rowIndex
                )
                if thisPosition in [piece.position for piece in self.allPieces]:
                    entity = "p"  # TODO extend to other pieces
                row += f"{cell}{entity}"
            row += "|"  # right hand closing

            grid += f"{rowIndex}{row}\n"

        footer = "  a b c d e f g h"
        return grid + footer

    def makeMove(self, desiredMove: Union[str, GridPosition]):
        try:
            self.activePlayer.attemptMove(desiredMove)
        except ValueError as e:
            print(e)
            raise
        else:
            self.activePlayer = (
                self.black if self.activePlayer == self.white else self.white
            )
