from enum import Enum
import copy


class Path:

    class Pair:
        def __init__(self, edge, node, depth):
            self.edge = edge
            self.node = node
            self.depth = depth

        def __repr__(self):
            return "{0}|{1}".format(self.edge, self.node)

        def __eq__(self, other):
            return (isinstance(other, self.__class__) and
                    getattr(other, 'edge', None) == self.edge and
                    getattr(other, 'node', None) == self.node)

        def __hash__(self):
            return hash(str(self.edge) + str(self.node))

    class Element:
        def __init__(self, data, type, depth = None):
            self.data = data
            self.type = type
            self.depth = depth

        def __eq__(self, other):
            return (isinstance(other, self.__class__) and
                    getattr(other, 'data', None) == self.data)

        def __hash__(self):
            return hash(str(self.data))

    class ElementType(Enum):
        NODE = 1
        EDGE = 2

    def __init__(self):
        self.elements = []

    def append_node(self, node, depth):
        element = Path.Element(node, Path.ElementType.NODE, depth)
        self.elements.append(element)

    def append_edge(self, edge):
        element = Path.Element(edge, Path.ElementType.EDGE)
        self.elements.append(element)

    def __repr__(self):
        path = ""
        for e in self.elements:
            if e.type == Path.ElementType.EDGE:
                edge = e.data.replace("|", "||")
                path += "|e{0}".format(edge)
            elif e.type == Path.ElementType.NODE:
                node = e.data.replace("|", "||")
                path += "|n{0}".format(node)
        return path

    def get_nodes(self):
        nodes = []
        for e in self.elements:
            if e.type == Path.ElementType.NODE:
                #nodes.append(e.data)
                nodes.append(e)
        return nodes

    def get_edges(self):
        edges = []
        for e in self.elements:
            if e.type == Path.ElementType.EDGE:
                edges.append(e.data)
        return edges

    def get_node(self, n):
        i = 0
        for e in self.elements:
            if e.type == Path.ElementType.NODE and n == i:
                return e.data
            if e.type == Path.ElementType.NODE:
                i += 1

    def get_edge(self, n):
        i = 0
        for e in self.elements:
            if e.type == Path.ElementType.EDGE and n == i:
                return e.data
            if e.type == Path.ElementType.EDGE:
                i += 1

    def get_pair(self, n):
        i = 0
        for e in range(len(self.elements)):
            if self.elements[e].type == Path.ElementType.EDGE and n == i:
                pair = Path.Pair(self.elements[e], self.elements[e+1])
                return pair
            if self.elements[e].type == Path.ElementType.EDGE:
                i += 1

    def get_pairs(self):
        pairs = []
        for e in range(len(self.elements)):
            if self.elements[e].type == Path.ElementType.EDGE:
                pair = Path.Pair(self.elements[e], self.elements[e+1])
                pairs.append(pair)
        return pairs

    def clone(self):
        return copy.deepcopy(self)

