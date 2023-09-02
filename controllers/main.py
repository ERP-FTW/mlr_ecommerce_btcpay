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

        headers = {"Authorization": "Bearer %s" % (api_key), "Content-Type": "application/json",
                   "Accept": "application/json"}

        _logger.info(f"value of server_url is {server_url} and method is {method}")

        if method == "GET":
            apiRes = requests.get(server_url, headers=headers)
        elif method == "POST":
            apiRes = requests.post(server_url, data=json.dumps(payload), headers=headers)

        return apiRes

    @route(_return_url, type='http', auth='public', methods=['GET', 'POST'], csrf=False)
    def custom_process_transaction(self, **post):
        _logger.info('custom process of transaction')
        trn = request.env['payment.transaction'].sudo().search(
            [('reference', '=', post['ref']), ('provider_code', '=', 'btcpay')])
        btcpay_invoice_id = trn.mapped('btcpay_invoice_id')[0]
        _logger.info(trn)
        _logger.info(btcpay_invoice_id)
        apiRes = self.btcpayApiCall({}, '/api/v1/store/{store_id}/invoice/' + btcpay_invoice_id, 'GET')
        _logger.info(post)
        _logger.info(apiRes.status_code)
        _logger.info(f"api respnse from return is {apiRes.json()}")
        if apiRes.status_code == 200:
            _logger.info(f"api respnse from return is {apiRes.json()}")
            resJson = apiRes.json()['data']
            _logger.info(resJson)
            if resJson.get('status') == "paid":
                #apiInvDet = self.btcpayApiCall({}, '/api/v1/store/{store_id}/invoice/' + resJson[0][
                #    'id'] + '/payment-methods', 'GET')
                #if apiInvDet.status_code == 200:
                    #invDet = apiInvDet.json()
                    #rate = float(invDet[1]['rate'])
                sats = float(resJson.get('satsAmount'))
                trn.write({
                    'btcpay_invoice_id': resJson.get('id'),
                    'btcpay_payment_link': resJson.get('checkoutLink'),
                    #'btcpay_conversion_rate': rate,
                    'btcpay_invoiced_sat_amount': sats,
                })
                trn._set_done()
            else:
                trn._set_error(f"Payment failed!, Nodeless Invoice status: {resJson[0]['status']}")
        else:
            trn._set_error(
                "Issue while checking Nodeless invoice, retry after sometime, if issue persits, please contact support or write to us")

        return request.redirect('/payment/status')

    @route(_create_invoice, type='http', auth='public', methods=['POST'], csrf=False)
    def create_invoice(self, **post):
        _logger.info("Inside create_invoice")
        _logger.info(post)
        web_base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        _logger.info(web_base_url)
        checkout = f"{web_base_url}/payment/btcpay/return?ref={post['ref']}"

        payload = {
            "amount": post['amount'],
            "redirectUrl": checkout,
            "currency": post['currency'],
            "metadata": [post['ref']]
        }

        _logger.info("request payload")
        _logger.info(json.dumps(payload))

        apiRes = self.btcpayApiCall(payload, '/api/v1/store/{store_id}/invoice', 'POST')
        _logger.info(f"response from api call {apiRes.json()}")
        apiRes_json = apiRes.json()['data']
        _logger.info(f"response from api call {apiRes}")

        if apiRes.status_code == 201:
            trn = request.env['payment.transaction'].sudo().search([('reference', '=', post['ref']), ('provider_code', '=', 'btcpay')])
            trn.write({'btcpay_invoice_id': apiRes_json.get('id')})
            _logger.info(trn)
            _logger.info({'btcpay_invoice_id': apiRes_json.get('id')})
            return request.redirect(apiRes_json.get('checkoutLink'), local=False)
        else:
            trn = request.env['payment.transaction'].sudo().search(
                [('reference', '=', post['ref']), ('provider_code', '=', 'btcpay')])
            trn._set_error(
                "Issue while creating Nodeless invoice, retry after sometime, if issue persits, please contact support or write to us")
            return request.redirect('/payment/status')
