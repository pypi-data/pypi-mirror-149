import numpy as np
import math as m


def rank_cal_s(n):
    return (1-m.exp((n-1.0)*(1.0-n)/2.0))


rank_cal = np.vectorize(rank_cal_s)


def method_FRLF(clp, rank, confi):
    H = 4
    pr = 0.33
    pc = 0.05

    rs0 = 0
    rs1 = 0
    cf0 = 0
    cf1 = 0

    ls = []
    # for class 0
    # for vgg16
    if clp['vgg16'] == 0:
        rs0 += rank['vgg16'][0]
        cf0 += confi['vgg16'][0]

        rs1 += rank['vgg16'][1]
        cf1 += confi['vgg16'][1]
    else:
        rs0 += pr
        cf0 += pc

        rs1 += pr
        cf1 += pc
    # for xception
    if clp['xcep'] == 0:
        rs0 += rank['xcep'][0]
        cf0 += confi['xcep'][0]

        rs1 += rank['xcep'][1]
        cf1 += confi['xcep'][1]
    else:
        rs0 += pr
        cf0 += pc

        rs0 += pr
        cf0 += pc
    # for res50
    if clp['res50'] == 0:
        rs0 += rank['res50'][0]
        cf0 += confi['res50'][0]

        rs1 += rank['res50'][1]
        cf1 += confi['res50'][1]
    else:
        rs0 += pr
        cf0 += pc

        rs1 += pr
        cf1 += pc
    # for incv3
    if clp['incv3'] == 0:
        rs0 += rank['incv3'][0]
        cf0 += confi['incv3'][0]

        rs1 += rank['incv3'][1]
        cf1 += confi['incv3'][1]
    else:
        rs0 += pr
        cf0 += pc

        rs1 += pr
        cf1 += pc

    cf0 = 1-(cf0/H)
    cf1 = 1-(cf1/H)

    ls.append(rs0*cf0)
    ls.append(rs1*cf1)
    return np.argmin(ls)


def sum_rule(confi):
    """[summary]

    Args:
        confi (dict): Class confidence

    Returns:
        [type]: [description]
    """
    pred = None
    data = confi
    sum0 = data['vgg16'][0]+data['incv3'][0] + data['xcep'][0]+data['res50'][0]
    sum1 = data['vgg16'][1]+data['incv3'][1] + data['xcep'][1]+data['res50'][1]
    if sum0 > sum1:
        pred = 0
    else:
        pred = 1
    return pred


def product_rule(confi):
    """[summary]

    Args:
        confi (dict): Class confidence

    Returns:
        [type]: [description]
    """
    pred = None
    data = confi
    sum0 = data['vgg16'][0]*data['incv3'][0] * data['xcep'][0]*data['res50'][0]
    sum1 = data['vgg16'][1]*data['incv3'][1] * data['xcep'][1]*data['res50'][1]
    if sum0 > sum1:
        pred = 0
    else:
        pred = 1
    return pred


def majority_voting(data):
    """[summary]

    Args:
        data (dict): Class prediction

    Returns:
        [type]: [description]
    """
    sum0 = 0
    sum1 = 0

    if data['vgg16'] == 0:
        sum0 += 1
    else:
        sum1 += 1

    if data['xcep'] == 0:
        sum0 += 1
    else:
        sum1 += 1

    if data['res50'] == 0:
        sum0 += 1
    else:
        sum1 += 1

    if data['incv3'] == 0:
        sum0 += 1
    else:
        sum1 += 1

    if sum0 > sum1:
        return 0
    else:
        return 1
