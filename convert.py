from garnett.reader import*
from garnett.writer import*
import garnett
import gsd

xml_reader = HOOMDXMLFileReader()
gsd_reader = GSDHOOMDFileReader()

with open('2021-11-13 15:50:39.831410-2--pentagons--4442277.gsd', 'rb') as gsdfile:
    trajectory = gsd_reader.read(gsdfile)

writer = PosFileWriter()
with open('a_posfile.pos', 'w', encoding='utf-8') as posfile:
    writer.write(trajectory, posfile)