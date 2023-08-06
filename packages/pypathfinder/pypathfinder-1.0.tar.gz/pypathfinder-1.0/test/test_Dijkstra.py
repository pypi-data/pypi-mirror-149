from unittest import TestCase, main

from ex import example1, example2
from pypathfinder.Dijkstra import Node, bestpath
"""
def example() -> Tuple[Node, Node]:
    # https://de.wikipedia.org/wiki/Dijkstra-Algorithmus#Beispiel_mit_bekanntem_Zielknoten
    frankfurt = Node("Frankfurt")
    mannheim = Node("Mannheim")
    kassel = Node("Kassel")
    wuerzburg = Node("Würzburg")
    frankfurt.connect({mannheim: 85, wuerzburg: 217, kassel: 173}, True)

    karlsruhe = Node("Karlsruhe")
    mannheim.connect({karlsruhe:80}, True)

    erfurt = Node("Erfurt")
    nuernberg = Node("Nürnberg")
    wuerzburg.connect({erfurt: 186, nuernberg: 103}, True)

    stuttgart = Node("Stuttgart")
    nuernberg.connect({stuttgart: 183}, True)

    augsburg = Node("Augsburg")
    karlsruhe.connect({augsburg: 250}, True)

    muenchen = Node("München")
    muenchen.connect({augsburg: 84, nuernberg: 167, kassel: 502}, True)
    return frankfurt, muenchen
"""
class TestDijkstra(TestCase):
    def test_bestpath1(self):
        frankfurt, muenchen = example1(Node)
        path = bestpath(frankfurt, muenchen)
        self.assertEqual(path, [Node("Frankfurt"), Node("Würzburg"), Node("Nürnberg"), Node("München")])
        self.assertEqual(path[-1].cost, 487)
    
    def test_bestpath2(self):
        frankfurt, muenchen = example1(Node)
        path = bestpath(frankfurt, muenchen, True)
        self.assertEqual(path, [Node("Frankfurt"), Node("Würzburg"), Node("Nürnberg"), Node("München")])
        self.assertEqual(path[-1].cost, 487)
    
    def test_bestpath3(self): #TODO
        start, stop, matrix, solution = example2(Node, 2)
        path = bestpath(start, stop, True)
        self.assertEqual(path[-1].cost, solution)

if __name__ == "__main__":
    main()