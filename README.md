# 📦 Estudo de FastAPI com REST - Sistema de Delivery

> **⚠️ Este projeto é de caráter didático. O código está extensivamente comentado para facilitar o entendimento de quem está aprendendo.**

## 🧠 Objetivo

Este projeto tem como objetivo apresentar a implementação completa de uma API RESTful utilizando **FastAPI**, simulando o funcionamento básico de um sistema de **delivery online**. O sistema cobre aspectos essenciais como cadastro de usuários, restaurantes, produtos, pedidos e autenticação.

## 🚀 Tecnologias Utilizadas

- **FastAPI** - Framework web moderno e rápido para criação de APIs em Python  
- **Pydantic** - Validação de dados e definição de modelos  
- **SQLAlchemy** - ORM para manipulação do banco de dados  
- **SQLite** - Banco de dados leve utilizado para fins de teste  
- **Uvicorn** - Servidor ASGI para rodar a aplicação  
- **JWT** - Autenticação baseada em tokens  

## 🔐 Funcionalidades Implementadas

- [x] Cadastro e login de usuários com autenticação JWT  
- [x] Criação e gerenciamento de restaurantes  
- [x] Cadastro e listagem de produtos por restaurante  
- [x] Criação e acompanhamento de pedidos  
- [x] Rotas protegidas por autenticação  
- [x] Comentários explicativos no código para facilitar o aprendizado  

## 🧪 Como Rodar Localmente

1. Clone o repositório:
   ```bash
   git clone https://github.com/seuusuario/fastapi-delivery-study.git
   cd fastapi-delivery-study

2. Crie um ambiente virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate  # ou venv\Scripts\activate no Windows
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Execute a aplicação:

   ```bash
   uvicorn app.main:app --reload
   ```

5. Acesse a documentação interativa em:

   ```
   http://127.0.0.1:8000/docs
   ```

## 📖 Considerações

Este projeto não possui foco em segurança ou performance em ambiente de produção. É uma base sólida para estudos, podendo ser expandido futuramente com:

* Pagamentos online simulados
* Painel de administração
* Deploy em nuvem
* Testes automatizados

---

## 📌 Aviso

> Todo o código está comentado com explicações passo a passo para facilitar o aprendizado de quem está estudando FastAPI e APIs REST.
> Sinta-se à vontade para clonar, modificar, e usar como base para seus próprios estudos.

## REFERÊNCIAS
>https://www.youtube.com/@HashtagProgramacao
>https://chatgpt.com/
>https://www.youtube.com/watch?v=2MmmjUv_tRc&pp=ygUNZmFzdCBhcGkgcmVzdA%3D%3D
