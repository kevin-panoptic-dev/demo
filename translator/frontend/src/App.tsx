import { Navbar } from "./navbar/Navbar";
import { Routes, Route } from "react-router-dom";
import { ErrorProvider } from "./contexts/ErrorContext";
import { ShowError } from "./pages/Error";
import { Home } from "./pages/Home";
import { Protect } from "./components/Protect";
import { Login } from "./pages/Login";
import { Translate } from "./pages/Translate";
import { Register } from "./pages/Register";
import "./css/app.css";
import { Navigate } from "react-router-dom";
import { Privacy } from "./pages/Privacy";
import { IntelligentTranslate } from "./pages/IntelligentTranslate";

function Logout() {
    localStorage.clear();
    return <Navigate to="/login"></Navigate>;
}

function RegisterAndLogout() {
    localStorage.clear();
    return <Register></Register>;
}
function App() {
    return (
        <ErrorProvider>
            <Navbar></Navbar>
            <main className="main-content">
                <Routes>
                    <Route
                        path="/translate"
                        element={
                            <Protect>
                                <Translate></Translate>
                            </Protect>
                        }
                    ></Route>
                    <Route
                        path="/ai-translate"
                        element={
                            <Protect>
                                <IntelligentTranslate route="/service/request/"></IntelligentTranslate>
                            </Protect>
                        }
                    ></Route>
                    <Route path="/login" element={<Login></Login>}></Route>
                    <Route
                        path="/register"
                        element={<RegisterAndLogout></RegisterAndLogout>}
                    ></Route>
                    <Route path="/" element={<Home></Home>}></Route>
                    <Route path="/privacy" element={<Privacy></Privacy>}></Route>
                    <Route path="/logout" element={<Logout></Logout>}></Route>
                    <Route path="/error" element={<ShowError></ShowError>}></Route>
                    <Route path="*" element={<ShowError></ShowError>}></Route>
                </Routes>
            </main>
        </ErrorProvider>
    );
}

export { App };
