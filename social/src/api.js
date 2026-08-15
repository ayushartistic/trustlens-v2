const API_BASE_URL = "http://127.0.0.1:8000";


// ==================================================
// POSTS
// ==================================================

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


// ==================================================
// COMMENTS
// ==================================================

export async function getPostComments(postId) {
    const response = await fetch(
        `${API_BASE_URL}/api/posts/${postId}/comments`
    );

    if (!response.ok) {
        throw new Error("Failed to fetch comments");
    }

    return response.json();
}


export async function createComment(
    postId,
    text,
    accessToken
) {
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


// ==================================================
// USERS / PROFILES
// ==================================================

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


export async function getCurrentUserProfile(accessToken) {
    const response = await fetch(
        `${API_BASE_URL}/api/users/me`,
        {
            headers: {
                "Authorization": `Bearer ${accessToken}`,
            },
        }
    );

    if (!response.ok) {
        const errorData = await response.json();

        throw new Error(
            errorData.detail ||
            "Failed to fetch current user profile"
        );
    }

    return response.json();
}


// ==================================================
// FOLLOWERS / FOLLOWING
// ==================================================

export async function getFollowers(userId) {
    const response = await fetch(
        `${API_BASE_URL}/api/users/${userId}/followers`
    );

    if (!response.ok) {
        const errorData = await response.json();

        throw new Error(
            errorData.detail ||
            "Failed to fetch followers"
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
            errorData.detail ||
            "Failed to fetch following"
        );
    }

    return response.json();
}


// ==================================================
// FOLLOW / UNFOLLOW
// ==================================================

export async function getFollowingStatus(
    userId,
    accessToken
) {
    const response = await fetch(
        `${API_BASE_URL}/api/users/${userId}/following-status`,
        {
            headers: {
                "Authorization": `Bearer ${accessToken}`,
            },
        }
    );

    if (!response.ok) {
        const errorData = await response.json();

        throw new Error(
            errorData.detail ||
            "Failed to check following status"
        );
    }

    return response.json();
}


export async function followUser(
    userId,
    accessToken
) {
    const response = await fetch(
        `${API_BASE_URL}/api/users/${userId}/follow`,
        {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${accessToken}`,
            },
        }
    );

    if (!response.ok) {
        const errorData = await response.json();

        throw new Error(
            errorData.detail ||
            "Failed to follow user"
        );
    }

    return response.json();
}


export async function unfollowUser(
    userId,
    accessToken
) {
    const response = await fetch(
        `${API_BASE_URL}/api/users/${userId}/follow`,
        {
            method: "DELETE",
            headers: {
                "Authorization": `Bearer ${accessToken}`,
            },
        }
    );

    if (!response.ok) {
        const errorData = await response.json();

        throw new Error(
            errorData.detail ||
            "Failed to unfollow user"
        );
    }

    return response.json();
}


// ==================================================
// BACKEND HEALTH
// ==================================================

export async function checkBackendHealth() {
    const response = await fetch(
        `${API_BASE_URL}/health`
    );

    if (!response.ok) {
        throw new Error("Backend health check failed");
    }

    return response.json();
}