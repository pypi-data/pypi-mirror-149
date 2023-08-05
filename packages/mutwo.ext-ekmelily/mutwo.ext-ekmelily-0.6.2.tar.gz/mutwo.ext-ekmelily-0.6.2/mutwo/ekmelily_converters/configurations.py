"""Configure default behaviour of :mod:`mutwo.ekmelily_converters`"""

try:
    import quicktions as fractions  # type: ignore
except ImportError:
    import fractions  # type: ignore


DEFAULT_GLOBAL_SCALE = (
    fractions.Fraction(0),
    fractions.Fraction(1),
    fractions.Fraction(2),
    fractions.Fraction(5, 2),
    fractions.Fraction(7, 2),
    fractions.Fraction(9, 2),
    fractions.Fraction(11, 2),
)
"""Default value for
:class:`~mutwo.ext.converters.frontends.ekmelily.EkmelilyTuningFileConverter`
argument `global_scale`."""


DEFAULT_PRIME_TO_HEJI_ACCIDENTAL_NAME_DICT = {
    prime: accidental_name
    for prime, accidental_name in zip(
        (5, 7, 11, 13, 17, 19, 23), "a b c d e f g".split(" ")
    )
}
"""Default mapping for
:class:`~mutwo.ext.converters.frontends.ekmelily.HEJIEkmelilyTuningFileConverter`
argument `prime_to_heji_accidental_name`."""

DEFAULT_PRIME_TO_HIGHEST_ALLOWED_EXPONENT_DICT = {
    prime: highest_allowed_comma
    # all potentially supported prime / max_exponent pairs:
    # (not used by default, because Lilypond would take too
    #  long for parsing)
    # for prime, highest_allowed_comma in zip(
    #     (5, 7, 11, 13, 17, 19, 23), (3, 2, 1, 1, 1, 1, 1),
    # )
    for prime, highest_allowed_comma in zip(
        (5, 7, 11, 13, 17),
        (3, 2, 1, 1, 1),
    )
}
"""Default value for
:class:`~mutwo.ext.converters.frontends.ekmelily.HEJIEkmelilyTuningFileConverter`
argument `prime_to_highest_allowed_exponent`."""

DEFAULT_TEMPERED_PITCH_INDICATOR = "t"
"""Default value for
:class:`~mutwo.ext.converters.frontends.ekmelily.HEJIEkmelilyTuningFileConverter`
argument `tempered_pitch_indicator`."""

DEFAULT_OTONALITY_INDICATOR = "o"
"""Default value for
:class:`~mutwo.ext.converters.frontends.ekmelily.HEJIEkmelilyTuningFileConverter`
argument `otonality_indicator`."""

DEFAULT_UTONALITY_INDICATOR = "u"
"""Default value for
:class:`~mutwo.ext.converters.frontends.ekmelily.HEJIEkmelilyTuningFileConverter`
argument `utonality_indicator`."""

# solution from: https://stackoverflow.com/questions/23199733/convert-numbers-into-corresponding-letter-using-python
DEFAULT_EXPONENT_TO_EXPONENT_INDICATOR = lambda exponent: chr(ord("a") + exponent)
"""Default function for
:class:`~mutwo.ext.converters.frontends.ekmelily.HEJIEkmelilyTuningFileConverter`
argument `exponent_to_exponent_indicator`."""

# Cleanup
del fractions
