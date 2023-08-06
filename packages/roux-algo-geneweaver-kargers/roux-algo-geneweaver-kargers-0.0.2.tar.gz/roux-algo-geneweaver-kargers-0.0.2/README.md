# roux-cs5800-karger-genesets

WARNING: This package is under active development. The API may change at any time. Documentation may
be out of date.

## Installation

### Set Up
It's usaully a good idea to install this package in a python virtual environment.
```
python3 -m venv $NAME_OF_VENV
source $NAME_OF_VENV/bin/activate
pip install 
```

## Usage
Two data formats are currently supported, "Node and Edges List" and "Adjacency List" formats. If you
use the "Adjacency List" format, you will need to convert it to the "Node and Edges List" format
before using it with Karger's. We included utility methods to make this easy.

#### Load Data
```python
from roux.algo.geneweaver.kargers import *
nodes, edges = karger_io.load_nodes_edges('nodes_edges_file.json')
```

##### Load Data from Adjacency List Source
```python
from roux.algo.geneweaver.kargers import *
graph = karger_io.load_graph('graph_file.json')
nodes, edges = karger_tf.adj_graph_to_edge_list(graph)
edges = karger_tf.deduplicate_edge_list(edges)
```

#### Run Kargers on Data
```python
from roux.algo.geneweaver.kargers import *
nodes, edges = karger_io.load_nodes_edges('nodes_edges_file.json')
k_inst = KargerMinCut(nodes, edges)
min_cut, best_cuts, result = k_inst.min_cut()

...

super_nodes = karger_tf.union_find_to_geneset_list(result.roots(), result.non_roots())
```


## Developer Setup

#### Base Tools

1. Install [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
2. Install [python3.9](https://www.python.org/downloads/release/python-3912/)
   1. Note: install method varies by operating system
3. Install [poetry](https://python-poetry.org/docs/)

#### Set up

4. Clone [this repository](https://github.com/bergsalex/cs5800-final-project)
5. Move to cloned directory (e.g. `cd cs5800-final-project`)
6. Run `poetry install`
7. If you need to connect to the database, create a .env configuration file 

You should now be able to use the python package:

1. Run `poetry shell`
2. Run `python3`

```python
from roux.algo.geneweaver.kargers import kragers_poc as kpm
from roux.algo.geneweaver.kargers.utils import build_graph as bg
from roux.algo.geneweaver.kargers.db.session import SessionLocal

db = SessionLocal()
graph = bg.build_graph(db, {i for i in range(349100, 349110)})
result = kpm.kragers_poc_1(graph)
```



### Create the Tier 2 Dataset

```python
from roux.algo.geneweaver.kargers.utils import build_graph as bg
from roux.algo.geneweaver.kargers.db.session import SessionLocal

db = SessionLocal()
# The dataset is slightly smaller than 19000 nodes
graph = bg.get_adjacency_exclusive_new(db, 2, 19000)
```

#### To save the dataset

```python
from roux.algo.geneweaver.kargers.utils import load_save_graph as ls

# Build the graph above
graph = ...

### Get all Tier 2 Genesets
ls.save_graph('filename.json', graph)
```

### Get all Tier 2 Genesets

```python
from roux.algo.geneweaver.kargers.utils import build_graph as bg
from roux.algo.geneweaver.kargers.db.session import SessionLocal

db = SessionLocal()
tier_2_genesets = bg.get_all_genesets_by_tier(db, 2)
```
