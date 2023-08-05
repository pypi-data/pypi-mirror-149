import os
import json
import shutil
import tarfile
from os import devnull
from zipfile import ZipFile
from typing import Any, List, Tuple
from dataclasses import dataclass
from contextlib import contextmanager, redirect_stderr, redirect_stdout


@contextmanager
def suppress_stdout_stderr():
    """A context manager that redirects stdout and stderr to devnull"""
    with open(devnull, "w") as fnull:
        with redirect_stderr(fnull) as err, redirect_stdout(fnull) as out:
            yield (err, out)


@dataclass
class failed_test:
    """Class that represents a failed test case"""
    msg: str = ""
    want: Any = None
    got: Any = None


@dataclass
class failed_partid:
    """Class that represents a failed test case"""
    test_name: str
    failed_tests: List[failed_test]
    num_tests: int


def unzip_submission(file_path, destination):  
    with ZipFile(file_path, 'r') as zip:
        zip.extractall(destination)
        file_path
    if os.path.exists(file_path):
        os.remove(file_path)



def send_feedback(score: float, msg: str, feedback_path: str = "/shared/feedback.json", err: bool = False) -> None:
    """Sends feedback to the learner.
    Args:
        score (float): Grading score to show on Coursera for the assignment.
        msg (str): Message providing additional feedback.
        err (bool, optional): True if there was an error while grading. Defaults to False.
    """

    post = {"fractionalScore": score, "feedback": msg}
    print(json.dumps(post))

    with open(feedback_path, "w") as outfile:
        json.dump(post, outfile)

    if err:
        exit(1)

    exit(0)


def copy_submission_to_workdir(origin: str = "/shared/submission/", destination: str = "./submission/", extension: str = ".ipynb") -> None:
    """Copies submission file from bind mount into working directory.
    Args:
        config (Config): An instance of Config that includes the paths to copy from/to.
        extension (str): Extension of the submission file.
    """

    files = [file for file in os.listdir(origin) if file.endswith(extension)]
    learner_zip = files[0]

    file_initial_path = os.path.join(origin, learner_zip)
    file_final_path = os.path.join(destination, learner_zip)

    shutil.copyfile(file_initial_path, file_final_path)


def compute_grading_score_multi_partid(failed_cases: List[failed_partid]) -> Tuple[float, str]:
    """Computes the score based on the number of failed and total cases.
    Args:
        failed_partid (List): Failed cases for every part.
    Returns:
        Tuple[float, str]: The grade and feedback message.
    """
    scores = []
    msgs = []

    for f in failed_cases:
        feedback_msg = f"All tests passed for {f.test_name}!\n"
        score = 1.0 - len(f.failed_tests) / f.num_tests
        score = round(score, 2)
        scores.append(score)

        if f.failed_tests:
            feedback_msg = f"Details of failed tests for {f.test_name}\n\n"
            for failed_case in f.failed_tests:
                feedback_msg += f"Failed test case: {failed_case.msg}.\nExpected:\n{failed_case.want},\nbut got:\n{failed_case.got}.\n\n"
        msgs.append(feedback_msg)

    final_score = sum(scores)/len(scores)
    final_score = round(final_score, 2)
    final_msg = "\n".join(msgs)

    return final_score, final_msg


def compute_grading_score(failed_cases: List[failed_test], num_cases: int) -> Tuple[float, str]:
    """Computes the score based on the number of failed and total cases.
    Args:
        failed_cases (List): Failed cases.
        num_cases (int): Total number of cases.
    Returns:
        Tuple[float, str]: The grade and feedback message.
    """

    score = 1.0 - len(failed_cases) / num_cases
    feedback_msg = "All tests passed! Congratulations!"

    if failed_cases:
        feedback_msg = ""
        for failed_case in failed_cases:
            feedback_msg += f"Failed test case: {failed_case.msg}.\nExpected:\n{failed_case.want},\nbut got:\n{failed_case.got}.\n\n"
        return round(score, 2), feedback_msg

    return score, feedback_msg


def object_to_grade(origin_module, attr_name):
    """Used as a parameterized decorator to get an attribute from a module.

    Args:
        origin_module (ModuleType): A module.
        attr_name (str): Name of the attribute to extract from the module.
    """
    def middle(func):
        def wrapper():
            val = getattr(origin_module, attr_name, None)
            return func(val)
        return wrapper
    return middle


def extract_tar(file_path: str, destination: str):
    with tarfile.open(origin, 'r') as my_tar:
        my_tar.extractall(destination)

    if os.path.exists(file_path):
        os.remove(file_path)