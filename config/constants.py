# Cores e configurações de design
COLORS = {
    "primary": "#0e2d26",
    "secondary": "#078B6C", 
    "accent": "#FFD770",
    "text": "#FFFFFF",
    "hover": "#FFD770"
}

# Configurações de caminhos
PATHS = {
    "database": "data/bjj_digital.db",
    "logo": "assets/logo.png",
    "selo": "assets/selo_dourado.png",
    "fonte_assinatura": "assets/fonts/Allura-Regular.ttf"
}

# Textos e mensagens
MESSAGES = {
    "welcome": "Bem-vindo ao BJJ Digital",
    "login_success": "Login realizado com sucesso!",
    "logout_success": "Logout realizado com sucesso!"
}

# CSS global
STYLES = {
    "global": """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap');
        
        .stButton>button {
            background: linear-gradient(90deg, #078B6C, #056853);
            color: white;
            font-weight: bold;
            border: none;
            padding: 0.6em 1.2em;
            border-radius: 10px;
            transition: 0.3s;
        }
        
        .login-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 80vh;
        }
        
        .login-title {
            color: #FFD770;
            text-align: center;
            margin-bottom: 2rem;
        }
        </style>
    """
}
