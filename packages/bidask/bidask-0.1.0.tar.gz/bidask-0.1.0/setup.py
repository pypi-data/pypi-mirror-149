# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bidask']

package_data = \
{'': ['*']}

install_requires = \
['numpy']

setup_kwargs = {
    'name': 'bidask',
    'version': '0.1.0',
    'description': 'Efficient Estimation of Bid-Ask Spreads from Open, High, Low, and Close Prices',
    'long_description': '# Efficient Estimation of Bid-Ask Spreads from Open, High, Low, and Close Prices\n\nImplements an efficient estimation procedure of the bid-ask spread from Open, High, Low, and Close prices as proposed in Ardia, Guidotti, Kroencke (2021): https://www.ssrn.com/abstract=3892335\n\n## Installation\n\nInstall this package with:\n\n```bash\npip install bidask\n```\n\n## Usage\n\nImport the estimator\n\n```python\nfrom bidask import edge\n```\n\nEstimate the spread\n\n```python\nedge(open, high, low, close)\n```\n\n- `open`: array-like vector of Open prices.\n- `high`: array-like vector of High prices.\n- `low`: array-like vector of Low prices.\n- `close`: array-like vector of Close prices.\n\nPrices must be sorted in ascending order of the timestamp.\n\n## Cite as\n\n*Ardia, David and Guidotti, Emanuele and Kroencke, Tim Alexander, "Efficient Estimation of Bid-Ask Spreads from Open, High, Low, and Close Prices". Available at SSRN: https://ssrn.com/abstract=3892335*\n\nA BibTex  entry for LaTeX users is:\n\n```bibtex\n@unpublished{edge2021,\n    author = {Ardia, David and Guidotti, Emanuele and Kroencke, Tim},\n    title  = {Efficient Estimation of Bid-Ask Spreads from Open, High, Low, and Close Prices},\n    year   = {2021},\n    note   = {Available at SSRN}\n    url    = {https://ssrn.com/abstract=3892335}\n}\n```\n',
    'author': 'Emanuele Guidotti',
    'author_email': 'emanuele.guidotti@unine.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eguidotti/bidask',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
