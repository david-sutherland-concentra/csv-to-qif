
import csv

def convert_standard_csv_to_qif(csv_file_path, qif_file_path):
    with open(csv_file_path, 'r', encoding='utf-8-sig') as csv_file, open(qif_file_path, 'w', encoding='utf-8') as qif_file:
        reader = csv.DictReader(csv_file)

        # Write the account header for an investment account
        qif_file.write("!Type:Invst\n")

        for row in reader:
            # Map CSV fields to QIF fields
            qif_file.write("D" + row['Transaction Date'] + "\n")  # Date
            qif_file.write("T" + row['Total Amount'] + "\n")      # Total Amount
            qif_file.write("P" + row['Activity Description'] + "\n") # Payee / Activity Description
            qif_file.write("N" + row['Description'] + "\n")       # Transaction Type/Description
            # Additional details (like symbol, quantity) in memo field
            memo = f"Symbol: {row['Symbol']}, Quantity: {row['Quantity']}, Price: {row['Price']} {row['Price Currency']}"
            qif_file.write("M" + memo + "\n")
            # End of entry
            qif_file.write("^\n")

    print(f"Conversion complete. QIF file saved as: {qif_file_path}")

# File paths (these need to be set by the user)
csv_file_path = 'path_to_your_csv_file.csv'
qif_file_path = 'path_to_your_qif_file.qif'

# Perform the conversion
convert_standard_csv_to_qif(csv_file_path, qif_file_path)
