import json
import os
import sys
from typing import TextIO, Dict
from dotenv import load_dotenv

import google.generativeai as genai
from common.base import BaseAnalyzer
from common.util import Statement


class LLMAstAnalyzer(BaseAnalyzer):

    def __init__(self):
        super().__init__()
        self.program = None
        api_key = self._prepare()
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-pro')

    @staticmethod
    def _prepare():
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key is None:
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        return api_key

    def document(self, _input: str, _output: TextIO = sys.stdout) -> str:
        self._input = _input
        self.program = self.fetch_program()
        res = self.generate_documentation()
        _output.write(res)
        return res

    def generate_documentation(self) -> str:
        template_path = os.path.join(os.path.dirname(__file__), '../resources/prompt.template')
        template = open(template_path).read()
        ast_dict = self._ast_to_dict()
        ast_json = json.dumps(ast_dict, indent=2)
        prompt = \
            f"""You are a COBOL documentation expert. You are given a parsed Abstract Syntax Tree (AST) of a COBOL program in JSON format. Generate comprehensive documentation in this EXACT format:
        {template}

        AST STRUCTURE (JSON):
        {ast_json}

Analyze the AST structure and generate documentation following the format above EXACTLY. The AST contains:
- program.name: Program identifier
- program.variables: List of variable declarations with level, name, picture, value
- program.paragraphs: List of procedures with statements

Each statement has:
- type: Statement type (MOVE, ADD, COMPUTE, PERFORM, IF, etc.)
- data: Dictionary with statement-specific fields
"""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating documentation: {str(e)}"

    def _ast_to_dict(self) -> Dict:
        return {
            "program_name": self.program.name,
            "variables": [
                {
                    "level": var.level,
                    "name": var.name,
                    "picture": var.picture,
                    "value": var.value
                }
                for var in self.program.variables
            ],
            "procedures": [
                {
                    "name": para.name,
                    "statements": [
                        self._statement_to_dict(stmt)
                        for stmt in para.statements
                    ]
                }
                for para in self.program.paragraphs
            ]
        }

    def _statement_to_dict(self, stmt) -> Dict:
        stmt_dict = {
            "type": stmt.type,
            "data": {}
        }

        for key, value in stmt.data.items():
            if isinstance(value, list):
                stmt_dict["data"][key] = [
                    self._statement_to_dict(s) if isinstance(s, Statement) else s
                    for s in value
                ]
            elif isinstance(value, Statement):
                stmt_dict["data"][key] = self._statement_to_dict(value)
            else:
                stmt_dict["data"][key] = value

        return stmt_dict