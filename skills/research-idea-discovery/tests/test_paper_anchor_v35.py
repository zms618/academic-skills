"""Synthetic fixtures; NEVER evidence of scientific validity."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from scripts.paper_anchor_audit import assess
from scripts.workflow import main, validate_stage_evidence
from tests.helpers import motivation_fixture
from tests.test_portfolio_v34 import portfolio, gap


def paper_card():
    papers=[]
    for i,role in enumerate(['ANCHOR','BENCHMARK','RIVAL','MECHANISM']):
        papers.append({'paper_id':f'fictional_paper_{i}','title':f'FICTIONAL experiment description {i}',
            'source_url':f'https://example.org/not-real-paper-{i}',
            'role':role,
            'task_protocol':'Fictional multimodal DG task with held-out domains; synthetic test only.',
            'reported_observation':'A fictional source claims some performance difference on unobserved domains.',
            'counterpoint':'This imaginary observation might be caused by unmatched compute and tuning.',
            'reading_depth':'TABLE_LOCATED',
            'evidence_locator':f'FICTIONAL paper Table {i}, not actually read.',
            'code_status':'UNKNOWN', 'dataset_status':'UNKNOWN','checkpoint_status':'UNKNOWN'})
    return {'papers':papers,'problem_lineage':[
        {'problem_id':'fixture_motivation_0','source_paper_ids':['fictional_paper_0','fictional_paper_1'],
         'observed_vs_hypothesized':'Synthetic apparent test performance reversal, not a fact in any real paper.',
         'null_explanation':'An unequal training budget could completely explain an apparent source baseline benefit.',
         'minimal_falsifier':'Repeat the fictional result on matched splits and training budgets using identical seeds.',
         'status':'PROBE_ONLY'}],
        'scope_limits':'All material is synthetic unit-test evidence and cannot be cited as science.',
        'reproduction_first_action':'Inspect the actual paper data and available checkpoints before running any training.'}

class PaperAnchoredV35(unittest.TestCase):
    def test_structural_card_passes_not_science(self):
        x=assess(paper_card());self.assertTrue(x['ready'],x['issues'])
        self.assertIn('not',x['note'].lower());self.assertEqual(4,x['paper_count'])
    def test_abstract_only_is_not_read_papers(self):
        x=paper_card()
        for p in x['papers']:p['reading_depth']='ABSTRACT_LEAD'
        self.assertIn('need_two_located_paper_evidence_units_no_abstract_only_portfolio',assess(x)['issues'])
    def test_missing_locator_breaks_source_evidence(self):
        x=paper_card();x['papers'][1]['evidence_locator']='';self.assertFalse(assess(x)['ready'])
    def test_same_role_echo_chamber_fails(self):
        x=paper_card()
        for p in x['papers']:p['role']='ANCHOR'
        self.assertFalse(assess(x)['ready'])
    def test_no_lineage_fails(self):
        x=paper_card();x['problem_lineage']=[];self.assertFalse(assess(x)['ready'])
    def test_fake_three_contributions_before_motivation_fails(self):
        x=paper_card();x['problem_lineage'][0]['three_contributions']='novel model 1, 2, and 3';self.assertFalse(assess(x)['ready'])
    def test_fabricated_reproduced_checkpoint_without_log_fails(self):
        x=paper_card();x['papers'][0]['checkpoint_status']='WEIGHTS_LOADED';self.assertFalse(assess(x)['ready'])
    def test_apparent_contradiction_requires_comparable_settings(self):
        x=paper_card();x['contradictions']=[{'paper_ids':['fictional_paper_0','fictional_paper_2'],
           'status':'ESTABLISHED','comparability_check':'Different backbones and splits: not comparable.'}]
        self.assertIn('contradiction_0_unmatched_claimed_as_established',assess(x)['issues'])
        x['contradictions'][0]['status']='APPARENT';self.assertTrue(assess(x)['ready'])
    def test_wrong_or_absent_paper_anchors_block_progress(self):
        with tempfile.TemporaryDirectory() as tmp:
            pr=Path(tmp)
            main(['init','--project',tmp,'--goal','CVPR_BEST_PAPER_ASPIRATION',
                  '--discovery-entry','PAPER_ANCHORED'])
            for stage in ('SEARCH','EXPLAIN','MOTIVATION_GATE'):
                self.assertEqual(0,main(['advance','--project',tmp,'--stage',stage,'--reason','synthetic test']))
            self.assertFalse(validate_stage_evidence(pr,'DIVERGE'))
            src=pr/'paper.json';src.write_text(json.dumps(paper_card()))
            self.assertEqual(0,main(['paper-anchors','--project',tmp,'--card',str(src)]))
            card=pr/'motivation_portfolio_card.json';card.write_text(json.dumps(portfolio()))
            self.assertEqual(0,main(['motivation-portfolio','--project',tmp,'--card',str(card)]))
            m0=motivation_fixture();m0['problem_id']='fixture_motivation_0'
            inp=pr/'m0.json';inp.write_text(json.dumps(m0))
            self.assertEqual(0,main(['motivation-gate','--project',tmp,'--card',str(inp)]))
            gp=pr/'gap.json';gp.write_text(json.dumps(gap()))
            self.assertEqual(0,main(['gap-investigation','--project',tmp,'--card',str(gp)]))
            self.assertTrue(validate_stage_evidence(pr,'DIVERGE'))
            self.assertEqual(0,main(['advance','--project',tmp,'--stage','DIVERGE','--reason','paper + portfolio + M0 + gap']))
            original=pr/'paper_anchor_card.json'
            x=json.loads(original.read_text(encoding='utf-8'));x['papers'][0]['reading_depth']='ABSTRACT_LEAD'
            original.write_text(json.dumps(x));self.assertFalse(validate_stage_evidence(pr,'DIVERGE'))
    def test_open_problem_not_forced_to_have_papers(self):
        with tempfile.TemporaryDirectory() as tmp:
            main(['init','--project',tmp,'--goal','multimodal DG','--discovery-entry','OPEN_PROBLEM'])
            st=json.loads((Path(tmp)/'workflow_state.json').read_text(encoding='utf-8'))
            self.assertFalse(st['paper_anchor_required'])
            self.assertEqual('OPEN_PROBLEM',st['discovery_entry'])
    def test_main_source_includes_motivation_and_method_boundaries(self):
        s=(Path(__file__).parent.parent/'skills/research-idea-discovery/SKILL.md').read_text(encoding='utf-8')
        for k in ('paper-lineage-and-critical-reading.md','reproduction-asset-policy.md','research-paper-anchor-scout','M0'):
            self.assertIn(k,s)

if __name__=='__main__':unittest.main()
