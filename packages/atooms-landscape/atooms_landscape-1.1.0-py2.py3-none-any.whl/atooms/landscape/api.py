import os
from atooms.core.utils import mkdir
from atooms.trajectory import Trajectory
from atooms.models.f90 import Interaction
from .factory import optimize
from .core import normal_modes_analysis
from .helpers import zero_modes, unstable_modes, format_table


# The disadvantage of a single entry point + factory is that there is an extra layer to propagate the options

def pes(file_inp, frame=0, method='ef', nma=False, model=None,
        file_out='{file_inp}.{method}',
        file_cfg='{file_out}.{fmt}',
        file_log='{file_out}.log',
        file_nma='{file_out}.nma', fmt='xyz',
        lbfgs_gtol=1e-10, lbfgs_maxcor=300, lbfgs_verbose=False,
        wmin_gtol=1e-10, wmin_maxcor=300, wmin_verbose=False,
        ef_freeze_modes=-1, ef_gtol=1e-10, ef_trust_radius=0.2,
        ef_freeze_iter=-1, ef_freeze_gnorm=-1.0, ef_max_trust=1.0,
        ef_file_debug=None,
        ef_max_iter=4000):

    config = locals()

    # Interpolate paths with local variables
    file_out = file_out.format(**locals())
    file_cfg = file_cfg.format(**locals())
    file_log = file_log.format(**locals())
    file_nma = file_nma.format(**locals())
    mkdir(os.path.dirname(file_out))

    # Provide interaction and analyze frame
    with Trajectory(file_inp) as th:
        system = th[frame]
        system.species_layout = 'F'
        system.interaction = Interaction(model)
        step = th.steps[frame]
    # Optimize
    out = optimize(method, system, **config)

    # Write stats
    with open(file_log, 'w') as fh_out:
        txt = format_table(out, layout='plain')
        fh_out.write(txt)

    # Write optimized system
    with Trajectory(file_cfg, 'w', fmt=fmt) as th_out:
        if model is not None:
            th_out.metadata['model'] = model
        th_out.precision = 14
        th_out.write(system, step=step)

    # Normal modes analysis
    if nma:
        out = normal_modes_analysis(system)
        out['step'] = step
        with open(file_nma, 'w') as fh_out:
            txt = format_table(out, columns=['eigenvalue', 'participation_ratio'])
            fh_out.write(txt)

    # with TrajectoryHDF5(file_out, 'w') as th:
    #     system.interaction = None  # remove interaction from hdf5 file
    #     for p in system.particle:
    #         p.species = p.species[()]
    #     th.write(system, step=0)


# TODO: use file_out
def nma(file_inp, model=None, frame=0, file_nma='{file_inp}.nma'):

    config = locals()

    # Interpolate paths with local variables
    file_nma = file_nma.format(**locals())
    mkdir(os.path.dirname(file_nma))

    # Provide interaction and analyze frame
    with Trajectory(file_inp) as th:
        system = th[frame]
        system.species_layout = 'F'
        system.interaction = Interaction(model)
        step = th.steps[frame]

    out = normal_modes_analysis(system)
    out['step'] = step

    with open(file_nma, 'w') as fh_out:
        txt = format_table(out, columns=['eigenvalue', 'participation_ratio'])
        fh_out.write(txt)
