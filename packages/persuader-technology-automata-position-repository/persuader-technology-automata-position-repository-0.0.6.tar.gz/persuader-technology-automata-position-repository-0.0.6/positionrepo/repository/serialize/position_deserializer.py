from core.number.BigFloat import BigFloat
from core.position.Position import Position
from utility.json_utility import as_data


def deserialize(position) -> Position:
    instrument = as_data(position, 'instrument')
    quantity = BigFloat(as_data(position, 'quantity'))
    instant = as_data(position, 'instant')
    deserialized_position = Position(instrument, quantity, instant)
    deserialize_exchanged_from(deserialized_position, as_data(position, 'exchanged_from'))
    return deserialized_position


def deserialize_exchanged_from(deserialized_position, value):
    if value is not None:
        deserialized_position.exchanged_from = value
