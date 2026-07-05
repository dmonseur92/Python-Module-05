from typing import Any
from abc import ABC, abstractmethod

class DataProcessor(ABC):
    def __init__(self):
        self.storage = []
    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        pass


class NumericProcessor(DataProcessor):
    def __init__(self):
        super().__init__()
        self.piece = 0

    def validate(self, data: Any) -> bool:
        return isinstance(data, (int, float)) or (
            isinstance(data, list) and all(isinstance(x,(int, float)) for x in data))

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")
        if isinstance(data, list):
            for x in data:
                self.storage.append(str(x))
        else:
            self.storage.append(str(data))
        print(data)

    def output(self) -> tuple[int, str]:
        value = self.storage.pop(0)
        piece = self.piece
        self.piece += 1
        return (piece, value)

class TextProcessor(DataProcessor):
    def __init__(self):
        super().__init__()

    def validate(self, data: Any) -> bool:
        return isinstance(data, str) or (
            isinstance(data, list) and all(isinstance(x, str) for x in data))

    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        pass

class LogProcessor(DataProcessor):
    def __init__(self):
        super().__init__()

    def validate(self, data: Any) -> bool:
        if isinstance(data, dict):
            return all(isinstance(x, str) and isinstance(y, str) for x, y in data.items())
        elif isinstance(data, list):
            return all(isinstance(x, dict) and
            all(isinstance(y, str) and isinstance (z, str)
            for y, z in x.items()) for x in data)

    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        pass


if __name__ == "__main__":
    list_nb = [1, 2, 3, 4 , 5]
    list_str = ["abc", "def", "xyz"]
    dict_str = {"key" : "value"}
    list_dict_str = [
        {"key" : "value"},
        {"key2" : "value2"},
    ]
    num = NumericProcessor()
    txt = TextProcessor()
    log = LogProcessor()
    print("=== Code Nexus - Data Processor ===\n")
    print("Testing Numeric Processor...")
    print(f"Trying to validate input '42': {num.validate(42)}")
    print(f"Trying to validate input 'Hello': {num.validate('Hello')}")
    print(f"Trying to validate input '{list_nb}': {num.validate(list_nb)}")
    print(f"Trying to validate input '{list_str}': {num.validate(list_str)}")
    print(f"Test invalid ingestion of string 'foo' without prior validation:")
    try:
        num.ingest('foo')
    except ValueError as e:
        print(f"Got exception: {e}")
    print()
    print("Testing Text Processor...")
    print(f"Trying to validate input '42': {txt.validate(42)}")
    print(f"Trying to validate input 'Hello': {txt.validate('Hello')}")
    print(f"Trying to validate input '{list_nb}': {txt.validate(list_nb)}")
    print(f"Trying to validate input '{list_str}': {txt.validate(list_str)}")
    print()
    print("Testing Log Processor...")
    print(f"Trying to validate input '{dict_str}': {log.validate(dict_str)}")
    print(f"Trying to validate input '{list_dict_str}': {log.validate(list_dict_str)}")
