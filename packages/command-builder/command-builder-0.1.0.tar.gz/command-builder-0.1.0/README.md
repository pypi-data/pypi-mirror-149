# Command Builder

Command Builder is a library that manages the execution of shell commands, creating a summary of the executions. The objective is to facilitate the perception of errors.

## Installation

> You need Python 3.7 or above.

From the terminal, enter:

```bash
pip install -U command-builder
```

## Getting started

> The examples refer to the newest version (0.1.0) of command-builder.

First, let's init the command-builder:

```python
from command_builder.command_builder import CommandBuilder

command_builder = CommandBuilder()

```

Adding commands:

```python
command_builder.add(name="ls", command=["ls", "-a"])
command_builder.add(name="pwd", command=["pwd", "-o"])
```

Running commands:

```python
command_builder.run()
```

Output:

```diff
______________________________summary______________________________
+ ls: commands succeeded
- ERROR: pwd: commands failed
```

