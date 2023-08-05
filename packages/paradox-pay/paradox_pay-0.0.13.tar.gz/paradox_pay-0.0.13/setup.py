from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
with open(this_directory / "README.md", encoding="utf8", errors='ignore') as f:
    long_description = f.read()

setup(
    name='paradox_pay',
    # other arguments omitted
    long_description=long_description,
    long_description_content_type='text/markdown'
)