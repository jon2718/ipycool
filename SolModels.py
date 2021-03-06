models = {
    'model_descriptor': {
        'desc': 'Name of model parameter descriptor',
        'name': 'model',
        'num_parms': 15,
        'for001_format': {
            'line_splits': [15]}},
    'bz': {
        'desc': 'Bz with constant central region + linear ends',
        'doc': '',
        'icool_model_name': 1,
        'parms': {
            'model': {
                'pos': 1, 'type': 'String', 'doc': ''},
            'strength': {
                'pos': 2, 'type': 'Real', 'doc': 'Field strength [T] '},
            'clen': {
                'pos': 3, 'type': 'Real', 'doc': 'Length of central region, CLEN[m] (You can use this to get a tapered field profile)'},
            'elen1': {
                'pos': 4, 'type': 'Real', 'doc': 'Length of entrance end region, ELEN1 [m].  This is the displacement of the upstream end of '
                                                 'the solenoid from the start of the region'},
            'offset': {
                'pos': 5, 'type': 'Real', 'doc': 'Use parameter 5 to get an indefinitely long, constant solenoidal field.'},
            'elen2': {
                'pos': 6, 'type': 'Real', 'doc': 'Length of exit end region, ELEN2 [m]. For a symmetric field, set:'
                                                 'SLEN =CLEN + ELEN1 + ELEN2. '
                                                 'Hard-edge field models can include the focusing effects of the missing fringe field by using EDGE '
                                                 'commands before and after the hard-edge field region'}}},
    'dtanh': {
            'desc': 'dTANH(z) Bz dependence',
            'doc': '',
            'icool_model_name': 2,
            'parms': {
                'model': {
                    'pos': 1, 'type': 'String', 'doc': ''},
                'strength': {
                    'pos': 2, 'type': 'Real', 'doc': 'Field strength [T] '},
                'clen': {
                    'pos': 3, 'type': 'Real', 'doc': 'Length of central region, CLEN[m] (You can use this to get a tapered field '
                                                     'profile)'},
                'elen': {
                    'pos': 4, 'type': 'Real', 'doc': 'Length for end region, ELEN [m] (This is the displacement of the upstream end of the solenoid '
                                                     'from the start of the region; for a symmetric field, set SLEN =CLEN + 2*ELEN.)'},
                'order': {
                    'pos': 5, 'type': 'Real', 'doc': 'Order of vector potential expansion {1, 3, 5, 7}'},
                'att_len': {
                    'pos': 6, 'type': 'Real', 'doc': 'End attenuation length, [m] (Set larger than maximum beam size) '},
                'offset': {
                    'pos': 7, 'type': 'Real', 'doc': 'Constant offset for Bs [T].  For a symmetric field, set'}}},
    'circ': {
            'desc': 'Field from sum of circular current loops',
            'doc': 'For a symmetric field with 1 loop, set ELEN=0.5 SLEN.',
            'icool_model_name': 3,
            'parms': {
                'model': {
                    'pos': 1, 'type': 'String', 'doc': ''},
                'strength': {
                    'pos': 2, 'type': 'Real', 'doc': 'Field strength [T] '},
                'clen': {
                    'pos': 3, 'type': 'Real', 'doc': 'Length of central region, CLEN[m].  (This is the region over which the coils are distributed))'},
                'elen': {
                    'pos': 4, 'type': 'Real', 'doc': 'Length for end region, ELEN [m] (This is the displacement of the upstream end of the solenoid '
                                                     'from the start of the region; for a symmetric field, set SLEN =CLEN + 2*ELEN.)'},
                'loops': {
                    'pos': 5, 'type': 'Real', 'doc': 'Number of coil loops'},
                'radius': {
                    'pos': 6, 'type': 'Real', 'doc': 'Radius of coils [m]'}}},
    'sheet': {
                'desc': 'Field from annular current sheet',
                'doc': '',
                'icool_model_name': 4,
                'parms': {
                    'model': {
                        'pos': 1, 'type': 'String', 'doc': ''},
                    'strength': {
                        'pos': 2, 'type': 'Real', 'doc': 'Field strength [T] '},
                    'length': {
                        'pos': 3, 'type': 'Real', 'doc': 'Length of sheet [m] '},
                    'z_offset': {
                        'pos': 4, 'type': 'Real', 'doc': 'z offset of center of sheet from start of region [m]'},
                    'radius': {
                        'pos': 5, 'type': 'Real', 'doc': 'Radius of sheet [m]'}}},
    'block': {
                'desc': 'Field from thick annular current block',
                'doc': '',
                'icool_model_name': 5,
                'parms': {
                    'model': {
                        'pos': 1, 'type': 'String', 'doc': ''},
                    'strength': {
                        'pos': 2, 'type': 'Real', 'doc': 'Field strength [T] '},
                    'length': {
                        'pos': 3, 'type': 'Real', 'doc': 'Length of block [m] '},
                    'z_offset': {
                        'pos': 4, 'type': 'Real', 'doc': 'z offset of center of block from start of of region [m]'},
                    'inner': {
                        'pos': 5, 'type': 'Real', 'doc': 'Inner radius of block [m]'},
                    'outer': {
                        'pos': 6, 'type': 'Real', 'doc': 'Outer radius of block [m]'}}},
    'interp': {
                'desc': 'Interpolate field from predefined USER r-z grid',
                'doc': 'The required format of the field map is:\n'
                       'title (A80)\n'
                       '# of z grid points (I) {1-5000}\n'
                       '# of r grid points (I) {1-100}\n'
                       'i, j, zi, rj, BZi,j, BRi,j (I, R)', 'icool_model_name': 6,
                'parms': {
                    'model': {
                        'pos': 1, 'type': 'String', 'doc': ''},
                    'grid': {
                        'pos': 2, 'type': 'Real', 'doc': 'Grid ##of user-supplied field {1-4} '},
                    'level': {
                        'pos': 3, 'type': 'Int', 'doc': 'Interpolation level {1-3}:\n'
                                                        '1: bi-linear\n'
                                                        '2: bi-quadratic polynomial\n'
                                                        '3: bi-cubic polynomial ', 'min': 1, 'max': 3}}},
    'tapered': {
                'desc': 'Tapered radius', 'doc': 'This model applies a geometry cut on particles whose radius exceeds the specified radial taper.',
                'icool_model_name': 7, 'parms': {
                    'model': {
                        'pos': 1, 'type': 'String', 'doc': ''},
                    'bc': {
                        'pos': 2, 'type': 'Real', 'doc': 'Bc [T] (flat central field strength) '},
                    'rc': {
                        'pos': 3, 'type': 'Real', 'doc': 'Rc [m] (flat central coil radius) '},
                    'lc': {
                        'pos': 4, 'type': 'Real', 'doc': 'Lc [m] (central field length) '},
                    'b1': {
                        'pos': 5, 'type': 'Real', 'doc': 'B1 [T] (starting field strength)'},
                    'r1': {
                        'pos': 6, 'type': 'Real', 'doc': 'R1 [m] (starting coil radius)'},
                    'l1': {
                        'pos': 7, 'type': 'Real', 'doc': 'L1 [m] (length of entrance transition region)'},
                    'b2': {
                        'pos': 8, 'type': 'Real', 'doc': 'B2 [T] (ending field strength)'},
                    'r2': {
                        'pos': 9, 'type': 'Real', 'doc': 'R2 [m] (ending coil radius)'},
                    'l2': {
                        'pos': 10, 'type': 'Real', 'doc': 'L2 [m] (length of exit transition region)'}}},
    'edge': {
                'desc': 'Hard-edge with adjustable end fields',
                'doc': 'The focusing deficit is B2L - ∫B2 ds. The deficit is independent of the focusing effect chosen with parameter 3.',
                'icool_model_name': 8,
                'parms': {
                    'model': {
                        'pos': 1, 'type': 'String', 'doc': ''},
                    'bs': {
                        'pos': 2, 'type': 'Real', 'doc': 'Bc [T] (flat central field strength) '},
                    'foc_flag': {
                        'pos': 3, 'type': 'Integer', 'doc': 'Flag on whether to include end focusing:\n'
                                                            '0: both entrance and exit focusing\n'
                                                            '1: exit focusing only\n'
                                                            '2: entrance focusing only\n'
                                                            '3: no edge focusing ',
                        'min': 0, 'max': 3},
                    'ent_def': {
                        'pos': 4, 'type': 'Real', 'doc': 'Focusing deficit at entrance [T2 m] '},
                    'ex_def': {
                        'pos': 5, 'type': 'Real', 'doc': 'focusing deficit at exit [T2 m]'}}},
    'fourier': {
                'desc': 'Determine field from file of Fourier coefficients',
                'doc': 'The contents of the input file for0JK.dat is\n'
                       '1 title (A80)\n'
                       '2.1 period, λ (R)\n'
                       '2.2 field strength, S (R)\n'
                       '3 maximum Fourier order (I)\n'
                       '(4 repeated for each order)\n'
                       '4.1 order, m (I) {0 – 199}\n'
                       '4.2 cm (R)\n'
                       '4.3 dm (R)\n'
                       'The on-axis field is given by:\n'
                       'f (s) = S Σ ( cm COS(u) + dm SIN(u) )\n'
                       'where u = 2πms / λ.', 'icool_model_name': 9,
                'parms': {
                        'model': {
                            'pos': 1, 'type': 'String', 'doc': ''},
                        'order': {
                            'pos': 2, 'type': 'Integer', 'doc': 'Order of off-axis expansion (I) {1, 3, 5, 7} '},
                        'scale': {
                            'pos': 3, 'type': 'Real', 'doc': '(R) Multiplies field strength '}}},
    'on_axis': {
                'desc': 'Determine field from file of on-axis field',
                'doc': '',
                'icool_model_name': 10,
                'parms': {
                        'model': {
                            'pos': 1, 'type': 'String', 'doc': ''},
                        'file_num': {
                            'pos': 2, 'type': 'Integer', 'doc': 'File number JK for input data (I) File name is for0JK.dat'},
                        'order': {
                            'pos': 3, 'type': 'Integer', 'doc': 'Order of off-axis expansion (I) {1, 3, 5, 7} '},
                        'scale': {
                            'pos': 4, 'type': 'Real', 'doc': '(R) Multiplies field strength '}}}}                                                                                             