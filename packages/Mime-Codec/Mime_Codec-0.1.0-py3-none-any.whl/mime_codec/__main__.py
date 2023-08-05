import sys
from .mime_codec import *

if __name__ == '__main__':
    print(get_mime_codec(sys.argv[1]))
