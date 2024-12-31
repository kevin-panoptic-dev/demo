import styles from "./form.module.css";
import { useErrorContext } from "../../components/context/error";
import { useNavigate } from "react-router-dom";
import api from "../../utilities/api/api";
import { LOGIN_PATH } from "../../utilities/constants";
import LoadingIndicator from "../loading/loading";
import { useState, FormEvent } from "react";
import { REFRESH_TOKEN, ACCESS_TOKEN } from "../../utilities/api/constants";

interface LoginFormType {
    firstField: [string, React.Dispatch<React.SetStateAction<string>>];
    secondField: [string, React.Dispatch<React.SetStateAction<string>>];
    placeholders: [string, string];
}

function LoginForm({
    firstField: [firstValue, setFirstValue],
    secondField: [secondValue, setSecondValue],
    placeholders: [type1, type2],
}: LoginFormType) {
    const navigate = useNavigate();
    const toErrorPage = () => navigate("/error");
    const { updateErrorMessage } = useErrorContext();
    const [isLoading, setIsLoading] = useState(false);
    const [showInvalid, setShowInvalid] = useState(false);
    const [countDown, setCountDown] = useState(3);

    const getInputType = (type: string) => {
        switch (type) {
            case "password":
                return "password";
            case "email":
                return "email";
            case "username":
                return "text";
            default:
                updateErrorMessage(
                    `Invalid input value ${type}, must be password, username, or email.`
                );
                toErrorPage();
                return "";
        }
    };
    const inputTypes: string[] = [];
    inputTypes.push(getInputType(type1));
    inputTypes.push(getInputType(type2));

    const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        try {
            setIsLoading(true);
            const response = await api.post(LOGIN_PATH, { type1: firstValue, type2: secondValue });
            if (response.status === 200) {
                localStorage.setItem(ACCESS_TOKEN, response.data.access);
                localStorage.setItem(REFRESH_TOKEN, response.data.refresh);

                // do something later
            } else if (response.status === 401) {
                setCountDown((previous) => previous - 1);
                setFirstValue("");
                setSecondValue("");
                if (!countDown) {
                    updateErrorMessage("f;Too many invalid inputs.");
                    toErrorPage();
                }
                if (!showInvalid) {
                    setShowInvalid(true);
                }
            } else {
                updateErrorMessage(`b;${response.status} error: ${response.data.detail}`);
                toErrorPage();
            }
        } catch (error) {
            if (error instanceof Error) {
                updateErrorMessage(`f;${error.message}`);
            } else {
                updateErrorMessage(`f;caught error ${error} is not an instance of Error.`);
            }
            toErrorPage();
        } finally {
            setIsLoading(false);
        }
    };

    if (isLoading) {
        return <LoadingIndicator message={"you are almost logged in..."}></LoadingIndicator>;
    } else {
        return (
            <div className={styles.container}>
                <form onSubmit={(e) => e.preventDefault()}>
                    <input
                        type={inputTypes[0]}
                        value={firstValue}
                        onChange={(e) => setFirstValue(e.target.value)}
                        placeholder={type1}
                        className={styles.inputBox}
                    />
                    <input
                        type={inputTypes[1]}
                        value={secondValue}
                        onChange={(e) => setSecondValue(e.target.value)}
                        placeholder={type2}
                        className={styles.inputBox}
                    />
                </form>
                {showInvalid && (
                    <p className={styles.warning}>
                        Invalid authentication credential, you have {countDown} attempts left.
                    </p>
                )}
            </div>
        );
    }
}

export default LoginForm;
