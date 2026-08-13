import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { supabase } from "../lib/supabase";

function Home() {
    const { user } = useAuth();
    const navigate = useNavigate();

    async function handleLogout() {
        const { error } = await supabase.auth.signOut();

        if (error) {
            console.error("Logout failed:", error.message);
            return;
        }

        navigate("/login", { replace: true });
    }

    return (
        <div>
            <h1>TrustLens Social</h1>

            <p>
                Logged in as: {user?.email}
            </p>

            <button onClick={handleLogout}>
                Logout
            </button>

            <p>
                Social media home page coming next.
            </p>
        </div>
    );
}

export default Home;