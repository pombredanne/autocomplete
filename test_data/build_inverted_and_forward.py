import sys
import numpy as np

input_filename = sys.argv[1]

tokens = {}
print("building dictionary...")
id = 1 # reserve id 0 to mark the end of a string
with open(input_filename + ".dict") as f:
    for line in f:
        t = line.rstrip('\n')
        tokens[t] = id
        id += 1

lines = 0
inverted = open(input_filename + ".inverted", 'w')
forward = open(input_filename + ".forward", 'w')

num_terms = 0
num_docs = 0
with open(input_filename + ".mapped.stats") as f:
    num_terms = int(f.readline())
    print num_terms
    num_docs = int(f.readline())
    print num_docs

inverted_index = [[] for i in range(num_terms + 1)] # id 0 is not assigned
forward_index = [[] for i in range(num_docs)]

with open(input_filename, 'r') as f:
    for line in f:
        x = line.rstrip('\n').split()
        mapped = []
        doc_id = int(x[0])
        for i in range(1, len(x)):
            term = x[i].encode('utf-8')
            try:
                term_id = tokens[term]
                mapped.append(term_id)
                inverted_index[term_id].append(doc_id)
            except KeyError:
                print("'" + term + "' not found in dictionary")
                print(line)
                exit()

        forward_index[doc_id] = mapped;

        lines += 1
        if lines % 1000000 == 0:
            print("processed " + str(lines) + " lines")

for i in range(0, num_docs):
    s = [str(k) for k in forward_index[i]]
    forward.write(str(len(forward_index[i])) + " ")
    forward.write(" ".join(s) + "\n")
forward.close()

for i in range(1, num_terms + 1):
    posting_list = inverted_index[i]
    unique = sorted(set(posting_list));
    s = [str(i) for i in unique] # remove any possible duplicate
    inverted.write(str(len(unique)) + " ")
    inverted.write(" ".join(s) + "\n")
inverted.close()