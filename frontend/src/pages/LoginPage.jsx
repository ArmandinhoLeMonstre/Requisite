import { useState } from "react";
import { useNavigate } from "react-router-dom";

export const LoginPage = () => {
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("")
	const navigate = useNavigate();

	async function handleClick() {
		const formData = new FormData();
		formData.append("username", email);
		formData.append("password", password);
		try {
			const res = await fetch("http://localhost:8080/api/users/token", {
				method: "POST",
				body: formData,
			});
			const data = await res.json();
			localStorage.setItem("token", data.access_token);
			navigate("/chat");

		} catch (error) {
			console.log(error)
			return ;
		}
	}

	return (
		<div className="min-h-screen bg-white flex items-center justify-center">
			<div className="bg-gray-950 py-20 px-5 flex flex-col rounded-2xl gap-3 w-80 shadow-md">
				<div className="flex flex-col text-white">
					<label className="text-white text-sm">Email</label>
					<input
						type="email"
						value={email}
						onChange={(e) => setEmail(e.target.value)}
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
	);
}