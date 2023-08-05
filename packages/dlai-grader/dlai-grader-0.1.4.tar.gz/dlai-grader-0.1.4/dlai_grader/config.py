import os
from dataclasses import dataclass


def get_part_id() -> str:
    """Get part id from environment variable.
    Returns:
        str: The part id.
    """
    part_id = os.getenv("partId")
    if part_id is None:
        return ""
    return part_id


@dataclass
class Config:
    bind_mount: str = "/shared/submission/"
    submission_workdir: str = "./submission/"
    solution_workdir: str = "./solution/"
    solution_file: str = "solution.ipynb"
    solution_file_path: str = os.path.join(solution_workdir, solution_file)
    submission_file: str = "submission.ipynb"
    submission_file_path: str = os.path.join(submission_workdir, submission_file)
    feedback_file_path: str = "/shared/feedback.json"
    part_id: str = get_part_id()


    def update_submission_file_path(self):
        self.submission_file_path = os.path.join(self.submission_workdir, self.submission_file)
