# Pathfinding

This package provides a pure Python implementation for Dijkstra and A-Star as well as a faster Cython implementation.

## Using the pure Python Djikstra

````Python
from pypathfinder.Dijkstra import Node, bestpath
def example_nodesystem():
    # https://de.wikipedia.org/wiki/Dijkstra-Algorithmus#Beispiel_mit_bekanntem_Zielknoten
    frankfurt = Node("Frankfurt")
    mannheim = Node("Mannheim")
    kassel = Node("Kassel")
    wuerzburg = Node("Würzburg")
    frankfurt.connect({mannheim: 85, wuerzburg: 217, kassel: 173}, True)
    # True value results in connecting all the given Nodes to frankfurt and back with the same cost
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

frankfurt, muenchen = example_nodesystem()
path = bestpath(frankfurt, muenchen)
# path includes start and endpoint
# all Nodes have a cost value now
````
## Using the Cython Djikstra

````Python
from pypathfinder.fast import CNode, djikstra_bestpath
def example_nodesystem():
    # https://de.wikipedia.org/wiki/Dijkstra-Algorithmus#Beispiel_mit_bekanntem_Zielknoten
    frankfurt = CNode("Frankfurt")
    mannheim = CNode("Mannheim")
    kassel = CNode("Kassel")
    wuerzburg = CNode("Würzburg")
    frankfurt.connect({mannheim: 85, wuerzburg: 217, kassel: 173}, True)

    karlsruhe = CNode("Karlsruhe")
    mannheim.connect({karlsruhe:80}, True)

    erfurt = CNode("Erfurt")
    nuernberg = CNode("Nürnberg")
    wuerzburg.connect({erfurt: 186, nuernberg: 103}, True)

    stuttgart = CNode("Stuttgart")
    nuernberg.connect({stuttgart: 183}, True)

    augsburg = CNode("Augsburg")
    karlsruhe.connect({augsburg: 250}, True)

    muenchen = CNode("München")
    muenchen.connect({augsburg: 84, nuernberg: 167, kassel: 502}, True)
    return frankfurt, muenchen

frankfurt, muenchen = example_nodesystem()
path = bestpath(frankfurt, muenchen)
# path includes start and endpoint
# all Nodes have a cost value now
````