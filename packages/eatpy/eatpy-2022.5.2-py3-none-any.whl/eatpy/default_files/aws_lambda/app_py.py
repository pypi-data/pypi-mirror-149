APP_PY = """\
# not ".src" just "src"!
from src import task

# handler
def {HANDLER}(event: dict, context: object) -> dict:
    results = task.run(event=event, context=context)
    return results
"""
