import sys

class Table():
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
