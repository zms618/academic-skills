#!/usr/bin/env python3
"""Schema-based usefulness check. Does NOT certify that a method works or that data exist."""
import argparse,json
from pathlib import Path
from advisor_report_check import audit

RUBRIC={
 'understand_problem':lambda x:all(x.get(k) for k in ('plain_language_question','concrete_example','motivation','hypothesis')),
 'separate_contributions':lambda x:isinstance(x.get('potential_contributions'),list) and all(isinstance(z,dict) and z.get('distinguishing_test') and z.get('necessity_ablation') for z in x['potential_contributions']),
 'operational_method':lambda x:isinstance(x.get('method_design'),dict) and all(x['method_design'].get(k) for k in ('decision_rule','weakest_assumption','implementation_limitations')),
 'implementer_entrypoint':lambda x:isinstance(x.get('method_design'),dict) and isinstance(x['method_design'].get('integration'),dict) and bool(x['method_design']['integration'].get('first_function')),
 'data_model_baseline':lambda x:isinstance(x.get('feasibility'),dict) and all(x['feasibility'].get(k) for k in ('dataset','model_checkpoint','baselines','data_access_status','evaluation_protocol')),
 'falsifiable_E0':lambda x:bool(x.get('first_48h')) and bool(x.get('kill_criteria')),
 'three_action_cards':lambda x:isinstance(x.get('action_cards'),list) and len(x['action_cards'])>=3 and all(isinstance(z,dict) and z.get('artifact') for z in x['action_cards']),
 'adversarial_self_review':lambda x:isinstance(x.get('researcher_trial'),dict) and bool(x['researcher_trial'].get('student_blockers')) and bool(x['researcher_trial'].get('reviewer_attacks'))
}
def score(report):
 details={k:bool(test(report)) for k,test in RUBRIC.items()}
 return {'rubric_pass':sum(details.values()),'rubric_total':len(details),'details':details,'schema_issues':audit(report),
 'warning':'Desk/structure utility only. It cannot establish mechanism novelty, working downloads, scientific validity or actual user satisfaction.'}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--output');args=ap.parse_args()
 data=json.loads(Path(args.input).read_text(encoding='utf-8'))
 result=score(data);txt=json.dumps(result,ensure_ascii=False,indent=2)
 if args.output:Path(args.output).write_text(txt,encoding='utf-8')
 print(txt)
 return 0 if result['rubric_pass']==result['rubric_total'] and not result['schema_issues'] else 2
if __name__=='__main__':raise SystemExit(main())
