from typing import List, Union, overload

from pydantic import BaseModel

from model_parser.custom_types import JsonObject
from model_parser.mapper import BaseMapper


class Parser:
    """
    The Parser takes in a Pydantic `BaseModel` and a `model_parser.BaseMapper` to
    perform transformations and parse the object into the defined entity.

    Attributes:

        _model BaseModel: The Pydantic Model

        _mapper BaseMapper: The Mapper Class defined using model_parser.mapper.BaseMapper
    """

    def __init__(self, entity_model: BaseModel, mapper: BaseMapper) -> None:
        self._model = entity_model
        self._mapper = mapper

    @overload
    def parse(self, data: JsonObject) -> BaseModel:
        """
        The parse function takes in either [dict | list[dict]], performs the
        transformations as defined in the _mapper attribute and parses into
        the _model as a Pydantic entity

        Args:
            data (Union[JsonObject, List[JsonObject]]): The raw data to transform and parse

        Returns:
            Union[BaseModel, List[BaseModel]]: The `Pydantic` entities as defined by  the _model attr

        Raise:
            ValidationError: Raised if there is a Validation Error that is detected by `Pydantic`. e.g. Invalid type-casting.
        """
        ...

    @overload
    def parse(self, data: List[JsonObject]) -> List[BaseModel]:
        ...

    def parse(
        self, data: Union[JsonObject, List[JsonObject]]
    ) -> Union[BaseModel, List[BaseModel]]:
        if isinstance(data, dict):
            parsed = self._mapper.transform(data)
            return self._model.parse_obj(parsed)

        parsed = [self._mapper.transform(item) for item in data]
        return [self._model.parse_obj(item) for item in parsed]
