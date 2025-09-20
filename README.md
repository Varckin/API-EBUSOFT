# API EBUSOFT

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.116-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Docker](https://img.shields.io/badge/Docker-Supported-blue)
![Contributions](https://img.shields.io/badge/Contributions-Welcome-brightgreen)

</div>

---

## 📌 About the Project

**API EBUSOFT** is a modular API service built with **FastAPI**, providing a collection of tools for developers, engineers, and researchers.

It combines dozens of useful microservices: from UUID and password generation to working with QR codes, Base64, PGP encryption, and certificate analysis.

The project was developed as a **universal platform for development, testing, and prototyping**, and can be used for both personal and corporate purposes.

---

## ✨ Features

Main project modules:

- 🔑 **Data Generation**
  - UUID (`gen_uuid`)
  - Passwords (`gen_pass`)
  - Hashes (`gen_hash`)
  - IDs (`id_generator`)

- 🗄 **Encoding Utilities**
  - Base64 (`base64_coder`)
  - URL encode/decode (`url_codec`)
  - Slugify (`slug`)
  - Data converter (`data_converter`)

- 🔒 **Cryptography & Security**
  - Certificate validation (`cert`)
  - PGP encryption/decryption (`pgp`)
  - Data validator (`data_validator`)

- 🌍 **Networking Tools**
  - DNS forward/reverse (`dns_forw_rev`)
  - IP geolocation (`ip_geo_lookup`)
  - Traceroute (`traceroute`)

- 📊 **Utilities**
  - QR code generator (`qr_code`)
  - Audio processing (`speech`)
  - Video downloader (`ytdlp`)

---

## 🚀 Installation & Run

1. Clone the repository

```bash
git clone https://github.com/Varckin/API-EBUSOFT.git
cd API-EBUSOFT
```

2. Install dependencies

Use a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Run locally

```bash
uvicorn main:app --reload
```

After startup, documentation will be available at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

4. Run with Docker

```bash
docker-compose up --build
```

## ⚙️ Configuration

The project supports configuration through a `.env` file. Example:

```.env
CRT_BASE=url

CITY_DB_PATH=path
ASN_DB_PATH=path
COUNTRY_DB_PATH=path
```

## 📚 Usage Examples

Generate UUID:

```bash
curl -X POST http://127.0.0.1:8000/uuid
```

Base64 encoding:

```bash
curl -X POST -F "data=Hello" http://127.0.0.1:8000/base64/string
```

Generate QR code:

```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"data": "https://ebusoft.xyz", "format": "png"}' \
     http://127.0.0.1:8000/qr
```

Check SSL certificate:

```bash
curl -X POST -d "domain=example.com" http://127.0.0.1:8000/cert/search
```

## 🧩 Project Architecture

```text
API EBUSOFT/
│
├── main.py               # FastAPI entry point
├── requirements.txt      # Dependencies
├── docker-compose.yml    # Docker environment
├── Dockerfile            # Docker build
│
├── base64_coder/         # Base64 module
├── cert/                 # Certificates
├── data_converter/       # Data conversion
├── data_validator/       # Schema validation
├── dns_forw_rev/         # DNS forward/reverse lookup
├── gen_hash/             # Hash generation
├── gen_pass/             # Password generation
├── gen_uuid/             # UUID generation
├── id_generator/         # Identifier generation
├── ip_geo_lookup/        # IP geolocation
├── qr_code/              # QR codes
├── slug/                 # Slugify
├── speech/               # Audio processing
├── traceroute/           # Traceroute
├── url_codec/            # URL encode/decode
└── ytdlp/                # YouTube/Insta/SoundCloud downloader
```

## 🧪 Testing

The project uses pytest:

```bash
pytest -v
```

## 📖 Documentation

Detailed documentation is located in the `docs` directory. It includes request examples, schemas, and API descriptions.

## 🤝 Contributing

Any suggestions and improvements are welcome! Please check `CONTRIBUTING.md` to learn how you can contribute.

## 📜 License

This project is distributed under the MIT license.

## ⭐ Support the Project

If you like this project, don’t forget to give it a ⭐ on GitHub!
