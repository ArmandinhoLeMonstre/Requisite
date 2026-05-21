import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error),
);

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

export async function getChats(ticketId) {
  try {
    const response = await api.get(`/tickets/${ticketId}/chats`);
    return response.data;
  } catch (error) {
    console.error(error);
    throw error;
  }
}

export async function sendMessage(ticketId, message) {
  const body = { sender: "user", message };

  try {
    const response = await api.post(`/tickets/${ticketId}`, body);
    return response.data;
  } catch (error) {
    console.error(error);
    throw error;
  }
}

export async function createTicket(user_message) {
  const body = { user_message };

  try {
    const response = await api.post("/tickets", body);
    return response.data;
  } catch (error) {
    console.error(error);
    throw error;
  }
}

export async function getTicket(ticket_id) {
  try {
    const response = await api.get(`/tickets/${ticket_id}`);
    return response;
  } catch (error) {
    console.error(error);
    throw error;
  }
}

export async function getTickets() {
  try {
    const response = await api.get("/tickets");
    return response.data;
  } catch (error) {
    console.error(error);
    throw error;
  }
}

export async function changeTicketStatus(ticket_id, status) {
  try {
    const response = await api.patch(`/tickets/${ticket_id}/status`, null, {
      params: { status },
    });
    return response;
  } catch (error) {
    console.error(error);
    throw error;
  }
}

export async function getGroupTickets() {
  try {
    const response = await api.get("/tickets/manager");
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
  const body = { name, email, role, password };

  try {
    const response = await api.post("/users", body);
    return response.data;
  } catch (error) {
    console.error(error);
    throw error;
  }
}

export async function verifyUser(token) {
  try {
    const response = await api.get(`/users/verification/${token}`);
    return response;
  } catch (error) {
    console.error(error);
    throw error;
  }
}

export async function getMe() {
  try {
    const response = await api.get("/users/me");
    return response;
  } catch (error) {
    console.error(error);
    throw error;
  }
}

export async function createGroup() {
  try {
    const response = await api.post("/groups", null);
    return response.data;
  } catch (error) {
    console.error(error);
    throw error;
  }
}

export async function joinGroup(user_id, code) {
  try {
    const response = await api.patch(`/users/${user_id}/group`, null, {
      params: { code },
    });
    return response;
  } catch (error) {
    console.error(error);
    throw error;
  }
}

export async function getGroup(group_id) {
  try {
    const reponse = await api.get(`/groups/${group_id}`);
    return reponse;
  } catch (error) {
    console.error(error);
    throw error;
  }
}

export async function getCommonItems() {
  try {
    const response = await api.get("/inventory/common");
    return response.data;
  } catch (error) {
    console.error(error);
    throw error;
  }
}

export async function getManagerItems() {
  try {
    const response = await api.get("/inventory/manager");
    return response.data;
  } catch (error) {
    console.error(error);
    throw error;
  }
}

export async function addInventoryItems(
  title,
  objectType,
  objectSpecs,
  quantity,
) {
  const body = {
    title,
    object_type: objectType,
    object_specs: objectSpecs,
    quantity,
  };

  try {
    const response = await api.post("/inventory/add", body);
    return response.data;
  } catch (error) {
    console.error(error);
    throw error;
  }
}
