def paginate(name, items):
    return {
        "_embed": {name: items},
        "count": len(items),
        "_links": {"next": None, "previous": None},
    }
