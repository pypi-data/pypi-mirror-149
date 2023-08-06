# Polidoro CLI
[![Upload Python Package](https://github.com/heitorpolidoro/polidoro-cli/actions/workflows/python-publish.yml/badge.svg)](https://github.com/heitorpolidoro/polidoro-cli/actions/workflows/python-publish.yml)
[![Lint with comments](https://github.com/heitorpolidoro/polidoro-cli/actions/workflows/python-lint.yml/badge.svg)](https://github.com/heitorpolidoro/polidoro-cli/actions/workflows/python-lint.yml)
![GitHub last commit](https://img.shields.io/github/last-commit/heitorpolidoro/polidoro-cli)
[![Coverage Status](https://coveralls.io/repos/github/heitorpolidoro/polidoro-cli/badge.svg?branch=master)](https://coveralls.io/github/heitorpolidoro/polidoro-cli?branch=master)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=heitorpolidoro_polidoro-cli&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=heitorpolidoro_polidoro-cli)

[![Latest](https://img.shields.io/github/release/heitorpolidoro/polidoro-cli.svg?label=latest)](https://github.com/heitorpolidoro/polidoro-cli/releases/latest)
![GitHub Release Date](https://img.shields.io/github/release-date/heitorpolidoro/polidoro-cli)

![PyPI - Downloads](https://img.shields.io/pypi/dm/polidoro-cli?label=PyPi%20Downloads)

![GitHub](https://img.shields.io/github/license/heitorpolidoro/polidoro-cli)
### To install

```
sudo apt install python3-pip -y
pip3 install polidoro_cli
```

Then add to your `.bashrc`
```
export PATH="$PATH:$HOME/.local/bin/"
```

### To use:
`cli --help`

### Tips:
Create alias for the CLI commands:

Add in your `.bashrc`
```
alias dk='cli docker'
alias ex='cli elixir'
alias dj='cli django'
alias rb='cli ruby'
alias g='cli git'
...
```
Or run `cli create_aliases` to create aliases for all default CLIs
### Default CLIs:
- **Django** [more information](README_DJANGO.md)
- **Docker:** [more information](README_DOCKER.md)
- **Elixir:** [more information](README_ELIXIR.md)
- **Git:** [more information](README_GIT.md)
- **NPM:** [more information](README_NPM.md)
- **PyTest:** [more information](README_PYTEST.md)
- **Ruby:** [more information](README_RUBY.md)

### Creating your own CLI
To create your CLI just create a file in `~/.cli` with the CLI name `NAME.cli` or `NAME.py` then call it with `cli name` or create an alias for it:
```shell
alias name='cli name'
```
In the `.cli` file, create aliases similar to the bash
```
# git.cli
ps=git push
```
To call run `cli git ps`. Or create an bash alias `alias g=cli git` then run using only `g ps` 

#### Multiples aliases
To create multiples aliases separate by `,`
```
# git.cli
simple_log,l=git log --one-line
```
You can call using either `g simple_log` or `g l`.

#### Multiples commands
To create a command with multiple commands separate by `;`
```
# git.cli
commit_push,cp=git commit;git push
```
**NOTE:** If any command fails, will not execute the other commands

#### Using arguments
The CLI will put any arguments at the end of the command, by default, 
but you can specify where use those arguments using `$args`.
```
# git.cli
commit_push,cp=git commit -m "$args";git push
```
Run with `g cp batata` will execute `git commit -m "batata"` then `git push`

It is possible to specify the argument
```
# postgres.cli
run=psql -U $arg0 -d $arg1 -c $arg2
```
Running `cli postgres run heitor polidoro_db "select * from table"` will execute 
`psql -U 'heitor' -d 'polidoro_db' -c 'select * from table'`

Use `${argN:DEFAULT_VALUE}` to specify a default value to the argument

#### Variables

To set some variable use `set NAME=VALE` and use it with `$NAME`
```
# postgres.cli
set DB_USER=heitor
set DB_NAME=polidoro_db

run=psql -U $USER -d $DB_NAME -c 
```
Running `cli postgres run "select * from table"` will execute
`psql -U 'heitor' -d 'polidoro_db' -c 'select * from table'`

There is a special variable called `DEFAULT_COMMAND`, when set will start all commands with the value. 
```
# git.cli
set DEFAULT_COMMAND=git

ps=push
pl=pull
commit_push,cp=commit -m "$args";push
```
When run `g ps` will execute `git push`. Also works with multiple commands, like `g cp msg` will execute 
`git commit -m "msg"` then `git push`. Also, when `DEFAULT_COMMAND` is set, all commands that is not set in 
the `.cli` file will be called using the `DEFAULT_COMMAND`. `g fetch` will call `git fetch` even if the command
`fetch` is not in the `git.cli`, and, when run `--help` will show the `DEFAULT_COMMAND` help then the CLI help.

There is a pair of special variables called `docker` and `service`, you can't (shouldn't) set, but you can use. When used will 
replace the `$docker` with `docker-compose exec $service` if the parameter `-d/--docker` is in the command line.
The CLI will replace `$service` for the first argument from the command line, if is a valid service,
or will use the first service with `build` in `docker-compose.yml`.

```
# elixir.cli
deps=$docker mix deps.get
```
If you call `ex deps` will execute `mix deps.get`, if you call `ex deps -d` will execute `docker-compose exec service_name mix deps.get`
or `ex deps -d other_service` will execute `docker-compose exec other_service mix deps.get`. 
With the `$docker` variable you can create CLIs that runs in the host or in the container.

You can combine things like:
```
# elixir.cli
set DEFAULT_COMMAND=$docker mix

deps=deps.get
setup=ecto.setup
reset=ecto.reset
```
All commands will run in the host or in the container if `-d/--docker` is in the parameters

You can explicit the command (or replace the `DEFAULT_COMMAND`) passing a dict (Python format) as command.
```
# elixir.cli
set DEFAULT_COMMAND=mix

deps=deps.get
iex={'command': 'iex -S mix'}
```
In this case, when you call `ex iex` will run `iex -S mix` without the `DEFAULT_COMMAND`

These ar the values you can use:

| Key | Description |
| ---: | --- |
| `command` | The command to execute |
| `help` | Replace the generated help |
| `show_cmd` | To print or not the command (default=`True`) |
| `exit_on_fail` | if `False` will not terminate multiples commands when any one fails (default=`True`) |
| `messages` | Another dict with Messages to print: <br> `start`: Print the message before any command <br> `success`: Print the message when the command finish with success <br> `error`: Print the message when the command fails <br> `finish`: Print the message regardless the command result |
| `ANY_THNG` | Will set environment variable

Examples:
```
test={
    'command': '$docker mix test',
    'MIX_ENV': 'test'
}
```
Will set the environment variable `MIX_ENV` to `test` then run `mix test`

#### Environment Variables
To set an environment variable for the CLIs commands use `export` like in bash
```
# pytest.cli
export DJANGO_LOG_FILE=/tmp/log
export PYTEST_ADDOPTS="--color=yes"
```
Any command in the Pytest CLI will use those environment variables

#### Complex Commands
To create more complexes commands, you can create a `NAME.py` file. Create a class with the name of the CLI,
annotate the method you want with `@Command` and run the commands with `CLI.execute`
```
# git.py
import os

from polidoro_argument import Command
from polidoro_cli import CLI


class Git(object):
    @staticmethod
    @Command(help='Run "git fetch" in all git projects')
    def fetch_all():
        for dir in os.listdir():
            if os.path.isdir(dir):
                os.chdir(dir)
                if os.path.exists('.git'):
                    print(f'Fetching in {dir}...')
                    CLI.execute('git fetch', show_cmd=False)
                os.chdir('..')
```

