#!/usr/bin/env python
# coding: utf-8

# In[1]:


### Max Clique problem
### Maximum Independent Set
### Minimum Vertex Cover
### it is a maximal clique or maximal complete subgraph in the complementary graph.


import sys
import os
import networkx as nx
import networkx as nx
import numpy as np
import copy
import time
from itertools import tee, chain
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QLabel
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import (QWidget, QPushButton, QFrame,QColorDialog, QApplication)
from PyQt5.QtGui import QColor


### Opening the GUI file which is being saved at the same folder of this program
### qtcreator_file would store the GUI file name...
qtcreator_file  = "GraphGUI.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        
        canvas = QtGui.QPixmap(2000,2000)
        self.label.setPixmap(canvas)
        self.nod=0
        self.edge=0
        self.del1=0
        self.save=0
        self.open=0
        self.clicked=0
        self.mov=0
        self.del2=0
        self.color=0
        self.changenodec=0
        self.changeedgec=0
        self.pencolor="#ffffff"
        self.pencolorchange="#ffffff"
        self.match=0
        ### connecting the function to the Option in Menu in GUI which is being clicked
        self.actionNew.triggered.connect(self.blankscreen)
        self.actionOpen.triggered.connect(self.opengraph)
        self.actionSave_File.triggered.connect(self.savegraph)
        self.actionAdd_Node.triggered.connect(self.addnode)
        self.actionAdd_Edge.triggered.connect(self.addedge)
        self.actionDelete_Node.triggered.connect(self.deletenode)
        self.actionDelete_Edge.triggered.connect(self.deleteedge)
        self.actionMove_Node.triggered.connect(self.movenode)
        self.actionSet_Pen_Color.triggered.connect(self.showColorMenu)
        self.actionChange_Node_Color.triggered.connect(self.changeNodeColor)
        self.actionChange_Edge_Color.triggered.connect(self.changeEdgeColor)
        self.actionFind_Maximal_Matching.triggered.connect(self.Maximum_Edge_Matching)
        self.actionMaximum_Matching.triggered.connect(self.Maximum_Edge_Matching)
        self.actionMaximum_Clique.triggered.connect(self.Max_Clique)
        self.actionMaximum_Vertex_Cover.triggered.connect(self.Max_Vertex_Cover)
        self.actionMaximum_Independent_Set.triggered.connect(self.Max_Independent_Set)
        ### connecting the function to the Button in GUI which is being clicked
        self.Add_Vertex.clicked.connect(self.addnode)
        self.AddEdge.clicked.connect(self.addedge)
        self.DelNode.clicked.connect(self.deletenode)
        self.DelEdge.clicked.connect(self.deleteedge)
        self.move.clicked.connect(self.movenode)
        self.changecolor.clicked.connect(self.showColorMenu)
        self.changeNodeCol.clicked.connect(self.changeNodeColor)
        self.changeEdgeCol.clicked.connect(self.changeEdgeColor)
        self.maxMatch.clicked.connect(self.Maximum_Edge_Matching)
        self.initUI()
     
    
    ### Defining self.nod =0 means if self.nod is 1 then in the mouse release event method
    ### will add a node to the graph till any other operation is not declared by gui window user
    ### A nod will be added in the variable self.vertex.........
    def addnode(self):
        if self.nod==0:
            self.nod=1
            self.edge=0
            self.del1=0
            self.mov=0
            self.del2=0
            self.color=0
            self.changenodec=0
            self.changeedgec=0
            self.match=0
            self.update()
            
    ### Defining self.edge =0 means if self.edge is 1 then in the mouse release event method
    ### A edge will be added in the variable self.edge.........
    def addedge(self):
        if self.edge==0:
            self.edge=1
            self.nod=0
            self.del1=0
            self.mov=0
            self.del2=0
            self.color=0
            self.changenodec=0
            self.changeedgec=0
            self.match=0
            self.update()
            
    def deletenode(self):
        if self.del1==0:
            self.del1=1
            self.nod=0
            self.edge=0
            self.mov=0
            self.del2=0
            self.color=0
            self.changenodec=0
            self.changeedgec=0
            self.match=0
            self.update()
            
    def deleteedge(self):
        if self.del2==0:
            self.del2=1
            self.del1=0
            self.nod=0
            self.edge=0
            self.mov=0
            self.color=0
            self.changenodec=0
            self.changeedgec=0
            self.match=0
            self.update()
            
    def movenode(self):
        if self.mov==0:
            self.mov=1
            self.del1=0
            self.nod=0
            self.edge=0
            self.del2=0
            self.color=0
            self.changenodec=0
            self.changeedgec=0
            self.match=0
            self.update()
    
    
    ### Now From here starts Max Clique Code



    
    
    ### This is a recursive method....
    ### python does not allow more than 999 recursion
    ### since algorithm's coplexity is O(V^2*E) so it doesn't give maximum matching for 
    ### V^2*E >= 1000
    def find_maximum_matching(self,G,M):
        P = self.finding_aug_path(G,M)
        if P == []:    ### Base Case
            return M
        else:   ### Augment P to M
                ### Add the alternating edges of P to M
            for i in range(0,len(P)-2,2): 
                M.add_edge(P[i],P[i+1])
                M.remove_edge(P[i+1],P[i+2])
            M.add_edge(P[-2],P[-1])
            return self.find_maximum_matching(G,M)
    
    ### Returns the distance of the node to the root of the tree to which tree this node belongs
    def dist_to_root(self,point,root,Graph):
        path = nx.shortest_path(Graph, source = point, target = root)
        return (len(path)-1)
    
    
    def finding_aug_path(self,G,M,Blossom_stack=[]):
        Forest = [] #Storing the Forests
        Path = [] # The final path 

        unmarked_edges = list(set(G.edges()) - set(M.edges()))
        unmarked_nodes = list(G.nodes())
        Forest_nodes = []
        ## we need a map from v to the tree
        tree_to_root = {} # key=idx of tree in forest, val=root
        root_to_tree = {} # key=root, val=idx of tree in forest

        ##List of exposed vertices - ROOTS OF TREES
        exp_vertex = list(set(G.nodes()) - set(M.nodes()))

        counter = 0
        #List of trees with the exposed vertices as the roots
        for v in exp_vertex:  
            temp = nx.Graph()
            temp.add_node(v)
            Forest.append(temp)
            Forest_nodes.append(v)

            #link each root to its tree
            tree_to_root[counter] = v
            root_to_tree[v] = counter
            counter = counter + 1


        for v in Forest_nodes:  
            root_of_v = None
            tree_num_of_v = None
            for tree_number in range(len(Forest)): 
                tree_in = Forest[tree_number]
                if tree_in.has_node(v) == True:
                    root_of_v = tree_to_root[tree_number]
                    tree_num_of_v = tree_number
                    break #Break out of the for loop
            edges_v = list(G.edges(v))
            for edge_number in range(len(edges_v)): 
                e = edges_v[edge_number]
                e2 = (e[1],e[0]) #the edge in the other order
                if ((e in unmarked_edges or e2 in unmarked_edges) and e!=[]):
                    w = e[1] # the other vertex of the unmarked edge
                    w_in_Forest = 0; ##Indicator for w in F or not

                    ##Go through all the trees in the forest to check if w in F
                    tree_of_w = None
                    tree_num_of_w = None
                    for tree_number in range(len(Forest)):
                        tree = Forest[tree_number]
                        if tree.has_node(w) == True:
                            w_in_Forest = 1
                            root_of_w = tree_to_root[tree_number]
                            tree_num_of_w = tree_number
                            tree_of_w = Forest[tree_num_of_w]
                            break #Break the outer for loop

                    if w_in_Forest == 0:
                        ## w is matched, so add e and w's matched edge to F
                        Forest[tree_num_of_v].add_edge(e[0],e[1]) # edge {v,w}
                        # Note: we don't add w to forest nodes b/c it's odd dist from root
                        #assert(M.has_node(w))
                        edge_w = list(M.edges(w))[0] # get edge {w,x}
                        Forest[tree_num_of_v].add_edge(edge_w[0],edge_w[1]) # add edge{w,x}
                        Forest_nodes.append(edge_w[1]) ## add {x} to the list of forest nodes

                    else: ## w is in Forest
                        # if odd, do nothing.
                        if self.dist_to_root(w,root_of_w,Forest[tree_num_of_w])%2 == 0:
                            if (tree_num_of_v != tree_num_of_w):
                                ##Shortest path from root(v)--->v-->w---->root(w)
                                path_in_v = nx.shortest_path(Forest[tree_num_of_v], source = root_of_v, target = v)
                                path_in_w = nx.shortest_path(Forest[tree_num_of_w], source = w, target = root_of_w)

                                return path_in_v + path_in_w
                            else: ##Contract the blossom
                                # create blossom
                                blossom = nx.shortest_path(tree_of_w, source=v, target=w)
                                blossom.append(v)
                                #assert(len(blossom)%2 == 0)
                                # contract blossom into single node w
                                contracted_G = copy.deepcopy(G)
                                contracted_M = copy.deepcopy(M)
                                for node in blossom[0:len(blossom)-1]:
                                    if node != w:
                                        contracted_G = nx.contracted_nodes(contracted_G, w, node, self_loops=False)
                                        if node in contracted_M.nodes(): 
                                            edge_rm = list(M.edges(node))[0] #this will be exactly one edge
                                            contracted_M.remove_node(node)
                                            contracted_M.remove_node(edge_rm[1])
                                           #assert(len(list(contracted_M.nodes()))%2 == 0)
                                # add blossom to our stack
                                Blossom_stack.append(w)

                                # recurse
                                aug_path = self.finding_aug_path(contracted_G, contracted_M, Blossom_stack)

                                # check if blossom exists in aug_path 
                                v_B = Blossom_stack.pop()
                                if (v_B in aug_path):
                                    ##Define the L_stem and R_stem
                                    L_stem = aug_path[0:aug_path.index(v_B)]
                                    R_stem = aug_path[aug_path.index(v_B)+1:]
                                    lifted_blossom = [] #stores the path within the blossom to take
                                    # Find base of blossom
                                    i = 0
                                    base = None
                                    base_idx = -1
                                    blossom_ext = blossom + [blossom[1]] 
                                    while base == None and i < len(blossom) - 1:
                                        if not(M.has_edge(blossom[i],blossom[i+1])):
                                            if not(M.has_edge(blossom[i+1],blossom_ext[i+2])): 
                                                base = blossom[i+1]
                                                base_idx = i+1
                                            else:
                                                i += 2
                                        else:
                                            i += 1
                                    # if needed, create list of blossom nodes starting at base
                                    if blossom[0] != base:
                                        based_blossom = []
                                        base_idx = blossom.index(base)
                                        for i in range(base_idx,len(blossom)-1):
                                            based_blossom.append(blossom[i])
                                        for i in range(0,base_idx):
                                            based_blossom.append(blossom[i])
                                        based_blossom.append(base)
                                    else:
                                        based_blossom = blossom

                                    # CHECK IF BLOSSOM IS ENDPT
                                    if L_stem == [] or R_stem == []:
                                        if L_stem != []:
                                            if G.has_edge(base, L_stem[-1]):
                                                # CASE 1:
                                                # Chuck the blossom
                                                return L_stem + [base]
                                            else:
                                                # CASE 2:
                                                # find where Lstem is connected
                                                i = 1
                                                while (lifted_blossom == []):
                                                    #assert(i < len(based_blossom)-1)
                                                    if G.has_edge(based_blossom[i],L_stem[-1]):
                                                        # make sure we're adding the even part to lifted path
                                                        if i%2 == 0: # same dir path
                                                            lifted_blossom = list(reversed(based_blossom))[-i-1:] ####################
                                                        else: # opposite dir path
                                                            lifted_blossom = based_blossom[i:]##########################
                                                    i += 1
                                                return L_stem + lifted_blossom

                                        else:
                                            if G.has_edge(base, R_stem[0]):
                                                # CASE 1:
                                                # Chuck the blossom. 
                                                return [base] + R_stem
                                            else:
                                                # CASE 2:
                                                # find where R_stem is connected
                                                i = 1
                                                while (lifted_blossom == []):
                                                    #assert(i < len(based_blossom)-1)
                                                    if G.has_edge(based_blossom[i],R_stem[0]):
                                                        # make sure we're adding the even part to lifted path
                                                        if i%2 == 0: # same dir path
                                                            lifted_blossom = based_blossom[:i+1]
                                                            #print lifted_blossom
                                                        else: # opposite dir path
                                                            lifted_blossom = list(reversed(based_blossom))[:-i]
                                                    i += 1
                                                return lifted_blossom + R_stem

                                    else: # blossom is in the middle
                                        # LIFT the blossom
                                        # check if L_stem attaches to base
                                        if M.has_edge(base, L_stem[-1]):
                                            # find where right stem attaches
                                            if G.has_edge(base, R_stem[0]):
                                                # blossom is useless
                                                return L_stem + [base] + R_stem
                                            else:
                                                # blossom needs to be lifted
                                                i = 1
                                                while (lifted_blossom == []):
                                                    # assert(i < len(based_blossom)-1)
                                                    if G.has_edge(based_blossom[i],R_stem[0]):
                                                        # make sure we're adding the even part to lifted path
                                                        if i%2 == 0: # same dir path
                                                            lifted_blossom = based_blossom[:i+1] 
                                                            # print lifted_blossom
                                                        else: # opposite dir path
                                                            lifted_blossom = list(reversed(based_blossom))[:-i]
                                                            # print lifted_blossom
                                                    i += 1
                                                return L_stem + lifted_blossom + R_stem
                                        else: 
                                            # R stem to base is in matching
                                            # assert(M.has_edge(base, R_stem[0]))
                                            # check where left stem attaches
                                            if G.has_edge(base, L_stem[-1]):
                                                # blossom is useless
                                                return L_stem + [base] + R_stem
                                            else:
                                                # blossom needs to be lifted
                                                i = 1
                                                while (lifted_blossom == []):
                                                    # assert(i < len(based_blossom)-1)
                                                    if G.has_edge(based_blossom[i],L_stem[-1]):
                                                        # make sure we're adding the even part to lifted path
                                                        if i%2 == 0: # same dir path
                                                            lifted_blossom = list(reversed(based_blossom))[-i-1:] 
                                                        else: # opposite dir path
                                                            lifted_blossom = based_blossom[i:] 
                                                    i += 1
                                                return L_stem + list((lifted_blossom)) + R_stem
                                else: # blossom is not in aug_path
                                    return aug_path
        ##IF Nothing is Found
        return Path ##Empty Path

    
    
    '''def is_iterator(obj):
        has_next_attr = hasattr(obj, '__next__') or hasattr(obj, 'next')
        return iter(obj) is obj and has_next_attr'''
    
    def is_iterator(self, obj):
        has_next_attr = hasattr(obj, '__next__') or hasattr(obj, 'next')
        return iter(obj) is obj and has_next_attr
    
    def arbitrary_element(self, iterable):
        if self.is_iterator(iterable):
            raise ValueError('cannot return an arbitrary item from an iterator')
        # Another possible implementation is ``for x in iterable: return x``.
        return next(iter(iterable))


    def ramsey_R2(self, G):
        if not G:
            return set(), set()

        node = self.arbitrary_element(G)
        nbrs = nx.all_neighbors(G, node)
        nnbrs = nx.non_neighbors(G, node)
        c_1, i_1 = self.ramsey_R2(G.subgraph(nbrs).copy())
        c_2, i_2 = self.ramsey_R2(G.subgraph(nnbrs).copy())

        c_1.add(node)
        i_2.add(node)
        # Choose the larger of the two cliques and the larger of the two
        # independent sets, according to cardinality.
        return max(c_1, c_2, key=len), max(i_1, i_2, key=len)

    def max_clique(self, G):
        if G is None:
            raise ValueError("Expected NetworkX graph!")

        # finding the maximum clique in a graph is equivalent to finding
        # the independent set in the complementary graph
        cgraph = nx.complement(G)
        iset, _ = self.clique_removal(cgraph)
        return iset


    def clique_removal(self, G):
        graph = G.copy()
        c_i, i_i = self.ramsey_R2(graph)
        cliques = [c_i]
        isets = [i_i]
        while graph:
            graph.remove_nodes_from(c_i)
            c_i, i_i = self.ramsey_R2(graph)
            if c_i:
                cliques.append(c_i)
            if i_i:
                isets.append(i_i)
        # Determine the largest independent set as measured by cardinality.
        maxiset = max(isets, key=len)
        return maxiset, cliques


    ##@not_implemented_for('directed')
    ##@not_implemented_for('multigraph')
    def large_clique_size(self, G):
        degrees = G.degree

        def _clique_heuristic(G, U, size, best_size):
            if not U:
                return max(best_size, size)
            u = max(U, key=degrees)
            U.remove(u)
            N_prime = {v for v in G[u] if degrees[v] >= best_size}
            return _clique_heuristic(G, U & N_prime, size + 1, best_size)

        best_size = 0
        nodes = (u for u in G if degrees[u] >= best_size)
        for u in nodes:
            neighbors = {v for v in G[u] if degrees[v] >= best_size}
            best_size = _clique_heuristic(G, neighbors, 1, best_size)
        return best_size

    
    def Maximum_Edge_Matching(self):
        if self.match==0:
            self.match=1
            self.mov=0
            self.del1=0
            self.nod=0
            self.edge=0
            self.del2=0
            self.color=0
            self.changenodec=0
            self.changeedgec=0
            self.update()
            
            
        for i in range(len(self.vertex)):
            print(self.vertex[i][0], self.vertex[i][1])
            
        listt=[]
        for i in range(len(self.vertex)):
            listt.append((self.vertex[i][0], self.vertex[i][1]))
        print(listt)
        
        #print(type(self.vertex[0]))
        ### Creating a normal graph by networkx library
        G = nx.Graph()
        ### Adding the nodes in the graph in the form (x,y)
        for i in range(len(self.vertex)):
            G.add_node((self.vertex[i][0],self.vertex[i][1]))
        ### Adding edges in the graph in the form ((x1,y1),(x2,y2))
        for i in range(len(self.edges)):
            G.add_edge((self.edges[i][0][0],self.edges[i][0][1]),(self.edges[i][1][0],self.edges[i][1][1]))
            
            
            
        ### print("Max Independ", nx.maximal_independent_set(G))
        
        #print(self.max_clique(G))
        ### Checking Other Operations at the same time also.....
        print("Max Clique")
        MCq = self.max_clique(G)
        print(type(MCq),' ',type(G))
        print(MCq)
         
        print("Max Independent")
        II = nx.complement(G)
        ISt = self.max_clique(II)
        print(ISt)
        
        print("Min vertex cover")
        VC = [x for x in listt if x not in ISt]
        print(VC)
        
                
        
        ### Just clarifying our generated graph...
        print("Total Nodes ", G.number_of_nodes())
        print("Total Edges ", G.number_of_edges())
        ### Creating an empty augumenting path to which we would add edges
        ### If no more vertex can be added that would be our maximum matching
        M = nx.Graph()
        ### Here MM is our maximum matching
        MM = self.find_maximum_matching(G, M)
        
        ### Just clarifying Maximum Matching Nodes and Edges...
        print("Maximum Matching Nodes ", end = ' ')
        for jj in list(MM.nodes()):
            print(jj, end = ' ')
        print()
        
        
    
        
        
        ### Setting color to exposed vertices to Green and which are in the matching to Red
        ### Setting color to edges which are in matching to Blue and which re not in 
        ### matching to white...
        ### First Color to white all vertices......
        for ii in range(len(self.vertex)):
            self.nodecolor[ii] = "#55aa00"
        Exposed_Vertices = list(set(G.nodes())-set(MM.nodes()))
        for ii in Exposed_Vertices:
            for jj in range(len(self.vertex)):
                if(ii[0]==self.vertex[jj][0] and ii[1]==self.vertex[jj][1]):
                    self.nodecolor[jj] = "#55aa00"
        for ii in list(MM.nodes()):
            for jj in range(len(self.vertex)):
                if(ii[0]==self.vertex[jj][0] and ii[1]==self.vertex[jj][1]):
                    self.nodecolor[jj] = "#ff0000"
        
        print("All Edges ")
        for ii in list(G.edges()):
            print(ii)
        print()
        
        print("Maximum Matching Edges ")
        for ii in list(MM.edges()):
            print(ii)
        print()
        
        for ii in range(len(self.edges)):
            self.edgecolor[ii] = "#ffffff"
        
        
        
        for ii in list(MM.edges()):
            for jj in range(len(self.edges)):
                flag1 = False
                flag2 = False
                if(ii[0][0]==self.edges[jj][0][0] and ii[0][1]==self.edges[jj][0][1] and 
                           ii[1][0]==self.edges[jj][1][0] and ii[1][1]==self.edges[jj][1][1]):
                    flag1 = True
                if(ii[1][0]==self.edges[jj][0][0] and ii[1][1]==self.edges[jj][0][1] and 
                           ii[0][0]==self.edges[jj][1][0] and ii[0][1]==self.edges[jj][1][1]):
                    flag2 = True
                if(flag1 or flag2):
                    self.edgecolor[jj] = "#5500ff"
        
        print("type self.edges ", type(self.edges))
        
        ### Now update all things to reprint all the changes of colorings...
        self.update()
        
    
    def Max_Clique(self):
        #print(type(self.vertex[0]))
        
        ### Just color changing to White of all Edges and Nodes.....
        for ii in range(len(self.vertex)):
            self.nodecolor[ii] = "#ffffff"
        for ii in range(len(self.edges)):
            self.edgecolor[ii] = "#ffffff"
            
        ### Creating a normal graph by networkx library
        G = nx.Graph()
        ### Adding the nodes in the graph in the form (x,y)
        for i in range(len(self.vertex)):
            G.add_node((self.vertex[i][0],self.vertex[i][1]))
        ### Adding edges in the graph in the form ((x1,y1),(x2,y2))
        for i in range(len(self.edges)):
            G.add_edge((self.edges[i][0][0],self.edges[i][0][1]),(self.edges[i][1][0],self.edges[i][1][1]))
            
        #print("Max Independ", nx.maximal_independent_set(G))
        
        #print(self.max_clique(G))
        print("Max Clique")
        MCq = self.max_clique(G)
        print(type(MCq),' ',type(G))
        print(MCq)
        
        ### Initializin  colors of all edges and vertices to default
        for ii in range(len(self.vertex)):
            self.nodecolor[ii] = "#55aa00"
        for ii in range(len(self.edges)):
            self.edgecolor[ii] = "#ffffff"
        
        
        ### Changing color of all Vertices in Max Clique
        for ii in MCq:
            for jj in range(len(self.vertex)):
                if(ii[0]==self.vertex[jj][0] and ii[1]==self.vertex[jj][1]):
                    self.nodecolor[jj] = "#ff0000"
                    
               
        ### Changing color of all Edges in Max Clique
        for xx in MCq:
            for yy in MCq:
                if xx != yy:
                    for jj in range(len(self.edges)):
                        flag1 = False
                        flag2 = False
                        if(xx[0]==self.edges[jj][0][0] and xx[1]==self.edges[jj][0][1] and 
                                   yy[0]==self.edges[jj][1][0] and yy[1]==self.edges[jj][1][1]):
                            flag1 = True
                        if(yy[0]==self.edges[jj][0][0] and yy[1]==self.edges[jj][0][1] and 
                                   xx[0]==self.edges[jj][1][0] and xx[1]==self.edges[jj][1][1]):
                            flag2 = True
                        if(flag1 or flag2):
                            self.edgecolor[jj] = "#5500ff"
                    
        #########----------------------------------
        self.update()
            
            
            
    
    def Max_Independent_Set(self):
        #print(type(self.vertex[0]))
        
        ### Just color changing to White of all Edges and Nodes.....
        for ii in range(len(self.vertex)):
            self.nodecolor[ii] = "#ffffff"
        for ii in range(len(self.edges)):
            self.edgecolor[ii] = "#ffffff"
            
        ### Creating a normal graph by networkx library
        G = nx.Graph()
        ### Adding the nodes in the graph in the form (x,y)
        for i in range(len(self.vertex)):
            G.add_node((self.vertex[i][0],self.vertex[i][1]))
        ### Adding edges in the graph in the form ((x1,y1),(x2,y2))
        for i in range(len(self.edges)):
            G.add_edge((self.edges[i][0][0],self.edges[i][0][1]),(self.edges[i][1][0],self.edges[i][1][1]))
            
        ### print("Max Independ", nx.maximal_independent_set(G))
        
        #print(self.max_clique(G))
        print("Max Independent")
        II = nx.complement(G)
        ISt = self.max_clique(II)
        print(ISt)
        print(type(ISt))
        
        for ii in range(len(self.vertex)):
            self.nodecolor[ii] = "#ffffff"
        for ii in range(len(self.edges)):
            self.edgecolor[ii] = "#ffffff"
        
        for ii in ISt:
            for jj in range(len(self.vertex)):
                if(ii[0]==self.vertex[jj][0] and ii[1]==self.vertex[jj][1]):
                    self.nodecolor[jj] = "#ff0000"
                    
                    
        
                    
        #########----------------------------------
        self.update()
        
        
        
    def Max_Vertex_Cover(self):
            
        listt=[]
        for i in range(len(self.vertex)):
            listt.append((self.vertex[i][0], self.vertex[i][1]))
        print(listt)
        
        ### Just color changing to White of all Edges and Nodes.....
        for ii in range(len(self.vertex)):
            self.nodecolor[ii] = "#ffffff"
        for ii in range(len(self.edges)):
            self.edgecolor[ii] = "#ffffff"
        
        #print(type(self.vertex[0]))
        ### Creating a normal graph by networkx library
        G = nx.Graph()
        ### Adding the nodes in the graph in the form (x,y)
        for i in range(len(self.vertex)):
            G.add_node((self.vertex[i][0],self.vertex[i][1]))
        ### Adding edges in the graph in the form ((x1,y1),(x2,y2))
        for i in range(len(self.edges)):
            G.add_edge((self.edges[i][0][0],self.edges[i][0][1]),(self.edges[i][1][0],self.edges[i][1][1]))
            
        ### print("Max Independ", nx.maximal_independent_set(G))
        
        #print(self.max_clique(G))
        #print("Max Independent")
        II = nx.complement(G)
        ISt = self.max_clique(II)
        #print(ISt)
        
        print("ISt :- ",type(self.vertex),"  ,ISt[0]", type(self.vertex[0]))
        print("self.vertex :- ",type(self.vertex),"  ,self.vertex[0]", type(self.vertex[0]))
        print("Total Nodes ", G.number_of_nodes())
        print("Total Edges ", G.number_of_edges())
        
        print("Min vertex cover")
        VC = [x for x in listt if x not in ISt]
        print(VC)
        print(type(VC))
        
        
        for ii in range(len(self.vertex)):
            self.nodecolor[ii] = "#55aa00"
        for ii in range(len(self.vertex)):
            self.nodecolor[ii] = "#ffffff"
        for ii in range(len(self.edges)):
            self.edgecolor[ii] = "#ffffff"
        
        for ii in VC:
            for jj in range(len(self.vertex)):
                if(ii[0]==self.vertex[jj][0] and ii[1]==self.vertex[jj][1]):
                    self.nodecolor[jj] = "#ff0000"
                    
                    
        
                    
        #########----------------------------------
        self.update()
        
        
    
    
    def neighbour(self, x, y):
        for i in range(len(self.vertex)):
            if x<self.vertex[i][0]+2 and x>self.vertex[i][0]-2 and y<self.vertex[i][1]+2 and y>self.vertex[i][1]-2:
                return 1
        return 0
    
    
    def blankscreen(self):
        self.x = 0
        self.y = 0
        self.del1=0
        self.mov=0
        self.nod=0
        self.edge=0
        self.del2=0
        self.color=0
        self.changenodec=0
        self.changeedgec=0
        self.vertex=[]
        self.edges=[]
        self.edges1=[]
        self.edgecolor=[]
        self.nodecolor=[]
        self.pencolor="#ffffff"
        self.pencolorchange="#ffffff"
        self.match=0
        canvas = QtGui.QPixmap(2000,2000)
        self.label.setPixmap(canvas)
        self.update()
    
    
    def savegraph(self):
        if self.save==0:
            self.folder=os.getcwd()
            self.del1=0
            self.mov=0
            self.nod=0
            self.edge=0
            self.del2=0
            self.color=0
            self.changenodec=0
            self.changeedgec=0
            fileName, _ = QFileDialog.getSaveFileName(self,
                                                      "Save Design", os.path.join(str(self.folder), "untitled.txt"),
                                                      "Input Files(*.txt)")

            if not fileName:
                return

            try:
                out_file = open(str(fileName), 'w')

            except IOError:
                QMessageBox.information(self, "Unable to open file",
                                        "There was an error opening \"%s\"" % fileName)
                return
            
            for i in range(len(self.vertex)):
                out_file.write(str(self.vertex[i][0])+','+str(self.vertex[i][1])+','+str(self.nodecolor[i])+'\n')
            out_file.write('***********************\n')
            for i in range(len(self.edges)):
                out_file.write(str(self.edges[i][0][0])+','+str(self.edges[i][0][1])+','+str(self.edges[i][1][0])+','+
                               str(self.edges[i][1][1])+','+str(self.edgecolor[i])+'\n')
            out_file.close()
            pass
        
    
    #This function is for opening the pre loaded file for prdefined graph for
    #File which has First total vertex and then ***....** and then Edges....
    def opengraph(self):
        if self.open==0:
            
            self.folder=os.getcwd()
            self.x = 0
            self.y = 0
            self.del1=0
            self.mov=0
            self.nod=0
            self.edge=0
            self.del2=0
            self.color=0
            self.changenodec=0
            self.changeedgec=0
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            filename,_= QFileDialog.getOpenFileName(self, 'Open File', os.path.join(str(self.folder), "*.txt"))
            
            if filename!="":
                self.vertex=[]
                self.edges=[]
                self.edges1=[]
                self.edgecolor=[]
                self.nodecolor=[]
                f=open(filename, "r")
                print("Here in open")
                if f.mode == 'r':
                    contents =f.read()
                lines = contents.split('\n')
                flag=1
                ### Since the file is storing all the data like
                '''
                819 , 816
                493 , 809
                686 , 486
                427 , 127
                1108 , 121
                721 , 161
                1336 , 462
                *************************************
                1336 , 462 , 1073  , 320
                1073 , 320 , 1106  , 535
                1106 , 535 , 1288  , 712
                1288 , 712 , 1336  , 462
                1336 , 462 , 1546  , 598
                '''
                ### All lines above 'star' line is for vertex, cordinates of all nodes
                ### All lines below 'star' line is for Edges 1st two No.s for coordinate of starting point
                ### Remaining two No.s are for coordinates of ending node of the edge.....
                for line in lines:
                    if line:
                        if(line[0]=='*'):
                            flag=0
                            continue
                        if(flag):
                            self.vertex.append([int(line.split(',')[0]), int(line.split(',')[1])])
                            self.nodecolor.append((line.split(',')[2]))
                        else:
                            self.edges.append([[int(line.split(',')[0]), int(line.split(',')[1])], [int(line.split(',')[2]), int(line.split(',')[3])]])
                            self.edgecolor.append((line.split(',')[4]))
                canvas = QtGui.QPixmap(2000,2000)
                self.label.setPixmap(canvas)
                self.update()
            
    def window2(self):                                             
        self.w = Window2()
        self.w.show()
        
        
        
        
    def showColorMenu(self):
        if self.color==0:
            self.color=1
            '''self.mov=0
            self.del1=0
            self.nod=0
            self.edge=0
            self.del2=0
            self.changenodec=0
            self.changeedgec=0'''
            col = QColorDialog.getColor()
            
            if col.isValid():
                #self.frm.setStyleSheet("QWidget { background-color: %s }"% col.name())
                self.pencolor=col.name()
                self.color=0
    
    
    def changeNodeColor(self):
        if self.changenodec==0:
            self.changenodec=1
        self.color=0
        self.mov=0
        self.del1=0
        self.nod=0
        self.edge=0
        self.del2=0
        self.changeedgec=0
        col = QColorDialog.getColor()
        
        if col.isValid():
            #self.frm.setStyleSheet("QWidget { background-color: %s }"% col.name())
            self.pencolorchange=col.name()
            self.update()
        
        
        
    def changeEdgeColor(self):
        if self.changeedgec==0:
            self.changeedgec=1
        self.color=0
        self.mov=0
        self.del1=0
        self.nod=0
        self.edge=0
        self.del2=0
        self.changenodec=0
        col = QColorDialog.getColor()
        
        if col.isValid():
            #self.frm.setStyleSheet("QWidget { background-color: %s }"% col.name())
            self.pencolorchange=col.name()
            self.update()
    
    
    def initUI(self):      
        
        self.x = 0
        self.y = 0
        
        
        self.vertex=[]
        self.edges=[]
        self.nodecolor=[]
        self.edgecolor=[]
        self.setMouseTracking(True)
       
        self.show()
        
    
    
    def mousePressEvent(self, ev):
        self.x = ev.x()
        self.y = ev.y()
                    
                    
                    
    
    
    def mouseReleaseEvent(self, ev):
        ### self.vertex contains all vertex in the [x-coordinate, y-coordinate] format
        ### Like each element of self.vertex is the 2-elemented list of x-coordinate, y-coordinate of vertex
        ### And self.vertex is itself a list of all points
        if self.nod==1:
            if self.x==ev.x() and self.y==ev.y():
                self.vertex.append([self.x,self.y])
                self.nodecolor.append(self.pencolor)
                self.update()
        
        ### self.vertex contains all edges in the format [ [x1,y1] , [x2,y2] ]
        ### (x1,y1) and (x2,y2) are coordinates of starting and ending point of the edge
        elif self.edge==1:
            if self.x!=ev.x() and self.y!=ev.y():
                
                ### index1 is used here for storing the index of such vertex in the list of vertices self.vertex
                ### on adding edge if the point of clicked point is in range of circle of radius of 10 unit
                ### then change the value of index from -1--> to the index of such vertex in self.vertex
                ### index1 is used for starting of the edge and
                ### index2 is used for ending of edge means mouse_release_event
                index1=-1
                index2=-1
                for i in range(len(self.vertex)):
                    if self.x<self.vertex[i][0]+10 and self.x>self.vertex[i][0]-10 and self.y<self.vertex[i][1]+10 and self.y>self.vertex[i][1]-10:
                        index1=i
                        
                    if ev.x()<self.vertex[i][0]+10 and ev.x()>self.vertex[i][0]-10 and ev.y()<self.vertex[i][1]+10 and ev.y()>self.vertex[i][1]-10:
                        index2=i
                ### If there exist starting and ending vertex of edge in the list self.vertex
                if index1!=-1 and index2!=-1:       
                    self.edges.append([self.vertex[index1],self.vertex[index2]])
                    self.edgecolor.append(self.pencolor)
                ### Basically self.update is used for calling whole programme again to paint or adding node
                ### edge or deleting the node Painting the node or edge
                self.update()
                
                
                
        ### If the clicked point is in the range of any vertex in the self.vertex
        ### Then all edges which are not containing this vertex is stored in lst list
        ### and then it is being is copied into self.edges back to back
        ### same is being is done for vertex
        elif self.del1==1:
            if self.x==ev.x() and self.y==ev.y():
                index=-1
                for i in range(len(self.vertex)):
                    if self.x<self.vertex[i][0]+10 and self.x>self.vertex[i][0]-10 and self.y<self.vertex[i][1]+10 and self.y>self.vertex[i][1]-10:
                        index=i
                        break
                lst=[]
                lst1=[]
                if index!=-1:
                    for i in range(len(self.edges)):
                        if self.vertex[index] not in self.edges[i]:
                            lst.append(self.edges[i])
                            lst1.append(self.edgecolor[i])
                    self.edges=lst
                    self.edgecolor=lst1
                    lst=[]
                    lst1=[]
                    for i in range(len(self.vertex)):
                        if i!=index:
                            lst.append(self.vertex[i])
                            lst1.append(self.nodecolor[i])
                    self.vertex=lst
                    self.nodecolor=lst1
                ### Now again defining the canvas and painting each node and edges
                canvas = QtGui.QPixmap(2000,2000)
                self.label.setPixmap(canvas)
                self.update()
                
        elif self.del2==1:
            if self.x==ev.x() and self.y==ev.y():
                index=-1
                for i in range(len(self.edges)):
                    var1=(self.y-self.edges[i][0][1])*(self.edges[i][1][0]-self.edges[i][0][0])
                    var2=(self.edges[i][1][1]-self.edges[i][0][1])*(self.x-self.edges[i][0][0])
                    var3=(self.x-self.edges[i][0][0])*(self.x-self.edges[i][1][0])
                    
                    if var1-var2>-1000 and var1-var2<1000 and var3<0:
                        index=i
                        break
                        
    
                
                if index!=-1:
                    del self.edges[index]
                    del self.edgecolor[index]
                ### Now again defining the canvas and painting each node and edges
                canvas = QtGui.QPixmap(2000,2000)
                self.label.setPixmap(canvas)
                self.update()
            
        elif self.mov==1:
            if self.x!=ev.x() or self.y!=ev.y():
                index=-1
                for i in range(len(self.vertex)):
                    if self.x<self.vertex[i][0]+10 and self.x>self.vertex[i][0]-10 and self.y<self.vertex[i][1]+10 and self.y>self.vertex[i][1]-10:
                        index=i
                        break
                lst=[]
                if index!=-1:
                    for i in range(len(self.edges)):
                        if self.vertex[index] in self.edges[i]:
                            self.edges[i].remove(self.vertex[index])
                            self.edges[i].append([ev.x(),ev.y()])
                        
                    del self.vertex[index]
                    color=self.nodecolor[index]
                    del self.nodecolor[index]
                    self.vertex.append([ev.x(),ev.y()])
                    self.nodecolor.append(color)
                    
                canvas = QtGui.QPixmap(2000,2000)
                self.label.setPixmap(canvas)
                self.update()
                
        elif self.changenodec==1:
            if self.x==ev.x() and self.y==ev.y():
                index=-1
                for i in range(len(self.vertex)):
                    if self.x<self.vertex[i][0]+10 and self.x>self.vertex[i][0]-10 and self.y<self.vertex[i][1]+10 and self.y>self.vertex[i][1]-10:
                        index=i
                        break
                if index!=-1:     
                    self.nodecolor[index]=self.pencolorchange
                
                canvas = QtGui.QPixmap(2000,2000)
                self.label.setPixmap(canvas)
                self.update()
                
        
        elif self.changeedgec==1:
            if self.x==ev.x() and self.y==ev.y():
                index=-1
                for i in range(len(self.edges)):
                    var1=(self.y-self.edges[i][0][1])*(self.edges[i][1][0]-self.edges[i][0][0])
                    var2=(self.edges[i][1][1]-self.edges[i][0][1])*(self.x-self.edges[i][0][0])
                    var3=(self.x-self.edges[i][0][0])*(self.x-self.edges[i][1][0])
                    
                    if var1-var2>-1000 and var1-var2<1000 and var3<0:
                        index=i
                        break
                        
                if index!=-1:
                    self.edgecolor[index]=self.pencolorchange
                    
                canvas = QtGui.QPixmap(2000,2000)
                self.label.setPixmap(canvas)
                self.update()
                    
    
                    
        
    ### This is paint event 
    ### Painting Each node and edges between nodes....
    def paintEvent(self, event):
        q = QPainter(self.label.pixmap())
        #q.setPen(QPen(QtGui.QColor(self.pencolor),  5, Qt.SolidLine))
        #q.setBrush(QBrush(QtGui.QColor(self.pencolor), Qt.SolidPattern))
        
        for i in range(len(self.vertex)):
            q.setPen(QPen(QtGui.QColor(self.nodecolor[i]),  5, Qt.SolidLine))
            q.setBrush(QBrush(QtGui.QColor(self.nodecolor[i]), Qt.SolidPattern))
            q.drawEllipse(QtCore.QPoint(self.vertex[i][0]-34, self.vertex[i][1]+495), 5, 5)

        #q.setPen(QPen(Qt.red,  5, Qt.SolidLine))
        #q.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        
        for i in range(len(self.edges)):
            q.setPen(QPen(QtGui.QColor(self.edgecolor[i]),  5, Qt.SolidLine))
            q.drawLine(self.edges[i][0][0]-34,self.edges[i][0][1]+495,self.edges[i][1][0]-34,self.edges[i][1][1]+495)
            
    
    
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())


# In[ ]:




