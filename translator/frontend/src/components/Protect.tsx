import { jwtDecode } from "jwt-decode";
import { api } from "../api/api";
import { useState, useEffect, ReactNode } from "react";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../api/constants";
import { useNavigate, Navigate } from "react-router-dom";
import { useErrorContext } from "../contexts/ErrorContext";
import { Loading } from "./Loading";

interface childrenType {
    children: ReactNode;
}

function Protect({ children }: childrenType) {
    const [isAuthorized, setIsAuthorized] = useState<null | boolean>(null);
    const context = useErrorContext();
    if (!context) {
        throw new Error("context === null");
    }
    const { displayError } = context;
    const navigate = useNavigate();

    useEffect(() => {
        auth().catch((error) => {
            setIsAuthorized(false);
            displayError(`api ${error}`);
            navigate("/error");
        });
    }, []);

    const refresh = async () => {
        const refreshToken = localStorage.getItem(REFRESH_TOKEN);
        try {
            const response = await api.post("api/token/refresh/", { refresh: refreshToken });
            if (response.status === 200) {
                localStorage.setItem(ACCESS_TOKEN, response.data.access);
                setIsAuthorized(true);
            } else {
                setIsAuthorized(false);
            }
        } catch (error) {
            setIsAuthorized(false);
        }
    };

    const auth = async () => {
        const token = localStorage.getItem(ACCESS_TOKEN);

        if (!token) {
            setIsAuthorized(false);
            return;
        }
        const decodedToken = jwtDecode(token);
        const tokenExpiration = decodedToken.exp;
        const now = Date.now() / 1000;

        if (tokenExpiration) {
            if (tokenExpiration < now) {
                await refresh();
            } else {
                setIsAuthorized(true);
            }
        } else {
            displayError(`api invalid token expiration date ${tokenExpiration}`);
            navigate("/error");
        }
    };
    if (isAuthorized === null) {
        return <Loading />;
    }
    return isAuthorized ? children : <Navigate to="/login"></Navigate>;
}

export { Protect };
