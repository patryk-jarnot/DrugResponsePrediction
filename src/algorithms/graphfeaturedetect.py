from src.domain.Path import Path
import src.utils.sparqlutils as su


class NodeData:
    def __init__(self, max_depth = 6):
        self.counter = 0
        self.depths = [0 for i in range(max_depth)]


def get_paths_by_node(node):
    depth = 0
    paths = []
    tabu_list = []
    path = Path()
    path.append_node("http://bio2rdf.org/pubchem.compound:{0}".format(node), depth)
    get_paths(paths, tabu_list, path, depth+1, node)
    return paths


def get_paths(paths, tabu_list, current_path, depth, node):
    pairs = su.query_drug(current_path.get_nodes()[-1], node, depth)

    if depth == 6:
        paths.append(current_path)
        return None

    if pairs is None:
        paths.append(current_path)
        return None

    for pair in pairs:

        if str(pair) in tabu_list:
            continue
        else:
            tabu_list.append(str(pair))

        path = current_path.clone()
        path.append_edge(pair.edge)
        path.append_node(pair.node, depth)
        if pair.edge == "http://www.w3.org/2002/07/owl#sameAs":
            get_paths(paths, tabu_list, path, depth, node)
        else:
            get_paths(paths, tabu_list, path, depth + 1, node)


def get_pairs_from_paths(paths):
    pairs = set()

    for path in paths:
        for pair in path.get_pairs():
            pairs.add(pair)

    return pairs


def get_nodes_from_paths(paths):
    nodes = set()

    for path in paths:
        for node in path.get_nodes():
            nodes.add(node)

    return nodes


def count_items_in_set(nodes, counter_dict):
    for node in nodes:
        if node not in counter_dict:
            counter_dict[node] = NodeData()

        counter_dict[node].counter += 1
        counter_dict[node].depths[node.depth] += 1


def count_items_in_pairs_list(pairs_list):
    pairs_dict = {}
    for pairs in pairs_list:
        for pair in pairs:
            if pair not in pairs_dict:
                pairs_dict[pair] = 1
            else:
                pairs_dict[pair] += 1

    return pairs_dict


def filter_results(main_nodes, nodes_to_filter, ratio=8, threshold=2):
    main_result_dict = {}
    tabu_result_dict = {}
    for main_pair_key, main_pair_val in main_nodes.items():
        if main_pair_val.counter < threshold:
            continue

        if main_pair_key not in nodes_to_filter:
            main_result_dict[main_pair_key] = main_pair_val
        elif main_pair_val.counter / nodes_to_filter[main_pair_key].counter > ratio:
            main_result_dict[main_pair_key] = main_pair_val
            tabu_result_dict[main_pair_key] = nodes_to_filter[main_pair_key]

    return main_result_dict, tabu_result_dict


def write_results(file_name, main_nodes, tabu_nodes):
    with open(file_name, "w") as f:
        f.write("Node;positive;negative;depths\n")
        for main_key, main_val in main_nodes.items():
            if main_key in tabu_nodes:
                tabu_val = tabu_nodes[main_key]
            else:
                tabu_val = NodeData()

            f.write("\"{0}\";{1};{2};{3}\n".format(main_key.data, main_val.counter, tabu_val.counter, ','.join(str(x) for x in main_val.depths)))


