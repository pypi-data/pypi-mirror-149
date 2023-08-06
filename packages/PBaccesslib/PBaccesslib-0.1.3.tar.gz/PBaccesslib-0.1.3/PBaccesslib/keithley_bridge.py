from K2600acceslib.kth_integration import K2600Probecard


class KBridge:
    """"""
    def __init__(self, keithley_adress):
        self._inst = K2600Probecard(keithley_adress, verbose=True)

    def clear_inst(self):
        """"""
        self._inst.clear_reset()
        
    def set_values(self, a_l, b_l, rnge, level):
        """"""
        self._inst.set_values(a_l, b_l, rnge, level)
        
    def read_compare(self, avdd_v_c, avdd_c_c, vdd_v_c, vdd_c):
        """"""
        bin_array, test_output = self._inst.read_compare(avdd_v_c, avdd_c_c, vdd_v_c, vdd_c)
        return bin_array, test_output

    def set_2v5_on(self):
        """"""
        self._inst.set_k_out_on()

    def set_2v5_off(self):
        """"""
        self._inst.set_k_out_off()

    def close_connection(self):
        """"""
        self._inst.close_connection()
        
    def return_instrument(self):
        """"""
        return self._inst
        
        

