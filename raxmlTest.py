import os

input_file = "raxmlinput.txt"
output_file = "raxmlOutputTest.out"

os.system("raxmlHPC -f a -x12345 -p 12345 -# 100 -m GTRGAMMA -s {0} -n {1}".format(input_file, output_file))
