
<p align="center"><h1 align="center">MAINFRAME DOCUMENTER</h1></p>
<p align="center">
	<em><code>❯ A poc comparison between static documenter, natural llm and ast token llm</code></em>
</p>
<p align="center">
	<img src="https://img.shields.io/github/last-commit/Belovedbb/Documenter?style=default&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/Belovedbb/Documenter?style=default&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/Belovedbb/Documenter?style=default&color=0080ff" alt="repo-language-count">
</p>
<p align="center"><!-- default option, no dependency badges. -->
</p>
<p align="center">
	<!-- default option, no dependency badges. -->
</p>
<br>

##  Table of Contents

- [ Overview](#-overview)
- [ Features](#-features)
- [ Project Structure](#-project-structure)
  - [ Project Index](#-project-index)
- [ Getting Started](#-getting-started)
  - [ Prerequisites](#-prerequisites)
  - [ Installation](#-installation)
  - [ Usage](#-usage)
  - [ Testing](#-testing)
- [ Project Roadmap](#-project-roadmap)
- [ Contributing](#-contributing)
- [ License](#-license)
- [ Acknowledgments](#-acknowledgments)

---

##  Overview

<code>❯ This is a poc that shows how to build a documenter for the sake of studying optimal ways of generating and summarizing cobol code snippets.</code>

---

##  Features

- <code>❯ Parse and output minimal cobol ast </code>
- <code>❯ Use a static analyzer for summarization</code>
- <code>❯ Use an llm for code summarization</code>
- <code>❯ Use ast token as llm input for code summarization</code>
- <code>❯ Give casual metrics on the output</code>

---

##  Project Structure

```sh
└── Documenter/
    ├── requirements.txt
    ├── resources
    │   ├── input
    │   └── prompt.template
    ├── rules.ebnf
    └── src
        ├── common
        ├── llm_analyzer.py
        ├── llm_ast_analyzer.py
        ├── main.py
        ├── metrics.py
        └── static_analyzer.py
```


###  Project Index
<details open>
	<summary><b><code>DOCUMENTER/</code></b></summary>
	<details> <!-- __root__ Submodule -->
		<summary><b>__root__</b></summary>
		<blockquote>
			<table>
			<tr>
				<td><b><a href='https://github.com/Belovedbb/Documenter/blob/master/requirements.txt'>requirements.txt</a></b></td>
				<td><code>❯ Packages to be installed</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/Belovedbb/Documenter/blob/master/rules.ebnf'>rules.ebnf</a></b></td>
				<td><code>❯ cobol ebnf rules</code></td>
			</tr>
			</table>
		</blockquote>
	</details>
	<details> <!-- src Submodule -->
		<summary><b>src</b></summary>
		<blockquote>
			<table>
			<tr>
				<td><b><a href='https://github.com/Belovedbb/Documenter/blob/master/src/llm_ast_analyzer.py'>llm_ast_analyzer.py</a></b></td>
				<td><code>❯ an llm summarizer that takes ast as a token</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/Belovedbb/Documenter/blob/master/src/main.py'>main.py</a></b></td>
				<td><code>❯ main entry point</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/Belovedbb/Documenter/blob/master/src/metrics.py'>metrics.py</a></b></td>
				<td><code>❯ shows main summary of the documentation generated</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/Belovedbb/Documenter/blob/master/src/static_analyzer.py'>static_analyzer.py</a></b></td>
				<td><code>❯ static analyzer that makes use of parsed ast for documentation</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/Belovedbb/Documenter/blob/master/src/llm_analyzer.py'>llm_analyzer.py</a></b></td>
				<td><code>❯ an llm summarizer that takes natural words as a token</code></td>
			</tr>
			</table>
		</blockquote>
	</details>
</details>

---
##  Getting Started

###  Prerequisites

Before getting started with Documenter, ensure your runtime environment meets the following requirements:

- **Programming Language:** Python
- **Package Manager:** Pip


###  Installation

Install Documenter using one of the following methods:

**Build from source:**

1. Clone the Documenter repository:
```sh
❯ git clone https://github.com/Belovedbb/Documenter
```

2. Navigate to the project directory:
```sh
❯ cd Documenter
```

3. Install the project dependencies:

**Using `pip`** &nbsp; [<img align="center" src="https://img.shields.io/badge/Pip-3776AB.svg?style={badge_style}&logo=pypi&logoColor=white" />](https://pypi.org/project/pip/)

```sh
❯ pip install -r requirements.txt
```

###  Usage
Run Documenter using the following command:
**Using `pip`** &nbsp; [<img align="center" src="https://img.shields.io/badge/Pip-3776AB.svg?style={badge_style}&logo=pypi&logoColor=white" />](https://pypi.org/project/pip/)

```sh
❯ python main.py
```

---