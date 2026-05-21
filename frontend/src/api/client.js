import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8080/api",
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      const publicRoutes = ["/login", "/register"];
      if (!publicRoutes.includes(window.location.pathname)) {
        localStorage.removeItem("token");
        localStorage.removeItem("role");
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  },
);

function getToken() {
  return localStorage.getItem("token");
}

function authHeaders() {
  return {
    "Content-type": "application/json",
    Authorization: `Bearer ${getToken()}`,
  };
}

export async function getChats(ticketId) {
  const header = authHeaders();

  try {
    const response = await api.get(`/tickets/${ticketId}/chats`, {
      headers: header,
    });
    return response.data;
  } catch (error) {
    console.error(error);
    throw error;
  }
}

export async function sendMessage(ticketId, message) {
  const header = authHeaders();
  const body = { sender: "user", message };

  try {
    const response = await api.post(`/tickets/${ticketId}`, body, {
      headers: header,
    });
    return response.data;
  } catch (error) {
    console.error(error);
    throw error;
  }
}

export async function createTicket(user_message) {
  const header = authHeaders();
  const body = { user_message };

  try {
    const response = await api.post("/tickets", body, { headers: header });
    return response.data;
  } catch (error) {
    console.error(error);
    throw error;
  }
}

export async function getTicket(ticket_id) {
  const header = authHeaders();

  try {
    const response = await api.get(`/tickets/${ticket_id}`, {
      headers: header,
    });
    return response;
  } catch (error) {
    console.error(error);
    throw error;
  }
}

export async function getTickets() {
  const header = authHeaders();

  try {
    const response = await api.get("/tickets", { headers: header });
    return response.data;
  } catch (error) {
    console.error(error);
    throw error;
  }
}

export async function changeTicketStatus(ticket_id, status) {
  const header = authHeaders();

  try {
    const response = await api.patch(`/tickets/${ticket_id}/status`, null, {
      headers: header,
      params: { status },
    });
    return response;
  } catch (error) {
    console.error(error);
    throw error;
  }
}

export async function getGroupTickets() {
  const header = authHeaders();

  try {
    const response = await api.get("/tickets/manager", { headers: header });
    return response.data;
  } catch (error) {
    console.error(error);
    throw error;
  }
}

export async function createToken(email, password) {
  const formData = new FormData();
  formData.append("username", email);
  formData.append("password", password);

  try {
    const response = await api.post("/users/token", formData);
    return response.data;
  } catch (error) {
    console.error(error);
    throw error;
  }
}

export async function createUser(name, email, role, password) {
  const header = authHeaders();
  const body = { name, email, role, password };

  try {
    const response = await api.post("/users", body, { headers: header });
    return response.data;
  } catch (error) {
    console.error(error);
    throw error;
  }
}

export async function verifyUser(token) {
  const header = authHeaders();

  try {
    const response = await api.get(`/users/verification/${token}`);
    return response;
  } catch (error) {
    console.error(error);
    throw error;
  }
}

export async function getMe() {
  const header = authHeaders();

  try {
    const response = await api.get("/users/me", { headers: header });
    return response;
  } catch (error) {
    console.error(error);
    throw error;
  }
}

export async function createGroup() {
  const header = authHeaders();

  try {
    const response = await api.post("/groups", null, { headers: header });
    return response.data;
  } catch (error) {
    console.error(error);
    throw error;
  }
}

export async function joinGroup(user_id, code) {
  const header = authHeaders();

  try {
    const response = await api.patch(`/users/${user_id}/group`, null, {
      headers: header,
      params: { code },
    });
    return response;
  } catch (error) {
    console.error(error);
    throw error;
  }
}

export async function getGroup(group_id) {
  const header = authHeaders();

  try {
    const reponse = await api.get(`/groups/${group_id}`, { headers: header });
    return reponse;
  } catch (error) {
    console.error(error);
    throw error;
  }
}

export async function getCommonItems() {
  const header = authHeaders();

  try {
    const response = await api.get("/inventory/common", { headers: header });
    return response.data;
  } catch (error) {
    console.error(error);
    throw error;
  }
}

export async function getManagerItems() {
  const header = authHeaders();

  try {
    const response = await api.get("/inventory/manager", { headers: header });
    return response.data;
  } catch (error) {
    console.error(error);
    throw error;
  }
}

export async function addInventoryItemns(title, objectType, objectSpecs, quantity) {
	const header = authHeaders();
	const body = { title, object_type: objectType, object_specs: objectSpecs, quantity };

	try {
	const response = await api.post("/inventory/add", body, { headers: header });
	return response.data;
	} catch (error) {
	console.error(error);
	throw error;
	}
}