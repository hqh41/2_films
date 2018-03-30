# coding=utf-8

from __future__ import unicode_literals, print_function
import mongoengine

#默认连接本地27017端口，MongoDB的端口就是27017
#本机的IP地址是127.0.0.1
#Flask默认的端口是5000
mongoengine.connect('MovieLib')


class Player(mongoengine.Document):
    nickname = mongoengine.StringField()
    diff = mongoengine.StringField()
    score = mongoengine.IntField(default=0)
    created = mongoengine.DateTimeField()
