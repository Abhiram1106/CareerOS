"use client";
import { useRef } from "react";
import { useInView } from "motion/react";
import CountUp from "react-countup";

interface Props {
  end: number;
  prefix?: string;
  suffix?: string;
  decimals?: number;
  duration?: number;
  className?: string;
}

export function AnimatedCounter({
  end,
  prefix = "",
  suffix = "",
  decimals = 0,
  duration = 2.2,
  className,
}: Props) {
  const ref = useRef<HTMLSpanElement>(null);
  const isInView = useInView(ref, { once: true, margin: "-80px" });

  return (
    <span ref={ref} className={className}>
      {isInView ? (
        <CountUp
          start={0}
          end={end}
          prefix={prefix}
          suffix={suffix}
          decimals={decimals}
          duration={duration}
          useEasing
          easingFn={(t, b, c, d) => c * (1 - Math.pow(1 - t / d, 4)) + b}
        />
      ) : (
        <span aria-hidden="true">
          {prefix}0{suffix}
        </span>
      )}
    </span>
  );
}
