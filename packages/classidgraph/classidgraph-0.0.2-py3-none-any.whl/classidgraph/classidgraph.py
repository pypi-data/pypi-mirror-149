# Copyright 2022 Linguistic Agents. All Rights Reserved.
#
# Licensed under the MIT License
# ==============================================================================
""" Graph module of 'classidgraph'.

Version 0.0.2

This module contains all classes of the Linrary:
Node, Link, Graph, NodeLevel and MultiVector

"""

import math
import numpy as np
from typing import List
Vector = List[float]

class Node:
    """ A node in a graph. """

    def __init__(self, class_ : str, id_ : str, features : Vector):
        super(Node, self).__init__()

        self.class_ = class_
        self.id_ = id_

        self.sources = {}
        self.goals = {}
        self.features = np.array(features)
        self.all_levels = []

    def set_source(self, link):
        source_cl = link.source.class_
        source_id = link.source.id_
        self.sources [(source_cl,source_id)] = link

    def set_goal(self, link):
        goal_cl = link.goal.class_
        goal_id = link.goal.id_
        self.goals [(goal_cl,goal_id)] = link

    def get_input_vector(self, level : int, n_vector : int):
        node_level : NodeLevel = self.all_levels[level]
        return  node_level.get_input_vector(n_vector = n_vector)

    def get_output_vector(self, level : int, n_vector : int):
        node_level : NodeLevel = self.all_levels[level]
        return  np.array(node_level.intrinsic.vector_list[n_vector])


    def get_all_sources(self):
        the_list = []
        the_keys = self.sources.keys()

        for (class_, id_) in the_keys:
            the_node = self.sources[ (class_, id_) ] 
            the_list.append(the_node)

        return  the_list   # returns a List containing all the Nodes linked to this Node
    
    def get_all_goals(self):
        the_list = []
        the_keys = self.goals.keys()

        for (class_, id_) in the_keys:
            the_node = self.goals[ (class_, id_) ]
            the_list.append(the_node)

        return  the_list  # Returns a List containing all the Nodes to wich this Node links

class Link:
    """ A link connecting two nodes in a graph. """

    def __init__(self, source : Node, goal : Node):
        """ Constructorfor the class Link. """
        super(Link, self).__init__()

        self.source : Node = source
        self.goal   : Node = goal

class Graph:
    def __init__(
                    self, 
                    num_classes : int, 
                    num_features : int
                ):
        super(Graph, self).__init__()

        self.num_classes = num_classes
        self.num_features = num_features
        self.class_vectors = {}
        self.links = {}
        self.nodes_by_class = {}

    def add_node_object(self, the_node : Node):
        class_ = the_node.class_
        if not class_ in self.nodes_by_class:
            self.nodes_by_class[class_] = {}

        node_by_id = self.nodes_by_class[class_]
        if not the_node.id_ in node_by_id:
            node_by_id[the_node.id_] = the_node

        return  self

    def add_node(self, class_ : str, id_ : str, features : Vector = []):
        if not class_ in self.nodes_by_class:
            self.nodes_by_class[class_] = {}

        node_by_id = self.nodes_by_class[class_]
        if not id_ in node_by_id:
            the_node = Node(class_ = class_, id_ = id_, features = self.adjust_features(features) )
            node_by_id[id_] = the_node

        self.add_node_object(the_node = node_by_id[id_])

        return  the_node

    def  add_link_between(self, source, goal):
        new_link = Link(source, goal)

        goal.set_source(new_link)
        source.set_goal(new_link)

        key = (new_link.source.class_, new_link.source.id_, new_link.goal.class_, new_link.goal.id_)
        self.links[key] = new_link

        return  self

    def  link(self, source_class : str, source_id : str, goal_class : str, goal_id : str):
        if not source_class in self.nodes_by_class:
            raise Exception("Unknown Source Class")
        if not goal_class in self.nodes_by_class:
            raise Exception("Unknown Goal Class")
            
        by_id = self.nodes_by_class[source_class]
        if not source_id in by_id:
            raise Exception("Unknown Source Id")
        source = by_id[source_id]        

        by_id = self.nodes_by_class[goal_class]
        if not goal_id in by_id:
            raise Exception("Unknown Goal Id")
        goal = by_id[goal_id]        

        self.add_link_between(source = source, goal = goal)

        return  self

    def get_node(self, class_ : str, id_ : str):
        by_id = self.nodes_by_class[class_] 
        the_node : Node = by_id[id_]
        return  the_node

    def get_all_nodes(self):
        the_list = []
        for cl in self.nodes_by_class:
            by_id = self.nodes_by_class[cl] 
            for id in by_id:
                the_node : Node = by_id[id]
                the_list.append(the_node)

        return  the_list

    def adjust_features(self, features : Vector):
        if self.num_features <= len(features):
            return  features[:self.num_features]
        else:
            return  features + [ 0.0 for i in range(self.num_features - len(features)) ]

    def get_all_classes(self):
        return list(self.nodes_by_class.keys())

    def conclude (self):
        """ Assign one-hot representation vectors to all classes """
        nClass = 0
        for cl in self.nodes_by_class:
            self.class_vectors[cl] = self.representation_of_class(class_code = nClass)
            if nClass < self.num_classes - 1:
                nClass += 1

    def representation_of_class(self, class_code : int):
        """ Return the one-hot representation of 'class_'  """
        num_classes = self.num_classes
        the_vector = np.zeros(num_classes, dtype=float)

        if class_code < num_classes:
            the_vector[class_code] = float(1.0)
        else:
            the_vector[num_classes - 1] = float(1.0)

        return  the_vector   

    def aggregate_data(self, level : int):
        all_nodes = self.get_all_nodes()
        for target_node in all_nodes:
            for o in target_node.sources:
                (class_, id_) = o
                source_node = self.get_node(class_ = class_, id_ = id_)
                self.add_incoming_vectors(source_node, target_node, level = level)
            for o in target_node.goals:
                (class_, id_) = o
                goal_node = self.get_node(class_ = class_, id_ = id_)
                self.add_outgoing_vectors(target_node, goal_node, level = level)

    def add_incoming_vectors(self, source : Node, this_node : Node, level : int):
        this_incoming : MultiVector = this_node.all_levels[level].incoming
        source_intrinsic : MultiVector = source.all_levels[level].intrinsic

        num_colors = len(this_incoming.vector_list)
        for c in range(num_colors):
            this_incoming.vector_list[c] = this_incoming.vector_list[c] + source_intrinsic.vector_list[c]

    def add_outgoing_vectors(self, this_node : Node, goal : Node, level : int):
        this_outgoing  : MultiVector = this_node.all_levels[level].outgoing
        goal_intrinsic : MultiVector = goal.all_levels[level].intrinsic

        num_colors = len(this_outgoing.vector_list)
        for c in range(num_colors):
            this_outgoing.vector_list[c] = this_outgoing.vector_list[c] + goal_intrinsic.vector_list[c]

class NodeLevel():
    """ Contains three multivectors. """

    def __init__(self, node : Node, level: int, num_vectors : int, num_elements : int):
        """
        Construct an object of the class 'NodeLevel'

        Crete three multivectors:
        (1) an incoming multivector
        (2) an inherent multivector, and 
        (3) outgoing multivector
        """
        super(NodeLevel, self).__init__()
        self.level : int = level
        self.num_vectors : int = num_vectors
        self.num_elements : int = num_elements

        self.incoming  : MultiVector = MultiVector(num_vectors=self.num_vectors, num_elements=self.num_elements)
        self.intrinsic : MultiVector = MultiVector(num_vectors=self.num_vectors, num_elements=self.num_elements)
        self.outgoing  : MultiVector = MultiVector(num_vectors=self.num_vectors, num_elements=self.num_elements)

        # reset the new node level
        self.set_center([np.zeros(self.num_elements) for c in range(self.num_vectors)]) 
        self.reset_incoming()
        self.reset_outgoing()

    def set_center(self, for_all_vectors : List[Vector]):
        for n_vector in range(self.num_vectors):   
            self.set_center_for_vector(n_vector = n_vector, the_vector = for_all_vectors[n_vector])

    def set_center_for_vector(self, n_vector : int, the_vector : Vector):
        target : Vector = self.intrinsic.vector_list[n_vector]

        for d in range(len(the_vector)):
            target[d] = the_vector[d]

    def  reset_incoming(self):
        for n_vector in range(self.num_vectors):     
            self.incoming.vector_list[n_vector] = np.zeros(self.num_elements)

    def  reset_outgoing(self):
        for n_vector in range(self.num_vectors):     
            self.outgoing.vector_list[n_vector] = np.zeros(self.num_elements)

    def  get_input_vector(self, n_vector : int) -> Vector:
        input_vector = []

        for i in range(n_vector, self.num_vectors):
            incoming = self.incoming.vector_list[i]
            for n_element in range(self.num_elements):
                input_vector.append(incoming[n_element])

        for i in range(0, n_vector + 1):
            outgoing = self.outgoing.vector_list[i]
            for n_element in range(self.num_elements):
                input_vector.append(outgoing[n_element])

        return  np.array(input_vector)

class MultiVector:
    """ Collection of vectors
    """
    def __init__(self, num_vectors : int, num_elements : int):
        """
        The constructor of the class 'MultiVector'

        The size of each vector is given by the parameter 'num_elements'
        The number of vectors is given by the parameter 'num_elements'.
        """
        self.vector_list : List[Vector] = [ self.new_vector(num_elements = num_elements) for c in range(num_vectors) ]

    def new_vector(self, num_elements : int) -> Vector:
        return  np.array([ float(0) for d in range(num_elements)])

    """
    def add(self, multivector):
        for i in range(len(self.vector_list)):
            self.vector_list[i] = self.vector_list[i] + multivector.vector_list[i]
    """




