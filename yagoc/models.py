from typing import Union, ForwardRef

from pydantic import BaseModel, Field

Game = ForwardRef("yagoc.backend.Game")
# from yagoc.backend import Game


def int_to_hex(value: int) -> str:
    # double digit hex repr of an int
    return f"{value:02x}"


class Colour(BaseModel):
    red: int = Field(ge=0, le=255)
    green: int = Field(ge=0, le=255)
    blue: int = Field(ge=0, le=255)

    @property
    def rgb_hex(self) -> str:
        return int_to_hex(self.red) + int_to_hex(self.green) + int_to_hex(self.blue)


class GridPosition(BaseModel):
    horizontal: str = Field(pattern=r"^[a-h]{1}$", allow_mutation=False)  # a to h
    vertical: int = Field(ge=1, le=8, allow_mutation=False)

    @property
    def str_pos(self) -> str:
        return f"{self.horizontal}{self.vertical}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.str_pos}"


class Piece:
    def __init__(self, spawnPosition: GridPosition, value: int) -> None:
        self.position = spawnPosition
        self.value = value
        self.hasMoved: bool = False  # since pawns can initially move two squares, rook+kings can castle if not moved
        # TODO: should capturing be stored here or in Player? Probably Player

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} at {self.position}"


class Pawn(Piece):
    def __init__(self, spawnPosition: GridPosition) -> None:
        super().__init__(spawnPosition, value=1)


class Player:
    UP = True
    DOWN = False

    def __init__(
        self, colour: Colour, direction: bool, pieces: list[Piece], game: Game
    ) -> None:
        self.colour = colour
        self.direction = direction
        self.pieces = pieces
        self.game = game

        self.score = 0
        self.opponent_pieces_taken: list[Piece] = []
        self.own_pieces_lost: list[Piece] = []

    def attemptMove(self, desiredMove: Union[str, GridPosition]) -> None:
        """Attempt the move specified by algebraic notation.
        Will return if valid/successful; will raise an exception if the move is invalid.

        Examples:
            e4 attempts to move a pawn from its spawn position of e2 to e4
            Qf7 attempts to move a queen from wherever it is to f7

        """
        # normalise to grid position
        if isinstance(desiredMove, str):
            desiredMove = GridPosition(
                horizontal=desiredMove[0], vertical=int(desiredMove[1])
            )

        horizontalMove = desiredMove.horizontal
        verticalMove = int(desiredMove.vertical)

        # pawn move
        # iterate through pieces, attempting to find one that is within range of the desired move
        for piece in self.pieces:
            if piece.__class__.__name__ == "Pawn":
                # movement first
                if horizontalMove != piece.position.horizontal:
                    # TODO: ensure horizontal-only move is disallowed
                    # TODO: handle capturing
                    # TODO: handle en passant
                    continue

                if self.direction == self.UP:
                    if piece.hasMoved:
                        # e.g. starting at 4: needs to be 5
                        if verticalMove == piece.position.vertical + 1:
                            # ostensibly valid vertical move - but ensure vertical capturing is disallowed
                            if desiredMove in [
                                piece.position for piece in self.game.allPieces
                            ]:
                                raise ValueError(
                                    "Invalid move (pawn cannot capture vertically)"
                                )

                            # empty valid vertical square to move to - proceed
                            piece.position = desiredMove

                        else:
                            continue
                    else:  # e.g. starting at 2: needs to be > 2 and <= 4
                        if (
                            verticalMove > piece.position.vertical
                            and verticalMove <= piece.position.vertical + 2
                        ):
                            # ostensibly valid vertical move - but ensure vertical capturing is disallowed
                            if desiredMove in [piece.position for piece in self.pieces]:
                                raise ValueError(
                                    "Invalid move (pawn cannot capture vertically)"
                                )

                            # empty valid vertical square to move to - proceed
                            piece.position = desiredMove
                            piece.hasMoved = True
                        else:
                            continue

                elif self.direction == self.DOWN:
                    if piece.hasMoved:
                        # e.g. starting at 5: needs to be 4
                        if verticalMove == piece.position.vertical - 1:
                            piece.position = desiredMove
                        else:
                            raise ValueError("Invalid move")
                    else:  # e.g. starting at 7: needs to be < 7 and >= 5
                        if (
                            verticalMove < piece.position.vertical
                            and verticalMove >= piece.position.vertical - 2
                        ):
                            piece.position = desiredMove
                            piece.hasMoved = True
                        else:
                            raise ValueError("Invalid move")

                return  # success
            else:
                raise NotImplementedError("Other pieces not implemented yet")
        else:
            raise ValueError("Invalid or unhandled move")
