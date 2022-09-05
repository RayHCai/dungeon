# dungeon

A hidden file system for windows.

### Local Installation:

- Run install.py (need pip installed)

### Local Use

Open terminal and run `dungeon` for a list of comamnds.

### Code Layout

- Commands
    - own file within `commands` folder
    - class structure
    - **required** `run` method
        - this is method that is first run when the command is executed
    - **required** method `gen_{COMMAND_NAME}_command` method in `__init__.py` under `commands` folder
        - look at other gen methods for style

### Style

Errors
 - period at the end of error