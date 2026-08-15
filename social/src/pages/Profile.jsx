import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import {
    getUser,
    getFollowers,
    getFollowing
} from "../api";


function Profile() {

    const { userId } = useParams();
    const navigate = useNavigate();

    const [profile, setProfile] = useState(null);

    const [followersCount, setFollowersCount] = useState(0);
    const [followingCount, setFollowingCount] = useState(0);

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);


    async function loadProfile() {

        try {

            setLoading(true);
            setError(null);

            // ------------------------------------------
            // Load the actual profile
            // ------------------------------------------

            const profileData = await getUser(userId);

            setProfile(profileData);


            // ------------------------------------------
            // Load followers/following independently
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


    useEffect(() => {

        loadProfile();

    }, [userId]);


    // ----------------------------------------------
    // Loading state
    // ----------------------------------------------

    if (loading) {

        return (
            <div className="profile-page">

                <div className="profile-state">
                    Loading profile...
                </div>

            </div>
        );
    }


    // ----------------------------------------------
    // Profile loading error
    // ----------------------------------------------

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


    // ----------------------------------------------
    // No profile
    // ----------------------------------------------

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


    // ----------------------------------------------
    // Profile UI
    // ----------------------------------------------

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