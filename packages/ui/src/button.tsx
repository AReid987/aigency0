"use client";

import { ReactNode } from "react";

interface ButtonProps {
  children: ReactNode;
  className?: string;
  appName: string;
}

/**
 * Renders a customizable button component
 * @param {Object} props - The component props
 * @param {ReactNode} props.children - The content to be displayed inside the button
 * @param {string} props.className - Additional CSS classes to be applied to the button
 * @param {string} props.appName - The name of the app to be displayed in the alert message
 * @returns {JSX.Element} A button element with the specified properties
 */
export const Button = ({ children, className, appName }: ButtonProps) => {
  return (
    <button
      className={className}
      /**
       * Handles the click event and displays an alert with a greeting message.
       * @param {void} - This function doesn't take any parameters.
       * @returns {void} This function doesn't return a value.
       */
      onClick={() => alert(`Hello from your ${appName} app!`)}
    >
      {children}
    </button>
  );
};
