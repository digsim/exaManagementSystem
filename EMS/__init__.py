import sys
from exaManagementSystem import ExaManagementSystem

def main():
    """Entry point for the application script"""
    ems = ExaManagementSystem()
    ems.getArguments(sys.argv[1:])