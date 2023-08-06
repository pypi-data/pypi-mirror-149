from logging import Formatter


def create_formatter(
    levelname: bool = True,
    process: bool = True,
    name: bool = True,
    funcName: bool = True,
    lineno: bool = True,
    datetime_format: str = "%Y-%m-%d %H:%M:%S",
    simple_description: bool = False,
) -> Formatter:
    # Create a formatter with only date and message logs
    if simple_description:
        levelname = False
        process = False
        name = False
        funcName = False
        lineno = False

    logs_format = '%(asctime)s.%(msecs).0f'

    def include_info(logs_format: str,
                     info_name: str,
                     prefix: str = ' ',
                     print_format: str = 's',
                     should_include: bool = True
                     ) -> str:
        """Include some additional info if needed"""
        if should_include:
            logs_format += f'{prefix}%({info_name}){print_format}'

        return logs_format

    prefix_map = {'levelname': ' ',
                  'process': ' PID:',
                  'name': ' ',
                  'funcName': '.',
                  'lineno': ':',
                  }
    print_format_map = {'levelname': 's',
                        'process': 'd',
                        'name': 's',
                        'funcName': 's',
                        'lineno': 'd',
                        }
    for info_name in ['levelname', 'process', 'name', 'funcName', 'lineno']:
        should_include = locals()[info_name]
        logs_format = include_info(logs_format,
                                   info_name,
                                   prefix_map[info_name],
                                   print_format_map[info_name],
                                   should_include,
                                   )

    logs_format = include_info(logs_format, 'message', ' ')

    formatter = Formatter(fmt=logs_format, datefmt=datetime_format)
    return formatter
