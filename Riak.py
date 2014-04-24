""" Riak Plugin for Server Density

Make sure stats are enabled for riak (riak_kv_stat=true)

Add something like this to your SD config:

    [Riak]
    stats_url: http://127.0.0.1:8098/stats

You can also add a comma-separated list of stats to include or exclude
with whitelist or blacklist, respectively.

You can run `curl 10.0.0.2:8098/stats | python -m json.tool` to get an
idea of what stats are available.
"""
import json
import urllib2

# A list of keys and key suffixes to allow by default
_whitelist = [
    'memory_total', 'pbc_active',
    '_gets', '_gets_total',
    '_puts', '_puts_total',
    '_reads', '_reads_total',
    '_writes', '_writes_total',
    '_connects', '_connects_total',
    '_repairs', '_repairs_total',
    '_deletes', '_deletes_total',
    '_mean', 'executing_mappers',
    'sys_process_count',
]


class Riak(object):

    def __init__(self, agentConfig, checksLogger, rawConfig):
        self.config = agentConfig
        self.log = checksLogger
        self.raw_config = rawConfig

    def run(self):
        stat_url = self.raw_config['Riak']['stats_url']
        whitelist = set(filter(bool, [s.strip() for s in
                                      self.raw_config['Riak'].get('whitelist', '').split(',')]))
        whitelist.update(_whitelist)
        blacklist = set(filter(bool, [s.strip() for s in
                                      self.raw_config['Riak'].get('blacklist', '').split(',')]))
        try:
            res = urllib2.urlopen(stat_url)
            all_stats = json.load(res)
            stats = {}

            def filter_key(key):
                for k in blacklist:
                    if key.endswith(k):
                        return False
                for k in whitelist:
                    if key.endswith(k):
                        return True
                return False

            stats = {k: v for k, v in all_stats.iteritems() if filter_key(k)}
            self.log.info('RiakPlugin: Loaded Riak stats OK. Included {} of {} fields.'.format(
                len(stats), len(all_stats)))
        except Exception, e:
            self.log.error('RiakPlugin: Failed to load Riak stats.')
            self.log.error(e)
            stats = {}

        return stats
