import typing
from typing import Any
from abc import ABC, abstractmethod


class DataStream():
    def __init__(self) -> None:
        self.processors: Any = []

    def register_processor(self, proc: DataProcessor) -> None:
        self.processors.append(proc)

    def process_stream(self, stream: list[typing.Any]) -> None:
        for item in stream:
            sucess = False
            for processor in self.processors:
                if processor.validate(item):
                    processor.ingest(item)
                    sucess = True
                    break
            if not sucess:
                print(f"DataStream error - "
                      f"Can't process element in stream: {item}")

    def print_processors_stats(self) -> None:
        for processor in self.processors:
            print(f"{processor.__class__.__name__}:"
                  f"total {processor.total_processed}"
                  "items processed, remaining "
                  f"{len(processor.storage)} on processor")


class DataProcessor(ABC):
    def __init__(self) -> None:
        self.storage: list[tuple[int, str]] = []
        self.total_processed = 0

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
                self.total_processed += 1
        else:
            self.total_processed += 1
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
                self.total_processed += 1
        else:
            self.total_processed += 1
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
                self.total_processed += 1
        else:
            self.total_processed += 1
            self.storage.append((self.counter, format_log(data)))
            self.counter += 1


if __name__ == "__main__":
    stream = DataStream()
    num = NumericProcessor()
    txt = TextProcessor()
    log = LogProcessor()
    stream_data = [
        "Hello world",
        [3.14, -1, 2.71],
        [
            {
                "log_level": "WARNING",
                "log_message": "Telnet access! Use ssh instead",
            },
            {
                "log_level": "INFO",
                "log_message": "User wil is connected",
            },
        ],
        42,
        ["Hi", "five"],
    ]
    print("=== Code Nexus - Data Stream ===\n")
    print("Initialize Data Stream...")
    print("== DataStream statistics ==")
    print("No processor found, no data\n")
    print("Registering Numeric Processor\n")
    stream.register_processor(num)
    print(f"Send first batch of data on stream: {stream_data}")
    stream.process_stream(stream_data)
    print("== DataStream statistics ==")
    stream.print_processors_stats()
    print()
    print("Registering other data processors")
    stream.register_processor(txt)
    stream.register_processor(log)
    print("Send the same batch again")
    stream.process_stream(stream_data)
    stream.print_processors_stats()
    print()
    print("Consume some elements from the data processors:"
          " Numeric 3, Text 2, Log 1")
    for _ in range(3):
        num.output()
    for _ in range(2):
        txt.output()
    log.output()
    print("== DataStream statistics ==")
    stream.print_processors_stats()
