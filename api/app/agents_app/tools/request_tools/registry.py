from app.agents_app.agents.agent_inventory.agent_inventory_check import call_inventory_agent
from app.agents_app.agents.agent_purchase.amz_search_agent import call_amazon_agent
from app.agents_app.agents.agent_purchase.email_agent import call_email_agent

TOOL_REGISTRY = {
    "call_inventory_agent": call_inventory_agent,
	"call_amazon_agent": call_amazon_agent,
	"call_email_agent": call_email_agent
}