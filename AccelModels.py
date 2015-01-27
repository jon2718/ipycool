models = {
        'model_descriptor': {
            'desc': 'Name of model parameter descriptor',
            'name': 'model',
            'num_parms': 15,
            'for001_format': {
                'line_splits': [15]}},
        'ez': {
            'desc': 'Ez only with no transverse variation',
            'doc': '',
            'icool_model_name': 1,
            'parms': {
                'model': {
                    'pos': 1, 'type': 'String', 'doc': ''},
                'freq': {
                    'pos': 2, 'type': 'Real', 'doc': 'Frequency [MHz]'},
                'grad': {
                    'pos': 3, 'type': 'Real', 'doc': 'Gradient on-axis at center of gap [MV/m]'},
                'phase': {
                    'pos': 4, 'type': 'Real', 'doc': 'Phase shift [deg] {0-360}.'},
                'rect_cyn': {
                    'pos': 5, 'type': 'Real', 'doc': 'Parameter to approximate a rectangular cavity '
                                      'in cylindrical geometry; if set to radius of curvature ρ, then EZ is scaled by '
                                      '1-x/ ρ, where x is the horizontal distance from the reference circle.'},
                'mode': {
                    'pos': 8, 'type': 'Int', 'doc': '0 : Time-independent 1: sinusoidal time variation'}}},
        'cyn_pill': {
            'desc': 'Cylindrical TM01p pillbox',
            'doc': '', 'icool_model_name': 2,
            'parms': {
                    'model': {
                        'pos': 1, 'type': 'String', 'doc': ''},
                    'freq': {
                        'pos': 2, 'type': 'Real', 'doc': ''},
                    'grad': {
                        'pos': 3, 'type': 'Real', 'doc': ''},
                    'phase': {
                        'pos': 4, 'type': 'Real', 'doc': ''},
                    'rect_cyn': {
                        'pos': 5, 'type': 'Real', 'doc': ''},
                    'longitudinal_mode': {
                        'pos': 8, 'type': 'Real', 'doc': ''}}},
        'trav': {
            'desc': 'Traveling wave cavity',
            'doc': '',
            'icool_model_name': 3,
            'parms': {
                    'model': {
                        'pos': 1, 'type': 'String', 'doc': ''},
                    'freq': {
                        'pos': 2, 'type': 'Real', 'doc': ''},
                    'grad': {
                        'pos': 3, 'type': 'Real', 'doc': ''},
                    'phase': {
                        'pos': 4, 'type': 'Real', 'doc': ''},
                    'rect_cyn': {
                        'pos': 5, 'type': 'Real', 'doc': ''},
                    'x_offset': {
                        'pos': 6, 'type': 'Real', 'doc': ''},
                    'y_offset': {
                        'pos': 7, 'type': 'Real', 'doc': ''},
                    'phase_velocity': {
                        'pos': 8, 'type': 'Real', 'doc': ''}}},
        'circ_nose': {
            'desc': 'Approximate fields for symmetric circular-nosed cavity',
            'doc': '',
            'icool_model_name': 4,
            'parms': {
                    'model': {
                        'pos': 1, 'type': 'String', 'doc': ''},
                    'freq': {
                        'pos': 2, 'type': 'Real', 'doc': ''},
                    'grad': {
                        'pos': 3, 'type': 'Real', 'doc': ''},
                    'phase': {
                        'pos': 4, 'type': 'Real', 'doc': ''},
                    'length': {
                        'pos': 8, 'type': 'Real', 'doc': ''},
                    'gap': {
                        'pos': 9, 'type': 'Real', 'doc': ''},
                    'drift_tube_radius': {
                        'pos': 10, 'type': 'Real', 'doc': ''},
                    'nose_radius': {
                        'pos': 11, 'type': 'Real', 'doc': ''}}},
        'az_tm': {
            'desc': 'User-supplied azimuthally-symmetric TM mode (SuperFish)',
            'doc': '', 'icool_model_name': 5,
            'parms': {
                    'model': {
                        'pos': 1, 'type': 'String', 'doc': ''},
                    'freq': {
                        'pos': 2, 'type': 'Real', 'doc': ''},
                    'phase': {
                        'pos': 4, 'type': 'Real', 'doc': ''},
                    'file_no': {
                        'pos': 8, 'type': 'Real', 'doc': ''},
                    'field_strength_norm': {
                        'pos': 9, 'type': 'Real', 'doc': ''},
                    'rad_cut': {
                        'pos': 10, 'type': 'Real', 'doc': ''},
                    'axial_dist': {
                        'pos': 11, 'type': 'Real', 'doc': ''},
                    'daxial_sym': {
                        'pos': 12, 'type': 'Real', 'doc': ''}}},
        'ilpoly': {
            'desc': 'Induction linac model - waveform from user-supplied polynomial coefficients',
            'doc': '', 'icool_model_name': 6,
            'parms': {
                    'model': {
                        'pos': 1, 'type': 'String', 'doc': ''},
                    'time_offset': {
                        'pos': 2, 'type': 'Real', 'doc': ''},
                    'gap': {
                        'pos': 3, 'type': 'Real', 'doc': ''},
                    'time_reset': {
                        'pos': 4, 'type': 'Real', 'doc': ''},
                    'v0': {
                        'pos': 5, 'type': 'Real', 'doc': ''},
                    'v1': {
                        'pos': 6, 'type': 'Real', 'doc': ''},
                    'v2': {
                        'pos': 7, 'type': 'Real', 'doc': ''},
                    'v3': {
                        'pos': 8, 'type': 'Real', 'doc': ''},
                    'v4': {
                        'pos': 9, 'type': 'Real', 'doc': ''},
                    'v5': {
                        'pos': 10, 'type': 'Real', 'doc': ''},
                    'v6': {
                        'pos': 11, 'type': 'Real', 'doc': ''},
                    'v7': {
                        'pos': 12, 'type': 'Real', 'doc': ''},
                    'v8': {
                         'pos': 13, 'type': 'Real', 'doc': ''}}},
        'ilgen': {
            'desc': 'Induction linac model - waveform from internally generated waveform',
            'doc': '',
            'icool_model_name': 7,
            'parms': {
                    'model': {
                        'pos': 1, 'type': 'String', 'doc': ''},
                    'num_gaps': {
                        'pos': 2, 'type': 'Real', 'doc': ''},
                    'start_volt': {
                        'pos': 3, 'type': 'Real', 'doc': ''},
                    'volt_swing': {
                        'pos': 4, 'type': 'Real', 'doc': ''},
                    'time_offset': {
                        'pos': 5, 'type': 'Real', 'doc': ''},
                    'kin': {
                        'pos': 6, 'type': 'Real', 'doc': ''},
                    'pulse_dur': {
                        'pos': 7, 'type': 'Real', 'doc': ''},
                    'slope': {
                        'pos': 8, 'type': 'Real', 'doc': ''},
                    'bins': {
                        'pos': 9, 'type': 'Real', 'doc': ''},
                    'gap_len': {
                        'pos': 10, 'type': 'Real', 'doc': ''},
                    'file_num': {
                        'pos': 11, 'type': 'Real', 'doc': ''},
                    'kill': {
                        'pos': 12, 'type': 'Real', 'doc': ''},
                    'restart': {
                        'pos': 13, 'type': 'Real', 'doc': ''}}},
        'ilfile': {
            'desc': 'Induction linac model - Waveform from user-supplied file',
            'doc': '',
            'icool_model_name': 8,
            'parms': {
                    'model': {
                        'pos': 1, 'type': 'String', 'doc': ''},
                    'time_offset': {
                        'pos': 2, 'type': 'Real', 'doc': ''},
                    'gap': {
                        'pos': 3, 'type': 'Real', 'doc': ''},
                    'time_reset': {
                        'pos': 4, 'type': 'Real', 'doc': ''},
                    'file_num_wav': {
                        'pos': 5, 'type': 'Real', 'doc': ''},
                    'poly_order': {
                        'pos': 6, 'type': 'Real', 'doc': ''},
                    'file_num_out': {
                        'pos': 7, 'type': 'Real', 'doc': ''},
                    'time_inc': {
                        'pos': 8, 'type': 'Real', 'doc': ''}}},
        'sec_pill_circ': {
            'desc': 'Sector-shaped pillbox cavity (circular cross section)',
            'doc': '',
            'icool_model_name': 9,
            'parms': {
                    'model': {
                        'pos': 1, 'type': 'String', 'doc': ''},
                    'freq': {
                        'pos': 2, 'type': 'Real', 'doc': ''},
                    'grad': {
                        'pos': 3, 'type': 'Real', 'doc': ''},
                    'phase': {
                        'pos': 4, 'type': 'Real', 'doc': ''}}},
        'var_pill': {
            'desc': 'Variable {frequency gradient} pillbox cavity',
            'doc': '',
            'icool_model_name': 10,
            'parms': {
                    'model': {
                        'pos': 1, 'type': 'String', 'doc': ''},
                    'phase': {
                        'pos': 2, 'type': 'Real', 'doc': ''},
                    'num_wavelengths': {
                        'pos': 3, 'type': 'Real', 'doc': ''},
                    'reset_parms': {
                        'pos': 4, 'type': 'Real', 'doc': ''},
                    'buncher_len': {
                        'pos': 5, 'type': 'Real', 'doc': ''},
                    'g0': {
                        'pos': 6, 'type': 'Real', 'doc': ''},
                    'g1': {
                        'pos': 7, 'type': 'Real', 'doc': ''},
                    'g2': {
                        'pos': 8, 'type': 'Real', 'doc': ''},
                    'phase_model': {
                        'pos': 9, 'type': 'Real', 'doc': ''}}},
        'straight_pill': {
                'desc': 'Straight pillbox or SuperFish cavity in dipole region',
                'doc': '',
                'icool_model_name': 11,
                'parms': {
                        'model': {
                            'pos': 1, 'type': 'String', 'doc': ''},
                        'freq': {
                            'pos': 2, 'type': 'Real', 'doc': ''},
                        'grad': {
                            'pos': 3, 'type': 'Real', 'doc': ''},
                        'phase': {
                            'pos': 4, 'type': 'Real', 'doc': ''},
                        'radial_offset': {
                            'pos': 5, 'type': 'Real', 'doc': ''},
                        'axial_length': {
                            'pos': 6, 'type': 'Real', 'doc': ''},
                        'cavity_type': {
                            'pos': 7, 'type': 'Real', 'doc': ''},
                        'file_num': {
                            'pos': 8, 'type': 'Real', 'doc': ''},
                        'sf_field_norm': {
                            'pos': 9, 'type': 'Real', 'doc': ''},
                        'sf_rad_cut': {
                            'pos': 10, 'type': 'Real', 'doc': ''},
                        'sf_axial_disp': {
                            'pos': 11, 'type': 'Real', 'doc': ''},
                        'sf_axial_sym': {
                            'pos': 12, 'type': 'Real', 'doc': ''}}},
        'sec_pill_rec': {
                'desc': 'Variable {frequency gradient} pillbox cavity',
                'doc': '', 'icool_model_name': 12,
                'parms': {
                        'model': {
                            'pos': 1, 'type': 'String', 'doc': ''},
                        'freq': {
                            'pos': 2, 'type': 'Real', 'doc': ''},
                        'grad': {
                            'pos': 3, 'type': 'Real', 'doc': ''},
                        'phase': {
                            'pos': 4, 'type': 'Real', 'doc': ''},
                        'rad_offset': {
                            'pos': 5, 'type': 'Real', 'doc': ''},
                        'width': {
                            'pos': 6, 'type': 'Real', 'doc': ''},
                        'height': {
                            'pos': 7, 'type': 'Real', 'doc': ''}}},
        'open_cell_stand': {
                'desc': 'Open cell standing wave cavity',
                'doc': '',
                'icool_model_name': 13,
                'parms': {
                        'model': {
                            'pos': 1, 'type': 'String', 'doc': ''},
                        'freq': {
                            'pos': 2, 'type': 'Real', 'doc': ''},
                        'grad': {
                            'pos': 3, 'type': 'Real', 'doc': ''},
                        'phase': {
                            'pos': 4, 'type': 'Real', 'doc': ''},
                        'focus_flag': {
                            'pos': 5, 'type': 'Real', 'doc': ''}}}}
    