# -*- coding: utf-8 -*-
# File generated according to Generator/ClassesRef/Output/LUTdq.csv
# WARNING! All changes made in this file will be lost!
"""Method code available at https://github.com/Eomys/pyleecan/tree/master/pyleecan/Methods/Output/LUTdq
"""

from os import linesep
from sys import getsizeof
from logging import getLogger
from ._check import set_array, check_var, raise_
from ..Functions.get_logger import get_logger
from ..Functions.save import save
from ..Functions.copy import copy
from ..Functions.load import load_init_dict
from ..Functions.Load.import_class import import_class
from .LUT import LUT

# Import all class method
# Try/catch to remove unnecessary dependencies in unused method
try:
    from ..Methods.Output.LUTdq.get_L_dqh import get_L_dqh
except ImportError as error:
    get_L_dqh = error

try:
    from ..Methods.Output.LUTdq.get_Lm_dqh import get_Lm_dqh
except ImportError as error:
    get_Lm_dqh = error

try:
    from ..Methods.Output.LUTdq.get_Phi_dqh_mean import get_Phi_dqh_mean
except ImportError as error:
    get_Phi_dqh_mean = error

try:
    from ..Methods.Output.LUTdq.get_Phi_dqh_mag import get_Phi_dqh_mag
except ImportError as error:
    get_Phi_dqh_mag = error

try:
    from ..Methods.Output.LUTdq.get_Phi_dqh_mag_mean import get_Phi_dqh_mag_mean
except ImportError as error:
    get_Phi_dqh_mag_mean = error

try:
    from ..Methods.Output.LUTdq.interp_Phi_dqh import interp_Phi_dqh
except ImportError as error:
    interp_Phi_dqh = error

try:
    from ..Methods.Output.LUTdq.interp_Ploss_dqh import interp_Ploss_dqh
except ImportError as error:
    interp_Ploss_dqh = error

try:
    from ..Methods.Output.LUTdq.interp_Tem_rip_dqh import interp_Tem_rip_dqh
except ImportError as error:
    interp_Tem_rip_dqh = error


from numpy import array, array_equal
from ._check import InitUnKnowClassError


class LUTdq(LUT):
    """Look Up Table class for dq OP matrix"""

    VERSION = 1

    # Check ImportError to remove unnecessary dependencies in unused method
    # cf Methods.Output.LUTdq.get_L_dqh
    if isinstance(get_L_dqh, ImportError):
        get_L_dqh = property(
            fget=lambda x: raise_(
                ImportError("Can't use LUTdq method get_L_dqh: " + str(get_L_dqh))
            )
        )
    else:
        get_L_dqh = get_L_dqh
    # cf Methods.Output.LUTdq.get_Lm_dqh
    if isinstance(get_Lm_dqh, ImportError):
        get_Lm_dqh = property(
            fget=lambda x: raise_(
                ImportError("Can't use LUTdq method get_Lm_dqh: " + str(get_Lm_dqh))
            )
        )
    else:
        get_Lm_dqh = get_Lm_dqh
    # cf Methods.Output.LUTdq.get_Phi_dqh_mean
    if isinstance(get_Phi_dqh_mean, ImportError):
        get_Phi_dqh_mean = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use LUTdq method get_Phi_dqh_mean: " + str(get_Phi_dqh_mean)
                )
            )
        )
    else:
        get_Phi_dqh_mean = get_Phi_dqh_mean
    # cf Methods.Output.LUTdq.get_Phi_dqh_mag
    if isinstance(get_Phi_dqh_mag, ImportError):
        get_Phi_dqh_mag = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use LUTdq method get_Phi_dqh_mag: " + str(get_Phi_dqh_mag)
                )
            )
        )
    else:
        get_Phi_dqh_mag = get_Phi_dqh_mag
    # cf Methods.Output.LUTdq.get_Phi_dqh_mag_mean
    if isinstance(get_Phi_dqh_mag_mean, ImportError):
        get_Phi_dqh_mag_mean = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use LUTdq method get_Phi_dqh_mag_mean: "
                    + str(get_Phi_dqh_mag_mean)
                )
            )
        )
    else:
        get_Phi_dqh_mag_mean = get_Phi_dqh_mag_mean
    # cf Methods.Output.LUTdq.interp_Phi_dqh
    if isinstance(interp_Phi_dqh, ImportError):
        interp_Phi_dqh = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use LUTdq method interp_Phi_dqh: " + str(interp_Phi_dqh)
                )
            )
        )
    else:
        interp_Phi_dqh = interp_Phi_dqh
    # cf Methods.Output.LUTdq.interp_Ploss_dqh
    if isinstance(interp_Ploss_dqh, ImportError):
        interp_Ploss_dqh = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use LUTdq method interp_Ploss_dqh: " + str(interp_Ploss_dqh)
                )
            )
        )
    else:
        interp_Ploss_dqh = interp_Ploss_dqh
    # cf Methods.Output.LUTdq.interp_Tem_rip_dqh
    if isinstance(interp_Tem_rip_dqh, ImportError):
        interp_Tem_rip_dqh = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use LUTdq method interp_Tem_rip_dqh: "
                    + str(interp_Tem_rip_dqh)
                )
            )
        )
    else:
        interp_Tem_rip_dqh = interp_Tem_rip_dqh
    # save and copy methods are available in all object
    save = save
    copy = copy
    # get_logger method is available in all object
    get_logger = get_logger

    def __init__(
        self,
        Phi_dqh_mean=None,
        Phi_dqh_mag=None,
        paramexplorer_list=-1,
        output_list=-1,
        xoutput_dict=-1,
        nb_simu=0,
        xoutput_ref=None,
        xoutput_ref_index=None,
        simu=-1,
        path_result="",
        geo=-1,
        elec=-1,
        mag=-1,
        struct=-1,
        post=-1,
        logger_name="Pyleecan.Output",
        force=-1,
        loss=-1,
        init_dict=None,
        init_str=None,
    ):
        """Constructor of the class. Can be use in three ways :
        - __init__ (arg1 = 1, arg3 = 5) every parameters have name and default values
            for pyleecan type, -1 will call the default constructor
        - __init__ (init_dict = d) d must be a dictionary with property names as keys
        - __init__ (init_str = s) s must be a string
        s is the file path to load

        ndarray or list can be given for Vector and Matrix
        object or dict can be given for pyleecan Object"""

        if init_str is not None:  # Load from a file
            init_dict = load_init_dict(init_str)[1]
        if init_dict is not None:  # Initialisation by dict
            assert type(init_dict) is dict
            # Overwrite default value with init_dict content
            if "Phi_dqh_mean" in list(init_dict.keys()):
                Phi_dqh_mean = init_dict["Phi_dqh_mean"]
            if "Phi_dqh_mag" in list(init_dict.keys()):
                Phi_dqh_mag = init_dict["Phi_dqh_mag"]
            if "paramexplorer_list" in list(init_dict.keys()):
                paramexplorer_list = init_dict["paramexplorer_list"]
            if "output_list" in list(init_dict.keys()):
                output_list = init_dict["output_list"]
            if "xoutput_dict" in list(init_dict.keys()):
                xoutput_dict = init_dict["xoutput_dict"]
            if "nb_simu" in list(init_dict.keys()):
                nb_simu = init_dict["nb_simu"]
            if "xoutput_ref" in list(init_dict.keys()):
                xoutput_ref = init_dict["xoutput_ref"]
            if "xoutput_ref_index" in list(init_dict.keys()):
                xoutput_ref_index = init_dict["xoutput_ref_index"]
            if "simu" in list(init_dict.keys()):
                simu = init_dict["simu"]
            if "path_result" in list(init_dict.keys()):
                path_result = init_dict["path_result"]
            if "geo" in list(init_dict.keys()):
                geo = init_dict["geo"]
            if "elec" in list(init_dict.keys()):
                elec = init_dict["elec"]
            if "mag" in list(init_dict.keys()):
                mag = init_dict["mag"]
            if "struct" in list(init_dict.keys()):
                struct = init_dict["struct"]
            if "post" in list(init_dict.keys()):
                post = init_dict["post"]
            if "logger_name" in list(init_dict.keys()):
                logger_name = init_dict["logger_name"]
            if "force" in list(init_dict.keys()):
                force = init_dict["force"]
            if "loss" in list(init_dict.keys()):
                loss = init_dict["loss"]
        # Set the properties (value check and convertion are done in setter)
        self.Phi_dqh_mean = Phi_dqh_mean
        self.Phi_dqh_mag = Phi_dqh_mag
        # Call LUT init
        super(LUTdq, self).__init__(
            paramexplorer_list=paramexplorer_list,
            output_list=output_list,
            xoutput_dict=xoutput_dict,
            nb_simu=nb_simu,
            xoutput_ref=xoutput_ref,
            xoutput_ref_index=xoutput_ref_index,
            simu=simu,
            path_result=path_result,
            geo=geo,
            elec=elec,
            mag=mag,
            struct=struct,
            post=post,
            logger_name=logger_name,
            force=force,
            loss=loss,
        )
        # The class is frozen (in LUT init), for now it's impossible to
        # add new properties

    def __str__(self):
        """Convert this object in a readeable string (for print)"""

        LUTdq_str = ""
        # Get the properties inherited from LUT
        LUTdq_str += super(LUTdq, self).__str__()
        LUTdq_str += (
            "Phi_dqh_mean = "
            + linesep
            + str(self.Phi_dqh_mean).replace(linesep, linesep + "\t")
            + linesep
            + linesep
        )
        LUTdq_str += "Phi_dqh_mag = " + str(self.Phi_dqh_mag) + linesep + linesep
        return LUTdq_str

    def __eq__(self, other):
        """Compare two objects (skip parent)"""

        if type(other) != type(self):
            return False

        # Check the properties inherited from LUT
        if not super(LUTdq, self).__eq__(other):
            return False
        if not array_equal(other.Phi_dqh_mean, self.Phi_dqh_mean):
            return False
        if other.Phi_dqh_mag != self.Phi_dqh_mag:
            return False
        return True

    def compare(self, other, name="self", ignore_list=None):
        """Compare two objects and return list of differences"""

        if ignore_list is None:
            ignore_list = list()
        if type(other) != type(self):
            return ["type(" + name + ")"]
        diff_list = list()

        # Check the properties inherited from LUT
        diff_list.extend(super(LUTdq, self).compare(other, name=name))
        if not array_equal(other.Phi_dqh_mean, self.Phi_dqh_mean):
            diff_list.append(name + ".Phi_dqh_mean")
        if (other.Phi_dqh_mag is None and self.Phi_dqh_mag is not None) or (
            other.Phi_dqh_mag is not None and self.Phi_dqh_mag is None
        ):
            diff_list.append(name + ".Phi_dqh_mag None mismatch")
        elif self.Phi_dqh_mag is not None:
            diff_list.extend(
                self.Phi_dqh_mag.compare(other.Phi_dqh_mag, name=name + ".Phi_dqh_mag")
            )
        # Filter ignore differences
        diff_list = list(filter(lambda x: x not in ignore_list, diff_list))
        return diff_list

    def __sizeof__(self):
        """Return the size in memory of the object (including all subobject)"""

        S = 0  # Full size of the object

        # Get size of the properties inherited from LUT
        S += super(LUTdq, self).__sizeof__()
        S += getsizeof(self.Phi_dqh_mean)
        S += getsizeof(self.Phi_dqh_mag)
        return S

    def as_dict(self, type_handle_ndarray=0, keep_function=False, **kwargs):
        """
        Convert this object in a json serializable dict (can be use in __init__).
        type_handle_ndarray: int
            How to handle ndarray (0: tolist, 1: copy, 2: nothing)
        keep_function : bool
            True to keep the function object, else return str
        Optional keyword input parameter is for internal use only
        and may prevent json serializability.
        """

        # Get the properties inherited from LUT
        LUTdq_dict = super(LUTdq, self).as_dict(
            type_handle_ndarray=type_handle_ndarray,
            keep_function=keep_function,
            **kwargs
        )
        if self.Phi_dqh_mean is None:
            LUTdq_dict["Phi_dqh_mean"] = None
        else:
            if type_handle_ndarray == 0:
                LUTdq_dict["Phi_dqh_mean"] = self.Phi_dqh_mean.tolist()
            elif type_handle_ndarray == 1:
                LUTdq_dict["Phi_dqh_mean"] = self.Phi_dqh_mean.copy()
            elif type_handle_ndarray == 2:
                LUTdq_dict["Phi_dqh_mean"] = self.Phi_dqh_mean
            else:
                raise Exception(
                    "Unknown type_handle_ndarray: " + str(type_handle_ndarray)
                )
        if self.Phi_dqh_mag is None:
            LUTdq_dict["Phi_dqh_mag"] = None
        else:
            LUTdq_dict["Phi_dqh_mag"] = self.Phi_dqh_mag.as_dict(
                type_handle_ndarray=type_handle_ndarray,
                keep_function=keep_function,
                **kwargs
            )
        # The class name is added to the dict for deserialisation purpose
        # Overwrite the mother class name
        LUTdq_dict["__class__"] = "LUTdq"
        return LUTdq_dict

    def _set_None(self):
        """Set all the properties to None (except pyleecan object)"""

        self.Phi_dqh_mean = None
        self.Phi_dqh_mag = None
        # Set to None the properties inherited from LUT
        super(LUTdq, self)._set_None()

    def _get_Phi_dqh_mean(self):
        """getter of Phi_dqh_mean"""
        return self._Phi_dqh_mean

    def _set_Phi_dqh_mean(self, value):
        """setter of Phi_dqh_mean"""
        if type(value) is int and value == -1:
            value = array([])
        elif type(value) is list:
            try:
                value = array(value)
            except:
                pass
        check_var("Phi_dqh_mean", value, "ndarray")
        self._Phi_dqh_mean = value

    Phi_dqh_mean = property(
        fget=_get_Phi_dqh_mean,
        fset=_set_Phi_dqh_mean,
        doc=u"""RMS stator winding flux table in dqh frame (including magnets and currents given by I_dqh)

        :Type: ndarray
        """,
    )

    def _get_Phi_dqh_mag(self):
        """getter of Phi_dqh_mag"""
        return self._Phi_dqh_mag

    def _set_Phi_dqh_mag(self, value):
        """setter of Phi_dqh_mag"""
        if isinstance(value, str):  # Load from file
            try:
                value = load_init_dict(value)[1]
            except Exception as e:
                self.get_logger().error(
                    "Error while loading " + value + ", setting None instead"
                )
                value = None
        if isinstance(value, dict) and "__class__" in value:
            class_obj = import_class(
                "SciDataTool.Classes", value.get("__class__"), "Phi_dqh_mag"
            )
            value = class_obj(init_dict=value)
        elif type(value) is int and value == -1:  # Default constructor
            value = DataND()
        check_var("Phi_dqh_mag", value, "DataND")
        self._Phi_dqh_mag = value

    Phi_dqh_mag = property(
        fget=_get_Phi_dqh_mag,
        fset=_set_Phi_dqh_mag,
        doc=u"""RMS stator winding flux linkage spectrum in dqh frame including harmonics (only magnets)

        :Type: SciDataTool.Classes.DataND.DataND
        """,
    )
