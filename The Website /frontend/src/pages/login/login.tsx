import styles from "./login.module.css";
import api from "../../utilities/api/api";
import { LOGIN_PATH } from "../../utilities/constants";
import LoadingIndicator from "../loading/loading";
import { useState } from "react";
import LoginOnly from "../../components/authentication/login-checker";

function Login() {
    const [loading, setLoading] = useState(false);
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [email, setEmail] = useState("");
    const loginUser = async () => await api.post(LOGIN_PATH);

    if (loading) {
        return <LoadingIndicator message="you are almost logged in..."></LoadingIndicator>;
    } else {
        return;
    }
}

export default Login;
