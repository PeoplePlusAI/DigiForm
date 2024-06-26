Do you hate filling out forms? As a child (and maybe still), did you get your mother or father to fill out forms for you?

Form filling is a very manual process. 
It requires a lot of attention to detail and the chance of error is high. 
Forms builders are often sticklers about the format of data entry. 
What we often take for granted, is that form filling is a very difficult task for low literacy demographics of our country.

For most forms, we take information from existing base documents and re-enter it into the form. We then attach those same documents to the form as supporting evidence.

E.G. — You manually enter all the information on your 10th and 12th mark sheets to apply for college admission. You then attach those same mark sheets to your admission form.

Solution:
Build an AI-powered tool/bot/capability that can fill a form using speech recognition and image detection.

What If:

You can select OR upload the form you want to fill out (link, pdf, xls, doc format)
The AI reads the form and prompts you with which documents to upload to optimize the form-filling process
You upload those documents by taking photos of them or a file drag and drop.
An AI reads those documents and fills in the form provided
The AI then asks you for responses to the questions on the form that are remaining — through voice or text
You first review the fields on the form and then finalize the render. 
The AI then sends you a PDF of the form filled out — error-free, minimal effort, and time-saving
Cooler features — attach the supporting documents as a QR code on the form with verifiable credentialing so that it is paperless.

Applications of use case:

Government Schemes — social schemes with Aadhaar, Ration, PAN, Voter ID, etc.
College admissions — students fill out multiple applications across several colleges
Banking — account opening, applying for loans, other banking tools
Insurance — incident certificates, identity proof, cancelled cheque, supporting bills
Visa Application — passport, hotel, flight, employment, bank information

The plan of action:

Find 3 use cases for form filling and build a working prototype
Research the most common data points asked on forms and the most common documents required
Conduct user research across the initial use cases to understand their form-filling behaviour
Build a dataset of 1000+ forms that we can use for training and testing
Decide the best way to host a solution like this — Chatbot? Messaging app? Web app?
Design a front-end UI/UX that users can test the prototype on
Figure out how we can host several forms on this solution — should the user upload the form they wish to fill out each time? Or should the AI have an existing repository of forms?
Develop the tech stack and APIs required to build this solution — which LLM, Language Translation API, Hosting Platform, Server, etc
Build a go-to-market deck and strategy and model for this solution — who finally pays for the product? B2B or B2C?
Privacy and Safeguards — The documents shared could be sensitive information. Should the shared document be federated to the local device and enable a one-time share access approach? The opportunity cost is the lower efficiency from conversation history not maintained.
Modularity to ensure each component of the system can evolve independently and can be swapped with another component if needed.

## Setup

Rename [`.env.example`](.env.example) to `.env`, and add the missing fields.

To start the backend service along with the DB, run the following command:

```bash
docker compose up -d --build
```

### Telegram bot

Start chatting with the telegram bot with the `/start` command.
