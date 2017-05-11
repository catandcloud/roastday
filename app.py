import requests
import json
import arrow
import csv
import os
import shutil

# Shipstation API creds
api_key = '1faba07e6a5845e7a52111ccda1dae23'
api_secret = 'e5e6bdfc7333440a867d2b34ef133b18'

base_endpoint = 'https://ssapi.shipstation.com/'

# End the order query at midnight on the current day
# end_date = str(arrow.utcnow().to('US/Pacific'))
end_date = str(arrow.utcnow().to('US/Pacific').replace(hour=0, minute=0, second=0, microsecond=0))

endpoint = 'orders'
params = 'orderDateEnd=' + end_date + '&orderStatus=awaiting_shipment'
api_endpoint = endpoint + '?' + params

url = '{}{}'.format(base_endpoint, api_endpoint)
r = requests.get(url, auth=(api_key, api_secret))

order_results = r.json()

# print json.dumps(order_results['orders'][0], indent=4)

coffees = {}

# Loop through orders and get the coffees
for order in order_results['orders']:
	# Skip orders that were canceled or already shipped
	if order.get('orderStatus') in ['shipped', 'cancelled']:
		continue

	# Loop through items and add to coffees dict according to sku
	for item in order['items']:
		
		# Get sku and quantity of current item
		sku = item.get('sku')
		quantity = item.get('quantity')
		
		# Break if there is an item that does not have a sku - it wouldn't be possible to account for in the spreadsheet
		if not sku:
			print "No SKU for item " + item.get('name')
			continue

		# We only want coffee skus
		if "CFE" not in sku:
			continue

		# We only want the following coffee skus, so skip all others
		if not any(x in sku for x in ['10oz', '1lb', 'KILO', '5lb']):
			continue

		# Split the sku at the grind (since it has nothing to do with this)
		sku = sku.split('-')[1] + '-' + sku.split('-')[2]

		# Treat all subscription skus as the same
		if 'Sub' in sku or 'Staff' in sku:
			sku = 'Sub' + '-' + sku.split('-')[1]

		# Init the sku coffees dict entry for each new sku
		if not coffees.get(sku):
			coffees[sku] = 0
		
		# Increment the coffee sku entry by the quantity in the current order
		coffees[sku] += quantity

# Get the user's home dir from the shell
home_dir = os.getenv('HOME')
roast_dir = home_dir + '/Dropbox/Cat & Cloud Admin/Roasting'

# Open up the previous roast day csv file, copy EOD Stock
prev_roast_file = None
curr_stock = {}
for file in os.listdir(roast_dir):
	if file.endswith("Roast.csv"):
		prev_roast_file = roast_dir + '/' + file

if prev_roast_file:
	with open(prev_roast_file, 'r') as csvfile:
		reader = csv.DictReader(csvfile)

		# Loop through rows of csv file
		for row in reader:
			curr_sku = row.get('SKU')
			
			if not curr_stock.get(curr_sku):
				curr_stock[curr_sku] = 0
			
			if row.get('EOD STOCK'):
				curr_stock[curr_sku] = row.get('EOD STOCK')
else:
	print "Could not find previous roast day file - input current stock manually"

# Init the new rows list, which will store the quantities for each sku
new_rows_list = []

with open(roast_dir + '/Roast Day Template.csv', 'r') as csvfile:	
	reader = csv.DictReader(csvfile)

	# Loop through rows of csv file
	for idx, row in enumerate(reader):
		if row.get('SKU'):
			# Loop through coffees and write to the proper row/column, according to sku
			for coffee, quantity in coffees.iteritems():
				sku_cfe = coffee.split('-')[0]
				sku_size = coffee.split('-')[1]

				if row.get('SKU') == sku_cfe:
					row[sku_size] = quantity

					if curr_stock.get(sku_cfe):
						row['IN STOCK'] = curr_stock[sku_cfe]
		new_rows_list.append(row)

# Write to a new csv file
curr_roast_file = '%s_Roast.csv' % arrow.utcnow().to('US/Pacific').format('YYYY-MM-DD')
write_file = roast_dir + '/' + curr_roast_file
with open(write_file, 'w') as csvfile:
	fieldnames = ['SKU', 'Coffee', '10oz', '1lb', 'KILO', '5lb', 'IN STOCK', 'ROASTED LBS', 'GREEN LBS', 'BATCHES', 'EOD STOCK']
	writer = csv.DictWriter(csvfile, fieldnames)
	
	writer.writeheader()
	writer.writerows(new_rows_list)

# Archive previous roast day worksheets
archive_dir_path = roast_dir + '/Archive/Roast Day Archives'
for file in os.listdir(roast_dir):
	if file.endswith("Roast.csv"):
		# Skip the current roast file
		if file == curr_roast_file:
			continue
		shutil.move(roast_dir + '/' + file, archive_dir_path + '/' + file)
