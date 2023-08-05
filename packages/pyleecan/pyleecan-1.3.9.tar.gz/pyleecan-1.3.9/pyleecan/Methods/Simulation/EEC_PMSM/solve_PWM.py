import numpy as np

from SciDataTool import DataFreq, Data1D

from ....Functions.Electrical.dqh_transformation_freq import dqh2n_DataFreq


def solve_PWM(self, output, is_dqh_freq=False):
    """Get stator current harmonics due to PWM harmonics
    TODO: validation with transient FEA simulation

    Parameters
    ----------
    self : EEC_PMSM
        an EEC_PMSM object
    output: Output
        An Output object
    is_dqh_freq: bool
        True to consider frequencies in dqh frame

    Returns
    ------
    Is_PWM : DataFreq
        Stator current harmonics as DataFreq
    """
    self.get_logger().info("Calculating PWM current harmonics")

    # Get fundamental frequency
    felec = self.OP.get_felec()

    # Get stator winding phase number
    qs = output.simu.machine.stator.winding.qs

    # Get PWM frequencies in abc frame
    freqs_n = output.elec.Us.axes_df[0].values

    # Get stator voltage harmonics in dqh frame
    Us_PWM = output.elec.get_Us(is_dqh=True, is_harm_only=True, is_freq=True)
    result = Us_PWM.get_along("freqs", "phase")
    Udqh_val = result[Us_PWM.symbol]
    freqs_dqh = result["freqs"]

    # # Plot Us_n and U_dqh
    # output.elec.Us.plot_2D_Data("freqs=[0,2000]", "phase[0]")
    # Us_PWM.plot_2D_Data("freqs=[0,200]", "phase[0]")

    # Filter Udqh_val zeros values
    Udqh_norm = np.linalg.norm(Udqh_val, axis=-1)
    Iamp = Udqh_norm > 1e-6 * Udqh_norm.max()
    freqs_dqh = freqs_dqh[Iamp]
    Udqh_val = Udqh_val[Iamp, :]

    # Init current harmonics matrix
    Idqh_val = np.zeros((freqs_dqh.size, qs), dtype=complex)

    if is_dqh_freq:
        # Take dqh frequency values
        fn_dqh = freqs_dqh
    else:
        # Look for frequency value in n frame for each frequency in dqh frame
        fn_dqh = np.zeros(freqs_dqh.size)
        fn_pos = freqs_dqh + felec
        fn_neg = freqs_dqh - felec
        for ii, (fpos, fneg) in enumerate(zip(fn_pos, fn_neg)):
            fn_ii = None
            jj = 0
            while fn_ii is None and jj < freqs_n.size:
                if (
                    np.abs(fpos - freqs_n[jj]) < 1e-4
                    or np.abs(fneg - freqs_n[jj]) < 1e-4
                ):
                    fn_ii = freqs_n[jj]
                elif (
                    np.abs(fpos + freqs_n[jj]) < 1e-4
                    or np.abs(fneg + freqs_n[jj]) < 1e-4
                ):
                    fn_ii = -freqs_n[jj]
                else:
                    jj += 1
            if fn_ii is None:
                raise Exception("Cannot map dqh frequency back to n frequency")
            else:
                fn_dqh[ii] = fn_ii

        fn_dqh[np.abs(fn_dqh) < felec] = felec

    # Calculate impedances
    we = 0 * 2 * np.pi * felec
    wh = 2 * np.pi * fn_dqh
    a = self.R1 + 1j * wh * self.Ld
    b = -we * self.Lq
    c = we * self.Ld
    d = self.R1 + 1j * wh * self.Lq
    det = a * d - c * b
    # Calculate current harmonics
    # Calculate Id
    Idqh_val[:, 0] = (d * Udqh_val[:, 0] - b * Udqh_val[:, 1]) / det
    # Calculate Iq
    Idqh_val[:, 1] = (-c * Udqh_val[:, 0] + a * Udqh_val[:, 1]) / det
    # if np.any(np.abs(Idqh_val[:, 0]) > 20) or np.any(np.abs(Idqh_val[:, 1]) > 20):
    #     print("problem")

    # # Check
    # Ud = a * Idqh_val[If, 0] + b * Idqh_val[If, 1]
    # Uq = c * Idqh_val[If, 0] + d * Idqh_val[If, 1]
    # check_d = Ud - Udqh_val[If, 0]
    # check_q = Uq - Udqh_val[If, 1]

    # Create frequency axis
    Freqs_PWM = Us_PWM.axes[0]

    norm_freq = dict()
    if Freqs_PWM.normalizations is not None and len(Freqs_PWM.normalizations) > 0:
        for key, val in Freqs_PWM.normalizations.items():
            norm_freq[key] = val.copy()

    Freqs = Data1D(
        name=Freqs_PWM.name,
        symbol=Freqs_PWM.symbol,
        unit=Freqs_PWM.unit,
        values=freqs_dqh,
        normalizations=norm_freq,
    )

    # Create DataFreq in DQH Frame
    Is_PWM_dqh = DataFreq(
        name="Stator current",
        unit="A",
        symbol="I_s",
        axes=[Freqs, Us_PWM.axes[1].copy()],
        values=Idqh_val,
    )

    # # Plot PWM current in dqh frame over frequency
    # Is_PWM_dqh.plot_2D_Data("freqs=[0,20000]", "phase[]")

    # Convert I_dqh spectrum back to stator frame
    Is_PWM_n = dqh2n_DataFreq(
        Is_PWM_dqh,
        n=qs,
        phase_dir=output.elec.phase_dir,
        current_dir=output.elec.current_dir,
        felec=output.elec.OP.felec,
        is_n_rms=False,
    )

    # Reduce current to original voltage frequencies
    Is_PWM_n = Is_PWM_n.get_data_along("freqs=" + str(freqs_n.tolist()), "phase")

    return Is_PWM_n
