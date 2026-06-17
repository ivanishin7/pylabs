from __future__ import annotations

import csv
import io
import json

import yaml

from interfaces import Decorator


class JsonDecorator(Decorator):
    """Декоратор для форматирования данных в JSON."""

    def operation(self) -> str:
        """Вернуть курсы валют в формате JSON-строки."""
        data = self._get_data()
        return json.dumps(data, indent=4, ensure_ascii=False)


class YamlDecorator(Decorator):
    """Декоратор для форматирования данных в YAML."""

    def operation(self) -> str:
        """Вернуть курсы валют в формате YAML-строки."""
        data = self._get_data()
        return yaml.dump(data, allow_unicode=True, default_flow_style=False)


class CsvDecorator(Decorator):
    """Декоратор для форматирования данных в CSV."""

    def operation(self) -> str:
        """Вернуть курсы валют в формате CSV-строки."""
        data = self._get_data()
        date = data.get("date", "")
        rates = data.get("rates", {})

        output = io.StringIO()
        writer = csv.writer(output, lineterminator="\n")

        # Заголовок таблицы CSV
        writer.writerow(
            ["Date", "CharCode", "NumCode", "Nominal", "Name", "Value"]
        )

        for char_code, info in rates.items():
            writer.writerow(
                [
                    date,
                    char_code,
                    info.get("num_code", ""),
                    info.get("nominal", ""),
                    info.get("name", ""),
                    info.get("value", ""),
                ]
            )

        return output.getvalue()
