from dataclasses import dataclass

@dataclass
class Person:
    name: str
    balance: int = 0