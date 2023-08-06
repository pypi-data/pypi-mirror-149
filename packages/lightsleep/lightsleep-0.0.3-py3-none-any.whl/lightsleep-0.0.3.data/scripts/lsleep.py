#!python

import argparse
import setproctitle

from lightsleep import Sleep

def get_args():

    hooks = Sleep.hooks()

    epilog = 'HOOKS\n=====\n\n'

    for name, args in hooks.items():
        epilog += f'--hook {name}\n'
        for arg, default in args.items():
            epilog += f'    {arg}={default}\n'
        epilog += '\n'

    parser = argparse.ArgumentParser(description='Sleep which can awake', epilog=epilog,  formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('seconds', type=int)
    parser.add_argument('--hook', nargs='+', metavar=('METHOD', 'ARG'), help='use this hook with arguments')
    parser.add_argument('--title', '-t', default=None, help='set title to use with pidof/killall')
    return parser.parse_args()

def main():
    args = get_args()
    if args.title:
        setproctitle.setproctitle(args.title)
        
    s = Sleep(hook=args.hook)
    s.sleep(args.seconds)

if __name__ == '__main__':
    main()