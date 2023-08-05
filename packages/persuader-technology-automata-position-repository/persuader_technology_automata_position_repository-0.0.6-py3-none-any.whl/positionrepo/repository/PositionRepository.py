from cache.holder.RedisCacheHolder import RedisCacheHolder
from core.options.exception.MissingOptionError import MissingOptionError
from core.position.Position import Position

from positionrepo.repository.serialize.position_deserializer import deserialize
from positionrepo.repository.serialize.position_serializer import serialize

POSITION_KEY = 'POSITION_KEY'


class PositionRepository:

    def __init__(self, options):
        self.options = options
        self.__check_options()
        self.cache = RedisCacheHolder()

    def __check_options(self):
        if self.options is None:
            raise MissingOptionError(f'missing option please provide options {POSITION_KEY}')
        if POSITION_KEY not in self.options:
            raise MissingOptionError(f'missing option please provide option {POSITION_KEY}')

    def store(self, position: Position):
        position_key = self.options[POSITION_KEY]
        position_serialized = serialize(position)
        self.cache.store(position_key, position_serialized)

    def retrieve(self) -> Position:
        position_key = self.options[POSITION_KEY]
        raw_position = self.cache.fetch(position_key, as_type=dict)
        return deserialize(raw_position)
