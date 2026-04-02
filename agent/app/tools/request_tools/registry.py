from app.tools.request_tools.call_inventory_agent import call_inventory_agent
from app.tools.request_tools.call_amazon_agent import call_amazon_agent
from app.tools.request_tools.call_email_agent import call_email_agent

TOOL_REGISTRY = {
    "call_inventory_agent": call_inventory_agent,
	"call_amazon_agent": call_amazon_agent,
	"call_email_agent": call_email_agent
}