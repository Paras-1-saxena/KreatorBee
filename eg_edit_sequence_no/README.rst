Edit Sequence No
=================
Author: INKERP

This module allows users to edit the sequence numbers for sales orders, purchase orders, warehouse operations, and accounting invoices. 
It includes user-specific access control for editing the sequence number and provides validation to prevent duplicate sequence numbers.

Features:
---------
1) Users View:
   - In the user settings (Settings -> Users & Companies -> User), users can check the options for 'Account Invoice Edit Sequence', 
     'Purchase Order Edit Sequence', 'Sales Order Edit Sequence', and 'Warehouse Edit Sequence'. With these checkboxes checked, 
     the user can edit the sequence for each module separately.

2) Quotation View:
   - Users can edit the sequence number in the sales order, and validation will alert if the new sequence number already exists.
   - The same applies for purchase orders, invoices, and warehouse operations.

3) Inventory View:
   - Users can edit sequence numbers for warehouse operations with validation to avoid duplicate sequences.

4) Validation Error View:
   - Users will receive an alert if they attempt to set a sequence number that already exists in the system.

Installation:
-------------
1. Install the app from the Odoo Apps menu.
2. Navigate to Settings -> Users & Companies -> User to give users permission to edit sequence numbers.
3. Edit sequence numbers in the respective views (sales, purchase, warehouse, accounting) and save changes.

For more support, contact us:
Website: team@inkerp.com
