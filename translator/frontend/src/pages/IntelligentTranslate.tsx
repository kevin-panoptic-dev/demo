import { useState, useEffect } from "react";
import { useErrorContext } from "../contexts/ErrorContext";
import { useNavigate } from "react-router-dom";
import { Loading } from "../components/Loading";
import { VALID_CHECK_PROMPT, TRANSLATE_PROMPT } from "../api/constants";
import { callGeminiApi } from "../utility/callGeminiApi";
import "../css/test.css";

interface IntelligentTranslateType {
    route: string;
}
function IntelligentTranslate({ route }: IntelligentTranslateType) {
    /* `Step` is a number flag that represents the current step of translation.
        0: do nothing stage
        1: validate check stage
        2: translation stage
        3: change the return value into displayable format stage
    */
    const [step, setStep] = useState<number>(0);
    const [loading, setLoading] = useState(false);
    const [response, setResponse] = useState<string>("");
    const [userInput, setUserInput] = useState("");
    const [originLanguage, setOriginLanguage] = useState<string>("");
    const [correspondingLanguage, setCorrespondingLanguage] = useState<string>("");
    const context = useErrorContext();
    const navigate = useNavigate();

    if (!context) {
        throw new Error("context === undefined");
    }
    const { displayError } = context;

    useEffect(() => {
        const asyncall = async () => {
            try {
                setLoading(true);
                let result;
                if (step === 1) {
                    result = await updateState(
                        VALID_CHECK_PROMPT,
                        userInput,
                        `language: ${originLanguage}`,
                        "validate"
                    );
                    if (result) {
                        console.log("success in the first step");
                        setStep(2);
                    }
                } else if (step === 2) {
                    result = await updateState(
                        TRANSLATE_PROMPT,
                        userInput,
                        `Translate from ${originLanguage} to ${correspondingLanguage}`,
                        "translate"
                    );
                    if (result) {
                        console.log("success in the second step");
                        setStep(3);
                    }
                } else if (step === 3) {
                    return;
                }
            } catch (error) {
                console.log(error);
                displayError("API An unknown error occurred, view console to see more detail");
            } finally {
                setLoading(false);
            }
        };
        asyncall();
    }, [step]);

    const updateState = async (
        prompt: string,
        message: string,
        languageMessage: string,
        type: string
    ) => {
        const result: true | undefined = await callGeminiApi(
            route,
            message,
            prompt,
            languageMessage,
            type,
            displayError,
            navigate,
            setResponse
        );
        return !result ? false : true;
    };

    if (loading) return <Loading></Loading>;
    else if (step === 3)
        return (
            <>
                <h1 className="test">{response}</h1>
                <h1 className="test">{response}</h1>
                <h1 className="test">{response}</h1>
                <h1 className="test">{response}</h1>
                <h1 className="test">{response}</h1>
                <h1 className="test">{response}</h1>
                <h1 className="test">{response}</h1>
            </>
        );
    else {
        return (
            <div>
                <form
                    onSubmit={(e) => {
                        e.preventDefault();
                        setStep(1);
                    }}
                >
                    <h2>Hello, Bugs</h2>
                    <input
                        type="text"
                        value={originLanguage}
                        placeholder="original language here"
                        onChange={(e) => setOriginLanguage(e.target.value)}
                    />
                    <input
                        type="text"
                        value={correspondingLanguage}
                        placeholder="target language here"
                        onChange={(e) => setCorrespondingLanguage(e.target.value)}
                    />
                    <input
                        type="text"
                        value={userInput}
                        placeholder="type something here"
                        onChange={(e) => setUserInput(e.target.value)}
                    />
                    <button type="submit">Start Debug</button>
                </form>
            </div>
        );
    }
}

export { IntelligentTranslate };
