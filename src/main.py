import os
import sys
from os import mkdir
from typing import List, Dict

from metrics import DocumentationMetrics
from common.base import BaseAnalyzer
from common.util import read_file
from llm_analyzer import LLMAnalyzer
from llm_ast_analyzer import LLMAstAnalyzer
from static_analyzer import StaticAnalyzer

files_to_test: List = ['payroll']
dict_analyzer: Dict[str, 'BaseAnalyzer'] = {'static': StaticAnalyzer(), 'llm': LLMAnalyzer(), 'llm_ast': LLMAstAnalyzer()}
INPUT_PATH_TEMPLATE = '../resources/input/{}.cbl'
OUTPUT_PATH_TEMPLATE = '../resources/output/{}_{}.output'

def ensure_exist(file_path: str):
    if not os.path.isfile(file_path):
        mkdir(file_path)

if __name__ == '__main__':
    for file_name in files_to_test:
        for analyzer_name in dict_analyzer:
            try:
                input_: str = os.path.join(os.path.dirname(__file__), INPUT_PATH_TEMPLATE.format(file_name))
                output_: str = os.path.join(os.path.dirname(__file__), OUTPUT_PATH_TEMPLATE.format(analyzer_name, file_name))
                with open(output_, "w", encoding="utf-8") as f:
                    print(f'Analyzer {analyzer_name} started for file {file_name}...')
                    dict_analyzer[analyzer_name].document(read_file(input_), f)
                    metrics = DocumentationMetrics(output_)
                    print(metrics.get_summary())
            except Exception as e:
                print("Something went wrong!")
