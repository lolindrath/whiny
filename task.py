import re
from datetime import date
import hashlib

class Task():
    task = ""
    created_on = ""
    due_on = ""
    completed_on = ""
    projects = []
    contexts = []
    waiting = False
    done = False

    def to_hash(self):
        m = hashlib.sha256()
        m.update(self.to_s())
        return m.hexdigest()[:3]

    def to_array(self, fields):
        arr = []
        for f in fields:
            if hasattr(self, f):
                field = getattr(self, f)
                if isinstance(field, list):
                    arr.append(" ".join(field))
                else:
                    arr.append(field)

        return arr

    def to_s(self):
        t = ""
        if self.done:
            t += "DONE:" + self.completed_on

        if self.waiting:
            t += "WAIT "

        t += self.created_on + " " + self.task + " ".join(self.contexts) + " " + " ".join(self.projects) + "\n"

        return t

    def mark_done(self):
        self.done = True
        self.completed_on = date.today().strftime("%Y-%m-%d")
        self.waiting = False

    @staticmethod
    def parse_line(line):
        projects = []
        contexts = []
        waiting = False
        rest = ""
        created_on = ""
        completed_on = ""
        due_on = ""
        done = False

        if line.startswith("x"):
            done = True
            completed_match = re.search('x (\d\d\d\d-\d\d-\d\d)', line)
            completed_on = completed_match.group(1)
            line = line[completed_match.end():]


        words = line.split()

        for word in words:
            created_match = re.search('\d\d\d\d-\d\d-\d\d', word)
            due_match = re.search('DUE:(\d\d\d\d-\d\d-\d\d)', word)

            if word.startswith("@"):
                contexts.append(word)
            elif word.startswith("+"):
                projects.append(word)
            elif word == "WAIT":
                waiting = True
            elif created_match:
                created_on = created_match.group(0)
            elif due_match:
                due_on = due_match.group(1)
                pass
            else:
                rest = rest + word + " "

        t = Task()
        t.done = done
        t.task = rest
        t.created_on = created_on
        t.completed_on = completed_on
        t.due_on = due_on
        t.waiting = waiting
        t.projects = projects
        t.contexts = contexts

        return t


