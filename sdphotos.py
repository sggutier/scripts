#!/usr/bin/env python
# -*- coding: utf-8 -*-
import locale
import os
import platform
import re
import time
try:
    import shutil
    import exifread
except:
    print "Primero instala exifread y shutil con pip"
    print "(Quejate con Germán)"
    exit()


months_list = ['enero',
               'febrero',
               'marzo',
               'abril',
               'mayo',
               'junio',
               'julio',
               'agosto',
               'septiembre',
               'octubre',
               'noviembre',
               'diciembre']
pic_filetypes = ['jpg',
                 'jpeg',
                 'png',
                 'raw',
                 'exif',
                 'tiff',
                 'tif',
                 'rif',
                 'ari',
                 'gif',
                 'bmp',
                 'png',
                 'psd',
                 'cr2']


def is_string_number(S):
    try:
        int(S)
        res = True
    except:
        res = False
    return res


def get_additional_dirs():
    dirs_list = []
    root_dir = os.path.abspath(os.sep)
    username = os.getlogin()
    config_file = os.path.join(root_dir,
                               "home",
                               username,
                               ".sdphotos_files.txt")
    if os.path.exists(config_file):
        for line in open(config_file):
            dirs_list.append(line.rstrip().split(","))
    return dirs_list


def delete_photos_p():
    msgInicio = "¿Quieres borrar las fotos al terminar? (si/no): "
    strTmp = ""
    while not strTmp == 'si' and not strTmp == 'no':
        strTmp = raw_input(msgInicio)
    return strTmp == "si"


def get_cur_path():
    if platform.system() == "Windows":
        cur_path = os.path.dirname(os.path.abspath(__file__))
    else:
        root_dir = os.path.abspath(os.sep)
        username = os.getlogin()
        extra_dirs = get_additional_dirs()
        user_media_dir = os.path.join(root_dir,
                                      "media",
                                      username)
        user_media_dir_list = os.listdir(user_media_dir)
        cur_num = ""
        while (not is_string_number(cur_num) or
               not int(cur_num) in
               range(0, len(user_media_dir_list) + len(extra_dirs))):
            print "Selecciona el dispositivo del que se copiarán las fotos"
            for i in range(0, len(user_media_dir_list)):
                print "\t" + user_media_dir_list[i] + " (%d)" % i
            for i in range(0, len(extra_dirs)):
                print "\t" + \
                    extra_dirs[i][1] + \
                    " (%d)" % (i + len(user_media_dir_list))
            cur_num = raw_input("Escribe el número ")
        cur_num = int(cur_num)
        if cur_num in range(0, len(user_media_dir_list)):
            cur_path = os.path.join(user_media_dir,
                                    user_media_dir_list[cur_num])
        else:
            cur_path = os.path.join(user_media_dir,
                                    extra_dirs
                                    [cur_num -
                                     len(user_media_dir_list)][0])
    return cur_path


def get_pics_dir():
    if re.match("es", locale.getdefaultlocale()[0]):
        pics_dir = "Imágenes"
    else:
        pics_dir = "Pictures"
    return pics_dir


def get_dbase_path():
    return os.path.join(os.environ['HOME'],
                        pics_dir,
                        "archivo-fotografico")

flagDelFile = delete_photos_p()
cur_path = get_cur_path()
pics_dir = get_pics_dir()
dbase_path = get_dbase_path()

if not os.path.exists(dbase_path):
    os.makedirs(dbase_path)

for root, dirs, files in os.walk(cur_path):
    for cur_file in files:
        picFil = os.path.join(root, cur_file)
        f = open(picFil, 'rb')
        try:
            tags = exifread.process_file(f)
            takDate = str(tags['EXIF DateTimeOriginal'])\
                .split(' ')[0].split(':')
        except:
            if cur_file.lower().endswith(tuple(pic_filetypes)):
                tak_Date_tmp = time.gmtime(os.path.getmtime(picFil))
                tak_Date_tmp = [tak_Date_tmp.tm_year,
                                tak_Date_tmp.tm_mon,
                                tak_Date_tmp.tm_mday]
                takDate = []
                for t in tak_Date_tmp:
                    takDate.append("%d" % t)
            else:
                f.close()
                continue
        try:
            y = takDate[0]
            m = takDate[1] + " " + months_list[int(takDate[1])-1]
            d = takDate[2]
            print "Organizando " + \
                cur_file + \
                " (tomada el %s/%s/%s)" % (d, m.split()[1], y)
            datDir = os.path.join(dbase_path, y, m, d)
            if not os.path.exists(datDir):
                os.makedirs(datDir)
            cur_file2 = cur_file
            while os.path.isfile(os.path.join(datDir, cur_file2)):
                cur_file2 = "Copia de " + cur_file2
            shutil.copyfile(picFil, os.path.join(datDir, cur_file2))
            f.close()
            if flagDelFile:
                os.remove(os.path.join(root, cur_file))

        except:
            print "Error con la foto %s" % os.path.join(root, cur_file)
            f.close()
            raise
