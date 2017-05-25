def phylip2phylip(input_file, output_file):
    """
    Convert weird phylip format to normal phylip format ya feel
    """

    with open(input_file) as f:
        f_out = open(output_file + ".phylip", "w")

        sequence_info = f.readline().split()
        number_of_sequences = sequence_info[0]
        length_of_sequences = sequence_info[1]


        f_out.write(number_of_sequences + "\n")
        f_out.write(length_of_sequences + "\n")
        # print number_of_sequences, length_of_sequences

        for i in range(int(number_of_sequences)):
            line = f.readline().split()
            name = line[0]
            sequence = ""
            for j in range(1, len(line)):
                sequence += line[j]
            # print name, sequence

            f_out.write(name + " " + sequence + "\n")



phylip2phylip("testconvert.phylip", "out")