from Bio import AlignIO
from PyQt4 import QtCore

"""
Functions:
    file_converter(input_file, input_type, output_type, output_file)
~
Chabrielle Allen
Travis Benedict
Peter Dulworth
"""

class FileConverter(QtCore.QThread):
    def __init__(self, parent=None):
        super(FileConverter, self).__init__(parent)

    def fileConverter(self, input_file, input_type, output_type, output_file):
        input_handle = open(input_file, "rU")
        output_handle = open(output_file, "w")

        alignments = AlignIO.parse(input_handle, input_type)
        AlignIO.write(alignments, output_handle, output_type)

        output_handle.close()
        input_handle.close()

# local tests
if __name__ == '__main__':
    # create new instance of class
    fcc = FileConverter()
    # test converter function
    fcc.fileConverter('../testFiles/phylip.txt', 'phylip-relaxed', 'fasta', '../henlo')
