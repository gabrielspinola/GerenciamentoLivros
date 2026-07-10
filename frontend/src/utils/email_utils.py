import base64
import hashlib
import hmac
import json
import os
import smtplib
from email.message import EmailMessage


def generate_confirmation_token(email: str, login: str) -> str:
    payload = json.dumps({"email": email, "login": login}, sort_keys=True)
    secret = os.getenv("SECRET_KEY", "sua_chave_secreta_aqui_mude_em_producao")
    signature = hmac.new(secret.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256).hexdigest()
    token_data = f"{payload}:{signature}"
    return base64.urlsafe_b64encode(token_data.encode("utf-8")).decode("utf-8")


def verify_confirmation_token(token: str):
    try:
        decoded = base64.urlsafe_b64decode(token.encode("utf-8")).decode("utf-8")
        payload, signature = decoded.rsplit(":", 1)
        expected_signature = hmac.new(
            os.getenv("SECRET_KEY", "sua_chave_secreta_aqui_mude_em_producao").encode("utf-8"),
            payload.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        if hmac.compare_digest(signature, expected_signature):
            return json.loads(payload)
    except Exception:
        return None
    return None


def send_confirmation_email(to_email: str, nome: str, token: str) -> bool:
    confirmation_url = f"http://localhost:8080/confirmar-email/{token}"
    message = EmailMessage()
    message["Subject"] = "Confirme seu cadastro"
    message["From"] = os.getenv("MAIL_DEFAULT_SENDER", "no-reply@gerenciamentolivros.local")
    message["To"] = to_email
    message.set_content(
        f"Olá {nome},\n\n"
        f"Clique no link abaixo para confirmar o seu cadastro:\n{confirmation_url}\n\n"
        "Se você não criou uma conta, ignore esta mensagem."
    )

    smtp_server = os.getenv("MAIL_SERVER")
    if not smtp_server:
        print("[email] Servidor SMTP não configurado. Link de confirmação gerado:")
        print(confirmation_url)
        return True

    try:
        with smtplib.SMTP(smtp_server, int(os.getenv("MAIL_PORT", "587"))) as smtp:
            if os.getenv("MAIL_USE_TLS", "True").lower() in {"1", "true", "yes", "on"}:
                smtp.starttls()
            username = os.getenv("MAIL_USERNAME")
            password = os.getenv("MAIL_PASSWORD")
            if username and password:
                smtp.login(username, password)
            smtp.send_message(message)
        return True
    except Exception as exc:
        print(f"[email] Erro ao enviar e-mail: {exc}")
        print(confirmation_url)
        return False
