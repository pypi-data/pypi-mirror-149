# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kargers',
 'kargers.core',
 'kargers.db',
 'kargers.experimental',
 'kargers.utils',
 'kargers.viz']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.35,<2.0.0',
 'matplotlib>=3.5.1,<4.0.0',
 'networkx>=2.8,<3.0',
 'numpy>=1.22.3,<2.0.0',
 'psycopg2-binary>=2.9.3,<3.0.0',
 'pydantic[dotenv]>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'roux-algo-geneweaver-kargers',
    'version': '0.0.2',
    'description': "An implementation of Krager's Algorithm to find similar Genesets",
    'long_description': '# roux-cs5800-karger-genesets\n\nWARNING: This package is under active development. The API may change at any time. Documentation may\nbe out of date.\n\n## Installation\n\n### Set Up\nIt\'s usaully a good idea to install this package in a python virtual environment.\n```\npython3 -m venv $NAME_OF_VENV\nsource $NAME_OF_VENV/bin/activate\npip install \n```\n\n## Usage\nTwo data formats are currently supported, "Node and Edges List" and "Adjacency List" formats. If you\nuse the "Adjacency List" format, you will need to convert it to the "Node and Edges List" format\nbefore using it with Karger\'s. We included utility methods to make this easy.\n\n#### Load Data\n```python\nfrom roux.algo.geneweaver.kargers import *\nnodes, edges = karger_io.load_nodes_edges(\'nodes_edges_file.json\')\n```\n\n##### Load Data from Adjacency List Source\n```python\nfrom roux.algo.geneweaver.kargers import *\ngraph = karger_io.load_graph(\'graph_file.json\')\nnodes, edges = karger_tf.adj_graph_to_edge_list(graph)\nedges = karger_tf.deduplicate_edge_list(edges)\n```\n\n#### Run Kargers on Data\n```python\nfrom roux.algo.geneweaver.kargers import *\nnodes, edges = karger_io.load_nodes_edges(\'nodes_edges_file.json\')\nk_inst = KargerMinCut(nodes, edges)\nmin_cut, best_cuts, result = k_inst.min_cut()\n\n...\n\nsuper_nodes = karger_tf.union_find_to_geneset_list(result.roots(), result.non_roots())\n```\n\n\n## Developer Setup\n\n#### Base Tools\n\n1. Install [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)\n2. Install [python3.9](https://www.python.org/downloads/release/python-3912/)\n   1. Note: install method varies by operating system\n3. Install [poetry](https://python-poetry.org/docs/)\n\n#### Set up\n\n4. Clone [this repository](https://github.com/bergsalex/cs5800-final-project)\n5. Move to cloned directory (e.g. `cd cs5800-final-project`)\n6. Run `poetry install`\n7. If you need to connect to the database, create a .env configuration file \n\nYou should now be able to use the python package:\n\n1. Run `poetry shell`\n2. Run `python3`\n\n```python\nfrom roux.algo.geneweaver.kargers import kragers_poc as kpm\nfrom roux.algo.geneweaver.kargers.utils import build_graph as bg\nfrom roux.algo.geneweaver.kargers.db.session import SessionLocal\n\ndb = SessionLocal()\ngraph = bg.build_graph(db, {i for i in range(349100, 349110)})\nresult = kpm.kragers_poc_1(graph)\n```\n\n\n\n### Create the Tier 2 Dataset\n\n```python\nfrom roux.algo.geneweaver.kargers.utils import build_graph as bg\nfrom roux.algo.geneweaver.kargers.db.session import SessionLocal\n\ndb = SessionLocal()\n# The dataset is slightly smaller than 19000 nodes\ngraph = bg.get_adjacency_exclusive_new(db, 2, 19000)\n```\n\n#### To save the dataset\n\n```python\nfrom roux.algo.geneweaver.kargers.utils import load_save_graph as ls\n\n# Build the graph above\ngraph = ...\n\n### Get all Tier 2 Genesets\nls.save_graph(\'filename.json\', graph)\n```\n\n### Get all Tier 2 Genesets\n\n```python\nfrom roux.algo.geneweaver.kargers.utils import build_graph as bg\nfrom roux.algo.geneweaver.kargers.db.session import SessionLocal\n\ndb = SessionLocal()\ntier_2_genesets = bg.get_all_genesets_by_tier(db, 2)\n```\n',
    'author': 'Alex Berger',
    'author_email': 'berger.ale@northeastern.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
