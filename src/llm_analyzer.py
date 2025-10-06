import os
import sys
from typing import TextIO
from dotenv import load_dotenv

import google.generativeai as genai

from common.base import BaseAnalyzer


class LLMAnalyzer(BaseAnalyzer):

    def __init__(self):
        super().__init__()
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
        res = self.generate_documentation()
        _output.write(res)
        return res

    def generate_documentation(self) -> str:
        template_path = os.path.join(os.path.dirname(__file__), '../resources/prompt.template')
        template = open(template_path).read()
        prompt =\
            f"""You are a COBOL documentation expert. Analyze the following COBOL program and generate comprehensive documentation in this EXACT format:
        {template}
        
        COBOL CODE TO ANALYZE:
        {self._input}
        

Generate the documentation following the format above EXACTLY. Be thorough and accurate.
"""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating documentation: {str(e)}"