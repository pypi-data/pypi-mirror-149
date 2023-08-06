#!/usr/bin/env python3

""" polls JSD to find tickets I'm assigned to """

from configparser import ConfigParser, NoOptionError
import os
from pathlib import Path
import sys

from dateutil.parser import parse as parse_date
from jira import JIRA
import jira.exceptions
from texttable import Texttable # type: ignore


from loguru import logger

if not os.environ.get('LOGURU_LEVEL'):
    logger.remove()
    logger.add(sink=sys.stderr, level="INFO")


CONFIG_FILENAME = 'jsd_job_bot.ini'
JSD_SEARCH = """assignee = currentuser() ORDER BY updated ASC"""

IGNORED_STATUS = [
    'Completed',
    'Done',
    'Canceled',
    'Resolved',
    'Closed',
]


def ignore_this_field(fieldname: str) -> bool:
    """ filters fields """
    retval = False
    if fieldname.startswith("_"):
        retval = True
    elif fieldname.startswith("customfield"):
        retval = True
    return retval


def main() -> None:
    """ the function code """
    config = ConfigParser()
    for config_file in [Path(f'~/.config/{CONFIG_FILENAME}'),
                        Path(f'~/etc/{CONFIG_FILENAME}'),
                        Path(f'./{CONFIG_FILENAME}'),
                        ]:
        if config_file.resolve().expanduser().exists():
            logger.debug(f"Loading config: {config_file}")
            config.read(config_file.resolve().expanduser())
        else:
            logger.debug(f"Couldn't find {config_file}")

    # don't show things by default
    if not config.has_option('DEFAULT', 'SHOW_ALL_JOBS'):
        logger.debug("Setting show all jobs to false, currently unset")
        config.set('DEFAULT', 'SHOW_ALL_JOBS', 'false')

    assigned_issues = 0
    table = Texttable()
    table.set_cols_dtype(['a', 'a', 'a', 'a'])
    table.set_max_width(0)
    table.set_deco(Texttable.BORDER + Texttable.VLINES + Texttable.HEADER)
    table.add_row(['Issue', 'Status', 'Updated', 'Summary'])
    try:
        logger.debug(f"JIRA Server: '{config.get('DEFAULT', 'JSD_HOSTNAME')}'")
        logger.debug(f"JIRA Username: '{config.get('DEFAULT', 'JSD_USERNAME')}'")
        logger.debug(f"JIRA API Key: '{config.get('DEFAULT', 'JSD_API_KEY')}'")
        logger.debug("Instantiating JIRA connection...")
        jira_client_object = JIRA(
            f"https://{config.get('DEFAULT', 'JSD_HOSTNAME')}",
            basic_auth=(config.get('DEFAULT', 'JSD_USERNAME'), config.get('DEFAULT', 'JSD_API_KEY')),
            )
        logger.debug("Done instantiating JIRA connection...")
    except KeyError as key_error:
        logger.error("You're missing config options: {}", key_error)
        sys.exit(1)
    except NoOptionError as key_error:
        logger.error("You're missing config options: {}", key_error)
        sys.exit(1)
    except ConnectionError as error_message:
        logger.error(f"Connection error: {error_message}")

    try:
        logger.debug("Searching for jobs assigned to you...")
        issues = jira_client_object.search_issues(jql_str=JSD_SEARCH, maxResults=False)
        # noqa: pylint: disable=invalid-name
    except jira.exceptions.JIRAError as error_message:
        logger.error(error_message)
        sys.exit(1)

    for issue in issues:
        status = str(issue.fields.status) # type: ignore
        summary = str(issue.fields.summary) # type: ignore
        updated = str(issue.fields.updated) # type: ignore

        if config.getboolean('DEFAULT', 'SHOW_ALL_JOBS') or status.strip() not in IGNORED_STATUS:
            assigned_issues += 1
            updated_parsed = parse_date(updated)

            logger.debug(f"{issue}\t{status}\t{updated_parsed.date()}\t{summary}")
            table.add_row([str(issue),
                           status,
                           updated_parsed.date(),
                           summary,
                           ])
            #logger.debug([dirfield for dirfield in dir(issue.fields) if not ignore_this_field(dirfield)])
    print(table.draw())

    logger.info(f"{assigned_issues} tickets assigned to you...")
