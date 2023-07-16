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
   ![image](https://github.com/ERP-FTW/mlr_ecommerce_btcpay/assets/124227412/905b7ae1-6eb8-48ca-8edb-5205dff00f87)
3. Click on BTCpay server open the record.
4. Enter a Name for the Instance and Company Name to display on the receipt. Enter the expiration 
5. Login into the BTCpay server to be used and navigate to Account -> API Key. Create a key with full priviledges.
6. From BTCpay server copy the following information and paste in the Odoo BTCpay server Instance record: the server base URL, API key, and enter the password to BTCpay server.
7. Click Connect BTCpay Server to verify the information is correct. If it is correct a green popup will affirm so, if it is incorrect a red popup will appear.
8. In Configuration -> Payment Form select the icon for lightning, in Configuration -> Payment Followup select the Payment Journal
9. Select Enable to make BTCpay instance a current method and save (the first time a new Accounting Journal BTCpay will be created and used for recording transactions).
   

Operation
1. A customer will navigate to the Shop section of the website and add items to the cart. After initiating the checkout and filling in customer information the available payment methods will be displayed.
2. The customer can select the Bitcoin Lightning option and directions will appear below.
3. After clicking Pay Now  the customer will be taken to a BTCpay server page with the invoice and QR code to be paid.
4. The customer scans the QR code or pastes the invoice text as a send from their lightning wallet.
6. Upon BTCpay server confirmation of the order the customer can click Return or be returned automatically to the Odoo site depending on BTCpay server settings.
7. Odoo will process the order and create a sales order for fulfillment.
