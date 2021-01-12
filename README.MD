# Package description

## Folders: 
* system_screenshots
    *  Screenshots of all our user interfaces
        * Gated_counter: SSR (Single Shot Readout) data analysis (Left: Timetrace (Counts per interval), Right: Histograms)  
        * Transition_tracker: Current frequency shifts relative to the base RF frequency in [MHz] to obtain the transition frequency between two nuclear spin levels dependent on a certain electron spin state. 
        * ... 
* ssr_MW_wavefiles
    * All used Wavefiles in the readout of 13c414.
        * n+ file contains the data for a Robust MW electron pi which is selective on mn = +1/2 of 13c414
        * n- file contains the data for a Robust MW electron pi which is selective on mn = -1/2 of 13c414
* AWG_sequence_info
    * Nearly full sequence description 
* AWG_commands_during_runtime
    * Command list that we send to our Master and Slave AWG (Triggering, Removing sequences, Configs (Function mode)) 
* meas_code_results
    * Measurement code (meas_code.py)
    * Results in data.hdf (Use for opening maybe: pandas 0.24.2 version)
    * analyze_rotation_with_postselection.ipynb corresponding analysis script
    

## Wavefile column description: 
    First column: time [mus]
    Second column: Amplitude 
    Third column: Phase [rad]

## Informations regarding Wavefiles and our AWG: 
* A full Wavefile is written into one AWG Wavestep (length, amplitude, phase, frequency). The exact MW/ RF frequency for the AWG is provided by internal code 
* Multiple Wavesteps form a Segment 
    * Can be seen in /AWG_SEQUENCE_INFO/awg_printinfo.txt (e.g. Segment name: init_13c414, one Wavestep name: polarize)
* Multiple Segments form a Sequence
    * Can be seen in /AWG_SEQUENCE_INFO/awg_printinfo.txt (Sequence name: rx_pi_all_nuclear_spins8841.9200001)

## Information regarding the measurement script & data analysis: 
### Measurement:

* Initialization:
    * Initialize a certain nuclear spin Nitrogen (14n), Carbon 1 (13c414) or Carbon 2 (13c90) through the electron spin (SWAP)
    * Single Shot Readout for later data post-selection (450 SSR repetitions)
    * Electron spin initialization (ms = 0) (red laser light)
    * Charge state initialization (Green laser light)
    * Charge state measurement for post-selection (Orange laser light, 800 mus)
* Algorithm: 
    * Nuclear pi pulse on initialized nuclear spin (RF pulse (See transition tracker for frequency))
        * To distinguish 13c90 and 13c414 we flip the electron spin before into ms=-1
* Readout: 
    * Single Shot Readout on flipped state

### analysis
* Maybe pandas 0.24.2 and Python 2.7 is needed 
* For SSR information check https://www.researchgate.net/publication/44902077_Single-Shot_Readout_of_a_Single_Nuclear_Spin
