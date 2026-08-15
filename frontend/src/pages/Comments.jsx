import { useEffect, useState } from "react";
import { getComments } from "../api";


function Comments() {

    const [comments, setComments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [search, setSearch] = useState("");


    useEffect(() => {

        async function loadComments() {

            try {

                const data = await getComments();

                console.log(
                    "Comments data received:",
                    data
                );

                setComments(
                    data.comments || []
                );

            } catch (err) {

                console.error(
                    "Comments loading error:",
                    err
                );

                setError(err.message);

            } finally {

                setLoading(false);

            }
        }


        loadComments();

    }, []);


    const filteredComments = comments.filter(
        (comment) =>
            comment.text
                ?.toLowerCase()
                .includes(
                    search.toLowerCase()
                )
    );


    if (loading) {

        return (
            <div className="page-loading">
                Loading comments...
            </div>
        );

    }


    if (error) {

        return (
            <div className="page-error">
                Failed to load comments: {error}
            </div>
        );

    }


    return (

        <div className="dashboard-page">


            {/* -------------------------------------- */}
            {/* Page Header */}
            {/* -------------------------------------- */}

            <div className="page-header">

                <div>

                    <h1>
                        Comments
                    </h1>

                    <p>
                        Analyze comment activity and
                        spam indicators.
                    </p>

                </div>


                <div>

                    Showing{" "}
                    {filteredComments.length} of{" "}
                    {comments.length} comments

                </div>

            </div>


            {/* -------------------------------------- */}
            {/* Search */}
            {/* -------------------------------------- */}

            <div className="search-container">

                <input
                    type="text"
                    placeholder="Search comment content..."
                    value={search}
                    onChange={(event) =>
                        setSearch(
                            event.target.value
                        )
                    }
                />

            </div>


            {/* -------------------------------------- */}
            {/* Comments Table */}
            {/* -------------------------------------- */}

            <div className="data-table-container">

                <table className="data-table">

                    <thead>

                        <tr>

                            <th>
                                Comment
                            </th>

                            <th>
                                User ID
                            </th>

                            <th>
                                Post ID
                            </th>

                            <th>
                                Created
                            </th>

                        </tr>

                    </thead>


                    <tbody>

                        {filteredComments.map(
                            (comment) => (

                                <tr
                                    key={
                                        comment.id
                                    }
                                >

                                    <td>

                                        <div className="post-content">

                                            {comment.text}

                                        </div>

                                    </td>


                                    <td>

                                        <div className="secondary-text">

                                            {comment.user_id}

                                        </div>

                                    </td>


                                    <td>

                                        <div className="secondary-text">

                                            {comment.post_id}

                                        </div>

                                    </td>


                                    <td>

                                        {comment.created_at
                                            ? new Date(
                                                comment.created_at
                                            ).toLocaleString()
                                            : "—"}

                                    </td>

                                </tr>

                            )
                        )}

                    </tbody>

                </table>


                {filteredComments.length === 0 && (

                    <div className="empty-state">

                        No comments found.

                    </div>

                )}

            </div>

        </div>

    );
}


export default Comments;