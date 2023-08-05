"""The module is the entry point for the RSS reader project"""

from logging import getLogger, config

from argument_parser.arg_parser import handle_args
from config import logging_config
from content_aggregator.rss_aggregator import RSSAggregator
from output_manager import console_output, converter

config.dictConfig(logging_config)
logger = getLogger()
logger.disabled = True


def main() -> None:
    """The entry point function

    Returns:
        None
    """
    parser = handle_args()
    if parser.verbose:
        logger.disabled = False

    logger.debug('Program started.')
    rss_content = RSSAggregator(parser.source, parser.date, parser.limit)
    retrieved_rss_content = rss_content.retrieve_from_storage()
    logger.debug('Content retrieved.')

    if parser.pdf is not None:
        converter_ = converter.Converter(retrieved_rss_content)
        if parser.html is not None:
            converter_.generate_file('html', parser.html)
        converter_.generate_file('pdf', parser.pdf)
    elif parser.html is not None:
        converter_ = converter.Converter(retrieved_rss_content)
        converter_.generate_file('html', parser.html)

    if parser.json:
        print(console_output.to_json(retrieved_rss_content))
    elif parser.pdf is None and parser.html is None or parser.colorize:
        console_output.to_console(retrieved_rss_content, colorize=parser.colorize)


if __name__ == '__main__':
    main()
