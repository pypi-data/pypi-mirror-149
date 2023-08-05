class TargetText:
    def __init__(self, my_id, filename, target_locations):
        self.my_id = my_id
        self.filename = filename
        self.target_locations = target_locations

    def __hash__(self) -> int:  # pragma: no cover
        return hash((self.my_id, self.filename, hash(self.target_locations)))

    def __eq__(self, other):  # pragma: no cover
        if not isinstance(other, TargetText):
            return NotImplemented

        return self.my_id == other.my_id
