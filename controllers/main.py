# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import pprint

from odoo.http import Controller, request, route

_logger = logging.getLogger(__name__)


class CustomController(Controller):
    _return_url = '/payment/btcpay/return'

    @route(_return_url, type='http', auth='public', methods=['GET','POST'], csrf=False)
    def custom_process_transaction(self, **post):
        _logger.info("Handling custom processing with data:\n%s", pprint.pformat(post))
        _logger.info("Self :\n%s", pprint.pformat(self))
        _logger.info("Self :\n%s", pprint.pformat(self.invoice))
#        request.env['payment.transaction'].sudo()._handle_notification_data('btcpay', post)
        return request.redirect('/payment/status')
