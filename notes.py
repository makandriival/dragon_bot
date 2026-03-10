class Notes:
    def add_note(self, note: str):
        self.notes.append(note)

    def get_notes(self) -> list[str]:
        return self.notes
    
    # and any other methods you think are necessary for managing notes