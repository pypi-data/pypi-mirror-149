import argparse
import pathlib

import os
from .mime_codec import *


def main():
    parser = argparse.ArgumentParser(description='Mime Codec info')
    parser.add_argument('path', type=pathlib.Path)
    parser.add_argument('-r', '--recursive', action=argparse.BooleanOptionalAction, help='recursive folder')

    args = parser.parse_args()
    if args.recursive:
        for dp, dn, filenames in os.walk(args.path):
            for f in filenames:
                p = os.path.join(dp, f)
                try:
                    print('{}: {}'.format(p, get_mime_codec(p)))
                except MimeTypeNotSupportedException:
                    pass
        return
    print(get_mime_codec(args.path))


if __name__ == '__main__':
    main()
