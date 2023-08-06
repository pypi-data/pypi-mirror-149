import sys
import asyncio
import argparse

from urllib.parse import parse_qsl

from powerful_pipes import async_read_json_from_stdin, async_write_json_to_stdout, \
    async_report_exception, async_write_to_stderr

from .exceptions import *
from .config import RunningConfig
from .rules_engine import compile_rule, CompiledRule
from .destinations import connect_destination, NotifierInterface


async def run(
        connection: NotifierInterface,
        config: RunningConfig,
        compiled_rule: CompiledRule = None
):

    compiled_rule = compiled_rule or CompiledRule()

    async for error, json_message in async_read_json_from_stdin():

        if error:
            if config.echo:
                await async_write_to_stderr(json_message)

            # Not valid JSON data
            continue

        try:

            # Only notify if rules matches with users requirements
            if compiled_rule.match(json_message):

                json_message.setdefault("_meta", {})

                if config.labels:
                    for label in config.labels:
                        json_message.get("_meta").update(dict(parse_qsl(label)))

                if not config.debug:
                    await connection.notify(json_message)

            # Pass data thought pipeline or not
            if not config.no_display:
                await async_write_json_to_stdout(json_message, force_flush=True)

        except Exception as e:
            await async_report_exception({}, e)

    if not config.debug:
        await connection.join()


async def async_main(config: RunningConfig, compiled_rule: CompiledRule = None):

    if config.debug:
        con = None

    else:
        try:
            con = await connect_destination(config)

        except Exception as e:
            print(e)
            exit(1)

    await run(con, config, compiled_rule)

def main():
    banner = 'Notifier for OpenAPI Generator'

    parser = argparse.ArgumentParser(
        description=banner
    )
    parser.add_argument('labels',
                        nargs="*",
                        help="custom labels. Example: status=running")
    parser.add_argument('--debug',
                        default=False,
                        action="store_true",
                        help="enable debug mode")

    display = parser.add_argument_group("display options")
    display.add_argument('-b', '--banner',
                         default=False,
                         action="store_true",
                         help="displays tool banner")
    display.add_argument('-e', '--echo',
                         default=False,
                         action="store_true",
                         help="displays messages that can't be processed")
    display.add_argument('-nd', '--no-display',
                         default=False,
                         action="store_true",
                         help="do not display input messages in stdout")

    destinations = parser.add_argument_group("destination options")
    destinations.add_argument('-d', '--destination-uri',
                              required=True,
                              help="destination notifications. "
                                   "Allowed URI prefixes: 'http://'")
    destinations.add_argument('-t', '--timeout',
                              default=80.0,
                              type=float,
                              help="notification timeout (in seconds). "
                                   "Default: 1 sec")
    destinations.add_argument('-C', '--max-concurrency',
                              default=5,
                              type=int,
                              help="max notification concurrency")

    destinations = parser.add_argument_group("rules options")
    destinations.add_argument('-R', '--execution-rule',
                              default=None,
                              help="notification rules")

    parsed = parser.parse_args()

    config = RunningConfig.from_cli(parsed)

    if config.banner:
        print(f"[*] Starting {banner}", flush=True, file=sys.stderr)

    # Check rule format before start
    if config.execution_rule:

        try:
            compiled_rule = compile_rule(config.execution_rule)
        except NotifierException as e:
            print(f"[!] {str(e)}", flush=True, file=sys.stderr)
            exit(1)

    else:
        compiled_rule = None

    try:
        asyncio.run(async_main(config, compiled_rule))
    except KeyboardInterrupt:
        ...



if __name__ == '__main__':
    main()
