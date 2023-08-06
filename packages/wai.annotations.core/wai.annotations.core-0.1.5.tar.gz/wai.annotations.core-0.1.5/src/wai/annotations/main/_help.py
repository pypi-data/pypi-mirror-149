from .commands import list_commands


def main_help() -> str:
    """
    Formats the main -h/--help message for wai.annotations.

    :return:
                The help message.
    """
    return (
        f"Available commands:\n"
        f"  " + '\n  '.join(list_commands()) + f"\n"
        f"\n"
        f"Use:\n"
        f"      wai-annotations [command] -h\n"
        f"\n"
        f"for command-specific help.\n"
        f"\n"
        f"See following URL for usage and examples:\n"
        f"https://ufdl.cms.waikato.ac.nz/wai-annotations-manual/\n"
    )
