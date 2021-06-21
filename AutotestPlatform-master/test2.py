# -*- coding:utf-8 -*-
import os.path

oldhouzhui='js'
newhouzhui='txt'
aimdir = '/Users/kun/Desktop/test/'
for parent, dirnames, filename in os.walk(aimdir):
    for file in filename:
        portion = os.path.splitext(file)

        if portion[1] == '.'+oldhouzhui:
            print("Filename:", portion)
            newName = portion[0] + '.'+newhouzhui
            oldnamedir = parent+ '/' + file
            newNamedir = parent+ '/'+ newName
            os.rename(oldnamedir, newNamedir)

