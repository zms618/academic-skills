import copy
import json
import tempfile
import unittest
from pathlib import Path
from scripts.motivation_portfolio import assess_portfolio, assess_gap
from scripts.workflow import main
from tests.helpers import motivation_fixture
from scripts.advisor_report_check import audit


def portfolio():
    motives=[]
    names=['fusion_failure','erm_regression','modality_shortcut','unreliable_subgroups','pretraining_shift','benchmark_transfer']
    for i,n in enumerate(names):
        motives.append({
            'problem_id':f'fixture_motivation_{i}',
            'failure_family':n,
            'task_protocol':'Fictional multimodal classification on several held-out domains.',
            'observed_or_hypothesized_failure':'Fictional comparison indicates a candidate failure worth independently checking.',
            'scientific_importance':'If verified, the failure would challenge a common reliability assumption in unseen domains.',
            'strong_simple_baseline':'Frozen empirical risk minimization with matched encoders and experimental protocol.',
            'null_explanation':'Unmatched hyperparameters or source-domain composition may fully explain it.',
            'falsifier':'Matched seeds and identical source/target splits eliminate the apparent failure.',
            'source_locator':'fixture://fictional_source_'+str(i)+' Table 3 (UNVERIFIED, demonstration only)',
            'cvpr_scope_argument':'Affects robust audio/video recognition with visual representation components.',
            'evidence_status':'HYPOTHESIS_ONLY',
        })
    return {'motivations':motives,'shortlist':[
        {'problem_id':'fixture_motivation_0', 'why_selected_over_rival':'Potentially impacts fusion design more broadly than the benchmark-only alternative.', 'most_dangerous_uncertainty':'Strong frozen unimodal baseline may erase failure under fair controls.'},
        {'problem_id':'fixture_motivation_1','why_selected_over_rival':'A surprising baseline comparison may yield general methodological guidance if confirmed.', 'most_dangerous_uncertainty':'ERM reversal may be caused entirely by unequal tuning effort.'}],
        'search_scope_and_limits':'Synthetic fixture representing a bounded multi-topic scouting search, not an actual literature review.',
        'decision_caveat':'No fictional sample proves scientific significance, venue acceptance, or any Best Paper recognition.'}

def gap():
    findings=[]
    for i,state in enumerate(('SURVIVES_GAP','PROBE_ONLY')):
        findings.append({'problem_id':f'fixture_motivation_{i}',
            'known_explanation':'Existing methods may address some domain shifts, but this synthetic record is not verified.',
            'unresolved_testable_question':'Does the apparent performance reversal survive matching architecture and seeds?',
            'dangerous_simple_rival':'A stronger tuned ERM baseline may already resolve this result.',
            'counterevidence':'We have not independently reproduced the reported failure; outcome is uncertain.',
            'needed_discriminator':'Run identical test partitions and record domain-wise seed confidence intervals.',
            'coverage_limit':'Fictional URL used in a unit test; not a real research gap audit.',
            'status':state,
            'nearest_research':[{'title':'FICTIONAL nearest baseline paper',
                'source_url':'https://example.org/fictional-for-unit-test',
                'actual_method_or_finding':'A baseline result might explain the effect if methodology is controlled.',
                'reading_depth':'NOT_READ; fiction only'}]})
    return {'gap_findings':findings,'focus_problem_id':'fixture_motivation_0',
            'why_focus_over_alternatives':'Problem family zero can produce a cleaner falsifier before the other comparison.'}

class PortfolioV34(unittest.TestCase):
    def test_six_motives_two_shortlisted(self):
        r=assess_portfolio(portfolio())
        self.assertTrue(r['ready'],r['issues']);self.assertEqual(6,r['candidate_count'])
        self.assertEqual(2,len(r['shortlisted_problem_ids']))
    def test_relabelled_motivations_not_six_independent(self):
        p=portfolio()
        for m in p['motivations']:m['failure_family']='all_the_same_question'
        self.assertFalse(assess_portfolio(p)['ready'])
    def test_random_third_module_is_method_first(self):
        p=portfolio();p['motivations'][0]['architecture']='New router'
        self.assertFalse(assess_portfolio(p)['ready'])
    def test_source_unknown_not_verified(self):
        p=portfolio();self.assertTrue(assess_portfolio(p)['ready'])
        self.assertEqual('HYPOTHESIS_ONLY',p['motivations'][0]['evidence_status'])
        self.assertIn('NOT verified',assess_portfolio(p)['note'])
    def test_gap_checks_every_shortlisted_problem(self):
        g=gap(); self.assertTrue(assess_gap(g,assess_portfolio(portfolio()))['ready'])
        g['gap_findings']=g['gap_findings'][:1]
        self.assertFalse(assess_gap(g,assess_portfolio(portfolio()))['ready'])
    def test_already_solved_cannot_be_focus(self):
        g=gap();g['gap_findings'][0]['status']='ALREADY_SOLVED'
        self.assertFalse(assess_gap(g,assess_portfolio(portfolio()))['ready'])
    def test_wrong_single_motive_m0_cannot_cross_focus(self):
        with tempfile.TemporaryDirectory() as tmp:
            project=Path(tmp);main(['init','--project',tmp,'--goal','CVPR_BEST_PAPER_ASPIRATION'])
            for s in ('SEARCH','EXPLAIN','MOTIVATION_GATE'):
                self.assertEqual(0,main(['advance','--project',tmp,'--stage',s,'--reason','synthetic unit test']))
            with self.assertRaises(SystemExit):main(['advance','--project',tmp,'--stage','DIVERGE','--reason','no portfolio'])
            first=project/'motives.json';first.write_text(json.dumps(portfolio()))
            self.assertEqual(0,main(['motivation-portfolio','--project',tmp,'--card',str(first)]))
            m0=motivation_fixture();m0['problem_id']='fixture_motivation_1'
            first_m0=project/'m0.json';first_m0.write_text(json.dumps(m0))
            self.assertEqual(0,main(['motivation-gate','--project',tmp,'--card',str(first_m0)]))
            with self.assertRaises(SystemExit):main(['advance','--project',tmp,'--stage','DIVERGE','--reason','no gap'])
            g=project/'gap.json';g.write_text(json.dumps(gap()))
            with self.assertRaises(SystemExit):main(['gap-investigation','--project',tmp,'--card',str(g)])
            m0['problem_id']='fixture_motivation_0';first_m0.write_text(json.dumps(m0))
            self.assertEqual(0,main(['motivation-gate','--project',tmp,'--card',str(first_m0)]))
            self.assertEqual(0,main(['gap-investigation','--project',tmp,'--card',str(g)]))
            self.assertEqual(0,main(['advance','--project',tmp,'--stage','DIVERGE','--reason','both gates']) )
            p=project/'motivation_portfolio_card.json'
            card=json.loads(p.read_text(encoding='utf-8'));card['motivations'][0]['failure_family']='tampered';p.write_text(json.dumps(card))
            self.assertFalse(__import__('scripts.workflow',fromlist=['validate_stage_evidence']).validate_stage_evidence(project,'DIVERGE'))
    def test_normal_mode_keeps_single_m0(self):
        with tempfile.TemporaryDirectory() as tmp:
            main(['init','--project',tmp,'--goal','Research in materials'])
            st=json.loads((Path(tmp)/'workflow_state.json').read_text(encoding='utf-8'))
            self.assertFalse(st['portfolio_required'])
    def test_cvpr_best_paper_impact_audit_mandatory_at_full_report(self):
        from tests.test_advisor_v31 import good
        r=good();r.update({'protocol_version':'3.4','goal':'CVPR_BEST_PAPER_ASPIRATION',
            'motivation_landscape':'Six research problems, two priorities',
            'shortlisted_gap_reports':'Two references and an unverified gap',
            'gap_status':'PROVISIONAL_GAP_READY',
            'motivation_gate':{'status':'PASS_FOR_IDEATION'},
            'problem_evidence_card':'Two direct fictional observations with M0 probe'})
        self.assertTrue(any('impact review' in x for x in audit(r)))
        r['cvpr_aspiration_review']={k:'Unverified evidence-specific inquiry; no award is assured.' for k in (
            'vision_relevance','scientific_significance','potential_generalizable_insight',
            'closest_conceptual_rival','unique_discriminating_experiment','technical_soundness_risk',
            'expected_real_world_or_field_impact','reproducibility_limitations',
            'bold_hypothesis_falsifier','award_claim_limit')}
        self.assertEqual([],audit(r))
    def test_non_cvpr_portfolio_opt_in(self):
        with tempfile.TemporaryDirectory() as tmp:
            main(['init','--project',tmp,'--goal','NEURIPS','--motivation-mode','PORTFOLIO'])
            self.assertTrue(json.loads((Path(tmp)/'workflow_state.json').read_text(encoding='utf-8'))['portfolio_required'])
    def test_single_question_opt_out(self):
        with tempfile.TemporaryDirectory() as tmp:
            main(['init','--project',tmp,'--goal','CVPR_BEST_PAPER_ASPIRATION','--motivation-mode','SINGLE'])
            self.assertFalse(json.loads((Path(tmp)/'workflow_state.json').read_text(encoding='utf-8'))['portfolio_required'])
    def test_report_portfolio_no_innovations_before_shortlist(self):
        c={'protocol_version':'3.4','report_phase':'MOTIVATION_PORTFOLIO','status':'NEEDS_EVIDENCE',
            'action':'RESEARCH_MORE','motivation_landscape':'Six candidate scientific questions and limits',
            'source_coverage':'Mixed hypothetical and located sources',
            'comparative_shortlist':'Two high-risk shortlist candidates','counterevidence':'Confounds remain in all tests',
            'next_evidence_action':'Verify published tables and fair conditions'}
        self.assertEqual([],audit(c))
        c['potential_contributions']=[{'claim':'a made-up model'}]
        self.assertTrue(any('premature' in x for x in audit(c)))

if __name__=='__main__':unittest.main()
