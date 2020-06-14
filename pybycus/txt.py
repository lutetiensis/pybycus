""" TXT file parser. """

from pybycus.file import File

class Txt(File):
    """ Text Files

    A text file usually contains the writings (encoded as
    necessary) of one or more ancient authors. These all carry a
    traditional citation system. There are other kinds of text
    files, though, which may contain (e.g.) bibliographic data or
    morphologically analyzed text. For consistency, these texts
    also carry a citation system (usually a simple line
    increment).

    Text files are organized in blocks of 8192 bytes. Each
    block begins with the full citation for the first record of
    the block. Subsequent records are preceded by an abbreviated
    citation. Since the ID bytes are all marked with the sign bit
    set, the citation serves' to separate the variable length text
    records from one another. The end of block is signalled by an
    end of block marker in an ID field following the last record
    of the block. End of file is indicated by a marker preceding
    the end of block marker for the final block. Records do not
    span blocks. """

    def __init__(self, path):
        super().__init__(path)

        # Processing a block of text is therefore simple. Read in
        # all bytes with the sign bit set. This is the ID for the first
        # record. Call a subroutine to decode the ID data. Now read in
        # all bytes with the sign bit unset. This is the text of the
        # first record. Call a subroutine to process the text.  Repeat
        # this process for all records in the block, that is, until the
        # ID data contains the end of block marker.
        while True:
            if self.peek_ubyte() is None:
                break
            if self.peek_ubyte() == 0x00:
                _ = self.read_ubyte()
            elif self.peek_ubyte() > 0x7f:
                ids = self.read_id()
            else:
                self._content.append([self._id.copy(), self.read_string()])

def content(path):
    """ Return the content of a TXT file. """
    return Txt(path).content()

if __name__ == "__main__":
    import sys
    import pprint
    pprint.pprint(content(sys.argv[1]))
