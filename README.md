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
   ![image](https://github.com/ERP-FTW/mlr_ecommerce_btcpay/assets/124227412/9964cfe3-f9c0-49b9-9d01-caaf5ad23e94)
9. In Configuration -> Payment Form select the icon for lightning, in Configuration -> Payment Followup select the Payment Journal.
    ![image](https://github.com/ERP-FTW/mlr_ecommerce_btcpay/assets/124227412/9aa6d542-2425-434f-87c4-1e3fcef9b51d)
10. Select Enable to make BTCpay instance a current method and save (the first time a new Accounting Journal BTCpay will be created and used for recording transactions).
   

Operation
1. A customer will navigate to the Shop section of the website and add items to the cart. After initiating the checkout and filling in customer information the available payment methods will be displayed.
   ![image](https://github.com/ERP-FTW/mlr_ecommerce_btcpay/assets/124227412/99aa0e84-48ed-437c-a803-f239f2161e81)
3. The customer can select the Bitcoin Lightning option and directions will appear below.
   ![image](https://github.com/ERP-FTW/mlr_ecommerce_btcpay/assets/124227412/b08d55e1-b803-4ed4-ab8e-7ff051ed6d65)
4. After clicking Pay Now  the customer will be taken to a BTCpay server page with the invoice and QR code to be paid.
   ![image](https://github.com/ERP-FTW/mlr_ecommerce_btcpay/assets/124227412/6906aea1-d548-463c-912b-df803e65524f)
5. The customer scans the QR code or pastes the invoice text as a send from their lightning wallet.
   ![image](https://github.com/ERP-FTW/mlr_ecommerce_btcpay/assets/124227412/7571de90-8c77-46ab-bbb1-119f0c948d82)
6. Upon BTCpay server confirmation of the order the customer can click Return or be returned automatically to the receipt page of the Odoo site depending on BTCpay server settings.
   ![image](https://github.com/ERP-FTW/mlr_ecommerce_btcpay/assets/124227412/a9aea695-d356-4fad-a00a-0308de976818)
8. Odoo will process the order and create a sales order for fulfillment.
   ![image](https://github.com/ERP-FTW/mlr_ecommerce_btcpay/assets/124227412/a391c517-415d-4613-8153-4bb89ada13ca)

