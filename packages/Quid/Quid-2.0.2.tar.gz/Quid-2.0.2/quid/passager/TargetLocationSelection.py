from typing import List


class TargetLocationSelection:
    def __init__(self, target_text_id: int, target_location_ids: List[int]):
        self.target_text_id = target_text_id
        self.target_location_ids = target_location_ids

    @classmethod
    def from_value(cls, target_text_id, target_location_id):  # pragma: no cover
        return cls(target_text_id, [target_location_id])

    def add_target_location_id(self, target_location_id):
        if target_location_id not in self.target_location_ids:
            self.target_location_ids.append(target_location_id)
