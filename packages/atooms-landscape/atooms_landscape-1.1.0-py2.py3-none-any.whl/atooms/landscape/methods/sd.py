from __future__ import print_function
import logging
import numpy


_log = logging.getLogger(__name__)


def steepest_descent(coords, function, gradient, zero=1e-10,
                     maxiter=10000, gtol=1e-10, dx=0.001,
                     dump_coords=False, args=()):

    # Initialize data structures
    ndof = coords.size
    result = {}
    _log.info('# columns:iteration,U,W,n_u\n')

    # Main loop
    Uold = None
    for iteration in range(maxiter):
        grad = gradient(coords, *args)
        U = function(coords, *args)
        W = numpy.sum(grad**2) / ndof
        if dump_coords:
            _log.info(('{} {} {} {} {}\n'.format(iteration, U, W, -1, coords)).replace(']', '').replace('[', ''))
        else:
            _log.info('{} {} {} {}\n'.format(iteration, U, W, -1))

        if W < gtol:
            _log.info('# Reached convergence W={} (GTOL)\n'.format(W))
            break
        if iteration > 0 and abs(U - Uold) < zero:
            _log.info('# Reached function tolerance (FTOL) !\n')
            break
        if iteration == maxiter - 1:
            _log.info('# Reached maximum number of iterations {} (MAXITER)\n'.format(maxiter))

        # Store old values at this step
        Uold = U

        # Update coordinates
        coords -= grad * dx

    result['x'] = coords
    return result
