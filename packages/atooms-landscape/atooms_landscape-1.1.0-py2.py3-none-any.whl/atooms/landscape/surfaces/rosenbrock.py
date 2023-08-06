import numpy

# The rosenbrock function


def rosenbrock(x):
    return .5 * (1 - x[0])**2 + (x[1] - x[0]**2)**2


def d_rosenbrock(x):
    return numpy.array((-2 * .5 * (1 - x[0]) - 4 * x[0] * (x[1] - x[0]**2), 2 * (x[1] - x[0]**2)))


def dd_rosenbrock(x):
    return numpy.array([[1 - 4 * (x[1] - x[0]**2) + 8 * x[0]**2, -4 * x[0]], [-4 * x[0], 2]])


def nm_rosenbrock(x):
    H = dd_rosenbrock(x)
    from scipy.linalg import eigh as eig
    eigvalues, eigvectors = eig(H)
    eigvalues = numpy.array([float(_) for _ in eigvalues])
    return eigvalues, eigvectors
