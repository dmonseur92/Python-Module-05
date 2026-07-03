from typing import Any
from abc import ABC, abstractmethod

class DataProcessor(ABC):
    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        pass


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        return isinstance(data, (int, float)) or (
            isinstance(data, list) and all(isinstance(x,(int, float)) for x in data))

    def ingest(self, data: Any) -> None:
        self.sorted = []
        try:
            new_data = str(data)
            self.sorted.append(new_data)
        except Exception:
            print("Got exception: Improper numeric data")

    def output(self) -> tuple[int, str]:
        pass

class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        return isinstance(data, (str)) or (
            isinstance(data, list) and all(isinstance(x,(str)) for x in data))

    def ingest(self, data: Any) -> None:
        self.sorted = []
        try:
            new_data = str(data)
            self.sorted.append(new_data)
        except Exception:
            print("Got exception: Improper numeric data")

class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        return isinstance(data, (dict)) or (
            isinstance(data, list) and all(isinstance(x,(dict)) for x in data))

    def ingest(self, data: Any) -> None:
        self.sorted = []
        try:
            new_data = str(data)
            self.sorted.append(new_data)
        except Exception:
            print("Got exception: Improper numeric data")


if __name__ == "__main__":
    list_nb = [2, 3, 4]
    list_str = ["abc", "def", "xyz"]
    num = NumericProcessor()
    txt = TextProcessor()
    print("=== Code Nexus - Data Processor ===\n")
    print("Testing Numeric Processor...")
    print(f"Trying to validate input '42': {num.validate(42)}")
    print(f"Trying to validate input 'Hello': {num.validate('Hello')}")
    print(f"Trying to validate input '{list_nb}': {num.validate(list_nb)}")
    print(f"Trying to validate input '{list_str}': {num.validate(list_str)}")
    # print(f"Test invalid ingestion of string '{num.ingest('foo')}' without prior validation:")
    print()
    print("Testing Text Processor...")
    print(f"Trying to validate input '42': {txt.validate(42)}")
    print(f"Trying to validate input 'Hello': {txt.validate('Hello')}")
    print(f"Trying to validate input '{list_nb}': {txt.validate(list_nb)}")
    print(f"Trying to validate input '{list_str}': {txt.validate(list_str)}")
