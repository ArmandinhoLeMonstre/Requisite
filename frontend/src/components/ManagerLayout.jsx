import { Link, Outlet, useNavigate } from "react-router-dom";

export const ManagerLayout = () => {
  const navigate = useNavigate();

  function handleLogout() {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    navigate("/login");
  }

  return (
    <div className="h-screen bg-gray-950 overflow-hidden">
      <nav className="flex flex-row fixed top-0 left-0 right-0 z-10 h-16 border border-white justify-center items-center gap-20 text-2xl">
        <span className="text-white">Requisite</span>
        <div className=" text-white">
          <Link to="/manager/requests">Requests</Link>
        </div>
        <button
          className="text-white"
          onClick={() => handleLogout()}
        >
          Logout
        </button>
      </nav>
      <main className="pt-16">
          <Outlet />
        </main>
    </div>
  );
};
