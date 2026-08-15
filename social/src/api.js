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

// export async function createPost(text, accessToken) {
//     const response = await fetch(
//         `${API_BASE_URL}/api/posts/`,
//         {
//             method: "POST",
//             headers: {
//                 "Content-Type": "application/json",
//                 "Authorization": `Bearer ${accessToken}`,
//             },
//             body: JSON.stringify({
//                 text: text,
//             }),
//         }
//     );

//     const responseText = await response.text();

//     console.log("Create post status:", response.status);
//     console.log("Create post response:", responseText);

//     if (!response.ok) {
//         throw new Error(
//             `Create post failed (${response.status}): ${responseText}`
//         );
//     }

//     return JSON.parse(responseText);
// }

export async function checkBackendHealth() {
    const response = await fetch(
        `${API_BASE_URL}/health`
    );

    if (!response.ok) {
        throw new Error("Backend health check failed");
    }

    return response.json();
}