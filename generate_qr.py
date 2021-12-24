import qrcode
from PIL import Image



qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)

qr.add_data(
    {
        '1': 'Bread                  1.00',
        '2': 'Eggs                   4.50',
        '3': 'Probrand 2L Milk       2.30',
        '4': 'Recoffee               3.00',
        'total_price': 'Total Price            10.80'
    }
)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
img.save("shopping_summary.png")
