import math
import random


def read_phylip(filename):
    """
    Read a file in Phylip format and return the length of the
    sequences and the taxa and sequences.

    Arguments:
    filename -- name of file in Phylip format

    Returns:
    A tuple where the first element is the length of the sequences and
    the second argument is a dictionary mapping taxa to sequences.
    """
    # Initialize return values in case file is bogus
    m = 0
    tsmap = {}

    with open(filename) as f:
        # First line contains n and m separated by a space
        nm = f.readline()
        nm = nm.split()
        n = int(nm[0])
        m = int(nm[1])

        # Subsequent lines contain taxon and sequence separated by a space
        for i in range(n):
            l = f.readline()
            l = l.split()
            tsmap[l[0]] = l[1]

    # Return sequence length and mapping of taxa to sequences
    return m, tsmap

def splittr(filename, window_size, step_size, destination_directory):
    """
        node 
    """

    output_files = []

    with open(filename) as f:
        # First line contains n and m separated by a space
        number_of_sequences = int(f.readline())
        length_of_sequences = int(f.readline())
        print 'number_of_sequences:', number_of_sequences
        print 'length_of_sequences:', length_of_sequences

        i = 0
        BENEDICTRs_CONST = 0

        while(i + window_size - 1 < length_of_sequences):
            i += step_size
            BENEDICTRs_CONST += 1

        print "BENEDICTRs CONSTANT", BENEDICTRs_CONST

        for i in range(BENEDICTRs_CONST):
            output_files.append(open("window" + str(i + 1) + ".phylip", "w"))

        for i in range(BENEDICTRs_CONST):
            output_files[i].write(str(number_of_sequences) + "\n")
            output_files[i].write(str(BENEDICTRs_CONST) + "\n")

        l = 0

        # Subsequent lines contain taxon and sequence separated by a space
        for i in range(number_of_sequences):
            line = f.readline()
            line = line.split()

            taxon = line[0]
            sequence = line[1]

            for j in range(BENEDICTRs_CONST):
                l = j * step_size
                output_files[j].write(taxon + " ")
                window = ""
                for k in range(window_size):
                    window += sequence[l+k]
                print window
                output_files[j].write(window + "\n")

        for i in range(len(output_files)):
            output_files[i].close()

    # Return sequence length and mapping of taxa to sequences
    return None

splittr("phylip.txt", 1000, 2000, "none")
