import numpy as np
import pandas as pd


def get_group(pid, groups):
    """
    This functions get the group of the corresponding id of the page.

    Parameters
    ----------
    pid:
        type: str
        page_id to conpute the group for.
    groups:
        type: dict
        Maps the group to the page ids.

    Returns
    -------
    str
    """

    group_out = "no_group"
    try:
        for group in groups:
            if pid in groups[group]:
                group_out = group
    except Exception:
        pass
    return group_out


def discretize(df, from_column, to_column=None, n_groups=10):
    """
    This functions discretizes de column 'from_column' into the column 'to_column' in the
    dataframe df.

    Parameters
    ----------
    n_groups:
        type: str
        Number of groups to split the column 'from_column'.
        default=10

    Returns
    -------
    None
    """
    if from_column in df.keys():
        if to_column:
            df[to_column] = pd.cut(
                df[from_column], n_groups, labels=range(1, n_groups + 1)
            )
        else:
            df[f"disc_{from_column}"] = pd.cut(
                df[from_column], n_groups, labels=range(1, n_groups + 1)
            )
    else:
        raise RuntimeError(
            f"{from_column} is not a column available of input DataFrame."
        )
