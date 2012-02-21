#!/usr/bin/python

# bash like command-line support
#import cmd2 as cmd 
import cmd
# ANSI color support
#from colorama import init, Fore, Back, Style

import sys, os
import pprint
import re, string
import subprocess, shlex

#WHINY_PATH = os.path.join(os.path.expanduser("~"), ".whiny")
WHINY_PATH = os.path.expanduser("~/docs")
if os.environ.has_key('WHINY_PATH'):
    WHINY_PATH = os.environ['WHINY_PATH']
TODO_PATH = os.path.join(WHINY_PATH, "TODO.txt")
PROJ_PATH = os.path.join(WHINY_PATH, "PROJECTS.md")
DONE_PATH = os.path.join(WHINY_PATH, "DONE.txt")

class TodoTxt():
    self.tasks = {}

    def write_tasks(self):
        pass

    def read_tasks(self, file):
        count = 0
        tasks = {}

        try:
            for line in open(file).readlines():
                if(line.strip() == ""):
                    continue
                count = count + 1
                tasks[count] = self.parse_line(line.rstrip())
            return tasks
        except(IOError, os.error):
            return {}

    def parse_line(self, line):
        words = line.split()
        projects = []
        contexts = []
        waiting = False
        rest = ""
        created_on = ""

        for word in words:
            match = re.search('\d\d\d\d-\d\d-\d\d', word)

            if word.startswith("@"):
                contexts.append(word)
            elif word.startswith("+"):
                projects.append(word)
            elif word == "WAIT":
                waiting = True
            elif match:
                created_on = match.group(0)
            elif word.startswith("DUE:"):
                #TODO: implement me
                pass
            else:
                rest = rest + word + " "

        return [rest, contexts, projects, created_on, waiting]

class Table():
    def __init__(self):
        pass

    def create_table(self, data):
        width = len(data[0]) * [0]

        #calc max width of each column
        for row in data:
            for idx, col in enumerate(row):
                if len(str(col)) > width[idx]:
                    width[idx] = len(str(col))
                    #spaces[idx] = (width[idx] - len(str(col)))
                    #print("width[%s] = %s spaces[%s] = %s" % (idx, width[idx], idx, spaces[idx]))

        max_width = 0
        # calc the max width of the whole table
        for idx, w in enumerate(width):
            max_width = max_width + w + 3
        max_width = max_width + 2

        print "-" * max_width

        for row_idx,row in enumerate(data):
            for idx, col in enumerate(row):
                if str(col) == 'None':
                    col = ''

                space = " " * (width[idx] - len(str(col)))
                sys.stdout.write("| %s%s " % (str(col), space))
            print " |"
            if row_idx == 0:
                print "-" *  max_width

        print "-" * max_width

class Whiny(cmd.Cmd):
    """ Whiny """

    #Constants

    prompt = "Whiny> "

    def change_prompt(self):
        self.prompt = ""
        if self.cur_project and self.cur_context:
            self.prompt = "%s/%s> " % (self.cur_project, self.cur_context)
        elif self.cur_project and not self.cur_context:
            self.prompt = "%s> " % (self.cur_project)
        elif not self.cur_project and self.cur_context:
            self.prompt = "%s> " % (self.cur_context)
        else:
            self.prompt = "Whiny> "


    def __init__(self, completekey=None, stdin=None, stdout=None):
        #start up the command handling
        cmd.Cmd.__init__(self)
        #start up the ANSI color support 
        #init()
        if not os.path.exists(WHINY_PATH):
            os.mkdir(WHINY_PATH)

        self.cur_context = None
        self.cur_project = None

        self.parser = TodoTxt()
        self.tasks = self.parser.read_tasks(TODO_PATH)

    def do_cd(self, dir):
        if dir.startswith('@'):
            pass
        elif dir.startswith('+'):
            pass
        elif dir.startswith(".."):
            pass

    def do_add(self, line):
        task = self.parser.parse_line(line)
        pprint.pprint(task)
        pass

    def do_rm(self, line):
        # TODO:
        pass

    def do_ls(self, line):
        #TODO: list tasks in current project/context
        #TODO: add searching
        pprint.pprint(self.tasks)

    def do_do(self, line):
        pass

    def do_done(self, line):
        pass

    def do_exit(self, line):
        return True

    def do_quit(self, line):
        return True

    def do_EOF(self, line):
        return True

    def postloop(self):
        print
        print "Goodbye."

def main():
    Whiny().cmdloop()

if __name__ == '__main__':
    main()


