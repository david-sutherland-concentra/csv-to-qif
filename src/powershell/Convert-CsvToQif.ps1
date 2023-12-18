# Define CSV and QIF file paths
$csvFilePath = "path\to\your\csvfile.csv"
$qifFilePath = "path\to\output.qif"

# Read the CSV file
$csvData = Import-Csv -Path $csvFilePath

# Filter out only Buy transactions
$buyTransactions = $csvData | Where-Object { $_.ActivityDescription -eq "Buy" }

# Function to format a transaction to QIF format
function Format-ToQif($transaction) {
    $date = [DateTime]::ParseExact($transaction.TransactionDate, "yyyy-MM-dd", $null).ToString("M/d'yy")
    $amount = [math]::Abs([decimal]$transaction.TotalAmount)
    $symbol = $transaction.Symbol
    $description = $transaction.Description

    # QIF format for a buy transaction
    $qifTrans = @"
D$date
NBuy
Y$symbol - $description
T-$amount
^
"@
    return $qifTrans
}

# Process each buy transaction and write to QIF file
foreach ($transaction in $buyTransactions) {
    $qifTrans = Format-ToQif -transaction $transaction
    Add-Content -Path $qifFilePath -Value $qifTrans
}
