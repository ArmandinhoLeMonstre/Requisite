import { useEffect, useState } from "react"
import { useParams, useNavigate } from "react-router-dom"
import { verifyUser } from "../api/client"

export const VerificationPage = () => {

	const { token } = useParams()
	const [status, setStatus] = useState("loading")
	const navigate = useNavigate()

	useEffect(() => {
		async function verify(token) {
			try {
				const res = await verifyUser(token)
				setStatus("success")
				setTimeout(() => navigate("/login"), 3000)
			} catch {
				setStatus("error")
			}
		}
		verify(token)
	}, [token])

	return (
		<div className="bg-gray-950">
			{status === "success" && (
				<div>
					<h2>Email verified</h2>
					<p>Redirection to login in 3 seconds</p>
				</div>
			)}
			{status === "error" && (
				<div>
					<h2>Invalid or expired link</h2>
				</div>
			)}
		</div>
	)
}