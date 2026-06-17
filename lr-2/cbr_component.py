from __future__ import annotations

import urllib.request
import xml.etree.ElementTree as ET
from typing import Any

from interfaces import Component


class ConcreteComponent(Component):
    """Компонент для получения курсов валют Центробанка РФ."""

    def __init__(
        self, url: str = "https://www.cbr.ru/scripts/XML_daily.asp"
    ) -> None:
        """Инициализировать компонент адресом API Центробанка."""
        self._url: str = url

    def operation(self) -> dict[str, Any]:
        """Загрузить XML-данные от Центробанка и распарсить в словарь."""
        req = urllib.request.Request(
            self._url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read()

        xml_text = xml_data.decode("windows-1251")
        root = ET.fromstring(xml_text)
        date = root.attrib.get("Date", "")

        rates: dict[str, dict[str, Any]] = {}
        for valute in root.findall("Valute"):
            char_code = valute.find("CharCode")
            num_code = valute.find("NumCode")
            nominal = valute.find("Nominal")
            name = valute.find("Name")
            value = valute.find("Value")

            if (
                char_code is not None
                and num_code is not None
                and nominal is not None
                and name is not None
                and value is not None
            ):
                val_str = value.text.replace(",", ".") if value.text else "0"
                rates[char_code.text] = {
                    "num_code": num_code.text,
                    "nominal": int(nominal.text) if nominal.text else 1,
                    "name": name.text,
                    "value": float(val_str),
                }

        return {"date": date, "rates": rates}
