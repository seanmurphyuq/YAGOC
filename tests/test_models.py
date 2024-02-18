import math

import pytest
from pydantic import ValidationError

from yagoc.models import Colour, GridPosition

def nextInt(value: int) -> int:
    return math.ceil(math.nextafter(value, math.inf))

def prevInt(value: int) -> int:
    return math.floor(math.nextafter(value, -math.inf))

def test_Colour():
    #positive tests
    #arrange/act
    white = Colour(red=255, green=255, blue=255)
    black = Colour(red=0,green=0,blue=0)

    # assert
    assert white.rgb_hex == "ffffff"
    assert black.rgb_hex == "000000"

    #negative tests
    #arrange
    upper_valid = 255
    lower_valid = 0
    upper_invalid = nextInt(upper_valid)
    lower_invalid = prevInt(lower_valid)

    # assert
    for valid_value, invalid_value in ((lower_valid, lower_invalid), (upper_valid, upper_invalid)):
        with pytest.raises(ValidationError):
            _ = Colour(red=invalid_value, green=valid_value, blue=valid_value)
        
        with pytest.raises(ValidationError):
            _ = Colour(red=valid_value, green=invalid_value, blue=valid_value)

        with pytest.raises(ValidationError):
            _ = Colour(red=valid_value, green=valid_value, blue=invalid_value)
            
def test_GridPosition():
    #positive tests
    for vertical in range(1,9):
        for horizontal in ("a","b","c","d","e","f","g","h"):
            pos = GridPosition(horizontal=horizontal, vertical=vertical)
            assert len(pos.str_pos) == 2

    #negative tests
    validVertical = 1
    for horizontal in ("i,j,k"):
        with pytest.raises(ValidationError):
            _ = GridPosition(horizontal=horizontal, vertical=validVertical)
    
    validHorizontal = "a"
    for vertical in (0,9,10):
        with pytest.raises(ValidationError):
            _ = GridPosition(horizontal=validHorizontal, vertical=vertical)