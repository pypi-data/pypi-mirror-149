import math
import numpy


def _muller_brown(xi):
    """
    The Muller-Brown surface
    """
    A = (-200.0, -100.0, -170.0, 15.0)
    a = (-1.0, -1.0, -6.5, 0.7)
    b = (0.0, 0.0, 11.0, 0.6)
    c = (-10.0, -10.0, -6.5, 0.7)
    xb = (1.0, 0.0, -0.5, -1.0)
    yb = (0.0, 0.5, 1.5, 1.0)
    x, y = xi[0], xi[1]

    val = 0.0
    der = numpy.array([0.0, 0.0])
    dder = numpy.array([[0.0, 0.0], [0.0, 0.0]])
    for i in range(4):
        expo = math.exp(a[i] * (x - xb[i])**2 + b[i] * (x - xb[i]) * (y - yb[i]) + c[i] * (y - yb[i])**2)
        val += A[i] * expo
        der[0] += A[i] * (2 * a[i] * (x - xb[i]) + b[i] * (y - yb[i])) * expo
        der[1] += A[i] * (2 * c[i] * (y - yb[i]) + b[i] * (x - xb[i])) * expo
        dder[0, 0] += A[i] * (2 * a[i] + (2 * a[i] * (x - xb[i]) + b[i] * (y - yb[i]))**2) * expo
        dder[1, 1] += A[i] * (2 * c[i] + (2 * c[i] * (y - yb[i]) + b[i] * (x - xb[i]))**2) * expo
        cross = A[i] * (b[i] + (2 * a[i] * (x - xb[i]) + b[i] * (y - yb[i])) * (2 * c[i] * (y - yb[i]) + b[i] * (x - xb[i]))) * expo
        dder[0, 1] += cross
        dder[1, 0] += cross

    return val, der, dder


def value(x):
    res, _, _ = _muller_brown(x)
    return res


def gradient(x):
    _, res, _ = _muller_brown(x)
    return res


def hessian(x):
    _, _, res = _muller_brown(x)
    return res


def normal_modes(x):
    from scipy.linalg import eigh as eig

    H = hessian(x)
    eigvalues, eigvectors = eig(H)
    # Sanitize eigenvectors and make it a list of vectors
    eigvectors = [eigvectors[:, i] for i in range(eigvectors.shape[1])]
    eigvalues = numpy.array([float(_) for _ in eigvalues])
    return eigvalues, eigvectors


# def _debug_mb():
#     delta = 1e-6
#     for x in linear_grid(-1.5, 0.9, 10):
#         for y in linear_grid(-0.2, 1.8, 10):
#             dxx = (d_muller_brown([x+delta, y])[0]-d_muller_brown([x-delta, y])[0])/(2*delta) - dd_muller_brown([x, y])[0, 0]
#             dxy = (d_muller_brown([x+delta, y])[1]-d_muller_brown([x-delta, y])[1])/(2*delta) - dd_muller_brown([x, y])[0, 1]
#             dyx = (d_muller_brown([x, y+delta])[0]-d_muller_brown([x, y-delta])[0])/(2*delta) - dd_muller_brown([x, y])[1, 0]
#             dyy = (d_muller_brown([x, y+delta])[1]-d_muller_brown([x, y-delta])[1])/(2*delta) - dd_muller_brown([x, y])[1, 1]

#             dx = (muller_brown([x+delta, y])-muller_brown([x-delta, y]))/(2*delta) - d_muller_brown([x, y])[0]
#             dy = (muller_brown([x, y+delta])-muller_brown([x, y-delta]))/(2*delta) - d_muller_brown([x, y])[1]

#             for _ in [dx, dy, dxx, dxy, dyx, dyy]:
#                 if abs(_) > 1e-5:
#                     raise ValueError('error too large', _)
