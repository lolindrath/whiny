#!/usr/bin/python

# bash like command-line support
#import cmd2 as cmd 
import cmd
# ANSI color support
#from colorama import init, Fore, Back, Style

import sys, os
import pprint

#Whiny modules
from todotxt import TodoTxt
from table import Table

#WHINY_PATH = os.path.join(os.path.expanduser("~"), ".whiny")
WHINY_PATH = os.path.expanduser("~/docs")
if os.environ.has_key('WHINY_PATH'):
    WHINY_PATH = os.environ['WHINY_PATH']
TODO_PATH = os.path.join(WHINY_PATH, "TODO.txt")
PROJ_PATH = os.path.join(WHINY_PATH, "PROJECTS.md")
DONE_PATH = os.path.join(WHINY_PATH, "DONE.txt")


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

        self.todotxt = TodoTxt()
        self.todotxt.read_tasks(TODO_PATH)

        pprint.pprint(self.todotxt.get_contexts())
        pprint.pprint(self.todotxt.get_projects())

    def do_cd(self, dir):
        if dir.startswith('@'):
            pass
        elif dir.startswith('+'):
            pass
        elif dir.startswith(".."):
            pass

    def do_add(self, line):
        task = self.todotxt.add(line)
        pprint.pprint(task)
        pass

    def do_rm(self, line):
        # TODO:
        pass

    def do_ls(self, line):
        #TODO: list tasks in current project/context
        #TODO: add searching
        #pprint.pprint(self.todotxt.get_tasks())
        table = Table()
        table.create_table(self.todotxt.get_tasks_table())

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


