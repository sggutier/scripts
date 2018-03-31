#!/usr/bin/env python3

# import hashlib
import requests
import os
import sys
import itertools


flat = itertools.chain.from_iterable


def get_filename(d):
    return ''.join([d['filename'], d['ext']])


def get_md5(d):
    return str(d['md5'])


def get_filepath(d):
    global mserv, board
    return '/'.join([mserv, board, 'src', (''.join([str(d['tim']),
                                                    str(d['ext'])]))])


# def md5(fname):
#     hash_md5 = hashlib.md5()
#     with open(fname, "rb") as f:
#         for chunk in iter(lambda: f.read(4096), b""):
#             hash_md5.update(chunk)
#     return hash_md5.hexdigest()


def isDownloaded(d):
    name = get_filename(d)
    if not os.path.exists(name):
        return False
    return True
#     return md5(name) == get_md5(d)


def set_board(lnk):
    global chan, mserv, board
    lnk = lnk.split(r"/")[2:]
    chan, board = lnk[0], lnk[1]
    if chan == "boards.4chan.org" or chan == "4chan.org":
        mserv = "i.4cdn.org"
    elif chan == "8ch.net":
        mserv = "media.8ch.net"
    else:
        mserv = chan + ''
    mserv = 'https://' + mserv
    chan = 'https://' + chan
    return lnk[-1:][0].split('.')[0]


def getFilList(tn):
    global chan, board, post
    post = 'res/{}.json'.format(tn)
    url = '/'.join([chan, board, post])
    print(url)
    posts = requests.get(url).json()['posts']
    files = flat([[(get_filename(post), get_filepath(post))
                   for post in posts
                   if 'filename' in post and not isDownloaded(post)],
                  flat([
                      [(get_filename(file), get_filepath(file))
                       for file in post['extra_files']
                       if not isDownloaded(file)]
                      for post in posts
                      if 'extra_files' in post
                  ])])
    return files


def print_help():
    print("Usage: ./iboarddown.py somelink (downloaddir)")


def main(tn=None, dest_dir="./"):
    args = sys.argv[1:]
    if len(args) < 1:
        print_help()
        return -1
    tn = args[0]
    if len(args) > 1:
        dest_dir = args[1]
    files = getFilList(set_board(tn))
    for name, path in files:
        print("Downloading: \"" + name + "\"")
        r = requests.get(path)
        with open(os.path.join(dest_dir, name), 'wb') as fd:
            fd.write(r.content)


if __name__ == "__main__":
    main()
