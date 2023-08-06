import re
import subprocess
import sys
import os
from collections import OrderedDict
from pkg_resources import RequirementParseError
from pkg_resources.extern.packaging.requirements import InvalidRequirement

try:
    import requirements
except ImportError:
    print('Error: dependency "requirements_parser" is required: '
          'https://pypi.org/project/requirements-parser/')
    exit(1)


def inspect(wd):
    results = {}
    idx = 0
    for d in subdirs(wd):
        files = has_requirements_txt(os.path.join(wd, d))
        for sd in subdirs(d):
            files += has_requirements_txt(os.path.join(wd, d, sd))

        if files:
            idx += 1
            results[d] = {
                'index': idx,
                'files': files,
            }

    return results


def has_requirements_txt(path):
    path, _, files = next(os.walk(path))
    return [
        os.path.join(path, s) for s in files
        if (
            ('requirements' in s
             or path.endswith('/requirements'))
            and s.endswith('.txt')
        )]


def subdirs(d):
    return next(os.walk(d))[1]


def print_data(data, selection=None, lines=None):
    lines = lines or (lambda k, v: [k])

    selection = selection or set()
    for d, di in data.items():
        head, *tail = lines(d, di)
        print(f'{"* " if di["index"] in selection else "  "}{di["index"]}: {head}')
        for line in tail:
            print(f'    {line}')


def prompt_user_selection(data, text, lines=None, only_one=False):
    selection = set()

    while 1:
        print(f'\n{text}')
        print_data(data, selection, lines=lines)

        s = input('\nType a number or "q" to continue >')
        method = 'remove' if s.startswith('-') else 'add'

        try:
            s = int(s)
            if s in selection:
                selection.remove(s)
            elif s in [d['index'] for d in data.values()]:
                selection.add(s)
                if only_one:
                    break
        except Exception:
            if not only_one and s == 'a':
                [selection.add(d['index']) for d in data.values()]
                continue

            if s in ['exit', 'q']:
                break
            print('Bad input')

    return {k: v for k, v in data.items() if v['index'] in selection}


def get_summary(wd, data):
    summary = {}

    for app_name, results in data.items():
        for req_file in results['files']:
            with open(req_file, 'r') as f:
                try:
                    for req in requirements.parse(f):
                        if req.name:
                            summary.setdefault(req.name.lower(), {'raw': []})['raw'].append(
                                {
                                    'app_name': app_name,
                                    'req_file': req_file,
                                    'req': req,
                                }
                            )
                        else:
                            print(f'Failed to handle requirement {req}')
                except (RequirementParseError, InvalidRequirement) as e:
                    print(f'Failed to parse requirements ({req_file}): {e}')

    summary_items = summary.items()
    summary_items = sorted(summary_items, key=lambda d: len(d[1]['raw']), reverse=True)

    ret = OrderedDict()

    for req_name, value in summary_items:
        details = value['raw']
        if len(details) == 1 and '--min=2' in sys.argv:
            continue

        different_versions = set(tuple(d['req'].specs) for d in details)
        if len(different_versions) == 1 and '--min-different=2' in sys.argv:
            continue

        if all(not d['req'].specs for d in details) and '--ignore-no-version' in sys.argv:
            continue

        value['lines'] = [f'{req_name}, {len(different_versions)} different versions']
        for dets in details:
            specs = [''.join(specs) for specs in dets['req'].specs]
            specs = ', '.join(f'"{s}"' for s in specs)
            value['lines'].append(f'  * {dets["req_file"].split(wd)[1][1:]}: {specs}')

        ret[req_name] = value

    return ret


def get_latest_version(req_name):
    s = subprocess.run(
        [sys.executable, '-m', 'pip', 'index', 'versions', req_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL)
    output = s.stdout.decode('utf-8')
    try:
        line = output.split('\n')[0]
        return line[line.index('(') + 1:-1] or 'unknown'
    except Exception:
        print('fFailed to check latest version for {req_name} (output: {output}')
        return 'unknown'


def print_lines(header, data):
    print(f'\n--- {header} ---')
    for k, v in data.items():
        for line in v['lines']:
            print(line)


def console_command():
    wd = os.getcwd()
    data = inspect(wd)
    data = prompt_user_selection(data, text='Select repositories (or "a" for all)')
    summary = get_summary(wd, data)

    print_lines('Summary', summary)

    for i, key in enumerate(summary.keys()):
        summary[key]['index'] =  i + 1

    options = {
        'Compare to latest available versions': {'index': 1},
        'Quit': {'index': 2},
    }

    # "Main loop"
    while 1:
        selection = prompt_user_selection(options, text='Select what to do', only_one=True)
        if not selection:
            break

        sel = list(selection.values())[0]['index']
        if sel == 1:
            selected = prompt_user_selection(
                summary, text='Select package for introspection',
                lines=lambda k, v: v['lines'])
            for req_name in selected.keys():
                selected[req_name]['latest_version'] = get_latest_version(req_name)
                selected[req_name]['lines'][0] += f' (current version: {selected[req_name]["latest_version"]})'

            print_lines('Summary', selected)

        elif sel == 2:
            break


if __name__ == '__main__':
    console_command()
