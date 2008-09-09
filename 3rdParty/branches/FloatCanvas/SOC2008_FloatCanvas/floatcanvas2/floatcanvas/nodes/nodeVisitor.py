from ..patterns.asSequence import asSequence

class NodeVisitor(object):
    ''' Derive from this class to visit a tree of nodes and override the pre-
         and postVisit methods to implement the custom behaviour.
        Traversal is depth-first.
    '''
    def __init__(self, visitChildren = True):
        ''' If visitChildren is True then child nodes will be visited, else not
        '''
        self.visitChildren = visitChildren
    
    def preVisit(self, node):
        ''' This is called when a node is visited, before the children are
            going to be visited
        '''        
        return True
    
    def postVisit(self, node):
        ''' This is called when a node is visited, after the children were
            visited
        '''        
        return True
    
    def visit(self, nodes):
        ''' This is the method you should call to do the work. Nodes is a
            sequence of nodes
        '''
        for node in asSequence(nodes):
            if not node.visit(self, self.visitChildren):
                return False
        return True
    
    
class TextTreeFormatVisitor(NodeVisitor):
    ''' Outputs a formatted tree of nodes to a stream, useful for debugging '''
    def __init__(self, stream, indentString = ' -> ', visitChildren = True):
        super(TextTreeFormatVisitor, self).__init__( visitChildren )
        self.level = 0
        self.stream = stream
        self.indentString = indentString
    
    def preVisit(self, node):
        self.level += 1
        indent = self.indentString * (self.level - 1)
        self.stream.write( '%s%s\n' % (indent, node.name) )
        self.stream.flush()
        
        return True
    
    def postVisit(self, node):
        self.level -= 1
        return True


class GetNodesAsFlatListVisitor(NodeVisitor):
    ''' Simply returns the node tree in a flat list which will be stored in the
         .nodes property.
    '''
    def __init__(self, visitChildren = True):
        super(GetNodesAsFlatListVisitor, self).__init__( visitChildren )
        self.nodes = []
        
    def preVisit(self, node):
        self.nodes.append( node )
        return True
    
    
class FindNodesByNamesVisitor(NodeVisitor):
    ''' Input a sequence of names and find all nodes in a tree which match them.
        Output is stored in the .nodes property.
    '''
    def __init__(self, names, visitChildren = True):
        super(FindNodesByNamesVisitor, self).__init__( visitChildren )
        self.names = names
        self.nodes = []
        
    def preVisit(self, node):
        if node.name in self.names:
            self.nodes.append( node )
        
        return True
    
    
class EnumerateNodesVisitor(NodeVisitor):
    ''' Enumerates the nodes with numbers from 0 to n. Each node is assigned a
        number in the order they're visited.
        Later the number of a node, or the node belonging to a number can be
        retrieved.
    '''
    def __init__(self, visitChildren = True):
        super( EnumerateNodesVisitor, self ).__init__( visitChildren )
        self.node_to_number = {}
        self.number_to_node = {}
        self.current_number = 0
        
    def preVisit(self, node):
        ''' Insert node to our bookkeeping and increment the number '''
        self.node_to_number[node] = self.current_number
        self.number_to_node [self.current_number] = node
        self.current_number += 1
        return True
    
    def getPosition(self, node):
        ''' Returns the number of a given node '''
        return self.node_to_number[node]
    
    def getNode(self, position):
        ''' Returns the node of a given number '''
        return self.number_to_node[position]
