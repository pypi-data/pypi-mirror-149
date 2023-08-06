
class NoDraftFound(Exception):
    def __init__(self, deposition_id: str):
        self.deposition_id: str = deposition_id

    def __str__(self):
        return (
            f"No drafts were found for the deposition with id: {self.deposition_id} "
            "make sure that a new version of the deposition exists."
        )
