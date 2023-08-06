import numpy

# Multi saddle


def value(x):
    return -2.0 * x[0]**2 - 2.0 * x[1]**2 + 0.1 * x[0]**4 + 0.1 * x[1]**4


def gradient(x):
    return numpy.array([-4.0 * x[0] + 0.4 * x[0]**3, -4.0 * x[1] + 0.4 * x[1]**3])


def hessian(x):
    return numpy.array([[-4.0 + 1.2 * x[0]**2, 0], [0.0, -4.0 + 1.2 * x[1]**2]])


def normal_modes(x):
    from scipy.linalg import eigh as eig
    H = hessian(x)
    eigvalues, eigvectors = eig(H)
    eigvalues = numpy.array([float(_) for _ in eigvalues])
    return eigvalues, eigvectors
