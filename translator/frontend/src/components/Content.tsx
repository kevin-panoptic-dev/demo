import React, { useEffect, useState, useRef } from "react";
import "../css/content.css";

interface childrenProps {
    children: React.ReactNode;
}

function FadeDivision({ children }: childrenProps) {
    const [isVisible, setIsVisible] = useState<boolean>(false);
    const ref = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const observer = new IntersectionObserver(
            ([entry]) => {
                if (entry.isIntersecting) {
                    setIsVisible(true);
                    observer.unobserve(entry.target);
                }
            },
            { threshold: 0.1 }
        );

        if (ref.current) {
            observer.observe(ref.current);
        }

        return () => {
            observer.disconnect();
        };
    }, []);

    return (
        <div className={`fade-division ${isVisible ? "visible" : ""}`} ref={ref}>
            {children}
        </div>
    );
}

export { FadeDivision };
