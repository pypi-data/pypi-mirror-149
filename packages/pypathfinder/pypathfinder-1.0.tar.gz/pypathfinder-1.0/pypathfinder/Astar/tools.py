from heapq import heappop, heappush
from typing import Callable, Dict, Hashable, List, Union
from pypathfinder.utils import LowComby, HighComby, get_pop, get_push
from pypathfinder.Dijkstra import Node, construct

class ANode(Node):
    def __init__(self, id: Hashable, connections: Dict["ANode", int] = None):
        super().__init__(id, connections)
        self.probable_cost = float("inf")
        self._connections: Dict[ANode, int]
    
    def __str__(self) -> str:
        return f"Node(id={self.id}, cost={self.cost}, probable_cost={self.probable_cost})"
    
    def __hash__(self) -> int:
        return super().__hash__()
    
    def __lt__(self, other):
        if not isinstance(other, type(self)):
            raise NotImplemented
        return self.probable_cost < other.probable_cost
    
    def __le__(self, other):
        if not isinstance(other, type(self)):
            raise NotImplemented
        return self.probable_cost <= other.probable_cost
    
    def __gt__(self, other):
        if not isinstance(other, type(self)):
            raise NotImplemented
        return self.probable_cost > other.probable_cost

    def __ge__(self, other):
        if not isinstance(other, type(self)):
            raise NotImplemented
        return self.probable_cost >= other.probable_cost
    
    def connect(self, conn: Dict["ANode", int], reflect: bool = False):
        return super().connect(conn, reflect)
    

def bestpath(startnode: ANode, endnode: ANode, func: Callable, first_contact: bool = False, queue_type: Union[list, LowComby, HighComby]=list, args: list = None) -> List[ANode]:
    """
    Args:
        startnode: starting point
        endnode: ending point
        first_contact: if True, pathfinding will end as soon as the endnode has first been discoverd
        queue_type: type used for queueing nodes; LowComby can be faster but consumes more memory
    
    Returns:
        list of nodes, creating a path
    """
    if args is None:
        args = []
    
    # get costs
    startnode.cost = startnode.probable_cost = 0
    queue: Union[List[ANode], LowComby] = queue_type()
    queue.append(startnode)
    use_heappop = get_pop(queue)
    use_heappush = get_push(queue)

    while len(queue) != 0:
        currentnode = use_heappop(queue)
        for node, cost in currentnode._connections.items():
                
            new_cost = currentnode.cost + cost
            if new_cost < node.cost:
                node.cost = new_cost
                node.probable_cost = new_cost+ func(node, args)
                if node not in queue:
                    use_heappush(queue, node)
                    #queue.append(node)

        if endnode.cost <= currentnode.probable_cost:
            break
        if first_contact and currentnode is endnode:
            break
    
    # get path
    return construct(startnode, endnode)