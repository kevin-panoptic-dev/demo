import { Link } from "react-router-dom";
import "../css/navbar.css";

function Navbar() {
    return (
        <nav className="navbar">
            <div className="navbar-brand">
                <Link to="/" className="navbar-brand">
                    Home
                </Link>
            </div>
            <div className="navbar-links">
                <Link to="/translate" className="nav-links">
                    Translate
                </Link>
                <Link to="/ai-translate" className="nav-links">
                    AI Translate
                </Link>
                <Link to="/writing" className="nav-links">
                    AI writing
                </Link>
                <Link to="/login" className="nav-links">
                    login
                </Link>
                <Link to="/register" className="nav-links">
                    register
                </Link>
                <Link to="/privacy" className="nav-links">
                    privacy
                </Link>
            </div>
        </nav>
    );
}

export { Navbar };
