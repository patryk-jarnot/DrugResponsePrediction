from SPARQLWrapper import SPARQLWrapper, JSON, DIGEST
from src.domain.Path import Path
from src.utils.passwords import SparqlCredentials
import hashlib
import os
import pickle


# def hit_database(id, node, cache_path="/home/pjarnot/windata/tmp/sparql/"):
def hit_database(id, node, cache_path="/home/pjarnot/tmp/sparql/"):
    sparql = SPARQLWrapper("http://pgxlod.loria.fr/sparql")

    ''' Uncomment this if you want to switch to private server '''
    # sparql = SPARQLWrapper("http://pgxlod-private.loria.fr/sparql")
    # sparql.setHTTPAuth(DIGEST)
    # sparql.setCredentials(SparqlCredentials.user, SparqlCredentials.password)

    if not id.data.startswith("http"):
        return None

    if cache_path is not None:
        hash_object = hashlib.sha256(str(node).encode())
        hex_node = hash_object.hexdigest()

        hash_object = hashlib.sha256(id.data.encode())
        hex_dig = hash_object.hexdigest()

        tmp_dir = "{0}{1}".format(cache_path, hex_node)
        tmp_file = "{0}{1}/{2}".format(cache_path, hex_node, hex_dig)
    else:
        tmp_dir = ""
        tmp_file = ""

    if not os.path.isdir(tmp_dir):
        os.mkdir(tmp_dir)

    if os.path.isfile(tmp_file):
        try:
            results = pickle.load( open( tmp_file, "rb" ) )
        except EOFError:
            results = None

    else:
        sparql.setQuery("select ?p ?o where {<%s> ?p ?o.} LIMIT 1000" % (id.data))
        sparql.setReturnFormat(JSON)
        try:
            results = sparql.query().convert()

            pickle.dump(results, open(tmp_file, "wb"))
        except:
            results = None
    return results


def query_drug(id, node, depth):
    results = hit_database(id, node)

    if results is None:
        return None

    pairs = []
    for result in results["results"]["bindings"]:
        pair = Path.Pair(result["p"]["value"], result["o"]["value"], depth)

        pairs.append(pair)

    return pairs
