from dataclasses import dataclass
from typing import List
from visualization.Info import Info
from visualization.TargetHtml import TargetHtml


@dataclass(frozen=True)
class Visualization:
    info: Info
    source_html: str
    targets_html: List[TargetHtml]
