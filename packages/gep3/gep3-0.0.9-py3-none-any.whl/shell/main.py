"""GEP3 Shell application
"""

# Standard library imports

# Third party imports
import cmd2

# Local application imports

# Module variables
INTRO_STRING = "Welcome to GEP3 Shell v0.1\n(c) 2022 Sebastien Pochic\n\
------------------------------------------------------------------------------"
DEFAULT_PROMPT_NAME = "(GEP3Shell) "

class Gep3Shell(cmd2.Cmd):
    """GEP3 Shell application."""

    def __init__(self, *args, **kwargs):
        print("DEBUG:Gep3Shell.__init__()")
        super().__init__(*args, **kwargs)
        self.intro = INTRO_STRING
        self.prompt = DEFAULT_PROMPT_NAME

if __name__ == '__main__':
    import sys
    app = Gep3Shell()
    sys.exit(app.cmdloop())
