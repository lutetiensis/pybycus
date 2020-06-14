""" AUTHTAB.DIR file parser. """

from pybycus.file import File

class AuthTab(File):
    """ The Author List (with the filename AUTHTAB.DIR) contains
    descriptive information for each text file on the disc. The
    purpose of the Author Table is to allow the user to ask for
    the author Plato, for example, without having to know that
    the actual file name is TLG0059. Each entry contains the
    author name, the corresponding file name, synonyms, remarks,
    and language. The entries are arranged by category. """

    def __init__(self, path):
        super().__init__(path)

        while True:
             # An (optional) synonym for the author name is introduced by a
             # byte of hex 80 and is terminated by the first byte value above
             # hex 7f. Up to five synonyms are allowed for each author name.
             # pylint: disable=E0601
            if self.peek_ubyte() == 0x80:
                _ = self.read_ubyte()
                synonym = self.read_string()
                entry["aliases"].append(synonym)
                assert len(entry["aliases"]) <= 5
            # The (optional) remarks field is introduced by a byte of hex 81
            # and is terminated by the first byte value above hex 7f.
            elif self.peek_ubyte() == 0x81:
                assert False
            # The optional file size field is introduced by a byte of hex 82
            # and is terminated by the first byte value above hex 7f.
            elif self.peek_ubyte() == 0x82:
                assert False
            # The optional language code field is introduced by a byte of hex 83
            # and is terminated by the first byte value above hex 7f.
            elif self.peek_ubyte() == 0x83:
                _ = self.read_ubyte()
                language_code = self.read_string()
                entry["language_code"] = language_code
            # The entry is terminated by at least one hex ff (decimal 255). A
            # second ff is used when needed to pad the entry to an even byte
            # boundary.
            elif self.peek_ubyte() == 0xff:
                _ = self.read_ubyte()
            # Each entry begins with a file name (without any file name
            # extension) on an even byte boundary. The name is padded with
            # blanks if necessary to reach the fixed length of 8 bytes.
            else:
                # If the file name starts with an asterisk, it is a library
                # name (four characters including the asterisk). In this case
                # the second four bytes are the binary length of the library
                # (including the 8 bytes for the asterisk, name and length).
                if chr(self.peek_ubyte()) == '*':
                    name = self.read_nstring(4)
                    # If the file name starts *END it marks the end of the
                    # list. The second four bytes are binary zeroes.
                    if name == "*END":
                        padding = self.read_uint()
                        assert len(name) == 4 and padding == 0x0000
                        break
                    listlen = self.read_uint()
                    title = self.read_string()
                    library = {"name": name, "title": title, "entries": []}
                    self._content.append(library)
                # The full author name (of any reasonable length) starts after
                # the filename and is terminated by the first byte value above
                # 7f (decimal 127).
                else:
                    filename = self.read_string()
                    entry = {"id": filename[:7],
                             "name": filename[8:],
                             "aliases": []}
                    library["entries"].append(entry)

def content(path):
    """ Return the content of an AUTHTAB.DIR file. """
    return AuthTab(path).content()

if __name__ == "__main__":
    import sys
    import pprint
    pprint.pprint(content(sys.argv[1]))
