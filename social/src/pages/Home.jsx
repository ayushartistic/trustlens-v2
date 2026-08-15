import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { supabase } from "../lib/supabase";
import { useEffect, useState } from "react";
import { getPosts, createPost } from "../api";

function Home() {
    const { user,session } = useAuth();
    const navigate = useNavigate();

    const [posts, setPosts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [postText, setPostText] = useState("");
    const [creatingPost, setCreatingPost] = useState(false);
    const [createPostError, setCreatePostError] = useState(null);

    async function loadPosts() {
        try {
            setLoading(true);
            setError(null);

            const data = await getPosts();

            setPosts(data.posts);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }

    async function handleCreatePost(event) {
    event.preventDefault();

    if (!postText.trim()) {
        return;
    }

    if (!session?.access_token) {
        setCreatePostError("You are not authenticated.");
        return;
    }

    try {
        setCreatingPost(true);
        setCreatePostError(null);

        await createPost(
            postText,
            session.access_token
        );

        setPostText("");

        await loadPosts();

    } catch (err) {
        setCreatePostError(err.message);
    } finally {
        setCreatingPost(false);
    }
    }

    useEffect(() => {
        loadPosts();
    }, []);
    async function handleLogout() {
        const { error } = await supabase.auth.signOut();

        if (error) {
            console.error("Logout failed:", error.message);
            return;
        }

        navigate("/login", { replace: true });
    }

        return (
        <div className="home-page">

            <header className="home-header">
                <div>
                    <h1>TrustLens Social</h1>
                    <p>
                        Welcome, {user?.user_metadata?.display_name || user?.email}
                    </p>
                </div>

                <button onClick={handleLogout}>
                    Logout
                </button>
            </header>

            <main className="feed-container">
                <section className="create-post-section">

    <h2>Create a Post</h2>

    <form onSubmit={handleCreatePost}>

        <textarea
            value={postText}
            onChange={(event) => setPostText(event.target.value)}
            placeholder="What's happening?"
            rows="4"
            maxLength="1000"
        />

        <div className="create-post-footer">

            <span>
                {postText.length}/1000
            </span>

            <button
                type="submit"
                disabled={
                    creatingPost ||
                    !postText.trim()
                }
            >
                {creatingPost ? "Posting..." : "Post"}
            </button>

        </div>

    </form>

    {createPostError && (
        <div className="feed-error">
            {createPostError}
        </div>
    )}

</section>

                <section className="feed-header">
                    <h2>Home Feed</h2>
                    <p>
                        Recent posts from the TrustLens social environment.
                    </p>
                </section>

                {loading && (
                    <div className="feed-state">
                        Loading posts...
                    </div>
                )}

                {error && (
                    <div className="feed-error">
                        Failed to load posts: {error}
                    </div>
                )}

                {!loading && !error && posts.length === 0 && (
                    <div className="feed-state">
                        No posts available.
                    </div>
                )}

                <section className="posts-list">
                    {!loading &&
                        !error &&
                        posts.map((post) => (
                            <article
                                className="post-card"
                                key={post.id}
                            >
                                <div className="post-author">
                                    <strong>
                                        @{post.users?.username || "unknown"}
                                    </strong>

                                    <span>
                                        {post.users?.display_name || "Unknown User"}
                                    </span>
                                </div>

                                <div className="post-content">
                                    {post.text}
                                </div>

                                <div className="post-meta">
                                    {post.contexts && (
                                        <span>
                                            {post.contexts.context_name}
                                        </span>
                                    )}

                                    <span>
                                        {new Date(
                                            post.created_at
                                        ).toLocaleString()}
                                    </span>
                                </div>

                                <button className="comments-button">
                                    View comments
                                </button>
                            </article>
                        ))}
                </section>

            </main>

        </div>
    );
}

export default Home;