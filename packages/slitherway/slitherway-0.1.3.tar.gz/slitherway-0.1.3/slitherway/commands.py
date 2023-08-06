import subprocess
from subprocess import CompletedProcess
from typing import Optional

from slitherway.models import FlywayCommandArgs


def migrate(args: Optional[FlywayCommandArgs] = None) -> CompletedProcess:
    command = "flyway migrate"
    return __execute(command, args)


def clean(args: Optional[FlywayCommandArgs] = None) -> CompletedProcess:
    command = "flyway clean"
    return __execute(command, args)


def __execute(command: str, args: Optional[FlywayCommandArgs]) -> CompletedProcess:
    if args:
        if args.config_files:
            config_files = ",".join(args.config_files)
            command += f" -config-files={config_files}"

        if args.user:
            command += f" -user={args.user}"

        if args.password:
            command += f" -password={args.password}"

        if args.url:
            command += f" -url={args.url}"

        if args.locations:
            locations = ",".join(args.locations)
            command += f" -locations={locations}"

    return subprocess.run(command, shell=True, check=True)
