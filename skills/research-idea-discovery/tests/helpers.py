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
