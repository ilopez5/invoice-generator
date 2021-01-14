#!/bin/python3
import traceback
import datetime
import requests
import sys
sys.dont_write_bytecode = True
import spout
import os

# init progress bar
pb = spout.ProgressBar(width=50, pad=60)

def getAccessToken():
    pb.begin("Acquiring ZipBooks Access Token", stages=2)
    # read credentials from file
    with open(sys.argv[1], "r") as fd:
        credentials = fd.read().splitlines()
        email = credentials[0].split("=")[1]
        password = credentials[1].split("=")[1]
    pb.checkpoint()

    # assemble and make cURL request for access token and 
    url      = 'https://api.zipbooks.com/v2/auth/login'
    headers  = {'Content-Type':'application/json'}
    data     = f'{{"email": "{email}", "password": "{password}"}}'
    response = requests.post(url, headers=headers, data=data).json()

    # parse response
    access_token = response['data']['attributes']['user-tokens'][0]['token']
    pb.checkpoint()
    pb.end()
    return access_token

def getData(access_token):
    pb.begin("Downloading time entries", stages=1)
    assert(access_token)

    # assemble cURL request for time entries
    url     = 'https://api.zipbooks.com/v2/time-entries'
    headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
    }
    
    # make request and capture response
    response = requests.get(url, headers=headers).json()
    data = response['included']
    pb.checkpoint()
    pb.end()
    return data

def parseData(data):
    pb.begin("Parsing JSON data", stages=3)
    wage = 15
    output = list()
    entries = dict()

    # get all unpaid entries
    for entry in data:
        # we only care about unpaid entries
        if entry['type'] == 'time-entry' and not entry['attributes']['paid']:
            year, month, day = [int(x) for x in entry['attributes']['date'].split('-')]
            hours = entry['attributes']['duration'] / 3600
            date  = datetime.date(year, month, day)
            entries[date] = hours
    pb.checkpoint()

    # sort and assemble 
    for date in sorted(entries):
        hours = entries[date]
        fdate = date.strftime("%B %d, %Y")
        output.append(f"\hourrow{{{fdate}}}{{{hours}}}{{{wage}}}\n")
    pb.checkpoint()
    
    # write LaTeX formatted entries to file
    with open("entries.tex", "w+") as fd:
        fd.writelines(output)
    pb.checkpoint()
    pb.end()
    return

def compileInvoice():
    pb.begin("Compiling PDF", stages=2)
    # get current invoice number and write to file
    _, _, files = next(os.walk(sys.argv[2]))
    invoice_number = str(len(files) + 1).zfill(3)
    with open("invoice_num.tex", "w+") as fd:
        fd.write(invoice_number)
    pb.checkpoint()

    # compile with pdflatex
    os.system("pdflatex --interaction=batchmode invoice.tex 2>&1 > /dev/null")
    pb.checkpoint()
    pb.end()
    return invoice_number

def clean(invoice_number=0):
    pb.begin("Cleaning up auxiliary files", stages=2)

    # remove any auxiliary files
    os.system("rm -rf *.aux *.log invoice_num.tex entries.tex")
    pb.checkpoint()

    # rename pdf to include invoice number
    if os.path.exists("invoice.pdf"):
        os.rename("invoice.pdf", f"invoice_{invoice_number}.pdf")
    pb.checkpoint()
    pb.end()

def main():
    try:
        # get ZipBooks Access Token
        access_token = getAccessToken()

        # use access token to pull data
        data = getData(access_token)

        # parse data and save to .tex file
        parseData(data)

        # compile latex document
        invoice_number = compileInvoice()

        # remove any auto-generated or associated files
        clean(invoice_number)
    except Exception as e:
        print("Error:\n" + traceback.format_exc())

if __name__ == '__main__':
    main()
