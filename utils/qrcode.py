QRCODE_API_URL = 'https://qrcode.tec-it.com/API/QRCode?data={data}&quietzone={quietzone}'


def generate_qr_code_url(data: str | int, quietzone: int = 4): 
    return QRCODE_API_URL.format(
        data=data,
        quietzone=quietzone
    )
