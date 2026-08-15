import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

import {
    getUser,
    getFollowers,
    getFollowing,
    getFollowingStatus,
    followUser,
    unfollowUser
} from "../api";


function Profile() {

    const { userId } = useParams();
    const navigate = useNavigate();

    const { session } = useAuth();


    // --------------------------------------------------
    // Profile
    // --------------------------------------------------

    const [profile, setProfile] = useState(null);

    const [followersCount, setFollowersCount] = useState(0);
    const [followingCount, setFollowingCount] = useState(0);


    // --------------------------------------------------
    // Follow state
    // --------------------------------------------------

    const [isFollowing, setIsFollowing] = useState(false);
    const [isSelf, setIsSelf] = useState(false);

    const [followLoading, setFollowLoading] = useState(false);
    const [followError, setFollowError] = useState(null);


    // --------------------------------------------------
    // Page state
    // --------------------------------------------------

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);


    // --------------------------------------------------
    // Load profile
    // --------------------------------------------------

    async function loadProfile() {

        try {

            setLoading(true);
            setError(null);
            setFollowError(null);


            // ------------------------------------------
            // Load profile
            // ------------------------------------------

            const profileData = await getUser(userId);

            setProfile(profileData);


            // ------------------------------------------
            // Load followers
            // ------------------------------------------

            try {

                const followersData =
                    await getFollowers(userId);

                setFollowersCount(
                    followersData.count
                );

            } catch (err) {

                console.error(
                    "Failed to load followers:",
                    err
                );

                setFollowersCount(0);
            }


            // ------------------------------------------
            // Load following
            // ------------------------------------------

            try {

                const followingData =
                    await getFollowing(userId);

                setFollowingCount(
                    followingData.count
                );

            } catch (err) {

                console.error(
                    "Failed to load following:",
                    err
                );

                setFollowingCount(0);
            }


            // ------------------------------------------
            // Load following status
            // ------------------------------------------

            if (session?.access_token) {

                try {

                    const followingStatus =
                        await getFollowingStatus(
                            userId,
                            session.access_token
                        );

                    setIsFollowing(
                        followingStatus.is_following
                    );

                    setIsSelf(
                        followingStatus.is_self
                    );

                } catch (err) {

                    console.error(
                        "Failed to load following status:",
                        err
                    );

                    setIsFollowing(false);
                    setIsSelf(false);
                }

            }

        } catch (err) {

            console.error(
                "Failed to load profile:",
                err
            );

            setError(err.message);

        } finally {

            setLoading(false);

        }
    }


    // --------------------------------------------------
    // Follow / Unfollow
    // --------------------------------------------------

    async function handleFollowToggle() {

        if (!session?.access_token) {

            setFollowError(
                "You are not authenticated."
            );

            return;
        }


        try {

            setFollowLoading(true);
            setFollowError(null);


            if (isFollowing) {

                // --------------------------------------
                // Unfollow
                // --------------------------------------

                await unfollowUser(
                    userId,
                    session.access_token
                );

                setIsFollowing(false);

                setFollowersCount(
                    (prev) => Math.max(0, prev - 1)
                );

            } else {

                // --------------------------------------
                // Follow
                // --------------------------------------

                await followUser(
                    userId,
                    session.access_token
                );

                setIsFollowing(true);

                setFollowersCount(
                    (prev) => prev + 1
                );
            }

        } catch (err) {

            console.error(
                "Follow action failed:",
                err
            );

            setFollowError(
                err.message
            );

        } finally {

            setFollowLoading(false);

        }
    }


    // --------------------------------------------------
    // Load profile when page opens
    // --------------------------------------------------

    useEffect(() => {

        loadProfile();

    }, [userId, session?.access_token]);


    // --------------------------------------------------
    // Loading state
    // --------------------------------------------------

    if (loading) {

        return (
            <div className="profile-page">

                <div className="profile-state">
                    Loading profile...
                </div>

            </div>
        );
    }


    // --------------------------------------------------
    // Profile loading error
    // --------------------------------------------------

    if (error) {

        return (
            <div className="profile-page">

                <div className="profile-error">
                    Failed to load profile: {error}
                </div>

                <button
                    onClick={() => navigate(-1)}
                >
                    Go Back
                </button>

            </div>
        );
    }


    // --------------------------------------------------
    // No profile
    // --------------------------------------------------

    if (!profile) {

        return (
            <div className="profile-page">

                <div className="profile-state">
                    User not found.
                </div>

                <button
                    onClick={() => navigate(-1)}
                >
                    Go Back
                </button>

            </div>
        );
    }


    // --------------------------------------------------
    // Profile UI
    // --------------------------------------------------

    return (
        <div className="profile-page">

            <header className="profile-header">

                <button
                    onClick={() => navigate(-1)}
                >
                    ← Back
                </button>

            </header>


            <main className="profile-container">

                <section className="profile-card">


                    {/* -------------------------------- */}
                    {/* Profile Image */}
                    {/* -------------------------------- */}

                    <div className="profile-image-container">

                        {profile.profile_image_url ? (

                            <img
                                src={
                                    profile.profile_image_url
                                }
                                alt={
                                    `${profile.display_name} profile`
                                }
                                className="profile-image"
                            />

                        ) : (

                            <div className="profile-image-placeholder">

                                {(
                                    profile.display_name ||
                                    profile.username ||
                                    "U"
                                )
                                    .charAt(0)
                                    .toUpperCase()}

                            </div>

                        )}

                    </div>


                    {/* -------------------------------- */}
                    {/* Identity */}
                    {/* -------------------------------- */}

                    <div className="profile-identity">

                        <h1>
                            {profile.display_name ||
                                "Unknown User"}
                        </h1>

                        <p className="profile-username">
                            @{profile.username}
                        </p>

                    </div>


                    {/* -------------------------------- */}
                    {/* Follow Button */}
                    {/* -------------------------------- */}

                    {!isSelf && (

                        <div className="profile-follow-section">

                            <button
                                className={
                                    isFollowing
                                        ? "unfollow-button"
                                        : "follow-button"
                                }
                                onClick={handleFollowToggle}
                                disabled={followLoading}
                            >

                                {followLoading
                                    ? "Loading..."
                                    : isFollowing
                                        ? "Following"
                                        : "Follow"}

                            </button>


                            {followError && (

                                <div className="profile-follow-error">

                                    {followError}

                                </div>

                            )}

                        </div>

                    )}


                    {/* -------------------------------- */}
                    {/* Bio */}
                    {/* -------------------------------- */}

                    <div className="profile-bio">

                        {profile.bio ? (

                            <p>
                                {profile.bio}
                            </p>

                        ) : (

                            <p className="profile-no-bio">
                                No bio yet.
                            </p>

                        )}

                    </div>


                    {/* -------------------------------- */}
                    {/* Statistics */}
                    {/* -------------------------------- */}

                    <div className="profile-stats">

                        <div className="profile-stat">

                            <strong>
                                {followersCount}
                            </strong>

                            <span>
                                Followers
                            </span>

                        </div>


                        <div className="profile-stat">

                            <strong>
                                {followingCount}
                            </strong>

                            <span>
                                Following
                            </span>

                        </div>

                    </div>


                    {/* -------------------------------- */}
                    {/* Account Information */}
                    {/* -------------------------------- */}

                    <div className="profile-info">

                        <p>

                            <strong>
                                Joined:
                            </strong>{" "}

                            {profile.account_created_at
                                ? new Date(
                                    profile.account_created_at
                                ).toLocaleDateString()
                                : "Unknown"}

                        </p>

                    </div>

                </section>

            </main>

        </div>
    );
}


export default Profile;