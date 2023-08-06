"""
Atooms wrappers to the optimization methods.

They require an atooms compatible `system` object and the desired
`surface` to optimize.
"""

import numpy
from atooms.core.utils import setup_logging
from .helpers import zero_modes, unstable_modes, smallest_nonzero_mode
from .surfaces import potential_energy, force_norm_square


__all__ = ["eigenvector_following", "conjugate_gradient",
           "limited_bfgs", "l_bfgs", "normal_modes_analysis",
           "steepest_descent", "force_minimization"]


def _setup_log(file_log, verbose):
    if file_log is not None:
        setup_logging(level=20, filename=file_log)
    if verbose:
        setup_logging(level=20)


# TODO: add fold parameter to make sure particles are folded during the minimiization
def eigenvector_following(system, surface=potential_energy,
                          trust_radius=0.2, file_log=None,
                          file_debug=None, freeze_iter=-1,
                          freeze_gnorm=-1.0, freeze_modes=None,
                          unstable_modes=-1, max_iter=4000,
                          max_trust=1.0, gtol=1e-10,
                          threshold_error=1.0, trust_scale_up=1.2,
                          kick_tol=-1.0, kick_delta=1e-5,
                          trust_scale_down=1.2, zero_mode=1e-10,
                          callback=None, debug=False, verbose=False):
    from .methods import eigenvector_following as _eigenvector_following

    # Alias (to be deprecated)
    if freeze_modes is not None:
        unstable_modes = int(freeze_modes)
    _setup_log(file_log, verbose)
    coords = system.dump("position", view=True, order='F')
    stats = _eigenvector_following(coords,
                                   function=surface.value,
                                   gradient=surface.gradient,
                                   normal_modes=surface.normal_modes,
                                   callback=callback,
                                   args=(system, ),
                                   file_debug=file_debug,
                                   trust_radius=trust_radius,
                                   max_iter=max_iter,
                                   gtol=gtol,
                                   trust_fixed=False,
                                   freeze_iter=freeze_iter,
                                   freeze_gnorm=freeze_gnorm,
                                   unstable_modes=unstable_modes,
                                   max_trust=max_trust,
                                   min_trust=1e-7,
                                   threshold_error=threshold_error,
                                   trust_scale_up=trust_scale_up,
                                   trust_scale_down=trust_scale_down,
                                   kick_tol=kick_tol, kick_delta=kick_delta,
                                   zero_mode=zero_mode,
                                   debug=debug
                                   )
    system.fold()
    return stats


def conjugate_gradient(system, surface=potential_energy, verbose=False):
    from scipy.optimize import minimize

    coords = system.dump("position", order='F', flat=True)
    # Clearing the dump is necessary, otherwise the particle data will
    # point to a dead array, it seems, and they will receive no update
    # when dumping with a view.
    system.dump(clear=True)
    result = minimize(surface.value, coords, method='CG',
                      args=(system, ), jac=surface.gradient,
                      options={'gtol': 1e-10}
                      )
    result.pop('x')
    result.pop('jac')
    system.fold()
    return result


def l_bfgs(system, surface=potential_energy, maxcor=300, gtol=1e-10,
           verbose=False):
    from scipy.optimize import minimize

    coords = system.dump("position", order='F', flat=True)
    # Clearing the dump is necessary, otherwise the particle data will
    # point to a dead array, it seems, and they will receive no update
    # when dumping with a view.
    system.dump(clear=True)

    result = minimize(surface.value,
                      coords, method='L-BFGS-B',
                      args=(system, ),
                      jac=surface.gradient,
                      options={'ftol': 1e-14,
                               'gtol': gtol,
                               'iprint': 10 if verbose else -1,
                               'maxcor': maxcor})
    result['iterations'] = result['nit']
    result['function'] = surface.value(result['x'], system)
    result['gradient_norm_square'] = numpy.sum(surface.gradient(result['x'], system)**2)
    result.pop('x')
    result.pop('jac')
    system.fold()
    return result


# Alias
limited_bfgs = l_bfgs


def force_minimization(system, maxcor=300, gtol=1e-10, verbose=False):
    result = l_bfgs(system, surface=force_norm_square, maxcor=maxcor,
                    gtol=gtol, verbose=verbose)
    return result


def steepest_descent(system, surface=potential_energy, file_log=None,
                     sample=0, maxiter=4000000, verbose=False):
    from .methods import steepest_descent

    _setup_log(file_log, verbose)
    coords = system.dump("position", view=True, order='F')
    result = steepest_descent(coords,
                              function=surface.value,
                              gradient=surface.gradient,
                              maxiter=maxiter,
                              args=(system, ),
                              )
    result['gradient_norm_square'] = numpy.sum(surface.gradient(coords, system)**2)
    system.fold()
    return result


def normal_modes_analysis(system, surface=potential_energy):
    from .helpers import participation_ratio

    coords = system.dump("position", view=True, order='F')
    eigvalues, eigvectors = potential_energy.normal_modes(coords, system)
    system.eigvalues = eigvalues
    system.eigvectors = eigvectors

    N = len(system.particle)
    L = system.cell.side[0]

    db = {}
    db['eigenvalue'] = eigvalues
    db['eigenvector'] = eigvectors
    db['number_of_zero_modes'] = zero_modes(eigvalues)
    db['number_of_unstable_modes'] = unstable_modes(eigvalues)
    db['smallest_nonzero_mode'] = smallest_nonzero_mode(eigvalues)
    db['fraction_of_unstable_modes'] = float(unstable_modes(eigvalues)) / len(eigvalues)
    db['potential_energy'] = system.potential_energy(per_particle=True, cache=True)
    db['force_norm_square'] = system.force_norm_square(per_particle=True, cache=True)
    db['participation_ratio'] = [participation_ratio(eigvectors[i]) for i in range(len(eigvectors))]
    db['participation_ratio_over_L'] = [_ / L for _ in db['participation_ratio']]
    db['participation_ratio_over_N'] = [_ / N for _ in db['participation_ratio']]

    return db
