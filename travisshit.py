import os

directory = "windows"

destination_directory = "RAx Files2"

if not os.path.exists(destination_directory):
    os.makedirs(destination_directory)

# Initialize a count to 0 to be used for file naming
count = 0

# Iterate over each folder in the given directory
for filename in os.listdir(directory):

    count += 1

    # If file is a phylip file run RAxML on it
    if filename.endswith(".phylip"):

        # print filename
        input_file = os.path.join(directory, filename)
        output_file = os.path.join(destination_directory, "raxmlOutputTest"+str(count)+".out")

        os.system("raxmlHPC -f a -x12345 -p 12345 -# 3 -m GTRGAMMA -s {0} -n {1}".format(input_file, output_file))
        dir_path = os.path.dirname(os.path.realpath(output_file))