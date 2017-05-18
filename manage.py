#!/usr/bin/env python
import os
import sys
import socket

if __name__ == "__main__":
    hostname = socket.gethostname()
    if hostname == 'ubuntu-msproperties':
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "homesoko.settings")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "homesoko.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)