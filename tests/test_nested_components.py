# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import json
import logging
import unittest

from datetime import datetime, date

from tests.utils import readfile
from formiodata.builder import Builder
from formiodata.form import Form, FormRenderer
from formiodata.components import columnsComponent, datetimeComponent, emailComponent, numberComponent, \
    selectComponent, textfieldComponent, panelComponent, datagridComponent


class NestedTestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format='\n%(message)s', level=logging.INFO)

    def setUp(self):
        super(NestedTestCase, self).setUp()

        # logging
        msg = self.id()
        if self.shortDescription():
            msg += ' -- %s' % self.shortDescription()
        self.logger.info(msg)

        self.builder_json = readfile('data', 'test_nested_components_builder.json')
        self.form_json = readfile('data', 'test_nested_components_form.json')


    def test_Builder_component_ids(self):
        """ Builder: component_ids (Dict) for direct mapping """

        builder = Builder(self.builder_json)

        # for key, comp in builder.component_ids.items():
        #     if comp.parent:
        #         print((comp.id, comp.key, comp.type, comp.parent, comp.parent.id))
        #     else:
        #         print((comp.id, comp.key, comp))

        self.assertEqual(len(builder.component_ids.keys()), 32)

    def test_Builder_components(self):
        """ Builder: components (OrderedDict) hierarchy, from toplevel and traverse
        nested components """

        """
        Top level components:
        - columns
        - content
        - radio
        - panel
        - survey
        - datagrid
        - html
        - columns (deep nested components)
        - signature
        - file (storage; Base64)
        - file (storage: Url)
        - button (submit)
        """

        builder = Builder(self.builder_json)

        ## debug
        # for key, comp in builder.components.items():
        #     print((comp.id, comp.key, comp.type, comp.parent))

        self.assertEqual(len(builder.components.keys()), 12)

        #################################
        # (top) columnsComponent: columns
        #################################
        # parent: None
        # components: firstName, lastName etc

        columns = builder.component_ids['ez2p9i']

        self.assertIsInstance(columns, columnsComponent)
        self.assertEqual(columns.key, 'columns')
        self.assertIsNone(columns.parent)

        # print('\n# (top) columnsComponent')
        # for key, comp in columns.components.items():
        #     print((comp.id, comp.key, comp))

        self.assertEqual(len(columns.components), 6)
        self.assertEqual(len(builder.components['columns'].components), 6)

        #############################
        # (top) panelComponent: panel
        #############################
        # parent: None
        # components: favouriteSeason, favouriteFood

        panel = builder.component_ids['em39da']

        self.assertIsInstance(panel, panelComponent)
        self.assertEqual(panel.key, 'panel')

        # parent
        self.assertIsNone(panel.parent)

        # print('\n# (top) panelsComponent')
        # for key, comp in panel.components.items():
        #     print((comp.id, comp.key, comp))

        # components
        self.assertEqual(len(panel.components), 2)
        self.assertEqual(len(builder.components['panel'].components), 2)

        ##################################
        # (top) columnsComponent: columns1
        ##################################
        # parent: None
        # components: actionType, startDateTime, dataGrid1 (deviceType, measurementTime, temperatureCelsius)

        columns = builder.component_ids['ejghurn']

        self.assertIsInstance(columns, columnsComponent)
        self.assertEqual(columns.key, 'columns1')

        # parent
        self.assertIsNone(columns.parent)

        # components

        # print('\n# (top) columnsComponent (columns1)')
        # for key, comp in columns.components.items():
        #     print((comp.id, comp.key, comp))

        self.assertEqual(len(columns.components), 3)
        self.assertEqual(len(builder.components['columns1'].components), 3)

        keys = ['actionType', 'startDateTime', 'dataGrid1']
        for key, comp in builder.components['columns1'].components.items():
            self.assertIn(comp.key, keys)

        ###################################
        # (top) datagridComponent: dataGrid
        ###################################
        # parent: None
        # components: name, email

        datagrid = builder.component_ids['ecw3wx']

        self.assertIsInstance(datagrid, datagridComponent)
        self.assertEqual(datagrid.key, 'dataGrid')

        # parent
        self.assertIsNone(columns.parent)

        # components

        # print('\n# (top) datagridComponent')
        # for key, comp in columns.components.items():
        #     print((comp.id, comp.key, comp))

        self.assertEqual(len(datagrid.components), 2)
        self.assertEqual(len(builder.components['dataGrid'].components), 2)

        keys = ['email', 'registrationDateTime']
        for key, comp in builder.components['dataGrid'].components.items():
            self.assertIn(comp.key, keys)

        ##########################################
        # datagridComponent: columns1 => dataGrid1
        ##########################################
        # parent: columns1
        # components: columns (which contains: panel, escalate checkbox)

        datagrid = builder.component_ids['eea699r']

        self.assertIsInstance(datagrid, datagridComponent)
        self.assertEqual(datagrid.key, 'dataGrid1')

        # parent
        self.assertIsInstance(datagrid.parent, columnsComponent)
        self.assertEqual(datagrid.parent.key, 'columns1')

        # components

        # print('\n# Component: columns1 => dataGrid')
        # for key, comp in datagrid.components.items():
        #     print((comp.id, comp.key, comp))

        # dataGrid1.components: columns
        self.assertEqual(len(datagrid.components), 1)
        self.assertEqual(builder.component_ids['eea699r'].components['columns'].id, 'eleoxql00')

        ####################################################
        # columnsComponent: columns1 => dataGrid1 => columns
        ####################################################
        # parent: dataGrid1
        # components: panel, escalate (checkbox)

        columns = builder.component_ids['eleoxql00']

        self.assertIsInstance(columns, columnsComponent)
        self.assertEqual(len(columns.components), 2)

        # parent
        self.assertIsInstance(columns.parent, datagridComponent)
        self.assertEqual(columns.parent.key, 'dataGrid1')

        # components

        # print('\n# Component: columns1 => dataGrid1 => columns')
        # for key, comp in columns.components.items():
        #     print((comp.id, comp.key, comp))

        keys = ['panel', 'escalate']
        for key, comp in columns.components.items():
            self.assertIn(comp.key, keys)

        ###########################################################
        # panelComponent: columns1 => dataGrid1 => columns => panel
        ###########################################################
        # parent: columns
        # components: columns

        panel = builder.component_ids['ek5p7n6'] 

        self.assertIsInstance(panel, panelComponent)
        self.assertEqual(len(panel.components), 1)

        # parent
        self.assertIsInstance(panel.parent, columnsComponent)
        self.assertEqual(panel.parent.key, 'columns')

        # components

        # print('\n# Component: columns1 => dataGrid1 => columns => panel')
        # for key, comp in panel.components.items():
        #     print((comp.id, comp.key, comp))

        #########################################################################
        # columnsComponent: columns1 => dataGrid1 => columns => panel => columns1
        #########################################################################
        # parent: panel
        # components: col (select) | col (datetime) | col (number)

        columns = builder.component_ids['ep08ekn']

        self.assertIsInstance(columns, columnsComponent)
        self.assertEqual(columns.key, 'columns1')

        # parent
        self.assertIsInstance(columns.parent, panelComponent)
        self.assertEqual(columns.parent.key, 'panel')

        # components
        self.assertEqual(len(columns.components), 3)

        # print('\n# Component: columns1 => dataGrid1 => columns => panel => columns1')
        # for key, comp in columns.components.items():
        #     print((comp.id, comp.key, comp))

        keys = ['deviceType', 'measurementTime', 'temperatureCelsius']
        for key, comp in builder.component_ids['ep08ekn'].components.items():
            self.assertIn(comp.key, keys)

        for key, comp in columns.components.items():
            # parent
            self.assertIsInstance(comp.parent, columnsComponent)
            self.assertEqual(comp.parent.key, 'columns1')

            if key == 'deviceType':
                self.assertIsInstance(comp, selectComponent)
                self.assertEqual(comp.label, 'Device Type')
                # setter
                comp.label = 'Machine Type'
                self.assertEqual(comp.label, 'Machine Type')
            if key == 'measurementTime':
                self.assertIsInstance(comp, datetimeComponent)
                self.assertEqual(comp.label, 'Measurement Time')
                # setter
                comp.label = 'Measurement Date / Time'
                self.assertEqual(comp.label, 'Measurement Date / Time')
            if key == 'temperatureCelsius':
                self.assertIsInstance(comp, numberComponent)
                self.assertEqual(comp.label, 'Temperature Celsius')
                # setter
                comp.label = 'Temperature Fahrenheit'
                self.assertEqual(comp.label, 'Temperature Fahrenheit')

    def test_Builder_form_components(self):
        """ Builder: form_components should have the same structure as the Form (submission) JSON """

        builder = Builder(self.builder_json)

        # print('\n# Builder.form_components')
        # for key, comp in builder.form_components.items():
        #     if comp.parent:
        #         print((comp.id, comp.key, comp.type, comp.parent, comp.parent.id))
        #     else:
        #         print((comp.id, comp.key, comp.type))

        # Those 17 form_components are present in key/val of file: data/test_nesting_form.json
        # (except the submit ie buttonComponent)
        self.assertEqual(len(builder.form_components), 17)

    def test_Form_components(self):
        """ Form: components structure """

        builder = Builder(self.builder_json)
        form = Form(self.form_json, builder)

        # print('\n# Form.form_components')
        # for key, comp in form.components.items():
        #     if comp.parent:
        #         print((comp.id, comp.key, comp.type, comp.parent, comp.parent.id))
        #     else:
        #         print((comp.id, comp.key, comp.type))

        self.assertEqual(len(form.components), 17)

    def test_Form_not_datagrid(self):
        """ Form: basic (not datagrid) input components """

        builder = Builder(self.builder_json)
        form = Form(self.form_json, builder)

        # firstName in columnsComponent
        firstName = form.components['firstName']
        self.assertIsInstance(firstName, textfieldComponent)
        self.assertEqual(firstName.label, 'First Name')
        self.assertEqual(firstName.value, 'Bob')
        self.assertEqual(firstName.type, 'textfield')

        # birthdate in columnsComponent
        birthdate = form.components['birthdate']
        self.assertIsInstance(birthdate, datetimeComponent)
        self.assertEqual(birthdate.label, 'Birthdate')
        self.assertEqual(birthdate.value, '1999-12-31')
        self.assertEqual(birthdate.type, 'datetime')
        self.assertIsInstance(birthdate.to_datetime().date(), date)

        # favouriteSeason in panelComponent
        season = form.components['favouriteSeason']
        self.assertEqual(season.label, 'Favourite Season')
        self.assertEqual(season.value, 'autumn')
        self.assertEqual(season.value_label, 'Autumn')        
        self.assertEqual(season.type, 'select')

    def test_Form_datagrid_simple(self):
        """ Form: simple datagrid without (deep) nested components """

        builder = Builder(self.builder_json)
        form = Form(self.form_json, builder)

        self.assertIn('dataGrid', builder.form_components.keys())

        datagrid = form.components['dataGrid']

        self.assertEqual(len(datagrid.rows), 2)

        email = ['bob@example.com', 'foo@example.com']
        for row in datagrid.rows:
            # component object
            self.assertIsInstance(row['email'], emailComponent)
            self.assertIsInstance(row['registrationDateTime'], datetimeComponent)
            # value
            self.assertIn(row['email'].value, emails)

    def test_Form_datagrid_nested_components(self):
        """ Form: complex datagrid with (deep) nested components """

        builder = Builder(self.builder_json)
        form = Form(self.form_json, builder)

        self.assertIn('dataGrid1', builder.form_components.keys())

        datagrid = form.components['dataGrid1']

        self.assertEqual(len(datagrid.rows), 3)

        # components
        deviceType = ['pumpB', 'pumpA', 'pumpC']
        tempCelcius = [65, 78, 55]
        escalate = [False, True]
        measurement_date = date(2021, 4, 9)

        for row in datagrid.rows:
            # TODO in Form components the datagrid.rows should only
            # have input components (not layout)

            # component object
            self.assertIsInstance(row['deviceType'], selectComponent)
            self.assertIsInstance(row['measurementTime'], datetimeComponent)
            self.assertIsInstance(row['temperatureCelsius'], integerComponent)
            self.assertIsInstance(row['escalate'], checkboxComponent)
            # value
            self.assertIn(row['deviceType'].value, deviceType)
            self.assertEqual(row['measurementTime'].to_date(), measurement_date)
            self.assertIn(row['temperatureCelsius'].value, tempCelcius)
            self.assertIn(row['escalate'].value, tempCelcius)

    def test_FormRenderer_as_Builder(self):
        """ FormRenderer: same structure as Builder """

        builder = Builder(self.builder_json)
        form = Form(self.form_json, builder)
        renderer = form.render()
        
        self.assertIsInstance(renderer, FormRenderer)

        # FormRenderer has same compoonents structure as Builder
        self.assertEqual(len(renderer.components), 12)
        builder_components = sorted(builder.components.keys())
        renderer_components = sorted(renderer.components.keys())
        self.assertEqual(renderer_components, builder_components)

    def test_FormRenderer_simple_components(self):
        """ FormRenderer: simple components """

        builder = Builder(self.builder_json)
        form = Form(self.form_json, builder)
        renderer = form.render()

        #################################
        # (top) columnsComponent: columns
        #################################
        
        columns = renderer.components['columns']
        self.assertIsInstance(columns, columnsComponent)
        self.assertEqual(columns.key, 'columns')

        # row (only 1 row here)
        row = columns.rows[0]

        # col_1
        col_1 = row[0]
        col_1_keys = ['firstName', 'email', 'birthdate', 'appointmentDateTime']

        ## keys
        for comp in col_1['components']:
            self.assertIn(comp.key, col_1_keys)

        ## component objects
        for comp in col_1['components']:
            if comp.key == 'firstName':
                self.assertIsInstance(comp, textfieldComponent)
            elif comp.key == 'email':
                self.assertIsInstance(comp, emailComponent)
            elif comp.key == 'birthdate':
                self.assertIsInstance(comp, datetimeComponent)
            elif comp.key == 'appointmentDateTime':
                self.assertIsInstance(comp, datetimeComponent)

        ## values
        for comp in col_1['components']:
            if comp.key == 'firstName':
                self.assertEqual(comp.value, 'Bob')
            elif comp.key == 'email':
                self.assertEqual(comp.value, 'bob@novacode.nl')
            elif comp.key == 'birthdate':
                self.assertEqual(comp.to_date(), date(1999, 12, 31))
            elif comp.key == 'appointmentDateTime':
                self.assertEqual(comp.to_date(), date(2021, 2, 26))

        # col_2
        col_2 = row[1]
        col_2_keys = ['lastName', 'phoneNumber']

        ## keys
        for comp in col_2['components']:
            self.assertIn(comp.key, col_2_keys)

        ## values
        for comp in col_2['components']:
            if comp.key == 'lastName':
                self.assertEqual(comp.value, 'Leers')
            elif comp.key == 'phoneNumber':
                self.assertEqual(comp.value, '(069) 999-9999')

    def test_FormRenderer_nested_components_row_1_simple(self):
        """ FormRenderer: nested components SIMPLE """

        #############################
        # columns1 // row_1 // SIMPLE
        #############################

        builder = Builder(self.builder_json)
        form = Form(self.form_json, builder)
        renderer = form.render()

        columns1 = renderer.components['columns1']
        self.assertIsInstance(columns1, columnsComponent)
        self.assertEqual(columns1.key, 'columns1')
        self.assertEqual(len(columns1.rows), 2)

        # row_1 has 2 columns
        row_1 = columns1.rows[0]

        # row_1: col_1
        row_1_col_1 = row_1[0]

        ## keys
        keys = ['actionType']
        for comp in row_1_col_1['components']:
            self.assertIn(comp.key, keys)

        ## values
        # for comp in col_1['components']:
        #     if comp.key == 'actionType':
        #         self.assertEqual(comp.value, 'check')

        # row_1: col_2
        row_1_col_2 = row_1[1]

        ## keys
        keys = ['startDateTime']
        for comp in row_1_col_2['components']:
            self.assertIn(comp.key, keys)

        ## values
        # for comp in row_1_col_2['components']:
        #     if comp.key == 'startDateTime':
        #         self.assertEqual(comp.to_date(), date(2021, 4, 9))

    def test_FormRenderer_nested_components_row_1_complex(self):
        """ FormRenderer: nested components COMPLEX """

        ##########################################
        # columns1 // row_2 // columns1 // COMPLEX
        ##########################################

        builder = Builder(self.builder_json)
        form = Form(self.form_json, builder)
        renderer = form.render()

        columns1 = renderer.components['columns1']
        self.assertIsInstance(columns1, columnsComponent)
        self.assertEqual(columns1.key, 'columns1')
        self.assertEqual(len(columns1.rows), 2)

        # row_2 has 1 column
        row_2 = columns1.rows[1]
        row_2_col_1 = row_2[0]

        ## keys
        keys = ['dataGrid1']
        dataGrid1 = None
        for comp in row_2_col_1['components']:
            self.assertIn(comp.key, keys)

            if comp.key == 'dataGrid1':
                dataGrid1 = comp

        # dataGrid1
        self.assertEqual(len(dataGrid1.rows), 3)
        for row in dataGrid1.rows:
            # row has only 1 component
            comp = row[0]
            self.assertIsInstance(comp, columnsComponent)
            self.assertIsEqual(comp.key, 'columns')

        ## dataGrid1 // row 1
        dataGrid1_row_1 = dataGrid1.rows[0]
        row_1_panel = dataGrid1_row_1[0]
        row_1_escalate_checkbox = dataGrid1_row_1[1]

        # XXX panel.components is OrderedDict()
        columns_in_panel = row_1_panel.components['panel']

        # only 1 row
        self.assertEqual(len(columns_in_panel.rows), 1)
        row_columns_in_panel_ = columns_in_panel.rows[0]

        ## keys
        keys = ['deviceType', 'measurementTime', 'temperatureCelsius']
        for comp in row_columns_in_panel['components']:
            self.assertIn(comp.key, keys)

        ## component objects
        for comp in row_columns_in_panel['components']:
            if comp.key == 'deviceType':
                self.assertIsInstance(comp, selectComponent)
            elif comp.key == 'measurementTime':
                self.assertIsInstance(comp, datetimeComponent)
            elif comp.key == 'temperatureCelsius':
                self.assertIsInstance(comp, integerComponent)

        ## values
        measurementTime = datetime(2021, 4, 9, 9, 00)
        for comp in col_1['components']:
            if comp.key == 'deviceType':
                self.assertEqual(comp.value, 'pumpB')
            elif comp.key == 'measurementTime':
                self.assertEqual(comp.to_datetime(), measurementTime)
            elif comp.key == 'temperatureCelsius':
                self.assertEqual(comp.value, 65)

        ## TODO dataGrid1 // row 2
        # dataGrid1_row_2 = dataGrid1.rows[1]

        ## TODO dataGrid1 // row 3
        # dataGrid1_row_3 = dataGrid1.rows[2]
