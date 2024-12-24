from enum import Enum

from utils.musical_layout.precise_aftermath import Ratio

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
    def to_beats(self) -> float:
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

    def to_ratio(self):
        durations = {
            Duration.LONGA: Ratio(t=(4, 1)),
            Duration.BREVE: Ratio(t=(2, 1)),
            Duration.WHOLE: Ratio(t=(1, 1)),
            Duration.HALF: Ratio(t=(1, 2)),
            Duration.QUARTER: Ratio(t=(1, 4)),
            Duration.EIGHTH: Ratio(t=(1, 8)),
            Duration.SIXTEENTH: Ratio(t=(1, 16)),
            Duration.THIRTY_SECOND: Ratio(t=(1, 32)),
            Duration.SIXTY_FOURTH: Ratio(t=(1, 64))
        }
        return durations[self]
        
        
    def get_all_durations():
        all_durations = [
            Duration.LONGA,
            Duration.BREVE,
            Duration.WHOLE,
            Duration.HALF,
            Duration.QUARTER,
            Duration.EIGHTH,
            Duration.SIXTEENTH,
            Duration.THIRTY_SECOND,
            Duration.SIXTY_FOURTH,
        ]
        return all_durations
    
    
# Example usage:
note = Duration.QUARTER
print(f"Duration of {note.value} in beats: {note.to_beats}")
