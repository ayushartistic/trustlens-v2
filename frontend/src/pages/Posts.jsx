import { useEffect, useState } from "react";
import { getPosts } from "../api";

function Posts() {
    const [posts, setPosts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [search, setSearch] = useState("");

    useEffect(() => {
        async function loadPosts() {
            try {
                const data = await getPosts();

                setPosts(data.posts || []);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        }

        loadPosts();
    }, []);

    const filteredPosts = posts.filter((post) =>
        post.text?.toLowerCase().includes(search.toLowerCase())
    );

    if (loading) {
        return <div className="page-loading">Loading posts...</div>;
    }

    if (error) {
        return (
            <div className="page-error">
                Failed to load posts: {error}
            </div>
        );
    }

    return (
        <div className="dashboard-page">

            <div className="page-header">
                <div>
                    <h1>Posts</h1>

                    <p>
                        Social-media posts and their associated contexts.
                    </p>
                </div>

                <div>
                    Showing {filteredPosts.length} of {posts.length} posts
                </div>
            </div>

            <div className="search-container">
                <input
                    type="text"
                    placeholder="Search post content..."
                    value={search}
                    onChange={(event) => setSearch(event.target.value)}
                />
            </div>

            <div className="data-table-container">

                <table className="data-table">

                    <thead>
                        <tr>
                            <th>Post</th>
                            <th>Author</th>
                            <th>Context</th>
                            <th>Created</th>
                        </tr>
                    </thead>

                    <tbody>

                        {filteredPosts.map((post) => (
                            <tr key={post.id}>

                                <td>
                                    <div className="post-content">
                                        {post.text}
                                    </div>
                                </td>

                                <td>
    {post.users ? (
        <div>
            <strong>@{post.users.username}</strong>
            <div className="secondary-text">
                {post.users.display_name}
            </div>
        </div>
    ) : (
        "Unknown user"
    )}
</td>

<td>
    {post.contexts
        ? (
            <div>
                <strong>{post.contexts.context_name}</strong>
                <div className="secondary-text">
                    {post.contexts.context_type}
                </div>
            </div>
        )
        : "—"
    }
</td>

                                <td>
                                    {new Date(
                                        post.created_at
                                    ).toLocaleString()}
                                </td>

                            </tr>
                        ))}

                    </tbody>

                </table>

                {filteredPosts.length === 0 && (
                    <div className="empty-state">
                        No posts found.
                    </div>
                )}

            </div>

        </div>
    );
}

export default Posts;