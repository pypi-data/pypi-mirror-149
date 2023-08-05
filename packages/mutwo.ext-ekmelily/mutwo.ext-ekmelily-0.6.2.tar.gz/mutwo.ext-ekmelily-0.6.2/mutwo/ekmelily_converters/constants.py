"""Constants to be used for and with :mod:`mutwo.ekmelily_converters`.
"""

try:
    import quicktions as fractions  # type: ignore
except ImportError:
    import fractions  # type: ignore

from mutwo import music_parameters


# TODO(find glyph names in 'EkmelosGlyphNames.nam' file, provided
#      by Ekmelos 3.5 (instead of hard coding hexacodes))
PRIME_AND_EXPONENT_AND_TRADITIONAL_ACCIDENTAL_TO_ACCIDENTAL_GLYPH_DICT = {
    (
        None,
        None,
        music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
            fractions.Fraction(0, 1)
        ],
    ): ("#xE261"),
    (
        None,
        None,
        music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
            fractions.Fraction(1, 1)
        ],
    ): ("#xE262"),
    (
        None,
        None,
        music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
            fractions.Fraction(2, 1)
        ],
    ): ("#xE263"),
    (
        None,
        None,
        music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
            -fractions.Fraction(1, 1)
        ],
    ): ("#xE260"),
    (
        None,
        None,
        music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
            -fractions.Fraction(2, 1)
        ],
    ): ("#xE264"),
    (
        5,
        1,
        music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
            fractions.Fraction(0, 1)
        ],
    ): ("#xE2C2"),
    (
        5,
        2,
        music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
            fractions.Fraction(0, 1)
        ],
    ): ("#xE2C2"),
    (
        5,
        3,
        music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
            fractions.Fraction(0, 1)
        ],
    ): ("#xE2D6"),
    (
        5,
        -1,
        music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
            fractions.Fraction(0, 1)
        ],
    ): ("#xE2C7"),
    (
        5,
        -2,
        music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
            fractions.Fraction(0, 1)
        ],
    ): ("#xE2D1"),
    (
        5,
        -3,
        music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
            fractions.Fraction(0, 1)
        ],
    ): ("#xE2DB"),
    (
        5,
        1,
        music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
            fractions.Fraction(1, 1)
        ],
    ): ("#xE2C3"),
    (
        5,
        2,
        music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
            fractions.Fraction(1, 1)
        ],
    ): ("#xE2CD"),
    (
        5,
        3,
        music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
            fractions.Fraction(1, 1)
        ],
    ): ("#xE2D7"),
    (
        5,
        -1,
        music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
            fractions.Fraction(1, 1)
        ],
    ): ("#xE2C8"),
    (
        5,
        -2,
        music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
            fractions.Fraction(1, 1)
        ],
    ): ("#xE2D2"),
    (
        5,
        -3,
        music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
            fractions.Fraction(1, 1)
        ],
    ): ("#xE2DC"),
    (
        5,
        1,
        music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
            fractions.Fraction(2, 1)
        ],
    ): ("#xE2C4"),
    (
        5,
        2,
        music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
            fractions.Fraction(2, 1)
        ],
    ): ("#xE2CE"),
    (
        5,
        3,
        music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
            fractions.Fraction(2, 1)
        ],
    ): ("#xE2D8"),
    (
        5,
        -1,
        music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
            fractions.Fraction(2, 1)
        ],
    ): ("#xE2C9"),
    (
        5,
        -2,
        music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
            fractions.Fraction(2, 1)
        ],
    ): ("#xE2D3"),
    (
        5,
        -3,
        music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
            fractions.Fraction(2, 1)
        ],
    ): ("#xE2DD"),
    (
        5,
        1,
        music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
            -fractions.Fraction(1, 1)
        ],
    ): ("#xE2C1"),
    (
        5,
        2,
        music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
            -fractions.Fraction(1, 1)
        ],
    ): ("#xE2CB"),
    (
        5,
        3,
        music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
            -fractions.Fraction(1, 1)
        ],
    ): ("#xE2D5"),
    (
        5,
        -1,
        music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
            -fractions.Fraction(1, 1)
        ],
    ): ("#xE2C6"),
    (
        5,
        -2,
        music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
            -fractions.Fraction(1, 1)
        ],
    ): ("#xE2D0"),
    (
        5,
        -3,
        music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
            -fractions.Fraction(1, 1)
        ],
    ): ("#xE2DA"),
    (
        5,
        1,
        music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
            -fractions.Fraction(2, 1)
        ],
    ): ("#xE2C0"),
    (
        5,
        2,
        music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
            -fractions.Fraction(2, 1)
        ],
    ): ("#xE2CA"),
    (
        5,
        3,
        music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
            -fractions.Fraction(2, 1)
        ],
    ): ("#xE2D4"),
    (
        5,
        -1,
        music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
            -fractions.Fraction(2, 1)
        ],
    ): ("#xE2C5"),
    (
        5,
        -2,
        music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
            -fractions.Fraction(2, 1)
        ],
    ): ("#xE2CF"),
    (
        5,
        -3,
        music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
            -fractions.Fraction(2, 1)
        ],
    ): ("#xE2D9"),
    (7, 1, None): "#xE2DE",
    (7, 2, None): "#xE2E0",
    (7, -1, None): "#xE2DF",
    (7, -2, None): "#xE2E1",
    (11, 1, None): "#xE2E3",
    (11, -1, None): "#xE2E2",
    (13, 1, None): "#xE2E4",
    (13, -1, None): "#xE2E5",
    (17, 1, None): "#xE2E6",
    (17, -1, None): "#xE2E7",
    (19, 1, None): "#xE2E9",
    (19, -1, None): "#xE2E8",
    (23, 1, None): "#xE2EA",
    (23, -1, None): "#xE2EB",
}
"""Mapping of prime, exponent and pythagorean accidental to accidental
glyph name in Ekmelos."""


TEMPERED_ACCIDENTAL_TO_ACCIDENTAL_GLYPH_DICT = {
    music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
        fractions.Fraction(0, 1)
    ]: ("#xE2F2"),
    music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
        fractions.Fraction(1, 1)
    ]: ("#xE2F3"),
    music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
        fractions.Fraction(2, 1)
    ]: ("#xE2F4"),
    music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
        -fractions.Fraction(1, 1)
    ]: ("#xE2F1"),
    music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
        -fractions.Fraction(2, 1)
    ]: ("#xE2F0"),
    music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
        fractions.Fraction(1, 2)
    ]: ("#xE2F6"),
    music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
        -fractions.Fraction(1, 2)
    ]: ("#xE2F5"),
}
"""Mapping of tempered accidental name to glyph name in Ekmelos."""

TEMPERED_ACCIDENTAL_TO_CENT_DEVIATION_DICT = {
    music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
        fractions.Fraction(0, 1)
    ]: 0,
    music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
        fractions.Fraction(1, 1)
    ]: 100,
    music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
        fractions.Fraction(2, 1)
    ]: 200,
    music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
        -fractions.Fraction(1, 1)
    ]: -100,
    music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
        -fractions.Fraction(2, 1)
    ]: -200,
    music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
        fractions.Fraction(1, 2)
    ]: 50,
    music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
        -fractions.Fraction(1, 2)
    ]: -50,
}
"""Mapping of tempered accidental name to cent deviation."""


PYTHAGOREAN_ACCIDENTAL_CENT_DEVIATION_SIZE = round(
    (music_parameters.JustIntonationPitch((0, 7)).normalize(mutate=False).interval), 2  # type: ignore
)
"""Step in cents for one pythagorean accidental (# or b)."""

PYTHAGOREAN_ACCIDENTAL_TO_CENT_DEVIATION_DICT = {
    music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
        fractions.Fraction(0, 1)
    ]: 0,
    music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
        fractions.Fraction(1, 1)
    ]: PYTHAGOREAN_ACCIDENTAL_CENT_DEVIATION_SIZE,
    music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
        fractions.Fraction(2, 1)
    ]: PYTHAGOREAN_ACCIDENTAL_CENT_DEVIATION_SIZE
    * 2,
    music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
        -fractions.Fraction(1, 1)
    ]: -PYTHAGOREAN_ACCIDENTAL_CENT_DEVIATION_SIZE,
    music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
        -fractions.Fraction(2, 1)
    ]: -2
    * PYTHAGOREAN_ACCIDENTAL_CENT_DEVIATION_SIZE,
}
"""Step in cents mapping for each pythagorean accidental (# or b)."""

DIFFERENCE_BETWEEN_PYTHAGOREAN_AND_TEMPERED_FIFTH = (
    music_parameters.JustIntonationPitch("3/2").interval - 700
)
"""The difference in cents between a just fifth (3/2) and
a 12-EDO fifth. This constant is used in
:class:`~mutwo.ext.converters.frontends.ekmelily.HEJIEkmelilyTuningFileConverter`.
"""

# Cleanup
del fractions, music_parameters
