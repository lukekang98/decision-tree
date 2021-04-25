#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 13:50:42 2021

@author: kangyifu
"""

class Tree:
    class Position:
        def element(self):
            raise NotImplementedError('must be implemented by subclasses!')
            
        def __eq__(self, other):
            raise NotImplementedError('must be implemented by subclasses!')
        
        def __ne__(self, other):
            raise NotImplementedError('must be implemented by subclasses!')
            
    def root(self):
        raise NotImplementedError('must be implemented by subclasses!')
        
    def parent(self, p):
        raise NotImplementedError('must be implemented by subclasses!')
        
    def num_children(self, p):
        raise NotImplementedError('must be implemented by subclasses!')
        
    def children(self, p):
        raise NotImplementedError('must be implemented by subclasses!')
        
    def __len__(self):
        raise NotImplementedError('must be implemented by subclasses!')
        
    def is_root(self, p):
        return self.root()==p
    
    def is_leaf(self, p):
        return self.num_children(p)==0
    
    def is_empty(self):
        return len(self)==0
    
    def depth(self, p):
        if self.is_root(p):
            return 0
        else:
            return 1+self.depth(self.parent(p))
        
    def height(self, p):
        if self.is_leaf(p):
            return 0
        else:
            return 1+max(self.height(c) for c in self.children(p))
    
    def total_height(self, p=None):
        if p is None:
            p = self.root()
        return self.height(p)
    
    def __iter__(self):
        for p in self.positions():
            yield p.element()
        
    
    def preorder(self):
        if not self.is_empty():
            for p in self._subtree_preorder(self.root()):
                yield p
                
    def _subtree_preorder(self, p):
        yield p
        for c in self.children(p):
            for other in self._subtree_preorder(c):
                yield other
        
    
    
    def preorder_indent(self, p, d):
        print(2*d*' ', str(p.element()))
        for c in self.children(p):
            self.preorder_indent(c, d+1)
            
    def preorder_label(self, p, d, path):
        label='.'.join(str(j+1) for j in path)
        print(2*d*' '+label, str(p.element()))
        path.append(0)
        for c in self.children(p):
            self.preorder_label(c, d+1, path)
            path[-1] += 1
        path.pop()
            
    
    
    def postorder(self):
        if not self.is_empty():
            for p in self._subtree_postorder(self.root()):
                yield p
       
    def _subtree_postorder(self, p):
        for c in self.children(p):
            for other in self._subtree_postorder(c):
                yield other
        yield p


    

class BinaryTree(Tree):
    
    def left(self, p):
        raise NotImplementedError('must be implemented by subclasses!')
        
    def right(self, p):
        raise NotImplementedError('must be implemented by subclasses!')
        
    def sibling(self, p):
        parent=self.parent(p)
        if parent == None:
            return None
        else:
            if p == self.right(parent):
                return self.left(parent)
            else:
                return self.right(parent)
            
    def children(self, p): #iteration
        if self.right(p) is not None:
            yield self.right(p)
        if self.left(p) is not None:
            yield self.left(p)
            
    def inorder(self):
        if not self.is_empty():
            for p in self._subtree_inorder(self.root()):
                yield p
                
    def _subtree_inorder(self, p):
        if self.left(p) is not None:
            for other in self._subtree_inorder(self.left(p)):
                yield other
        yield p
        if self.right(p) is not None:
            for other in self._subtree_inorder(self.right(p)):
                yield other
                
    

class LinkedBinaryTree(BinaryTree):
    
    class _Node:
        __slots__ = '_element', '_parent', '_left', '_right'
        def __init__(self, element, left = None, right = None, parent = None):
            self._element = element
            self._left = left
            self._right = right
            self._parent = parent
            
    class Position(BinaryTree.Position):
        
        def __init__(self,container,node):
            self._container=container
            self._node=node
            
        def element(self):
            return self._node._element
        
        def __eq__(self, other):
            return type(other) is type(self) and other._node is self._node
        
    def _validate(self, p):
        if not isinstance(p, self.Position):
            raise TypeError("P must be a Postion Type")
        if p._container is not self:
            raise ValueError("P does not belong to this container")
            
        if p._node._parent == p._node:
            return ValueError('P is no longer valid ')
            
        return p._node
        
    def _make_position(self,node):
        return self.Position(self, node) if node is not None else None
        
        
    def __init__(self):
        self._root = None
        self._size = 0
    
    def __len__(self):
        return self._size
    
    def root(self):
        return self._make_position(self._root)
    
    def parent(self, p):
        node = self._validate(p)
        return self._make_position(node._parent)
    
    def left(self, p):
        node = self._validate(p)
        return self._make_position(node._left)
    
    def right(self,p):
        node = self._validate(p)
        return self._make_position(node._right)
    
    def num_children(self, p):
        node = self._validate(p)
        num=0
        if node._left is not None:
            num += 1
        if node._right is not None:
            num += 1
            
        return num
    
    def _all_left(self, p):
        if self.is_leaf(p):
            return 0
        else:
            if self.left(p) is None:
                return self._all_left(self.right(p))
            elif self.right(p) is None:
                return 1 + self._all_left(self.left(p)) 
            else:
                return 1 + self._all_left(self.left(p)) + self._all_left(self.right(p))

    def cpt_left(self):
        return self._all_left(self.root())
            
        
    
    def _add_root(self, e):
        if self._root is not None:
            raise ValueError('root exists')
        else:
            self._size += 1
            self._root = self._Node(e)
            return self._make_position(self._root)
        
    def _add_left(self, p, e):
        node = self._validate(p)
        if node._left is not None:
            raise ValueError('Left child already exists')
        else:
            self._size += 1
            node._left = self._Node(e, parent = node)
            return self._make_position(node._left)
        
    
        
            
    def _add_right(self, p, e):
        node = self._validate(p)
        if node._right is not None:
            raise ValueError('Right child already exists')
        else:
            self._size += 1
            node._right = self._Node(e, parent = node)
            return self._make_position(node._right)
        
    def _replace(self,p ,e):
        node = self._validate(p)
        old = node._element
        node._element=e
        return old
    
    def _delete(self, p):
        node = self._validate(p)
        if self.num_children(node)==2:
            raise ValueError('p has 2 children')
        child = node._left if node._left else node._right
        if child is not None:
            parent = node._parent
            child._parent = parent
        if node is self.root:
            self._root=child 
        else:
            parent = node._parent
            if node is parent._left:
                parent._left = child
            else:
                parent._right = child
        self._size -= 1
        node = node.parent
        return node.element
    
    def _attach(self,p,t1,t2):
        node = self._validate(p)
        if not self._is_leaf(p):
            raise ValueError('No more postion for trees')
        if not type(self) is type(t1) is type(t2):
            raise TypeError('Tree types must be the same')
        self._size += len(t1)+len(t2)
        if not t1.is_empty():
            t1._root._parent = node
            node._left = t1._root
            t1._size = 0
            t1._root = None
        if not t2.is_empty():
            t2._root._parent = node
            node._right = t2._root
            t2._size = 0
            t2._root = None
            
            
class EulerTour:
    
    def __init__(self, tree):
        self._tree = tree
        
    def tree(self):
        return self._tree
    
    def execute(self):
        if len(self._tree) > 0:
            return self._tour(self._tree.root(), 0, [], 0)
        
    def _tour(self, p, d, path, fp):
        self._hook_previsit( p, d, path, fp)
        fp = 2 * fp + 1
        path.append(0)
        results=[]
        for c in self._tree.children(p):
            results.append(self._tour(c, d+1, path, fp))
            fp += 1
            path[-1] += 1
        fp = (fp - 2) / 2
        path.pop()
        answer = self._hook_postvisit(p, d+1, path, results)
        return answer
    
    def _hook_previsit(self, p, d, path, fp):
        pass
    
    def _hook_postvisit(self, p, d, path, results):
        pass
                    
class fp(EulerTour):
    def _hook_previsit(self, p, d, path,fp):
        print(2*d*' ' + str(fp), str(p.element()))


class ExpressionTree(LinkedBinaryTree):
    
    def __init__(self, token, left = None, right = None):
        super().__init__()
        if not isinstance(token, str):
            raise TypeError('Token must be str type')
        self._add_root(token)
        if left is not None:
            if token not in '+-*x/':
                raise ValueError('token must be valid operator')
            self._attach(self._root(), left, right)
            
    def __str__(self):
        pieces = []
        self._parenthesize_recur(self.root(), pieces)
        return ''.join(pieces)
    
    def _parenthesize_recur(self, p, result):
        if self.is_leaf(p):
            result.append(str(p.element()))
        else:
            result.append('(')
            self._parenthesize_recur(self.left(p), result)
            result.append(p.element())
            self._parenthesize_recur(self.right(p), result)
            result.append(')')
            
    def evaluate(self):
        return self._evaluate_recur(self.root())
    
    def _evaluate_recur(self, p):
        if self.is_leaf(p):
            return float(p.element())
        else:
            op = p.element()
            left_val = self._evaluate_recur(self.left(p))
            right_val = self._evalaute_recur(self.rigth(p))
            if op == '+': 
                return left_val + right_val
            elif op == '-':
                return left_val - right_val
            elif op == '*':
                return left_val * right_val
            else:
                return left_val / right_val
            
            
    
        

tree=LinkedBinaryTree()
p1=tree._add_root('Sustech')
p2=tree._add_right(p1,'Math')
p3=tree._add_left(p1,'Physics')
p4=tree._add_left(p2,'finmath')
p5=tree._add_right(p2,'Applied math')
p6=tree._add_left(p3,'Applied Physics')


f=fp(tree)
f.execute()




            
    
















