# Riak Plugin for Server Density

Make sure stats are enabled for riak (riak_kv_stat=true)

Add something like this to your SD config:

    [Riak]
    stats_url: http://127.0.0.1:8098/stats

You can also add a comma-separated list of stats to include or exclude
with whitelist or blacklist, respectively.

You can run `curl 10.0.0.2:8098/stats | python -m json.tool` to get an
idea of what stats are available.