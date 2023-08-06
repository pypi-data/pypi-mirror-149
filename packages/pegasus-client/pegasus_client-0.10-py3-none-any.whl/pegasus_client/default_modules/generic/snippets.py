
'''csv'''
import csv

with open('example.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            print(
                f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
            line_count += 1
    print(f'Processed {line_count} lines.')
'''csv'''

'''pandas'''
for i in loop:
    print(i)
'''pandas'''

'''class'''


class ClassName:

    def __init__(self):
        pass

    def function_here(self):
        pass


'''class'''


'''arg'''
print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)
'''arg'''
