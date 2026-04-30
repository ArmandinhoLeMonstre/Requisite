from app.agents_app.agents.inventory_agent import call_inventory_agent
from app.agents_app.agents.amazon_agent import call_amazon_agent
from app.agents_app.agents.mailing_agent import call_email_agent

TOOL_REGISTRY = {
    "call_inventory_agent": call_inventory_agent,
	"call_amazon_agent": call_amazon_agent,
	"call_email_agent": call_email_agent
}