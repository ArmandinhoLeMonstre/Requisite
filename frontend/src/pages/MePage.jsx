import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { getMe } from "../api/client";

export const MePage = () => {
	const [user, setUser] = useState(null);
	const navigate = useNavigate();

	useEffect(() => {
		async function loadUser() {
			const token = localStorage.getItem("token");

			if (!token) {
				navigate("/login")
				return ;
			}

			const res = await getMe()

			if (res.status === 401) {
				localStorage.removeItem("token");
				navigate("/login");
			}

			const data = await res.data;
			setUser(data);
		}
		loadUser();
	}, []);

	if (!user) return <p>Loading...</p>;

	return (
		<div className="min-h-screen flex items-center justify-center">
			<div className="flex flex-col gap-2">
				<p>Name: {user.name}</p>
			</div>
		</div>
	)
}