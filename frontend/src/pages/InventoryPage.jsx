import { useEffect, useState } from "react"
import { getCommonItems, getManagerItems } from "../api/client"

export const InventoryPage = () => {

	const [commonItems, setCommonItems] = useState([])
	const [managerItems, setManagerItems] = useState([])

	useEffect(() => {
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
		fetchItems()
	}, [])

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

		</div>
	)
}