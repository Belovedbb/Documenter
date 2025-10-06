import re


class DocumentationMetrics:
    def __init__(self, filepath):
        self.filepath = filepath
        self.content = self._load_file()
        self.info = self._extract_info()

    def _load_file(self):
        with open(self.filepath, 'r', encoding='utf-8') as f:
            return f.read()

    def _extract_info(self):
        info = {
            'procedures': set(),
            'variables': set(),
            'statements_count': 0,
            'purposes': [],
            'data_flows': [],
            'calls': [],
            'total_lines': 0,
            'total_chars': 0
        }

        proc_matches = re.findall(r'PROCEDURE:\s+(\S+)', self.content)
        info['procedures'] = set(proc_matches)

        var_matches = re.findall(r'01\s+(\S+)', self.content)
        info['variables'] = set(var_matches)

        stmt_matches = re.findall(r'Statements\s+\((\d+)\s+total\)', self.content)
        info['statements_count'] = sum(int(x) for x in stmt_matches)

        purpose_matches = re.findall(r'Purpose:\s+(.+?)(?:\n|$)', self.content)
        info['purposes'] = [p.strip() for p in purpose_matches]

        flow_matches = re.findall(r'(\w+)\s+---?\[(?:writes|reads)\]---?>\s+(\w+)', self.content)
        info['data_flows'] = flow_matches

        call_matches = re.findall(r'Calls:\s+(.+?)(?:\n|$)', self.content)
        info['calls'] = call_matches

        info['total_lines'] = len(self.content.split('\n'))
        info['total_chars'] = len(self.content)

        return info

    def completeness_score(self):
        score = 0

        if len(self.info['procedures']) > 0:
            score += 30

        if len(self.info['variables']) > 0:
            score += 20

        if len(self.info['purposes']) > 0:
            score += 25

        if len(self.info['data_flows']) > 0:
            score += 25

        return score

    def detail_richness_score(self):
        score = 0

        if self.info['purposes']:
            avg_purpose_len = sum(len(p) for p in self.info['purposes']) / len(self.info['purposes'])
            # Score up to 40 points (capped at 200 chars avg = max points)
            score += min(40, (avg_purpose_len / 200) * 40)

        score += min(30, len(self.info['data_flows']) * 5)

        score += min(30, len(self.info['calls']) * 5)

        return round(score, 2)

    def structure_score(self):
        score = 0

        sections = [
            'PROGRAM SUMMARY',
            'EXECUTION FLOW',
            'DATA FLOW',
            'PROCEDURE ANALYSIS',
            'VARIABLE REFERENCE'
        ]

        for section in sections:
            if section in self.content:
                score += 20

        return min(100, score)

    def coverage_score(self):
        proc_count = len(self.info['procedures'])
        var_count = len(self.info['variables'])
        score = 0
        score += min(40, proc_count * 10)

        score += min(40, var_count * 10)

        if var_count > 0:
            flow_coverage = len(self.info['data_flows']) / var_count
            score += min(20, flow_coverage * 20)

        return round(score, 2)

    def readability_score(self):
        score = 0

        descriptive_purposes = [p for p in self.info['purposes']
                                if len(p) > 20 and 'data storage' not in p.lower()]

        if self.info['purposes']:
            desc_ratio = len(descriptive_purposes) / len(self.info['purposes'])
            score += desc_ratio * 50

        keywords = ['perform', 'calculate', 'display', 'initialize', 'execute', 'control']
        keyword_count = sum(1 for kw in keywords if kw in self.content.lower())
        score += min(50, keyword_count * 8)

        return round(score, 2)

    def calculate_all_metrics(self):
        return {
            'completeness': self.completeness_score(),
            'detail_richness': self.detail_richness_score(),
            'structure': self.structure_score(),
            'coverage': self.coverage_score(),
            'readability': self.readability_score(),
            'overall': self._calculate_overall()
        }

    def _calculate_overall(self):
        weights = {
            'completeness': 0.25,
            'detail_richness': 0.20,
            'structure': 0.15,
            'coverage': 0.25,
            'readability': 0.15
        }

        scores = {
            'completeness': self.completeness_score(),
            'detail_richness': self.detail_richness_score(),
            'structure': self.structure_score(),
            'coverage': self.coverage_score(),
            'readability': self.readability_score()
        }

        overall = sum(scores[k] * weights[k] for k in weights)
        return round(overall, 2)

    def get_summary(self):
        metrics = self.calculate_all_metrics()
        summary = f"""
{'=' * 70}
DOCUMENTATION QUALITY METRICS: {self.filepath}
{'=' * 70}

Completeness:     {metrics['completeness']:.1f}/100
Detail Richness:  {metrics['detail_richness']:.1f}/100
Structure:        {metrics['structure']:.1f}/100
Coverage:         {metrics['coverage']:.1f}/100
Readability:      {metrics['readability']:.1f}/100

{'=' * 70}
OVERALL SCORE:    {metrics['overall']:.1f}/100
{'=' * 70}

Statistics:
  - Procedures documented: {len(self.info['procedures'])}
  - Variables documented:  {len(self.info['variables'])}
  - Data flows tracked:    {len(self.info['data_flows'])}
  - Purpose descriptions:  {len(self.info['purposes'])}
  - Total lines:           {self.info['total_lines']}
"""
        return summary

if __name__ == "__main__":
    print("Analyzing Static Analyzer Output...")
    static_metrics = DocumentationMetrics('../resources/output/static_add_mul_cal.output')
    print(static_metrics.get_summary())


    print("Analyzing LLM Generated Output...")
    llm_metrics = DocumentationMetrics('../resources/output/llm_add_mul_cal.output')
    print(llm_metrics.get_summary())
