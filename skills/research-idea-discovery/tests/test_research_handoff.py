import pathlib, tempfile, unittest, json
from scripts.research_handoff import assemble_prompt,export_handoff,ingest_report

class HandoffTests(unittest.TestCase):
    def context(self):
        return {'domain':'Multimodal TTA','focus':'reliability under partial shifts',
        'goal':'CVPR','unresolved_questions':['Is a selective router equivalent to prior work?', 'Can public datasets test partial shift?'],
        'rejected_ideas':['Single modality router already studied'],
        'verified_prior_works':['Paper X, 2025, verified URL https://example.org/x'],
        'constraints':['No new labeling; modest compute'],
        'private_notes':['SECRET unpublished theorem']}
    def test_prompt_is_targeted_and_privacy_filtered(self):
        prompt=assemble_prompt(self.context())
        for token in ['Multimodal TTA','CVPR','Is a selective router','No new labeling','VERIFIED / PARTIALLY_VERIFIED / NOT_VERIFIED']:
            self.assertIn(token,prompt)
        self.assertNotIn('SECRET',prompt)
        self.assertIn('低成本',prompt)
    def test_prompt_requires_specific_missing_evidence(self):
        with self.assertRaises(ValueError):assemble_prompt({'focus':'novelty'})
        with self.assertRaises(ValueError):assemble_prompt({'unresolved_questions':['find ideas']})
    def test_export_then_import_is_unverified(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=pathlib.Path(tmp)
            state={'domain':'Multimodal TTA','goal':'CVPR','stage':'SCOOP','history':[]}
            (p/'workflow_state.json').write_text(json.dumps(state))
            context=p/'context.json';context.write_text(json.dumps(self.context()))
            rec=export_handoff(p,context,p/'prompt.md')
            self.assertEqual(rec['status'],'PENDING_USER_DEEP_RESEARCH')
            self.assertEqual(json.loads((p/'workflow_state.json').read_text(encoding='utf-8'))['stage'],'SCOOP')
            report=p/'report.md';report.write_text('Citations and dataset sources must be checked. '*3)
            received=ingest_report(p,report)
            self.assertEqual(received['status'],'RECEIVED_UNVERIFIED')
            state=json.loads((p/'workflow_state.json').read_text(encoding='utf-8'))
            self.assertEqual(state['evidence_status'],'IMPORTED_UNVERIFIED')
            self.assertEqual(state['stage'],'SCOOP') # no auto-advancement
            with self.assertRaises(ValueError):ingest_report(p,report)
    def test_no_fake_research_without_export(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=pathlib.Path(tmp);report=p/'r.md';report.write_text('x'*90)
            with self.assertRaises(ValueError):ingest_report(p,report)
    def test_cli_does_not_claim_research_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=pathlib.Path(tmp);context=p/'ctx.json';context.write_text(json.dumps(self.context()))
            rec=export_handoff(p,context,p/'prompt.md')
            self.assertIn('NOT been run',rec['disclaimer'])

if __name__=='__main__':unittest.main()
