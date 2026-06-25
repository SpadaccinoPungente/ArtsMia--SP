from dataclasses import dataclass


@dataclass
class ArtObject:
    title: str
    style: str
    object_name: str
    object_id: int
    nationality: str
    dated: str
    classification: str

    def __hash__(self):
        return hash(self.object_id)

    def __str__(self):
        return f"{self.title}, {self.style}, {self.nationality}, {self.dated}"