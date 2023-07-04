# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import pprint
import requests
import json

from odoo.http import Controller, request, route

_logger = logging.getLogger(__name__)

# TODO
# auth should be public or something else for create invoice?

class CustomController(Controller):
    _return_url = '/payment/btcpay/return'
    _create_invoice = '/payment/btcpay/createInvoice'

    @route(_return_url, type='http', auth='public', methods=['GET','POST'], csrf=False)
    def custom_process_transaction(self, **post):
        _logger.info("Handling custom processing with data:\n%s", pprint.pformat(post))
        _logger.info("Self :\n%s", pprint.pformat(post))
        _logger.info("Requet :\n%s", pprint.pformat(request))
        _logger.info("Requet :\n%s", pprint.pformat(request.env))
#        request.env['payment.transaction'].sudo()._handle_notification_data('btcpay', post)
        return request.redirect('/payment/status')


    @route(_create_invoice, type='http', auth='public', methods=['POST'], csrf=False)
    def create_invoice(self, **post):
        _logger.info("Inside create_invoice")
        _logger.info(post)
    
        btcpay_details = request.env['payment.provider'].search([('code', '=', 'btcpay')])
        base_url = btcpay_details.mapped('btcpay_server_url')[0]
        store_id = btcpay_details.mapped('btcpay_store_id')[0]
        api_key = btcpay_details.mapped('btcpay_api_key')[0]
    
        _logger.info("btcpay details")
        _logger.info(base_url + store_id + api_key)
    
        server_url = f"{base_url}/api/v1/stores/{store_id}/invoices"
        headers = {
            "Authorization": f"Token {api_key}",
            "Content-Type": "application/json"
        }
    
        checkout = {
            "redirectURL": f"http://localhost:8069/payment/btcpay/return?ref={post['ref']}",
            "paymentMethods": ["BTC-LightningNetwork"]
        }
    
        payload = {
            "amount": post['amount'],
            "checkout": checkout,
            "currency": post['currency']
        }
    
        _logger.info("request payload")
        _logger.info(json.dumps(payload))
        _logger.info(base_url)
    
        apiRes = requests.post(server_url, data=json.dumps(payload), headers=headers)
        _logger.info(f"calling the url now {base_url}/i/{apiRes.json()['id']}")
        return request.redirect(f"{base_url}/i/{apiRes.json()['id']}",local=False)
