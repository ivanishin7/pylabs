from __future__ import annotations

from cbr_component import ConcreteComponent
from decorators import CsvDecorator, JsonDecorator, YamlDecorator


def main() -> None:
    """Запустить демонстрацию работы компонентов и декораторов."""
    print("Получение данных с Центробанка...")
    try:
        base_rates = ConcreteComponent()
        print("\n--- 1. Базовый компонент (возвращает dict) ---")
        res_dict = base_rates.operation()
        print(f"Тип: {type(res_dict)}")
        print(f"Дата: {res_dict.get('date')}")
        print(f"Количество валют: {len(res_dict.get('rates', {}))}")

        import os

        current_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(current_dir, "output")
        os.makedirs(output_dir, exist_ok=True)

        print("\n--- 2. Декоратор JSON ---")
        json_decorator = JsonDecorator(base_rates)
        json_str = json_decorator.operation()
        print(json_str[:300] + "\n...")
        json_path = os.path.join(output_dir, "rates.json")
        json_decorator.save_to_file(json_path)
        print(f"Сохранено в {os.path.relpath(json_path, current_dir)}")

        print("\n--- 3. Декоратор YAML ---")
        yaml_decorator = YamlDecorator(base_rates)
        yaml_str = yaml_decorator.operation()
        print(yaml_str[:300] + "\n...")
        yaml_path = os.path.join(output_dir, "rates.yaml")
        yaml_decorator.save_to_file(yaml_path)
        print(f"Сохранено в {os.path.relpath(yaml_path, current_dir)}")

        print("\n--- 4. Декоратор CSV ---")
        csv_decorator = CsvDecorator(base_rates)
        csv_str = csv_decorator.operation()
        print(csv_str[:300] + "\n...")
        csv_path = os.path.join(output_dir, "rates.csv")
        csv_decorator.save_to_file(csv_path)
        print(f"Сохранено в {os.path.relpath(csv_path, current_dir)}")

    except Exception as e:
        print(f"Произошла ошибка при выполнении демонстрации: {e}")


if __name__ == "__main__":
    main()
