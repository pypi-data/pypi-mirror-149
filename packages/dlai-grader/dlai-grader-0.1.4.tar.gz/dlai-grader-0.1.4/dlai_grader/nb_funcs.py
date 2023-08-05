import re
import nbformat
import jupytext
from nbformat.notebooknode import NotebookNode


def nb_to_py(nb: NotebookNode) -> str:
    """Converts a notebook into a python script serialized as a string.
    Args:
        nb (NotebookNode): Notebook to convert into script.
    Returns:
        str: Python script representation as string.
    """
    return jupytext.writes(nb, fmt="py:percent")


def read_nb(path: str) -> NotebookNode:
    """Reads a notebook found in the given path and returns a serialized version.
    Args:
        path (str): Path of the notebook file to read.
    Returns:
        NotebookNode: Representation of the notebook following nbformat convention.
    """
    return nbformat.read(path, as_version=nbformat.NO_CONVERT)


def filter_nb(notebook: NotebookNode) -> NotebookNode:
    """Filters a notebook to exclude additional cells created by learners.
       Also used for partial grading if the tag has been provided.
    Args:
        notebook (NotebookNode): Notebook to filter.
    Returns:
        NotebookNode: The filtered notebook.
    """
    filtered_cells = []
    partial_grade_regex = "(grade)(.|[ \t]*)(up)(.|[ \t]*)(to)(.|[ \t]*)(here)"
    
    for cell in notebook["cells"]:
        if not "tags" in cell["metadata"] or not "graded" in cell["metadata"]["tags"]:
            continue
        filtered_cells.append(cell)

        if cell["cell_type"] == "code" and re.search(partial_grade_regex, cell["source"]):
            break

    notebook["cells"] = filtered_cells
    return notebook


def get_named_cells_as_json(nb_json: NotebookNode) -> dict:
    """Returns the named cells for cases when grading is done using cell's output.
    Args:
        nb_json (NotebookNode): The notebook from the learner.
    Returns:
        dict: All named cells encoded as a dictionary.
    """
    cells = {}
    for cell in nb_json.get("cells"):
        metadata = cell.get("metadata")
        if not "name" in metadata:
            continue
        cells.update({metadata.get("name"): cell})
    return cells


def tag_code_cells(notebook: NotebookNode) -> NotebookNode:
    """Filters a notebook to exclude additional cells created by learners.
       Also used for partial grading if the tag has been provided.
    Args:
        notebook (NotebookNode): Notebook to filter.
    Returns:
        NotebookNode: The filtered notebook.
    """
    filtered_cells = []
    
    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            if not "tags" in cell["metadata"]:      
                cell["metadata"]["tags"] = []
            
            tags = cell["metadata"]["tags"]
            tags.append("graded")
            cell["metadata"]["tags"] = tags

        filtered_cells.append(cell)


    notebook["cells"] = filtered_cells
    return notebook


def tag_notebook_in_place(path):
    nb = read_nb(path)
    nb = tag_code_cells(nb)
    jupytext.write(nb, path)