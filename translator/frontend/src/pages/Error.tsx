import { useErrorContext } from "../contexts/ErrorContext";
import "../css/error.css";

function ShowError() {
    const context = useErrorContext();
    if (context === null) {
        throw new Error("Context === null");
    }
    const { error }: { error: string } = context;
    if (!error) {
        // default error page, assume nobody is intended to open /error page.
        return (
            <div className="error-container">
                <p className="error-content">
                    404 Error: URL not found, please use navbar to redirect to other pages.
                </p>
            </div>
        );
    } else {
        if (error.toLowerCase().startsWith("api")) {
            return (
                <div className="error-container">
                    <p className="error-content">API Error: {error}</p>
                </div>
            );
        } else {
            return (
                <div className="error-container">
                    <p className="error-content">System Error: {error}</p>
                </div>
            );
        }
    }
}

export { ShowError };
