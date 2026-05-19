import { useEffect, useState } from "react"
import { getCommonItems, getManagerItems, addInventoryItemns } from "../api/client"

export const InventoryPage = () => {

	const [commonItems, setCommonItems] = useState([])
	const [managerItems, setManagerItems] = useState([])
	const [title, setTitle] = useState("")
	const [objectType, setObjectType] = useState("")
	const [objectSpecs, setObjectSpecs] = useState("")
	const [quantity, setQuantity] = useState("")

	async function fetchItems() {
		try {
			const CommonItems = await getCommonItems()
			const ManagerItems = await getManagerItems()
			setCommonItems(CommonItems)
			setManagerItems(ManagerItems)
		} catch (error) {
			console.log(error)
		}
	}

	useEffect(() => {
		fetchItems()
	}, [])

	async function addObject() {
		try {
			await addInventoryItemns(title, objectType, objectSpecs, quantity);
			await fetchItems()
		} catch (error) {
			console.log(error)
		}
	}
	return (
		<div className="flex flex-col p-8 min-h-screen bg-gray-950">

			<div className="flex items-center justify-between mb-6">
				<h1 className="text-white text-xl font-medium">Inventory</h1>
				<div className="flex items-center gap-2">
					<span className="text-gray-400 text-sm bg-gray-800 px-3 py-1 rounded-md">
						{commonItems.length} common items
					</span>
					<span className="text-gray-400 text-sm bg-gray-800 px-3 py-1 rounded-md">
						{managerItems.length} / 3 your items
					</span>
				</div>
			</div>

			<p className="text-gray-500 text-xs uppercase tracking-widest mb-2">
				Common items
			</p>

			<ul className="flex flex-col gap-2 w-full">
				{commonItems.map((item, index) => (
					<li key={index} className="flex items-center gap-4 bg-gray-900 border border-gray-800 px-4 py-3 rounded-lg opacity-70">
						<span className="text-gray-500 text-sm">🔒</span>
						<span className="text-white text-sm flex-1 truncate">{item.title}</span>
						<span className="text-gray-400 text-xs bg-gray-800 px-2 py-1 rounded w-24 text-center truncate">{item.object_type}</span>
						<span className="text-gray-400 text-xs w-40 truncate">{item.object_specs}</span>
						<span className="text-gray-500 text-xs w-8 text-right">x{item.available}</span>
					</li>
				))}
			</ul>

			

			<p className="text-gray-500 text-xs uppercase tracking-widest mb-2 mt-6">
				Your items
			</p>

			<ul className="flex flex-col gap-2 w-full">
				{managerItems.map((item, index) => (
					<li key={index} className="flex items-center gap-4 bg-gray-900 border border-gray-700 px-4 py-3 rounded-lg">
						<span className="text-white text-sm flex-1 truncate">{item.title}</span>
						<span className="text-gray-400 text-xs bg-gray-800 px-2 py-1 rounded w-24 text-center truncate">{item.object_type}</span>
						<span className="text-gray-400 text-xs w-40 truncate">{item.object_specs}</span>
						<span className="text-gray-500 text-xs w-8 text-right">x{item.available}</span>
					</li>
				))}
			</ul>
			<div className="flex items-center gap-3 border border-dashed border-gray-700 px-4 py-3 rounded-lg mt-6">
				<input 
					type="text" 
					placeholder="Title"
					value={title}
					onChange={(e) => setTitle(e.target.value)}
					className="bg-gray-800 text-white text-sm px-3 py-1.5 rounded flex-1 border border-gray-700 placeholder-gray-600 focus:outline-none"
				/>
				<input 
					type="text" 
					placeholder="Object Type"
					value={objectType}
					onChange={(e) => setObjectType(e.target.value)}
					className="bg-gray-800 text-white text-sm px-3 py-1.5 rounded flex-1 border border-gray-700 placeholder-gray-600 focus:outline-none"
				/>
				<input 
					type="text" 
					placeholder="Specs"
					value={objectSpecs}
					onChange={(e) => setObjectSpecs(e.target.value)}
					className="bg-gray-800 text-white text-sm px-3 py-1.5 rounded flex-1 border border-gray-700 placeholder-gray-600 focus:outline-none"
				/>
				<input 
					type="number" 
					placeholder="Quantity"
					value={quantity}
					onChange={(e) => setQuantity(e.target.value)}
					className="bg-gray-800 text-white text-sm px-3 py-1.5 rounded flex-1 border border-gray-700 placeholder-gray-600 focus:outline-none"
				/>
				<button
					onClick={addObject}
					className="bg-gray-600 hover:bg-gray-500 text-white rounded-lg py-2 text-sm disabled:bg-gray-950 disabled:border disabled:border-gray-500"
				>
				Submit
				</button>
			</div>
		</div>
	)
}