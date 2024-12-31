import { api } from "../api/api";

interface geminiResponseType {
    data: {
        error: string;
        error_message: string | null;
        response: string | null;
    };
}

async function callGeminiApi(
    route: string,
    prompt: string,
    message: string,
    language_message: string,
    type: string,
    displayError: (error: string) => void,
    navigate: (path: string) => void,
    setResponse: (response: string) => void
) {
    try {
        const response: geminiResponseType = await api.post(route, {
            message,
            prompt,
            language_message,
            type,
        });

        if (response.data.error === "1") {
            // has error
            if (response.data.error_message === null) {
                throw new Error(
                    "response have an error with no message, could be a bug in backend return part."
                );
            }
            throw new Error(response.data.error_message);
        } else {
            if (response.data.response === null) {
                throw new Error(
                    "response doesn't have an error but with a null response, could be a bug in backend return part"
                );
            }
            // console.warn("The message is coming!");
            // console.log(`response = ${JSON.stringify(response.data.response.trim())}`);
            setResponse(JSON.stringify(response.data.response.trim()));
            return true;
        }
    } catch (error) {
        displayError(`api ${error}`);
        navigate("/error");
    }
}

export { callGeminiApi };
