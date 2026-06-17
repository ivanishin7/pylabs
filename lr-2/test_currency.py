from __future__ import annotations

import json
import os
import tempfile
import unittest
import urllib.error
from unittest.mock import MagicMock, patch

import yaml

from cbr_component import ConcreteComponent
from decorators import CsvDecorator, JsonDecorator, YamlDecorator

# Пример корректного XML-ответа Центробанка
XML_SAMPLE = """<?xml version="1.0" encoding="windows-1251"?>
<ValCurs Date="17.06.2026" name="Foreign Currency Market">
    <Valute ID="R01235">
        <NumCode>840</NumCode>
        <CharCode>USD</CharCode>
        <Nominal>1</Nominal>
        <Name>Доллар США</Name>
        <Value>85,1234</Value>
    </Valute>
    <Valute ID="R01239">
        <NumCode>978</NumCode>
        <CharCode>EUR</CharCode>
        <Nominal>1</Nominal>
        <Name>Евро</Name>
        <Value>92,5678</Value>
    </Valute>
</ValCurs>
"""


class TestConcreteComponent(unittest.TestCase):
    """Тесты для базового компонента получения курсов валют."""

    @patch("urllib.request.urlopen")
    def test_successful_fetch(self, mock_urlopen: MagicMock) -> None:
        """Проверка успешного получения и парсинга XML в словарь."""
        # Настройка мока для urlopen
        mock_response = MagicMock()
        mock_response.read.return_value = XML_SAMPLE.encode("windows-1251")
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        component = ConcreteComponent()
        result = component.operation()

        # Проверка структуры и значений результата
        self.assertEqual(result["date"], "17.06.2026")
        self.assertIn("USD", result["rates"])
        self.assertIn("EUR", result["rates"])

        usd = result["rates"]["USD"]
        self.assertEqual(usd["num_code"], "840")
        self.assertEqual(usd["nominal"], 1)
        self.assertEqual(usd["name"], "Доллар США")
        self.assertEqual(usd["value"], 85.1234)

        eur = result["rates"]["EUR"]
        self.assertEqual(eur["num_code"], "978")
        self.assertEqual(eur["nominal"], 1)
        self.assertEqual(eur["name"], "Евро")
        self.assertEqual(eur["value"], 92.5678)

    @patch("urllib.request.urlopen")
    def test_network_error(self, mock_urlopen: MagicMock) -> None:
        """Проверка обработки сетевой ошибки при запросе."""
        mock_urlopen.side_effect = urllib.error.URLError("Connection refused")

        component = ConcreteComponent()
        with self.assertRaises(urllib.error.URLError):
            component.operation()


class TestJsonDecorator(unittest.TestCase):
    """Тесты для JSON-декоратора."""

    def setUp(self) -> None:
        """Создать тестовый компонент с фиксированными данными."""
        self.base_data = {
            "date": "17.06.2026",
            "rates": {
                "USD": {
                    "num_code": "840",
                    "nominal": 1,
                    "name": "Доллар США",
                    "value": 85.1234,
                }
            },
        }
        self.mock_component = MagicMock()
        self.mock_component.operation.return_value = self.base_data

    def test_json_formatting(self) -> None:
        """Проверка корректности форматирования в JSON."""
        decorator = JsonDecorator(self.mock_component)
        result_str = decorator.operation()

        # Проверяем, что результат является валидным JSON-ом
        parsed = json.loads(result_str)
        self.assertEqual(parsed, self.base_data)

    def test_json_save_to_file(self) -> None:
        """Проверка сохранения JSON-строки в файл."""
        decorator = JsonDecorator(self.mock_component)

        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test.json")
            decorator.save_to_file(filepath)

            # Проверяем запись на диск
            self.assertTrue(os.path.exists(filepath))
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            parsed = json.loads(content)
            self.assertEqual(parsed, self.base_data)


class TestYamlDecorator(unittest.TestCase):
    """Тесты для YAML-декоратора."""

    def setUp(self) -> None:
        """Создать тестовый компонент с фиксированными данными."""
        self.base_data = {
            "date": "17.06.2026",
            "rates": {
                "USD": {
                    "num_code": "840",
                    "nominal": 1,
                    "name": "Доллар США",
                    "value": 85.1234,
                }
            },
        }
        self.mock_component = MagicMock()
        self.mock_component.operation.return_value = self.base_data

    def test_yaml_formatting(self) -> None:
        """Проверка корректности форматирования в YAML."""
        decorator = YamlDecorator(self.mock_component)
        result_str = decorator.operation()

        # Проверяем, что результат является валидным YAML-ом
        parsed = yaml.safe_load(result_str)
        self.assertEqual(parsed, self.base_data)

    def test_yaml_save_to_file(self) -> None:
        """Проверка сохранения YAML-строки в файл."""
        decorator = YamlDecorator(self.mock_component)

        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test.yaml")
            decorator.save_to_file(filepath)

            # Проверяем запись на диск
            self.assertTrue(os.path.exists(filepath))
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            parsed = yaml.safe_load(content)
            self.assertEqual(parsed, self.base_data)


class TestCsvDecorator(unittest.TestCase):
    """Тесты для CSV-декоратора."""

    def setUp(self) -> None:
        """Создать тестовый компонент с фиксированными данными."""
        self.base_data = {
            "date": "17.06.2026",
            "rates": {
                "USD": {
                    "num_code": "840",
                    "nominal": 1,
                    "name": "Доллар США",
                    "value": 85.1234,
                },
                "EUR": {
                    "num_code": "978",
                    "nominal": 1,
                    "name": "Евро",
                    "value": 92.5678,
                },
            },
        }
        self.mock_component = MagicMock()
        self.mock_component.operation.return_value = self.base_data

    def test_csv_formatting(self) -> None:
        """Проверка корректности форматирования в CSV (заголовок и строки)."""
        decorator = CsvDecorator(self.mock_component)
        result_str = decorator.operation()

        lines = result_str.strip().split("\n")
        self.assertEqual(len(lines), 3)  # Заголовок + 2 строки валют

        # Проверка заголовка
        self.assertEqual(
            lines[0], "Date,CharCode,NumCode,Nominal,Name,Value"
        )

        # Проверка строк
        self.assertEqual(lines[1], "17.06.2026,USD,840,1,Доллар США,85.1234")
        self.assertEqual(lines[2], "17.06.2026,EUR,978,1,Евро,92.5678")

    def test_csv_save_to_file(self) -> None:
        """Проверка сохранения CSV-строки в файл."""
        decorator = CsvDecorator(self.mock_component)

        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test.csv")
            decorator.save_to_file(filepath)

            # Проверяем запись на диск
            self.assertTrue(os.path.exists(filepath))
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            lines = content.strip().split("\n")
            self.assertEqual(len(lines), 3)
            self.assertEqual(
                lines[0], "Date,CharCode,NumCode,Nominal,Name,Value"
            )
            self.assertEqual(lines[1], "17.06.2026,USD,840,1,Доллар США,85.1234")


class TestNestedDecorators(unittest.TestCase):
    """Тесты для вложенных декораторов (один поверх другого)."""

    def test_nesting_yaml_after_json(self) -> None:
        """Декоратор YAML может оборачивать декоратор JSON."""
        base_data = {
            "date": "17.06.2026",
            "rates": {
                "USD": {
                    "num_code": "840",
                    "nominal": 1,
                    "name": "Доллар США",
                    "value": 85.1234,
                }
            },
        }
        mock_component = MagicMock()
        mock_component.operation.return_value = base_data

        json_dec = JsonDecorator(mock_component)
        yaml_dec = YamlDecorator(json_dec)

        # Проверяем, что YAML декоратор успешно распаривает JSON-строку
        # от вложенного декоратора и выдает валидный YAML
        yaml_str = yaml_dec.operation()
        parsed = yaml.safe_load(yaml_str)
        self.assertEqual(parsed, base_data)


if __name__ == "__main__":
    unittest.main()
