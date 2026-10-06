# Arquivo de teste para funcionalidades diversas

#from werkzeug.security import generate_password_hash, check_password_hash

#hashed_password = generate_password_hash("123456")
#print(hashed_password)
#print(check_password_hash(hashed_password, "123456"))
#from datetime import date, datetime

#print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
#print(datetime.strptime('1985-12-15',"%d/%m/%Y"))

import qrcode
from pathlib import Path


def gerar_qrcode(dados: str, caminho_saida: str = "qrcode.png",
                  cor_frente: str = "black", cor_fundo: str = "white") -> str:
    qr = qrcode.QRCode(
        version=None,               # ajusta automaticamente o tamanho
        error_correction=qrcode.constants.ERROR_CORRECT_M,  # correção de erro média
        box_size=10,
        border=4,
    )
    qr.add_data(dados)
    qr.make(fit=True)

    imagem = qr.make_image(fill_color=cor_frente, back_color=cor_fundo)
    Path(caminho_saida).parent.mkdir(parents=True, exist_ok=True)
    imagem.save(caminho_saida)
    return caminho_saida


if __name__ == "__main__":
    # Exemplo: gera um QR Code apontando para uma URL fixa, sem expiração
    destino = gerar_qrcode(
        dados="https://share.busquereinna.com.br/post/f6a14772-bca4-4574-a99f-0e847cee3169?share_v=4",
        caminho_saida="output/qrcode.png",
    )
    print(f"QR Code gerado em: {destino}")