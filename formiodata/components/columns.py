# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from .layout_base import layoutComponentBase


class columnsComponent(layoutComponentBase):

    def load_data(self, data, is_form=False):
        for column in self.raw['columns']:
            for component in column['components']:
                # Only determine and load class if component type.
                if 'type' in component:
                    component_obj = self.builder.get_component_object(component)
                    component_obj.load(
                        self.child_component_owner,
                        parent=self,
                        data=data,
                        all_data=self._all_data,
                        is_form=is_form,
                    )

    @property
    def rows(self):
        rows = []

        row = []
        col_data = {'column': None, 'components': []}
        total_width = 0

        for col in self.raw['columns']:
            components = []

            for col_comp in col['components']:
                for key, comp in self.components.items():
                    if col_comp['id'] == comp.id:
                        components.append(comp)

            if col['width'] >= 12:
                # add previous (loop) row
                if row:
                    rows.append(row)

                # init new row and add to rows
                row = [{'column': col, 'components': components}]
                rows.append(row)

                # init next loop (new row and total_width)
                row = []
                total_width = 0
            elif total_width >= 12:
                # add previous (loop) row
                rows.append(row)
                row = []
                # init new row for next loop
                col_data = {'column': col, 'components': components}
                row.append(col_data)
                total_width = col['width']
            else:
                if not row:
                    row = [{'column': col, 'components': components}]
                else:
                    col_data = {'column': col, 'components': components}
                    row.append(col_data)
                total_width += col['width']
        if row:
            # add last generated row
            rows.append(row)
        return rows

    def render(self):
        html_rows = []
        for row in self.rows:
            html_cells = []
            for col in row:
                for component in col['components']:
                    if component.is_visible:
                        component.render()
                    else:
                        component.html_component = ''
                    html_cells.append('<td>'+component.html_component+'</td>')

            html_rows.append('<tr>'+(''.join(html_cells))+'</tr>')

        self.html_component = '<table>'+(''.join(html_rows))+'</table>'
