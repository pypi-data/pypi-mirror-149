# -*- coding: utf-8 -*-
"""
Parsers accept linter output and return file paths and all of the violations in that file.
"""
import collections
import json
import os
import re

from unidiff import PatchSet

from .violations import Violation


class BaseLintParser(object):

    def parse_violations(self, output):
        raise NotImplementedError

    def _get_working_dir(self):
        return os.getcwd()

    def _normalize_path(self, path):
        """
        Normalizes a file path so that it returns a path relative to the root repo directory.
        """
        # Override the file/path provided by the tool with what is provided
        #   in an environment variable.
        # Useful when the linter tool does not provide a full path and filename.
        # Super-linter can override the tool and provide the information.
        env_path = os.environ.get("LINTLY_FILE_OVERRIDE", None)
        if env_path:
            path = env_path

        norm_path = os.path.normpath(path)
        return os.path.relpath(norm_path, start=self._get_working_dir())

    def _constuct_pr_message(self, linter_message, inline_ignore_message=None):
        pr_message = linter_message
        if inline_ignore_message:
            pr_message += (
                '\n'
                '***'  # Horizontal line separator
                '\n'
                f'{inline_ignore_message}'
            )
        return pr_message


class LineRegexParser(BaseLintParser):
    """
    A parser that runs a regular expression on each line of the output to return violations.
    The regex should match the following capture groups:

        - path
        - line
        - column
        - code
        - message
    """

    def __init__(self, regex):
        self.regex = regex

    @staticmethod
    def _get_from_match(match, key, not_found_value=None):
        if key in match.groupdict():
            return match.group(key)
        return not_found_value

    def parse_violations(self, output):
        violations = collections.defaultdict(list)

        line_regex = re.compile(self.regex)

        # Collect all the issues into a dict where the keys are the file paths and the values are a
        # list of the issues in that file.
        for line in output.strip().splitlines():
            clean_line = line.strip()

            match = line_regex.match(clean_line)

            if not match:
                continue

            path = self._normalize_path(LineRegexParser._get_from_match(match, "path"))
            code = LineRegexParser._get_from_match(match, "code", "")
            message = LineRegexParser._get_from_match(match, "message", "")

            # report the findings at beginning of file if no line numbers are given
            line = int(LineRegexParser._get_from_match(match, "line", 0))
            # column numbers do not matter for reporting logic; default to 0
            column = int(LineRegexParser._get_from_match(match, "column", 0))

            violation = Violation(
                line=line,
                column=column,
                code=code,
                message=message
            )

            violations[path].append(violation)

        return violations


class PylintJSONParser(BaseLintParser):
    """
    Pylint JSON format:

        [
            {
                "type": "convention",
                "module": "lintly.backends.base",
                "obj": "BaseGitBackend.post_status",
                "line": 54,
                "column": 4,
                "path": "lintly/backends/base.py",
                "symbol": "missing-docstring",
                "message": "Missing method docstring",
                "message-id": "C0111"
            }
        ]
    """

    def parse_violations(self, output):
        # Sometimes pylint will output "No config file found, using default configuration".
        # This handles that case by removing that line.
        if output and output.startswith('No config'):
            output = '\n'.join(output.splitlines()[1:])

        output = output.strip()
        if not output:
            return dict()

        json_data = json.loads(output)

        violations = collections.defaultdict(list)

        for violation_json in json_data:
            violation = Violation(
                line=violation_json['line'],
                column=violation_json['column'],
                code='{} ({})'.format(violation_json['message-id'], violation_json['symbol']),
                message=violation_json['message']
            )

            path = self._normalize_path(violation_json['path'])
            violations[path].append(violation)

        return violations


class ESLintParser(BaseLintParser):

    def parse_violations(self, output):
        violations = collections.defaultdict(list)

        current_file = None

        # Collect all the issues into a dict where the keys are the file paths and the values are a
        # list of the issues in that file.
        for line in output.strip().splitlines():
            if line.startswith(' '):
                # This line is a linting violation
                regex = r'^(?P<line>\d+):(?P<column>\d+)\s+(error|warning)\s+(?P<message>.*)\s+(?P<code>.+)$'
                match = re.match(regex, line.strip())

                violation = Violation(
                    line=int(match.group('line')),
                    column=int(match.group('column')),
                    code=match.group('code').strip(),
                    message=match.group('message').strip()
                )
                violations[current_file].append(violation)
            elif line.startswith('✖'):
                # We're at the end of the file
                break
            else:
                # This line is a file path
                current_file = self._normalize_path(line)

        return violations


class StylelintParser(BaseLintParser):

    def parse_violations(self, output):
        violations = collections.defaultdict(list)

        current_file = None

        # Collect all the issues into a dict where the keys are the file paths and the values are a
        # list of the issues in that file.
        for line in output.strip().splitlines():
            if line.startswith(' '):
                # This line is a linting violation
                regex = r'^(?P<line>\d+):(?P<column>\d+)\s+✖\s+(?P<message>.*)\s+(?P<code>.+)$'
                match = re.match(regex, line.strip())

                violation = Violation(
                    line=int(match.group('line')),
                    column=int(match.group('column')),
                    code=match.group('code').strip(),
                    message=match.group('message').strip()
                )
                violations[current_file].append(violation)
            else:
                # This line is a file path
                current_file = self._normalize_path(line)

        return violations


class BlackParser(BaseLintParser):
    """A parser for the `black [source] --diff --check` command."""

    MESSAGE_FORMAT = (
        "This code block needs to be reformatted.\n\n"
        "<details><summary>Expand to show diff</summary>\n\n"
        "```\n"
        "{hunk}\n"
        "```\n"
        "</details>\n")

    def parse_violations(self, output):
        violations = collections.defaultdict(list)
        for changed_file in PatchSet(output, metadata_only=False):
            path = changed_file.source_file
            for hunk in changed_file:
                violation = Violation(
                    line=hunk.source_start,
                    column=0,
                    code="`black`",
                    message=self.MESSAGE_FORMAT.format(hunk=str(hunk)))
                violations[path].append(violation)
        return violations


class CfnLintParser(BaseLintParser):
    """A parser for the `cfn-lint` command.

      cfn-lint output example:

      W2001 Parameter UnusedParameter not used.
      template.yaml:2:9
    """

    def parse_violations(self, output):
        violations = collections.defaultdict(list)

        regex = re.compile(r"[EW]\d{4}\s")

        next_line_is_path = False
        current_violation = None
        for line in output.strip().splitlines():
            if regex.match(line):
                # This line is a cfn-lint error or warning
                next_line_is_path = True
                current_violation = line
            elif next_line_is_path:
                # This line is a filepath:line_number:column_number
                path, line_number, column = line.split(":")
                path = self._normalize_path(path)

                code, message = current_violation.split(" ", 1)

                violation = Violation(line=int(line_number),
                                      column=int(column),
                                      code=code,
                                      message=message)
                violations[path].append(violation)

                next_line_is_path = False
                current_violation = None

        return violations


class BanditJSONParser(BaseLintParser):
    """
    Bandit JSON format:

      [
          {
              "errors": [],
              "generated_at": "2021-01-07T23:39:39Z",
              "metrics": {
                  "./lintly/formatters.py": {
                      "CONFIDENCE.HIGH": 1.0,
                      "CONFIDENCE.LOW": 0.0,
                      "CONFIDENCE.MEDIUM": 0.0,
                      "CONFIDENCE.UNDEFINED": 0.0,
                      "SEVERITY.HIGH": 1.0,
                      "SEVERITY.LOW": 0.0,
                      "SEVERITY.MEDIUM": 0.0,
                      "SEVERITY.UNDEFINED": 0.0,
                      "loc": 31,
                      "nosec": 0
                      },
              "results": [
                  {
                      "code": "13 \n14 env = Environment(\n15 loader=FileSystemLoader(TEMPLATES_PATH),
                                  \n16 autoescape=False\n17 )\n",
                      "filename": "./lintly/formatters.py",
                      "issue_confidence": "HIGH",
                      "issue_severity": "HIGH",
                      "issue_text": "Using jinja2 templates with autoescape=False is dangerous and can lead to XSS."
                                    "Use autoescape=True or use the select_autoescape function.",
                      "line_number": 14,
                      "line_range": [
                          14,
                          15,
                          16
                          ],
                     "more_info": "https://bandit.readthedocs.io/en/latest/plugins/b701_jinja2_autoescape_false.html",
                     "test_id": "B701"
                     "test_name": "jinja2_autoescape_false"
                }
            ]
         }
     ]

    """

    ignore_instructions = (
        'Add a `# nosec` comment to this line to silence this alert. '
        '([Bandit documentation](https://bandit.readthedocs.io/en/latest/config.html#suppressing-individual-lines))'
    )

    def parse_violations(self, output):

        output = output.strip()
        if not output:
            return dict()

        json_data = json.loads(output)

        violations = collections.defaultdict(list)
        linter_violations = json_data.get("results", []) or []
        for violation_json in linter_violations:
            violation = Violation(
                line=violation_json["line_number"],
                column=0,
                code="{} ({})".format(
                    violation_json["test_id"], violation_json["test_name"]
                ),
                message=self._constuct_pr_message(
                    violation_json["issue_text"], self.ignore_instructions
                )
            )

            path = self._normalize_path(violation_json["filename"])
            violations[path].append(violation)

        return violations


class CfnNagParser(BaseLintParser):

    ignore_instructions_format = (
        'To silence this alert, add a `Metadata` block to this resource. '
        '([cfn_nag documentation](https://github.com/stelligent/cfn_nag#per-resource-rule-suppression))'
        '\n\n'
        '<details><summary>Expand to show example</summary>\n\n'
        '```\n'
        'Metadata:\n'
        '  cfn_nag:\n'
        '    rules_to_suppress:\n'
        '    - id: {rule_id}\n'
        '      reason: "Your reason here"\n'
        '    - id: <another_rule_id>\n'
        '      reason: "Your reason here"\n'
        '```\n'
        '</details>\n'
    )

    def parse_violations(self, output):

        file_list = json.loads(output)
        violations = {}

        for file in file_list:
            file_violations = []
            linter_violations = file.get("file_results", {}).get("violations", []) or []
            for violation_info in linter_violations:
                for line_number in violation_info["line_numbers"]:
                    violation = Violation(
                        line=line_number,
                        column=0,
                        code=violation_info["id"],
                        message=self._constuct_pr_message(
                            violation_info["message"],
                            self.ignore_instructions_format.format(rule_id=violation_info["id"])
                        )
                    )

                    file_violations.append(violation)

            path = self._normalize_path(file["filename"])
            violations[path] = file_violations

        return violations


class GitLeaksParser(BaseLintParser):
    """
    Gitleaks JSON format

        {
            "line": "-----BEGIN PRIVATE KEY-----",
            "lineNumber": 59,
            "offender": "-----BEGIN PRIVATE KEY-----",
            "commit": "111111111111111111111000000000",
            "repo": ".",
            "repoURL": "",
            "leakURL": "",
            "rule": "Asymmetric Private Key",
            "commitMessage": "any commit message \n",
            "author": "bob s",
            "email": "bob@example.com",
            "file": "relative/path/to/output",
            "date": "2020-04-14T15:17:53-07:00",
            "tags": "key, AsymmetricPrivateKey"
        }

    """

    ignore_instructions = (
        'Add a `# nosec` comment to this line to silence this alert. '
        '([gitleaks config](https://github.com/23andMe/super-linter/blob/main/TEMPLATES/.gitleaks.toml#L171))'
    )

    def parse_violations(self, output):
        if not output:
            return dict()

        json_data = json.loads(output)

        violations = collections.defaultdict(list)
        for violation_data in json_data:
            violation = Violation(
                line=violation_data["lineNumber"],
                column=0,
                code=violation_data["offender"],
                message=self._constuct_pr_message(
                    violation_data["rule"], self.ignore_instructions
                )
            )

            path = self._normalize_path(violation_data['file'])
            violations[path].append(violation)

        return violations


class HadolintParser(BaseLintParser):
    """
    Hadolint JSON format

       {
            "line": 20,
            "code": "DL3020",
            "message": "Use COPY instead of ADD for files and folders",
            "column": 1,
            "file": "cfn-nag-lintly-action/Dockerfile",
            "level": "error"
        }

    """

    ignore_instructions_format = (
        'To silence this alert, add a '
        '`hadolint ignore=<rule_id_1>,<rule_id_2>` comment above this line. '
        '([hadolint documentation](https://github.com/hadolint/hadolint#inline-ignores))'
        '\n\n'
        '<details><summary>Expand to show example</summary>\n\n'
        '```\n'
        '# hadolint ignore={rule_id}\n'
        '```\n'
        '</details>\n'
    )

    def parse_violations(self, output):
        if not output:
            return dict()

        json_data = json.loads(output)

        violations = collections.defaultdict(list)

        for violation_json in json_data:
            violation = Violation(
                line=violation_json['line'],
                column=violation_json['column'],
                code=violation_json["code"],
                message=self._constuct_pr_message(
                    violation_json['message'],
                    self.ignore_instructions_format.format(rule_id=violation_json["code"])
                )
            )

            path = self._normalize_path(violation_json['file'])
            violations[path].append(violation)

        return violations


class TerrascanParser(BaseLintParser):
    """
    Terrascan JSON format
    {
        "results": {
            "violations": [
                {
                     "rule_name": "apiGatewayName",
                     "description": "Enable AWS CloudWatch Logs for APIs",
                     "rule_id": "AC_AWS_0014",
                     "severity": "MEDIUM",
                     "category": "Logging",
                     "resource_name": "this",
                     "resource_type": "aws_api_gateway_stage",
                     "file": "api_gateway_config.tf",
                     "line": 15
                }
            ],
            "skipped_violations": null,
            "scan_summary": {
                "file/folder": "/path/to/the/file/location",
                "iac_type": "terraform",
                "scanned_at": "2021-03-17 18:46:52.24701 +0000 UTC",
                "policies_validated": 562,
                "violated_policies": 7,
                "low": 4,
                "medium": 1,
                "high": 2
            }
        }
    }

    """

    ignore_instructions_format = (
        'To silence this alert, add a `ts:skip=<rule_id><reason>` comment inside this resource. '
        '([Terrascan documentation]'
        '(https://github.com/accurics/terrascan#how-to-exclude-a-policy-while-scanning-a-resource), '
        '[rule_id format update]'
        '(https://github.com/accurics/terrascan/issues/868#issuecomment-865956273))'
        '\n\n'
        '<details><summary>Expand to show example</summary>\n\n'
        '```\n'
        '# ts:skip={rule_id} Your reason here\n'
        '# ts:skip=<another_rule_id> Your reason here\n'
        '```\n'
        '</details>\n'
    )

    def parse_violations(self, output):
        if not output:
            return dict()

        json_data = json.loads(output)

        violations = collections.defaultdict(list)

        linter_violations = json_data.get("results", {}).get("violations", []) or []
        for violation_json in linter_violations:
            violation = Violation(
                line=violation_json['line'],
                column=0,
                code=violation_json["rule_id"],
                message=self._constuct_pr_message(
                    violation_json["description"],
                    self.ignore_instructions_format.format(rule_id=violation_json["rule_id"])
                )
            )

            path = self._normalize_path(violation_json["file"])
            violations[path].append(violation)

        return violations


class TrivyParser(BaseLintParser):
    """
    Trivy JSON format
    {
        "results": [
            {
                "Target": "Cargo.lock",
                "Type": "cargo",
                "Vulnerabilities": [
                    {
                        "VulnerabilityID": "RUSTSEC-2019-0001",
                        "PkgName": "ammonia",
                        "InstalledVersion": "1.9.0",
                        "FixedVersion": "\u003e= 2.1.0",
                        "Layer": {
                            "DiffID": "sha256:9d79b7f65e624be5aa0858c78c99cf169f68e2c7db49a5e610cdb5d56f18bf9c"
                            },
                        "PrimaryURL": "https://rustsec.org/advisories/RUSTSEC-2019-0001",
                        "Title": "Uncontrolled recursion leads HTML serialization",
                        "Description": "Affected versions crate use recursion for serialization of HTML\nDOM.",
                        "Severity": "UNKNOWN",
                        "References": [
                                "https://github.com/rust-ammonia/ammonia/blob/master/CHANGELOG.md#210"
                            ]
                    }
                ]
            }
        ]
    }

    """

    def parse_violations(self, output):
        if not output:
            return dict()

        json_data = json.loads(output)

        violations = collections.defaultdict(list)

        for data in json_data:
            for violation_json in data["Vulnerabilities"]:
                violation = Violation(
                    line=0,
                    column=0,
                    code="{} ({})".format(
                        violation_json["VulnerabilityID"], violation_json["Title"]
                    ),
                    message=violation_json["Description"],
                )

                path = self._normalize_path(data["Target"])
                violations[path].append(violation)

        return violations


class TfsecParser(BaseLintParser):
    """
    Tfsec JSON format
    {
        "results": [
            {
                "rule_id": "AWS025",
                "rule_description": "API Gateway domain name uses outdated SSL/TLS protocols.",
                "rule_provider": "aws",
                "link": "See https://tfsec.dev/docs/aws/AWS025/ for more information.",
                "location": {
                    "filename": "path/to/file",
                    "start_line": 29,
                    "end_line": 29
                    },
                "description": "aws_api_gateway_domain_name.empty_security_policy defines outdated SSL/TLS).",
                "severity": "ERROR",
                "passed": false
            }
        ]
    }

    """

    def parse_violations(self, output):
        if not output:
            return dict()

        json_data = json.loads(output)

        violations = collections.defaultdict(list)

        linter_violations = json_data.get("results", []) or []
        for violation_json in linter_violations:
            violation = Violation(
                line=violation_json["location"]["start_line"],
                column=0,
                code="{} ({})".format(
                    violation_json["rule_id"], violation_json["rule_description"]
                ),
                message=violation_json["description"],
            )

            path = self._normalize_path(violation_json["location"]["filename"])
            violations[path].append(violation)

        return violations


class SemgrepParser(BaseLintParser):
    """
    Semgrep JSON format
    {
        "errors": [],
        "results": [{
            "check_id": "python.jinja2.security.audit.autoescape-disabled.autoescape-disabled",
            "end": {
                "col": 77,
                "line": 14
                },
            "extra": {
                "fix_regex": {
                    "regex": "(.*)\\)",
                    "replacement": "\\1, autoescape=True)"
                    },
                "is_ignored": false,
                "lines": "env = Environment(loader=FileSystemLoader(TEMPLATES_PATH), autoescape=False)",
                "message": "Detected a Jinja2 environment without autoescaping.",
                "metadata": {
                    "category": "security",
                    "cwe": "CWE-116: Improper Encoding or Escaping of Output",
                    "license": "Commons Clause License Condition v1.0[LGPL-2.1-only]",
                    "owasp": "A6: Security Misconfiguration",
                    "references": ["https://jinja.palletsprojects.com/en/2.11.x/api/#basics"],
                    "technology": ["jinja2"]
                    },
                "metavars": {},
                "severity": "WARNING"
                },
            "path": "path/to/file",
            "start": {
                "col": 7,
                "line": 14
                }
            }
        ]
    }
    """

    ignore_instructions = (
        'Add a `nosemgrep` comment to the first line of this finding to silence this alert. '
        '([semgrep documentation](https://semgrep.dev/docs/ignoring-findings/))'
    )

    def parse_violations(self, output):
        if not output:
            return dict()

        json_data = json.loads(output)

        violations = collections.defaultdict(list)

        linter_violations = json_data.get("results", []) or []
        for violation_json in linter_violations:
            violation = Violation(
                line=violation_json["start"]["line"],
                column=violation_json["start"]["col"],
                code=violation_json["check_id"],
                message=self._constuct_pr_message(
                    violation_json["extra"]["message"], self.ignore_instructions
                )
            )

            path = self._normalize_path(violation_json["path"])
            violations[path].append(violation)

        return violations


DEFAULT_PARSER = LineRegexParser(r'^(?P<path>.*):(?P<line>\d+):(?P<column>\d+): (?P<code>\w\d+) (?P<message>.*)$')


PARSERS = {
    # Default flake8 format
    # docs/conf.py:230:1: E265 block comment should start with '# '
    # path:line:column: CODE message
    'unix': DEFAULT_PARSER,
    'flake8': DEFAULT_PARSER,
    'deps-checker': DEFAULT_PARSER,

    # Pylint ---output-format=json
    'pylint-json': PylintJSONParser(),

    # ESLint's default formatter
    # /Users/grant/project/file1.js
    #     1:1    error  '$' is not defined                              no-undef
    'eslint': ESLintParser(),

    # ESLint's unix formatter
    # lintly/static/js/scripts.js:69:1: 'lintly' is not defined. [Error/no-undef]
    # path:line:column: message [CODE]
    'eslint-unix': LineRegexParser(r'^(?P<path>.*):(?P<line>\d+):(?P<column>\d+): '
                                   r'(?P<message>.+) \[(Warning|Error)/(?P<code>.+)\]$'),

    # Checkmake uses a custom formatter
    # must set LINTLY_FILE_OVERRIDE envvar as checkmake does not provide path
    # (line):(rule:rule_description)
    'checkmake': LineRegexParser(r'^(?P<line>\d+):(?P<message>[^$]+)$'),

    # Stylelint's default formatter
    # lintly/static/sass/file1.scss
    #   13:1  ✖  Expected no more than 1 empty line   max-empty-lines
    'stylelint': StylelintParser(),

    # Black's check command default formatter.
    'black': BlackParser(),

    # cfn-lint default formatter
    'cfn-lint': CfnLintParser(),

    # Bandit Parser
    "bandit-json": BanditJSONParser(),

    # cfn-nag JSON output
    'cfn-nag': CfnNagParser(),

    # gitleaks JSON Parser
    "gitleaks": GitLeaksParser(),

    # hadolint JSON output
    "hadolint": HadolintParser(),

    # terrascan JSON output
    "terrascan": TerrascanParser(),

    # trivy JSON output
    "trivy": TrivyParser(),

    # tfsec JSON output
    "tfsec": TfsecParser(),

    # semgrep JSON output
    "semgrep": SemgrepParser(),
}
