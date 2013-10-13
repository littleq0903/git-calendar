#!/usr/bin/env python
from pipes import quote
from utils import get_output_from_command
from utils import GitCalendar

def git_calendar(author=None, range=None, **options):
    '''
    It shows the commit statistics in a github calendar form
    '''
    if range:
        options['range'] = range
    shell_args = ['--period=daily', '--number=367']

    for k,v in options.items():
        if isinstance(v, bool) and v:
            shell_args.append('--%s' % k.replace('_', '-'))
        elif v:
            shell_args.append('--%s=%s' % (k.replace('_', '-'), quote(v)))

    output = get_output_from_command('git count %s' % ' '.join(shell_args))
    output = output.strip()

    results = []
    for day_result in output.split('\n'):
        day_result = day_result.strip().split('\t')
        result = (day_result[0], int(day_result[1]))
        results.append(result)

    git_log = dict(results)
    git_calendar = GitCalendar(git_log)
    
    print git_calendar.render_calendar()

def main():
    try:
        import clime
    except ImportError:
        clime = None

    if clime:
        clime.start({'calendar': git_calendar})
    else:
        raise Exception("I need clime.")

if __name__ == '__main__':
    main()
