import os
import subprocess as sub

input_file = "raxmlinput.txt"
output_file = "raxmlOutputTest.out"

# os.system("raxmlHPC -f a -x12345 -p 12345 -# 100 -m GTRGAMMA -s {0} -n {1}".format(input_file, output_file))

# raxmlHPC -f a -x12345 -p 12345 -# 100 -m GTRGAMMA -s "raxmlinput.txt" -n "raxmlOutputTest.out"

# p = os.popen("raxmlHPC -f a -x12345 -p 12345 -# 20 -m GTRGAMMA -s {0} -n {1}".format(input_file, output_file))



for i in range(1,3,1):
    output_file = "raxmlOutputTest" + str(i) + ".out"
    p = sub.Popen("raxmlHPC -f a -x12345 -p 12345 -# "+str(i*10)+" -m GTRGAMMA -s {0} -n {1}".format(input_file, output_file))
    p.wait()


# for i in range(1,3,1):
    # os.wait()
    # output_file = "raxmlOutputTest2.out"

    # os.system("raxmlHPC -f a -x12345 -p 12345 -# 20 -m GTRGAMMA -s {0} -n {1}".format(input_file, output_file))
            # os.wait()
# os.system("raxmlHPC -f a -x12345 -p 12345 -# "+ str(i*10)+" -m GTRGAMMA -s {0} -n {1}".format(input_file, output_file))