"""
Copyright (c) 2022 Plugin Andrey (9keepa@gmail.com)
Licensed under the MIT License
"""
import os
import re
import sys
from io import IOBase
from paramiko import SSHClient, AutoAddPolicy
from paramiko.channel import ChannelFile
from jinja2 import Template
from .tool import log
from configparser import ConfigParser, ExtendedInterpolation
from typing import Union, Any, Callable


def is_posix():
    try:
        import posix
        return True
    except Exception:
        return False


logger = log(__name__)


DEFAULT_TEMPLATE = """
{% set runcmd = Self.color.WHITE + '[ Run command ] ' + Self.color.COMMAND + Self.command + " " + Self.color.END %}
{% set stdout = Self.color.OKGREEN + '[ STDOUT ]' + Self.color.END %}
{% set stderr = Self.color.RED + '[ STDERR ]' + Self.color.END %}
{% set result = Self.color.OKCYAN + '[ Result ] ' + Self.color.COMMAND + Self.command + Self.color.END + Self.color.OKGREEN + " return_code " + Self.stdout_return_code + Self.color.END %}
{{runcmd}}
{% if stdout_rows %}{{stdout}}{{'-' * (Self.terminal_columns - stdout|length)}}{% endif +%}
{% for line in stdout_rows -%}{{line}}{% endfor %}
{% if stderr_rows %}{{stderr}}{{'-' * (Self.terminal_columns - stderr|length)}}{% endif +%}
{% for line in stderr_rows -%}{{line}}{% endfor %}
{{result}}
""".strip()


class BaseSCError(Exception):
    """BaseServerClientError"""
    pass


class ExecuteCommandError(BaseSCError):
    pass


class Response:
    class color:
        """https://habr.com/ru/company/macloud/blog/558316/
        """
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        END = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        RED = '\033[31m'
        WHITE = '\033[37m'
        COMMAND = '\033[2;34m'

    def __init__(self, stdout=None, stdin=None,
                 stderr=None, encoding=None, command='',
                 shell='', env=None, exited=0, pty=False, hide=()):

        self.terminal_columns = 120
        self.terminal_lines = 10
        try:
            self.ts = os.get_terminal_size()
            self.terminal_columns = self.ts.columns
            self.terminal_lines = self.ts.lines
        except OSError:
            pass
        self.stdin: ChannelFile = stdin
        self.stdout: ChannelFile = stdout
        self.stderr: ChannelFile = stderr
        self.encoding:str = encoding
        self.command:str = command
        self.stdout_rows = [x for x in self.stdout]
        self.stderr_rows = [x for x in self.stderr]
        self.stdout_return_code = str(self.return_code())

        self.rows = []
        self.rows.extend(self.stdout_rows)
        self.rows.extend(self.stderr_rows)

    def return_code(self)->int:
        return self.stdout.channel.recv_exit_status()

    def __bool__(self):
        return self.return_code() == 0

    def __str__(self):

        # jinja_env = Environment(loader=FileSystemLoader(".", ), trim_blocks=True)
        # template = jinja_env.get_template("response_template")
        jinja_template = Template(DEFAULT_TEMPLATE, trim_blocks=True)
        string = jinja_template.render(Self=self,
                               stdout_rows=self.stdout_rows,
                               stderr_rows=self.stderr_rows)
        string = re.sub(r"\n{1,}", "\n", string)
        return string

    def pprint(self):
        print(self)


class RemoteShell:

    def __init__(self,
                 server: str, user: str, port=22, password=None,
                 response=Response):
        self.response = response
        self.server = server
        self.port = port
        self.user = user
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())  # no known_hosts error
        if is_posix():
            client.load_system_host_keys()
        client.connect(self.server, username=self.user, port=self.port, password=password)
        self.client = client

    def _execute(self, command:str):
        stdin, stdout, stderr = self.client.exec_command(command)
        return (stdin, stdout, stderr)

    def get_sftp(self):
        return self._get_sftp()

    def _get_sftp(self):
        return self.client.open_sftp()

    def get_file(self, remotepath, localpath):

        def progress(count, total, status=f' File {self.server}:{remotepath} download.'):
            bar_len = 60
            filled_len = int(round(bar_len * count / float(total)))

            percents = round(100.0 * count / float(total), 1)
            bar = '=' * filled_len + '-' * (bar_len - filled_len)

            sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
            sys.stdout.flush()

        sftp = self._get_sftp()
        sftp.get(remotepath, os.path.join(localpath), callback=progress)
        logger.info(f"File {localpath} is downloaded from {self.server}:{remotepath}")

    def put_file(self, localpath, remotepath ):

        def progress(count, total, status=f' File {localpath} upload.'):
            bar_len = 60
            filled_len = int(round(bar_len * count / float(total)))

            percents = round(100.0 * count / float(total), 1)
            bar = '=' * filled_len + '-' * (bar_len - filled_len)

            sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
            sys.stdout.flush()
        sftp = self._get_sftp()

        if isinstance(localpath, IOBase):
            file_object: IOBase = localpath
            sftp.putfo(file_object, remotepath)
        else:
            sftp.put(os.path.join(localpath), remotepath, callback=progress)
        logger.info(f"File {localpath} is uploaded into {self.server}:{remotepath}")

    def exec_command(self, command: str):
        stdin, stdout, stderr = self._execute(command)
        return self.response(stdin=stdin,stdout=stdout, stderr=stderr, command=command)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()


class Server:

    def __init__(self, server:str, user:str, port:int=22,
                 password=None, pkey=None, response=Response
                 ):

        self.response = response
        self._shell = RemoteShell(server, user, port=port, password=password,
                                  response=response)
        logger.info(f"Ok connected to server {server}:{port}")

    def monitor_server(self):
        """https://github.com/afaqurk/linux-dash"""
        pass

    def free(self):
        response = self.shell("free -h")
        return response

    def shell(self, command: str, debug=True):
        response = self._shell.exec_command(command)
        if debug:
            response.pprint()
        return response

    def struct_shell(self, command: str, debug=True):
        response = self._shell.exec_command(command)
        if debug:
            response.pprint()
        if not response:
            raise ExecuteCommandError(
                f"Command {command} completed with error. return_code {response.return_code()}")
        return response


    def command(self, *args, **kwargs):
        return self.shell(*args, **kwargs)

    def cmd(self, *args, **kwargs):
        return self.shell(*args, **kwargs)

    def execute_command(self, *args, **kwargs):
        return self.shell(*args, **kwargs)

    def put_file(self, local_path, remote_path):
        self._shell.put_file(local_path, remote_path)

    def get_file(self, remote_path, local_path):
        self._shell.get_file(remote_path, local_path)

    def get_sftp(self):
        return self._shell.get_sftp()

    def mkdir(self, path, parents=False):
        if parents:
            self._shell.exec_command(f"mkdir -p {path}")
        else:
            self._shell.exec_command(f"mkdir {path}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connect()

    def close_connect(self):
        self._shell.client.close()
        logger.info(f"Connect closed the server {self._shell.server}:{self._shell.port}")


class Config:

    class Field:
        def __init__(self, dictionary: dict):
            for k, v in dictionary.items():
                setattr(self, k, v)

    def __init__(self, *args, **kwargs):
        pass

    def read(self, path):
        config = ConfigParser(interpolation=ExtendedInterpolation())
        config.read(path)

        my_config_parser_dict = {s: dict(config.items(s)) for s in config.sections()}
        for key in my_config_parser_dict:
            val = my_config_parser_dict[key]
            fields = Config.Field(val)
            setattr(self, key, fields)
