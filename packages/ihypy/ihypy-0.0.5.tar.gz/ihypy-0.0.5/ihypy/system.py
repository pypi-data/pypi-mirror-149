import abc as _abc
import re as _re

from . import theory as _theory

class NotationError(Exception):
    """Exception raised for errors in string representations of musical notation.

    Attributes
    ----------
    notation : str
        The faulty musical notation, expressed as a string.
    notation_system : str
        The notation system, expressed as a string.
    """

    def __init__(self, notation: str, notation_system: str):
        self.notation = notation
        self.notation_system = notation_system

    def __str__(self):
        return f"{self.notation} is not a valid musical notation in the {self.notation_system} notation system."

class TuningSystem(_abc.ABC):
    """Abstract class for tuning systems."""

    @_abc.abstractmethod
    def __init__(self):
        pass

    @_abc.abstractmethod
    def __str__(self):
        pass

    @_abc.abstractmethod
    def get_frequency_ratio(self, delta_unit: int | float) -> int | float:
        pass

class TwelveToneEqualTemperament(TuningSystem):
    """A 12 tone equal temperament tuning system, standard for pianos."""

    def __init__(self):
        self.__r = 2 ** (1 / 12)
        pass

    def __str__(self):
        return "EqualTemperament"

    def get_frequency_ratio(self, delta_half_step: int) -> float:
        """Get the frequency ratio based on the number of half_steps between two notes. This is the ratio between the after and before pitch.

        Parameters
        ----------
        delta_half_step : int
            The integer number of half_steps going from a pitch to another. A negative value indicates going down to the note.

        Returns
        -------
        float
            The ratio of frequencies.
        """
        return self.__r ** delta_half_step

class FiveLimitTuning(TuningSystem):
    """Just intonation, with 5-limit tuning."""

    def __init__(self):
        self.__interval_ratio = [1, 25/24, 9/8, 6/5, 5/4, 4/3, 45/32, 3/2, 8/5, 5/3, 9/5, 15/8]
        self.__octave_ratio = 2
        pass

    def __str__(self):
        return "FiveLimitTuning"

    def get_frequency_ratio(self, delta_half_step: int) -> float:
        """Get the frequency ratio based on the number of half_steps between two notes. This is the ratio between the after and before pitch.

        Parameters
        ----------
        delta_half_step : int
            The integer number of half_steps going from a pitch to another. A negative value indicates going down to the note.

        Returns
        -------
        float
            The ratio of frequencies.
        """
        ascending = 1 if delta_half_step >= 0 else -1
        octave, interval = divmod(abs(delta_half_step), 12)
        return (self.__octave_ratio ** octave * self.__interval_ratio[interval]) ** ascending

class NotationSystem(_abc.ABC):
    """Abstract class for notation systems.

    Attributes
    ----------
    valid_notation_pattern : re.Pattern
        The regular expression to fully match a musical object's notation.

    Methods
    -------
    validate_notation(notation: str) -> bool
        Check whether a certain notation is valid, based on the valid_notation_pattern.
    """

    @_abc.abstractmethod
    def __init__(self):
        pass

    @_abc.abstractmethod
    def __str__(self):
        pass

    @property
    def valid_notation_pattern(self) -> _re.Pattern:
        return self._valid_notation_pattern

    def validate_notation(self, notation: str) -> bool:
        """Check whether the string notation is valid.

        Parameters
        ----------
        notation : str
            The notation used to represent the note.

        Returns
        -------
        bool
            Whether the notation was valid.
        """
        return _re.fullmatch(self.valid_notation_pattern, notation) is not None

class NoteNotationSystem(NotationSystem):
    """Abstract class for notation systems of musical notes.

    Methods
    -------
    get_interval_between(self, from_notation: str, to_notation: str) -> Interval
        Get the interval between two notes based on their notations.
    """

    @_abc.abstractmethod
    def get_interval_between(self, from_notation: str, to_notation: str) -> _theory.Interval:
        pass

class InternationalPitchNotation(NoteNotationSystem):
    """The international pitch notation, described by pitch name, accidental, and octave number."""
    
    def __init__(self):
        self._pitch_conversion = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
        self._accidental_conversion = {"𝄫": -2, "bb": -2, "double_flat": -2, "df": -2,
                                        "♭": -1, "b": -1, "flat": -1, "f": -1,
                                        "♮": 0, "": 0, "natural": 0, "n": 0,
                                        "♯": 1, "#": 1, "sharp": 1, "s": 1,
                                        "𝄪": 2, "x": 2, "double_sharp": 2, "ds": 2}
        self.__pitch = "[A-G]"
        self.__accidental = "(" + "|".join(self._accidental_conversion.keys()) + ")"
        # self.__accidental = "(𝄫|bb|double_flat|df|♭|b|flat|f|♮||natural|n|♯|#|sharp|s|𝄪|x|double_sharp|ds)"
        self.__octave = "[+-]?\d+"
        self._valid_notation_pattern = _re.compile(self.__pitch + self.__accidental + self.__octave)

    def __str__(self):
        return "International Pitch Notation"

    def __get_absolute_half_step(self, notation):
        # get the absolute number of half_steps, with 0 half_steps defined as C0.

        _, start_accidental_index = _re.search(self.__pitch, notation).span()
        end_accidental_index, _ = _re.search(self.__octave, notation).span()
        
        pitch = notation[ : start_accidental_index]
        accidental = notation[start_accidental_index : end_accidental_index]
        octave = notation[end_accidental_index : ]

        return int(octave) * 12 + self._pitch_conversion[pitch] + self._accidental_conversion[accidental]

    def get_interval_between(self, from_notation: str, to_notation: str) -> _theory.SemitoneInterval:
        """Get the interval, in half_steps, between two pitches based on their notations.

        Parameters
        ----------
        from_notation : str
            The notation used to represent the starting note.
        to_notation : str
            The notation used to represent the ending note.

        Returns
        -------
        SemitoneInterval
            An interval with the number of half_steps. A negative number indicates going down.

        Raises
        ------
        NotationError
            If either of the notations are invalid.
        """
        if not self.validate_notation(from_notation):
            raise NotationError(from_notation, self)
        if not self.validate_notation(to_notation):
            raise NotationError(to_notation, self)
        return _theory.SemitoneInterval(self.__get_absolute_half_step(to_notation) - self.__get_absolute_half_step(from_notation))

class IntervalNotationSystem(NotationSystem):
    """Abstract class for notation systems of musical intervals.

    Methods
    -------
    get_interval : Interval
        Get the interval from an interval's notation.
    """
    @_abc.abstractmethod
    def __init__(self):
        pass

    @_abc.abstractmethod
    def get_interval(self, notation: str) -> _theory.Interval:
        pass

class QualityNumberSystem(IntervalNotationSystem):
    """Interval notation using quality and number for the chromatic scale."""

    def __init__(self):

        # define interval notation
        self.__quality_conversion_perfect = {"diminished": -1, "perfect": 0, "augmented": 1}
        self.__quality_conversion_perfect_abbrev = {"d": -1, "P": 0, "A": 1}
        self.__quality_conversion_imperfect = {"diminished": -1.5, "minor": -0.5, "major": 0.5, "augmented": 1.5}
        self.__quality_conversion_imperfect_abbrev = {"d": -1.5, "m": -0.5, "M": 0.5, "A": 1.5}

        self.__number_conversion_perfect = {"unison": 0, "fourth": 5, "fifth": 7, "octave": 12}
        self.__number_conversion_perfect_abbrev = {"1": 0, "4": 5, "5": 7, "8": 12}
        self.__number_conversion_imperfect = {"second": 1.5, "third": 3.5, "sixth": 8.5, "seventh": 10.5}
        self.__number_conversion_imperfect_abbrev = {"2": 1.5, "3": 3.5, "6": 8.5, "7": 10.5}
        
        self.__alternative  = {"semitone": 1, "half tone": 1, "half step": 1,
                               "tone": 1, "whole tone": 1, "whole step": 1,
                               "trisemitone": 3,
                               "tritone": 6}

        self.__quality_number_conversion = {}

        # full
        for quality_perfect, semitone_modification in self.__quality_conversion_perfect.items():
            for number_perfect, semitone_guess in self.__number_conversion_perfect.items():
                quality = quality_perfect + " " + number_perfect
                number = semitone_guess + semitone_modification
                self.__quality_number_conversion[quality] = number
                self.__quality_number_conversion[quality.title()] = number
        for quality_perfect, semitone_modification in self.__quality_conversion_imperfect.items():
            for number_perfect, semitone_guess in self.__number_conversion_imperfect.items():
                quality = quality_perfect + " " + number_perfect
                number = semitone_guess + semitone_modification
                self.__quality_number_conversion[quality] = number
                self.__quality_number_conversion[quality.title()] = number

        # abbreviated
        for quality_perfect, semitone_modification in self.__quality_conversion_perfect_abbrev.items():
            for number_perfect, semitone_guess in self.__number_conversion_perfect_abbrev.items():
                quality = quality_perfect + number_perfect
                number = semitone_guess + semitone_modification
                self.__quality_number_conversion[quality] = number
        for quality_perfect, semitone_modification in self.__quality_conversion_imperfect_abbrev.items():
            for number_perfect, semitone_guess in self.__number_conversion_imperfect_abbrev.items():
                quality = quality_perfect + number_perfect
                number = semitone_guess + semitone_modification
                self.__quality_number_conversion[quality] = number

        # other
        for quality, number in self.__alternative.items():
            self.__quality_number_conversion[quality] = number
            self.__quality_number_conversion[quality.title()] = number

        self._valid_notation_pattern = _re.compile("(" + "|".join(self.__quality_number_conversion.keys()) + ")")

    def __str__(self):
        return "Quality Number Notation"

    def get_interval(self, notation: str) -> _theory.SemitoneInterval:
        """Get the interval described by quality number notation in semitones.
        
        Parameters
        ----------
        notation: str
            The interval's notation. Abbreviations and common names acceptable.
        
        Returns
        -------
        SemitoneInterval
            The interval.

        Raises
        ------
        NotationError
            If the interval notation is invalid.
        """
        if not self.validate_notation(notation):
            raise NotationError(notation, str(self))
        return _theory.SemitoneInterval(self.__quality_number_conversion[notation])

class MusicalSystem(_abc.ABC):
    """Abstract class for musical systems, containing a notation system, tuning system, and pitch standard.

    Attributes
    ----------
    note_notation_system : NoteNotationSystem
        The notation system to use for notes.
    interval_notation_system : IntervalNotationSystem
        The interval notation system to use for intervals.
    tuning_system : TuningSystem
        The tuning system to use.
    pitch_standard : tuple[str, int | float]
        The pitch tuned to an absolute frequency.
    valid_chord_pattern : re.Pattern
        The regular expression to fully match a chord's notation.
    
    Methods
    -------
    create_note(notation: str) -> Note
        Create a note with the given notation based on the musical system's notation_system and tuning_system.
    create_scale(scale: Scale, notation: str) -> list[Note]
        Create a list of notes starting from the given notation based on the scale increments and musical system's notation_system and tuning_system.
    create_interval(interval: SemitoneInterval | str, note: Note | str = None) -> list[list[Note]] | SemitoneInterval
        Create a specific interval or generic SemitoneInterval.
    create_chord(chord: SemitoneChord | str, note: Note | str = None) -> list[list[Note]] | SemitoneChord
        Create a specific chord or generic SemitoneChord. The original root of the chord will be ignored if note is None. If the root of the chord and note do not match, the chord will be transposed to note.

    Notes
    -----
    With the exception of create_note, create_... methods have a corresponding _create_... method for a unit of measurement, such as interval. This allows for multiple musical systems to know how to create a chord similarly.
    """
    
    @_abc.abstractmethod
    def __init__(self):
        pass

    @property
    def note_notation_system(self) -> NoteNotationSystem:
        return self._note_notation_system

    @property
    def interval_notation_system(self) -> IntervalNotationSystem:
        return self._interval_notation_system

    @property
    def tuning_system(self) -> TuningSystem:
        return self._tuning_system

    @property
    def pitch_standard(self) -> tuple[str, int | float]:
        return (self._pitch_standard_notation, self._pitch_standard_frequency)

    @property
    def valid_chord_pattern(self) -> _re.Pattern:
        return self._valid_chord_pattern

    @_abc.abstractmethod
    def get_frequency(self, notation):
        # not truly abstract
        if not self.note_notation_system.validate_notation(notation):
            raise NotationError(self.note_notation_system, self.tuning_system)

    def create_note(self, notation: str) -> _theory.Note:
        """Create a note based on its notation.

        Parameters
        ----------
        notation : str
            The notation as a string.
    
        Returns
        -------
        Note
            The note, with the associated frequency.
        """
        return _theory.Note(self.get_frequency(notation))

    @_abc.abstractmethod
    def create_scale(self, scale: _theory.Scale, note: _theory.Note | str = None) -> list[_theory.Note]:
        pass

    @_abc.abstractmethod
    def create_interval(self, interval: _theory.Interval, note: _theory.Note | str = None) -> list[list[_theory.Note]] | _theory.Interval:
        pass

    @_abc.abstractmethod
    def create_chord(self, scale: _theory.Chord, note: _theory.Note | str = None) -> list[list[_theory.Note]] | _theory.Chord:
        pass

    def _create_scale(self, scale: _theory.Scale, note: _theory.Note | str) -> list[_theory.Note]:
        """Create a scale based on a starting note's notation and the scale structure.

        Parameters
        ----------
        scale : Scale
            The structure of the scale.
        note : Note | str
            The notation as a string, or the note itself.
    
        Returns
        -------
        list[Note]
            A list of notes.
        """
        if isinstance(note, str):
            note = self.create_note(note)
        scale_instance = [note]
        for delta_unit in scale.increment:
            frequency_ratio = self.tuning_system.get_frequency_ratio(delta_unit)
            prev_note = scale_instance[-1]
            scale_instance.append(_theory.Note(prev_note.frequency * frequency_ratio))
        return scale_instance

    def _create_semitone_interval(self, interval: _theory.SemitoneInterval | str, note: _theory.Note | str = None) -> list[list[_theory.Note]] | _theory.SemitoneInterval:
        """Create an interval based on a tonic note's notation and the interval structure.

        Parameters
        ----------
        interval : SemitoneInterval | str
            The structure of the scale. Either a string or SemitoneInterval.
        note : Note | str = None
            The tonic note's notation as a Note or string. If not specified, a generic interval will be returned.
    
        Returns
        -------
        list[list[Note]] | SemitoneInterval
            A list of singletons containing one note, or a SemitoneInterval.
        """
        if isinstance(interval, str):
            interval = self.interval_notation_system.get_interval(interval)
        if note is None:
            return interval

        if isinstance(note, str):
            tonic = self.create_note(note)
        else:
            tonic = note
        
        interval_instance = [[tonic], [_theory.Note(tonic.frequency * self.tuning_system.get_frequency_ratio(interval.relation))]]
        return interval_instance

    def __parse_semitone_chord(self, chord):
        # root -> quality (possibly an empty string) -> extension (possibly an empty string) -> altered (optional) -> suspended (optional) -> added (optional) -> slash (optional)
        pitch = chord[0]

        accidental_index = 1
        for possible_accidental in ['double_sharp', 'double_flat', 'natural', 'sharp', 'flat', 'bb', 'df', 'ds', '𝄫', '♭', 'b', 'f', '♮', 'n', '♯', '#', 's', '𝄪', 'x', '']:
            if chord[accidental_index:len(possible_accidental) + accidental_index] == possible_accidental:
                accidental = possible_accidental
                extension_index = len(possible_accidental) + accidental_index
                break
        root = pitch + accidental

        for possible_extension in ['minorMaj13', 'minorMaj11', 'halfdim11', 'minorMaj9', 'minorMaj7', 'halfdim13', 'augMaj11', 'minMaj11', 'augMaj13', 'minorM11', 'minorM13', 'minorΔ13', 'minMaj13', 'halfdim7', 'halfdim9', 'minorΔ11', 'minMaj9', 'augMaj7', 'halfdim', 'minorM9', 'minorΔ9', 'minor13', 'augMaj9', 'minorM7', 'minMaj7', 'minorΔ7', 'minor11', 'minM11', '+Maj11', '+Maj13', 'minΔ13', 'mMaj13', '-Maj11', 'augΔ11', 'augM11', 'minM13', 'augM13', '-Maj13', 'augΔ13', 'minor7', 'minΔ11', 'mMaj11', 'minor9', 'augΔ7', 'minM7', '-Maj7', 'minΔ9', 'min13', 'minor', '-Maj9', 'min11', 'aug13', 'aug11', 'augM7', 'dom11', 'Maj11', 'mMaj9', '+Maj7', 'dim11', 'augΔ9', 'dim13', 'dom13', 'mMaj7', 'minM9', 'minΔ7', 'Maj13', 'augM9', '+Maj9', 'min9', '-M11', 'mM11', 'dim7', 'dom9', '-M13', 'min7', 'Maj7', 'aug7', '+Δ11', 'mΔ13', 'mM13', 'dim9', '-Δ11', 'aug9', 'mΔ11', '-Δ13', 'dom7', 'Maj9', '+M13', '+Δ13', '+M11', '+M9', 'dim', 'Δ13', 'M13', '+Δ7', 'o11', '+13', 'Δ11', 'mΔ9', '-Δ9', 'ø11', '-M7', 'dom', 'm11', 'Maj', 'M11', '+11', '+M7', 'aug', 'o13', 'm13', 'min', '-M9', '+Δ9', '°13', 'mM7', '-13', '°11', 'mM9', '-Δ7', '-11', 'mΔ7', 'ø13', 'Δ7', '°7', '13', '-9', '11', '°9', '-7', 'ø7', '+9', 'ø9', 'M9', 'M7', 'o9', 'm9', '+7', 'm7', 'Δ9', 'o7', 'o', 'm', 'ø', '+', 'Δ', 'M', '-', '7', '°', '9', '']:
            if chord[extension_index:len(possible_extension) + extension_index] == possible_extension:
                extension = possible_extension
                altered_index = len(possible_extension) + extension_index
                break

        checking_altered = True
        altered = []
        while checking_altered:
            checking_altered = False

            for possible_altered in ['double_sharp13', 'double_sharp11', 'double_sharp5', 'double_sharp6', 'double_sharp7', 'double_sharp9', 'double_flat11', 'double_flat13', 'double_flat7', 'double_flat6', 'double_flat9', 'double_flat5', 'natural13', 'natural11', 'natural9', 'natural6', 'natural5', 'natural7', 'sharp13', 'sharp11', 'sharp5', 'flat11', 'sharp7', 'sharp6', 'sharp9', 'flat13', 'flat6', 'flat5', 'flat9', 'flat7', 'df11', 'df13', 'bb11', 'ds13', 'ds11', 'bb13', 'b13', '𝄫11', 's11', '𝄪13', '♭13', 'df5', 'n13', 'x13', 'bb5', '♭11', 'bb9', 'ds9', '♯13', '𝄫13', 'ds7', 'bb7', '#11', 'x11', 'ds5', 's13', 'f11', '♯11', '#13', 'df6', 'b11', '𝄪11', '♮11', '♮13', 'ds6', 'df9', 'n11', 'df7', 'bb6', 'f13', 'b7', 'n5', '♭7', '13', '♮7', 'f9', '𝄪6', 'n9', 'f5', 's5', '♮5', '♭9', 's7', 'b5', 'n6', 'x9', 'f6', '♯7', 'b9', '#5', '♭6', 'f7', 's9', '𝄫7', '11', '#6', '𝄫9', '𝄪9', 'x7', '♮6', 's6', '♮9', '#9', 'x5', '♭5', '𝄪7', '𝄪5', 'b6', '𝄫6', '♯9', 'n7', '𝄫5', '♯5', 'x6', '#7', '♯6', '6', '9', '5', '7']:
                if chord[altered_index:len(possible_altered) + altered_index] == possible_altered:
                    altered.append(possible_altered)
                    altered_index = len(possible_altered) + altered_index
                    checking_altered = True
                    break
        
        suspension_index = altered_index
        for possible_suspension in ["sus11", "sus9", "sus4", "sus2", ""]:
            if chord[suspension_index:len(possible_suspension) + suspension_index] == possible_suspension:
                suspension = possible_suspension
                add_index = len(possible_suspension) + suspension_index
                break

        for possible_add in ["add9", "add6", "add4", "add2", ""]:
            if chord[add_index:len(possible_add) + add_index] == possible_add:
                add = possible_add
                slash_index = len(possible_add) + add_index
                break

        slash = chord[slash_index:]
        
        return (root, extension, altered, suspension, add, slash)

    def __parse_root_slash(self, root, slash):
        # get the downwards interval from the root to slash
        
        # pick a random octave, adjust to force it to go down
        octave = "4"
        interval = self.note_notation_system.get_interval_between(root + octave, slash[1:] + octave)
        if interval.relation > 0:
            interval = _theory.SemitoneInterval(interval.relation - 12)
        return interval
    
    def __parse_extension(self, extension):

        intervals = []

        # add >7 extension (major/perfect), then replace with a 7
        if "13" in extension:
            intervals.append(_theory.MajorThirteenth())
            extension.replace("13", "7")
        elif "11" in extension:
            intervals.append(_theory.PerfectEleventh())
            extension.replace("11", "7")
        elif "9" in extension:
            intervals.append(_theory.MajorNinth())
            extension.replace("9", "7")

        # process any of the tertian sevenths
        if "7" in extension:

            # minor-major
            if ("m" in extension or "-" in extension) and ("M" in extension or "∆" in extension):
                intervals.append(_theory.MajorSeventh())
                intervals.append(_theory.PerfectFifth())
                intervals.append(_theory.MinorThird())

            # augmented major
            elif ("aug" in extension or "+" in extension) and ("M" in extension or "∆" in extension):
                intervals.append(_theory.MajorSeventh())
                intervals.append(_theory.AugmentedFifth())
                intervals.append(_theory.MajorThird())

            # half-dim
            elif ("halfdim" in extension or "ø" in extension):
                intervals.append(_theory.MinorSeventh())
                intervals.append(_theory.DiminishedFifth())
                intervals.append(_theory.MinorThird())

            # dim
            elif ("dim" in extension or "o" in extension or "°" in extension):
                intervals.append(_theory.DiminishedSeventh())
                intervals.append(_theory.DiminishedFifth())
                intervals.append(_theory.MinorThird())

            # major
            elif ("M" in extension or "∆" in extension):
                intervals.append(_theory.MajorSeventh())
                intervals.append(_theory.PerfectFifth())
                intervals.append(_theory.MajorThird())

            # minor
            elif ("m" in extension or "-" in extension):
                intervals.append(_theory.MinorSeventh())
                intervals.append(_theory.PerfectFifth())
                intervals.append(_theory.MinorThird())

            # dom
            else:
                intervals.append(_theory.MinorSeventh())
                intervals.append(_theory.PerfectFifth())
                intervals.append(_theory.MajorThird())

        # process any triads
        else:

            # diminished
            if ("dim" in extension or "o" in extension or "°" in extension):
                intervals.append(_theory.DiminishedFifth())
                intervals.append(_theory.MinorThird())

            # augmented
            elif ("aug" in extension or "+" in extension):
                intervals.append(_theory.AugmentedFifth())
                intervals.append(_theory.MajorThird())

            # minor
            elif ("m" in extension or "-" in extension):
                intervals.append(_theory.PerfectFifth())
                intervals.append(_theory.MinorThird())

            # major
            else:
                intervals.append(_theory.PerfectFifth())
                intervals.append(_theory.MajorThird())

        return intervals

    def __parse_altered(self, altered, intervals):

        num_conversion = {"5": 7,
                          "6": 9,
                          "7": 11,
                          "9": 14,
                          "11": 17,
                          "13": 21}

        for alter in altered:

            accidental = ""
            num = ""
            num_index = -1
            for i, char in enumerate(alter):
                if char.isdigit():
                    num += char
                else:
                    accidental += char
                    num_index = i
            num_index += 1

            semitones = self.note_notation_system._accidental_conversion[accidental] + num_conversion[num]

            # correction
            if _theory.SemitoneInterval(num_conversion[num]) in intervals:
                intervals.remove(_theory.SemitoneInterval(num_conversion[num]))
            intervals.append(_theory.SemitoneInterval(semitones))

        return intervals

    def __parse_suspension(self, suspension, intervals):

        if suspension == "sus2" or suspension == "sus4":
            if _theory.MinorThird() in intervals:
                intervals.remove(_theory.MinorThird())
            elif _theory.MajorThird() in intervals:
                intervals.remove(_theory.MajorThird())
            
            if suspension == "sus2":
                intervals.append(_theory.MajorSecond())
            else:
                intervals.append(_theory.PerfectFourth())

        elif suspension == "sus9":
            intervals.append(_theory.MajorNinth())
        elif suspension == "sus11":
            intervals.append(_theory.PerfectEleventh())

        return intervals

    def __parse_add(self, add):

        if add == "add2":
            return _theory.MajorSecond()
        elif add == "add4":
            return _theory.PerfectFourth()
        elif add == "add6":
            return _theory.MajorSixth()
        elif add == "add9":
            return _theory.MajorNinth()

    def _create_semitone_chord(self, chord: _theory.SemitoneChord | str, note: _theory.Note | str = None) -> list[list[_theory.Note]] | _theory.SemitoneChord:
        """Create a chord based on a tonic note's notation and the chord structure.

        Parameters
        ----------
        chord : SemitoneChord | str
            The structure of the chord. Either a string or SemitoneInterval.
        note : Note | str = None
            The tonic note's notation as a Note or string. If not specified, a generic interval will be returned.
    
        Returns
        -------
        list[list[Note]] | SemitoneChord
            A list of singletons containing one note, or a SemitoneChord.
        """
        
        if isinstance(chord, str):
            if _re.fullmatch(self.valid_chord_pattern, chord) is None:
                raise NotationError(chord, self)
            
            root, extension, altered, suspension, add, slash =  self.__parse_semitone_chord(chord)

            intervals = []
            if slash != "":
                intervals.append(self.__parse_root_slash(root, slash))
            intervals += self.__parse_extension(extension)
            intervals = self.__parse_altered(altered, intervals)
            intervals = self.__parse_suspension(suspension, intervals)
            if add != "":
                intervals.append(self.__parse_add(add))
            intervals.sort(key = lambda interval: interval.relation)
            
            chord = _theory.SemitoneChord(intervals)

        if note is None:
            return chord

        if isinstance(note, str):
            tonic = self.create_note(note)
        else:
            tonic = note

        chord_instance = [[tonic]]
        for interval in chord.intervals:
            chord_instance.append([_theory.Note(tonic.frequency * self.tuning_system.get_frequency_ratio(interval.relation))])
        return chord_instance

class WesternClassicalSystem(MusicalSystem):
    """A standard Western classical system, using IPN and 12-TET.
    
    Methods
    -------
    get_frequency(notation: str) -> float
        Get the frequency, tuned by 12-TET, associated with the notation expressed in IPN.
    """

    def __init__(self):
        self._note_notation_system = InternationalPitchNotation()
        self._interval_notation_system = QualityNumberSystem()
        self._tuning_system = TwelveToneEqualTemperament()
        self._pitch_standard_notation = "A4"
        self._pitch_standard_frequency = 440
        self._valid_chord_pattern = _re.compile("([A-G](𝄫|bb|double_flat|df|♭|b|flat|f|♮||natural|n|♯|#|sharp|s|𝄪|x|double_sharp|ds))(°|o|dim|ø|halfdim|m|min|minor|-|dom||M|Maj|Δ|aug|\+)?((°|o|dim|ø|halfdim|m|min|minor|-|dom||M|Maj|Δ|aug|\+)?(7|9|11|13))?((𝄫|bb|double_flat|df|♭|b|flat|f|♮||natural|n|♯|#|sharp|s|𝄪|x|double_sharp|ds)(5|6|7|9|11|13))*(sus(2|4|9|11))?(add(2|4|6|9))?(\/[A-G](𝄫|bb|double_flat|df|♭|b|flat|f|♮||natural|n|♯|#|sharp|s|𝄪|x|double_sharp|ds))?")

    def get_frequency(self, notation: str) -> float:
        """Get the 12-TET frequency of the IPN notation.

        Parameters
        ----------
        notation : str
            The IPN notation as a string.
    
        Returns
        -------
        float
            The frequency, in Hz.
        """
        super().get_frequency(notation)
        pitch_standard_notation, pitch_standard_frequency = self.pitch_standard
        delta_half_step = self.note_notation_system.get_interval_between(pitch_standard_notation, notation).relation
        return pitch_standard_frequency * self.tuning_system.get_frequency_ratio(delta_half_step)

    def create_scale(self, scale: _theory.Scale, note: _theory.Note | str = None) -> list[_theory.Note]:
        return self._create_scale(scale, note)

    def create_interval(self, interval: _theory.Interval, note: _theory.Note | str = None) -> list[list[_theory.Note]] | _theory.Interval:
        return self._create_semitone_interval(interval, note)

    def create_chord(self, scale: _theory.Chord, note: _theory.Note | str = None) -> list[list[_theory.Note]] | _theory.Chord:
        return self._create_semitone_chord(scale, note)

class PtolemaicSystem(MusicalSystem):
    """A Ptolemaic sequence, or justly tuned major scale, using IPN and 5-limit tuning.
    
    Methods
    -------
    get_frequency(notation: str) -> float
        Get the frequency, tuned by Ptolemy's intense diatonic scale, associated with the notation expressed in IPN.
    """

    def __init__(self):
        self._note_notation_system = InternationalPitchNotation()
        self._interval_notation_system = QualityNumberSystem()
        self._tuning_system = FiveLimitTuning()
        self._pitch_standard_notation = "A4"
        self._pitch_standard_frequency = 440
        self._valid_chord_pattern = _re.compile("([A-G](𝄫|bb|double_flat|df|♭|b|flat|f|♮||natural|n|♯|#|sharp|s|𝄪|x|double_sharp|ds))(°|o|dim|ø|halfdim|m|min|minor|-|dom||M|Maj|Δ|aug|\+)?((°|o|dim|ø|halfdim|m|min|minor|-|dom||M|Maj|Δ|aug|\+)?(7|9|11|13))?((𝄫|bb|double_flat|df|♭|b|flat|f|♮||natural|n|♯|#|sharp|s|𝄪|x|double_sharp|ds)(5|6|7|9|11|13))*(sus(2|4|9|11))?(add(2|4|6|9))?(\/[A-G](𝄫|bb|double_flat|df|♭|b|flat|f|♮||natural|n|♯|#|sharp|s|𝄪|x|double_sharp|ds))?")

    def get_frequency(self, notation: str) -> float:
        """Get the 5-limit tuning frequency of the IPN notation.

        Parameters
        ----------
        notation : str
            The IPN notation as a string.
    
        Returns
        -------
        float
            The frequency, in Hz.
        """
        super().get_frequency(notation)
        pitch_standard_notation, pitch_standard_frequency = self.pitch_standard
        delta_half_step = self.note_notation_system.get_interval_between(pitch_standard_notation, notation).relation
        return pitch_standard_frequency * self.tuning_system.get_frequency_ratio(delta_half_step)

    def create_scale(self, scale: _theory.Scale, note: _theory.Note | str = None) -> list[_theory.Note]:
        return self._create_scale(scale, note)

    def create_interval(self, interval: _theory.Interval, note: _theory.Note | str = None) -> list[list[_theory.Note]] | _theory.Interval:
        return self._create_semitone_interval(interval, note)

    def create_chord(self, scale: _theory.Chord, note: _theory.Note | str = None) -> list[list[_theory.Note]] | _theory.Chord:
        return self._create_semitone_chord(scale, note)