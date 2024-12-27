from enum import Enum

from model.ratio import Ratio
class Dotting(Enum):
    NO_DOT = Ratio(t=(1,1))
    ONE_DOT = Ratio(t=(3,2))
    TWO_DOTS = Ratio(t=(7,4))
    THREE_DOTS = Ratio(t=(15,8))
    FOUR_DOTS = Ratio(t=(31,16))
    
class DurationBase():
    LONGA = Ratio(t=(4,1))               # 4 times a whole note
    BREVE = Ratio(t=(2,1))               # 2 times a whole note
    WHOLE = Ratio(t=(1,1))               # 1 whole note
    HALF = Ratio(t=(1,2))                # 1/2 of a whole note
    QUARTER = Ratio(t=(1,4))             # 1/4 of a whole note
    EIGHTH = Ratio(t=(1,8))              # 1/8 of a whole note
    SIXTEENTH = Ratio(t=(1,16))          # 1/16 of a whole note
    THIRTY_SECOND = Ratio(t=(1,32))      # 1/32 of a whole note
    SIXTY_FOURTH = Ratio(t=(1,64))       # 1/64 of a whole note

    @property
    def to_beats(self) -> float:
        """Returns the note duration in terms of whole note beats"""
        durations = {
            DurationBase.LONGA: Ratio(t=(4,1)),
            DurationBase.BREVE: Ratio(t=(2,1)),
            DurationBase.WHOLE: Ratio(t=(1,1)),
            DurationBase.HALF: Ratio(t=(1,2)),
            DurationBase.QUARTER: Ratio(t=(1,4)),
            DurationBase.EIGHTH: Ratio(t=(1,8)),
            DurationBase.SIXTEENTH: Ratio(t=(1,16)),
            DurationBase.THIRTY_SECOND: Ratio(t=(1,32)),
            DurationBase.SIXTY_FOURTH: Ratio(t=(1,64)),
        }
        return durations[self]
        
    def get_all_durations():
        all_durations = [
            DurationBase.LONGA,
            DurationBase.BREVE,
            DurationBase.WHOLE,
            DurationBase.HALF,
            DurationBase.QUARTER,
            DurationBase.EIGHTH,
            DurationBase.SIXTEENTH,
            DurationBase.THIRTY_SECOND,
            DurationBase.SIXTY_FOURTH,
        ]
        return all_durations
    
