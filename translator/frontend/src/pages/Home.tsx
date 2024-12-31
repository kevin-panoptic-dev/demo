import { useNavigate } from "react-router-dom";
import React from "react";
import { useState, useEffect } from "react";
import { FadeDivision } from "../components/Content";
import "../css/home.css";
import "../css/content.css";

const descriptions: string[] = [
    "Intuitive design prioritizes clarity, making translation tasks straightforward for all users, regardless of technical expertise.",
    "Streamlined interface combines functionality with simplicity, enhancing the translation experience from start to finish.",
    "Effortless navigation ensures users quickly access translation tools without confusion, delivering a seamless, user-friendly interface.",
    "Modern layout fosters quick understanding, enabling users to translate content with minimal effort.",
    "Responsive design adapts smoothly across devices, ensuring a consistent experience everywhere.",
    "Key features are strategically placed for easy access, reducing time spent on translation tasks.",
    "Clear, concise prompts guide users through translations without unnecessary complexity.",
    "Efficient tools are tailored for real-time translations, boosting productivity with ease.",
    "Intelligently structured workflows remove barriers, making translations quicker and more intuitive.",
    "Seamlessly integrates AI tools for enhanced translation accuracy, adapting context and tone effortlessly.",
    "AI-powered suggestions streamline workflows, ensuring polished, professional translations every time.",
    "Real-time AI assistance improves productivity, delivering faster, smarter translation results.",
    "Cutting-edge AI features enhance user confidence, offering reliable, contextually accurate translations at the click of a button.",
    "Clean layout ensures content is logically arranged, simplifying the translation process.",
    "Clearly defined sections guide users through tools and features effortlessly.",
    "Structured organization minimizes clutter, enhancing focus and usability.",
    "Information hierarchy ensures key functions are always within reach.",
    "Consistent formatting creates a visually harmonious, user-friendly experience.",
    "Well-grouped tools promote efficiency, allowing users to complete tasks quickly.",
    "Logical flow of content eliminates confusion, making translations straightforward.",
    "Thoughtful arrangement of features enhances accessibility for all skill levels.",
    "The built-in writing assistant refines content, ensuring translations are polished and professional.",
    "AI-enhanced writing assistant adapts tone and style to suit diverse translation needs.",
    "Real-time feedback from the writing assistant improves clarity and linguistic accuracy effortlessly.",
    "Open-source foundation fosters transparency, empowering users to understand and customize the platform.",
    "Community-driven development ensures constant improvements and innovative features.",
    "Accessible source code allows seamless integration with other tools and systems.",
    "Flexible licensing encourages contributions, enhancing collaboration across diverse user bases.",
    "Open-source design supports adaptability, catering to a wide range of use cases.",
    "Developers can personalize features, tailoring the platform to specific needs.",
    "Transparent code ensures reliability, with a global community maintaining quality and security.",
    "Community support makes troubleshooting and feature requests efficient and user-centric.",
    "Open-source approach fosters inclusivity, welcoming developers worldwide to innovate and contribute.",
];

function Home() {
    // constants
    const criticalValue = 20;
    const zoomSpeed = 0.14;
    const navigate = useNavigate();
    const redirect = (location: string): void => {
        navigate(`/${location}`);
    };
    const [zoomLevel, setZoomLevel] = useState<number>(1);
    const [secondaryFix, setSecondaryFix] = useState<boolean>(true);
    const scrollFix = () => {
        window.scrollTo({
            top: 0,
            left: 0,
            behavior: "smooth",
        });
    };

    // effects
    useEffect(() => {
        const handleScroll = (event: globalThis.WheelEvent) => {
            if (event.deltaY > 0) {
                setZoomLevel((prev) => Math.min(prev + zoomSpeed, criticalValue));
            } else {
                if (zoomLevel < criticalValue * 0.9) {
                    setZoomLevel((prev) => Math.max(prev - zoomSpeed, 1));
                } else {
                    null;
                }
            }
        };

        window.addEventListener("wheel", handleScroll);

        return () => {
            window.removeEventListener("wheel", handleScroll);
        };
    }, [zoomLevel]);

    if (zoomLevel < 20) {
        scrollFix();
        if (!secondaryFix) {
            setSecondaryFix(true);
        }
        return (
            <div
                className="home"
                style={{ transform: `scale(${zoomLevel})`, transformOrigin: "center" }}
            >
                <div className="icon-division">
                    <img src="src/assets/translate-icon.png" className="translate-icon" />
                </div>

                <h1 className="home-title">Aloy's Translator</h1>
                <p className="home-description">free, open-source AI translation</p>
                <button
                    type="submit"
                    onClick={() => {
                        redirect("ai-translate");
                    }}
                    className="home-button"
                >
                    Try
                </button>
                <div className="arrow-division">
                    <img src="src/assets/arrow.png" className="arrow" />
                </div>
            </div>
        );
    } else {
        if (secondaryFix) {
            scrollFix();
            setSecondaryFix(false);
        }
        return (
            <div className="content">
                <FadeDivision>
                    <div className="first-content">
                        <h1>
                            Make Translation Even <span className="first-span">Easier</span>!
                        </h1>
                        <p className="first-title">
                            Smooth, <span className="first-span">Intuitive</span> User Experience
                        </p>
                        <button
                            type="button"
                            className="content-button"
                            onClick={() => {
                                redirect("translate");
                            }}
                        >
                            try
                        </button>
                        <div className="first-description">
                            {descriptions.slice(0, 9).map((text, index) => (
                                <p className="first-words" key={index}>
                                    {text}
                                </p>
                            ))}
                        </div>
                    </div>
                </FadeDivision>
                <FadeDivision>
                    <div className="second-content">
                        <p className="second-title">
                            Integrate <span className="second-span">AI</span> Smoother than a Straw
                        </p>
                        <button
                            type="button"
                            className="content-button"
                            onClick={() => {
                                redirect("ai-translate");
                            }}
                        >
                            try
                        </button>
                        <div className="second-description">
                            {descriptions.slice(9, 13).map((text, index) => (
                                <p className="second-words" key={index}>
                                    {text}
                                </p>
                            ))}
                        </div>
                    </div>
                </FadeDivision>
                <FadeDivision>
                    <div className="third-content">
                        <p className="third-title">
                            <span className="third-span">Organized</span> Content, Professional and
                            User-Friendly
                        </p>
                        <button
                            type="button"
                            className="content-button"
                            onClick={() => {
                                redirect("translate");
                            }}
                        >
                            try
                        </button>
                        <div className="third-description">
                            {descriptions.slice(13, 21).map((text, index) => (
                                <p className="third-words" key={index}>
                                    {text}
                                </p>
                            ))}
                        </div>
                    </div>
                </FadeDivision>

                <FadeDivision>
                    <div className="forth-content">
                        <p className="forth-title">
                            Writing Assistant, <span className="forth-span">10x</span> Your
                            Productivity
                        </p>
                        <button
                            type="button"
                            className="content-button"
                            onClick={() => {
                                redirect("ai-writing");
                            }}
                        >
                            try
                        </button>
                        <div className="forth-description">
                            {descriptions.slice(21, 24).map((text, index) => (
                                <p className="forth-words" key={index}>
                                    {text}
                                </p>
                            ))}
                        </div>
                    </div>
                </FadeDivision>

                <FadeDivision>
                    <div className="fifth-content">
                        <p className="fifth-title">
                            Open Source, Reliable and <span className="fifth-span">Free</span> to
                            Use
                        </p>
                        <button
                            type="button"
                            className="content-button"
                            onClick={() => {
                                redirect("login");
                            }}
                        >
                            support us
                        </button>
                        <div className="fifth-description">
                            {descriptions.slice(21, 30).map((text, index) => (
                                <p className="fifth-words" key={index}>
                                    {text}
                                </p>
                            ))}
                        </div>
                    </div>
                </FadeDivision>

                <FadeDivision>
                    <div className="sixth-content">
                        <h2>...</h2>
                    </div>
                </FadeDivision>
            </div>
        );
    }
}

export { Home };
