# mlr_ecommerce_btcpay
Lightning Rod Ecommcerce BTCpay Readme

Overview
This custom module for Odoo 16+ adds BTCpay server as a payment provider to the Ecommerce application. A BTCpay server connected to a lightning node is queried by API calls from Odoo. BTCpay server API access is provided to Odoo and a Bitcoin Lightning option is added to the customer checkout. If the Bitcoin payment option is selected by a cutomer, they are forwarded to a BTCpay site with a created invoice and QR code for scanning by customers. After the payment is confirmed the customer can be redirected back to the Odoo online store receipt page and the order is registered and queued.

Prerequisites (versions)
Compatible with Odoo 16
Postgres 14+
BTCpay server connected to Lightning node

Installation (see this video for tutorial on Odoo module installation)
1. Download repository and place extracted folder in the Odoo addons folder.
2. Login to Odoo database to upgrade and enable developer mode under settings.
3. Under apps Update the App list.
4. Search for the module (MLR) and install.

Setup

1. In Odoo navigate to Website-> Ecommerce -> Payment Providers.
2. Click Open to create a new record.
4. Enter a Name for the Instance and Company Name to display on the receipt. Enter the expiration 
5. Login into the BTCpay server to be used and navigate to Account -> API Key. Create a key with full priviledges.
6. From BTCpay server copy the following information and paste in the Odoo BTCpay server Instance record: the server base URL, API key, and enter the password to BTCpay server.
7. Click Connect BTCpay Server to verify the information is correct. If it is correct a green popup will affirm so, if it is incorrect a red popup will appear.
8. In Configuration -> Payment Form select the icon for lightning, in Configuration -> Payment Followup select the Payment Journal
9. Select Enable to make BTCpay instance a current method and save (the first time a new Accounting Journal BTCpay will be created and used for recording transactions).
   

Operation
1. From the Point of Sale Dashboard open a New Session.
2. After creating an order click Create Invoice to generate Lightning Invoice. The generated invoice ID from BTCpay server will appear on a popup, acknowledge by clicking Ok.
4. To view the invoice QR code click Bill. The QR code can be presented to the customer on the screen or with a printed receipt.
6. From the order navigate to the Payment screen. If the the customer paid with Lightning click Validate to confirm and close the order, if the invoice is unpaid a message will alert the user and an alternative payment method can be used. If the customer wishes to use another payment method, exe out the BTCpay server payment line and use the other payment method.
8. Lightning payment information, satoshi amount and conversion rate, will be stored on the payment model. To view after closing the session navigate to Orders-> Payments and open a specific record.
