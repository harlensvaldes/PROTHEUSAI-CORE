import json
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import met001


class MetricsTest(unittest.TestCase):
    def test_dedup_cutoff_incomplete_and_inherited(self):
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / 'events.jsonl'
            usage = dict(input_tokens=100, cached_input_tokens=40, cache_write_input_tokens=0,
                         output_tokens=10, reasoning_output_tokens=3, total_tokens=110)
            events = [
                {'type': 'session_meta', 'payload': {'id': 's', 'source': 'cli'}},
                {'type': 'event_msg', 'timestamp': '2026-01-01T00:00:00Z', 'payload': {'type': 'token_count', 'info': {'total_token_usage': usage}}},
                {'type': 'token_usage_record', 'timestamp': '2026-01-01T00:00:01Z', 'payload': {'session_id': 's', 'thread_id': 's', 'response_id': 'r', 'usage': usage}},
                {'type': 'token_usage_record', 'timestamp': '2026-01-01T00:00:02Z', 'payload': {'session_id': 's', 'thread_id': 's', 'response_id': 'r', 'usage': usage}},
                {'type': 'token_usage_record', 'timestamp': '2026-01-01T00:00:03Z', 'payload': {'session_id': 's', 'thread_id': 's', 'response_id': 'bad', 'usage': {}}},
                {'type': 'token_usage_record', 'timestamp': '2026-01-01T00:00:04Z', 'payload': {'session_id': 's', 'thread_id': 's', 'response_id': 'late', 'usage': usage}},
            ]
            p.write_text('\n'.join(json.dumps(e) for e in events), encoding='utf-8')
            a = met001.extract(Path(directory), 's', '2026-01-01T00:00:04Z')
            self.assertEqual(a['totals']['total_tokens'], 110)
            self.assertEqual(a['totals']['cached_input_tokens'], 40)
            self.assertEqual(a['anomalies']['duplicate_response_id'], 1)
            self.assertEqual(a['anomalies']['incomplete'], 1)
            self.assertEqual(a['ignored_cumulative_events'], 1)
            self.assertEqual(a['by_model']['unknown']['responses'], 1)
            self.assertEqual(a, met001.extract(Path(directory), 's', '2026-01-01T00:00:04Z'))
            self.assertIsNone(a['actual_cost'])
            self.assertIsNone(a['hypothetical_cost'])
            self.assertIn('110', met001.markdown(a))

    def test_conflicting_duplicate_not_counted_as_exact(self):
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / 'e.jsonl'
            u = dict(input_tokens=1, cached_input_tokens=0, cache_write_input_tokens=0, output_tokens=1, reasoning_output_tokens=0, total_tokens=2)
            def event(usage):
                return {'type': 'token_usage_record', 'timestamp': '2026-01-01T00:00:01Z', 'payload': {'session_id': 's', 'thread_id': 's', 'response_id': 'r', 'usage': usage}}
            p.write_text('\n'.join(map(json.dumps, [{'type':'session_meta','payload':{'id':'s'}}, event(u), event({**u,'input_tokens':2,'total_tokens':3})])), encoding='utf-8')
            a = met001.extract(Path(directory), 's', '2026-01-02T00:00:00Z')
            self.assertEqual(a['anomalies']['duplicate_conflicts'], 1)
            self.assertEqual(a['measurement_status'], 'partial')

    def test_unattributed_price_phase_and_identity(self):
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / 'e.jsonl'
            u = dict(input_tokens=100, cached_input_tokens=40, cache_write_input_tokens=0, output_tokens=10, reasoning_output_tokens=3, total_tokens=110)
            events = [
                {'type':'session_meta','payload':{'id':'s','source':{'subagent':{'thread_spawn':{'agent_path':'/root/quality','parent_thread_id':'parent'}}}}},
                {'type':'turn_context','payload':{'turn_id':'t','model':'model-a'}},
                {'type':'token_usage_record','timestamp':'2026-01-01T00:00:01Z','payload':{'session_id':'s','thread_id':'s','response_id':'r','turn_id':'t','usage':u}},
                {'type':'token_usage_record','timestamp':'2026-01-01T00:00:02Z','payload':{'thread_id':'s','response_id':'unattributed','usage':u}},
            ]
            p.write_text('\n'.join(map(json.dumps, events)), encoding='utf-8')
            prices = {'currency':'USD','effective_date':'2026-01-01','source':'test', 'models':{'model-a':{'input':'1','cached_input':'0.1','cache_write_input':'1.25','output':'5'}}}
            phases = [{'name':'test','start':'2026-01-01T00:00:00Z'}]
            a = met001.extract(Path(directory), 's', '2026-01-01T00:01:00Z', phases, prices)
            self.assertEqual(a['anomalies']['unattributable'], 1)
            self.assertEqual(a['measurement_status'], 'partial')
            self.assertEqual(a['phase_windows'][0]['duration_seconds'], 60)
            self.assertEqual(a['thread_identities']['s']['parent_thread_id'], 'parent')
            self.assertEqual(a['hypothetical_cost']['amount'], '0.000114')
            self.assertIsNone(a['actual_cost'])
            prices['models']['model-a'].pop('output')
            b = met001.extract(Path(directory), 's', '2026-01-01T00:01:00Z', phases, prices)
            self.assertEqual(b['hypothetical_cost']['status'], 'partial')
            self.assertEqual(b['hypothetical_cost']['priced_responses'], 0)

    def test_post_cutoff_and_malformed_payload(self):
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / 'e.jsonl'
            events = [{'type':'session_meta','payload':{'id':'s'}},
                      {'type':'token_usage_record','timestamp':'2026-01-02T00:00:00Z','payload':{'thread_id':'s'}},
                      {'type':'token_usage_record','timestamp':'2026-01-01T00:00:01Z','payload':['bad']}]
            p.write_text('\n'.join(map(json.dumps, events)), encoding='utf-8')
            result = met001.extract(Path(directory), 's', '2026-01-01T12:00:00Z')
            self.assertNotIn('unattributable', result['anomalies'])
            self.assertEqual(result['anomalies']['invalid_event'], 1)

    def test_bad_session_metadata_does_not_abort(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'a.jsonl').write_text(json.dumps({'type':'session_meta','payload':[]}), encoding='utf-8')
            (root / 'b.jsonl').write_text(json.dumps({'type':'session_meta','payload':{'id':'s','source':{'subagent':[]}}}), encoding='utf-8')
            result = met001.extract(root, 's', '2026-01-01T12:00:00Z')
            self.assertEqual(result['anomalies']['file_read_errors'], 1)
            self.assertEqual(result['files_scanned'], 1)


if __name__ == '__main__':
    unittest.main()
