"use client";
import { useRef } from "react";
import { m, useInView, type Variants } from "motion/react";

interface Props {
  text: string;
  delay?: number;
  className?: string;
  as?: "h1" | "h2" | "h3" | "p" | "span";
}

// cubic-bezier typed as const tuple to satisfy Motion's Easing type
const EASE = [0.16, 1, 0.3, 1] as [number, number, number, number];

const wordVariants: Variants = {
  hidden: { opacity: 0, y: 18, clipPath: "inset(0 0 100% 0)" },
  visible: (i: number) => ({
    opacity: 1,
    y: 0,
    clipPath: "inset(0 0 0% 0)",
    transition: { duration: 0.55, delay: i * 0.07, ease: EASE },
  }),
};

export function TextReveal({ text, delay = 0, className, as: Tag = "span" }: Props) {
  const ref = useRef<HTMLElement>(null);
  const isInView = useInView(ref, { once: true, margin: "-60px" });
  const words = text.split(" ");

  return (
    <Tag
      // @ts-expect-error ref polymorphism across element tags
      ref={ref}
      className={`word-reveal-wrapper ${className ?? ""}`}
      aria-label={text}
    >
      {words.map((word, i) => (
        <m.span
          key={`${word}-${i}`}
          custom={i + delay / 0.07}
          variants={wordVariants}
          initial="hidden"
          animate={isInView ? "visible" : "hidden"}
          style={{ display: "inline-block" }}
        >
          {word}
        </m.span>
      ))}
    </Tag>
  );
}
