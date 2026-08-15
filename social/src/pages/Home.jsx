import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { supabase } from "../lib/supabase";
import { useEffect, useState } from "react";

import {
    getPosts,
    createPost,
    getPostComments,
    createComment,
    getCurrentUserProfile
} from "../api";


function Home() {

    const { user, session } = useAuth();
    const navigate = useNavigate();


    // --------------------------------------------------
    // Posts
    // --------------------------------------------------

    const [posts, setPosts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);


    // --------------------------------------------------
    // Create post
    // --------------------------------------------------

    const [postText, setPostText] = useState("");
    const [creatingPost, setCreatingPost] = useState(false);
    const [createPostError, setCreatePostError] = useState(null);


    // --------------------------------------------------
    // Comments
    // --------------------------------------------------

    const [expandedPost, setExpandedPost] = useState(null);

    const [comments, setComments] = useState({});

    const [commentText, setCommentText] = useState({});

    const [commentLoading, setCommentLoading] = useState({});

    const [commentSubmitting, setCommentSubmitting] = useState({});

    const [commentError, setCommentError] = useState({});


    // --------------------------------------------------
    // Load posts
    // --------------------------------------------------

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


    // --------------------------------------------------
    // Create post
    // --------------------------------------------------

    async function handleCreatePost(event) {

        event.preventDefault();

        if (!postText.trim()) {
            return;
        }

        if (!session?.access_token) {

            setCreatePostError(
                "You are not authenticated."
            );

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


    // --------------------------------------------------
    // Load comments for a post
    // --------------------------------------------------

    async function handleViewComments(postId) {

        // If this post is already open,
        // close its comment section.
        if (expandedPost === postId) {

            setExpandedPost(null);

            return;
        }


        try {

            setExpandedPost(postId);

            setCommentLoading((prev) => ({
                ...prev,
                [postId]: true
            }));

            setCommentError((prev) => ({
                ...prev,
                [postId]: null
            }));


            const data = await getPostComments(postId);


            setComments((prev) => ({
                ...prev,
                [postId]: data.comments
            }));


        } catch (err) {

            setCommentError((prev) => ({
                ...prev,
                [postId]: err.message
            }));

        } finally {

            setCommentLoading((prev) => ({
                ...prev,
                [postId]: false
            }));

        }
    }


    // --------------------------------------------------
    // Submit comment
    // --------------------------------------------------

    async function handleSubmitComment(postId) {

        const text = commentText[postId]?.trim();


        if (!text) {
            return;
        }


        if (!session?.access_token) {

            setCommentError((prev) => ({
                ...prev,
                [postId]: "You are not authenticated."
            }));

            return;
        }


        try {

            setCommentSubmitting((prev) => ({
                ...prev,
                [postId]: true
            }));

            setCommentError((prev) => ({
                ...prev,
                [postId]: null
            }));


            // const newComment = await createComment(
            //     postId,
            //     text,
            //     session.access_token
            // );


            // // Immediately add the new comment
            // // to the currently displayed comments.
            // setComments((prev) => ({
            //     ...prev,
            //     [postId]: [
            //         ...(prev[postId] || []),
            //         newComment
            //     ]
            // }));

            await createComment(
    postId,
    text,
    session.access_token
);

const data = await getPostComments(postId);

setComments((prev) => ({
    ...prev,
    [postId]: data.comments
}));


            // Clear input.
            setCommentText((prev) => ({
                ...prev,
                [postId]: ""
            }));


        } catch (err) {

            setCommentError((prev) => ({
                ...prev,
                [postId]: err.message
            }));

        } finally {

            setCommentSubmitting((prev) => ({
                ...prev,
                [postId]: false
            }));

        }
    }


    // --------------------------------------------------
    // Load posts when page opens
    // --------------------------------------------------

    useEffect(() => {

        loadPosts();

    }, []);

    async function handleMyProfile() {

    if (!session?.access_token) {
        return;
    }

    try {

        const profile = await getCurrentUserProfile(
            session.access_token
        );

        navigate(`/profile/${profile.id}`);

    } catch (err) {

        console.error(
            "Failed to load own profile:",
            err
        );

    }
}
    // --------------------------------------------------
    // Logout
    // --------------------------------------------------

    async function handleLogout() {

        const { error } = await supabase.auth.signOut();


        if (error) {

            console.error(
                "Logout failed:",
                error.message
            );

            return;
        }


        navigate("/login", {
            replace: true
        });
    }


    // --------------------------------------------------
    // UI
    // --------------------------------------------------

    return (
        <div className="home-page">

            {/* ------------------------------------------ */}
            {/* Header */}
            {/* ------------------------------------------ */}

<header className="home-header">

    <div>

        <h1>
            TrustLens Social
        </h1>

        <p>
            Welcome,{" "}
            {user?.user_metadata?.display_name ||
                user?.email}
        </p>

    </div>


    <div className="home-header-actions">

        <button onClick={handleMyProfile}>
            Profile
        </button>

        <button onClick={handleLogout}>
            Logout
        </button>

    </div>

</header>


            <main className="feed-container">


                {/* -------------------------------------- */}
                {/* Create Post */}
                {/* -------------------------------------- */}

                <section className="create-post-section">

                    <h2>
                        Create a Post
                    </h2>


                    <form onSubmit={handleCreatePost}>

                        <textarea
                            value={postText}
                            onChange={(event) =>
                                setPostText(
                                    event.target.value
                                )
                            }
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
                                {creatingPost
                                    ? "Posting..."
                                    : "Post"}
                            </button>

                        </div>

                    </form>


                    {createPostError && (

                        <div className="feed-error">

                            {createPostError}

                        </div>

                    )}

                </section>


                {/* -------------------------------------- */}
                {/* Feed Header */}
                {/* -------------------------------------- */}

                <section className="feed-header">

                    <h2>
                        Home Feed
                    </h2>

                    <p>
                        Recent posts from the TrustLens
                        social environment.
                    </p>

                </section>


                {/* -------------------------------------- */}
                {/* Loading */}
                {/* -------------------------------------- */}

                {loading && (

                    <div className="feed-state">
                        Loading posts...
                    </div>

                )}


                {/* -------------------------------------- */}
                {/* Feed Error */}
                {/* -------------------------------------- */}

                {error && (

                    <div className="feed-error">

                        Failed to load posts: {error}

                    </div>

                )}


                {/* -------------------------------------- */}
                {/* Empty Feed */}
                {/* -------------------------------------- */}

                {!loading &&
                    !error &&
                    posts.length === 0 && (

                        <div className="feed-state">
                            No posts available.
                        </div>

                    )}


                {/* -------------------------------------- */}
                {/* Posts */}
                {/* -------------------------------------- */}

                <section className="posts-list">

                    {!loading &&
                        !error &&
                        posts.map((post) => (

                            <article
                                className="post-card"
                                key={post.id}
                            >


                                {/* ---------------------- */}
                                {/* Post Author */}
                                {/* ---------------------- */}

                                <div className="post-author">

    {post.users?.id ? (

        <button
            className="post-author-button"
            onClick={() =>
                navigate(`/profile/${post.users.id}`)
            }
        >
            <strong>
                @{post.users?.username || "unknown"}
            </strong>

            <span>
                {post.users?.display_name ||
                    "Unknown User"}
            </span>
        </button>

    ) : (

        <>
            <strong>
                @{post.users?.username || "unknown"}
            </strong>

            <span>
                {post.users?.display_name ||
                    "Unknown User"}
            </span>
        </>

    )}

</div>


                                {/* ---------------------- */}
                                {/* Post Content */}
                                {/* ---------------------- */}

                                <div className="post-content">

                                    {post.text}

                                </div>


                                {/* ---------------------- */}
                                {/* Post Metadata */}
                                {/* ---------------------- */}

                                <div className="post-meta">

                                    {post.contexts && (

                                        <span>
                                            {
                                                post.contexts
                                                    .context_name
                                            }
                                        </span>

                                    )}


                                    <span>

                                        {new Date(
                                            post.created_at
                                        ).toLocaleString()}

                                    </span>

                                </div>


                                {/* ---------------------- */}
                                {/* Comments Button */}
                                {/* ---------------------- */}

                                <button
                                    className="comments-button"
                                    onClick={() =>
                                        handleViewComments(
                                            post.id
                                        )
                                    }
                                >

                                    {expandedPost === post.id
                                        ? "Hide comments"
                                        : "View comments"}

                                </button>


                                {/* ---------------------- */}
                                {/* Comments Section */}
                                {/* ---------------------- */}

                                {expandedPost === post.id && (

                                    <div className="comments-section">


                                        {/* Loading */}

                                        {commentLoading[
                                            post.id
                                        ] && (

                                            <div className="comments-state">

                                                Loading comments...

                                            </div>

                                        )}


                                        {/* Error */}

                                        {commentError[
                                            post.id
                                        ] && (

                                            <div className="comments-error">

                                                {
                                                    commentError[
                                                        post.id
                                                    ]
                                                }

                                            </div>

                                        )}


                                        {/* No comments */}

                                        {!commentLoading[
                                            post.id
                                        ] &&
                                            !commentError[
                                                post.id
                                            ] &&
                                            comments[
                                                post.id
                                            ]?.length === 0 && (

                                                <div className="comments-state">

                                                    No comments yet.

                                                </div>

                                            )}


                                        {/* Existing comments */}

                                        {!commentLoading[
                                            post.id
                                        ] &&
                                            comments[
                                                post.id
                                            ]?.map(
                                                (comment) => (

                                                    <div
                                                        className="comment-item"
                                                        key={
                                                            comment.id
                                                        }
                                                    >

                                                       <div className="comment-author">

    <strong>
        @{comment.users?.username || "unknown"}
    </strong>

    <span>
        {comment.users?.display_name || "Unknown User"}
    </span>

</div>


                                                        <div className="comment-text">

                                                            {
                                                                comment.text
                                                            }

                                                        </div>


                                                        <div className="comment-time">

                                                            {new Date(
                                                                comment.created_at
                                                            ).toLocaleString()}

                                                        </div>

                                                    </div>

                                                )
                                            )}


                                        {/* ------------------ */}
                                        {/* New Comment Form */}
                                        {/* ------------------ */}

                                        <div className="comment-form">

                                            <input
                                                type="text"
                                                placeholder="Write a comment..."
                                                value={
                                                    commentText[
                                                        post.id
                                                    ] || ""
                                                }
                                                maxLength="500"
                                                onChange={(
                                                    event
                                                ) =>
                                                    setCommentText(
                                                        (prev) => ({
                                                            ...prev,
                                                            [post.id]:
                                                                event
                                                                    .target
                                                                    .value
                                                        })
                                                    )
                                                }
                                                onKeyDown={(
                                                    event
                                                ) => {

                                                    if (
                                                        event.key ===
                                                        "Enter"
                                                    ) {

                                                        event.preventDefault();

                                                        handleSubmitComment(
                                                            post.id
                                                        );

                                                    }

                                                }}
                                            />


                                            <button
                                                onClick={() =>
                                                    handleSubmitComment(
                                                        post.id
                                                    )
                                                }
                                                disabled={
                                                    commentSubmitting[
                                                        post.id
                                                    ] ||
                                                    !commentText[
                                                        post.id
                                                    ]?.trim()
                                                }
                                            >

                                                {commentSubmitting[
                                                    post.id
                                                ]
                                                    ? "Posting..."
                                                    : "Comment"}

                                            </button>

                                        </div>


                                    </div>

                                )}

                            </article>

                        ))}

                </section>

            </main>

        </div>
    );
}


export default Home;