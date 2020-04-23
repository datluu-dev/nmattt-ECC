from modularInverse import modularInverse as m_i
from extendedGCD import extendedGCD as gcd
import math
import random
import traceback
import csv
'''
E(a,b) = X^3 + ax +b
'''

def get_point_lists(a,b,p):
    # Q_p phần tử thặng dư bậc 2
    Q_p_dict = {}
    for i in range(1,p//2):
        Q_p_dict[i**2 % p] = i


    # List of point
    point_list = []
    for x in range(0,p):
        vtrai = (x**3 + a*x + b) % p
        # y = math.sqrt(vtrai)
        if vtrai in Q_p_dict:
            # print(x, Q_p_dict[vtrai])
            point_list.append((x, Q_p_dict[vtrai]))
            # print(x,p-vtrai)
            point_list.append((x,p-Q_p_dict[vtrai]))
        if vtrai == 0:
            # print(x, vtrai)
            point_list.append((x,vtrai))

    return point_list

def find_lambda(P,Q,a,p):
    if P==Q:
        ts = 3*(P[0]**2) + a
        ms = 2*P[1]
    else:
        ts = Q[1] - P[1]
        ms = Q[0] - P[0]

    ts_old = (ts%p) 
    ms_old = (ms%p) 

    gcd_val = gcd(ts_old, ms_old)
    ts = ts_old // gcd_val
    ms = ms_old // gcd_val

    return ((ts%p) * (m_i(ms,p)%p)) % p

def find_cyclic_point(P, Q, a, p):
    lambda_val = find_lambda(P, Q, a,p)
    # print(lambda_val)
    x3 = (lambda_val**2 - P[0] - Q[0]) % p
    y3 = (lambda_val * (P[0]-x3) - P[1]) % p
    return (x3, y3), lambda_val

def make_table(a,p,k_num,file,init_point=(3,10)):
    with open(file, mode='w') as csv_file:
        columns = ['K', 'Lambda', 'x3', 'y3', 'kP']
        writer = csv.DictWriter(csv_file, fieldnames=columns)

        list_kP = [(0, None, init_point)]
        # print(f'k={1}, lambda={None}, x3={None}, y3={None}, kP={init_point}')    
        writer.writerow({
            'K': 0,
            'Lambda': 'None',
            'x3': 'None',
            'y3': 'None',
            'kP': str(init_point)
        })
        for k in range(2,k_num+1):
            if (k==2):
                last_point = init_point
            try:
                cyclic_point, lambda_val = find_cyclic_point(init_point, last_point, a, p)
                list_kP.append((k, lambda_val, cyclic_point))
                last_point = cyclic_point
                # print(f'k={k}, lambda={lambda_val}, x3={cyclic_point[0]}, y3={cyclic_point[1]}, kP={cyclic_point}')
                writer.writerow({
                    'K': k,
                    'Lambda': lambda_val,
                    'x3': cyclic_point[0],
                    'y3': cyclic_point[1],
                    'kP': str(cyclic_point)
                })
            except Exception as e:
                writer.writerow({
                    'K': k,
                    'Lambda': 'None',
                    'x3': 'None',
                    'y3': 'None',
                    'kP': 0
                })

        return list_kP

def main(a, b, p, file):
    pl = get_point_lists(a, b, p)
    # print(f'Các điểm E({a}, {b}):')
    # for point in pl:
    #     print(point)
    # print('------------------')
    k_num = len(pl)
    random_init_point = (0,376)
    # random_init_point = pl[random.randint(0, len(pl))]
    # print('Bảng kP:')
    make_table(a, p, k_num, file,random_init_point)

if __name__ == '__main__':
    a = -1  
    b = 188
    p = 751
    file = ('out.csv')
    main(a, b, p, file)