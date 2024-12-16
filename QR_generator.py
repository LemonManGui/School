import qrcode

def generate_qr_code(text, file_name): # Create QR object with specific configuration
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    # add data to the QR code
    qr.add_data(text)
    qr.make(fit=True)
    
    # Generate en image of the QR code
    img = qr.make_image(fill_color="#FFA500", back_color="#F5F5DC")
    # Save the image
    #img.save(file_name)
    # Option: Show the image
    img.show()

    
# Input text to generate QR code for
text = "https://www.myrapilar.com/"
# File name to save QR code image
file_name = "/Users/gui/Desktop/School/QR_test.png"

# Generate the QR code
generate_qr_code(text, file_name)
print(f"QR code saved as {file_name}")
        
