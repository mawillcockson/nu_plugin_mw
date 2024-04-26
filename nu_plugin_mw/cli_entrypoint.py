"""
the various functions to call for ways of running plugins from the command-line
"""


def encoding_type() -> bytes:
    "report which encoding we'll use to communicate with nu"
    encoding: str = "json"
    length = len(encoding).to_bytes(length=1, byteorder="big", signed=False)
    return length + encoding.encode("ascii")


def nu_plugin_main() -> None:
    "discover plugins and communicate with nu"
    import sys
    from argparse import ArgumentParser

    parser = ArgumentParser()
    # https://www.nushell.sh/contributor-book/plugin_protocol_reference.html#how-nu-runs-plugins
    parser.add_argument(
        "--stdio",
        action="store_true",
        required=True,
        help="perform nu protocol communication over stdin and stdout",
    )

    _ = parser.parse_args()

    if not hasattr(sys.stdout, "buffer"):
        raise TypeError("expected sys.stdout to have a buffer to write bytes to")
    sys.stdout.buffer.write(encoding_type())
    sys.stdout.flush()
