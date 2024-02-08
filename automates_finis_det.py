#====================================#
# UE Calculabilite L3 / M1 SFTR      #
# TME Automates finis deterministes  #
# Mathieu.Jaume@lip6.fr              #
#====================================#

from automates_finis import *

# Liste des transitions de T dont l'origine est l'etat s
# ------------------------------------------------------

def lt_from_s(eqS,s,T):
    # eqS : fonction d'egalite sur les etats
    # s : etat
    # T : liste de transitions
    return [(s1,l,s2) for (s1,l,s2) in T if eqS(s1,s)]

# Liste des labels presents sur les transitions issues d'un etat s
# ----------------------------------------------------------------

def label_from(eqS,s,T):
    # eqS : fonction d'egalite sur les etats
    # s : etat
    # T : liste de transitions
    R = []
    for (si,l,sf) in T:
        if eqS(si,s) and l != None:
            R = ajout(eq_atom,l,R)
    return R

# Liste des labels presents sur les transitions issues d'un ensemble d'etats
# --------------------------------------------------------------------------

def label_from_set(eqS,S,T):
    # eqS : fonction d'egalite sur les etats
    # S : liste d'etats
    # T : liste de transitions
    R = []
    for s in S:
        R = union(eq_atom,label_from(eqS,s,T),R)
    return R

# Automates finis deterministes
#------------------------------

# determine si la relation de transition a partir d'un etat s est
# fonctionnelle et ne contient aucune epsilon-transition
# ---------------------------------------------------------------

def lt_from_s_deterministic(T):
    # T : liste de transitions
    def _aux(L):
        if len(L)==0:
            return True
        else:
            if L[0] == None or L[0] in L[1:]:
                return False
            else:
                return _aux(L[1:])
    return _aux([l for (_,l,_) in T])


# determine si un automate est deterministe
# -----------------------------------------

def is_deterministic(A):
    # A : automate fini
    (S,T,I,F,eqS) = A
    if len(I)!= 1 :
        return False
    for s in S:
        Ts = lt_from_s(eqS, s, T)
        if not lt_from_s_deterministic(Ts) :
            return False
    return True

# Determinisation
#----------------

# Egalite entre transitions d'un automate
# ---------------------------------------

def eq_trans(eqS,t1,t2):
    (si1,l1,sf1) = t1
    (si2,l2,sf2) = t2
    return l1==l2 and eqS(si1,si2) and eqS(sf1,sf2)

def make_eq_trans(eqS):
    def _eq_trans(t1,t2):
        return eq_trans(eqS,t1,t2)
    return _eq_trans

# Determinisation d'un automate fini avec epsilon-transitions
# -----------------------------------------------------------

def make_det(A):
    # A : automate fini
    (S, T, I, F, eqS) = A
    done=[]
    to_do = [eps_cl_set(eqS, I, T)]
    Tdet=[]
    eqSet = make_eq_set(eqS)
    eqT = make_eq_trans(eqS)
    while to_do != []:
        temp=to_do[0]
        done = ajout(eqSet, to_do[0], done)
        to_do = diff_set(eqSet, [to_do[0]], to_do)

        for l in label_from_set(eqS, to_do, T):
            etat=[]
            for s in temp:
                etat=union(eqS, reach_from(eqS, s, l, T), etat)
            if not is_in(eqS, etat, done) and etat != []:
                done =ajout(eqSet, etat, done)
                Tdet=ajout(eqT, (temp, l, etat), T)
    
    Fdet=[]
    for i in done:
        for j in i:
            if is_in(eqS, j, F):
                Fdet=ajout(eqS, i, Fdet)
                
    return (done, Tdet, eps_cl_set(eqS, I, T), Fdet, eqS)

