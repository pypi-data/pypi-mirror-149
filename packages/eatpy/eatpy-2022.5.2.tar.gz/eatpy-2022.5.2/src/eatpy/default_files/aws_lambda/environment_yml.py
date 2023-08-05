ENVIRONMENT_YML = """\
name: conda-env
channels:
  - conda-forge
dependencies:
  - python={PYTHON_VERSION}
  - pip
  - pip:
    - -r requirements.txt
"""
