from dataclasses import dataclass
from key_passager.TargetText import TargetText


@dataclass(frozen=True)
class TargetTextWithContent:
    target_text: TargetText
    content: str
