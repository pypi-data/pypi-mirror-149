#
# Copyright (c) 2020-2021 eGauge Systems LLC
#       1644 Conestoga St, Suite 2
#       Boulder, CO 80301
#       voice: 720-545-9767
#       email: davidm@egauge.net
#
# All rights reserved.
#
# MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
from PySide2.QtWidgets import QMessageBox, QWidget

import egauge.ctid as ctid

def invalid_double(string):
    try:
        float(string)
    except ValueError:
        return True
    return False

class Sensor_Params:
    def __init__(self, ui, parent, title='Sensor Parameters'):
        self.parent = parent
        self.ui = ui
        self.widget = QWidget(parent)
        self.widget.setVisible(False)
        self.ui.setupUi(self.widget)
        self.title = title

    def activate(self):
        '''Display our set of sensor parameters.'''
        self.widget.setVisible(True)
        self.parent.setTitle(self.title)

    def deactivate(self):
        '''Hide our set of sensor parameters.'''
        self.widget.setVisible(False)
        self.parent.setTitle('Sensor Parameters')

    def set_input_enabled(self, enabled):
        '''Enable or disable inputs.'''

    def load(self, template):
        '''Load sensor parameters from a template.'''

    def save(self, template):
        '''Save sensor parameters in the template dictionary, without
        validation.

        '''

    def validate(self, template):
        '''Validate the parameter values in the template.  If there are any
        errors, focus on the input element with the erroneous value
        and return False, otherwise return True.

        '''
        return True

    def encoder_argv(self, template):
        '''Convert the parameter values to the argument list required for the
        CTid-encoder program.'''
        return []

    def table_to_template(self, table, template):
        '''Extract sensor parameters from table and add them to the template.'''

class CT(Sensor_Params):
    def set_input_enabled(self, enabled):
        self.ui.current_spinbox.setEnabled(enabled)
        self.ui.size_spinbox.setEnabled(enabled)
        self.ui.output_voltage_spinbox.setEnabled(enabled)
        self.ui.bias_voltage_spinbox.setEnabled(enabled)
        self.ui.phase_spinbox.setEnabled(enabled)
        self.ui.voltage_temp_coeff_spinbox.setEnabled(enabled)
        self.ui.phase_temp_coeff_spinbox.setEnabled(enabled)
        for row in range(4):
            v_cal = self.ui.__dict__['calv%d' % (row + 1)]
            p_cal = self.ui.__dict__['calp%d' % (row + 1)]
            v_cal.setEnabled(enabled)
            p_cal.setEnabled(enabled)

    def load(self, template):
        self.ui.current_spinbox.setValue(template['current'])
        self.ui.size_spinbox.setValue(template['size'])
        self.ui.output_voltage_spinbox.setValue(template['v_output'])
        self.ui.bias_voltage_spinbox.setValue(template['v_bias'])
        self.ui.phase_spinbox.setValue(template['phi'])
        self.ui.voltage_temp_coeff_spinbox.setValue(template['v_temp_coeff'])
        self.ui.phase_temp_coeff_spinbox.setValue(template['phi_temp_coeff'])

        cal_table = template['cal_table']
        for row in range(4):
            levels = ['1.5', '5', '15', '50']
            v_cal = self.ui.__dict__['calv%d' % (row + 1)]
            p_cal = self.ui.__dict__['calp%d' % (row + 1)]
            if levels[row] not in cal_table:
                v_cal.setValue(0.0)
                p_cal.setValue(0.0)
                continue
            adj = cal_table[levels[row]]
            v_cal.setValue(adj[0])
            p_cal.setValue(adj[1])

    def save(self, template):
        template['current'] = self.ui.current_spinbox.value()
        template['size'] = self.ui.size_spinbox.value()
        template['v_output'] = self.ui.output_voltage_spinbox.value()
        template['v_bias'] = self.ui.bias_voltage_spinbox.value()
        template['phi'] = self.ui.phase_spinbox.value()
        template['v_temp_coeff'] = self.ui.voltage_temp_coeff_spinbox.value()
        template['phi_temp_coeff'] = self.ui.phase_temp_coeff_spinbox.value()
        cal_table = {}
        for row in range(4):
            levels = ['1.5', '5', '15', '50']
            v_cal = self.ui.__dict__['calv%d' % (row + 1)].value()
            p_cal = self.ui.__dict__['calp%d' % (row + 1)].value()
            if v_cal == 0.0 and p_cal == 0.0:
                continue
            cal_table[levels[row]] = (v_cal, p_cal)
        template['cal_table'] = cal_table

    def encoder_argv(self, template):
        argv = ['-s', '%.1f' % template['size'],
                '-c', '%.1f' % template['current'],
                '-v', '%.5f' % template['v_output'],
                '-b', '%.6f' % (1e-3 * template['v_bias']),
                '-p', '%.2f' % template['phi'],
                '-t', '%d' % template['v_temp_coeff'],
                '-T', '%.1f' % template['phi_temp_coeff']]
        for lvl, adj in template['cal_table'].items():
            argv += ['-a', '%s:%.3f/%.3f' % (lvl, adj[0], adj[1])]
        return argv

    def table_to_template(self, table, template):
        template['current'] = table.rated_current
        template['size'] = table.size
        template['v_output'] = table.voltage_at_rated_current
        template['v_bias'] = 1e3 * table.bias_voltage
        template['phi'] = table.phase_at_rated_current
        template['v_temp_coeff'] = table.voltage_temp_coeff
        template['phi_temp_coeff'] = table.phase_temp_coeff
        cal_table = {}
        for row in range(4):
            levels = [1.5, 5, 15, 50]
            v_cal = table.cal_table[levels[row]][0]
            p_cal = table.cal_table[levels[row]][1]
            if v_cal == 0.0 and p_cal == 0.0:
                continue
            cal_table[str(levels[row])] = (v_cal, p_cal)
        template['cal_table'] = cal_table

class Linear(Sensor_Params):
    def __init__(self, ui, parent, title):
        super().__init__(ui, parent, title)
        max_float = 3.4028235e38
        self.ui.scale_spinbox.setRange(-max_float, max_float)
        self.ui.offset_spinbox.setRange(-max_float, max_float)
        for _, unit_desc in ctid.SENSOR_UNITS:
            self.ui.unit_comboBox.addItem(unit_desc)
        self.ui.unit_comboBox.currentIndexChanged.connect(self._unit_changed)

    def _unit_changed(self):
        unit_code = self.ui.unit_comboBox.currentIndex()
        unit = ctid.get_sensor_unit(unit_code)
        if unit == '':
            scale_unit = ' 1/V'
            offset_unit = ''
        else:
            scale_unit = ' %s/V' % unit
            offset_unit = ' %s' % unit
        self.ui.scale_spinbox.setSuffix(scale_unit)
        self.ui.offset_spinbox.setSuffix(offset_unit)

    def set_input_enabled(self, enabled):
        self.ui.unit_comboBox.setEnabled(enabled)
        self.ui.scale_spinbox.setEnabled(enabled)
        self.ui.offset_spinbox.setEnabled(enabled)
        self.ui.delay_spinbox.setEnabled(enabled)

    def load(self, template):
        self.ui.unit_comboBox.setCurrentIndex(template['unit'])
        self.ui.scale_spinbox.setValue(template['scale'])
        self.ui.offset_spinbox.setValue(template['offset'])
        self.ui.delay_spinbox.setValue(template['delay'])

    def save(self, template):
        template['unit'] = self.ui.unit_comboBox.currentIndex()
        template['scale'] = self.ui.scale_spinbox.value()
        template['offset'] = self.ui.offset_spinbox.value()
        template['delay'] = self.ui.delay_spinbox.value()

    def encoder_argv(self, template):
        return ['--unit', str(template['unit']),
                '--scale', str(template['scale']),
                '--offset', str(template['offset']),
                '--delay', str(template['delay'])]

    def table_to_template(self, table, template):
        template['unit'] = table.sensor_unit
        template['scale'] = table.scale
        template['offset'] = table.offset
        template['delay'] = table.delay

class Temp(Sensor_Params):
    def set_input_enabled(self, enabled):
        self.ui.scale_spinbox.setEnabled(enabled)
        self.ui.offset_spinbox.setEnabled(enabled)

    def load(self, template):
        self.ui.scale_spinbox.setValue(template['scale'])
        self.ui.offset_spinbox.setValue(template['offset'])

    def save(self, template):
        template['scale'] = self.ui.scale_spinbox.value()
        template['offset'] = self.ui.offset_spinbox.value()

    def encoder_argv(self, template):
        # convert from °C/V to °C/V:
        return ['--scale', str(template['scale']),
                '--offset', str(template['offset'])]

    def table_to_template(self, table, template):
        template['scale'] = table.scale
        template['offset'] = table.offset

class NTC(Sensor_Params):
    '''Note that the NTC parameters are line editors rather than spinboxes
    because their value can be any double value, including some really
    tiny values that are best entered via exponent notation.  The QT4
    double spinbox is not well setup for such values.

    '''

    def set_input_enabled(self, enabled):
        self.ui.ntc_a_lineEdit.setEnabled(enabled)
        self.ui.ntc_b_lineEdit.setEnabled(enabled)
        self.ui.ntc_c_lineEdit.setEnabled(enabled)
        self.ui.ntc_m_lineEdit.setEnabled(enabled)
        self.ui.ntc_n_lineEdit.setEnabled(enabled)
        self.ui.ntc_k_lineEdit.setEnabled(enabled)

    def load(self, template):
        self.ui.ntc_a_lineEdit.setText(template['ntc_a'])
        self.ui.ntc_b_lineEdit.setText(template['ntc_b'])
        self.ui.ntc_c_lineEdit.setText(template['ntc_c'])
        self.ui.ntc_m_lineEdit.setText(template['ntc_m'])
        self.ui.ntc_n_lineEdit.setText(template['ntc_n'])
        self.ui.ntc_k_lineEdit.setText(template['ntc_k'])

    def save(self, template):
        template['ntc_a'] = self.ui.ntc_a_lineEdit.text()
        template['ntc_b'] = self.ui.ntc_b_lineEdit.text()
        template['ntc_c'] = self.ui.ntc_c_lineEdit.text()
        template['ntc_m'] = self.ui.ntc_m_lineEdit.text()
        template['ntc_n'] = self.ui.ntc_n_lineEdit.text()
        template['ntc_k'] = self.ui.ntc_k_lineEdit.text()

    def validate(self, template):
        bad_field = None
        if invalid_double(template['ntc_a']):
            bad_field = self.ui.ntc_a_lineEdit
        elif invalid_double(template['ntc_b']):
            bad_field = self.ui.ntc_b_lineEdit
        elif invalid_double(template['ntc_c']):
            bad_field = self.ui.ntc_d_lineEdit
        elif invalid_double(template['ntc_m']):
            bad_field = self.ui.ntc_m_lineEdit
        elif invalid_double(template['ntc_n']):
            bad_field = self.ui.ntc_r1_lineEdit
        elif invalid_double(template['ntc_k']):
            bad_field = self.ui.ntc_r1_lineEdit

        if bad_field is not None:
            QMessageBox.warning(self, 'Invalid number',
                                'Please enter a value number.',
                                QMessageBox.Ok)
            bad_field.setFocus()
            return False

        return True

    def encoder_argv(self, template):
        return ['--ntc-a', str(template['ntc_a']),
                '--ntc-b', str(template['ntc_b']),
                '--ntc-c', str(template['ntc_c']),
                '--ntc-m', str(template['ntc_m']),
                '--ntc-n', str(template['ntc_n']),
                '--ntc-k', str(template['ntc_k'])]

    def table_to_template(self, table, template):
        template['ntc_a'] = str(table.ntc_a)
        template['ntc_b'] = str(table.ntc_b)
        template['ntc_c'] = str(table.ntc_c)
        template['ntc_m'] = str(table.ntc_m)
        template['ntc_n'] = str(table.ntc_n)
        template['ntc_k'] = str(table.ntc_k)

class Pulse(Sensor_Params):
    '''Note that the NTC parameters are line editors rather than spinboxes
    because their value can be any double value, including some really
    tiny values that are best entered via exponent notation.  The QT4
    double spinbox is not well setup for such values.

    '''

    def set_input_enabled(self, enabled):
        self.ui.threshold_spinbox.setEnabled(enabled)
        self.ui.hysteresis_spinbox.setEnabled(enabled)
        self.ui.debounce_spinbox.setEnabled(enabled)
        self.ui.edge_comboBox.setEnabled(enabled)

    def load(self, template):
        self.ui.threshold_spinbox.setValue(template['threshold'])
        self.ui.hysteresis_spinbox.setValue(template['hysteresis'])
        self.ui.debounce_spinbox.setValue(template['debounce_time'])
        idx = 0		# default to 'rising edge'
        edge = template['edge_mask']
        if edge == 'falling':
            idx = 1
        elif edge == 'both':
            idx = 2
        self.ui.edge_comboBox.setCurrentIndex(idx)

    def save(self, template):
        mask = ['rising', 'falling', 'both']
        template['threshold'] = self.ui.threshold_spinbox.value()
        template['hysteresis'] = self.ui.hysteresis_spinbox.value()
        template['debounce_time'] = self.ui.debounce_spinbox.value()
        template['edge_mask'] = mask[self.ui.edge_comboBox.currentIndex()]

    def encoder_argv(self, template):
        return ['--threshold', str(1e-3 * template['threshold']),
                '--hysteresis', str(1e-3 * template['hysteresis']),
                '--debounce-time', str(template['debounce_time']),
                '--edge-mask', template['edge_mask']]

    def table_to_template(self, table, template):
        mask = ['none', 'rising', 'falling', 'both']
        template['threshold'] = 1e3 * table.threshold
        template['hysteresis'] = 1e3 * table.hysteresis
        template['debounce_time'] = table.debounce_time
        template['edge_mask'] = mask[table.edge_mask]
