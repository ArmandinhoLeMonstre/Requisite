import json, smtplib, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from openai import OpenAI

op_client = OpenAI()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

SYSTEM_PROMPT = """You are an email composition agent.
                You will receive a ticket context and must compose a professional approval request email for a manager.
                The email must clearly present:
                - The employee's name
                - The reason for the request
                - The product details (name, price, source, link if available)
                - The ticket ID
                You must return ONLY a valid JSON object, no explanation, no markdown, no backticks.
				The email is sent by an AI so it doesn't need to be signed
                The JSON must follow this exact structure:
                {
                    "subject": string,
                    "body": string
                }"""

def send_email(to_send: str, subject: str, body: str):
	msg = MIMEMultipart()
	msg["From"] = SMTP_USER
	msg["To"] = to_send
	msg["Subject"] = subject
	msg.attach(MIMEText(body, "plain"))

	try:
		with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
			server.starttls()
			server.login(SMTP_USER, SMTP_PASSWORD)
			server.sendmail(SMTP_USER, to_send, msg.as_string())
		return True
	except Exception as e:
		return str(e)

def call_email_agent(data):
	input_list = [
		{
			"role":"system",
			"content": SYSTEM_PROMPT,
		},
		{
			"role": "user",
			"content": json.dumps(data),
		}
	]

	try:
		response = op_client.responses.create(
			model="gpt-4o-mini",
			input=input_list,
		)
	except Exception as e:
		return {"sent": False, "error": str(e)}
	
	try:
		email_content = json.loads(response.output_text)
	except json.JSONDecodeError:
		return {"sent": False, "error": "Invalid JSON returned by model"}

	result = send_email(data["manager"]["email"],
					 email_content["subject"],
					 email_content["body"])
	
	if result is True:
		return {"sent": True, "to": data['manager']["email"],}
	else:
		return {"sent": False, "error": result}
	
# data = {
#     "employee": {
#         "name": "Ricardo",
#         "department": "Marketing",
#         "email": "rafael.nascimento@outlook.be"
#     },
#     "manager": {
#         "name": "Asa",
#         "email": "rafael.nascimento@outlook.be"
#     },
#     "ticket": {
#         "id": "#4821",
#         "reason": "Keyboard broke, keys are no longer registering",
#         "created_at": "2026-04-05"
#     },
#     "product": {
#         "name": "Logitech MK470",
#         "source": "amazon",
#         "price": 65,
#         "link": "https://amazon.com/..."
#     }
# }

# print(call_email_agent(data))