import os
from dataclasses import dataclass

from github import Github
from github.PullRequest import PullRequest
from github.Repository import Repository
from bigeye_sdk.generated.com.torodata.models.generated import ComparisonTableInfo
from bigeye_sdk.model.vendor_report import VendorReport, format_table, create_records
from bigeye_sdk.model import TABLE_HEADER, fields, alignment


@dataclass
class GitHubReport(VendorReport):
    github_token: str
    git: Github = None
    repo: Repository = None
    pr: PullRequest = None

    def __post_init__(self):
        self.git = Github(self.github_token)
        self.repo = self.git.get_repo(os.environ['CURRENT_REPO'])
        self.pr = self.repo.get_pull(int(os.environ['PR_NUMBER']))

    def publish(self, source_table_name: str, target_table_name: str, cti: ComparisonTableInfo):
        issue_title = f'Bigeye Delta failure for PR: {self.pr.title}'

        records = create_records(source_table_name, target_table_name, cti.comparison_metric_infos)

        table = format_table("\n", records, fields, TABLE_HEADER, alignment)

        link = f"\n\n[See Delta](https://app.bigeye.com/deltas/{cti.comparison_table_configuration.id})"
        table_with_title = f"Source Table: {source_table_name}\nTarget Table: {target_table_name}\n\n{table}{link}"
        html = self.git.render_markdown(text=table, context=self.repo)

        self.repo.create_issue(title=issue_title, body=table_with_title, assignee=self.pr.user, labels=['bug'])
