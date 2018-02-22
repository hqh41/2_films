# coding=utf-8

from __future__ import unicode_literals, print_function
import mongoengine


mongoengine.connect('MovieLib')


class Player(mongoengine.Document):
    nickname = mongoengine.StringField()
    diff = mongoengine.StringField()
    score = mongoengine.IntField(default=0)
    created = mongoengine.DateTimeField()
