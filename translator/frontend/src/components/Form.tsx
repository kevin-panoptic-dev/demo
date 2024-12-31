import { useState, FormEvent } from "react";
import { api } from "../api/api";
import { useNavigate, Link } from "react-router-dom";
import { useErrorContext } from "../contexts/ErrorContext";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../api/constants";
import { Loading } from "./Loading";
import "../css/form.css";

interface formType {
    route: string;
    method: string;
}

function Form({ route, method }: formType) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const type = method === "login" ? "Login" : "Register";
    const navigate = useNavigate();
    const context = useErrorContext();
    if (!context) {
        throw new Error("context === null");
    }
    const { displayError } = context;

    const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        try {
            setLoading(true);
            const response = await api.post(route, { username, password });
            if (type === "Login") {
                localStorage.setItem(ACCESS_TOKEN, response.data.access);
                localStorage.setItem(REFRESH_TOKEN, response.data.response);
                console.log("redirect to translate page");
                navigate("/translate");
            } else {
                console.log("redirect to login");
                navigate("/login");
            }
        } catch (error) {
            displayError(`api ${error}`);
            navigate("/error");
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return <Loading></Loading>;
    } else {
        return (
            <>
                <form onSubmit={(e) => handleSubmit(e)} className="form-container">
                    <h2>{type}</h2>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        placeholder="username"
                        className="form-input"
                    />
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="password"
                        className="form-input"
                    />
                    {type === "Register" && (
                        <h5 className="form-thank">Thank You for Choosing Us</h5>
                    )}
                    <button type="submit" className="form-button">
                        {type}
                    </button>
                    <div>
                        {type === "Login" && (
                            <>
                                <p className="form-link">New to here? Click to </p>
                                <Link to="/register" className="form-link">
                                    register
                                </Link>
                            </>
                        )}
                        {type === "Register" && (
                            <>
                                <p className="form-link">Already have an account? Click to </p>
                                <Link to="/login" className="form-link">
                                    login
                                </Link>
                            </>
                        )}
                    </div>
                </form>
            </>
        );
    }
}

export { Form };
