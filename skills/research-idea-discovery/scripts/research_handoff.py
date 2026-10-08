#!/usr/bin/env python3
"""Export a context-aware, copyable ChatGPT Deep Research prompt and record return.

NO calls to ChatGPT, Deep Research, browsing, model APIs, or scientific verification.
Only vetted public/context fields are exported; confidential details are opt-in
and deliberately not supported by this CLI.
"""
import argparse
import datetime as dt
import hashlib
import json
import shutil
import sys
from pathlib import Path

MAX_REPORT_SIZE = 5 * 1024 * 1024

def load_json(p):
    return json.loads(Path(p).read_text(encoding='utf-8'))

def store_json(p, value):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def safe_str(v):
    return str(v).strip() if isinstance(v, (str, int, float)) and not isinstance(v, bool) else ''

def string_items(value, limit=12):
    if not isinstance(value, list):
        return []
    return [safe_str(x)[:800] for x in value[:limit] if safe_str(x)]

def assemble_prompt(context, default_domain='OPEN', default_goal='UNSPECIFIED'):
    if not isinstance(context, dict):
        raise ValueError('Context must be an object')
    scope = safe_str(context.get('focus')) or safe_str(context.get('research_question'))
    if not scope:
        raise ValueError('Context requires focus or research_question')
    domain = safe_str(context.get('domain')) or default_domain
    goal = safe_str(context.get('goal')) or default_goal
    questions = string_items(context.get('unresolved_questions'))
    if not questions:
        raise ValueError('Supply at least one specific unresolved_questions item; no generic handoff')
    examined = string_items(context.get('verified_prior_works'))
    ruled_out = string_items(context.get('rejected_ideas'))
    datasets = string_items(context.get('dataset_leads'))
    constraints = string_items(context.get('constraints'))
    queries = string_items(context.get('searched_queries'))
    why = safe_str(context.get('escalation_reason')) or '候选 Idea 未通过审计或关键研究证据不足'
    def lst(items, empty):
        return '\n'.join(f'- {a}' for a in items) if items else f'- {empty}'
    return f'''请使用 ChatGPT 深度研究（Deep Research）对以下研究证据缺口做系统性、可追踪的学术调研。不要为了满足数量要求而制造创新点，不要声称完成未经执行的实验。

【研究目标】
- 领域：{domain}
- 研究范围：{scope}
- 投稿/项目目标：{goal}
- 触发调研的原因：{why}
- 现实约束：优先现有公开/获许可的数据集及其低成本衍生；不从零大规模采集，不依赖昂贵新增人工标注。需要有可执行的评估协议与 Baseline，算力/费用未知时写明未知，不能默认无上限。
{lst(constraints, '尚无更具体的计算/时间限制；评估时不得假设无限预算')}

【已经核查的近邻论文/研究基础，仅作线索，不可假装已经核实全部内容】
{lst(examined, '未确认可靠近邻，请从零检索并记录来源与检索范围')}

【已有检索式/可能的覆盖盲点】
{lst(queries, '检索记录尚未结构化；请主动记录本轮查询与搜索日期')}

【已发现缺陷、撞车或不可行路线，不要改名重提】
{lst(ruled_out, '暂无线索；必须主动构造最强既有方法与简单替代方案')}

【数据集线索（不得凭名称认定可用）】
{lst(datasets, '暂无已核实数据集；请独立发现现有公开数据和低成本可衍生数据')}

【必须优先解决的具体证据问题】
{lst(questions, '无')}

【检索任务】
1. 检索同研究问题、同计算机制、同训练/测试目标，以及跨领域功能等价机制；优先近年真实论文，同时沿引用链追溯经典工作。写明本次检索截至日期、搜索式、筛选准则及覆盖局限，不把未找到等同于不存在。
2. 优先原论文 Method/Experiments/Appendix、官方会议记录、DOI/arXiv、公开代码与作者项目页。找到冲突结论、负面消融、未解释失败、协议差异以及最有威胁的已有方法。
3. 研究可执行性：每个重要方向至少调查一个真实已有/可低成本衍生的数据集候选，给官方地址、可获取性/许可核查状态、模态字段/标签、划分、Baseline、指标方向、模型/代码获取途径、低成本 E0 最小反证实验与资源粗估；不可只报名字。
4. 识别不超过 3–5 个仍值得进一步验证的研究问题簇（若没有就明确为 0），每个都需要已有证据、潜在新假设、最危险近邻、最简单竞争解释、可证伪预测、可用数据候选与主要未知项。不要自动写成已证明创新的论文方法。
5. 说明任何无法获取原论文/无法验证数据许可证或实验成本的项目，并单列 NOT_VERIFIED；不捏造作者、年份、性能、会议与实验结果。

【交付格式】
A. 检索范围、时间戳、查询记录与主要证据局限。
B. Prior-art 对照表：标题、年份、正式发表/预印本状态、DOI/URL、阅读深度、问题、核心机制、监督协议、关键证据与真正局限。
C. Dataset/Code 可行性表：官方链接、授权/许可、必要字段、标注及预算、评测/泄漏风险、Baseline 代码链接、目前核验深度。
D. 直接回答上面每一条缺口问题，分别标 VERIFIED / PARTIALLY_VERIFIED / NOT_VERIFIED，附具体源链接和章节/页码（如果实际获得）。
E. 不重复已有工作的科学机会、最危险反例与最小证伪实验；可选 0 个机会。
F. 仍需核对的文献/数据清单和最值得先做的 3 项低成本验证。

请将结果整理为便于我上传回原 Idea Discovery 插件的 Markdown 报告，并保留可点击来源；不要使用未知的内部用户私密论文内容进行公共搜索。
'''

def export_handoff(project, context_path, out):
    project=Path(project)
    state=load_json(project/'workflow_state.json') if (project/'workflow_state.json').exists() else {}
    ctx=load_json(context_path)
    prompt=assemble_prompt(ctx, state.get('domain', 'OPEN'), state.get('goal', 'UNSPECIFIED'))
    out=Path(out)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(prompt,encoding='utf-8')
    pid=hashlib.sha256(prompt.encode('utf-8')).hexdigest()[:16]
    handoff={'handoff_id':pid,'status':'PENDING_USER_DEEP_RESEARCH','prompt_file':str(out),
             'created_at_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
             'reason':safe_str(ctx.get('escalation_reason')) or 'EVIDENCE_GAP',
             'research_question':safe_str(ctx.get('focus')) or safe_str(ctx.get('research_question')),
             'unresolved_questions':string_items(ctx.get('unresolved_questions')),
             'disclaimer':'Prompt export only. ChatGPT Deep Research has NOT been run.'}
    store_json(project/'research_handoff_state.json',handoff)
    if state:
        state['research_handoff']={'handoff_id':pid,'status':handoff['status']}
        store_json(project/'workflow_state.json',state)
    return handoff

def ingest_report(project, report):
    project=Path(project)
    pending_file=project/'research_handoff_state.json'
    if not pending_file.exists():raise ValueError('No pending handoff: export a prompt first')
    pending=load_json(pending_file)
    if pending.get('status') != 'PENDING_USER_DEEP_RESEARCH':
        raise ValueError('Handoff is not pending')
    report=Path(report)
    if report.suffix.lower() not in ('.md','.txt'):
        raise ValueError('CLI accepts Markdown/text only. For PDF/DOCX, upload to ChatGPT instead')
    if not report.is_file() or report.stat().st_size>MAX_REPORT_SIZE:
        raise ValueError('Report does not exist or exceeds CLI size limit')
    content=report.read_text(encoding='utf-8')
    if len(content.strip())<50:raise ValueError('Report too short to retain as research evidence')
    to=project/'imported_reports'/f"{pending['handoff_id']}.md"
    to.parent.mkdir(parents=True,exist_ok=True)
    if report.resolve()!=to.resolve():shutil.copyfile(report,to)
    pending['status']='RECEIVED_UNVERIFIED'
    pending['report_file']=str(to)
    pending['imported_at_utc']=dt.datetime.now(dt.timezone.utc).isoformat()
    pending['source_sha256']=hashlib.sha256(content.encode('utf-8')).hexdigest()
    pending['disclaimer']='A human/assistant MUST verify primary sources and rerun affected scientific checks. Not automatically a valid Idea.'
    store_json(pending_file,pending)
    fp=project/'workflow_state.json'
    if fp.exists():
        state=load_json(fp)
        state['research_handoff']={'handoff_id':pending['handoff_id'],'status':'RECEIVED_UNVERIFIED'}
        state['evidence_status']='IMPORTED_UNVERIFIED'
        store_json(fp,state)
    return pending

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest='command',required=True)
    e=sub.add_parser('export');e.add_argument('--project',required=True);e.add_argument('--context',required=True);e.add_argument('--out',required=True)
    a=sub.add_parser('ingest');a.add_argument('--project',required=True);a.add_argument('--report',required=True)
    args=p.parse_args(argv)
    try:
        val=export_handoff(args.project,args.context,args.out) if args.command=='export' else ingest_report(args.project,args.report)
    except (OSError,ValueError,json.JSONDecodeError) as exc:
        print(str(exc),file=sys.stderr)
        return 2
    print(json.dumps(val,ensure_ascii=False,indent=2))
    return 0

if __name__=='__main__':sys.exit(main())
