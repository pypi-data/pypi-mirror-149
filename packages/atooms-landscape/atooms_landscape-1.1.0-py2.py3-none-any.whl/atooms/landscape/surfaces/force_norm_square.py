cache_value = False

# TODO: refactor this


def _pack_coords(coords, system):
    for i, p in enumerate(system.particle):
        p.position[:] = coords[3 * i: 3 * (i + 1)]


def value(coords, system, flat=False):
    if cache_value:
        return system.force_norm_square(cache=True, per_particle=False)
    else:
        if len(coords.shape) == 1:
            _pack_coords(coords, system)
        return system.force_norm_square(per_particle=False)


def gradient(coords, system, flat=False):
    if len(coords.shape) == 1:
        _pack_coords(coords, system)
        system.compute_interaction("gradw")
        return system.interaction.gradw.flatten(order='F')
    else:
        return system.interaction.gradw
