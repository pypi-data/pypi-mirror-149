"""
Usage:
    ansible-events [options]

Options:
    -h, --help                  Show this page
    -v, --vars=<v>              Variables file
    -i, --inventory=<i>         Inventory
    --rules=<r>                 The rules file or rules from a collection
    -S=<S>, --source_dir=<S>    Source dir
    --vars=<v>                  A vars file
    --env-vars=<e>              Comma separated list of variables to import from the environment
    --redis_host_name=<h>       Redis host name
    --redis_port=<p>            Redis port
    --debug                     Show debug logging
    --verbose                   Show verbose logging
"""
import argparse
import sys
import os
import yaml
import logging
import multiprocessing as mp

import ansible_events.rules_parser as rules_parser
from ansible_events.engine import start_source, run_rulesets
from ansible_events.rule_types import RuleSet
from ansible_events.util import load_inventory
from ansible_events.collection import has_rules, split_collection_name
from ansible_events.collection import load_rules as collection_load_rules

from typing import Dict, List


def load_vars(parsed_args) -> Dict[str, str]:
    variables = dict()
    if parsed_args.vars:
        with open(parsed_args.vars) as f:
            variables.update(yaml.safe_load(f.read()))

    if parsed_args.env_vars:
        for env_var in parsed_args.env_vars.split(","):
            env_var = env_var.strip()
            if env_var not in os.environ:
                raise KeyError(f'Could not find environment variable "{env_var}"')
            variables[env_var] = os.environ[env_var]

    return variables


def load_rules(parsed_args) -> List[RuleSet]:
    logger = mp.log_to_stderr()
    if not parsed_args.rules:
        logger.debug('Loading no rules')
        return []
    elif os.path.exists(parsed_args.rules):
        logger.debug(f'Loading rules from the file system {parsed_args.rules}')
        with open(parsed_args.rules) as f:
            return rules_parser.parse_rule_sets(yaml.safe_load(f.read()))
    elif has_rules(*split_collection_name(parsed_args.rules)):
        logger.debug(f'Loading rules from a collection {parsed_args.rules}')
        return rules_parser.parse_rule_sets(collection_load_rules(*split_collection_name(parsed_args.rules)))
    else:
        raise Exception(f'Could not find ruleset {parsed_args.rules}')



def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rules')
    parser.add_argument('--vars')
    parser.add_argument('--env-vars')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--redis-host-name')
    parser.add_argument('--redis-port')
    parser.add_argument('-S', '--source-dir')
    parser.add_argument('-i', '--inventory')
    return parser


def main(args):
    """Console script for ansible_events."""
    parser = get_parser()
    parsed_args = parser.parse_args(args)
    logger = mp.log_to_stderr()
    if parsed_args.debug:
        logger.setLevel(logging.DEBUG)
    elif parsed_args.verbose:
        logger.setLevel(logging.INFO)
    variables = load_vars(parsed_args)
    rulesets = load_rules(parsed_args)
    if parsed_args.inventory:
        inventory = load_inventory(parsed_args.inventory)
    else:
        inventory = {}

    tasks = []
    ruleset_queues = []

    event_log: mp.Queue = mp.Queue()

    for ruleset in rulesets:
        sources = ruleset.sources
        queue: mp.Queue = mp.Queue()

        for source in sources:
            tasks.append(mp.Process(target=start_source, args=(source, [parsed_args.source_dir], variables, queue)))
        ruleset_queues.append((ruleset, queue))

    tasks.append(
        mp.Process(
            target=run_rulesets,
            args=(
                event_log,
                ruleset_queues,
                variables,
                inventory,
                parsed_args.redis_host_name,
                parsed_args.redis_port,
            ),
        )
    )
    logger.info("Starting processes")
    for task in tasks:
        task.start()

    logger.info("Joining processes")
    try:
        for task in tasks:
            task.join()
    except KeyboardInterrupt:
        pass

    return 0


def entry_point() -> None:
    main(sys.argv[1:])


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))  # pragma: no cover
