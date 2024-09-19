```
/**
 * Renders a code element with optional className
 * @param {Object} props - The component props
 * @param {React.ReactNode} props.children - The content to be wrapped in the code element
 * @param {string} [props.className] - Optional CSS class name for styling the code element
 * @returns {JSX.Element} A JSX element representing the code snippet
 */
```
export function Code({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}): JSX.Element {
  return <code className={className}>{children}</code>;
}
