"""

"""
import time
from contextlib import contextmanager
from collections import defaultdict

from sqlalchemy.orm import Session
from roux.algo.geneweaver.kargers.types import AdjGraph, AdjCallable, GsidSet, EdgeList
from roux.algo.geneweaver.kargers.utils.transform import query_result_to_set

TRACK_TIME = True


def get_all_genesets_by_tier(db: Session, tier: int) -> GsidSet:
    query = db.execute("""SELECT gs_id 
        FROM production.geneset 
        WHERE gs_status NOT LIKE 'de%' AND cur_id = :tier;
        """, {'tier': tier})
    result = query.fetchall()

    return query_result_to_set(result)


@contextmanager
def interested_genesets(db: Session, tier: int, limit=10000):
    temp_table_name = 'temp_interested_genesets'
    db.execute("""
        CREATE TEMP TABLE temp_interested_genesets AS
        SELECT gs_id FROM production.geneset
        WHERE gs_status NOT LIKE 'de%' AND cur_id = :tier LIMIT :limit;
        """, {'tier': tier, 'limit': limit})
    db.execute("""
        CREATE INDEX ON temp_interested_genesets(gs_id);
        """)

    yield temp_table_name

    db.execute("""
        DROP TABLE temp_interested_genesets;
    """)


def get_adjacency_simple(db: Session, gs_id: int) -> GsidSet:
    query = db.execute("""SELECT DISTINCT gvv.gs_id
        FROM production.geneset g
            INNER JOIN extsrc.geneset_value gv ON g.gs_id = gv.gs_id
            INNER JOIN extsrc.geneset_value gvv on gv.ode_gene_id = gvv.ode_gene_id
        WHERE g.gs_id = :gs_id;
    """, {'gs_id': gs_id})
    result = query.fetchall()

    return query_result_to_set(result)


def get_adjacency_full(db: Session, gs_id: int, genesets: GsidSet) -> GsidSet:
    query = db.execute("""SELECT DISTINCT gvv.gs_id
        FROM production.geneset g
            INNER JOIN extsrc.geneset_value gv ON g.gs_id = gv.gs_id
            INNER JOIN extsrc.geneset_value gvv on gv.ode_gene_id = gvv.ode_gene_id
        WHERE g.gs_id = :gs_id AND gvv.gs_id != g.gs_id AND gvv.gs_id IN :genesets;
    """, {'gs_id': gs_id, 'genesets': tuple(genesets)})
    result = query.fetchall()

    return query_result_to_set(result)


def get_adjacency_exclusive(db: Session, gs_id: int, genesets: GsidSet) -> GsidSet:
    start = time.time() if TRACK_TIME else 0

    query = db.execute("""SELECT DISTINCT gvv.gs_id
        FROM production.geneset g
            INNER JOIN extsrc.geneset_value gv ON g.gs_id = gv.gs_id
            INNER JOIN extsrc.geneset_value gvv on gv.ode_gene_id = gvv.ode_gene_id
        WHERE g.gs_id = :gs_id AND gvv.gs_id != g.gs_id AND gvv.gs_id IN :genesets;
    """, {'gs_id': gs_id, 'genesets': tuple(genesets)})

    if TRACK_TIME:
        print(f"{gs_id} executed in {time.time() - start} s")

    result = query.fetchall()

    if TRACK_TIME:
        print(f"{gs_id} retrieved in {time.time() - start} s")

    result = query_result_to_set(result)

    if TRACK_TIME:
        print(f"{gs_id} formatted in {time.time() - start} s")

    return result


def get_adjacency_exclusive_new(db: Session, tier: int = 2, limit: int = 100) -> AdjGraph:
    """"""

    start = time.time() if TRACK_TIME else 0

    with interested_genesets(db, tier, limit):
        if TRACK_TIME:
            print(f"Set up in {time.time() - start} s")

        query = db.execute("""CREATE TEMP TABLE gs_graph AS
                SELECT DISTINCT igs.gs_id gs_id1, gvv.gs_id gs_id2
                FROM temp_interested_genesets AS igs
                         JOIN extsrc.geneset_value gv ON igs.gs_id = gv.gs_id
                         JOIN
                     (SELECT igs.gs_id, ode_gene_id
                      FROM temp_interested_genesets AS igs
                               JOIN extsrc.geneset_value gsv
                                    ON igs.gs_id = gsv.gs_id) gvv
                     ON gv.ode_gene_id = gvv.ode_gene_id
                WHERE igs.gs_id != gvv.gs_id;
        """)

        print(f"Query table set up in {time.time() - start} s")

        remaining = True
        q_limit = 500000
        # Stupid index is off by 1
        q_offset = -1

        graph: AdjGraph = defaultdict(set)
        edge_list: EdgeList = []

        print("Starting fetch results calls")
        while remaining:
            if q_offset == -1:
                query = db.execute("""SELECT gs_id1, gs_id2
                        FROM gs_graph
                        LIMIT :q_limit;
                """, {'q_limit': q_limit})
            else:
                query = db.execute("""SELECT gs_id1, gs_id2
                        FROM gs_graph
                        LIMIT :q_limit OFFSET :q_offset;
                """, {'q_limit': q_limit, 'q_offset': q_offset})

            if TRACK_TIME:
                print(f"executed in {time.time() - start} s")

            new_rows = query.fetchall()
            print("fetched rows")

            if len(new_rows) == 0:
                remaining = False

            for r in new_rows:
                graph[int(r[0])].add(r[1])

            edge_list.extend([(int(r[0]), int(r[1])) for r in new_rows])

            print("formatted rows")
            q_offset += q_limit
            print(f"processed {q_offset + 1} rows so far ...")

        del query
        db.execute("DROP TABLE gs_graph;")

        if TRACK_TIME:
            print(f"formatted in {time.time() - start} s")

        return graph


def build_graph(db: Session,
                genesets: GsidSet,
                select_func: AdjCallable = get_adjacency_full) -> AdjGraph:
    """

    :param db:
    :param genesets:
    :param select_func:
    :return:
    """
    return {
        gs_id: select_func(db, gs_id, genesets)
        for gs_id in genesets
    }


def build_graph_timed(db: Session,
                      genesets: GsidSet,
                      select_func: AdjCallable = get_adjacency_full) -> AdjGraph:
    """

    :param db:
    :param genesets:
    :param select_func:
    :return:
    """
    start_outer = time.time()
    print(f"Building graph with {len(genesets)} nodes.")
    graph: AdjGraph = {}
    for gs_id in genesets:
        start_inner = time.time()
        result = select_func(db, gs_id, genesets)
        graph[gs_id] = result
        now = time.time()
        print(f"{gs_id} retrieved in {now - start_outer}s, {now - start_inner}s")
    print(f"Total time: {start_outer - time.time()}")
    return graph


def graph_has_edge(to_node: int, graph: AdjGraph):
    found = False
    while not found:
        for source, edges in graph.items():
            for edge in edges:
                if edge == to_node:
                    print(source, edge, to_node)
                    found = True
        break
    return found


def missing_nodes(graph: AdjGraph):
    keys = graph.keys()
    missing_nodes = []
    for source, edges in graph.items():
        for edge in edges:
            if edge not in keys and edge not in missing_nodes:
                missing_nodes.append(edge)
                print(f"Source {source} has edge to missing node {edge}")
    return missing_nodes