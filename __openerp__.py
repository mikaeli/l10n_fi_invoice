# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Avoin.Systems
#    Copyright 2015 Avoin.Systems
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

# noinspection PyStatementEffect
{
    "name": "Finnish Invoice (RF-version)",
    "version": "0.3.1",
    "license": "AGPL-3",
    "author": "Avoin.Systems",
    "category": "Localization",
    "website": "http://avoin.systems",
    "images": ["static/description/icon.png"],
    "depends": [
        'base',
        'account',
        'report',
        'email_template'
    ],
    "description": """
Finnish Invoice
===============
Make invoice reports look like Finnish standard invoices.
""",
    "data": [
        'data/common.xml',
        'report/report_layout.xml',
        'report/report_layout_header.xml',
        'report/report_layout_footer.xml',
        'report/report_invoice.xml',
        'view/account_invoice.xml'
    ],
    "summary": "Suomalainen laskupohja",
    "active": False,
    "installable": True,
    "auto_install": False,
    "application": False
}
