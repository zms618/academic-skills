import json
from pathlib import Path
from scripts.workflow import main

def confirm_dataset_sample(project):
    p=Path(project)
    sample=p/'local_sample.csv';sample.write_text('image,label\nimg001,cat\n',encoding='utf-8')
    license_file=p/'dataset_license.txt';license_file.write_text('Example fixture license record; NOT a real dataset grant.',encoding='utf-8')
    manifest=p/'sample_manifest.json';manifest.write_text(json.dumps({
        'sample_file':str(sample),'license_file':str(license_file),
        'required_fields':['image','label'],'source_url':'https://huggingface.co/datasets/example-research-lab/fixture'}))
    return main(['dataset-verify','--project',str(p),'--manifest',str(manifest)])

def confirm_literature_coverage(project):
    p=Path(project)
    axes=['same_problem','same_mechanism','same_objective','cross_task_equivalent']
    queries=[{'axis':axis,'query':'verified '+axis,'source':'OpenAlex','search_date':'2026-10-08'} for axis in axes]
    record={'queries':queries,'paper_checks':[{'title':'Demonstration only','url':'https://proceedings.mlr.press/',
             'locator':'Method Sec 3','evidence_level':'E3'}]}
    file=p/'search_coverage_manifest.json';file.write_text(json.dumps(record))
    return main(['literature-coverage','--project',str(p),'--manifest',str(file)])


def motivation_fixture():
    """Fictional twin-evidence fixtures: never valid real citations."""
    return {
        'problem_id':'fixture_problem_minimum_2026',
        'task_context':'Multimodal domain generalization classification on held-out domains',
        'scientific_question':'Does matched-control adaptation lose performance compared with empirical risk minimization?',
        'concrete_observation':'Two independent fictional controls report a matched performance reversal.',
        'observable_measure':'Accuracy difference in percent points on held-out domain samples.',
        'baseline_reference':'Frozen ERM baseline and corresponding domain generalization method with matching splits.',
        'problem_importance':'Understanding systematic regression under domain change would improve deployment robustness.',
        'falsification_probe':'If matched runs show no consistent negative difference, abandon the premise.',
        'bounded_probe':'Recompute matched baseline metric on one public sample split; save per-class CSV; no new model.',
        'independence_scope':'Fictional independent sources for the sole purpose of unit tests; not real publications.',
        'alternative_explanations':['Different optimization/tuning budgets produce the apparent difference.',
                                    'Class imbalance across held-out domains changes mean accuracy.'],
        'confounder_checks':['Match backbone and optimizer schedules and repeat random seeds.',
                             'Recompute per-class and macro-averaged accuracy with identical labels.'],
        'evidence':[
          {'evidence_type':'DIRECT_TABLE','source':'fixture://fictional_benchmark_A',
           'locator':'Table 3 fictional experiment','what_observed':'Fictional baseline reversal under matched trial.',
           'independence_key':'fictional_benchmark_A'},
          {'evidence_type':'DIRECT_REPLICATION','source':'fixture://fictional_replication_B',
           'locator':'Appendix B fictional trial','what_observed':'Fictional independent baseline reversal.',
           'independence_key':'fictional_replication_B'},
        ]}

def confirm_motivation_gate(project):
    p=Path(project)
    c=p/'m0-fixture.json';c.write_text(json.dumps(motivation_fixture(),ensure_ascii=False),encoding='utf-8')
    return main(['motivation-gate','--project',str(p),'--card',str(c)])
