from odoo import api, fields, models, Command,exceptions,_


class DocumentFolder(models.Model):
    _inherit = 'documents.document'

    course_id = fields.Many2one('slide.channel', compute='_compute_course_id', search='_search_course_id',
                                 export_string_translation=False)
    # task_id = fields.Many2one('project.task', compute='_compute_task_id', search='_search_task_id',
    #                           export_string_translation=False)
    # for folders
    course_ids = fields.One2many('slide.channel', 'documents_folder_id', string="Course")


    def _prepare_create_values(self, vals_list):
        vals_list = super()._prepare_create_values(vals_list)
        folder_ids = {folder_id for v in vals_list if (folder_id := v.get('folder_id')) and not v.get('res_id')}
        folder_id_values = {
            folder_id: self.browse(folder_id)._get_link_to_project_values()
            for folder_id in folder_ids
        }
        for vals in vals_list:
            if (folder_id := vals.get('folder_id')) and vals.get('type') != 'folder' and not vals.get('res_id'):
                vals.update(folder_id_values[folder_id])
        return vals_list

    def _add_missing_default_values(self, values):
        values = super()._add_missing_default_values(values)
        if self.env.context.get('apg_elearning') and not values.get('folder_id'):
            access_internal = values['access_internal'] or (
                'edit' if self.env.context.get('privacy_visibility') != 'followers' else 'none')
            values['folder_id'] = self.env.ref('apg_elearning.document_course_folder').id
            values['access_internal'] = access_internal
            values["children_ids"] = [Command.create({
                "access_internal": access_internal,
                "name": f'{values.get("name")} - {_("Shared")}',
                "type": 'folder',
            })]
        return values

    def _get_link_to_project_values(self):
        # print("_get_link_to_project_values",self._get_link_to_project_values())
        self.ensure_one()
        values = {}
        if course := self._get_project_from_closest_ancestor():
            if self.type == 'folder' and not self.shortcut_document_id:
                values.update({
                    'res_model': 'slide.channel',
                    'res_id': course.id,
                })
                if course.partner_id and not self.partner_id.id:
                    values['partner_id'] = course.partner_id.id
        return values

    def _get_project_from_closest_ancestor(self):
        # print("_get_project_from_closest_ancestor",self._get_project_from_closest_ancestor())
        """
        If the current folder is linked to exactly one project, this method returns
        that project.

        If the current folder doesn't match the criteria, but one of its ancestors
        does, this method will return the project linked to the closest ancestor
        matching the criteria.

        :return: The project linked to the closest valid ancestor, or an empty
        recordset if no project is found.
        """
        self.ensure_one()
        eligible_course = self.env['slide.channel'].sudo()._read_group(
            [('documents_folder_id', 'parent_of', self.id)],
            ['documents_folder_id'],
            having=[('__count', '=', 1)],
        )
        if not eligible_course:
            return self.env['slide.channel']

        # dict {folder_id: position}, where position is a value used to sort projects by their folder_id
        folder_id_order = {int(folder_id): i for i, folder_id in enumerate(reversed(self.parent_path[:-1].split('/')))}
        eligible_course.sort(key=lambda project_group: folder_id_order[project_group[0].id])
        return self.env['slide.channel'].sudo().search(
            [('documents_folder_id', '=', eligible_course[0][0].id)], limit=1).sudo(False)

    def unlink(self):
        print("Inside unlink method of documents.document")
        for document in self:
            # Check if the document is linked to a course (slide.channel)
            if document.res_model == 'slide.channel' and document.res_id:
                # Get the related course (slide.channel) record
                course = self.env['slide.channel'].browse(document.res_id)
                if course:
                    # Find the promotional material in the One2many field
                    promotional_material = course.promotional_material_ids.filtered(
                        lambda material: material.promotional_attachment_name == document.name
                    )
                    # Delete the promotional material entry if found
                    if promotional_material:
                        print(f"Deleting promotional material: {promotional_material}")
                        promotional_material.unlink()
        # Proceed with the deletion of the document
        return super(DocumentFolder, self).unlink()
