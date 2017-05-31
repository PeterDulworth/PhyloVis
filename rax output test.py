import subprocess

count = 1

# a = subprocess.Popen("find //cygdrive//c//Users//travi//Documents//Evolutionary-Diversity-Visualization-Python//RAx Files \( -type d -exec chmod u+rwx,g+rwx,o+rx {} \; -o -type f -exec chmod u+rw,g+rw,o+r {} \; \)")
# a.wait()
p = subprocess.Popen("raxmlHPC - f a - x12345 - p 12345 -  # 100 -m GTRGAMMA -s raxmlinput.txt -n out") #-w //cygdrive//c//Users//travi//Documents//Evolutionary-Diversity-Visualization-Python//RAx Files")
p.wait()
# -w $PWD/results_all