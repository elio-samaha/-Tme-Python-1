#============================================#
# UE Calculabilite L3 / M1 SFTR              #
# TME Automates finis : acceptation d'un mot #
# Mathieu.Jaume@lip6.fr                      #
#============================================#

from ensembles import *

# Automate represente par un tuple A = (S,T,I,F,eqS)
#---------------------------------------------------

# Exemple automate

ex_A = ([0,1,2,3,4],\
        [(0,None,2),(0,None,3),(1,"b",1),(1,"a",2),(1,"b",3), \
         (1,"b",4),(3,"a",1),(3,"b",1),(3,None,2),(4,"a",0),(4,None,0)],\
        [0],[2],eq_atom)

(ex_S,ex_T,ex_I,ex_F,ex_eqS) = ex_A

# Epsilon-fermeture d'un etat
#----------------------------

def eps_cl(eqS,s,T):
    # eqS : fonction d'egalite sur les etats
    # s : etat
    # T : liste de transitions
    done_i = []
    todo_i = [s]
    while todo_i != []:
        temp = todo_i
        for (s1 , a , s2) in T:
            if is_in(eqS , s1 , todo_i) and eqS(a , None) and not is_in(eqS , s1 , done_i):
                todo_i = ajout(eqS , s2 , todo_i)
        done_i = union(eqS , temp , done_i)
        todo_i = diff_set(eqS , todo_i , temp)
    return done_i

#Exemple test
"""
print(eps_cl(ex_eqS,0,ex_T))
print(eps_cl(ex_eqS,1,ex_T))
print(eps_cl(ex_eqS,4,ex_T))
"""

# Epsilon-fermeture d'un ensemble d'etats
#----------------------------------------

def eps_cl_set(eqS,S,T):
    # eqS : fonction d'egalite sur les etats
    # S : liste d'etats
    # T : liste de transitions
    res = []
    for s in S :
        res = union(eqS , res , eps_cl(eqS , s , T))
    return res

#Exemple test
"""
print(eps_cl_set(ex_eqS,[0,1],ex_T))
"""

# Liste des etats accessibles a partir d'un etat s et d'une lettre x
#-------------------------------------------------------------------

def reach_from(eqS,s,x,T):
    # eqS : fonction d'egalite sur les etats
    # s : etat
    # x : symbole de l'alphabet
    # T : liste de transitions
    s_sl = eps_cl(eqS,s,T)
    trans_x = []
    for (s1,l,s2) in T:
        if l==x and is_in(eqS,s1,s_sl):
            trans_x = ajout(eqS,s2,trans_x)
    return eps_cl_set(eqS,trans_x,T)


# Liste des successeurs d'un etat s
# ---------------------------------

def succ_s(eqS,s,T):
    # eqS : fonction d'egalite sur les etats
    # s : etat
    # T : liste de transitions
    r = []
    for (s1,_,s2) in T:
        if eqS(s,s1):
            r = ajout(eqS,s2,r)
    return r


# Liste des etats accessibles a partir d'un ensemble d'etats
# ----------------------------------------------------------

def reachable(eqS,Es,T):
    # eqS : fonction d'egalite sur les etats
    # Es : liste d'etats
    # T : liste de transitions
    _eqES = make_eq_set(eqS)
    def _add_reach(r):
        ar = []
        for qr in r:
            ar = union(eqS,ar,succ_s(eqS,qr,T))
        return union(eqS,r,ar)
    return fixpoint_from(_eqES,_add_reach,Es)


# Liste des etats accessibles a partir d'un etat initial
# ----------------------------------------------------------

def reach_A(A):
    # A : automate fini
    (S, T, I, F, eqS) = A
    return reachable(eqS , I , T)

# Liste des etats a partir desquels un etat acceptant est accessible
# ------------------------------------------------------------------

def co_reach_A(A):
    # A : automate fini
    (S, T, I, F, eqS) = A
    res = []
    for s in S:
        ans = reachable(eqS , [s] , T)
        if intersection(eqS , ans , F) != []:
            res = union(eqS , [s] , res)
    return res

ex_RcoR = ([0,1,2,3,4,5],[(0,"a",1), (0,"a",2), (1,"a",1), (1,"b",5), (2,None,3), (3,"a",3), (3,"b",3), (4,"b",3),(4,"a",5)],[0],[1,5],eq_atom)

#print(reach_A(ex_RcoR))
print(co_reach_A(ex_RcoR))

# Acceptation d'un mot
#---------------------

def accept_word_finite_aut(A,w):
    # A : automate fini
    # w : liste de symboles (mot)
    (S,T,I,F,eqS)=A
    def _aux(sa,wa):
        if wa==[]:
            return intersection(eqS,eps_cl(eqS,sa,T),F) !=[]
        else:
            trans = reach_from(eqS,sa,wa[0],T)
            for st in trans:
                if _aux(st,wa[1:]):
                    return True
            return False
    for si in I:
        if _aux(si,w):
            return True
    return False

