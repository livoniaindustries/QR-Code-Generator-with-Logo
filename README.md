QR Code Generator with Logo and Scan Me Badge
A Python tool to create professional QR codes with custom logos and "Scan Me" badges.

Features
Generate QR codes for any URL or text

Add your logo in the center of the QR code

Add a "Scan Me" badge below the QR code

Rounded corners on both the QR frame and badge

High error correction for reliable scanning

Requirements
Python 3.6 or higher

qrcode library

Pillow library

Installation
bash
pip install qrcode pillow
Required Files
File	Description
logo.png	Your logo (transparent background recommended)
scan_me.png	"Scan Me" badge image
qr_generator.py	The Python script
Quick Start
Place your logo.png and scan_me.png in the same folder as the script

Edit the URL in the script:

python
link = "https://your-website.com"
Run the script:

bash
python qr_generator.py
Find your QR code as final_qr.png

Customization Options
You can modify these parameters in the script:

frame_width - Thickness of the black border

corner_radius - Roundness of corners

logo_size - Size of logo (default: 30% of QR)

box_size - Size of QR code modules

Output Example
The script generates a single PNG file containing:

QR code with black rounded frame

Your logo centered in the QR code

"Scan Me" badge below with rounded corners
