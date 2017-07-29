#!/usr/bin/env python
import logging
import os
import argparse
import json
import sys

def main(args=None):

    # logging configuration
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.INFO)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)

    parser = argparse.ArgumentParser(description='CLI for Apache Ambari')
    parser.add_argument('--action',
                        dest='action',
                        choices=['create', 'stop', 'dump-config', 'update-config'],
                        required=True,
                        help='action to execute')

    parser.add_argument('--config-folder',
                        dest='config_folder',
                        required=True,
                        help='folder that holds the configuration')

    parser.add_argument('--ambari-host',
                        dest='ambari_host',
                        required=True,
                        help='hostname of the ambari server')

    parser.add_argument('--ambari-port',
                        dest='ambari_port',
                        type=int,
                        default=8080,
                        help='ambari port')

    parser.add_argument('--ambari-https',
                        dest='ambari_https',
                        type=bool,
                        default=False,
                        help='use secured https connection with ambari')

    parser.add_argument('--ambari-login',
                        dest='ambari_login',
                        default="admin",
                        help='ambari login')

    parser.add_argument('--ambari-password',
                        dest='ambari_password',
                        default="admin",
                        help='ambari password')

    parser.add_argument('--cluster-name',
                        dest='cluster_name',
                        default="hdp",
                        help='name of the cluster')

    parser.add_argument('--cluster-host-groups',
                        dest='cluster_host_groups',
                        default=None,
                        help='cluster host groups json file')

    parser.add_argument('--hdp-repo-url',
                        dest='hdp_repo_url',
                        default=None,
                        help='HDP custom repo url')

    parser.add_argument('--hdp-util-repo-url',
                        dest='hdp_util_repo_url',
                        default=None,
                        help='HDP Util custom repo url')

    args = parser.parse_args()

    ambari_client = AmbariClient()
    ambari_client.connect(
        args.ambari_host,
        args.cluster_name,
        port=args.ambari_port,
        https=args.ambari_https,
        login=args.ambari_login,
        password=args.ambari_password)

    cluster_host_groups = None
    if args.cluster_host_groups != None:
        with open(args.cluster_host_groups, 'r') as file:
            cluster_host_groups = json.load(file)

    if args.action == "create":
        ambari_client.create_cluster(
            args.config_folder,
            cluster_host_groups,
            hdp_repo_url=args.hdp_repo_url,
            hdp_util_repo_url=args.hdp_util_repo_url)
    elif args.action == "dump-config":
        ambari_client.dump_config(
            args.config_folder,
            cluster_host_groups)
    elif args.action == "update-config":
        ambari_client.update_cluster(
            args.config_folder,
            cluster_host_groups)
    elif args.action == "stop":
        ambari_client.stop_cluster()


if __name__ == '__main__':
    from ambariClient import AmbariClient
    sys.exit(main())
else:
    from .ambariClient import AmbariClient