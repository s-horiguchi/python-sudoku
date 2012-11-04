#!/usr/bin/env python
#-*- coding:utf-8 -*-

from __future__ import with_statement #for version <= 2.5
import os.path
import pickle
import copy
import datetime
import curses, locale


class Sudoku(object):
    def __init__(self, datafile, verbose=False):
        self.datafile = datafile
        self.verbose = verbose
        locale.setlocale(locale.LC_ALL,'')
        curses.wrapper(self.main)
        
    def log(self, message):
        if message == None:
            self.log_win.addstr("\n " + "-" * 30 + "\n")
        else:
            self.log_win.addstr(" [*] %s\n" % message)
        self.log_win.box()
        self.log_win.refresh()
        return

    def update_map(self, values):
        #print "\n".join(["  ".join([str(v) for v in va]) for va in values]) + "\n"
        """
        output like this:
        =========================================
        || 0 | 0 | 0 || 0 | 0 | 0 || 0 | 0 | 0 ||
        -----------------------------------------
        || 0 | 0 | 0 || 0 | 0 | 0 || 0 | 0 | 0 ||
        -----------------------------------------
        || 0 | 0 | 0 || 0 | 0 | 0 || 0 | 0 | 0 ||
        =========================================
        || 0 | 0 | 0 || 0 | 0 | 0 || 0 | 0 | 0 ||
        -----------------------------------------
        || 0 | 0 | 0 || 0 | 0 | 0 || 0 | 0 | 0 ||
        -----------------------------------------
        || 0 | 0 | 0 || 0 | 0 | 0 || 0 | 0 | 0 ||
        =========================================
        || 0 | 0 | 0 || 0 | 0 | 0 || 0 | 0 | 0 ||
        -----------------------------------------
        || 0 | 0 | 0 || 0 | 0 | 0 || 0 | 0 | 0 ||
        -----------------------------------------
        || 0 | 0 | 0 || 0 | 0 | 0 || 0 | 0 | 0 ||
        =========================================
        """
        output = "\n  %d | %d | %d || %d | %d | %d || %d | %d | %d \n" % tuple(values[0])
        output += " -----------||-----------||-----------\n"
        output += "  %d | %d | %d || %d | %d | %d || %d | %d | %d \n" % tuple(values[1])
        output += " -----------||-----------||-----------\n"
        output += "  %d | %d | %d || %d | %d | %d || %d | %d | %d \n" % tuple(values[2])
        output += " ===========  ===========  ===========\n"
        output += "  %d | %d | %d || %d | %d | %d || %d | %d | %d \n" % tuple(values[3])
        output += " -----------||-----------||-----------\n"
        output += "  %d | %d | %d || %d | %d | %d || %d | %d | %d \n" % tuple(values[4])
        output += " -----------||-----------||-----------\n"
        output += "  %d | %d | %d || %d | %d | %d || %d | %d | %d \n" % tuple(values[5])
        output += " ===========  ===========  ===========\n"
        output += "  %d | %d | %d || %d | %d | %d || %d | %d | %d \n" % tuple(values[6])
        output += " -----------||-----------||-----------\n"
        output += "  %d | %d | %d || %d | %d | %d || %d | %d | %d \n" % tuple(values[7])
        output += " -----------||-----------||-----------\n"
        output += "  %d | %d | %d || %d | %d | %d || %d | %d | %d \n" % tuple(values[8])
        
        self.map_win.addstr(0, 0, output)
        self.map_win.box()
        
        self.map_win.refresh()
        return

    def change_data(self, values, square, x, y, change_at, change_to):
        values[change_at[0]][change_at[1]] = change_to
        if self.verbose:
            self.log("%s -> %d" % (str(change_at), change_to))
        #print "\n".join(["  ".join([str(v) for v in va]) for va in values]) + "\n"
        square[(change_at[0]/3)*3+(change_at[1]/3)][0] += change_to
        square[(change_at[0]/3)*3+(change_at[1]/3)][1].remove(change_to)
        x[change_at[0]][0] += change_to
        x[change_at[0]][1].remove(change_to)
        y[change_at[1]][0] += change_to
        y[change_at[1]][1].remove(change_to)
        return values, square, x, y

    def get_cand(self, blank, square, x, y):
        cand = []
        for n1, n2 in blank:
            cand.append([])
            for sq in square[(n1/3)*3+(n2/3)][1]:
                if (sq in y[n2][1]) == True:
                    if (sq in x[n1][1]) == True:
                        cand[-1].append(sq)
                    else:
                        pass
                else:
                    pass
        return cand
    
    def solve_sudoku(self, values):
        # current data showing
        self.log(None)
        self.update_map(values)
        
        self.log("plotting given data...")
        prev_pkl = ""
        #set n
        n = len(values)
        #initial sum check
        blank = []
        prev_blank = [[],[]]
        square = [[0, range(1, n+1)] for i in range(n)]
        y = [[0, range(1, n+1)] for i in range(n)]
        x = [[0, range(1, n+1)] for i in range(n)]
        for n1 in range(n):
            for n2 in range(n):
                if values[n1][n2] > 0:
                    try:
                        values, square, x ,y = self.change_data(values, square, x, y, change_at=(n1, n2), change_to=values[n1][n2])
                    except ValueError:
                        self.log("ValueError!!!!")
                        raise
                else:
                    blank.append((n1, n2))
        self.log("finish plotting.")
        self.log("starting calclating...")
        
        while 1:
            cand = self.get_cand(blank, square, x, y)
            
            # loop check
            cur_pkl = pickle.dumps(values)
            if cur_pkl == prev_pkl:
                # looping (= no more automatical dicidable value)
                for b in zip(blank, cand):
                    for c in b[1]:
                        datas_org = copy.deepcopy((values, square, x, y))
                        self.log("supposing (%d, %d) is %d" % (b[0][0], b[0][1], c))
                        values, square, x ,y = self.change_data(values, square, x, y, change_at=(b[0][0], b[0][1]), change_to=c)
                        if self.solve_sudoku(values):
                            return True
                        values, square, x, y = datas_org
                        self.log("ended supposing (%d, %d) is %d" % (b[0][0], b[0][1], c))
                        # current data showing
                        self.log(None)
                        self.update_map(values)
                        if self.verbose:
                            self.log("blank : " + str(blank))
                            self.log("cand : " + str(cand))
                        
                return False
            else:
                pass
            prev_pkl = cur_pkl
            
            # current data showing
            self.update_map(values)
            if self.verbose:
                self.log("blank : " + str(blank))
                self.log("cand : " + str(cand))
            
            if [] in cand:
                self.log("This root is wrong.")
                return False
    
            for b in zip(blank, cand):
                #print b[0], b[1]
                if len(b[1]) == 1:
                    self.log("decided automatically that (%d, %d) is %d" % (b[0][0], b[0][1], b[1][0]))
                    blank.remove(b[0])
                    values, square, x ,y = self.change_data(values, square, x, y, change_at=(b[0][0], b[0][1]), change_to=b[1][0])
                    break
                else:
                    pass
            if len(blank) == 0:
                # finish!!
                self.update_map(values)
                return True
            
        
    def main(self, scr):
        self.map_win = scr.subwin(19, 39, 2, 3)
        self.map_win.box()
        self.log_win = scr.subwin(0, 46)
        self.log_win.box()
        self.log_win.scrollok(True)

        self.log("datafile = %s" % self.datafile)
        if not os.path.isfile(self.datafile):
            self.log("Error!: File not found.\n")
            return
        with open(self.datafile, "r") as fd:
            raw_data = fd.read()
            table = [[int(d.strip()) for d in data.split(" ") if d.strip()] for data in raw_data.split("\n") if data.strip()]
            start_time = datetime.datetime.now()
            if not self.solve_sudoku(table):
                delta = datetime.datetime.now() - start_time
                self.log("Running time: %ddays %dh:%dm:%d.%ds" % (delta.days, delta.seconds / 3600, (delta.seconds % 3600) / 60, (delta.seconds % 3600) % 60, delta.microseconds))
                
                self.log("Error!")
                self.log("Couldn't solve.....")
            else:
                delta = datetime.datetime.now() - start_time
                self.log("Running time: %ddays %dh:%dm:%d.%ds" % (delta.days, delta.seconds / 3600, (delta.seconds % 3600) / 60, (delta.seconds % 3600) % 60, delta.microseconds))
                
                self.log("Completed!!")
        self.log(None)
        self.log("Press any key to exit.>")
        scr.getch()
        return
    
        
if __name__ == "__main__":
    from optparse import OptionParser

    parser = OptionParser("Usage: ./%prog [options] DATAFILE")
    parser.add_option("-v", "--verbose", dest="verbose",
                      action="store_true", default=False,
                      help="enable verbose output(default:off)")
    (options, args) = parser.parse_args()

    if len(args) == 1:
        s = Sudoku(args[0], verbose=options.verbose)
    else:
        parser.print_help()
        
