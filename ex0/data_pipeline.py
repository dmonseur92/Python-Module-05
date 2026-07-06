from typing import Any
from abc import ABC, abstractmethod


class DataProcessor(ABC):
    def __init__(self) -> None:
        self.storage: list[tuple[int, str]] = []

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if not self.storage:
            raise IndexError("No data to output")
        return self.storage.pop(0)


class NumericProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__()
        self.counter = 0

    def validate(self, data: Any) -> bool:
        return isinstance(data, (int, float)) or (
            isinstance(data, list) and all(isinstance(x, (int, float))
                                           for x in data))

    def ingest(self, data: int | float | list[int] |
               list[float] | list[int | float]) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")

        if isinstance(data, list):
            for x in data:
                self.storage.append((self.counter, str(x)))
                self.counter += 1
        else:
            self.storage.append((self.counter, str(data)))
            self.counter += 1


class TextProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__()
        self.counter = 0

    def validate(self, data: Any) -> bool:
        return isinstance(data, str) or (
            isinstance(data, list) and all(isinstance(x, str) for x in data))

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")

        if isinstance(data, list):
            for x in data:
                self.storage.append((self.counter, x))
                self.counter += 1
        else:
            self.storage.append((self.counter, data))
            self.counter += 1


class LogProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__()
        self.counter = 0

    def validate(self, data: Any) -> bool:
        if isinstance(data, dict):
            return all(isinstance(k, str) and isinstance(v, str)
                       for k, v in data.items())
        elif isinstance(data, list):
            return all(
                isinstance(d, dict) and
                all(isinstance(k, str) and isinstance(v, str)
                    for k, v in d.items())
                for d in data
            )
        return False

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")

        def format_log(log: dict[str, str]) -> str:
            if "log_level" not in log or "log_message" not in log:
                raise ValueError("Invalid log format")
            return f"{log['log_level']}: {log['log_message']}"

        if isinstance(data, list):
            for log in data:
                self.storage.append((self.counter, format_log(log)))
                self.counter += 1
        else:
            self.storage.append((self.counter, format_log(data)))
            self.counter += 1


if __name__ == "__main__":
    list_nb = [1, 2, 3, 4, 5]
    list_str = ["Hello", "Nexus", "World"]
    list_dict_str = [
        {'log_level': 'NOTICE', 'log_message': 'Connection to server'},
        {'log_level': 'ERROR', 'log_message': 'Unauthorized access!!'}
    ]
    num = NumericProcessor()
    txt = TextProcessor()
    log = LogProcessor()
    print("=== Code Nexus - Data Processor ===\n")
    print("Testing Numeric Processor...")
    print(f"Trying to validate input '42': {num.validate(42)}")
    print(f"Trying to validate input 'Hello': {num.validate('Hello')}")
    print("Test invalid ingestion of string 'foo' without prior validation:")
    try:
        num.ingest('foo')
    except ValueError as e:
        print(f"Got exception: {e}")
    print(f"Processing data: {list_nb}")
    try:
        num.ingest(list_nb)
        print("Extracting 3 values...")
        for _ in range(3):
            rank, value = num.output()
            print(f"Numeric value {rank}: {value}")
    except ValueError as e:
        print(f"Got exception: {e}")

    print()
    print("Testing Text Processor...")
    print(f"Trying to validate input '42': {txt.validate(42)}")
    print(f"Processing data: {list_str}")
    try:
        txt.ingest(list_str)
        print("Extracting 3 values...")
        for _ in range(3):
            rank, value = txt.output()
            print(f"Text value {rank}: {value}")
    except ValueError as e:
        print(f"Got exception: {e}")
    print()
    print("Testing Log Processor...")
    print(f"Trying to validate input 'hello': {log.validate('hello')}")
    print(f"Processing data: {list_dict_str}")
    try:
        log.ingest(list_dict_str)
        print("Extracting 2 values...")
        for _ in range(2):
            rank, value = log.output()
            print(f"Log entry {rank}: {value}")
    except ValueError as e:
        print(f"Got exception: {e}")
