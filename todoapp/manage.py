#!/usr/bin/env python
import collections
import collections.abc
import os
import sys

collections.Callable = collections.abc.Callable

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "todoapp.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
