""" Beta code translation tables. """

class BetaCode:
    """ This class converts Beta Code to UTF-8.

    It was written based on:
    "The TLG® Beta Code Manual", last updated January 14, 2016, tlg@uci.edu
    http://stephanus.tlg.uci.edu/encoding/BCM.pdf """

    # 1. Alphabets and Basic Punctuation

    # Section 1 outlines the characters used to represent the alphabets, basic
    # punctuation and basic font formatting. (Beta Codes Categories $ and %)

    # 1.1 Greek
    ALPHABET_GREEK = {
        '*A': '\u0391',
        'A': '\u03B1',
        '*B': '\u0392',
        'B': '\u03B2',
        '*C': '\u039E',
        'C': '\u03BE',
        '*D': '\u0394',
        'D': '\u03B4',
        '*E': '\u0395',
        'E': '\u03B5',
        '*F': '\u03A6',
        'F': '\u03C6',
        '*G': '\u0393',
        'G': '\u03B3',
        '*H': '\u0397',
        'H': '\u03B7',
        '*I': '\u0399',
        'I': '\u03B9',
        '*K': '\u039A',
        'K': '\u03BA',
        '*L': '\u039B',
        'L': '\u03BB',
        '*M': '\u039C',
        'M': '\u03BC',
        '*N': '\u039D',
        'N': '\u03BD',
        '*O': '\u039F',
        'O': '\u03BF',
        '*P': '\u03A0',
        'P': '\u03C0',
        '*Q': '\u0398',
        'Q': '\u03B8',
        '*R': '\u03A1',
        'R': '\u03C1',
        '*S': '\u03A3',
        'S': '\u03C3', # or 03C2
        'S1': '\u03C3',
        'S2': '\u03C2',
        '*S3': '\u03F9',
        'S3': '\u03F2',
        '*T': '\u03A4',
        'T': '\u03C4',
        '*U': '\u03A5',
        'U': '\u03C5',
        '*V': '\u03DC',
        'V': '\u03DD',
        '*W': '\u03A9',
        'W': '\u03C9',
        '*X': '\u03A7',
        'X': '\u03C7',
        '*Y': '\u03A8',
        'Y': '\u03C8',
        '*Z': '\u0396',
        'Z': '\u03B6',
        ')': '\u0313',
        '(': '\u0314',
        '/': '\u0301',
        '=': '\u0342',
        '\\': '\u0300',
        '+': '\u0308',
        '|': '\u0345',
        '?': '\u0323',
        '.': '\u002E',
        ',': '\u002C',
        ':': '\u00B7',
        ';': '\u003B',
        "'": '\u2019',
        '-': '\u2010',
        '_': '\u2014',
    }

    # 1.2 Latin
    ALPHABET_LATIN = {
        'A': '\u0041',
        'a': '\u0061',
        'B': '\u0042',
        'b': '\u0062',
        'C': '\u0043',
        'c': '\u0063',
        'D': '\u0044',
        'd': '\u0064',
        'E': '\u0045',
        'e': '\u0065',
        'F': '\u0046',
        'f': '\u0066',
        'G': '\u0047',
        'g': '\u0067',
        'H': '\u0048',
        'h': '\u0068',
        'I': '\u0049',
        'i': '\u0069',
        'J': '\u004A',
        'j': '\u006A',
        'K': '\u004B',
        'k': '\u006B',
        'L': '\u004C',
        'l': '\u006C',
        'M': '\u004D',
        'm': '\u006D',
        'N': '\u004E',
        'n': '\u006E',
        'O': '\u004F',
        'o': '\u006F',
        'P': '\u0050',
        'p': '\u0070',
        'Q': '\u0051',
        'q': '\u0071',
        'R': '\u0052',
        'r': '\u0072',
        'S': '\u0053',
        's': '\u0073',
        'T': '\u0054',
        't': '\u0074',
        'U': '\u0055',
        'u': '\u0075',
        'V': '\u0056',
        'v': '\u0076',
        'W': '\u0057',
        'w': '\u0077',
        'X': '\u0058',
        'x': '\u0078',
        'Y': '\u0059',
        'y': '\u0079',
        'Z': '\u005A',
        'z': '\u007A',
        '-': '\u2010',
        '_': '\u2014',
    }

    # 1.3 Coptic
    ALPHABET_COPTIC = {
    }

    # 1.4 Hebrew
    ALPHABET_HEBREW = {
    }

    ALPHABET = {'g': ALPHABET_GREEK, 'l': ALPHABET_LATIN}

    # 1.5 $ and & – Text Styles

    def process_dollar(self, mod):
        """ Process beta code starting with $. """
        self._alphabet = "g"
        return ""

    def process_ampersand(self, mod):
        """ Process beta code starting with &. """
        self._alphabet = "l"
        return ""

    # 2. Formatting Beta Codes

    # Section 2 outlines the further Beta Code escapes for page formatting, text
    # markup and text formatting. (Beta Code Categories ^, @, { and <)

    # 2.1 ^ and @ – Page Formatting

    def process_hat(self, mod):
        """ Process beta code starting with ^. """
            # Blank Quarter Space
        return " " * int(mod / 4)

    def process_at(self, mod):
        """ Process beta code starting with @. """
            # Nothing to do
        return ""

    # 2.2 { – Textual Mark-Up

    def process_lcurly(self, mod):
        """ Process beta code starting with {. """
            # Nothing to do
        return ""

    def process_rcurly(self, mod):
        """ Process beta code starting with }. """
            # Nothing to do
        return ""

    # 2.3 < – Text Formatting

    def process_langle(self, mod):
        """ Process beta code starting with <. """
        return ""

    def process_rangle(self, mod):
        """ Process beta code starting with >. """
        return ""

    # 3. Further punctuation and characters

    # Section 3 outlines the further Beta Code escapes for punctuation and further
    # characters. (Beta Code Categories ", [, % and #)

    # 3.1 " – Quotation Marks
    ESCAPE_QUOTES = {
        0: {True:    '\u201C',     # “ Left Double Quotation Mark
            False:   '\u201D',     # ” Right Double Quotation Mark
            "state": True},
        1: {True:    '\u201E',     # „ Left Low Double Quotation Mark
            False:   '\u201E',
            "state": True},
        2: {True:    '\u201C',     # “ Right High Double Quotation Mark
            False:   '\u201C',
            "state": True},
        3: {True:    '\u2018',     # ‘ Left Single Quotation Mark
            False:   '\u2019',     # ’ Right Single Quotation Mark
            "state": True},
        4: {True:    '\u201A',     # ‚ Left Low Single Quotation Mark
            False:   '\u201A',
            "state": True},
        5: {True:    '\u201B',     # ‛ Right High Single Quotation Mark
            False:   '\u201B',
            "state": True},
        6: {True:    '\u00AB',     # « Left-Pointing Double Angle Quotation Mark
            False:   '\u00BB',     # » Right-Pointing Double Angle Quotation Mark
            "state": True},
        7: {True:    '\u2039',     # ‹ Left-Pointing Single Angle Quotation Mark
            False:   '\u203A',     # › Right-Pointing Single Angle Quotation Mark
            "state": True},
        8: {True:    '\u201C',     # “ Left High Double Quotation Mark
            False:   '\u201E',     # „ Right Low Double Quotation Mark
            "state": True},
        # "50-"59 Papyrological Project Quotation Marks
        # "60-"69 Epigraphical Project Quotation Marks
    }

    def process_quotes(self, mod):
        """ Process beta code starting with ". """
        try:
            state = self.ESCAPE_QUOTES[mod]["state"]
            string = self.ESCAPE_QUOTES[mod][state]
            self.ESCAPE_QUOTES[mod]["state"] = not state
            return string
        except KeyError:
            print("!!! [%s" % mod)
            return ""

    # 3.2. [ – Brackets
    ESCAPE_LSQUARE = {
        0: '\u005B',     # [ Left Square Bracket
        1: '\u0028',     # ( Left Parenthesis
        2: '\u2329',     # < Left-Pointing Angle Brackets
        3: '\u007B',     # { Left Curly Bracket
        4: '\u27E6',     # ⟦ Left White Square Bracket
        5: '\u2E44',     # ⌊ Left Low Corner Bracket
        6: '\u2E42',     # ⌈ Left High Corner Bracket
        7: '\u2E42',     # ⌈ Left High Corner Bracket
        8: '\u2E44',     # ⌊ Left Low Corner Bracket
        9: '\u2027',     # ‧ Hyphenation Point - Left Raised Dot Bracket
        10: '\u005B',     # [ Large Left Square Bracket
        11: '\u208D',     # ( Subscript Left Parentheses
        12: '\u2192',     # → Rightward Arrow - Left Arrow Bracket
        13: '$3\u005B',     # [ Italic Left Square Bracket
        14: '\u007c\u003a',     # |: Vertical Line and Colon - Left Hymn Refrain Bracket
        15: '',           # non-TLG Franklin Decipherment of Codes
        16: '\u27E6',     # ⟦ Left White Square Bracket
        17: '\u230A\u230A',     # ⌊⌊ Left Low White Corner Bracket
        18: '\u27EA',     # ⟪ Left Double Angle Bracket
        20: '\u23A7',     # ⎧ Left Curly Bracket Upper Hook
        21: '\u23AA',     # ⎪ Curly Bracket Extension
        22: '\u23A8',     # ⎨ Left Curly Bracket Middle Piece
        23: '\u23A9',     # ⎩ Left Curly Bracket Lower Hook
        30: '\u239B',     # ⎛ Left Parenthesis Upper Hook
        31: '\u239C',     # ⎜ Left Parenthesis Extension
        32: '\u239D',     # ⎝ Parenthesis Lower Hook
        33: '',           # non-TLG Parenthesis
        34: '',           # non-TLG Parenthesis
        35: '',           # non-TLG Papyrological Project Brackets
        50: '',           # non-TLG Rejected Text of Main Edition
        51: '',           # non-TLG Erased Text
        52: '',           # non-TLG Text Before Correction
        53: '',           # non-TLG Parenthesis
        54: '',           # non-TLG Epigraphical Project Brackets
        70: '\u2E02',     # ⸂ Left Substitution Bracket
        71: '\u2E04',     # ⸄ Left Dotted Substitution Bracket
        72: '\u2E09',     # ⸉ Left Transposition Bracket
        73: '\u2E0B',     # ⸋ Raised Square - Left Raised Omission Bracket
        80: '\u002F',     # / Solidus - Left Interlinear Addition Printed Inline
        81: '\u002F\u002F',     # // Solidus and Solidus - Left Marginal Addition Printed Inline
        # Next four characters were changed from \u2E4? to \u2E2?.
        82: '\u2E20',     # ⸠ Opening Editorial Deletion Bracket - Left Vertical Bar With Quill
        83: '\u2E21',     # ⸡ Opening Editorial Dittography Bracket - Right Vertical Bar With Quill
        84: '\u2E26', #􏰃⸦ Left Sideways U Bracket
        85: '\u2E28',     # (( Left Double Parenthesis
    }

    ESCAPE_RSQUARE = {
        0: '\u005D',     # ] Right Square Bracket
        1: '\u0029',     # ) Right Parenthesis
        2: '\u232A',     # > Right-Pointing Angle Brackets
        3: '\u007D',     # } Right Curly Bracket
        4: '\u27E7',     # ⟧ Right White Square Bracket
        5: '\u2E45',     # ⌋ Right Low Corner Bracket
        6: '\u2E43',     # ⌉ Right High Corner Bracket
        7: '\u2E45',     # ⌋ Right High Corner Bracket
        8: '\u2E43',     # ⌉ Right Low Corner Bracket
        9: '\u2027',     # ‧ Hyphenation Point - Right Raised Dot Bracket
        10: '\u005b',     # ] Large Right Square Bracket
        11: '\u208E',     # ) Subscript Right Parentheses
        12: '\u2190',     # ← Leftward Arrow - Right Arrow Bracket
        13: '\u005D$',     # ] Italic Right Square Bracket
        14: '\u003A\u007c',     # :| Colon and Vertical Line - Right Hymn Refrain Bracket
        15: '',           # non-TLG Franklin Decipherment of Codes
        16: '\u27E7',     # ⟧ Right White Square Bracket
        17: '\u230B\u230B',     # ⌋⌋ Right Low White Corner Bracket
        18: '\u27EB',     # ⟫ Right Double Angle Bracket
        20: '\u23AB',     # ⎫ Right Curly Bracket Upper Hook
        21: '\u23AA',     # ⎪ Curly Bracket Extension
        22: '\u23AC',     # ⎬ Right Curly Bracket Middle Piece
        23: '\u23AD',     # ⎭ Right Curly Bracket Lower Hook
        30: '\u239E',     # ⎞ Right Parenthesis Upper Hook
        31: '\u239F',     # ⎜ Right Parenthesis Extension
        # Next character was changed from \u32A0 for \23A0.
        32: '\u23A0',     # ⎠ Parenthesis Lower Hook
        33: '',           # non-TLG Parenthesis
        34: '',           # non-TLG Parenthesis
        35: '',           # non-TLG Papyrological Project Brackets
        50: '',           # non-TLG Rejected Text of Main Edition
        51: '',           # non-TLG Erased Text
        52: '',           # non-TLG Text Before Correction
        53: '',           # non-TLG Parenthesis
        54: '',           # non-TLG Epigraphical Project Brackets
        70: '\u2E03',     # ⸃ Right Substitution Bracket
        71: '\u2E05',     # ⸄ Right Dotted Substitution Bracket
        72: '\u2E0A',     # ⸊ Left Transposition Bracket
        73: '\u2E0C',     # ⸌ Left Raised Omission Bracket - Right Raised Omission Bracket
        80: '\u002F',     # / Solidus - Right Interlinear Addition Printed Inline
        81: '\u002F\u002F',     # // Solidus and Solidus - Right Marginal Addition Printed Inline
        # Next four characters were changed from \u2E4? to \u2E2?.
        82: '\u2E21',     # ⸡ Closing Editorial Deletion Bracket - Right Vertical Bar With Quill
        83: '\u2E20',     # ⸠ Closing Editorial Dittography Bracket - Left Vertical Bar With Quill
        84: '\u2E27', #􏰃⸧ Right Sideways U Bracket
        85: '\u2E29',     # )) Right Double Parenthesis
    }

    def process_lsquare(self, mod):
        """ Process beta code starting with [. """
        try:
            return self.ESCAPE_LSQUARE[mod]
        except KeyError:
            print("!!! [%s" % mod)
            return ""

    def process_rsquare(self, mod):
        """ Process beta code starting with ]. """
        try:
            return self.ESCAPE_RSQUARE[mod]
        except KeyError:
            print("!!! ]%s" % mod)
            return ""

    # 3.3 % – Additional Punctuation and Characters

    def process_percent(self, mod):
        """ Process beta code starting with %. """
        return ""

    # 3.4. # – Additional Characters

    def process_hash(self, mod):
        """ Process beta code starting with #. """
        return ""

    ESCAPE_CODES = {
        '$': process_dollar,
        '&': process_ampersand,
        '^': process_hat,
        '@': process_at,
        '{': process_lcurly,
        '}': process_rcurly,
        '<': process_langle,
        '>': process_rangle,
        '"': process_quotes,
        '[': process_lsquare,
        ']': process_rsquare,
        '%': process_percent,
        '#': process_hash,
    }

    def __init__(self, string):
        """ Convert beta code in a string. """
        self._content = u""
        self._alphabet = "l"
        i = 0
        while i < len(string):
            if string[i] in self.ESCAPE_CODES:
                esc = string[i]
                i += 1
                mod = 0
                while i < len(string) and string[i].isdigit():
                    mod = mod * 10 + int(string[i])
                    i += 1
                if i < len(string) and string[i] == '`':
                    i += 1
                self._content += self.ESCAPE_CODES[esc](self, mod)
            else:
                char = string[i]
                i += 1
                if i < len(string) and char == '*':
                    char += string[i]
                    i += 1
                if char in self.ALPHABET[self._alphabet]:
                    self._content += self.ALPHABET[self._alphabet][char]
                else:
                    self._content += char

    def get(self):
        """ Get the result of the conversion. """
        return self._content

def convert(string):
    """ Converts Beta Code string to UTF-8. """
    return BetaCode(string).get()
