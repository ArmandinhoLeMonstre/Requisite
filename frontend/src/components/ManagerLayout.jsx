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
      <nav className="flex flex-row fixed top-0 left-0 right-0 z-10 h-16 border border-white items-center">
        <div className="flex-1 flex justify-start pl-3">
          <span className="text-white text-2xl">Requisite</span>
        </div>
        <div className="flex flex-row gap-5 text-2xl">
          <div className="text-white">
            <Link to="/manager/requests">Requests</Link>
          </div>
          <div className="text-white">
            <Link to="/manager/requests">Inventory</Link>
          </div>
        </div>
        <div className="flex-1 flex justify-end pr-3">
          <button
            className="text-white text-2xl"
            onClick={() => handleLogout()}
          >
            Logout
          </button>
        </div>
      </nav>
      <main className="pt-16">
        <Outlet />
      </main>
    </div>
  );
};
