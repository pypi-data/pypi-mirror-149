#!/usr/bin/env python3

class InvalidPosError(Exception):
    """Exception raised when an element has an invalid position"""
    pass


class EmptyStackError(Exception):
    """Exception raised when trying to get a value from an empty stack"""
    pass


class LangError(Exception):
    """Exception raised when a problem is found while parsing a lang file"""
    def __init__(self, l_no, msg, file):
        if file != "<string>": file = f'"{file}"'
        _msg = f"File {file}, line {l_no + 1} - {msg}"
        super().__init__(_msg)
