## .env file

  SECRET_KEY=your_super_secret_key_for_jwt
  #You can generate one with: `from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())`
  FERNET_KEY=your_fernet_key
