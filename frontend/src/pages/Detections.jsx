import { useEffect, useMemo, useState } from "react";
import { getBotDetections } from "../api";

function Detections() {
    const [detectionData, setDetectionData] = useState(null);

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const [search, setSearch] = useState("");
    const [showBotsOnly, setShowBotsOnly] = useState(false);


    // --------------------------------------------------
    // Load bot detection results
    // --------------------------------------------------

    useEffect(() => {

        async function loadDetections() {

            try {

                setLoading(true);
                setError(null);

                const data = await getBotDetections();

                console.log(
                    "Bot detection data received:",
                    data
                );

                setDetectionData(data);

            } catch (err) {

                console.error(
                    "Bot detection loading error:",
                    err
                );

                setError(err.message);

            } finally {

                setLoading(false);

            }
        }

        loadDetections();

    }, []);


    // --------------------------------------------------
    // Filter users
    // --------------------------------------------------

    const filteredUsers = useMemo(() => {

        if (!detectionData?.users) {
            return [];
        }

        const searchText = search
            .toLowerCase()
            .trim();

        return detectionData.users
            .filter((user) => {

                const matchesSearch =
                    !searchText ||
                    user.username
                        ?.toLowerCase()
                        .includes(searchText) ||
                    user.display_name
                        ?.toLowerCase()
                        .includes(searchText);

                const matchesBotFilter =
                    !showBotsOnly ||
                    user.is_bot === 1;

                return (
                    matchesSearch &&
                    matchesBotFilter
                );

            })
            .sort(
                (a, b) =>
                    (b.bot_probability || 0) -
                    (a.bot_probability || 0)
            );

    }, [
        detectionData,
        search,
        showBotsOnly
    ]);


    // --------------------------------------------------
    // Loading state
    // --------------------------------------------------

    if (loading) {

        return (
            <div className="page-loading">
                Running bot detection analysis...
            </div>
        );

    }


    // --------------------------------------------------
    // Error state
    // --------------------------------------------------

    if (error) {

        return (
            <div className="page-error">

                <h2>
                    Bot detection failed
                </h2>

                <p>
                    {error}
                </p>

            </div>
        );

    }


    // --------------------------------------------------
    // No data
    // --------------------------------------------------

    if (!detectionData) {

        return (
            <div className="page-error">
                No detection data available.
            </div>
        );

    }


    // --------------------------------------------------
    // Render
    // --------------------------------------------------

    return (
        <div className="dashboard-page">

            {/* ------------------------------------------ */}
            {/* Page Header */}
            {/* ------------------------------------------ */}

            <div className="page-header">

                <div>

                    <h1>
                        Detection Results
                    </h1>

                    <p>
                        AI-powered analysis of user behavior
                        for detecting suspicious and bot-like
                        accounts.
                    </p>

                </div>

            </div>


            {/* ------------------------------------------ */}
            {/* Summary Cards */}
            {/* ------------------------------------------ */}

            <div className="stats-grid">

                <div className="stat-card">

                    <div className="stat-label">
                        Total Users
                    </div>

                    <div className="stat-value">
                        {detectionData.total_users}
                    </div>

                </div>


                <div className="stat-card">

                    <div className="stat-label">
                        Detected Bots
                    </div>

                    <div className="stat-value">
                        {detectionData.bot_count}
                    </div>

                </div>


                <div className="stat-card">

                    <div className="stat-label">
                        Humans
                    </div>

                    <div className="stat-value">
                        {detectionData.human_count}
                    </div>

                </div>


                <div className="stat-card">

                    <div className="stat-label">
                        Bot Percentage
                    </div>

                    <div className="stat-value">
                        {detectionData.bot_percentage}%
                    </div>

                </div>

            </div>


            {/* ------------------------------------------ */}
            {/* Detection Overview */}
            {/* ------------------------------------------ */}

            <div className="data-table-container">

                <div className="page-header">

                    <div>

                        <h2>
                            Detection Overview
                        </h2>

                        <p>
                            Distribution of detected account types.
                        </p>

                    </div>

                </div>


                <div className="detection-distribution">

                    <div className="detection-bar">

                        <div
                            className="detection-bar-human"
                            style={{
                                width: `${
                                    detectionData.total_users > 0
                                        ? (
                                            detectionData.human_count /
                                            detectionData.total_users
                                        ) * 100
                                        : 0
                                }%`
                            }}
                        />

                        <div
                            className="detection-bar-bot"
                            style={{
                                width: `${
                                    detectionData.total_users > 0
                                        ? (
                                            detectionData.bot_count /
                                            detectionData.total_users
                                        ) * 100
                                        : 0
                                }%`
                            }}
                        />

                    </div>


                    <div className="detection-legend">

                        <span>
                            Human:{" "}
                            <strong>
                                {detectionData.human_count}
                            </strong>
                        </span>

                        <span>
                            Bot:{" "}
                            <strong>
                                {detectionData.bot_count}
                            </strong>
                        </span>

                    </div>

                </div>

            </div>


            {/* ------------------------------------------ */}
            {/* Search / Filters */}
            {/* ------------------------------------------ */}

            <div className="search-container">

                <input
                    type="text"
                    placeholder="Search username or display name..."
                    value={search}
                    onChange={(event) =>
                        setSearch(event.target.value)
                    }
                />


                <button
                    type="button"
                    onClick={() =>
                        setShowBotsOnly(!showBotsOnly)
                    }
                >
                    {showBotsOnly
                        ? "Show All Users"
                        : "Show Bots Only"}
                </button>

            </div>


            {/* ------------------------------------------ */}
            {/* Results Information */}
            {/* ------------------------------------------ */}

            <div className="page-header">

                <div>

                    <h2>
                        User Detection Results
                    </h2>

                    <p>
                        Showing{" "}
                        {filteredUsers.length}{" "}
                        of{" "}
                        {detectionData.total_users}{" "}
                        analyzed users.
                    </p>

                </div>

            </div>


            {/* ------------------------------------------ */}
            {/* Detection Table */}
            {/* ------------------------------------------ */}

            <div className="data-table-container">

                <table className="data-table">

                    <thead>

                        <tr>

                            <th>
                                Username
                            </th>

                            <th>
                                Display Name
                            </th>

                            <th>
                                Prediction
                            </th>

                            <th>
                                Human Probability
                            </th>

                            <th>
                                Bot Probability
                            </th>

                        </tr>

                    </thead>


                    <tbody>

                        {filteredUsers.map((user) => (

                            <tr key={user.user_id}>

                                <td>

                                    <strong>
                                        @{user.username}
                                    </strong>

                                </td>


                                <td>
                                    {user.display_name}
                                </td>


                                <td>

                                    {user.prediction === "Bot" ? (

                                        <span className="detection-badge bot">
                                            Bot
                                        </span>

                                    ) : (

                                        <span className="detection-badge human">
                                            Human
                                        </span>

                                    )}

                                </td>


                                <td>

                                    {(
                                        (user.human_probability || 0) *
                                        100
                                    ).toFixed(2)}
                                    %

                                </td>


                                <td>

                                    <strong>
                                        {(
                                            (user.bot_probability || 0) *
                                            100
                                        ).toFixed(2)}
                                        %
                                    </strong>

                                </td>

                            </tr>

                        ))}


                        {filteredUsers.length === 0 && (

                            <tr>

                                <td
                                    colSpan="5"
                                    className="empty-table"
                                >
                                    No users found.
                                </td>

                            </tr>

                        )}

                    </tbody>

                </table>

            </div>

        </div>
    );
}


export default Detections;