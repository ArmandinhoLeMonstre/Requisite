import { useEffect, useState } from "react";
import {
  getCommonItems,
  getManagerItems,
  addInventoryItems,
  deleteInventoryItems,
} from "../api/client";

export const InventoryPage = () => {
  const [commonItems, setCommonItems] = useState([]);
  const [managerItems, setManagerItems] = useState([]);
  const [title, setTitle] = useState("");
  const [objectType, setObjectType] = useState("");
  const [objectSpecs, setObjectSpecs] = useState("");
  const [quantity, setQuantity] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  async function fetchItems() {
    try {
      const comItems = await getCommonItems();
      const ManagerItems = await getManagerItems();
      setCommonItems(comItems);
      setManagerItems(ManagerItems);
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    fetchItems();
  }, []);

  async function addObject() {
    try {
      await addInventoryItems(title, objectType, objectSpecs, quantity);
      await fetchItems();
      setObjectSpecs("");
      setObjectType("");
      setQuantity("");
      setTitle("");
    } catch (error) {
      console.error(error);
    }
  }

  async function deleteObject(item_id) {
	try {
      await deleteInventoryItems(item_id);
      await fetchItems();

    } catch (error) {
      console.error(error);
    }
  }
  if (isLoading)
    return (
      <div className="flex h-screen items-center justify-center bg-gray-950">
        <div className="w-6 h-6 rounded-full border-2 border-gray-600 border-t-white animate-spin" />
      </div>
    );
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
        {commonItems.map((item) => (
          <li
            key={item.id}
            className="flex items-center gap-4 bg-gray-900 border border-gray-800 px-4 py-3 rounded-lg opacity-70"
          >
            <span className="text-gray-500 text-sm">🔒</span>
            <span className="text-white text-sm flex-1 truncate">
              {item.title}
            </span>
            <span className="text-gray-400 text-xs bg-gray-800 px-2 py-1 rounded w-24 text-center truncate">
              {item.object_type}
            </span>
            <span className="text-gray-400 text-xs w-40 truncate">
              {item.object_specs}
            </span>
            <span className="text-gray-500 text-xs w-8 text-right">
              x{item.quantity}
            </span>
          </li>
        ))}
      </ul>

      <p className="text-gray-500 text-xs uppercase tracking-widest mb-2 mt-6">
        Your items
      </p>

      <ul className="flex flex-col gap-2 w-full">
        {managerItems.map((item) => (
          <li
            key={item.id}
            className="flex items-center gap-4 bg-gray-900 border border-gray-700 px-4 py-3 rounded-lg"
          >
            <span className="text-white text-sm flex-1 truncate">
              {item.title}
            </span>
            <span className="text-gray-400 text-xs bg-gray-800 px-2 py-1 rounded w-24 text-center truncate">
              {item.object_type}
            </span>
            <span className="text-gray-400 text-xs w-40 truncate">
              {item.object_specs}
            </span>
            <span className="text-gray-500 text-xs w-8 text-right">
              x{item.quantity}
            </span>
			<button
				onClick={() => deleteObject(item.id)}
				className="text-gray-500 hover:text-red-500 transition-colors ml-2"
				aria-label="Delete item"
			>
				<svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
				<polyline points="3 6 5 6 21 6" />
				<path d="M19 6l-1 14H6L5 6" />
				<path d="M10 11v6M14 11v6" />
				<path d="M9 6V4h6v2" />
				</svg>
			</button>
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
  );
};
