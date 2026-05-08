import { useState } from "react";
import { useNavigate } from "react-router-dom";

export const RegisterPage = () => {
	const [name, setName] = useState("");
	const [email, setEmail] = useState("");
	const [role, setRole] = useState("");
	const [password, setPassword] = useState("")

	const navigate = useNavigate();

	async function handleClick() {
		const res = await fetch("http://localhost:8080/api/users", {
			method: "POST",
			headers: { "Content-type": "application/json" },
			body: JSON.stringify({ name, email, role, password}),
		});

		const data = await res.json();

		if (res.status === 201) {
			navigate("/login");
		}
	};

	return (
		<div className="min-h-screen bg-white flex items-center justify-center">
			<div className="bg-gray-950 py-20 px-5 flex flex-col rounded-2xl gap-3 w-80 shadow-md">
				<div className="flex flex-col">
					<label className="text-white text-sm">Name</label>
					<input
						type="text"
						value={name}
						onChange={(e) => setName(e.target.value)}
						className="border rounded-lg px-3 py-2 text-sm"
					/>
				</div>
				<div className="flex flex-col">
					<label className="text-white text-sm">Email</label>
					<input
						type="text"
						value={email}
						onChange={(e) => setEmail(e.target.value)}
						className="border rounded-lg px-3 py-2 text-sm"
					/>
				</div>
				<div className="flex flex-col">
					<label className="text-white text-sm">Role</label>
					<input
						type="text"
						value={role}
						onChange={(e) => setRole(e.target.value)}
						className="border rounded-lg px-3 py-2 text-sm"
					/>
				</div>
				<div className="flex flex-col">
					<label className="text-white text-sm">Password</label>
					<input
						type="password"
						value={password}
						onChange={(e) => setPassword(e.target.value)}
						className="border rounded-lg px-3 py-2 text-sm"
					/>
				</div>
				<button 
					onClick={handleClick}
					className="bg-gray-600 text-white rounded-lg py-2 text-sm"
				>
					Submit
				</button>
			</div>
		</div>
	)
}