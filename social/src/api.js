const API_BASE_URL = "http://127.0.0.1:8000";

export async function getPosts(limit = 20, offset = 0) {
    const response = await fetch(
        `${API_BASE_URL}/api/posts/?limit=${limit}&offset=${offset}`
    );

    if (!response.ok) {
        throw new Error("Failed to fetch posts");
    }

    return response.json();
}


export async function createPost(text, accessToken) {
    const response = await fetch(
        `${API_BASE_URL}/api/posts/`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${accessToken}`,
            },
            body: JSON.stringify({
                text: text,
            }),
        }
    );

    if (!response.ok) {
        const errorData = await response.json();

        throw new Error(
            errorData.detail || "Failed to create post"
        );
    }

    return response.json();
}


export async function getPostComments(postId) {
    const response = await fetch(
        `${API_BASE_URL}/api/posts/${postId}/comments`
    );

    if (!response.ok) {
        throw new Error("Failed to fetch comments");
    }

    return response.json();
}


export async function createComment(postId, text, accessToken) {
    const response = await fetch(
        `${API_BASE_URL}/api/comments/`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${accessToken}`,
            },
            body: JSON.stringify({
                post_id: postId,
                text: text,
            }),
        }
    );

    if (!response.ok) {
        const errorData = await response.json();

        throw new Error(
            errorData.detail || "Failed to create comment"
        );
    }

    return response.json();
}


export async function getUser(userId) {
    const response = await fetch(
        `${API_BASE_URL}/api/users/${userId}`
    );

    if (!response.ok) {

        const errorData = await response.json();

        throw new Error(
            errorData.detail || "Failed to fetch user"
        );
    }

    return response.json();
}


export async function getFollowers(userId) {
    const response = await fetch(
        `${API_BASE_URL}/api/users/${userId}/followers`
    );

    if (!response.ok) {

        const errorData = await response.json();

        throw new Error(
            errorData.detail || "Failed to fetch followers"
        );
    }

    return response.json();
}


export async function getFollowing(userId) {
    const response = await fetch(
        `${API_BASE_URL}/api/users/${userId}/following`
    );

    if (!response.ok) {

        const errorData = await response.json();

        throw new Error(
            errorData.detail || "Failed to fetch following"
        );
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