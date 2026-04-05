from app.tools.purchase_tools.functions import get_amz_product_list


TOOL_REGISTRY = {
    "get_amz_product_list": get_amz_product_list,
}

PARAM_REGISTRY = {
	"get_amz_product_list": "product_info",
}