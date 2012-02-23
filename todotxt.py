import os
from sets import Set
# local imports
from task import Task

class TodoTxt():
    tasks = {}
    done = {}

    dirty = False

    def filter(self, fields):
        tasks = {}

        if fields == None or fields == {}:
            return self.tasks

        for k,task in self.tasks.iteritems():
            #gather all field match values
            values = []
            for f,v in fields.iteritems():
                values.append(getattr(task, f) == v)

            # do an AND of all the results
            if len(values) * [True] == values:
                tasks[k] = task

        return tasks

    def get_tasks_table(self, filter):
        table_tasks = []
        titles = ['hash', 'task', 'contexts', 'projects']

        tasks = self.filter(filter)

        for k,task in tasks.iteritems():
            hash = task.to_hash()
            task = task.to_array(titles)
            task.insert(0, hash)
            table_tasks.append(task)

        table_tasks = sorted(table_tasks, key=lambda task: task[3])
        table_tasks.insert(0, titles)
        return table_tasks

    def mark_done(self, hash):
        self.dirty = True
        self.tasks[hash].mark_done()
        self.done[hash] = self.tasks[hash]
        del self.tasks[hash]

    def get_tasks(self):
        return self.tasks

    def get_contexts(self):
        contexts = []
        for k,v in self.tasks.iteritems():
            contexts.extend(v.contexts)

        return Set(contexts)

    def get_projects(self):
        projects = []
        for k,v in self.tasks.iteritems():
            projects.extend(v.projects)

        return Set(projects)

    def add(self, line):
        self.dirty = True
        task = self.parse_line(line)
        self.tasks[task.to_hash()] = task
        return task

    def remove(self, hash):
        self.dirty = True
        del self.tasks[hash]

    def save(self, tasks_file, done_file):
        with open(tasks_file, "w") as f:
            for num,task in self.tasks.iteritems():
                f.write(task.to_s())

        with open(done_file, "w") as f:
            for num,task in self.done.iteritems():
                f.write(task.to_s())

        self.dirty = False

    def read_tasks(self, tasks_file, done_file):
        tasks = {}
        done = {}

        try:
            with open(tasks_file) as f:
                for line in f.readlines():
                    if(line.strip() == ""):
                        continue
                    task = Task.parse_line(line.rstrip())
                    tasks[task.to_hash()] = task
                self.tasks = tasks

            with open(done_file) as f:
                for line in f.readlines():
                    if(line.strip() == ""):
                        continue
                    task = Task.parse_line(line.rstrip())
                    task.done = True
                    done[task.to_hash()] = task
                self.done = done
        except(IOError, os.error):
            return {}




