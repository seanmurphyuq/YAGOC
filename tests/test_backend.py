import pytest

from yagoc.backend import Game


def test_allPieces():
    game = Game()
    assert len(game.allPieces) > 8  # TODO: update as pieces are added


def test_state():
    game = Game()
    print("\n" + game.state)
    assert len(game.state) == 169  # 13x13 char grid


def test_pawn_movement():
    # positive
    game = Game()
    assert game.activePlayer == game.white  # initial

    game.makeMove("e4")
    assert game.activePlayer == game.black

    # TODO assert game.grid("e4") contains a white pawn
    # and assert game.grid("e2") doesn't

    game.makeMove("e5")
    assert game.activePlayer == game.white

    game.makeMove("b4")
    assert game.activePlayer == game.black

    game.makeMove("h6")
    assert game.activePlayer == game.white

    # negative (always white attempting to move since these moves are invalid)
    with pytest.raises(ValueError):
        # cannot capture an opponent's pawn vertically
        game.makeMove("e5")

    assert game.activePlayer == game.white

    with pytest.raises(ValueError):
        # cannot move 2 after first move
        game.makeMove("b6")

    assert game.activePlayer == game.white

    with pytest.raises(ValueError):
        # cannot move 3 initially
        game.makeMove("a5")

    assert game.activePlayer == game.white

    # TODO: if possible test to ensure horizontal movement is disallowed
    # difficult to actually test with a normal starting board layout
