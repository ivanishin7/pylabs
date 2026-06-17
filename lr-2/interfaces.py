from __future__ import annotations

import abc
import json
from typing import Any, Union

import yaml


class Component(abc.ABC):
    """Абстрактный базовый класс для компонентов и декораторов."""

    @abc.abstractmethod
    def operation(self) -> Union[dict[str, Any], str]:
        """Вернуть данные о курсах валют."""
        pass


class Decorator(Component):
    """Базовый класс декоратора, хранящий ссылку на вложенный компонент."""

    def __init__(self, component: Component) -> None:
        """Инициализировать декоратор вложенным компонентом."""
        self._component: Component = component

    @property
    def component(self) -> Component:
        """Получить обёрнутый компонент."""
        return self._component

    def operation(self) -> Union[dict[str, Any], str]:
        """Делегировать выполнение операции вложенному компоненту."""
        return self._component.operation()

    def _get_data(self) -> dict[str, Any]:
        """Получить исходные данные в виде словаря, парся строки при необходимости."""
        data = self._component.operation()
        if isinstance(data, dict):
            return data

        if isinstance(data, str):
            try:
                parsed_json = json.loads(data)
                if isinstance(parsed_json, dict):
                    return parsed_json
            except json.JSONDecodeError:
                pass

            try:
                parsed_yaml = yaml.safe_load(data)
                if isinstance(parsed_yaml, dict):
                    return parsed_yaml
            except Exception:
                pass

        raise ValueError("Неподдерживаемый формат данных.")

    def save_to_file(self, filepath: str) -> None:
        """Сохранить результат форматирования в файл."""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(str(self.operation()))
