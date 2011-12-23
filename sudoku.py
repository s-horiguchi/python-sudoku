#!/usr/bin/env python
#-*- coding:utf-8 -*-

from __future__ import with_statement #for version <= 2.5
import sys
import os.path
import pickle

def solve_sudoku(values):
    prev_pkl = ""
    #set n
    n = len(values)
    #initial sum check
    blank = []
    prev_blank = [[],[]]
    square = [[0, range(1, n+1)] for i in range(n)]
    y = [[0, range(1, n+1)] for i in range(n)]
    x = [[0, range(1, n+1)] for i in range(n)]
    #slant = [[0, range(n)] for i in range(n)]
    for n1 in range(n):
        for n2 in range(n):
            if values[n1][n2] > 0:
                square[(n1/3)*3+(n2/3)][0] += values[n1][n2]
                square[(n1/3)*3+(n2/3)][1].remove(values[n1][n2])
                y[n2][0] += values[n1][n2]
                y[n2][1].remove(values[n1][n2])
                x[n1][0] += values[n1][n2]
                x[n1][1].remove(values[n1][n2])
                #if n1 == n2:
                #    slant[0][0] += values[n1][n2]
                #    slant[0][1].remove(values[n1][n2])
                #elif (n1+n2) == (n-1):
                #    slant[1][0] += values[n1][n2]
                #    slant[1][1].remove(values[n1][n2])
            else:
                blank.append((n1, n2))
    while 1:
        # current data showing
        for value in values:
            print value
        print "blank :", blank
        #print "square=", square
        #print "y=", y
        #print "x=", x
        #print "slant=", slant

        # loop check
        cur_pkl = pickle.dumps(values)
        if cur_pkl == prev_pkl:
            print "Error!"
            print u"解けませんでした。"
            return False
        prev_pkl = cur_pkl
        
        cand = []
        for n1, n2 in blank:
            cand.append([])
            for sq in square[(n1/3)*3+(n2/3)][1]:
                if (sq in y[n2][1]) == True:
                    if (sq in x[n1][1]) == True:
                        cand[-1].append(sq)
                    else:
                        pass
                        #print "miss", sq, "on", (n1, n2), "(x)"
                else:
                    pass
                    #print "miss", sq, "on", (n1, n2), "(y)"

        for b in zip(blank, cand):
            #print b[0], b[1]
            if len(b[1]) == 1:
                blank.remove(b[0])
                values[b[0][0]][b[0][1]] = b[1][0]
                square[(b[0][0]/3)*3+(b[0][1]/3)][0] += b[1][0]
                square[(b[0][0]/3)*3+(b[0][1]/3)][1].remove(b[1][0])
                y[b[0][1]][0] += b[1][0]
                y[b[0][1]][1].remove(b[1][0])
                x[b[0][0]][0] += b[1][0]
                x[b[0][0]][1].remove(b[1][0])
            elif len(b[1]) == 0:
                print "Error!"
                print u"入力が間違っていませんか？"
                return False
            else:
                pass
        if len(blank) == 0:
            print "Complete!!"
            for value in values:
                print value
            return True
        
        
def main():
    if len(sys.argv) == 1:
        filename = "sudoku.txt"
    else:
        filename = sys.argv[1]
    if not os.path.isfile(filename):
        print "Error!: File not found.\n"
        return
    with open(filename, "r") as fd:
        raw_data = fd.read()
        table = [[int(d.strip()) for d in data.split(" ") if d.strip()] for data in raw_data.split("\n") if data.strip()]
        solve_sudoku(table)
        return
        
        
        
if __name__ == "__main__":
    main()
