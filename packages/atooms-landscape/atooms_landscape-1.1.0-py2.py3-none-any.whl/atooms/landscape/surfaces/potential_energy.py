cache_value = False


def normal_modes(coords, system):
    import os
    from scipy.linalg import eigh as eig

    os.environ['OPENBLAS_NUM_THREADS'] = '1'
    system.compute_interaction('hessian')
    ndof = len(system.particle) * system.number_of_dimensions
    hessian = system.interaction.hessian.reshape((ndof, ndof), order='F')
    eigvalues, eigvectors = eig(hessian)
    eigvalues = [float(_) for _ in eigvalues]
    tmp_eigv = []
    for i in range(len(eigvalues)):
        tmp_eigv.append(eigvectors[:, i].reshape((system.number_of_dimensions, len(system.particle)), order='F'))
    eigvectors = tmp_eigv
    return eigvalues, eigvectors


def _pack_coords(coords, system):
    for i, p in enumerate(system.particle):
        p.position[:] = coords[3 * i: 3 * (i + 1)]


def value(coords, system):
    """
    if `cache` is `True` we do not recompute the value but assume it
    has already been computed because e.g. of a call to `gradient`
    """
    if cache_value:
        return system.potential_energy(cache=True, per_particle=False)
    else:
        if len(coords.shape) == 1:
            _pack_coords(coords, system)
        return system.potential_energy(per_particle=False)


def gradient(coords, system):
    if len(coords.shape) == 1:
        _pack_coords(coords, system)
        system.compute_interaction("forces")
        return - system.interaction.forces.flatten(order='F')
    else:
        system.compute_interaction("forces")
        return - system.interaction.forces
