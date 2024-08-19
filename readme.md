### https://peopleplus.ai/digiform

## Setup

### Project Prerequisites

- A network-connected server with a minimum of 2 GB RAM
- Docker Compose V2
- Groq API Key
- Telegram Bot Token

This project can be run on [GitHub CodeSpaces](https://github.com/codespaces).

### Running the Backend

Rename [`.env.example`](.env.example) to `.env`, and add the missing fields.

A sample `.env` file will look like this:
```
PORT=6001
PGPORT=5432
POSTGRES_USER="digiform"
POSTGRES_PASSWORD="digiform"
POSTGRES_DB="digiform"
GROQ_API_KEY="<your-groq-api-key>"
GROQ_CHAT_MODEL="llama3-70b-8192"
DJANGO_SECRET_KEY="django-insecure-n^)*5*ysvl&@j!89mrjyu6^&*8(mvu9cc_78oa00tbb@=5l%0l"
TELEGRAM_BOT_TOKEN="<your-telegram-bot-token>"
```

To start the backend service along with the DB, run the following command:

```bash
docker compose up -d --build
```

### Telegram Bot

Once the backend service is running, you can start chatting with the telegram bot using the `/start` command.

The bot will greet you and request your mobile number. Enter your valid mobile number when prompted.

Next, the bot will ask for your email address. Provide your valid email address.

Now, the bot will prompt you to upload your Aadhaar and PAN documents. Send the scanned copies or clear photographs of your Aadhaar and PAN to the bot.

After receiving your documents, the bot will process the information and fill in the relevant fields in the form.

Once the form is filled, the bot will send you a table displaying the extracted information for your verification. If you want to update any information, you can do so here.

Finally, the bot will display the time taken to complete the entire process, with a Thank You message.

### Prerequisites for Using the Bot

- A Telegram account
- A valid mobile number
- A valid email address
- Either Aadhaar or PAN card documents (scanned or photographed)
