import nash
import numpy as np

def payoffw(A):
    '''
    this funtion in order to calculata playerA's equilibium payoff

    A refer to player_A's  strategic
    tupleA,tupleB refer to probability of palyerA,B 's equilibium strategic
    -----
    Return playA's equilibium payoff
    '''
    rps = nash.Game(A)
    eps = rps.support_enumeration()
    for ep in eps:
        tu = ep

    shape = A.shape
    payoff_all = 0

    for x in range(0, shape[0]):
        payoff_colum = 0
        for y in range(0, shape[1]):
            payoff_colum = payoff_colum + A[x][y] * tu[1][y]

        payoff_all = payoff_all + payoff_colum * tu[0][x]
    return payoff_all

def conquest_payoff(game):
    '''
    game is a nashgame
    Return conquest model payoff
    '''

    shape=game.shape
    pre_payoff=np.zeros((shape[0],shape[1]))

    if shape[0]==1:
        loss_pb=1
        for j in range(0,shape[1]):
            loss_pb=loss_pb*game[0][j]
        payoff_pb=1-loss_pb
        return payoff_pb

    if shape[1] == 1:
        payoff_pb = 1
        for i in range(0, shape[0]):
            payoff_pb = payoff_pb * game[i][0]
        return payoff_pb

    if shape[0]>1 and shape[1]>1:
        pre_payoff = np.zeros((shape[0], shape[1]))

        for i in range(0,shape[0]):
            for j in range(0,shape[1]):
                pre_payoff_win=np.delete(game,i,0)
                pre_payoff_loss=np.delete(game,j,1)
                pre_payoff[i][j]=game[i][j]*conquest_payoff(pre_payoff_win)+(1-game[i][j])*conquest_payoff(pre_payoff_loss)


        return payoffw(pre_payoff)



def conquest_strategic(game):

    shape=game.shape
    pre_payoff=np.zeros((shape[0],shape[1]))

    if shape[0]==1:
        loss_pb=1
        for j in range(0,shape[1]):
            loss_pb=loss_pb*game[0][j]
        payoff_pb=1-loss_pb
        return payoff_pb

    if shape[1] == 1:
        payoff_pb = 1
        for i in range(0, shape[0]):
            payoff_pb = payoff_pb * game[i][0]
        return payoff_pb

    if shape[0]>1 and shape[1]>1:
        pre_payoff = np.zeros((shape[0], shape[1]))

        for i in range(0,shape[0]):
            for j in range(0,shape[1]):
                pre_payoff_win=np.delete(game,i,0)
                pre_payoff_loss=np.delete(game,j,1)
                pre_payoff[i][j]=game[i][j]*conquest_payoff(pre_payoff_win)+(1-game[i][j])*conquest_payoff(pre_payoff_loss)

    rps = nash.Game(pre_payoff)

    return rps.support_enumeration()

'''Input:
game= np.array([[0.44,0.13],[ 0.10,0.40]])

print(payoffw(game))
print(conquest_payoff(game))
print(list(conquest_strategic(game)))


Output:
0.267213114754
0.288974048795
[(array([ 0.47640139,  0.52359861]), array([ 0.43646529,  0.56353471]))]

'''
