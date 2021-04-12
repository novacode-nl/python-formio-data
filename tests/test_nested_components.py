# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import json
import logging
import unittest

from datetime import datetime, date

from tests.utils import readfile
from formiodata.builder import Builder
from formiodata.form import Form, FormRenderer
from formiodata.components import columnsComponent, datetimeComponent, numberComponent, selectComponent, \
    textfieldComponent, panelComponent, datagridComponent


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


    def test_builder_component_ids(self):
        """ Builder: component_ids (Dict) for direct mapping """

        builder = Builder(self.builder_json)

        for c in builder.component_ids.items():
            comp = c[1]
            if comp.parent:
                print((comp.id, comp.key, comp.type, comp.parent, comp.parent.id))
            else:
                print((comp.id, comp.key, comp.type))
        self.assertEqual(len(builder.component_ids.keys()), 32)

    def test_builder_components(self):
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

        for key, comp in builder.components.items():
            print((comp.id, comp.key, comp.type, comp.parent))
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

        print('\n# Top component: columns')
        for comp in columns.components:
            print((comp))

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

        # components
        print('\n# Top component: panel')
        for comp in panel.components:
            print((comp))

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
        print('\n# Top component: columns1')
        for comp in columns.components:
            print((comp))

        self.assertEqual(len(columns.components), 3)
        self.assertEqual(len(builder.components['columns1'].components), 3)

        keys = ['actionType', 'startDateTime', 'dataGrid1']
        for key, comp in builder.components['columns1'].components.items():
            self.assertIn(comp.key, keys)

        ##################################
        # (top) datagridComponent: dataGrid
        ##################################
        # parent: None
        # components: name, email

        datagrid = builder.component_ids['ecw3wx']

        self.assertIsInstance(datagrid, datagridComponent)
        self.assertEqual(datagrid.key, 'dataGrid')

        # parent
        self.assertIsNone(columns.parent)

        # components
        print('\n# Top component: datagrid')
        for comp in columns.components:
            print((comp))

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
        print('\n# Component: columns1 => dataGrid')
        for comp in datagrid.components:
            print((comp))

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
        print('\n# Component: columns1 => dataGrid1 => columns')
        for comp in columns.components:
            print((comp))

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
        print('\n# Component: columns1 => dataGrid1 => columns => panel')
        for key, comp in panel.components.items():
            print((key, comp.id))

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

        print('\n# Component: columns1 => dataGrid1 => columns => panel => columns1')
        for key, comp in columns.components.items():
            print((key, comp.id))

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

    def test_builder_form_components(self):
        """ Builder: form_components should have the same structure as the Form (submission) JSON """

        builder = Builder(self.builder_json)

        print('\n# Builder.form_components')
        for key, comp in builder.form_components.items():
            if comp.parent:
                print((comp.id, comp.key, comp.type, comp.parent, comp.parent.id))
            else:
                print((comp.id, comp.key, comp.type))            

        # TODO FIX
        # datagrid (child) components shouldn't be present
        # 
        # Those 17 form_components are present in key/val of file: data/test_nesting_form.json
        # (except the submit ie buttonComponent)
        self.assertEqual(len(builder.form_components), 17)

    def test_form_not_datagrid(self):
        """ Form: basic (not datagrid) input components """

        builder = Builder(self.builder_json)
        form = Form(self.form_json, builder)

        print('\n# Form.form_components')
        for key, comp in form.components.items():
            if comp.parent:
                print((comp.id, comp.key, comp.type, comp.parent, comp.parent.id))
            else:
                print((comp.id, comp.key, comp.type))

        self.assertEqual(len(form.components), 17)

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

    def test_form_datagrid_simple(self):
        """ Form: simple datagrid without (deep) nested components """

        builder = Builder(self.builder_json)

        self.assertIn('dataGrid', builder.form_components.keys())

        form = Form(self.form_json, builder)

    def test_form_datagrid_nested_components(self):
        """ Form: complex datagrid with (deep) nested components """

        builder = Builder(self.builder_json)

        self.assertIn('dataGrid1', builder.form_components.keys())

        form = Form(self.form_json, builder)

    def test_form_renderer(self):
        """ FormRenderer: same structure has Builder and grid(s) properties with loaded data """

        # Absolutely test all nested components here !

        builder = Builder(self.builder_json)
        form = Form(self.form_json, builder)
        renderer = form.render()
        
        self.assertIsInstance(renderer, FormRenderer)
        self.assertEqual(len(renderer.components), 12)
        
        # FormRenderer
        ##############
        # - The components (types) are the same as Builder.
        # - Has data (value) set on input compoonents
        # - Has additional properties for layout components, eg columnComponent with rows (property).
        self.assertEqual(len(renderer.components), len(builder.components.keys()))
