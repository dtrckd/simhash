#!/usr/bin/env python3

from simhash import Simhash


if __name__ == '__main__':

    text1 = 'Hi, how are you ?'
    text2 = 'Hi, how are you darling ??'

    lsh1 = Simhash(text1, bits=32)
    lsh2 = Simhash(text2, bits=32)

    sim = lsh1.distsim(lsh2)

    print("Similarity (in [0,1]) between text1 and text2 : %s" % (sim))
