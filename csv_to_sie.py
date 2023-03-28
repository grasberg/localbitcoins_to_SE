#!/usr/bin/python3
import argparse
import csv

cstr1="1930"
cstr3="6571"

parser=argparse.ArgumentParser()

parser.add_argument("-i","--input",help="Input Filename, to process",required=True)
parser.add_argument("-o","--output",help="Output Filename",required=True)

args=parser.parse_args()

#arguments
op_file=args.output
inp_file=args.input

ofd=open(op_file,'w')

#read csv file
with open(inp_file) as f:
	csv_dict = csv.DictReader(f)

	seq=0

	for row in csv_dict:
		seq+=1
		dts=''.join(row['created_at'].split(" ")[0].split("-")[:3])
		dtf=''.join(row['transaction_released_at'].split(" ")[0].split("-")[:3])
		order_str=row['trade_type'].split("_")[1]
		if order_str == "BUY":
			name=row['seller']
			cstr2="4010"
			minusa="-"
			minusb=""
		elif order_str == "SELL":
			name=row['buyer']
			cstr2="3054"
			minusa=""
			minusb="-"

		refer_str=row['reference']
		fiat_amt=row['fiat_amount']
		fiat_fee=row['fiat_fee']
		btc_amount_less_fee=row['btc_amount_less_fee']
		
		record="#VER A "+str(seq)+" "+dts+" \""+order_str+" "+name+" "+btc_amount_less_fee+"btc\" "+dtf+"\n{\n   #TRANS "+cstr1+" {} "+minusa+fiat_amt+"\n   #TRANS "+cstr2+" {} "+minusb+fiat_amt+"\n   #TRANS "+cstr3+" {} "+fiat_fee+"\n   #TRANS "+cstr1+" {} "+"-"+fiat_fee+"\n}"
		print(record,file=ofd)


print("Converted "+str(seq)+" rows.")
ofd.close()


"""
#VER A 1 20171129 "BUY Intropia L16563438B9V0FI" 20171129
{
   #TRANS 1930 {} -4064.24
   #TRANS 1910 {} 4064.24
}
"""		