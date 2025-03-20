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
  "name"                 :  "Website Instamojo Payment Acquirer",
  "summary"              :  """Payment Acquirer: Instamojo Implementation""",
  "category"             :  "Website",
  "version"              :  "1.0.1",
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Website-Instamojo-Payment-Acquirer.html",
  "description"          :  """Instamojo Payment Acquirer
  Instamojo payment gateway supports only INR currency.""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=payment_instamojo_checkout",
  "depends"              :  ['account','payment'],
  "data"                 :  [
                              'views/payment_views.xml',
                              'views/payment_instamojo_templates.xml',
                              'data/payment_acquirer_data.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  99,
  "currency"             :  "USD",
  "pre_init_hook"        :  "pre_init_check",
}
