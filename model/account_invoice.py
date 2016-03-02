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

from openerp import models, fields, api
# noinspection PyProtectedMember
from openerp.tools.translate import _
import re
import logging

log = logging.getLogger(__name__)


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.one
    @api.depends('number', 'state')
    def _compute_ref_number(self):
        if self.number:
            invoice_number = re.sub(r'\D', '', self.number)
            checksum = sum((7, 3, 1)[idx % 3] * int(val)
                           for idx, val in enumerate(invoice_number[::-1]))
            ref_tmp=invoice_number + str((10 - (checksum % 10)) % 10)
            rf_check=98 - int(ref_tmp+"271500") % 97
            if rf_check < 10:
                self.ref_number = "RF0%s%s" % (rf_check,ref_tmp)
            else:
                self.ref_number = "RF%s%s" % (rf_check,ref_tmp)
            self.invoice_number = invoice_number
        else:
            self.invoice_number = False
            self.ref_number = False

    @api.one
    def _compute_barcode_string(self):
        primary_bank_account = self.partner_bank_id or \
            self.company_id.bank_ids and self.company_id.bank_ids[0]
        if (self.amount_total and primary_bank_account.acc_number
                and self.ref_number and self.date_due):
            amount_total_string = str(self.amount_total)
            if amount_total_string[-2:-1] == '.':
                amount_total_string += '0'
            amount_total_string = amount_total_string.zfill(9)
            receiver_bank_account = re\
                .sub("[^0-9]", "", str(primary_bank_account.acc_number))
            ref = str(self.ref_number)
            ref_check = ref[2:4]
            ref_code = ref[4:]
            ref_number_filled = ref_check + ref_code.zfill(21)
            self.barcode_string = '5' \
                                  + receiver_bank_account \
                                  + amount_total_string[:-3] \
                                  + amount_total_string[-2:] \
                                  + ref_number_filled \
                                  + self.date_due[2:4] \
                                  + self.date_due[5:-3] \
                                  + self.date_due[-2:]
            self.primary_bank_accnum = str(primary_bank_account.acc_number)
        else:
            self.barcode_string = False
            self.primary_bank_accnum = False


    invoice_number = fields.Char(
        'Invoice number',
        compute='_compute_ref_number',
        store=True,
        help=_('Identifier number used to refer to this invoice in '
               'accordance with https://www.fkl.fi/teemasivut/sepa/'
               'tekninen_dokumentaatio/Dokumentit/kotimaisen_viitte'
               'en_rakenneohje.pdf')
    )

    ref_number = fields.Char(
        'Reference Number',
        compute='_compute_ref_number',
        store=True,
        help=_('Invoice RF-reference number in accordance with https://'
               'www.fkl.fi/teemasivut/sepa/tekninen_dokumentaatio/Do'
               'kumentit/kansainvalisen_viitteen_rakenneohje.pdf')
    )

    date_delivered = fields.Date(
        'Date delivered',
        help=_('The date when the invoiced product or service was considered '
               'delivered, for taxation purposes.')
    )

    barcode_string = fields.Char(
        'Barcode String',
        compute='_compute_barcode_string',
        help=_('https://www.fkl.fi/teemasivut/sepa/tekninen_dokumentaatio/Dok'
               'umentit/Pankkiviivakoodi-opas.pdf')
    )

    primary_bank_accnum = fields.Char(
        'Primary bank account number',
        compute='_compute_barcode_string',
        help=_('Primary bank account number')
    )


    @api.multi
    def invoice_print(self):
        """ Print the invoice and mark it as sent, so that we can see more
            easily the next step of the workflow
        """
        assert len(self) == 1, \
            'This option should only be used for a single id at a time.'
        # noinspection PyAttributeOutsideInit
        self.sent = True
        return self.env['report']\
            .get_action(self,
                        'l10n_fi_invoice.report_invoice_finnish_translate')
