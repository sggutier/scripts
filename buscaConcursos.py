#!/usr/bin/env python3

import requests
import os
import sys
import itertools
import time


def makeCFLink(user, pini, cnt):
    return "http://codeforces.com/api/user.status?" \
        + "handle={0}".format(user) \
        + "&from={0}".format(pini) \
        + "&count={0}".format(cnt)


def getContests(subs):
    conts = {}
    for sub in subs:
        if 'contestId' in sub and 'author' in sub:
            cttype = sub['author']['participantType']
            if cttype in ('CONTESTANT', 'VIRTUAL'):
                dt = sub['creationTimeSeconds']
                conts[sub['contestId']] = time.localtime(dt)
    return conts


def getAllCs(subs):
    conts = {}
    for sub in subs:
        if 'contestId' in sub:
            dt = sub['creationTimeSeconds']
            if sub['contestId'] not in conts:
                conts[sub['contestId']] = time.localtime(dt)
    return conts


def notmain(user, pini=1, cnt=500):
    url = makeCFLink(user, pini, cnt)
    subs = requests.get(url).json()['result']
    return getContests(subs)


def amain(user, pini, cnt):
    url = makeCFLink(user, pini, cnt)
    subs = requests.get(url).json()['result']
    return getAllCs(subs)


def printConts(conts, gymOnly=False):
    for c, dt in conts.items():
        if not gymOnly or c > 1000:
            print("{0} :: {1}".format(c, time.strftime("%Y-%m-%d %H:%M:%S", dt)))


def print_help():
    print('usage: ./buscaConcursos.py codeforcesuser')


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) < 1:
        print_help()
        exit(-1)
    printConts(notmain(*args))
