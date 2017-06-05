def topologize(newick):
    print

import re

# phone = "2004-959-559 # This is Phone Number"
#
# # Delete Python-style comments
# num = re.sub(r'#.*$', "", phone)
# print "Phone Num : ", num
#
# # Remove anything other than digits
# num = re.sub(r"\d", "", phone)
# print "Phone Num : ", num


newick = "(seq4:34.53877639491068407551,(seq1:0.19030225670472911137,(seq2:0.22406303244340791681,seq3:0.39208792736040209981):0.00087295124196293521):34.53877639491068407551,seq0:34.53877639491068407551):0.0;"

# s = '<@ """@$ FSDF >something something <more noise>'
# s = re.sub('<[^>]+>', '', s)
# print s
# Regular expression for floats
float_pattern = "([+-]?\\d*\\.\\d+)(?![-+0-9\\.])"
s = re.sub(float_pattern, '', newick)
print s
s = s.replace(":","")
print s


