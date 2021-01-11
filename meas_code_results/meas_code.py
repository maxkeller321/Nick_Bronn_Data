# coding=utf-8
from pi3diamond import pi3d
import numpy as np
import os
import sys
import UserScripts.helpers.sequence_creation_helpers as sch; reload(sch)
import UserScripts.helpers.shared as shared; reload(shared)
import multi_channel_awg_seq as MCAS; reload(MCAS)
import UserScripts.helpers.snippets_awg as sna; reload(sna)
import UserScripts.helpers.shared as ush;reload(ush)
from qutip_enhanced import *
import AWG_M8190A_Elements as E
sys.path.append("D:\Python\pi3diamond\pym8190a")
import pym8190a
import operations as op; reload(op)

from collections import OrderedDict
# import necessary modules

seq_name = os.path.basename(__file__).split('.')[0]
nuclear = sch.create_nuclear(__file__)
with open(os.path.abspath(__file__).split('.')[0] + ".py", 'r') as f:
    meas_code = f.read()

__TAU_HALF__ = 2*192/12e3

ael = 1.0


def ret_ret_mcas(pdc):
    def ret_mcas(current_iterator_df):
        mcas = MCAS.MultiChSeq(seq_name=seq_name, ch_dict={'2g': [1, 2], '128m': [1, 2]})
        for idx, _I_ in current_iterator_df.iterrows():

            """
            Initialisation part 
            """


            if _I_['rotating_qubit'] == '14n': 
                state_init = '+'
            elif _I_['rotating_qubit'] == '13c414': 
                state_init = 'n+'
            elif _I_['rotating_qubit'] == '13c90': 
                state_init = 'nn+'


            if _I_['polarize']:
                op.initialise_nuclear_spin_register(mcas, state_init)

                op.readout_nuclear_spin_state(mcas, state_init, ssr_repetitions=450, step_idx=0)

                op.initialise_with_green(mcas)
                op.initialise_with_red(mcas)
                freq = pi3d.tt.mfl({'14N': [+1]}, ms_trans='0')
                sna.ssr(mcas, frequencies=freq, wait_dur=0.0, robust=False, nuc='charge_state', mixer_deg=-90, step_idx=1, laser_dur=800.0)


            """
            Algorithm part 
            """



            if _I_['rotating_qubit'] == '14n': 
                op.rx_nitrogen(mcas, np.pi)
                state_result = '0'
            elif _I_['rotating_qubit'] == '13c414': 
                op.electron_pi_pulse(mcas)
                state_result = 'n-'
                op.rx_carbon_414(mcas, np.pi, ms=-1)
            elif _I_['rotating_qubit'] == '13c90': 
                op.electron_pi_pulse(mcas)
                op.rx_carbon_90(mcas, np.pi, ms=-1)
                state_result = 'nn-'


            """
            Readout
            """

            op.readout_nuclear_spin_state(mcas, state_result, step_idx=2)
            #mcas.asc(length_mus=2000, name='wait')  # wait for spin resets

            pi3d.gated_counter.set_n_values(mcas)  ## storing time trace data from gated counter

        return mcas
    return ret_mcas


def settings(pdc={}):
    ana_seq=[
        ['init', '<', 0, 0, 10, 2],
        ['init', '<', 0, 0, 10, 1],
        ['result', '<', 0, 0, 10, 2]
    ]
    sch.settings(
        nuclear=nuclear,
        ret_mcas=ret_ret_mcas(pdc),
        analyze_sequence=ana_seq,
        pdc=pdc,
        meas_code=meas_code
    )

    nuclear.x_axis_title = 'tau_half [mus]'
    nuclear.analyze_type = 'standard'


    pi3d.gated_counter.trace.analyze_type = 'standard'
    pi3d.gated_counter.trace.consecutive_valid_result_numbers = [0]
    pi3d.gated_counter.trace.average_results = True

    nuclear.parameters = OrderedDict(
        (
            ('polarize', [True]),
            ('sweeps', range(20)),
            ('rotating_qubit', ['14n', '13c414', '13c90']),
        )
    )
    nuclear.number_of_simultaneous_measurements = 1#len(nuclear.parameters['phase_pi2_2'])

def run_fun(abort, **kwargs):
    pi3d.readout_duration = 150e6
    nuclear.debug_mode = False
    settings()
    nuclear.run(abort)
