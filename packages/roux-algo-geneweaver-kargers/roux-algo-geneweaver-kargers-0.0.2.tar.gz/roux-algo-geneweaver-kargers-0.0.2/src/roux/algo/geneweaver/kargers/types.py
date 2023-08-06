from sqlalchemy.orm import Session
from typing import List, Dict, Set, Callable, Tuple

AdjCallable = Callable[[Session, int, Set[int]], Set[int]]
AdjGraph = Dict[int, Set[int]]
AdjGraphList = Dict[int, List[int]]

GsidSet = Set[int]

EdgeList = List[Tuple[int, int]]
NodeList = List[int]
NodesAndEdges = Tuple[NodeList, EdgeList]
