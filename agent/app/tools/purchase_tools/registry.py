from app.tools.budget_tool import check_budget
from app.tools.policy_tools import get_material_type

TOOL_REGISTRY = {
    "check_budget": check_budget,
	"get_material_type": get_material_type
}