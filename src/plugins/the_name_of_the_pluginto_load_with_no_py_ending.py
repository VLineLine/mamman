# -*- coding: utf-8 -*
"""First plugin-test
"""
from yapsy import IPlugin

class test(IPlugin.IPlugin):
    "this plugin should be loaded automatically"
    print("this is a plugin!! j!!")
