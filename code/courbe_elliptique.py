import numpy as np
import matplotlib.pyplot as plt

# Point à l'infini (élément neutre)
POINT_INFINI = np.array([float("inf"), float("inf")])

def elliptic_curve_point(x, a, b):
    """Renvoie les deux points (x, y) et (x, -y) de la courbe y^2 = x^3 + a*x + b (si existants)."""
    res = x**3 + a*x + b
    if res >= 0:
        return [np.sqrt(res), -np.sqrt(res)]
    return None

def elliptic_curve_set(a, b, start, end, step):
    """Génère les points réels de la courbe elliptique entre start et end."""
    num_points = int((end - start) / step) + 1
    xy = []
    xy_neg = []
    for x in np.linspace(start, end, num_points):
        res = elliptic_curve_point(x, a, b)
        if res is not None:
            xy.insert(0, np.array([x, res[0]]))
            xy_neg.append(np.array([x, res[1]]))
    return np.array(xy + xy_neg)

def plot_elliptic_curve(x_start, x_end, y_start, y_end, points, *points_uniques):
    """Trace la courbe elliptique dans le plan réel."""
    plt.figure(figsize=(10, 10))
    plt.xlim(x_start, x_end)
    plt.ylim(y_start, y_end)
    plt.grid(True)
    plt.plot(points[:, 0], points[:, 1], '.')
    labels = "PQRSTUVWXYZ"
    for i in range(len(points_uniques)):
        if points_uniques[i][0] == float('inf'):
            raise ValueError("On ne peut pas plotter un point à l'infini")
        plt.plot(points_uniques[i][0], points_uniques[i][1], 'o', c='red')
        plt.annotate(labels[i], (points_uniques[i][0], points_uniques[i][1]),
                     textcoords='offset points', xytext=(10,10), ha='left',
                     color='red', fontsize=12)
    plt.show()

def elliptic_curve_sur_corps_fini(p, a, b):
    """Renvoie la liste des points (x, y) appartenant à la courbe elliptique mod p."""
    points = []
    for x in range(p):
        res = (x**3 + a*x + b) % p
        for y in range(p):
            if (y**2) % p == res:
                points.append(np.array([x, y]))
    return np.array(points)

def plot_elliptic_curve_sur_corps_fini(p, points_sur_corps_fini, *points_uniques):
    """Trace la courbe elliptique sur un corps fini F_p."""
    plt.figure(figsize=(10, 10))
    plt.xticks(range(p))
    plt.yticks(range(p))
    plt.grid(True)
    plt.plot(points_sur_corps_fini[:, 0], points_sur_corps_fini[:, 1], 'o')
    labels = "PQRSTUVWXYZ"
    for i in range(len(points_uniques)):
        if points_uniques[i][0] == float('inf'):
            raise ValueError("On ne peut pas plotter un point à l'infini")
        plt.plot(points_uniques[i][0], points_uniques[i][1], 'o', c='red')
        plt.annotate(labels[i], (points_uniques[i][0], points_uniques[i][1]),
                     textcoords='offset points', xytext=(10,10), ha='left',
                     color='red', fontsize=12)
    plt.show()

def multiplication_point_cf(k, P, a, p):
    if k % p == 0 or is_point_infini(P):
        return POINT_INFINI

    result = POINT_INFINI
    addend = P

    while k > 0:
        if k & 1:  # si bit = 1
            result = addition_deux_points_cf(result, addend, a, p)
        addend = addition_deux_points_cf(addend, addend, a, p)
        k >>= 1  # décale les bits
    return result


def addition_deux_points_cf(P, Q, a, p):
    if is_point_infini(P):
        return Q
    if is_point_infini(Q):
        return P

    xp, yp = P
    xq, yq = Q

    if xp == xq and (yp + yq) % p == 0:
        return POINT_INFINI

    if xp != xq:
        s = ((yq - yp) * inv_mod(xq - xp, p)) % p
    else:
        if yp == 0:
            return POINT_INFINI
        s = ((3 * xp**2 + a) * inv_mod(2 * yp, p)) % p

    xr = (s**2 - xp - xq) % p
    yr = (s * (xp - xr) - yp) % p
    return (xr, yr)


def trouver_ordre_point(G, a, p):
    n = 1
    P = G
    while not is_point_infini(P):
        P = addition_deux_points_cf(P, G, a, p)
        n += 1
    return n

POINT_INFINI = None


def is_point_infini(P):
    return P is None

def inv_mod(k, p):
    k = k % p
    if k == 0:
        raise ZeroDivisionError("Pas d'inverse pour 0 modulo p")
    return pow(int(k), p-2, p)