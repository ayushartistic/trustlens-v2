import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Home from "./pages/Home";

import ProtectedRoute from "./components/ProtectedRoute";
import PublicRoute from "./components/PublicRoute";
import { AuthProvider } from "./context/AuthContext";

function App() {
    return (
        <AuthProvider>
            <BrowserRouter>
                <Routes>
                    <Route
                        path="/login"
                        element={
                            <PublicRoute>
                                <Login />
                            </PublicRoute>
                        }
                    />

                    <Route
                        path="/register"
                        element={
                            <PublicRoute>
                                <Register />
                            </PublicRoute>
                        }
                    />

                    <Route
                        path="/"
                        element={
                            <ProtectedRoute>
                                <Home />
                            </ProtectedRoute>
                        }
                    />

                    <Route
                        path="*"
                        element={<Navigate to="/" replace />}
                    />
                </Routes>
            </BrowserRouter>
        </AuthProvider>
    );
}

export default App;