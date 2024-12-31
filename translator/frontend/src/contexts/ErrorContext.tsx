import { useContext, createContext, useState, ReactNode } from "react";

interface childrenType {
    children: ReactNode;
}

interface errorContextType {
    error: string;
    displayError: (message: string) => void;
}

const ErrorContext = createContext<errorContextType | undefined>(undefined);

function useErrorContext() {
    return useContext(ErrorContext);
}

function ErrorProvider({ children }: childrenType) {
    const [error, setError] = useState<string>("");

    const displayError = (message: string) => {
        setError(message);
    };

    const value: errorContextType = { error, displayError };

    return <ErrorContext.Provider value={value}>{children}</ErrorContext.Provider>;
}

export { useErrorContext };
export { ErrorProvider };
