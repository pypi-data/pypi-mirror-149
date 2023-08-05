from numpy import zeros

from ....Functions.Electrical.dqh_transformation import n2dqh_DataTime


def get_Phi_dqh_mean(self):
    """Get the mean value of stator flux along dqh axes

    Parameters
    ----------
    self : LUTdq
        a LUTdq object

    Returns
    ----------
    Phi_dqh_mean : ndarray
        mean flux linkage in dqh frame (N_dq, 3)
    """

    if self.Phi_dqh_mean is None:

        N_OP = len(self.output_list)

        Phi_dqh_mean = zeros((N_OP, 3))

        stator_label = self.simu.machine.stator.get_label()

        for ii in range(N_OP):

            if self.output_list[ii].mag.Phi_wind_slice is None:

                Phi_dqh_mean[ii, 0] = self.output_list[ii].elec.eec.Phid
                Phi_dqh_mean[ii, 1] = self.output_list[ii].elec.eec.Phiq

            else:
                # Integrate stator winding flux contained in LUT over z
                Phi_wind = (
                    self.output_list[ii]
                    .mag.Phi_wind_slice[stator_label]
                    .get_data_along("time", "phase", "z=integrate")
                )

                # dqh transform
                Phi_dqh = n2dqh_DataTime(
                    Phi_wind,
                    is_dqh_rms=True,
                    phase_dir=self.get_phase_dir(),
                )
                # mean over time axis
                Phi_dqh_mean[ii, :] = Phi_dqh.get_along("time=mean", "phase")[
                    Phi_dqh.symbol
                ]

        # Store for next call
        self.Phi_dqh_mean = Phi_dqh_mean

    return self.Phi_dqh_mean
