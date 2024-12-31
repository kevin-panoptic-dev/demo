import "../css/privacy.css";
import { useState } from "react";
import { FadeDivision } from "../components/Content";
import { Link } from "react-router-dom";

function Privacy() {
    const [personalDataFlag, setPersonalDataFlag] = useState(false);
    const [privacyRightFlag, setPrivacyRightFlag] = useState(false);
    const [dataCollectedFlag, setDataCollectedFlag] = useState(false);
    const [useOfDataFlag, setUseOfDataFlag] = useState(false);
    const [questionsFlag, setQuestionsFlag] = useState(false);

    return (
        <div className="wrapper">
            <div className="content-container">
                <FadeDivision>
                    <h1 className="heading-first">Our Privacy Policy</h1>
                </FadeDivision>
                <FadeDivision>
                    <h3 className="heading-second">Updated December 19, 2024</h3>
                </FadeDivision>
                <FadeDivision>
                    <p className="paragraph-third">
                        This privacy policy article describes how we collect, use, and share your
                        personal data.
                    </p>
                </FadeDivision>
                <FadeDivision>
                    <p className="paragraph-third">
                        In addition to this Privacy Policy, we provide data and privacy information
                        embedded in our products and certain features that ask to use your personal
                        data. This product-specific information is accompanied by our Data & Privacy
                        Icon.
                    </p>
                </FadeDivision>
                <FadeDivision>
                    <img className="image-forth" src="src/assets/privacy-icon.png" />
                </FadeDivision>
                <FadeDivision>
                    <p className="paragraph-third">
                        You will be given an opportunity to review this product-specific information
                        before using these features. You also can view this information at any time,
                        either in settings related to those features and/or online.
                    </p>
                </FadeDivision>
                <FadeDivision>
                    <p className="paragraph-third">
                        You can familiarize yourself with our privacy practices, accessible via the
                        headings below, and{" "}
                        <a href="mailto:inundatio.anonymus@gmail.com" className="contact-link">
                            contact us
                        </a>{" "}
                        if you have any questions.
                    </p>
                </FadeDivision>
            </div>

            {/* Personal Data */}
            <div className="article-division">
                <div className="boxes-container">
                    <FadeDivision>
                        <div className="divider-container">
                            <hr className="divider" />
                        </div>
                    </FadeDivision>
                    <FadeDivision>
                        <div className="header-container">
                            <h2
                                className="heading-fifth"
                                onClick={() => setPersonalDataFlag(!personalDataFlag)}
                            >
                                What's Personal Data?
                            </h2>
                            <div className="icon-container">
                                <img
                                    className={`click-icon ${personalDataFlag ? "onSelect" : ""}`}
                                    src="src/assets/plus-icon.png"
                                    onClick={() => setPersonalDataFlag(!personalDataFlag)}
                                />
                            </div>
                        </div>
                    </FadeDivision>
                    <FadeDivision>
                        <p className={`box-paragraph ${personalDataFlag ? "show" : "hide"}`}>
                            We believe strongly in fundamental privacy rights — and that those
                            fundamental rights should not differ depending on where you live in the
                            world.{" "}
                            <span className="paragraph-span">
                                That's why we treat any data that relates to an identified or
                                identifiable individual or that is linked or linkable to them as
                                “personal data,” no matter where the individual lives.
                            </span>{" "}
                            This means that data that directly identifies you — such as your name —
                            is personal data, and also data that does not directly identify you, but
                            that can reasonably be used to identify you — such as the serial number
                            of your device — is personal data.
                        </p>
                        <p className={`box-paragraph ${personalDataFlag ? "show" : "hide"}`}>
                            <span className="paragraph-span">
                                We will NOT collect any form of personal data.
                            </span>{" "}
                            You don't need provide any personal data in order to access any of our
                            services. But we still encourage you to read their privacy policies and
                            know your privacy rights before interacting with them.
                        </p>
                    </FadeDivision>
                </div>
            </div>

            {/* Privacy Rights */}
            <div className="article-division">
                <div className="boxes-container">
                    <FadeDivision>
                        <div className="divider-container">
                            <hr className="divider" />
                        </div>
                    </FadeDivision>
                    <FadeDivision>
                        <div className="header-container">
                            <h2
                                className="heading-fifth"
                                onClick={() => setPrivacyRightFlag(!privacyRightFlag)}
                            >
                                Privacy Rights
                            </h2>
                            <div className="icon-container">
                                <img
                                    className={`click-icon ${privacyRightFlag ? "onSelect" : ""}`}
                                    src="src/assets/plus-icon.png"
                                    onClick={() => setPrivacyRightFlag(!privacyRightFlag)}
                                />
                            </div>
                        </div>
                    </FadeDivision>
                    <FadeDivision>
                        <p className={`box-paragraph ${privacyRightFlag ? "show" : "hide"}`}>
                            We respect your ability to know, access, correct, transfer, restrict the
                            processing of, and delete your personal data. You can delete{" "}
                            <span className="paragraph-span">ANY</span> data we collect in any
                            condition at any time, and you can process these all by yourself without
                            sending any request. Visit{" "}
                            <Link to="/history" className="paragraph-link">
                                this history page
                            </Link>{" "}
                            to see more details.
                        </p>
                        <p className={`box-paragraph ${privacyRightFlag ? "show" : "hide"}`}>
                            In this page, you can see all the history data we collected, and you can
                            delete them all in a few clicks. You also have the right to prevent any
                            data tracking by default.
                        </p>
                    </FadeDivision>
                </div>
            </div>

            {/* Data Collected */}
            <div className="article-division">
                <div className="boxes-container">
                    <FadeDivision>
                        <div className="divider-container">
                            <hr className="divider" />
                        </div>
                    </FadeDivision>
                    <FadeDivision>
                        <div className="header-container">
                            <h2
                                className="heading-fifth"
                                onClick={() => setDataCollectedFlag(!dataCollectedFlag)}
                            >
                                Data Collected
                            </h2>
                            <div className="icon-container">
                                <img
                                    className={`click-icon ${dataCollectedFlag ? "onSelect" : ""}`}
                                    src="src/assets/plus-icon.png"
                                    onClick={() => setDataCollectedFlag(!dataCollectedFlag)}
                                />
                            </div>
                        </div>
                    </FadeDivision>
                    <FadeDivision>
                        <p className={`box-paragraph ${dataCollectedFlag ? "show" : "hide"}`}>
                            We believe that you can have{" "}
                            <span className="paragraph-span">great products</span> and{" "}
                            <span className="paragraph-span">great privacy</span> at the{" "}
                            <span className="paragraph-span">same</span> time. This means that we
                            strive to collect only the necessary data that we need. We only collect
                            your previous translation history, in order to infer the preferences of
                            the language and provide a better translation experience.
                        </p>
                        <p className={`box-paragraph ${dataCollectedFlag ? "show" : "hide"}`}>
                            This mean that you can always view your previous translation history,
                            without the need of re-translating them again. We also use the type of
                            language you select to infer the new translation language.
                        </p>
                    </FadeDivision>
                </div>
            </div>

            {/* Use of Data */}
            <div className="article-division">
                <div className="boxes-container">
                    <FadeDivision>
                        <div className="divider-container">
                            <hr className="divider" />
                        </div>
                    </FadeDivision>
                    <FadeDivision>
                        <div className="header-container">
                            <h2
                                className="heading-fifth"
                                onClick={() => setUseOfDataFlag(!useOfDataFlag)}
                            >
                                Use of Data
                            </h2>
                            <div className="icon-container">
                                <img
                                    className={`click-icon ${useOfDataFlag ? "onSelect" : ""}`}
                                    src="src/assets/plus-icon.png"
                                    onClick={() => setUseOfDataFlag(!setUseOfDataFlag)}
                                />
                            </div>
                        </div>
                    </FadeDivision>
                    <FadeDivision>
                        <p className={`box-paragraph ${useOfDataFlag ? "show" : "hide"}`}>
                            We will <span className="paragraph-span">NOT</span> share any data with
                            third parties; we will <span className="paragraph-span">NOT</span> use
                            any data for commercial purposes; and we will{" "}
                            <span className="paragraph-span">NOT</span> use any data for any other
                            purposes than providing a better translation experience.
                        </p>
                        <p className={`box-paragraph ${useOfDataFlag ? "show" : "hide"}`}>
                            We encourage developers to supervise our execute of our privacy policy,
                            visiting our{" "}
                            <a
                                href="https://github.com/kevin-panoptic-dev/translator"
                                className="paragraph-link"
                            >
                                github repository
                            </a>{" "}
                            to see more detail.
                        </p>
                    </FadeDivision>
                </div>
            </div>

            {/* Questions */}
            <div className="article-division">
                <div className="boxes-container">
                    <FadeDivision>
                        <div className="divider-container">
                            <hr className="divider" />
                        </div>
                    </FadeDivision>
                    <FadeDivision>
                        <div className="header-container">
                            <h2
                                className="heading-fifth"
                                onClick={() => setQuestionsFlag(!questionsFlag)}
                            >
                                Questions
                            </h2>
                            <div className="icon-container">
                                <img
                                    className={`click-icon ${questionsFlag ? "onSelect" : ""}`}
                                    src="src/assets/plus-icon.png"
                                    onClick={() => setQuestionsFlag(!questionsFlag)}
                                />
                            </div>
                        </div>
                    </FadeDivision>
                    <FadeDivision>
                        <p className={`box-paragraph ${questionsFlag ? "show" : "hide"}`}>
                            If you have any questions, please contact use though{" "}
                            <a
                                href="mailto:inundatio.anonymus@gmail.com"
                                className="paragraph-link"
                            >
                                this email
                            </a>
                            .
                        </p>
                        <p className={`box-paragraph ${questionsFlag ? "show" : "hide"}`}>
                            We take your privacy questions seriously. A dedicated team reviews your
                            inquiry to determine how best to respond to your question or concern,
                            including those inquiries received in response to an access or download
                            request. In most cases, all substantive contacts receive a response
                            within three hours. In other cases, we may require additional
                            information or let you know that we need more time to respond.
                        </p>
                        <p className={`box-paragraph ${questionsFlag ? "show" : "hide"}`}>
                            Where your complaint indicates an improvement could be made in our
                            handling of privacy issues, we will take steps to make such an update at
                            the next reasonable opportunity. In the event that a privacy issue has
                            resulted in a negative impact on you or another person, we will take
                            steps to address that with you or that other person.
                        </p>
                        <p className={`box-paragraph ${questionsFlag ? "show" : "hide"}`}>
                            You may at any time — including if you are not satisfied with Apple's
                            response — refer your complaint to the applicable regulator. If you ask
                            us, we will endeavor to provide you with information about relevant
                            complaint avenues which may be applicable to your circumstances.
                        </p>
                    </FadeDivision>
                </div>
            </div>
        </div>
    );
}

export { Privacy };
