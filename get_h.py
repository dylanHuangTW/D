import math as m

if __name__ == '__main__':
    # input parameters
    Q = 15.5        # discharge in (m3/s)
    b = 5.1         # bottom channel width (m)
    m_bank = 2.5    # bank slope
    k_st = 20       # Strickler value
    n_m = 1 / k_st  # Manning's n
    S = 0.005     # channel slope

    # call the solver with user-defined channel geometry and discharge

    #h_n = interpolate_h(Q, b, n_m=n_m, m_bank=m_bank, S=S)

def calc_discharge(b, h, k_st, m_bank, S):
    A = h * (b + h*m_bank)
    P = b + 2*h*(m.sqrt((m_bank**2) + 1))
    Q = k_st * (m.sqrt(S)) * ((A/P)**(2/3)) * A
    return Q


def interpolate_h( Q, b, m_bank, S, **kwargs):
    h=5000
    eps=1
    i=0
    for k in kwargs.items():
        if "n_m" in k[0]:
            coeff = k[1]
        elif "k_st" in k[0]:
            coeff = 1 / k[1]
        else:
            print("error")
            break
        while eps > 10 ** -3:
            i = i + 1
            A = h * (b + h * m_bank)
            P = b + 2 * h * (m.sqrt((m_bank ** 2) + 1))
            Qc = (1/coeff) * (m.sqrt(S)) * ((A/P)**(2/3)) * A
            eps = abs(Q - Qc) / Q
            dA_dh = b + 2 * m_bank * h
            dP_dh = 2 * m.sqrt((m_bank ** 2) + 1)
            F = (coeff) * Q * (P ** (2 / 3)) - (A ** (5 / 3)) * m.sqrt(S)
            dF_dh = 2 / 3 * (coeff) * Q * (P ** (-1 / 3)) * dP_dh - 5 / 3 * (A ** (2 / 3)) * m.sqrt(S) * dA_dh
            h = abs(h - F / dF_dh)
            if i > 1000:
                break
        return (h,eps,Qc,i)

h_n = interpolate_h(Q, b, m_bank, S,k_st = 20)
print(h_n)

