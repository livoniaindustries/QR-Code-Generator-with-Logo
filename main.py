import qrcode
from PIL import Image, ImageDraw

def add_rounded_rectangle_frame(image, frame_width, frame_color, corner_radius):
    # Create a new image slightly larger than the original for the frame
    new_size = (image.width + 2*frame_width, image.height + 2*frame_width)
    framed_image = Image.new("RGBA", new_size, (0, 0, 0, 0))
    
    # Draw rounded rectangle as background
    draw = ImageDraw.Draw(framed_image)
    rect_coords = [0, 0, new_size[0], new_size[1]]
    draw.rounded_rectangle(rect_coords, radius=corner_radius, fill=frame_color)
    
    # Paste the original image onto the center
    framed_image.paste(image, (frame_width, frame_width))
    
    return framed_image.convert('RGB')  # Convert back to RGB if needed

def add_rounded_corners(image, radius):
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([0, 0, image.size[0], image.size[1]], radius=radius, fill=255)
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    rounded = Image.new('RGBA', image.size)
    rounded.paste(image, (0, 0), mask=mask)
    return rounded

def generate_qr_with_logo_and_scan_me(link, logo_path, scan_me_path, output_path):
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color='black', back_color='white').convert('RGB')

    # Add rounded frame with slightly rounded corners
    frame_width = 10  # Adjust as needed
    frame_color = "black"  # Frame color
    corner_radius = 15  # Slightly rounded corners for the frame
    qr_with_frame = add_rounded_rectangle_frame(qr_img, frame_width, frame_color, corner_radius)

    # Load logo
    logo = Image.open(logo_path)

    # Resampling method
    try:
        resample_method = Image.Resampling.LANCZOS
    except AttributeError:
        resample_method = Image.ANTIALIAS

    # Resize logo to 20% of QR code size
    qr_size = qr_with_frame.size[0]
    logo_size = int(qr_size * 0.3)
    logo = logo.resize((logo_size, logo_size), resample_method)

    # Center logo on QR code with frame
    pos = ((qr_size - logo_size) // 2, (qr_size - logo_size) // 2)
    if logo.mode in ('RGBA', 'LA'):
        qr_with_frame.paste(logo, pos, mask=logo)
    else:
        qr_with_frame.paste(logo, pos)

    # Load 'scan_me.png'
    scan_me_img = Image.open(scan_me_path)

    # Add rounded corners to 'scan me' image
    corner_radius = 20  # Adjust as needed
    scan_me_rounded = add_rounded_corners(scan_me_img, corner_radius)

    # Resize the 'scan me' image to fit the width of the QR code with frame
    scan_me_width = qr_size
    scan_me_ratio = scan_me_width / scan_me_rounded.width
    new_height = int(scan_me_rounded.height * scan_me_ratio)
    scan_me_resized = scan_me_rounded.resize((scan_me_width, new_height), resample_method)

    # Combine QR code with frame and 'scan me' image
    total_height = qr_size + new_height
    combined_img = Image.new("RGB", (qr_size, total_height), "white")
    combined_img.paste(qr_with_frame, (0, 0))
    combined_img.paste(scan_me_resized, (0, qr_size), mask=scan_me_resized)

    # Save the final image
    combined_img.save(output_path)
    print(f"Saved final QR code with rounded frame and 'scan me' to {output_path}")

# Usage
link = "https://website.com"
logo_path = "logo.png"
scan_me_path = "scan_me.png"
output_path = "final_qr.png"

generate_qr_with_logo_and_scan_me(link, logo_path, scan_me_path, output_path)