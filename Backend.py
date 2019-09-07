#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QLabel
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


qtcreator_file  = "GraphGUI.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)


class Window2(QMainWindow):
    def __init__(self):
        super().__init__()
        self.left = 10
        self.top = 10
        self.width = 2000
        self.height = 2000
        self.setWindowTitle("About")
        label = QLabel(self)
        label.setGeometry(QtCore.QRect(0, -200, 1000,500))
        
        text="https://github.com/CircleJerkHug/GraphProj1"
        label.setText(text)
        file.close()
        

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
        ### connecting the function to the GUI which is being clicked
        self.Add_Vertex.clicked.connect(self.addnode)
        self.AddEdge.clicked.connect(self.addedge)
        self.DelNode.clicked.connect(self.deletenode)
        self.savefile.clicked.connect(self.save_design_inputs)
        self.openfile.clicked.connect(self.opengraph)
        self.move.clicked.connect(self.movenode)
        self.about.clicked.connect(self.window2)
        self.initUI()
     
    
    ### Defining self.nod =0 means if self.nod is 1 then in the mouse release event method
    ### A nod will be added in the variable self.vertex.........
    def addnode(self):
        if self.nod==0:
            self.nod=1
            self.edge=0
            self.del1=0
            self.mov=0
            self.update()
            
    ### Defining self.edge =0 means if self.edge is 1 then in the mouse release event method
    ### A edge will be added in the variable self.edge.........
    def addedge(self):
        if self.edge==0:
            self.edge=1
            self.nod=0
            self.del1=0
            self.mov=0
            self.update()
            
    def deletenode(self):
        if self.del1==0:
            self.del1=1
            self.nod=0
            self.edge=0
            self.mov=0
            self.update()
            
    def movenode(self):
        if self.mov==0:
            self.mov=1
            self.del1=0
            self.nod=0
            self.edge=0
            self.update()
            
    def neighbour(self, x, y):
        for i in range(len(self.vertex)):
            if x<self.vertex[i][0]+2 and x>self.vertex[i][0]-2 and y<self.vertex[i][1]+2 and y>self.vertex[i][1]-2:
                return 1
        return 0
    
    def save_design_inputs(self):
        if self.save==0:
            self.folder=os.getcwd()
            self.del1=0
            self.nod=0
            self.edge=0
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
                out_file.write(str(self.vertex[i][0])+','+str(self.vertex[i][1])+'\n')
            out_file.write('***********************')
            for i in range(len(self.edges)):
                out_file.write(str(self.edges[i][0][0])+','+str(self.edges[i][0][1])+','+str(self.edges[i][1][0])+','+str(self.edges[i][1][1])+'\n')
            out_file.close()
            pass
        
    
    #This function is for opening the pre loaded file for prdefined graph for
    #File which has First total vertex and then ***....** and then Edges....
    def opengraph(self):
        if self.open==0:
            
            self.folder=os.getcwd()
            self.x = 0
            self.y = 0
            self.vertex=[]
            self.edges=[]
            self.edges1=[]
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            filename,_= QFileDialog.getOpenFileName(self, 'Open File', os.path.join(str(self.folder), "*.txt"))
            
           
            f=open(filename, "r")
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
                    else:
                        self.edges.append([[int(line.split(',')[0]), int(line.split(',')[1])], [int(line.split(',')[2]), int(line.split(',')[3])]])
            canvas = QtGui.QPixmap(2000,2000)
            self.label.setPixmap(canvas)
            self.update()
            
    def window2(self):                                             
        self.w = Window2()
        self.w.show()
    
    def initUI(self):      
        
        self.x = 0
        self.y = 0
        
        
        self.vertex=[]
        self.edges=[]
        
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
                if index!=-1:
                    for i in range(len(self.edges)):
                        if self.vertex[index] not in self.edges[i]:
                            lst.append(self.edges[i])

                    self.edges=lst

                    lst=[]
                    for i in range(len(self.vertex)):
                        if i!=index:
                            lst.append(self.vertex[i])
                    self.vertex=lst
                ### Now again defining the canvas and painting each node and edges
                canvas = QtGui.QPixmap(2000,2000)
                self.label.setPixmap(canvas)
                self.update()
            
        elif self.mov==1:
            if self.x!=ev.x() and self.y!=ev.y():
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
                    self.vertex.append([ev.x(),ev.y()])
                    
                canvas = QtGui.QPixmap(2000,2000)
                self.label.setPixmap(canvas)
                self.update()
                    
    
                    
        
    ### This is paint event 
    ### Painting Each node and edges between nodes....
    def paintEvent(self, event):
        q = QPainter(self.label.pixmap())
        q.setPen(QPen(Qt.green,  5, Qt.SolidLine))
        q.setBrush(QBrush(Qt.green, Qt.SolidPattern))
        
        for pt in self.vertex:
            q.drawEllipse(QtCore.QPoint(pt[0]-34, pt[1]+495), 5, 5)

        q.setPen(QPen(Qt.red,  5, Qt.SolidLine))
        q.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        for i in range(len(self.edges)):
            q.drawLine(self.edges[i][0][0]-34,self.edges[i][0][1]+495,self.edges[i][1][0]-34,self.edges[i][1][1]+495)
            
        
        
    
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())

