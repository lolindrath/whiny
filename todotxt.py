import os, re
from sets import Set
import pprint

class TodoTxt():
    task_count = -1
    tasks = {}
    dirty = False

    def get_tasks_table(self):
        table_tasks = []
        titles = ['created_on', 'task', 'waiting', 'contexts', 'projects']
        tasks = [v for k,v in self.tasks.iteritems()]

        for task in tasks:
            t = []
            for title in titles:
                value = task[title]
                if isinstance(value, list):
                    value = " ".join(value)
                t.append(value)
            table_tasks.append(t)

        table_tasks = sorted(table_tasks, key=lambda task: task[3])
        table_tasks.insert(0, titles)
        return table_tasks

    def get_tasks(self):
        return self.tasks

    def get_contexts(self):
        contexts = []
        for k,v in self.tasks.iteritems():
            contexts.extend(v['contexts'])

        return Set(contexts)

    def get_projects(self):
        projects = []
        for k,v in self.tasks.iteritems():
            projects.extend(v['projects'])

        return Set(projects)

    def add(self, line):
        task = self.parse_line(line)
        self.task_count = self.task_count + 1
        self.tasks[self.task_count] = task
        return task

    def remove(self, num):
        del self.tasks[num]

    def write_tasks(self, file):
        with open(file, "w") as f:
            for num,task in self.tasks.iteritems():
                t = ""
                if task['waiting']:
                    t += "WAIT"
                t += task['created_on'] + " " + task['task'] + " ".join(task['contexts']) + " " + " ".join(task['projects']) + "\n"
                f.write(t)

    def read_tasks(self, file):
        count = 0
        tasks = {}

        try:
            with open(file) as f:
                for line in f.readlines():
                    if(line.strip() == ""):
                        continue
                    count = count + 1
                    tasks[count] = self.parse_line(line.rstrip())
                self.tasks = tasks
                self.task_count = count
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

        return { 'task': rest, 'contexts': contexts, 'projects': projects, 'created_on': created_on, 'waiting': waiting}




