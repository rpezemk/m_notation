from enum import Enum

class Duration(Enum):
    LONGA = "Longa"                # 4 times a whole note
    BREVE = "Breve"                # 2 times a whole note
    WHOLE = "Whole"                # 1 whole note
    HALF = "Half"                  # 1/2 of a whole note
    QUARTER = "Quarter"            # 1/4 of a whole note
    EIGHTH = "Eighth"              # 1/8 of a whole note
    SIXTEENTH = "Sixteenth"        # 1/16 of a whole note
    THIRTY_SECOND = "ThirtySecond" # 1/32 of a whole note
    SIXTY_FOURTH = "SixtyFourth"   # 1/64 of a whole note

    @property
    def duration_in_beats(self):
        """Returns the note duration in terms of whole note beats"""
        durations = {
            Duration.LONGA: 4,
            Duration.BREVE: 2,
            Duration.WHOLE: 1,
            Duration.HALF: 0.5,
            Duration.QUARTER: 0.25,
            Duration.EIGHTH: 0.125,
            Duration.SIXTEENTH: 0.0625,
            Duration.THIRTY_SECOND: 0.03125,
            Duration.SIXTY_FOURTH: 0.015625
        }
        return durations[self]

# Example usage:
note = Duration.QUARTER
print(f"Duration of {note.value} in beats: {note.duration_in_beats}")
