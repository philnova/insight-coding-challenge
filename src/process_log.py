import argparse
import run_features

parser = argparse.ArgumentParser(description='Process hits from a server log.')
parser.add_argument('input_server_log',
    help='ASCII file containing server log of requests.')
parser.add_argument('output_hosts',
    help='Writeable text file to contain list of the top 10 most active host/IP addresses that have accessed the site.')
parser.add_argument('output_hours',
    help='Writeable text file to contain list of 10 resources that consume the most bandwidth on the site.')
parser.add_argument('output_resources',
    help='Writeable text file to contain list of the top 10 most frequently visited 60-minute periods.')
parser.add_argument('output_blocked',
    help='Writeable text file to contain potential security threats.')
parser.add_argument('output_bins',
    const=None,
    nargs='?',
    help='Writeable text file to contain requests from single host binned by time')
parser.add_argument('host_to_track',
    const=None,
    nargs='?',
    help='Name of host that you would like to see an activity report for')
args = parser.parse_args()

run_features.run(
    args.input_server_log,
    args.output_hosts,
    args.output_hours,
    args.output_resources,
    args.output_blocked,
    args.output_bins,
    args.host_to_track)
