import json
import pathlib
import tempfile
import unittest
from scripts.literature_search import merge,parse_openalex,parse_crossref,run
from scripts.workflow import check_idea
from scripts.pilot_bridge import run as run_pilot

class Tests(unittest.TestCase):
  def test_records_dedup_doi_and_title(self):
    a=parse_openalex({'results':[{'title':'Some Research Paper','doi':'https://doi.org/10.1/abc','publication_year':2026,'id':'https://openalex.org/W1'}]})
    b=parse_crossref({'message':{'items':[{'title':['Some Research Paper'],'DOI':'10.1/ABC','published':{'date-parts':[[2026]]}}]}})
    out=merge(a+b)
    self.assertEqual(len(out),1)
    self.assertEqual(set(out[0]['source']),{'openalex','crossref'})
    self.assertEqual(out[0]['evidence_level'],'METADATA_ONLY')
  def test_fixture_metadata_remains_unverified(self):
    with tempfile.TemporaryDirectory() as p:
      root=pathlib.Path(p)
      (root/'openalex.json').write_text(json.dumps({'results':[{'title':'Demo Work','id':'W1'}]}))
      (root/'crossref.json').write_text(json.dumps({'message':{'items':[{'title':['Demo Work'],'DOI':'10.2/foo'}]}}))
      result=run('demo',fixture_dir=root)
      self.assertEqual(result['status'],'FIXTURE_ONLY')
      self.assertEqual(len(result['records']),1)
      self.assertFalse(result['records'][0]['claim_checked'])
  def test_gate_fail_closed(self):
    minimal={'idea_id':'X','revision':1,'problem':'P','hypothesis':'H','falsifier':'F','mechanism':'M','unique_prediction':'UP',
    'naive_baseline':'NB','closest_prior_work':[{'title':'X'}], 'pilot':{'kill_signal':'stop'},'sources':[{'evidence_level':'METADATA_ONLY'}],
    'novelty_verdict':'PROVISIONALLY_DIFFERENTIATED','resources_checked':True}
    r=check_idea(minimal)
    self.assertFalse(r['gate_presence']['G5_sources_fulltext'])
    self.assertEqual(r['status'],'EVIDENCE_OR_FIELDS_MISSING')
  def test_pilot_dry_and_executed(self):
    with tempfile.TemporaryDirectory() as p:
      root=pathlib.Path(p)
      d=run_pilot([sys.executable,'-c','print(123)'],root,root/'out',execute=False)
      self.assertEqual(d['status'],'DRY_RUN');self.assertFalse((root/'out'/'stdout.txt').exists())
      a=run_pilot([sys.executable,'-c','print(123)'],root,root/'out',execute=True)
      self.assertEqual(a['status'],'RUN_COMPLETE');self.assertIn('123',(root/'out'/'stdout.txt').read_text(encoding='utf-8'))

import sys
if __name__=='__main__':unittest.main()
