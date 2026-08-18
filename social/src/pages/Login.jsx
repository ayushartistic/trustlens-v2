// import { useState } from "react";
// import { supabase } from "../lib/supabase";
// import { Link, useNavigate } from "react-router-dom";

// function Login() {
//     const navigate = useNavigate();
//     const [form, setForm] = useState({
//         email: "",
//         password: "",
//     });

//     const [loading, setLoading] = useState(false);
//     const [error, setError] = useState("");

//     function handleChange(event) {
//         const { name, value } = event.target;

//         setForm((previous) => ({
//             ...previous,
//             [name]: value,
//         }));
//     }

//     async function handleSubmit(event) {
//         event.preventDefault();

//         setLoading(true);
//         setError("");

//         try {
//             const { error: loginError } =
//                 await supabase.auth.signInWithPassword({
//                     email: form.email,
//                     password: form.password,
//                 });

//             if (loginError) {
//                 throw loginError;
//             }

//             // window.location.href = "/";
//             navigate("/", { replace: true });
//         } catch (err) {
//             setError(err.message);
//         } finally {
//             setLoading(false);
//         }
//     }

//     return (
//         <div>
//             <h1>Login to TrustLens</h1>

//             <form onSubmit={handleSubmit}>
//                 <div>
//                     <label>Email</label>

//                     <input
//                         type="email"
//                         name="email"
//                         value={form.email}
//                         onChange={handleChange}
//                         required
//                     />
//                 </div>

//                 <div>
//                     <label>Password</label>

//                     <input
//                         type="password"
//                         name="password"
//                         value={form.password}
//                         onChange={handleChange}
//                         required
//                     />
//                 </div>

//                 <button type="submit" disabled={loading}>
//                     {loading ? "Logging in..." : "Login"}
//                 </button>
//             </form>

//             {error && <p>{error}</p>}
//             {/* <p>
//     Don't have an account?{" "}
//     <a href="/register">Create one</a>
// </p> */}
//     <p>
//     Don't have an account?{" "}
//     <Link to="/register">Create one</Link>
// </p>
//         </div>
//     );
// }

// export default Login;

import { useState } from "react";
import { supabase } from "../lib/supabase";
import { Link, useNavigate } from "react-router-dom";

function Login() {
    const navigate = useNavigate();

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

            navigate("/", { replace: true });
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="auth-page">

            <div className="auth-card">

                {/* Brand */}

                <div className="auth-brand">
                    TrustLens
                </div>


                {/* Heading */}

                <div className="auth-heading">

                    <h1>
                        Welcome back
                    </h1>

                    <p>
                        Sign in to continue to TrustLens Social.
                    </p>

                </div>


                {/* Login Form */}

                <form
                    className="auth-form"
                    onSubmit={handleSubmit}
                >

                    <div className="form-field">

                        <label htmlFor="login-email">
                            Email
                        </label>

                        <input
                            id="login-email"
                            type="email"
                            name="email"
                            value={form.email}
                            onChange={handleChange}
                            placeholder="you@example.com"
                            autoComplete="email"
                            required
                        />

                    </div>


                    <div className="form-field">

                        <label htmlFor="login-password">
                            Password
                        </label>

                        <input
                            id="login-password"
                            type="password"
                            name="password"
                            value={form.password}
                            onChange={handleChange}
                            placeholder="Enter your password"
                            autoComplete="current-password"
                            required
                        />

                    </div>


                    <button
                        className="auth-submit"
                        type="submit"
                        disabled={loading}
                    >
                        {loading
                            ? "Logging in..."
                            : "Login"}
                    </button>

                </form>


                {/* Error */}

                {error && (

                    <div className="auth-error">
                        {error}
                    </div>

                )}


                {/* Registration Link */}

                <p className="auth-switch">

                    Don't have an account?{" "}

                    <Link to="/register">
                        Create one
                    </Link>

                </p>

            </div>

        </div>
    );
}

export default Login;