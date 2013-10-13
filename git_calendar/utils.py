#!/usr/bin/env python
"""
here i wanna implement several helper functions for displaying calendar on user's terminal screen.
"""
from datetime import date
from datetime import timedelta

import shlex
import subprocess

class CommandStderrException(Exception):
    pass

def get_output_from_command(command):
    parsed_command = shlex.split(command)
    process = subprocess.Popen(parsed_command, stdout=subprocess.PIPE)
    out, err = process.communicate()
    if err:
        raise CommandStderrException(err)
    return out

def transpose_matrix(matrix):
    height = len(matrix)
    width  = len(matrix[0])
    lens = sum([ len(x) for x in matrix ])
    if lens != height * width:
        print '%(height)s x %(width)s = %(lens)s' % locals()
        raise Exception("argument 'matrix' must be in a shape of square.")
    return [[matrix[h][w] for h in range(height)] for w in range(width)]
    

class GitCalendar(object):
    def __init__(self, commit_number_log):
        """
        commit_number_log should be in form of:
        {
            '2012-01-02': 0,
            '2012-01-03': 1,
            '2012-01-05': 2
        }
        """

        # generate the symbol_map for more customization
        self.symbol_map = {
            'unknown': '-',
            'more': '+',
            'empty': '0',
        }
        one_to_ten = [str(x) for x in range(0, 10)]
        number_dict = zip(one_to_ten, one_to_ten)
        self.symbol_map.update(number_dict)
        self.commit_log = commit_number_log

    def gen_matrix(self, end_date, length=366):
        """
        generate the right shape matrix
        """
        one_day_delta = timedelta(days=1)
        end_date = date.today() - one_day_delta
        date_list = []
        for i in xrange(365):
            date_list.insert(0, end_date)
            end_date = end_date - one_day_delta

        # calculation
        def to_sunday_first_index(monday_first_index):
            return (monday_first_index + 1) % 7
        first_day = to_sunday_first_index(date_list[0].weekday())
        last_day = to_sunday_first_index(date_list[-1].weekday())

        # explain: filled with '-' to head and tail to became the multiple of 7
        unknown_substitute = 'unknown'
        for i in range(first_day): date_list.insert(0, unknown_substitute)
        for i in range(6-last_day): date_list.append(unknown_substitute)

        # form a 53 (height) x 7 (width) matrix 
        matrix = transpose_matrix([date_list[cursor:cursor+7] for cursor in range(len(date_list))[::7]])
        return matrix

    def gen_rendered_matrix(self, end_date):
        """
        Get a single string as the rendered calendar
        this one should use self.gen_matrix to get the result matrix
        """
        matrix = self.gen_matrix(end_date=end_date)
        def to2(d):
            d = str(d)
            return d if len(d) == 2 else '0'+d
        def stringify(day):
            return "%s-%s-%s" % (day.year, to2(day.month), to2(day.day)) if isinstance(day, date) else day

        def bind(m):
            return self.get_commits_by_date(stringify(m))

        string_list = (map(bind , row) for row in matrix)

        return string_list

    def get_commits_by_date(self, d):
        if str(d) in self.symbol_map:
            return self.symbol_map[d]
        else:
            try:
                rtn = self.commit_log[str(d)]
            except KeyError:
                rtn = 'empty'
            else:
                if rtn > 9: rtn = 'more'
            return self.symbol_map[str(rtn)]

    def new_symbol_map(self, new_map):
        self.symbol_map.update(new_map)

    def render_calendar(self, end_date = date.today()):
        matrix_to_print = self.gen_rendered_matrix(end_date=end_date)
        return '\n'.join([''.join(row) for row in matrix_to_print])

