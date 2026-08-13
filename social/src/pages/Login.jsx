import { useState } from "react";
import { supabase } from "../lib/supabase";
import { Link } from "react-router-dom";

function Login() {
    const [form, setForm] = useState({
        email: "",
        password: "",
    });

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    function handleChange(event) {
        const { name, value } = event.target;

        setForm((previous) => ({
            ...previous,
            [name]: value,
        }));
    }

    async function handleSubmit(event) {
        event.preventDefault();

        setLoading(true);
        setError("");

        try {
            const { error: loginError } =
                await supabase.auth.signInWithPassword({
                    email: form.email,
                    password: form.password,
                });

            if (loginError) {
                throw loginError;
            }

            window.location.href = "/";
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }

    return (
        <div>
            <h1>Login to TrustLens</h1>

            <form onSubmit={handleSubmit}>
                <div>
                    <label>Email</label>

                    <input
                        type="email"
                        name="email"
                        value={form.email}
                        onChange={handleChange}
                        required
                    />
                </div>

                <div>
                    <label>Password</label>

                    <input
                        type="password"
                        name="password"
                        value={form.password}
                        onChange={handleChange}
                        required
                    />
                </div>

                <button type="submit" disabled={loading}>
                    {loading ? "Logging in..." : "Login"}
                </button>
            </form>

            {error && <p>{error}</p>}
            {/* <p>
    Don't have an account?{" "}
    <a href="/register">Create one</a>
</p> */}
    <p>
    Don't have an account?{" "}
    <Link to="/register">Create one</Link>
</p>
        </div>
    );
}

export default Login;