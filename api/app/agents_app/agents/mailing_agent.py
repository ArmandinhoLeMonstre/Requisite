import json, smtplib, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from openai import AsyncOpenAI
from app.database import AsyncSessionLocal

from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError
from app.models.ticket_model import TicketStatus, Ticket, uuid

from app.agents_app.agents_exceptions import SubAgentError

openai_api_key = os.getenv("OPENAI_API_KEY")

client = AsyncOpenAI(
  api_key=openai_api_key
)

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

async def update_ticket_status(ticket_id: str):
	async with AsyncSessionLocal() as db:
			try:
				stmt = await db.execute(
					update(Ticket)
					.where(Ticket.id == ticket_id)
					.values()
				)

				await db.commit()

			except SQLAlchemyError as e:
				await db.rollback()
				raise

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
		raise SubAgentError(
			message=str(e),
			agent= "mail_agent",
			action= "Inform the user that there is a problem with the notifier agent, he can retry later",
			step="Email send"
		)
	

async def call_email_agent(data, product):
	final_data = data | product
	input_list = [
		{
			"role":"system",
			"content": SYSTEM_PROMPT,
		},
		{
			"role": "user",
			"content": json.dumps(final_data),
		}
	]

	try:
		response = await client.responses.create(
			model="gpt-4o-mini",
			input=input_list,
		)
	except Exception as e:
		raise SubAgentError(
				message=str(e),
				agent= "mail_agent",
				action= "Inform the user that there is a problem with the notifier agent, he can retry later",
				step="OpenAI call"
			)
	
	try:
		email_content = json.loads(response.output_text)
	except json.JSONDecodeError:
		raise SubAgentError(
			message="Invalid JSON returned by model",
			agent="mail_agent",
			action="your_action",
			step="json_parsing"
		)

	result = send_email(data["manager"]["email"],
					 email_content["subject"],
					 email_content["body"])
	
	if result is True:
		try:
			await update_ticket_status(data['ticket']["id"])
			return {"success": True, "to": data['manager']["email"]}
		except Exception as e:
			raise SubAgentError(
				message=str(e),
				agent= "mail_agent",
				action= "Inform the user that there is a problem with the notifier agent, he can retry later",
				step="update_ticket_status"
			)
	else:
		return {"success": False, "error": result}
