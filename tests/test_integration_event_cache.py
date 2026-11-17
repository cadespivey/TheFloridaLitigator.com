"""Repeated reuse checks retain fresh committed and transactional evidence."""
import json

from flwu import history as h, workflow as w


def test_control_event_cache_reuses_reads_and_observes_writes(tmp_path):
    config={'registry':{'stream':'fixture'}}; path=tmp_path/'history.sqlite'
    with h.database(path) as conn:
        queries=[]; conn.set_trace_callback(queries.append)
        def read():return w.events(conn,config,kinds=('integration_intent',))
        assert read()==read()==[]
        assert len([q for q in queries if 'json_extract' in q])==1
        first={'kind':'integration_intent','files':[]}
        w.record(conn,config,first)
        assert read()==[first]
        read()[0]['files'].append('caller mutation')
        assert read()==[first]
        with h.database(path) as other:
            w.record(other,config,dict(first,marker='external'))
        assert len(read())==2
        # Neither a transaction nor a rolled-back savepoint can poison reuse.
        conn.execute('SAVEPOINT pending')
        conn.execute("UPDATE captures SET payload=? WHERE stream=?",
                     (json.dumps({'workflow':dict(first,marker='temporary')}),w.stream(config)))
        assert all(e['marker']=='temporary' for e in read())
        conn.execute('ROLLBACK TO pending')
        assert read()==[first,dict(first,marker='external')]
        conn.execute('RELEASE pending')
        assert read()==[first,dict(first,marker='external')]
        assert w.events(conn,{'registry':{'stream':'other'}},kinds=('integration_intent',))==[]
