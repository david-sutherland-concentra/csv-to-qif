import csv

def load_security_names(qif_file_path):
    security_names = {}
    with open(qif_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for i in range(len(lines)):
            if lines[i].startswith('N') and i+1 < len(lines) and lines[i+1].startswith('S'):
                full_name = lines[i][1:].strip()
                symbol = lines[i+1][1:].strip()
                security_names[symbol] = full_name
    return security_names

def convert_csv_to_qif_with_reinvestment(csv_file_path, qif_file_path, security_list_path):
    # Load security names from the security list
    security_names = load_security_names(security_list_path)

    with open(csv_file_path, 'r', encoding='utf-8-sig') as csv_file, open(qif_file_path, 'w', encoding='utf-8') as qif_file:
        reader = csv.DictReader(csv_file)

        # Write the account header for an investment account
        qif_file.write("!Type:Invst\n")

        for row in reader:
            # Format the date
            qif_file.write("D" + row['Transaction Date'][5:7] + "/" + row['Transaction Date'][8:10] + "/" + row['Transaction Date'][0:4] + "\n")

            # Determine transaction type
            if row['Activity Description'] == 'Reinvestment':
                transaction_type = 'Buy'
            elif row['Symbol'] in ['ZAG', 'ZRR']:
                transaction_type = 'IntInc'  # Label for ZAG and ZRR transactions
            else:
                transaction_type = 'Div'  # Label for all other transactions

            # Add Transaction Type
            qif_file.write("N" + transaction_type + "\n")

            # Add Security Full Name
            full_name = security_names.get(row['Symbol'], row['Symbol'])
            qif_file.write("Y" + full_name + "\n")

            # Handling for different transaction types
            if transaction_type == 'Buy':
                # Calculate price per unit for Buy transactions
                quantity = float(row['Quantity'])
                total_amount = abs(float(row['Total Amount']))
                price_per_unit = total_amount / quantity if quantity != 0 else 0

                # Add Price, Quantity, Total Amount for Buy transactions
                qif_file.write("I{:.2f}\n".format(price_per_unit))
                qif_file.write("Q{:.0f}\n".format(quantity))
                qif_file.write("T{:.2f}\n".format(total_amount))
            else:
                # Add Price, Quantity, Total Amount for IntInc and Div transactions
                qif_file.write("I" + row['Price'] + "\n")
                if transaction_type != 'IntInc':
                    qif_file.write("Q" + row['Quantity'] + "\n")
                if transaction_type != 'Div':
                    qif_file.write("T" + row['Total Amount'] + "\n")

            # End of entry
            qif_file.write("^\n")

    print(f"Conversion complete. QIF file saved as: {qif_file_path}")

# File paths (these need to be set by the user)
csv_file_path = 'C:\DEV\Personal\Projects\csv-to-qif\data\TransactionHistory_22114431 - Reinvestments - 2023-10-01 to 2023-12-12.csv'
qif_file_path = 'C:\DEV\Personal\Projects\csv-to-qif\data\TransactionHistory_22114431 - Reinvestments - 2023-10-01 to 2023-12-12.qif'
security_list_path = 'C:\DEV\Personal\Projects\csv-to-qif\data\Quicken Export Security List.QIF'

# Perform the conversion
convert_csv_to_qif_with_reinvestment(csv_file_path, qif_file_path, security_list_path)
