from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from config import email, senha
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 
app.secret_key = 'amor'

mail_settings = {
    "MAIL_SERVER": 'smtp-mail.outlook.com',
    "MAIL_PORT": "587",
    "MAIL_USE_TLS": True,
    "MAIL_USE_SSL": False,
    "MAIL_USERNAME": email,
    "MAIL_PASSWORD": senha
}

app.config.update(mail_settings)

mail = Mail(app)

class Contact:
    def __init__(self, name, lastname, email, phone, subject, message):
        self.name = name
        self.lastname = lastname
        self.email = email
        self.phone = phone
        self.subject = subject
        self.message = message

@app.route('/send', methods=['POST'])
def send():
    data = request.form

    # Extrair os dados do formulário
    name = data['name']
    lastname = data['lastname']
    email = data['email']
    phone = data['phone']
    subject = data['subject']
    message = data['message']

    # Criar a message de email
    msg = Message(
        subject=f'{name} {lastname} te enviou uma mensagem',
        sender=app.config.get("MAIL_USERNAME"),
        recipients = ['adriano.rsouza@outlook.com.br', app.config.get("MAIL_USERNAME")],
        body=f'''
            {name} {lastname} com o email {email} e telefone {phone} te enviou a seguinte mensagem:

            Assunto: {subject}
            mensagem: {message}
        '''
    )

    # Enviar o email
    try:
        mail.send(msg)
        return jsonify({'message': 'Email enviado com sucesso'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)
