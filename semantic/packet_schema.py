from dataclasses import dataclass


@dataclass
class SemanticPacket:
    version: int
    language: str
    intent: str
    object: str
    location: str
    priority: str