

def hit_database(id, is_first_layer=True):
    sparql = SPARQLWrapper("http://pgxlod.loria.fr/sparql")
    # sparql.setQuery("select <http://bio2rdf.org/pubchem.compound:%d> ?p ?o ?p2 ?o2 where {<http://bio2rdf.org/pubchem.compound:%d> ?p ?o. ?o ?p2 ?o2.} LIMIT 100" % (id, id))
    if is_first_layer:
        # sparql.setQuery("select ?p ?o where {<http://bio2rdf.org/pubchem.compound:%d> ?p ?o.} LIMIT 1000" % (id))
        # sparql.setQuery("select ?p ?o ?p2 ?o2 ?p3 ?o3 where {<http://bio2rdf.org/pubchem.compound:%d> ?p ?o. ?o ?p2 ?o2. ?o2 ?p3 ?o3.} LIMIT 100000" % (id))
        sparql.setQuery("select ?p ?o ?p2 ?o2 ?p3 ?o3 ?p4 ?o4 where {<http://bio2rdf.org/pubchem.compound:%d> ?p ?o. ?o ?p2 ?o2. ?o2 ?p3 ?o3. ?o3 ?p4 ?o4.} LIMIT 100000" % (id))
    else:
        # print("id: {0}".format(id), file=sys.stderr)
        if not id.startswith("http"):
            return None
        sparql.setQuery("select ?p ?o where {<%s> ?p ?o.} LIMIT 1000" % (id))
    sparql.setReturnFormat(JSON)
    try:
        results = sparql.query().convert()
    except:
        return None
    return results
