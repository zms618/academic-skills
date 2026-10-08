from tests.helpers import confirm_dataset_sample
import json
import tempfile
import unittest
from pathlib import Path
from scripts.workflow import main
from scripts.dataset_discovery import discover,normalize_hf,normalize_zenodo
from tests.test_dataset_anchor import existing_fixture

class IdeaFirstTests(unittest.TestCase):
    def test_idea_seed_before_dataset_search_is_allowed(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            self.assertEqual(main(['init','--project',d]),0)
            for stage in ('SEARCH','EXPLAIN','DIVERGE','DATA_SEARCH','DATA_ANCHOR'):
                self.assertEqual(main(['advance','--project',d,'--stage',stage,'--reason','idea generated from literature']),0)
            self.assertEqual(json.loads((p/'workflow_state.json').read_text())['stage'],'DATA_ANCHOR')
    def test_dataset_required_after_idea_for_promotion(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            self.assertEqual(main(['init','--project',d]),0)
            for stage in ('SEARCH','EXPLAIN','DIVERGE','DATA_SEARCH','DATA_ANCHOR'):
                self.assertEqual(main(['advance','--project',d,'--stage',stage,'--reason','test']),0)
            with self.assertRaises(SystemExit):
                main(['advance','--project',d,'--stage','FEASIBILITY','--reason','no dataset'])
            a=p/'anchor.json';a.write_text(json.dumps(existing_fixture()))
            self.assertEqual(main(['dataset-anchor','--project',d,'--card',str(a)]),0)
            self.assertEqual(confirm_dataset_sample(d),0)
            self.assertEqual(main(['advance','--project',d,'--stage','FEASIBILITY','--reason','dataset card checked']),0)
            with self.assertRaises(SystemExit):
                main(['advance','--project',d,'--stage','FREEZE','--reason','premature candidate'])
            # G0 explicitly required at freeze; no mistaken candidate promotion.
    def test_hub_search_only_yields_unverified_leads(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            (p/'huggingface.json').write_text(json.dumps([{'id':'demo/visual-benchmark','tags':['image-classification']}]))
            (p/'zenodo.json').write_text(json.dumps({'hits':{'hits':[{'id':123,'metadata':{'title':'Example Dataset'},'links':{'html':'https://zenodo.org/records/123'}}]}}))
            r=discover('multimodal',fixture_dir=p)
            self.assertEqual(r['status'],'FIXTURE_ONLY')
            self.assertEqual(len(r['leads']),2)
            self.assertTrue(all(not x['access_confirmed'] for x in r['leads']))
            self.assertTrue(all(x['evidence']=='CATALOG_METADATA_ONLY' for x in r['leads']))
    def test_malformed_catalog_entries_ignored(self):
        self.assertEqual(normalize_hf([{}, {'id':None}]),[])
        self.assertEqual(normalize_zenodo({'hits':{'hits':[{'metadata':{'title':''}}]}}),[])
    def test_provider_failures_explicit(self):
        with tempfile.TemporaryDirectory() as d:
            r=discover('demo',fixture_dir=d)
            self.assertEqual(r['status'],'FIXTURE_ONLY')
            self.assertEqual(len(r['leads']),0)
            self.assertEqual([x['status'] for x in r['logs']],['ERROR','ERROR'])

if __name__=='__main__':unittest.main()
