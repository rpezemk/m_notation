class Glyphs:
    G_Clef = "\uE050"
    C_Clef = "\uE05C"
    F_Clef = "\uE062"
    Percussion_Clef_1 = "\uE069"
    Percussion_Clef_2 = "\uE06A"


    TimeSig_4_4 = "\uE08A"
    TimeSig_3_4 = "\uE086"
    TimeSig_2_4 = "\uE082"
    TimeSig_6_8 = "\uE09C"
    TimeSig_C = "\uE080"
    TimeSig_CutC = "\uE081"

    Staccato = "\uE4A0"
    Tenuto = "\uE4A3"
    Accent = "\uE4AC"
    Marcato = "\uE4A5"
    Fermata = "\uE4C0"

    Dynamic_Piano = "\uE520"
    Dynamic_MezzoPiano = "\uE521"
    Dynamic_MezzoForte = "\uE522"
    Dynamic_Forte = "\uE523"
    Dynamic_Fortissimo = "\uE524"
    Dynamic_Pianissimo = "\uE525"

    Barline_Single = "\uE030"
    Barline_Double = "\uE031"
    Barline_Final = "\uE032"
    Barline_Repeat_Left = "\uE040"
    Barline_Repeat_Right = "\uE041"

    Tuplet_3 = "\uE883"
    Tuplet_6 = "\uE886"

    Trill = "\uE566"
    Mordent = "\uE56A"
    Turn = "\uE56E"
    InvertedTurn = "\uE570"

    Arpeggio_Up = "\uE635"
    Arpeggio_Down = "\uE636"

    Octave_8va = "\uE510"
    Octave_15ma = "\uE512"
    Octave_22ma = "\uE514"

    BreathMark_Comma = "\uE4CE"
    BreathMark_Tick = "\uE4CF"
    # +E247

    
    RepeatEnding1 = "\uE00D"
    RepeatEnding2 = "\uE00E"

    Slur = "\uE010"
    Tie = "\uE015"

    GraceNoteSlash = "\uE2D4"
    GraceNoteAcciaccatura = "\uE563"

    Glissando = "\uE580"
    SlideIn = "\uE5B0"
    SlideOut = "\uE5B1"

    Tremolo_OneStroke = "\uE220"
    Tremolo_TwoStrokes = "\uE221"
    Tremolo_ThreeStrokes = "\uE222"

    Segno = "\uE047"
    Coda = "\uE048"
    DalSegno = "\uE045"
    DaCapo = "\uE046"
    Fine = "\uE044"

    PedalMark = "\uE650"
    PedalUpMark = "\uE653"

    Bracket = "\uE002"
    Brace = "\uE003"

    MarcatoStaccato = "\uE4B4"
    Staccatissimo = "\uE4A7"
    TenutoStaccato = "\uE4A6"

    OttavaAlta = "\uE510"
    OttavaBassa = "\uE511"

    Fingering_1 = "\uE550"
    Fingering_2 = "\uE551"
    Fingering_3 = "\uE552"
    Fingering_4 = "\uE553"
    Fingering_5 = "\uE554"

    StartSquareBracket = "\uE004"
    EndSquareBracket = "\uE005"

    MeasureRest = "\uE4E3"

    RepeatDot = "\uE043"

    StemUp = "\uE210"
    StemDown = "\uE211"

    BowingUp = "\uE610"
    BowingDown = "\uE611"

    BraceStaff = "\uE00F"

    Fermata_Upright = "\uE4C0"
    Fermata_Inverted = "\uE4C1"

    Forte = "\uE52F"
    Piano = "\uE530"
    Fortissimo = "\uE52A"
    Pianissimo = "\uE52B"



    AugDot = "\uE1E7"
    DoubleAugDot = "\uE1E8"
    
    LedgerLine = "\uE022"

    class Heads:
        Black = "\uE0A4"
        Half = "\uE0A3"
        Whole = "\uE0A2"
        DoubleWhole = "\uE0A0"
        X = "\uE0A7"

    class Notes():
        Maxima = "\uE95C"
        Longa = "\uE1D0"
        Breve = "\uE1D1"
        Whole = "\uE1D2"
        Half = "\uE1D3"
        Quarter = "\uE1D5"
        Eighth = "\uE1D7"
        Sixteenth = "\uE1D9"
        ThirtyTwo = "\uE1DB"
        SixtyFour = "\uE1DD"
    
    class Rests():
        Maxima = "\uE4E0"
        Longa = "\uE4E1"
        Breve = "\uE4E2"
        Whole = "\uE4E3"
        Half = "\uE4E4"
        Quarter = "\uE4E5"
        Eighth = "\uE4E6"
        Sixteenth = "\uE4E7"
        ThirtyTwo = "\uE4E8"
        SixtyFour = "\uE4E9"
        
    class Accidentals():
        Natural = "\uE260"
        Flat = "\uE261"
        Sharp = "\uE262"
        DoubleFlat = "\uE264"
        DoubleSharp = "\uE263"
        
    class Flags():
        class Up:
            Eighth = "\uE240"
            Sixteenth = "\uE242"
            ThirtySecond = "\uE244"  # Thirty-second note flag (upward)
            SixtyFourth = "\uE246"   # Sixty-fourth note flag (upward)
            ...
        class Down:
            Eighth = "\uE241"
            Sixteenth = "\uE243"
            ThirtySecond = "\uE245" # Thirty-second note flag (downward)
            SixtyFourth = "\uE247" # Sixty-fourth note flag (downward)
