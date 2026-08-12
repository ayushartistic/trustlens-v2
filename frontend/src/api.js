const API_BASE_URL = "http://127.0.0.1:8000";

export async function getDashboardSummary() {
  const response = await fetch(
    `${API_BASE_URL}/api/dashboard/summary`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch dashboard summary");
  }

  return response.json();
}

export async function checkBackendHealth() {
  const response = await fetch(
    `${API_BASE_URL}/health`
  );

  if (!response.ok) {
    throw new Error("Backend health check failed");
  }

  return response.json();
}

export async function getUsers(limit = 50, offset = 0) {
  const response = await fetch(
    `${API_BASE_URL}/api/users?limit=${limit}&offset=${offset}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch users");
  }

  return response.json();
}

export async function getPosts(limit = 50, offset = 0) {
    const response = await fetch(
        `${API_BASE_URL}/api/posts/?limit=${limit}&offset=${offset}`
    );

    if (!response.ok) {
        throw new Error("Failed to fetch posts");
    }

    return response.json();
}