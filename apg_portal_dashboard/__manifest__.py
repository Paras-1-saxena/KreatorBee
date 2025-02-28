# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
  "name"                 :  "APG Website Portal Dashboard",
  "summary"              :  """Dashboard For Website.""",
  "category"             :  "Website",
  "version"              :  "1.0.1",
  "sequence"             :  1,
  "author"               :  "Apagen solutions",
  "license"              :  "",
  "website"              :  "https://www.apagen.com",
  "description"          :  """https://www.apagen.com""",
  "live_test_url"        :  "",
  "depends"              :  ['base', 'web', 'website', 'portal'],
  "data"                 :  [
                                'views/courses_template.xml',
                                'views/dashboard_template.xml',
                                # 'views/my_portal_template.xml',
                                'views/signup_templates.xml',
                            ],
    "images"               :  ['static/description/Banner.png'],
    "application"          :  True,
    "installable"          :  True,
    "auto_install"         :  False,
    'assets':{
        'web.assets_frontend':[
        'apg_portal_dashboard/static/src/js/sidebar_menu.js',
        'apg_portal_dashboard/static/src/scss/side_bar.css',
        'apg_portal_dashboard/static/src/scss/signup.css',
    ],
  },
}
