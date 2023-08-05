from __future__ import annotations

from typing import Dict

from alicefluentcheck.chain import chained
from alicefluentcheck.constants import *


class AliceEntity:
    """
    Описание одной сущности: имя сущности, состав и положение

    Документация: https://yandex.ru/dev/dialogs/alice/doc/nlu.html
    """

    def __init__(self, entity_type=""):
        self.type = entity_type
        self.entity_tokens = {"start": 0, "end": 0}
        self.entity_value = ""

    @chained
    def tokens(self, start=0, end=0) -> AliceEntity:
        assert 0 <= start <= end, "Нарушен порядок позиций сущности"
        self.entity_tokens["start"] = start
        self.entity_tokens["end"] = end

    @chained
    def value(self, value) -> AliceEntity:
        self.entity_value = value

    @chained
    def fio(self, last_name="", first_name="", patronymic_name="") -> AliceEntity:
        assert (
            first_name or patronymic_name or last_name
        ), "Должна быть указана часть ФИО"

        self.type = YA_FIO
        value = {}
        if first_name:
            value["first_name"] = first_name
        if patronymic_name:
            value["patronymic_name"] = patronymic_name
        if last_name:
            value["last_name"] = last_name

        self.entity_value = value

    @chained
    def number(self, num: int) -> AliceEntity:
        self.type = YA_NUMBER
        self.entity_value = num

    @chained
    def datetime(
        self,
        year=None,
        year_is_relative=None,
        month=None,
        month_is_relative=None,
        day=None,
        day_is_relative=None,
        hour=None,
        hour_is_relative=None,
        minute=None,
        minute_is_relative=None,
    ) -> AliceEntity:
        self.type = YA_DATETIME
        value = {
            "year": year,
            "year_is_relative": year_is_relative,
            "month": month,
            "month_is_relative": month_is_relative,
            "day": day,
            "day_is_relative": day_is_relative,
            "hour": hour,
            "hour_is_relative": hour_is_relative,
            "minute": minute,
            "minute_is_relative": minute_is_relative,
        }
        value = {k: v for k, v in value.items() if v is not None}
        self.entity_value = value

    @chained
    def tomorrow(self):
        self.datetime(day=1, day_is_relative=True)

    @chained
    def yesterday(self):
        self.datetime(day=-1, day_is_relative=True)

    @property
    def val(self) -> Dict:
        """
        Собрать значение сущности
        :return: значение одной сущности: тип, позиции и значение
        """
        return {
            "type": self.type,
            "value": self.entity_value,
            "tokens": self.entity_tokens,
        }
