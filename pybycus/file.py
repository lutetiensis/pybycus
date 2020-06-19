""" File reading operations. """

import re
import pybycus.beta

class File:
    """ You may be able to use a standard software driver to
    locate the files in the directory and read the file data from
    the CD ROM, but your program will need to read the file in
    binary mode and extract the text records from the blocks
    according to the format information presented in this
    document. """

    def __init__(self, path):
        self._f = open(path, "rb")
        self._content = []
        self._id = {}

    def content(self):
        """ Return the content of the file. """
        return self._content

    def peek_ubyte(self):
        """ Get next unsigned byte without moving the cursor. """
        byte = self._f.read(1)
        if byte == b'':
            return None
        self._f.seek(-1, 1)
        return int.from_bytes(byte, byteorder="big")

    def read_ubyte(self):
        """ Read unsigned byte from file. """
        return int.from_bytes(self._f.read(1), byteorder="big")

    def read_ubyte7(self):
        """ Read unsigned 7-bit byte from file. """
        return self.read_ubyte() & 0x7f

    def read_ushort(self):
        """ Read unsigned short from file. """
        return int.from_bytes(self._f.read(2), byteorder="big")

    def read_ushort14(self):
        """ Read unsigned 14-bit short from file. """
        return (self.read_ubyte7() << 7) | self.read_ubyte7()

    def read_uint(self):
        """ Read unsigned int from file. """
        return int.from_bytes(self._f.read(4), byteorder="big")

    def read_nstring(self, length):
        """ Read string of length `length'. """
        string = self._f.read(length).decode("utf-8")
        return pybycus.beta.convert(string)

    def read_cstring(self):
        """ Read string terminated by 0xff. """
        string = u""
        while self.peek_ubyte() != 0xff:
            string += chr(self.read_ubyte7())
        return pybycus.beta.convert(string)

    def read_string(self):
        """ Read 7-bit character string. """
        string = u""
        while self.peek_ubyte() <= 0x7f:
            string += chr(self.read_ubyte())
        return pybycus.beta.convert(string)

    # pylint: disable=R0912,R0915
    def read_id(self):
        """ Read ID data. """
        level = None
        token = None

        while self.peek_ubyte() > 0x7f:
            code = self.read_ubyte()
            left, right = (code & 0xf0) >> 4, code & 0x0f

            # Special code (not an ID): see below
            if left == 0xf:
                # end-of-ASCII-string
                if code == 0xff:
                    pass
                # end-of-block
                elif code == 0xfe:
                    pass
                # end-of-file
                elif code == 0xf0:
                    pass
                # exception start
                elif code == 0xf8:
                    pass
                # exception end
                elif code == 0xf9:
                    pass
                continue

            # Escape code: ID level will be found in next ID byte
            if left == 0xe:
                level = self.read_ubyte()
                if 0x80 <= level <= 0x83:
                    # 0x80 a-level author ID
                    # 0x81 b-level work ID
                    # 0x82 c-level work abbreviation
                    # 0x83 d-level author abbreviation
                    pass
                # Descriptive data
                #
                # The optional descriptor ID levels (a..z) are used
                # independently of levels a..d,n,v..z to hold comments or
                # descriptive information. They are not part of the citation
                # scheme and are not themselves hierarchical. The comment
                # contained in a descriptor ID level applies to all the text
                # lines that follow until the value of that descriptor level
                # changes or a change in the work or document level sets all the
                # descriptor levels to null. Their assignment (level 1, for
                # example, to indicate the location of a papyrus, or d to
                # indicate its date) is determined by the data preparer.
                # Although there are twenty-six possible descriptor ID levels
                # (a..z), PHI has used no more than eight in a single document.
                # PHI reserves the z descriptor level as a comment sequence
                # number within a work: in the display of continuous text (with
                # optimized ID's), it facilitates determining where the data
                # preparer intended a comment to appear but has no other
                # conventional meaning and is not part of the original comment.
                # These descriptors are not included in ID Table files.
                elif level in [0xe3, 0xe4, 0xec, 0xfa, 0xfb]:
                    # 0xe3 ?
                    # 0xe4 ?
                    # 0xec ?
                    # 0xfa ?
                    # 0xfb ?
                    pass
                else:
                    assert False
            # 0x8 z-level ID
            # 0x9 y-level ID
            # 0xa x-level ID
            # 0xb w-level ID
            # 0xc v-level ID
            # 0xd n-level ID
            elif 0x8 <= left <= 0xd:
                level = left

            # increment the ID at this level
            if right == 0x0:
                level_s = [i for i in
                           re.split(r'([A-Za-z]+)', self._id[level]) if i]
                if level_s[-1] == "1-2": # 1512.001
                    level_s[-1] = "1-3"
                elif level_s[-1] == "39-40": # 0137.001
                    level_s[-1] = "40"
                elif re.match("[0-9]+", level_s[-1]): # number increment
                    level_s[-1] = str(int(level_s[-1]) + 1)
                else: # string increment
                    level_s[-1] = level_s[-1][:-1] + chr(ord(level_s[-1][-1]) + 1)
                self._id[level] = "".join(level_s)
            # literal binary ID values
            elif 0x1 <= right <= 0x7:
                self._id[level] = str(right)
            # 7-bit binary value
            elif right == 0x8:
                self._id[level] = str(self.read_ubyte7())
            # 7-bit binary value + single ASCII character
            elif right == 0x9:
                self._id[level] = str(self.read_ubyte7()) + \
                                  chr(self.read_ubyte7())
            # 7-bit binary value + ASCII string
            elif right == 0xa:
                self._id[level] = str(self.read_ubyte7()) + \
                                  self.read_cstring()
            # 14-bit binary value
            elif right == 0xb:
                self._id[level] = str(self.read_ushort14())
            # 14-bit binary value + single ASCII character
            elif right == 0xc:
                self._id[level] = str(self.read_ushort14()) + \
                                  chr(self.read_ubyte7())
            # 14-bit binary value + ASCII string
            elif right == 0xd:
                self._id[level] = str(self.read_ushort14()) + \
                                  self.read_cstring()
            # same binary value + new single ASCII character
            elif right == 0xe:
                self._id[level] += self.read_ubyte7()
            # no binary value + ASCII string
            elif right == 0xf:
                self._id[level] = self.read_cstring()

            if 0x8 <= level <= 0xd:
                for i in range(0x8, level):
                    self._id[i] = "1"

        return level, token
