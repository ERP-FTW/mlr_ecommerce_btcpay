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

    def btcpayApiCall(self, payload, api, method):
        btcpay_details = request.env['payment.provider'].sudo().search([('code', '=', 'btcpay')])
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
            apiRes = requests.get(server_url, headers=headers)
        elif method == "POST":
            apiRes = requests.post(server_url, data=json.dumps(payload), headers=headers)

        return apiRes

    @route(_return_url, type='http', auth='public', methods=['GET', 'POST'], csrf=False)
    def custom_process_transaction(self, **post):
        trn = request.env['payment.transaction'].sudo().search(
            [('reference', '=', post['ref']), ('provider_code', '=', 'btcpay')])
        apiRes = self.btcpayApiCall({}, '/api/v1/stores/{store_id}/invoices?textsearch=' + post['ref'], 'GET')

        if apiRes.status_code == 200:
            _logger.info(f"api respnse from return is {apiRes.json()}")
            resJson = apiRes.json()
            if resJson[0]['status'] == "Settled":
                apiInvDet = self.btcpayApiCall({}, '/api/v1/stores/{store_id}/invoices/' + resJson[0][
                    'id'] + '/payment-methods', 'GET')
                if apiInvDet.status_code == 200:
                    invDet = apiInvDet.json()
                    #rate = float(invDet[1]['rate'])
                    sats = float(invDet[0]['amount'])
                trn.write({
                    'btcpay_invoice_id': resJson[0]['id'],
                    'btcpay_payment_link': resJson[0]['checkoutLink'],
                    #'btcpay_conversion_rate': rate,
                    'btcpay_invoiced_sat_amount': sats,
                })
                trn._set_done()
            else:
                trn._set_error(f"Payment failed!, BTCPay Invoice status: {resJson[0]['status']}")
        else:
            trn._set_error(
                "Issue while creating BTCPay invoice, retry after sometime, if issue persits, please contact support or write to us")

        return request.redirect('/payment/status')

    @route(_create_invoice, type='http', auth='public', methods=['POST'], csrf=False)
    def create_invoice(self, **post):
        _logger.info("Inside create_invoice")
        _logger.info(post)

        checkout = {
            "redirectURL": f"http://localhost:8069/payment/btcpay/return?ref={post['ref']}",
            "paymentMethods": ["BTC", "BTC-LightningNetwork"]
        }

        payload = {
            "amount": post['amount'],
            "checkout": checkout,
            "currency": post['currency'],
            "additionalSearchTerms": [post['ref']]
        }

        _logger.info("request payload")
        _logger.info(json.dumps(payload))

        apiRes = self.btcpayApiCall(payload, '/api/v1/stores/{store_id}/invoices', 'POST')
        _logger.info(f"response from api call {apiRes.json()}")

        if apiRes.status_code == 200:
            return request.redirect(apiRes.json()['checkoutLink'], local=False)
        else:
            trn = request.env['payment.transaction'].sudo().search(
                [('reference', '=', post['ref']), ('provider_code', '=', 'btcpay')])
            trn._set_error(
                "Issue while creating BTCPay invoice, retry after sometime, if issue persits, please contact support or write to us")
            return request.redirect('/payment/status')
