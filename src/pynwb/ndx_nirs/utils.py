from copy import deepcopy

from hdmf.utils import get_docval


def update_docval(fn, *, keep=None, remove=None, updates=None):
    """Copy items from the docval for an existing function with updates

    Args:
        fn (callable): a function containing a pre-existing docval to be updated
        keep (list[str], None): a list of names of the docval items to keep. If None, then
            all items are kept. Cannot be used simultaneously with 'remove'. Default: None.
        remove (list[str], None): a list of names of the docval items to remove. If None,
            then no items are removed. Cannot be used simultaneously with 'keep'. Default: None.
        updates (dict, None): a dict containing any updates that should be made to docval items
            before returning them. Keys need to match the name of docval items, and the values
            need to be a dict containing the update.

    Returns:
        list[dict]: the list of filtered and updated docval items.

    Example:
    ```
    docval_items = update_docval(
        DynamicTable.__init__,
        remove=['columns', 'colnames'],
        updates=dict(
            name={'default_value': 'foo'},
            description={'default_value': 'An updated table'}
        )
    )
    ```
    """
    original_docval = get_docval(fn)
    new_docval = deepcopy(original_docval)
    item_names = {item["name"] for item in new_docval}
    if keep is not None and remove is not None:
        raise ValueError("'keep' and 'remove' cannot be used simultaneously")
    elif keep is not None:
        if any(name not in item_names for name in keep):
            raise ValueError(
                "The existing docval does not contain all items listed in 'keep'"
            )
        new_docval = list(filter(lambda x: x["name"] in keep, new_docval))
    elif remove is not None:
        if any(name not in item_names for name in remove):
            raise ValueError(
                "The existing docval does not contain all items listed in 'remove'"
            )
        new_docval = list(filter(lambda x: x["name"] not in remove, new_docval))

    if updates is not None:
        new_docval = _make_updates(new_docval, updates, fn.__name__)
    return new_docval


def _make_updates(docval_params, updates, fn_name):
    """Updates docval items based on the dictionary in 'updates'.

    'updates' is expected to be a dictionary of str: dict. The keys are used to identify
    which docval item to update and need to match the name field of existing parameter.
    The values are dicts that are then used to update the existing docval item fields.
    """
    for name, update_vals in updates.items():
        for item in docval_params:
            if item["name"] == name:
                item.update(update_vals)
                break
        else:
            msg = f"docval item named {name} does not exist for function {fn_name}"
            raise ValueError(msg)
    return docval_params
