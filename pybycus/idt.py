""" IDT file parser. """

from pybycus.file import File

class Idt(File):
    """ ID Table Files

    For each text file, the corresponding ID table file
    provides a detailed account of the identity and location of
    the authors and works for that file, the location of all major
    sections within the works, and a complete listing of the
    ending citation for each text block within a section. In the
    case of documents, information is given to the document (n)
    level only for the end of each text block and information
    about lower levels is not included. If the document id is the
    same at the end of consecutive blocks, the first block is
    marked with the document id, and the later ones have the new
    block code without any additional information.

    For example, the ID table for file TLG0012.TXT would tell
    us that the first author is named "Homer" and that-the author
    is cited "0012", that the first work is named "Iliad" and is
    cited "001", and that the first major section of this work is
    is Book 1. The block location for each of these is given, and
    the section data is followed by a list of the ending citations
    for each block in Book 1. The data for Book 1 will be followed
    by that for Book 2, and so forth until the second work is
    encountered.

    Note that each subdivision is nested, that is, the text
    for an author is divided into one or more works, the text for
    a work is divided into one or more sections, and the text for
    a section is divided into one or more blocks. A block may
    contain parts of two or more sections or works; work and
    section boundaries do not have to coincide with block
    boundaries. The works and sections are presented in the ID
    Table file in the same order as they are found in the text;
    they are not sorted.

    Because an editor will at times reorder a text but leave
    the traditional citation intact, the ID table makes provision
    for out-of-sequence lines. If an editor places a line numbered
    912 between lines 310 and 311, this will usually produce an
    exception field. An exception field lists the beginning and
    ending citation for lines which do not fall in the expected
    block. Note that if an editor positions line 314 between lines
    310 and 311, this will not usually produce an exception. The
    reason for this is that line 314 is very likely in the
    expected block, despite the fact that it is out of order
    within the block. Thus, to find line 912 in the example above,
    you would locate the block in the usual fashion. Immediately
    before the block which contains, say, lines 885-940, the
    exception would be listed along with the true block location
    for the line. """

    # pylint: disable=R0912,R0915
    def __init__(self, path):
        super().__init__(path)

        # Each entry in the ID table is introduced by a type code
        # byte from zero to thirty-one (decimal). Each type of entry
        # has its own form and function. The entry may introduce a
        # major section, provide descriptive information for a section,
        # or give the ID ranges for a section or block. The form of the
        # entries-is detailed below. Note that there is no length field
        # for entries which contain ID data. Since the ID data is
        # always the last field in the entry, and since ID bytes always
        # have the sign bit set, the end of the entry can be found by
        # reading the ID bytes until a byte is encountered with the
        # sign bit clear.
        while True:
            if self.peek_ubyte() is None:
                break
            # 0 * End of file.
            if self.peek_ubyte() == 0:
                _ = self.read_ubyte()
            # 1 * New author. Followed by a 2-byte length which is the
            # length of the author section (including all nested
            # works). The count includes the length field itself. The
            # length is followed by the- 2-byte block number. The block
            # number is the 8K block in which the author begins. The
            # block number is followed by the author ID.
            elif self.peek_ubyte() == 1:
                _ = self.read_ubyte()
                length = self.read_ushort()
                block = self.read_ushort()
                level, _ = self.read_id()
                assert level == 0x80
                author = {"anum": self._id[level], "works": {}}
                self._content.append(author)
            # 2 * New work. Followed by a 2-byte length which is the length
            # of the work section (including all nested subsections).
            # The count includes the length field itself. The length is
            # followed by the 2-byte block number. The block number is
            # the 8K block in which the work begins. The block number
            # is followed by the work ID.
            elif self.peek_ubyte() == 2:
                _ = self.read_ubyte()
                length = self.read_ushort()
                block = self.read_ushort()
                level, _ = self.read_id()
                assert level == 0x81
                work = {"wnum": self._id[level], "desc": {}}
                author["works"][work["wnum"]] = work
            # 3 * New section. This marks the next section within the work.
            # Followed by a 2-byte block number. The block number is
            # the 8K block in which the section begins.
            elif self.peek_ubyte() == 3:
                _ = self.read_ubyte()
                block = self.read_ushort()
            # 8 * Beginning ID for new section. This is the first entry
            # following the new subsection marker (type 3).
            elif self.peek_ubyte() == 8:
                _ = self.read_ubyte()
                ids = self.read_id()
            # 9 * Ending ID for new section. This is the last ID entry
            # for the subsection (unless followed by an exception).
            elif self.peek_ubyte() == 9:
                _ = self.read_ubyte()
                ids = self.read_id()
            # 10 * Last valid ID for the current block. One of these occurs
            # for each block.
            elif self.peek_ubyte() == 10:
                _ = self.read_ubyte()
                ids = self.read_id()
            # 11 * Start exception. This introduces an out-of-sequence ID
            # (i.e. one which does not belong in the current block).
            # The 2-byte block number precedes the ID.
            elif self.peek_ubyte() == 11:
                _ = self.read_ubyte()
                block = self.read_ushort()
                ids = self.read_id()
            # 12 * End exception. This gives the end range for the ID
            # exception whose starting range and block number is
            # given by type 11.
            elif self.peek_ubyte() == 12:
                _ = self.read_ubyte()
                ids = self.read_id()
            # 13 * Single exception: A single out-of-sequence id.
            elif self.peek_ubyte() == 13:
                _ = self.read_ubyte()
                block = self.read_ushort()
                ids = self.read_id()
            # 14 * Undefined.
            elif self.peek_ubyte() == 14:
                assert False
            # 16 * Description of ID fields a..b. Followed by a 1-byte
            # identifier (a..b=O..l) and a 1-byte length. The length
            # pertains to the description only and does not include
            # the type type, type identifier, or length byte. The
            # description is usually the author or work name. Given at
            # the author or work level, as appropriate. These fields
            # typically indicate the full name of the author and of
            # the works by that author; they should not be confused
            # with the abbreviated forms in-the d and c fields in the
            # actual citations in the texts.
            elif self.peek_ubyte() == 16:
                _ = self.read_ubyte()
                identifier = self.read_ubyte()
                length = self.read_ubyte()
                if identifier == 0x00:
                    author["anam"] = self.read_nstring(length)
                elif identifier == 0x01:
                    work["wnam"] = self.read_nstring(length)
            # 17 Description of ID fields n,v..z. Followed by a 1-byte field
            # identifier. For documents, the n-level identifier = 0,
            # and no other levels are described. For v..z levels, the
            # identifier is 4..0. The identifier is followed by a 1-
            # byte length. The length pertains to the description only and
            # does not include the type type, type identifier, or
            # length byte. Given at the work level. These indicate,
            # e.g., that the y level refers to a book of the Aeneid,
            # and the z level to a line within that book.
            elif self.peek_ubyte() == 17:
                _ = self.read_ubyte()
                level = self.read_ubyte()
                assert 0 <= level <= 4
                length = self.read_ubyte()
                desc = self.read_nstring(length)
                work["desc"][level] = desc
            # 18-30 * Undefined
            elif 18 <= self.peek_ubyte() <= 30:
                assert False
            # 31 * Introduces header of combined ID table. Followed by 3
            # length bytes, which give the total length in bytes of
            # the combined table. The count includes both the type
            # code byte and the length bytes.
            elif self.peek_ubyte() == 31:
                assert False
            else:
                assert False

        assert len(self._content) == 1
        self._content = self._content[0]

def content(path):
    """ Return the content of an IDT file. """
    return Idt(path).content()

if __name__ == "__main__":
    import sys
    import pprint
    pprint.pprint(content(sys.argv[1]))
