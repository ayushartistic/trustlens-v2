// import { useState } from "react";
// import { supabase } from "../lib/supabase";
// import { Link } from "react-router-dom";

// function Register() {
//     const [form, setForm] = useState({
//         username: "",
//         displayName: "",
//         email: "",
//         password: "",
//     });

//     const [loading, setLoading] = useState(false);
//     const [message, setMessage] = useState("");
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
//         setMessage("");
//         setError("");

//         try {
// const {
//     data: { user },
//     error: signUpError,
// } = await supabase.auth.signUp({
//     email: form.email,
//     password: form.password,
//     options: {
//         data: {
//             username: form.username,
//             display_name: form.displayName,
//         },
//     },
// });

//             if (signUpError) {
//                 throw signUpError;
//             }

//             if (!user) {
//                 throw new Error("Registration failed.");
//             }

//             // const { error: profileError } = await supabase
//             //     .from("users")
//             //     .insert({
//             //         auth_user_id: user.id,
//             //         username: form.username,
//             //         display_name: form.displayName,
//             //     });

//             // if (profileError) {
//             //     throw profileError;
//             // }

//             setMessage(
//                 "Registration successful. Your TrustLens account has been created."
//             );

//             setForm({
//                 username: "",
//                 displayName: "",
//                 email: "",
//                 password: "",
//             });
//         } catch (err) {
//             setError(err.message);
//         } finally {
//             setLoading(false);
//         }
//     }

//     return (
//         <div>
//             <h1>Create TrustLens Account</h1>

//             <form onSubmit={handleSubmit}>
//                 <div>
//                     <label>Username</label>
//                     <input
//                         type="text"
//                         name="username"
//                         value={form.username}
//                         onChange={handleChange}
//                         required
//                     />
//                 </div>

//                 <div>
//                     <label>Display Name</label>
//                     <input
//                         type="text"
//                         name="displayName"
//                         value={form.displayName}
//                         onChange={handleChange}
//                         required
//                     />
//                 </div>

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
//                         minLength={6}
//                     />
//                 </div>

//                 <button type="submit" disabled={loading}>
//                     {loading ? "Creating account..." : "Register"}
//                 </button>
//             </form>

//             {message && <p>{message}</p>}
//             {error && <p>{error}</p>}
//             {/* <p>
//     Already have an account?{" "}
//     <a href="/login">Login</a>
// </p> */}
//     <p>
//     Already have an account?{" "}
//     <Link to="/login">Login</Link>
// </p>
//         </div>
//     );
// }

// export default Register;

import { useState } from "react";
import { supabase } from "../lib/supabase";
import { Link } from "react-router-dom";

function Register() {
    const [form, setForm] = useState({
        username: "",
        displayName: "",
        email: "",
        password: "",
    });

    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState("");
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
        setMessage("");
        setError("");

        try {
            const {
                data: { user },
                error: signUpError,
            } = await supabase.auth.signUp({
                email: form.email,
                password: form.password,
                options: {
                    data: {
                        username: form.username,
                        display_name: form.displayName,
                    },
                },
            });

            if (signUpError) {
                throw signUpError;
            }

            if (!user) {
                throw new Error("Registration failed.");
            }

            setMessage(
                "Registration successful. Your TrustLens account has been created."
            );

            setForm({
                username: "",
                displayName: "",
                email: "",
                password: "",
            });
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="auth-page">

            <div className="auth-card auth-card-register">

                {/* Brand */}

                <div className="auth-brand">
                    TrustLens
                </div>


                {/* Heading */}

                <div className="auth-heading">

                    <h1>
                        Create your account
                    </h1>

                    <p>
                        Join the TrustLens social environment.
                    </p>

                </div>


                {/* Registration Form */}

                <form
                    className="auth-form"
                    onSubmit={handleSubmit}
                >

                    <div className="form-field">

                        <label htmlFor="register-username">
                            Username
                        </label>

                        <input
                            id="register-username"
                            type="text"
                            name="username"
                            value={form.username}
                            onChange={handleChange}
                            placeholder="Choose a username"
                            autoComplete="username"
                            required
                        />

                    </div>


                    <div className="form-field">

                        <label htmlFor="register-display-name">
                            Display Name
                        </label>

                        <input
                            id="register-display-name"
                            type="text"
                            name="displayName"
                            value={form.displayName}
                            onChange={handleChange}
                            placeholder="Your name"
                            autoComplete="name"
                            required
                        />

                    </div>


                    <div className="form-field">

                        <label htmlFor="register-email">
                            Email
                        </label>

                        <input
                            id="register-email"
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

                        <label htmlFor="register-password">
                            Password
                        </label>

                        <input
                            id="register-password"
                            type="password"
                            name="password"
                            value={form.password}
                            onChange={handleChange}
                            placeholder="Create a password"
                            autoComplete="new-password"
                            minLength={6}
                            required
                        />

                        <span className="form-hint">
                            Minimum 6 characters
                        </span>

                    </div>


                    <button
                        className="auth-submit"
                        type="submit"
                        disabled={loading}
                    >
                        {loading
                            ? "Creating account..."
                            : "Create account"}
                    </button>

                </form>


                {/* Success Message */}

                {message && (

                    <div className="auth-success">
                        {message}
                    </div>

                )}


                {/* Error Message */}

                {error && (

                    <div className="auth-error">
                        {error}
                    </div>

                )}


                {/* Login Link */}

                <p className="auth-switch">

                    Already have an account?{" "}

                    <Link to="/login">
                        Login
                    </Link>

                </p>

            </div>

        </div>
    );
}

export default Register;