from api.models.models import InputList
from sqlalchemy import select
from sqlalchemy.dialects.sqlite import insert
import json

def save_input_list(db, ticket_id, new_input_list):

	stmt = insert(InputList).values(
	    id=ticket_id, data=new_input_list
	)
	stmt = stmt.on_conflict_do_update(
		index_elements=["id"],
		set_={
			"data": stmt.excluded.data
		}
	)

	db.execute(stmt)
	db.commit()
	# db.add(to_add_input)
	# db.commit()
	# db.refresh(to_add_input)

	return 0

def retrieve_input_list(db, ticket_id):
	stmt = select(InputList).where(InputList.id == ticket_id)
	result = db.execute(stmt)
	existing_input_list = result.scalars().first()
	if existing_input_list is None:
		return None
	#print(existing_input_list.data)
	x = json.loads(existing_input_list.data)
	# print(type(x))
	return x