# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import logging
import unittest

from datetime import datetime, date, timezone, timedelta

from tests.utils import readfile

from formiodata.builder import Builder
from formiodata.form import Form
from formiodata.components.columns import columnsComponent
from formiodata.components.datetime import datetimeComponent
from formiodata.components.email import emailComponent
from formiodata.components.number import numberComponent
from formiodata.components.select import selectComponent
from formiodata.components.textfield import textfieldComponent
from formiodata.components.checkbox import checkboxComponent
from formiodata.components.panel import panelComponent
from formiodata.components.datagrid import datagridComponent
from formiodata.components.editgrid import editgridComponent


class NestedTestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format='\n%(message)s', level=logging.INFO)

    def setUp(self):
        super(NestedTestCase, self).setUp()

        # logging
        # msg = self.id()
        # if self.shortDescription():
        #     msg += ' -- %s' % self.shortDescription()
        # self.logger.info(msg)

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

        self.assertEqual(len(builder.component_ids.keys()), 40)

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

        #######
        # debug
        #######
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

        # components
        self.assertEqual(len(columns.components), 6)
        self.assertEqual(len(builder.components['columns'].components), 6)

        # paths
        self.assertEqual(columns.builder_path_key, ['columns'])
        self.assertEqual(columns.builder_path_label, ['Columns'])
        self.assertEqual(columns.builder_input_path_key, [])
        self.assertEqual(columns.builder_input_path_label, [])

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

        # paths
        self.assertEqual(panel.builder_path_key, ['panel'])
        self.assertEqual(panel.builder_path_label, ['Panel'])
        self.assertEqual(panel.builder_input_path_key, [])
        self.assertEqual(panel.builder_input_path_label, [])

        ##################################
        # (top) columnsComponent: columns1
        ##################################
        # parent: None
        # components: actionType, startDateTime, dataGrid1 (deviceType, measurementTime, temperatureCelsius)

        columns = builder.component_ids['ezrqb3e']

        self.assertIsInstance(columns, columnsComponent)
        self.assertEqual(columns.key, 'columns1')

        # parent
        self.assertIsNone(columns.parent)

        # components

        # print('\n# (top) columnsComponent (columns1)')
        # for key, comp in columns.components.items():
        #     print((comp.id, comp.key, comp))

        self.assertEqual(len(columns.components), 4)
        self.assertEqual(len(builder.components['columns1'].components), 4)

        keys = ['actionType', 'startDateTime', 'dataGrid1', 'editGrid1']
        for key, comp in builder.components['columns1'].components.items():
            self.assertIn(comp.key, keys)

        # paths
        self.assertEqual(columns.builder_path_key, ['columns1'])
        self.assertEqual(columns.builder_path_label, ['Columns'])
        self.assertEqual(columns.builder_input_path_key, [])
        self.assertEqual(columns.builder_input_path_label, [])

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

        # paths
        self.assertEqual(datagrid.builder_path_key, ['dataGrid'])
        self.assertEqual(datagrid.builder_path_label, ['Data Grid'])
        self.assertEqual(datagrid.builder_input_path_key, ['dataGrid'])
        self.assertEqual(datagrid.builder_input_path_label, ['Data Grid'])

        ##########################################
        # datagridComponent: columns1 => dataGrid1
        ##########################################
        # parent: columns1
        # components: columns (which contains: panel, escalate checkbox)

        datagrid = builder.component_ids['ehf11y9']

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
        self.assertEqual(builder.component_ids['ehf11y9'].components['columns'].id, 'ekgpz100')

        # paths
        self.assertEqual(datagrid.builder_path_key, ['columns1', 'dataGrid1'])
        self.assertEqual(datagrid.builder_path_label, ['Columns', 'Data Grid'])
        self.assertEqual(datagrid.builder_input_path_key, ['dataGrid1'])
        self.assertEqual(datagrid.builder_input_path_label, ['Data Grid'])

        ##########################################
        # editgridComponent: columns1 => editGrid1
        ##########################################
        # parent: columns1
        # components: columns (which contains: panel, escalate checkbox)

        editgrid = builder.component_ids['eh7pkpc']

        self.assertIsInstance(editgrid, editgridComponent)
        self.assertEqual(editgrid.key, 'editGrid1')

        # parent
        self.assertIsInstance(editgrid.parent, columnsComponent)
        self.assertEqual(editgrid.parent.key, 'columns1')

        # components

        # print('\n# Component: columns1 => dataGrid')
        # for key, comp in datagrid.components.items():
        #     print((comp.id, comp.key, comp))

        # dataGrid1.components: columns
        self.assertEqual(len(editgrid.components), 1)
        self.assertEqual(editgrid.components['columns'].id, 'e1u0nm')

        # paths
        self.assertEqual(editgrid.builder_path_key, ['columns1', 'editGrid1'])
        self.assertEqual(editgrid.builder_path_label, ['Columns', 'Edit Grid'])
        self.assertEqual(editgrid.builder_input_path_key, ['editGrid1'])
        self.assertEqual(editgrid.builder_input_path_label, ['Edit Grid'])

        #################################################################
        # columnsComponent: columns1 => dataGrid1 => <gridRow> => columns
        #################################################################
        # parent: dataGrid1
        # components: panel, escalate (checkbox)

        columns = builder.component_ids['ekgpz100']

        self.assertIsInstance(columns, columnsComponent)
        self.assertEqual(len(columns.components), 2)

        # parent
        self.assertIsInstance(columns.parent, datagridComponent.gridRow)
        self.assertEqual(columns.parent.grid.key, 'dataGrid1')

        # components
        keys = ['panel', 'escalate']
        for key, comp in columns.components.items():
            self.assertIn(comp.key, keys)

        # paths
        self.assertEqual(columns.builder_path_key, ['columns1', 'dataGrid1', 'columns'])
        self.assertEqual(columns.builder_path_label, ['Columns', 'Data Grid', 'Columns'])
        self.assertEqual(columns.builder_input_path_key, ['dataGrid1'])
        self.assertEqual(columns.builder_input_path_label, ['Data Grid'])

        ########################################################################
        # panelComponent: columns1 => dataGrid1 => <gridRow> => columns => panel
        ########################################################################
        # parent: columns
        # components: columns

        panel = builder.component_ids['eyhv2q']

        self.assertIsInstance(panel, panelComponent)
        self.assertEqual(len(panel.components), 1)

        # parent
        self.assertIsInstance(panel.parent, columnsComponent)
        self.assertEqual(panel.parent.key, 'columns')

        # paths
        self.assertEqual(panel.builder_path_key, ['columns1', 'dataGrid1', 'columns', 'panel'])
        self.assertEqual(panel.builder_path_label, ['Columns', 'Data Grid', 'Columns', 'Panel'])
        self.assertEqual(panel.builder_input_path_key, ['dataGrid1'])
        self.assertEqual(panel.builder_input_path_label, ['Data Grid'])

        ###################################################################################
        # columnsComponent: columns1 => dataGrid1 => <gridRow> columns => panel => columns1
        ###################################################################################
        # parent: panel
        # components: col (select) | col (datetime) | col (number)

        columns = builder.component_ids['es6547h']

        self.assertIsInstance(columns, columnsComponent)
        self.assertEqual(columns.key, 'columns1')

        # parent
        self.assertIsInstance(columns.parent, panelComponent)
        self.assertEqual(columns.parent.key, 'panel')

        # components
        self.assertEqual(len(columns.components), 3)

        keys = ['deviceType', 'measurementTime', 'temperatureCelsius']
        for key, comp in columns.components.items():
            self.assertIn(comp.key, keys)

        for key, comp in columns.components.items():
            # parent
            self.assertIsInstance(comp.parent, columnsComponent)
            self.assertEqual(comp.parent.key, 'columns1')

            if key == 'deviceType':
                self.assertIsInstance(comp, selectComponent)
                self.assertEqual(comp.label, 'Device Type')
                # paths
                self.assertEqual(
                    comp.builder_path_key,
                    ['columns1', 'dataGrid1', 'columns', 'panel', 'columns1', 'deviceType']
                )
                self.assertEqual(
                    comp.builder_path_label,
                    ['Columns', 'Data Grid', 'Columns', 'Panel', 'Columns', 'Device Type']
                )
                self.assertEqual(
                    comp.builder_input_path_key,
                    ['dataGrid1', 'deviceType']
                )
                self.assertEqual(
                    comp.builder_input_path_label,
                    ['Data Grid', 'Device Type']
                )
                # setter
                comp.label = 'Machine Type'
                self.assertEqual(comp.label, 'Machine Type')
            if key == 'measurementTime':
                self.assertIsInstance(comp, datetimeComponent)
                self.assertEqual(comp.label, 'Measurement Time')
                # paths
                self.assertEqual(
                    comp.builder_path_key,
                    ['columns1', 'dataGrid1', 'columns', 'panel', 'columns1', 'measurementTime']
                )
                self.assertEqual(
                    comp.builder_path_label,
                    ['Columns', 'Data Grid', 'Columns', 'Panel', 'Columns', 'Measurement Time']
                )
                self.assertEqual(
                    comp.builder_input_path_key,
                    ['dataGrid1', 'measurementTime']
                )
                self.assertEqual(
                    comp.builder_input_path_label,
                    ['Data Grid', 'Measurement Time']
                )
                # setter
                comp.label = 'Measurement Date / Time'
                self.assertEqual(comp.label, 'Measurement Date / Time')
            if key == 'temperatureCelsius':
                self.assertIsInstance(comp, numberComponent)
                self.assertEqual(comp.label, 'Temperature Celsius')
                # paths
                self.assertEqual(
                    comp.builder_path_key,
                    ['columns1', 'dataGrid1', 'columns', 'panel', 'columns1', 'temperatureCelsius']
                )
                self.assertEqual(
                    comp.builder_path_label,
                    ['Columns', 'Data Grid', 'Columns', 'Panel', 'Columns', 'Temperature Celsius']
                )
                self.assertEqual(
                    comp.builder_input_path_key,
                    ['dataGrid1', 'temperatureCelsius']
                )
                self.assertEqual(
                    comp.builder_input_path_label,
                    ['Data Grid', 'Temperature Celsius']
                )
                # setter
                comp.label = 'Temperature Fahrenheit'
                self.assertEqual(comp.label, 'Temperature Fahrenheit')

        # paths
        self.assertEqual(
            columns.builder_path_key,
            ['columns1', 'dataGrid1', 'columns', 'panel', 'columns1']
        )
        self.assertEqual(
            columns.builder_path_label,
            ['Columns', 'Data Grid', 'Columns', 'Panel', 'Columns']
        )
        self.assertEqual(
            columns.builder_input_path_key,
            ['dataGrid1']
        )
        self.assertEqual(
            columns.builder_input_path_label,
            ['Data Grid']
        )

    def test_Builder_components_count(self):
        builder = Builder(self.builder_json)
        self.assertEqual(len(builder.components), 12)

    def test_Builder_input_components_count(self):
        builder = Builder(self.builder_json)
        # 18 input_components are present in key/val of file: data/test_nesting_form.json
        # (except the submit ie buttonComponent)
        self.assertEqual(len(builder.input_components), 18)

    def test_Form_components_count(self):
        builder = Builder(self.builder_json)
        form = Form(self.form_json, builder)

        self.assertEqual(len(form.components), 12)

    def test_Form_input_components_count(self):
        builder = Builder(self.builder_json)
        form = Form(self.form_json, builder)
        # 18 input_components are present in key/val of file: data/test_nesting_form.json
        # (except the submit ie buttonComponent)
        self.assertEqual(len(form.input_components), 18)

    def test_Form_input_components_not_datagrid(self):
        """ Form: basic (not datagrid) input components """

        builder = Builder(self.builder_json)
        form = Form(self.form_json, builder)

        # firstName in columnsComponent
        firstName = form.input_components['firstName']
        self.assertIsInstance(firstName, textfieldComponent)
        self.assertEqual(firstName.label, 'First Name')
        self.assertEqual(firstName.value, 'Bob')
        self.assertEqual(firstName.type, 'textfield')

        # birthdate in columnsComponent
        birthdate = form.input_components['birthdate']
        self.assertIsInstance(birthdate, datetimeComponent)
        self.assertEqual(birthdate.label, 'Birthdate')
        self.assertEqual(birthdate.value, '1999-12-31')
        self.assertEqual(birthdate.type, 'datetime')
        self.assertIsInstance(birthdate.to_datetime().date(), date)

        # favouriteSeason in panelComponent
        season = form.input_components['favouriteSeason']
        self.assertEqual(season.label, 'Favourite Season')
        self.assertEqual(season.value, 'autumn')
        self.assertEqual(season.value_label, 'Autumn')
        self.assertEqual(season.type, 'select')

    def test_Form_input_components_datagrid_simple(self):
        """ Form: simple datagrid without nested (layout) components """

        builder = Builder(self.builder_json)
        form = Form(self.form_json, builder)

        self.assertIn('dataGrid', builder.input_components.keys())

        datagrid = form.input_components['dataGrid']

        self.assertEqual(len(datagrid.rows), 2)

        emails = ['bob@example.com', 'foo@example.com']
        tz = timezone(timedelta(hours=2))
        registrationDateTimes = [datetime(2021, 4, 5, 12, tzinfo=tz), datetime(2021, 4, 6, 22, tzinfo=tz)]

        for index, row in enumerate(datagrid.rows):
            # component object
            self.assertIsInstance(row.input_components['email'], emailComponent)
            self.assertIsInstance(row.input_components['registrationDateTime'], datetimeComponent)
            # value
            self.assertIn(row.input_components['email'].value, emails)
            self.assertEqual(row.input_components['registrationDateTime'].to_datetime(), registrationDateTimes[index])

    def test_Form_input_components_datagrid_nested(self):
        """ Form: complex datagrid with nested (layout) components """

        builder = Builder(self.builder_json)
        form = Form(self.form_json, builder)

        self.assertIn('dataGrid1', builder.input_components.keys())

        datagrid = form.input_components['dataGrid1']

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
            self.assertIsInstance(row.input_components['deviceType'], selectComponent)
            self.assertIsInstance(row.input_components['measurementTime'], datetimeComponent)
            self.assertIsInstance(row.input_components['temperatureCelsius'], numberComponent)
            self.assertIsInstance(row.input_components['escalate'], checkboxComponent)
            # value
            self.assertIn(row.input_components['deviceType'].value, deviceType)
            self.assertEqual(row.input_components['measurementTime'].to_date(), measurement_date)
            self.assertIn(row.input_components['temperatureCelsius'].value, tempCelcius)
            self.assertIn(row.input_components['escalate'].value, escalate)

    def test_Form_components_simple(self):
        """ Form: simple components """

        builder = Builder(self.builder_json)
        form = Form(self.form_json, builder)

        #################################
        # (top) columnsComponent: columns
        #################################

        columns = form.components['columns']
        self.assertIsInstance(columns, columnsComponent)
        self.assertEqual(columns.key, 'columns')

        # row (only 1 row here)
        row = columns.rows[0]

        # col_1
        col_1 = row[0]
        col_1_keys = ['firstName', 'email', 'birthdate', 'appointmentDateTime']

        # col_1 / keys
        for comp in col_1['components']:
            self.assertIn(comp.key, col_1_keys)

        # col_1 / component objects
        for comp in col_1['components']:
            if comp.key == 'firstName':
                self.assertIsInstance(comp, textfieldComponent)
            elif comp.key == 'email':
                self.assertIsInstance(comp, emailComponent)
            elif comp.key == 'birthdate':
                self.assertIsInstance(comp, datetimeComponent)
            elif comp.key == 'appointmentDateTime':
                self.assertIsInstance(comp, datetimeComponent)

        # col_1 / values
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

        # col_2 / keys
        for comp in col_2['components']:
            self.assertIn(comp.key, col_2_keys)

        # col_2 / values
        for comp in col_2['components']:
            if comp.key == 'lastName':
                self.assertEqual(comp.value, 'Leers')
            elif comp.key == 'phoneNumber':
                self.assertEqual(comp.value, '(069) 999-9999')

    def test_Form_components_row_1_simple(self):
        """ Form: nested components SIMPLE """

        #############################
        # columns1 // row_1 // SIMPLE
        #############################

        builder = Builder(self.builder_json)
        form = Form(self.form_json, builder)

        columns1 = form.components['columns1']
        self.assertIsInstance(columns1, columnsComponent)
        self.assertEqual(columns1.key, 'columns1')
        self.assertEqual(len(columns1.rows), 3)

        # row_1 has 2 columns
        row_1 = columns1.rows[0]

        # row_1: col_1
        row_1_col_1 = row_1[0]

        # keys
        keys = ['actionType']
        for comp in row_1_col_1['components']:
            self.assertIn(comp.key, keys)

        # values
        for comp in row_1_col_1['components']:
            if comp.key == 'actionType':
                self.assertEqual(comp.value, 'check')

        # row_1: col_2
        row_1_col_2 = row_1[1]

        # keys
        keys = ['startDateTime']
        for comp in row_1_col_2['components']:
            self.assertIn(comp.key, keys)

        # values
        for comp in row_1_col_2['components']:
            if comp.key == 'startDateTime':
                self.assertEqual(comp.to_date(), date(2021, 4, 9))

    def test_Form_components_row_1_complex(self):
        """ Form: nested components COMPLEX """

        ##########################################
        # columns1 // row_2 // columns1 // COMPLEX
        ##########################################

        builder = Builder(self.builder_json)
        form = Form(self.form_json, builder)

        columns1 = form.components['columns1']
        self.assertIsInstance(columns1, columnsComponent)
        self.assertEqual(columns1.key, 'columns1')
        self.assertEqual(len(columns1.rows), 3)

        # row_2 has 1 column
        row_2 = columns1.rows[1]
        self.assertEqual(1, len(row_2))
        row_2_col_1 = row_2[0]

        # row_3 also has 1 column
        row_3 = columns1.rows[2]
        self.assertEqual(1, len(row_3))
        row_3_col_1 = row_3[0]

        # keys
        keys = ['dataGrid1', 'editGrid1']
        dataGrid1 = None
        editGrid1 = None
        # NOTE: Why are we iterating?  Might as well pick the value directly...
        for comp in row_2_col_1['components']:
            self.assertIn(comp.key, keys)
            if comp.key == 'dataGrid1':
                dataGrid1 = comp

        for comp in row_3_col_1['components']:
            self.assertIn(comp.key, keys)
            if comp.key == 'editGrid1':
                editGrid1 = comp

        self.assertNotEqual(dataGrid1, editGrid1)
        self.assertIsNotNone(dataGrid1)
        self.assertIsNotNone(editGrid1)

        ###########
        # dataGrid1
        ###########
        self.assertEqual(len(dataGrid1.rows), 3)
        for row in dataGrid1.rows:
            # row has only 1 component
            self.assertEqual(1, len(row.components.keys()))
            comp = row.components['columns']
            self.assertIsInstance(comp, columnsComponent)
            self.assertEqual(comp.key, 'columns')

        # dataGrid1 // row 1
        columns_row = dataGrid1.rows[0]

        # XXX panel.components is OrderedDict()
        columns_in_panel = columns_row.components['columns'].components['panel'].components['columns1']

        # only 1 row
        self.assertEqual(len(columns_in_panel.rows), 1)
        row_columns_in_panel = columns_in_panel.rows[0]

        # keys
        keys = ['deviceType', 'measurementTime', 'temperatureCelsius']
        for comp in row_columns_in_panel[0]['components']:
            self.assertIn(comp.key, keys)

        # component objects
        for comp in row_columns_in_panel[0]['components']:
            if comp.key == 'deviceType':
                self.assertIsInstance(comp, selectComponent)
            elif comp.key == 'measurementTime':
                self.assertIsInstance(comp, datetimeComponent)
            elif comp.key == 'temperatureCelsius':
                self.assertIsInstance(comp, numberComponent)

        # values
        measurementTime = datetime(2021, 4, 9, 9, 00)
        for comp in row_columns_in_panel[0]['components']:
            if comp.key == 'deviceType':
                self.assertEqual(comp.value, 'pumpB')
            elif comp.key == 'measurementTime':
                self.assertEqual(comp.to_datetime(), measurementTime)
            elif comp.key == 'temperatureCelsius':
                self.assertEqual(comp.value, 65)

        # TODO dataGrid1 // row 2
        # dataGrid1_row_2 = dataGrid1.rows[1]

        # TODO dataGrid1 // row 3
        # dataGrid1_row_3 = dataGrid1.rows[2]

        ###########
        # editGrid1
        ###########
        self.assertEqual(len(editGrid1.rows), 3)
        for row in editGrid1.rows:
            # row has only 1 component
            self.assertEqual(1, len(row.components.keys()))
            comp = row.components['columns']
            self.assertIsInstance(comp, columnsComponent)
            self.assertEqual(comp.key, 'columns')

        # editGrid1 // row 1
        columns_row = editGrid1.rows[0]

        # XXX panel.components is OrderedDict()
        columns_in_panel = columns_row.components['columns'].components['panel1'].components['columns3']

        # only 1 row
        self.assertEqual(len(columns_in_panel.rows), 1)
        row_columns_in_panel = columns_in_panel.rows[0]

        # keys
        keys = ['presentColor', 'measurementTime', 'temperatureCelsius']
        for comp in row_columns_in_panel[0]['components']:
            self.assertIn(comp.key, keys)

        # component objects
        for comp in row_columns_in_panel[0]['components']:
            if comp.key == 'presentColor':
                self.assertIsInstance(comp, selectComponent)
            elif comp.key == 'measurementTime':
                self.assertIsInstance(comp, datetimeComponent)
            elif comp.key == 'temperatureCelsius':
                self.assertIsInstance(comp, numberComponent)

        # values
        measurementTime = datetime(2023, 5, 26, 9, 00)
        for comp in row_columns_in_panel[0]['components']:
            if comp.key == 'presentColor':
                self.assertEqual(comp.value, 'yellow')
            elif comp.key == 'measurementTime':
                self.assertEqual(comp.to_datetime(), measurementTime)
            elif comp.key == 'temperatureCelsius':
                self.assertEqual(comp.value, 45)
