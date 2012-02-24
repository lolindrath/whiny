#!/usr/bin/python

# bash like command-line support
import cmd2 as cmd 
#import cmd

# ANSI color support
from colorama import init, Fore, Back, Style

import sys, os
import pprint

#Whiny modules
from todotxt import TodoTxt
from table import Table

#WHINY_PATH = os.path.join(os.path.expanduser("~"), ".whiny")
#WHINY_PATH = os.path.expanduser("~/docs")
WHINY_PATH = os.path.expanduser("~/proj/whiny")
if os.environ.has_key('WHINY_PATH'):
    WHINY_PATH = os.environ['WHINY_PATH']
TODO_FILE = os.path.join(WHINY_PATH, "TODO.txt")
PROJ_FILE = os.path.join(WHINY_PATH, "PROJECTS.md")
DONE_FILE = os.path.join(WHINY_PATH, "DONE.txt")


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
        init()
        if not os.path.exists(WHINY_PATH):
            os.mkdir(WHINY_PATH)

        self.cur_context = None
        self.cur_project = None

        print "Reading tasks from: ", TODO_FILE
        self.todotxt = TodoTxt()
        self.todotxt.read_tasks(TODO_FILE, DONE_FILE)

        pprint.pprint(self.todotxt.get_contexts())
        pprint.pprint(self.todotxt.get_projects())

    def confirm(self, prompt_str="Confirm", allow_empty=False, default=False):
      fmt = (prompt_str, 'y', 'n') if default else (prompt_str, 'n', 'y')
      if allow_empty:
        prompt = '%s [%s]|%s: ' % fmt
      else:
        prompt = '%s %s|%s: ' % fmt
     
      while True:
        ans = raw_input(prompt).lower()
     
        if ans == '' and allow_empty:
          return default
        elif ans == 'y':
          return True
        elif ans == 'n':
          return False
        else:
          print 'Please enter y or n.'

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
        table = Table()
        table.create_table(self.todotxt.get_tasks_table({'done': False, 'waiting': False}))

    def do_waiting(self, line):
        #TODO: list tasks in current project/context
        #TODO: add searching
        table = Table()
        table.create_table(self.todotxt.get_tasks_table({'waiting': True, 'done': False}))

    def do_do(self, line):
        self.do_done(line)
        pass

    def do_done(self, line):
        #TODO: support multiple item #'s
        self.todotxt.mark_done(line)
        pass

    def do_due(self, line):
        #TODO: implement
        pass

    def do_append(self, line):
        #TODO: implement
        pass

    def do_save(self, line):
        print "Saving Tasks..."
        self.todotxt.save(TODO_FILE, DONE_FILE)

    def do_exit(self, line):
        return True

    def do_quit(self, line):
        return True

    def do_EOF(self, line):
        return True

    def postloop(self):
        if self.todotxt.dirty:
            if self.confirm("Do you want to save?", True, True):
                self.do_save("")
        print "Goodbye."

def main():
    Whiny().cmdloop()

if __name__ == '__main__':
    main()


