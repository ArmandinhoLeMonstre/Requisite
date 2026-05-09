import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8080/api",
});

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

export async function createTicket() {
  const header = authHeaders();

  try {
    const response = await api.post("/tickets", null, { headers: header });
    return response.data;
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

export async function getMe() {
  const header = authHeaders();

  try {
    const response = await api.get("/users/me", { headers: header });
    return response.data;
  } catch (error) {
    console.error(error);
    throw error;
  }
}
