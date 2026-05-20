"use client";
import { useRef, useState } from "react";
import { m } from "motion/react";
import type { ReactNode } from "react";

interface Props {
  children: ReactNode;
  className?: string;
  maxTilt?: number;
  scale?: number;
}

export function TiltCard({
  children,
  className = "",
  maxTilt = 10,
  scale = 1.02,
}: Props) {
  const ref = useRef<HTMLDivElement>(null);
  const [rotateX, setRotateX] = useState(0);
  const [rotateY, setRotateY] = useState(0);
  const [isHovered, setIsHovered] = useState(false);

  function handleMouseMove(e: React.MouseEvent<HTMLDivElement>) {
    if (!ref.current) return;
    const rect = ref.current.getBoundingClientRect();
    const x = (e.clientX - rect.left) / rect.width;
    const y = (e.clientY - rect.top)  / rect.height;
    setRotateX((y - 0.5) * -maxTilt * 2);
    setRotateY((x - 0.5) *  maxTilt * 2);
  }

  function handleMouseLeave() {
    setIsHovered(false);
    setRotateX(0);
    setRotateY(0);
  }

  return (
    <m.div
      ref={ref}
      className={`bento-card tilt-root ${className}`}
      animate={{ rotateX, rotateY, scale: isHovered ? scale : 1 }}
      transition={{ type: "spring", stiffness: 280, damping: 26, mass: 0.6 }}
      onMouseMove={handleMouseMove}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={handleMouseLeave}
    >
      <div className="bento-card-inner">{children}</div>
    </m.div>
  );
}
