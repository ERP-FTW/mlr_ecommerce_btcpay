# mlr_ecommerce_btcpay
Lightning Rod Point of Sale Community Edition Readme

Overview
This custom module for Odoo 16+ add BTCpay server as a payment method to the Point-of-Sale application. A BTCpay server connected to a lightning node is queried by API calls from Odoo. BTCpay server API access is provided to Odoo and a Create Invoice button is added to the POS action pad. A created invoice for an order is printed on the bill receipt for scanning by customers on paper or the screen. A customer can choose to pay in Lightning or a traditional payment method. The POS Validate payment button will check the status of the invoice and mark the order as paid if the invoice is settled. Conversion rate and invoiced satoshis are stored for each order.

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
2. Click New to create a new record.
   ![image](https://github.com/ERP-FTW/mlr_pos_community/assets/124227412/90591a58-7c0e-43da-931e-252fe154efbf)
4. Enter a Name for the Instance and Company Name to display on the receipt. Enter the expiration 
5. Login into the BTCpay server to be used and navigate to Account -> API Key. Create a key with full priviledges.
6. From BTCpay server copy the following information and paste in the Odoo BTCpay server Instance record: the server base URL, API key, and enter the password to BTCpay server.
   ![image](https://github.com/ERP-FTW/mlr_pos_community/assets/124227412/4ca911a4-94b2-46ff-90e6-fc88e73873d2)
7. Click Test Connection to verify the information is correct. If it is correct a green popup will affirm so, if it is incorrect a red popup will appear.
   ![image](https://github.com/ERP-FTW/mlr_pos_community/assets/124227412/04ec94a0-c1b6-4d62-b898-fac53ff70693)
9. Click Activate to make BTCpay instance a current method (the first time a new Accounting Journal BTCpay will be created and used for recording transactions).
10. In Configuration -> PoS Interface enable Is Bar/Restaurant, in Configuration -> Bar & Restaurant enable Early Receipt Printing, and Configuration -> Payment Methods add BTCpay and in Configuration.

Operation
1. From the Point of Sale Dashboard open a New Session.
2. After creating an order click Create Invoice to generate Lightning Invoice. The generated invoice ID from BTCpay server will appear on a popup, acknowledge by clicking Ok.
   ![image](https://github.com/ERP-FTW/mlr_pos_community/assets/124227412/a32262b0-6f72-49bd-bfc4-922983516567)
4. To view the invoice QR code click Bill. The QR code can be presented to the customer on the screen or with a printed receipt.
   ![image](https://github.com/ERP-FTW/mlr_pos_community/assets/124227412/e7030bfb-83f3-4b73-96b1-f2bab5a2d4e0)
6. From the order navigate to the Payment screen. If the the customer paid with Lightning click Validate to confirm and close the order, if the invoice is unpaid a message will alert the user and an alternative payment method can be used. If the customer wishes to use another payment method, exe out the BTCpay server payment line and use the other payment method.
   ![image](https://github.com/ERP-FTW/mlr_pos_community/assets/124227412/f81ed8f2-2186-4ef8-a023-55b3c336a142)
   ![image](https://github.com/ERP-FTW/mlr_pos_community/assets/124227412/cfc6dc9f-a824-4ceb-9828-247a97b17ce6)
   ![image](https://github.com/ERP-FTW/mlr_pos_community/assets/124227412/ade11951-04ca-477c-b5df-aed39ce8350d)
8. Lightning payment information, satoshi amount and conversion rate, will be stored on the payment model. To view after closing the session navigate to Orders-> Payments and open a specific record.
![image](https://github.com/ERP-FTW/mlr_pos_community/assets/124227412/90fef5a4-d74d-48c1-9a09-9f6e8d266fa1)

