from dataclasses import dataclass

@dataclass
class Person:
    full_name: str
    running_balance: int = 0