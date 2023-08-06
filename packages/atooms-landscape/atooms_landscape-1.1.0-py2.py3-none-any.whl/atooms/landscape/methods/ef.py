from __future__ import print_function
import sys
import os
import logging
import numpy
from atooms.core.utils import mkdir


_log = logging.getLogger(__name__)


def _zero_modes(eigvalues):
    return len([_ for _ in eigvalues if abs(_) < 1e-10])


def _unstable_modes(eigvalues):
    return len([_ for _ in eigvalues if _ < -1e-10])


def _stable_modes(eigvalues):
    return len([_ for _ in eigvalues if _ > -1e-10])


def eigenvector_following(coords, function, gradient, normal_modes,
                          callback=None, zero=numpy.finfo(float).eps,
                          zero_mode=1e-10, max_iter=10000,
                          method='ef', trust_radius=0.01,
                          trust_fixed=False, gtol=1e-10,
                          unstable_modes=-1, freeze_iter=-1,
                          freeze_gnorm=-1.0, step_scale=None,
                          min_trust=None, max_trust=None,
                          threshold_error=1.0, trust_scale_up=1.2,
                          trust_scale_down=1.2, kick_tol=-1.0,
                          kick_delta=1e-5,
                          W_max=numpy.finfo(float).max,
                          dump_coords=False, debug=False,
                          file_debug=None, args=()):

    # Checks
    assert abs(kick_tol) > zero, 'kick tolerance must be larger than function tolerance'

    initialized = False
    result = {}
    _log.info('# columns:iteration,U,W,n_u\n')

    if file_debug is not None:
        debug = True  # turns debugging on
        mkdir(os.path.dirname(file_debug))
        fh_debug = open(file_debug, "wb", buffering=0)
    else:
        fh_debug = None

    # Sanitize freeze
    if freeze_iter < 0:
        freeze_iter = max_iter

    # These variables will be initialized later on
    eigvectors = None
    eigvectors_old = None
    dx_old = None
    trust = None

    # Main loop
    U_old = None
    for iteration in range(max_iter):
        grad = gradient(coords, *args)
        U = function(coords, *args)
        W = numpy.sum(grad**2) / coords.size

        # If last step dangerously raised the gradient
        # - revert coordinates
        # - reduce the trust radii
        # - recompute function and gradient
        reverted = False
        if initialized and W > W_max:
            reverted = True
            _log.info('# revert step at {} because {} > {}\n'.format(iteration, W, W_max))
            nr_step = numpy.zeros_like(coords)
            for i in range(len(eigvectors)):
                nr_step += dx_old[i] * eigvectors_old[i]
            coords -= nr_step
            for i in range(len(trust)):
                trust[i] /= 10  # trust_scale_down
            grad = gradient(coords, *args)
            U = function(coords, *args)
            W = numpy.sum(grad**2) / coords.size

        # Compute eigenvalues and eigenvectors
        eigvalues, eigvectors = normal_modes(coords, *args)
        n_u = _unstable_modes(eigvalues)

        # Callback
        if callback is not None:
            callback(iteration, coords, *args)

        # Logs
        if dump_coords:
            _log.info(('{} {} {} {} {}\n'.format(iteration, U, W, n_u, coords)).replace(']', '').replace('[', ''))
        else:
            _log.info('{} {} {} {}\n'.format(iteration, U, W, n_u))

        # Convergence criteria
        if W < gtol:
            if unstable_modes < 0 or n_u == unstable_modes:
                result['success'] = True
                result['message'] = 'Reached norm gradient tolerance (GTOL)'
                _log.info('# Reached convergence W={} n_u={} after n_iter={} (GTOL)\n'.format(W, n_u, iteration))
                break
            else:
                result['success'] = False
                result['message'] = 'Reached convergence on W but n_u is wrong (ERR)'
                _log.info('# Reached convergence on W but n_u {} is wrong (should be {})\n'.format(n_u, unstable_modes))

        if iteration > 0 and abs(U - U_old) < zero and not reverted:
            result['success'] = False
            result['message'] = 'Reached function tolerance (FTOL)'
            _log.info('# Reached function tolerance (FTOL) !\n')
            break
        if iteration == max_iter - 1:
            result['success'] = False
            result['message'] = 'Reached maximum number of iterations (MAXITER)'
            _log.info('# Reached maximum number of iterations {} (MAXITER)\n'.format(max_iter))

        # Drop zero-mode entirely. This way the connect between
        # eigenvalues at successive steps is preserved
        # TODO: there must be a more efficient / elegant better way
        new_eigvalues = []
        new_eigvectors = []
        for i in range(len(eigvalues)):
            if abs(eigvalues[i]) > zero_mode:
                new_eigvectors.append(eigvectors[i])
                new_eigvalues.append(eigvalues[i])
        eigvalues = new_eigvalues
        eigvectors = new_eigvectors

        # Initialize data structures
        if not initialized:
            initialized = True
            ndof = len(eigvalues)
            trust = [trust_radius] * ndof
            gold = [None] * ndof
            dx = [0.0] * ndof
            dx_old = [None] * ndof
            eigvectors_old = [None] * ndof
            S = [0] * ndof
            frozen = False
            rel_err = [0.0] * ndof
            debug_info = {}
            U_old = None

        # Freeze a set of modes from the start
        if unstable_modes >= 0 and not frozen:
            frozen = True
            for i in range(len(S)):
                if i < unstable_modes:
                    S[i] = 1.0
                else:
                    S[i] = -1.0

        # Determine step dx along each eigenvector
        assert len(eigvalues) == ndof, 'number of zero modes changed, smallest is {}'.format(numpy.min(numpy.abs(eigvalues)))
        dx = [0.0] * len(eigvalues)
        for i in range(len(eigvalues)):
            gi = numpy.dot(grad.flatten(), eigvectors[i].flatten())
            hi = eigvalues[i]

            if method in ['newton-raphson', 'nr']:
                # Netwon-Rapshon step
                dx[i] = - gi / hi

            elif method in ['eigenvector-following', 'ef']:
                # Uphill/downhill step according to Wales JCP 101, 3750 (1994)
                if not frozen:
                    S[i] = 1.0 if hi < 0 else -1.0
                dx[i] = S[i] * (2 * gi) / (abs(hi) * (1.0 + (1.0 + (2.0 * gi / hi)**2)**0.5))
            else:
                raise ValueError('unknown method')

            # We compute the deviation of the estimated eigenvalue
            # along this direction and its actual value and update the
            # trust radius accordingly.
            if iteration > 0 and not trust_fixed:
                if abs(dx[i]) > 0 and abs(dx_old[i]) > 0:
                    # Estimate of eigenvalue
                    he = (gi - gold[i]) / dx_old[i]
                    # Ruscher correction
                    he -= (numpy.dot(grad.flatten(), (eigvectors[i] - eigvectors_old[i]).flatten())) / dx_old[i]
                    # Update local trust radius based on relative error, r, on eigenvalue
                    rel_err[i] = abs((he - hi) / hi)
                    # Relative threshold error of 100% is large but works well for high dimensional systems
                    # For he MB surface the choice 0.1 gives more stable results
                    if rel_err[i] < threshold_error:
                        trust[i] *= trust_scale_up
                    else:
                        trust[i] /= trust_scale_down
                    if max_trust is not None:
                        trust[i] = min(trust[i], max_trust)
                    if min_trust is not None:
                        trust[i] = max(trust[i], min_trust)

            gold[i] = gi.copy()
            eigvectors_old[i] = eigvectors[i].copy()

        # Determine whether to freeze the steps at next iteration (ef method)
        # Freeze signs after freeze_iter iterations.
        # Also if grad norm goes below freeze_gnorm then freeze the signs
        if not frozen:
            if (freeze_gnorm >= 0 and W <= freeze_gnorm) or \
               (freeze_iter >= 0 and iteration >= freeze_iter):
                frozen = True

        # Make sure all steps are within the trust radii
        scale = 1.0
        for i in range(len(dx)):
            if abs(dx[i]) > trust[i]:
                scale_i = abs(dx[i]) / trust[i]
                scale = max(scale, scale_i)

        for i in range(len(dx)):
            dx[i] /= scale

        # Update coordinates
        nr_step = numpy.zeros_like(coords)
        for i in range(len(eigvectors)):
            nr_step += dx[i] * eigvectors[i]
        coords += nr_step

        # If convergence is slow, try a random kick
        if U_old and kick_tol > 0.0 and abs(U - U_old) < kick_tol:
            print('# kicking at iteration', iteration, 'because', abs(U - U_old), '<', kick_tol)
            delta = kick_delta * (numpy.random.random(coords.shape) - 1.0)
            coords += delta

        # Store old values at this step
        U_old = U
        for i in range(len(dx)):
            dx_old[i] = dx[i]

        # Store debug info
        if debug:
            import warnings
            warnings.filterwarnings("ignore")
            debug_info['iteration'] = iteration
            debug_info['W'] = W
            debug_info['scale'] = scale
            debug_info['dx_mean'] = numpy.mean(numpy.abs(dx))
            debug_info['dx_max'] = numpy.max(numpy.abs(dx))
            debug_info['dx_max_eigval'] = eigvalues[numpy.argmax(numpy.abs(dx))]
            debug_info['dx_max_eigval_idx'] = numpy.argmax(numpy.abs(dx))
            debug_info['rel_err_mean'] = numpy.mean(rel_err)
            debug_info['rel_err_max'] = numpy.max(rel_err)
            debug_info['rel_err_min'] = numpy.min(rel_err)
            debug_info['rel_err_max_eigval'] = eigvalues[numpy.argmax(rel_err)]
            debug_info['rel_err_max_eigval_idx'] = numpy.argmax(rel_err)
            debug_info['rel_err_min_eigval'] = eigvalues[numpy.argmin(rel_err)]
            debug_info['rel_err_min_eigval_idx'] = numpy.argmin(rel_err)
            debug_info['eigval_softest'] = sorted(numpy.abs(eigvalues))[0]
            debug_info['eigval_unstable'] = n_u
            debug_info['trust_mean'] = numpy.mean(trust)
            debug_info['trust_at_max'] = len([_ for _ in trust if _ == max_trust])
            debug_info['trust_at_min'] = len([_ for _ in trust if _ == min_trust])
            debug_info['trust_at_max_eigval'] = numpy.mean([eigvalues[i] for i, _ in enumerate(trust) if _ == max_trust])
            debug_info['trust_at_min_eigval'] = numpy.mean([eigvalues[i] for i, _ in enumerate(trust) if _ == min_trust])
            warnings.resetwarnings()

            if fh_debug is not None:
                import pickle
                pickle.dump(debug_info, fh_debug)
            else:
                import copy
                if 'debug' not in result:
                    result['debug'] = []
                result['debug'].append(copy.deepcopy(debug_info))

    if fh_debug is not None:
        fh_debug.close()

    result['iterations'] = iteration
    result['function'] = U
    result['gradient_norm_square'] = W
    result['number_of_unstable_modes'] = n_u
    return result
