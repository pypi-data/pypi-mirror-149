TASK_PY = """\
# import required packages here

# run
def run(event: dict, context: object) -> dict:
    parsed_context = {
        k: v if isinstance(v, int) else str(v) for k, v in context.__dict__.items()
    }
    results = {
        "event": event,
        "context": parsed_context,
    }
    return results
"""
