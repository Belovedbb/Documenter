import sys
from typing import List, TextIO
import re
from common.base import BaseAnalyzer
from common.util import Variable, Statement

class StaticAnalyzer(BaseAnalyzer):
    def __init__(self):
        super().__init__()
        self.program = None
        self.var_usage = {}
        self.call_graph = {}
        self.dataflow = {}
        self.execution_flow = []

    def document(self, _input: str, _output: TextIO = sys.stdout) -> str:
        self._input = _input
        self.program = self.fetch_program()
        self.analyze()
        res = self.generate_documentation()
        _output.write(res)
        return res

    def analyze(self):
        self._init_variables()
        self._analyze_procedures()
        self._build_call_graph()
        self._trace_execution()
        self._analyze_dataflow_links()

    def _init_variables(self):
        for var in self.program.variables:
            self.var_usage[var.name] = {
                'definition': var,
                'reads': set(),
                'writes': set(),
                'purpose': self._infer_variable_purpose(var)
            }

    def _infer_variable_purpose(self, var: Variable) -> str:
        return "Data storage"

    def _analyze_procedures(self):
        for para in self.program.paragraphs:
            for stmt in para.statements:
                self._analyze_statement(stmt, para.name)

    def _analyze_statement(self, stmt: Statement, para_name: str):
        if stmt.type == 'MOVE':
            self._record_read(stmt.data['source'], para_name)
            self._record_write(stmt.data['target'], para_name)
        elif stmt.type == 'ADD':
            self._record_read(stmt.data['operand1'], para_name)
            self._record_read(stmt.data['operand2'], para_name)
            self._record_write(stmt.data['target'], para_name)
        elif stmt.type == 'SUBTRACT':
            self._record_read(stmt.data['operand1'], para_name)
            self._record_read(stmt.data['operand2'], para_name)
            self._record_write(stmt.data['target'], para_name)
        elif stmt.type == 'MULTIPLY':
            self._record_read(stmt.data['operand1'], para_name)
            self._record_read(stmt.data['operand2'], para_name)
            self._record_write(stmt.data['target'], para_name)
        elif stmt.type == 'COMPUTE':
            self._record_write(stmt.data['target'], para_name)
            for var in re.findall(r'[A-Za-z][A-Za-z0-9\-]*', stmt.data['expression']):
                self._record_read(var, para_name)
        elif stmt.type == 'DISPLAY':
            self._record_read(stmt.data['item'], para_name)
        elif stmt.type == 'IF':
            for var in re.findall(r'[A-Za-z][A-Za-z0-9\-]*', stmt.data['condition']):
                self._record_read(var, para_name)
            for s in stmt.data.get('then', []):
                self._analyze_statement(s, para_name)
            for s in stmt.data.get('else', []):
                self._analyze_statement(s, para_name)

    def _build_call_graph(self):
        for para in self.program.paragraphs:
            self.call_graph[para.name] = {
                'calls': set(),
                'called_by': set()
            }

        for para in self.program.paragraphs:
            for stmt in para.statements:
                if stmt.type == 'PERFORM':
                    target = stmt.data['target']
                    self.call_graph[para.name]['calls'].add(target)
                    if target in self.call_graph:
                        self.call_graph[target]['called_by'].add(para.name)

    def _trace_execution(self):
        if not self.program.paragraphs:
            return

        visited = set()
        self._trace_from_paragraph(self.program.paragraphs[0].name, visited, 0)

    def _trace_from_paragraph(self, para_name: str, visited: set, depth: int):
        if para_name in visited or depth > 10:
            return

        visited.add(para_name)
        self.execution_flow.append((depth, para_name))

        if para_name in self.call_graph:
            for called in self.call_graph[para_name]['calls']:
                self._trace_from_paragraph(called, visited, depth + 1)

    def _analyze_dataflow_links(self):
        for var_name in self.var_usage:
            writers = self.var_usage[var_name]['writes']
            readers = self.var_usage[var_name]['reads']

            for writer in writers:
                for reader in readers:
                    if writer != reader:
                        key = (writer, reader, var_name)
                        self.dataflow[key] = {
                            'from': writer,
                            'to': reader,
                            'variable': var_name
                        }

    def _record_read(self, var: str, location: str):
        if var in self.var_usage:
            self.var_usage[var]['reads'].add(location)

    def _record_write(self, var: str, location: str):
        if var in self.var_usage:
            self.var_usage[var]['writes'].add(location)

    def _generate_program_summary(self) -> List[str]:
        lines = []
        lines.append("\nPROGRAM SUMMARY")
        lines.append("=" * 80)

        main_para = self.program.paragraphs[0].name if self.program.paragraphs else "UNKNOWN"
        lines.append(f"\nMain Entry Point: {main_para}")

        total_stmts = sum(len(p.statements) for p in self.program.paragraphs)
        lines.append(f"Total Statements: {total_stmts}")
        lines.append(f"Total Procedures: {len(self.program.paragraphs)}")
        lines.append(f"Total Variables: {len(self.program.variables)}")

        lines.append("\nProgram Purpose Analysis:")

        computed_vars = [v for v in self.var_usage if self.var_usage[v]['writes']]
        if computed_vars:
            lines.append("\nKey Output Variables:")
            for var in computed_vars:
                purpose = self.var_usage[var]['purpose']
                lines.append(f"  - {var}: {purpose}")

        return lines

    def _generate_execution_trace(self) -> List[str]:
        lines = []
        lines.append("\nEXECUTION FLOW TRACE")
        lines.append("=" * 80)
        lines.append("\nProgram execution follows this call sequence:")
        lines.append("")

        for depth, para_name in self.execution_flow:
            indent = "  " * depth
            arrow = "|--->" if depth > 0 else ">"
            lines.append(f"{indent}{arrow} {para_name}")

        return lines

    def _generate_data_linkage(self) -> List[str]:
        lines = []
        lines.append("\nDATA LINKAGE ANALYSIS")
        lines.append("=" * 80)
        lines.append("\nShowing how data flows between procedures:")
        lines.append("")

        var_flows = {}
        for key, flow in self.dataflow.items():
            var = flow['variable']
            if var not in var_flows:
                var_flows[var] = []
            var_flows[var].append((flow['from'], flow['to']))

        for var, flows in sorted(var_flows.items()):
            lines.append(f"\n{var}:")
            purpose = self.var_usage[var]['purpose']
            lines.append(f"  Purpose: {purpose}")
            lines.append(f"  Data Flow:")
            for from_proc, to_proc in flows:
                lines.append(f"    {from_proc} --->[writes]---> {var} ----[reads]----> {to_proc}")
        return lines

    def _generate_procedure_details(self) -> List[str]:
        lines = []
        lines.append("\nDETAILED PROCEDURE ANALYSIS")
        lines.append("=" * 80)

        for para in self.program.paragraphs:
            lines.append(f"\n{'--' * 80}")
            lines.append(f"PROCEDURE: {para.name}")
            lines.append('--' * 80)

            name_upper = para.name.upper()
            if 'INIT' in name_upper:
                lines.append("Purpose: Initialize variables and setup")
            elif 'CALC' in name_upper or 'COMPUTE' in name_upper:
                lines.append("Purpose: Perform calculations")
            elif 'PROCESS' in name_upper:
                lines.append("Purpose: Main processing logic")
            elif 'DISPLAY' in name_upper or 'SHOW' in name_upper:
                lines.append("Purpose: Output results")
            elif 'MAIN' in name_upper:
                lines.append("Purpose: Main control flow")

            if para.name in self.call_graph:
                calls = self.call_graph[para.name]['calls']
                called_by = self.call_graph[para.name]['called_by']

                if called_by:
                    lines.append(f"Called by: {', '.join(sorted(called_by))}")
                if calls:
                    lines.append(f"Calls: {', '.join(sorted(calls))}")

            reads = set()
            writes = set()
            for var_name, usage in self.var_usage.items():
                if para.name in usage['reads']:
                    reads.add(var_name)
                if para.name in usage['writes']:
                    writes.add(var_name)

            if reads:
                lines.append(f"\nInput Variables (reads): {', '.join(sorted(reads))}")
            if writes:
                lines.append(f"Output Variables (writes): {', '.join(sorted(writes))}")

            lines.append(f"\nStatements ({len(para.statements)} total):")
            for i, stmt in enumerate(para.statements, 1):
                if stmt.type == 'MOVE':
                    lines.append(f"  {i}. MOVE {stmt.data['source']} TO {stmt.data['target']}")
                elif stmt.type in ['ADD', 'SUBTRACT', 'MULTIPLY']:
                    op1, op2, tgt = stmt.data['operand1'], stmt.data['operand2'], stmt.data['target']
                    lines.append(f"  {i}. {stmt.type} {op1} and {op2} -> {tgt}")
                elif stmt.type == 'COMPUTE':
                    lines.append(f"  {i}. COMPUTE {stmt.data['target']} = {stmt.data['expression']}")
                elif stmt.type == 'PERFORM':
                    target = stmt.data['target']
                    if 'until' in stmt.data:
                        lines.append(f"  {i}. PERFORM {target} UNTIL {stmt.data['until']}")
                    else:
                        lines.append(f"  {i}. PERFORM {target}")
                elif stmt.type == 'IF':
                    lines.append(f"  {i}. IF {stmt.data['condition']}")
                elif stmt.type == 'DISPLAY':
                    lines.append(f"  {i}. DISPLAY {stmt.data['item']}")
                else:
                    lines.append(f"  {i}. {stmt.type}")

        return lines

    def _generate_visual_graph(self) -> List[str]:
        lines = []
        lines.append("\nVISUAL CALL GRAPH")
        lines.append("=" * 80)
        lines.append("\nPROCEDURE CALL HIERARCHY")
        lines.append("")

        if self.program.paragraphs:
            self._draw_call_tree(self.program.paragraphs[0].name, lines, "", set())

        lines.append("\nDATA FLOW DIAGRAM")
        lines.append("")

        for para in self.program.paragraphs:
            writes = [v for v in self.var_usage if para.name in self.var_usage[v]['writes']]
            if writes:
                lines.append(f"[{para.name}]")
                for var in writes[:3]:
                    lines.append(f"    |")
                    lines.append(f"    |----> {var}")
                lines.append("")

        return lines

    def _draw_call_tree(self, para_name: str, lines: List[str], prefix: str, visited: set):
        if para_name in visited:
            lines.append(f"{prefix}|-- {para_name} (already shown)")
            return

        visited.add(para_name)
        lines.append(f"{prefix}|-- {para_name}")

        if para_name in self.call_graph:
            calls = sorted(self.call_graph[para_name]['calls'])
            for i, called in enumerate(calls):
                is_last = (i == len(calls) - 1)
                new_prefix = prefix + ("   " if is_last else "|  ")
                self._draw_call_tree(called, lines, new_prefix, visited)

    def generate_documentation(self) -> str:
        lines = []
        lines.append("=" * 80)
        lines.append(f"COBOL PROGRAM DOCUMENTATION: {self.program.name}")
        lines.append("=" * 80)

        lines.extend(self._generate_program_summary())
        lines.extend(self._generate_execution_trace())
        lines.extend(self._generate_visual_graph())
        lines.extend(self._generate_data_linkage())
        lines.extend(self._generate_procedure_details())

        lines.append("\n\nVARIABLE REFERENCE")
        lines.append("=" * 80)
        for var in self.program.variables:
            lines.append(f"\n{var.level:02d} {var.name}")
            if var.picture:
                lines.append(f"    PIC: {var.picture}")
            if var.value:
                lines.append(f"    VALUE: {var.value}")
            if var.name in self.var_usage:
                lines.append(f"    Purpose: {self.var_usage[var.name]['purpose']}")

        lines.append("\n" + "=" * 80)
        lines.append("END OF DOCUMENTATION")
        lines.append("=" * 80)
        return "\n".join(lines)