import numpy


def _pratio(vec):
    """
    Return the participation in two normalization flavors.  Let P be
    the unnormalized participation ratio, which scales as N for
    delocalized modes.  We return 1. P/N and 2. P/L where L is the
    linear size of the system.
    """
    pra = numpy.sum([numpy.dot(ri, ri)**2 for ri in vec])
    return 1.0 / pra


def participation_ratio(vec):
    """
    Return the participation in two normalization flavors.  Let P be
    the unnormalized participation ratio, which scales as N for
    delocalized modes.  We return 1. P/N and 2. P/L where L is the
    linear size of the system.
    """
    pra = numpy.sum([numpy.dot(vec[:, i], vec[:, i])**2 for i in range(vec.shape[1])])
    return 1.0 / pra


def zero_modes(eigvalues):
    return len([_ for _ in eigvalues if abs(_) < 1e-10])


def unstable_modes(eigvalues):
    return len([_ for _ in eigvalues if _ < -1e-10])


def smallest_nonzero_mode(eigvalues):
    # We assume eigvalues are sorted
    small = None
    zero = 1e-10
    for eigv in eigvalues:
        if eigv < -zero:
            # Unstable modes
            small = eigv
        elif abs(eigv) <= zero:
            # Zero modes
            continue
        else:
            # Compare the smallest positive and negative
            if small is None or eigv < abs(small):
                small = eigv
            break
    return small


def format_table(db, fmt=None, columns=None, layout='xyz'):

    # We partition the dict into scalars and vectors entries
    scalars = {}
    vectors = {}
    for key in db:
        if isinstance(db[key], (tuple, list, numpy.ndarray)):
            vectors[key] = db[key]
        else:
            scalars[key] = db[key]

    # We will format all vectors as columns, unless columns is given
    if columns is None:
        columns = vectors.keys()
    else:
        # Make sure requested columns are there
        diff = set(columns) - set(vectors.keys())
        if len(diff) > 0:
            raise ValueError('some requested columns are not found {}'.format(diff))

    # Formatting options
    if layout == 'xyz':
        comment = ''
        scalar_sep = ' '
    elif layout == 'plain':
        if len(vectors) > 0:
            comment = '# '
            scalar_sep = '\n'
        else:
            comment = ''
            scalar_sep = '\n'

    # We provide formatting fields for every key (some may be provided)
    _fmt = {}
    for key in db:
        if fmt is not None and key in fmt:
            _fmt[key] = fmt[key]
        else:
            _fmt[key] = ''

    # The head (first line) is empty by default
    head = ''
    meta = []

    # Format scalars as metadata
    if len(scalars) > 0:
        lines = []
        for key in sorted(scalars):
            local_fmt = '{comment}{{}}={{:{fmt}}}'.format(comment=comment, fmt=_fmt[key])
            meta.append(local_fmt.format(key, scalars[key]))

    # Format arrays into columns
    if len(vectors) > 0:
        # Check that all arrays have the same length
        all_len = [len(vectors[key]) for key in vectors]
        if len(set(all_len)) == 1:
            actual_len = all_len[0]
        else:
            raise ValueError('cannot format vectors of different sizes')

        # In xyz format, the head is the number of lines following the comment line
        head = '{}\n'.format(actual_len)
        # Add information on the columns being formatted
        entry = ','.join(columns)
        meta.append('{}columns={}'.format(comment, entry))

        # Format lines element-wise
        lines = []
        for i in range(actual_len):
            data = []
            for key in columns:
                local_fmt = '{{:{fmt}}}'.format(fmt=_fmt[key])
                data.append(local_fmt.format(vectors[key][i]))
            lines.append(' '.join(data))

    if layout == 'xyz':
        txt = head + scalar_sep.join(meta).strip() + '\n' + '\n'.join(lines) + '\n'
    else:
        txt = scalar_sep.join(meta) + '\n' + '\n'.join(lines) + '\n'
    return txt.strip()

# db = {'test1': 'AA', 'test': 1.0, 'array': [1.0, 2.0, 3.0], 'array2': [1,2,3] }
# fmt = {'array2': 'd', 'array': '.8f'}
# print format_table(db, fmt)
# print format_table(db, fmt, columns=('array', 'array2'))
# print format_table(db, fmt, layout='plain')

# db = {key: db[key] for key in db if not key.startswith('array')}
# print format_table(db, fmt, layout='plain')
