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


    def btcpayApiCall(self,payload,api,method):
        btcpay_details = request.env['payment.provider'].search([('code', '=', 'btcpay')])
        base_url = btcpay_details.mapped('btcpay_server_url')[0]
        store_id = btcpay_details.mapped('btcpay_store_id')[0]
        api_key = btcpay_details.mapped('btcpay_api_key')[0]
        server_url = f"{base_url}{api.format(store_id=store_id)}"

        headers = {
            "Authorization": f"Token {api_key}",
            "Content-Type": "application/json"
        }

        _logger.info(f"value of server_url is {server_url} and method is {method}")

        if method == "GET":
            apiRes=requests.get(server_url,headers=headers)
        elif method == "POST":
            apiRes = requests.post(server_url, data=json.dumps(payload), headers=headers)

        return apiRes

    @route(_return_url, type='http', auth='public', methods=['GET','POST'], csrf=False)
    def custom_process_transaction(self, **post):
        _logger.info("Handling custom processing with data:\n%s", pprint.pformat(post))
        _logger.info("Self :\n%s", pprint.pformat(post))
        _logger.info("Requet :\n%s", pprint.pformat(request))
        _logger.info("Requet :\n%s", pprint.pformat(request.env))
#        request.env['payment.transaction'].sudo()._handle_notification_data('btcpay', post)
        trn = request.env['payment.transaction'].search([('reference', '=', post['ref']), ('provider_code', '=', 'btcpay')])
        apiRes=self.btcpayApiCall({},'/api/v1/stores/{store_id}/invoices?textsearch='+post['ref'],'GET')
        _logger.info(f"api respnse from return is {apiRes.json()}")
        resJson=apiRes.json()
        if resJson[0]['status'] == "Settled":
            trn.write({
                'btcpay_invoice_id':resJson[0]['id'],
                'btcpay_payment_link':resJson[0]['checkoutLink'],
            })
            trn._set_done() 

        return request.redirect('/payment/status')


    @route(_create_invoice, type='http', auth='public', methods=['POST'], csrf=False)
    def create_invoice(self, **post):
        _logger.info("Inside create_invoice")
        _logger.info(post)
    
        checkout = {
            "redirectURL": f"http://localhost:8069/payment/btcpay/return?ref={post['ref']}",
            "paymentMethods": ["BTC-LightningNetwork"]
        }
    
        payload = {
            "amount": post['amount'],
            "checkout": checkout,
            "currency": post['currency'],
            "additionalSearchTerms" : [post['ref']]
        }
    
        _logger.info("request payload")
        _logger.info(json.dumps(payload))
    
        apiRes = self.btcpayApiCall(payload, '/api/v1/stores/{store_id}/invoices', 'POST')

        return request.redirect(apiRes.json()['checkoutLink'],local=False)

